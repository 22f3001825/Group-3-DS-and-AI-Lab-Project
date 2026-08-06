"""Qdrant synchronisation for database-backed question units.

The outbox is durable in SQLite; failure here never rolls back or invalidates the
authoritative relational question bank. Calling ``sync_outbox`` again is safe.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from ...database.models import QuestionBankOutbox, QuestionUnit
from ..dependencies import _normalize_url

QUESTION_COLLECTION = "mlt_question_units"
VECTOR_SIZE = 384


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _point_id(unit_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"mlt-question-unit:{unit_id}"))


def _client() -> Any:
    from qdrant_client import QdrantClient  # noqa: PLC0415

    url = _normalize_url(os.getenv("QDRANT_URL", ""))
    if not url:
        raise RuntimeError("QDRANT_URL is not set; question vectors remain queued.")
    return QdrantClient(url=url, api_key=os.getenv("QDRANT_API_KEY"))


def ensure_collection(client: Any | None = None) -> Any:
    from qdrant_client import models  # noqa: PLC0415

    client = client or _client()
    if not client.collection_exists(QUESTION_COLLECTION):
        client.create_collection(
            collection_name=QUESTION_COLLECTION,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
    # Repeating a payload-index creation is accepted by Qdrant, so this is idempotent.
    for field, schema in (
        ("unit_id", models.PayloadSchemaType.KEYWORD),
        ("bank_version_id", models.PayloadSchemaType.KEYWORD),
        ("cluster_id", models.PayloadSchemaType.KEYWORD),
        ("duplicate_group_id", models.PayloadSchemaType.KEYWORD),
        ("source_type", models.PayloadSchemaType.KEYWORD),
        ("week", models.PayloadSchemaType.INTEGER),
        ("origin", models.PayloadSchemaType.KEYWORD),
    ):
        client.create_payload_index(QUESTION_COLLECTION, field_name=field, field_schema=schema)
    return client


def sync_outbox(db: Session, limit: int = 100, client: Any | None = None) -> dict[str, int]:
    """Synchronise pending operations and retain failures for a later retry."""
    from qdrant_client import models  # noqa: PLC0415

    rows = (db.query(QuestionBankOutbox)
            .filter(QuestionBankOutbox.status.in_(("pending", "failed")))
            .order_by(QuestionBankOutbox.created_at).limit(limit).all())
    result = {"synced": 0, "failed": 0, "pending": len(rows)}
    if not rows:
        return result
    try:
        client = ensure_collection(client)
    except Exception as exc:  # retain all operations for recovery
        for row in rows:
            row.status = "failed"
            row.retry_count += 1
            row.last_error = f"{type(exc).__name__}: {exc}"
        db.commit()
        result["failed"] = len(rows)
        return result

    for row in rows:
        try:
            row.status = "processing"
            db.flush()
            if row.operation == "delete":
                client.delete(QUESTION_COLLECTION, points_selector=models.PointIdsList(points=[_point_id(row.unit_id)]))
            elif row.operation == "upsert":
                payload = dict(row.payload or {})
                vector = payload.pop("vector", None)
                if not vector or len(vector) != VECTOR_SIZE:
                    raise ValueError("outbox vector is missing or has the wrong dimension")
                client.upsert(QUESTION_COLLECTION, points=[models.PointStruct(
                    id=_point_id(row.unit_id), vector=vector, payload=payload,
                )])
                unit = db.get(QuestionUnit, row.unit_id)
                if unit:
                    unit.vector_status = "synced"
            else:
                raise ValueError(f"unknown outbox operation '{row.operation}'")
            row.status = "synced"
            row.processed_at = _now()
            row.last_error = None
            result["synced"] += 1
        except Exception as exc:  # noqa: BLE001
            row.status = "failed"
            row.retry_count += 1
            row.last_error = f"{type(exc).__name__}: {exc}"
            result["failed"] += 1
    db.commit()
    return result
