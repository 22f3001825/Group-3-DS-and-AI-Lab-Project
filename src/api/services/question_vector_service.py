"""Qdrant synchronisation for database-backed question intelligence.

The outbox is durable in SQLite; failure here never rolls back or invalidates the
authoritative relational state. Calling ``sync_outbox`` again is safe.

Two entity types drain through one loop:

  question_unit  → a point in `mlt_question_units` (this module owns that collection)
  course_chunk   → chunks appended to, or deleted from, the live `mlt_course_bot`
                   collection through the same vector-store singleton the chat path uses

The second exists so that an admin commit is exactly one database transaction. Writing
chunks inline would mean a Qdrant outage either failed the request after the relational
work had been decided, or committed relational state describing chunks that are not
there. Queued instead, an outage leaves visible, retryable work.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

import numpy as np
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


def _unit_vector(unit: QuestionUnit | None) -> list[float] | None:
    """The stored embedding, or None when it is absent or the wrong dimension.

    Read from the unit rather than from the outbox payload, so a synced row does not
    keep a second copy of every embedding and a re-queue needs no embedding run.
    """
    if unit is None or not unit.vector:
        return None
    values = np.frombuffer(unit.vector, dtype=np.float32)
    if values.size != VECTOR_SIZE:
        return None
    return values.astype(float).tolist()


# ── Course chunks (the live retrieval collection) ─────────────────────────────

def _vector_store() -> Any:
    from ..dependencies import _build_vector_store  # noqa: PLC0415

    return _build_vector_store()


def _apply_course_chunk(row: QuestionBankOutbox, vector_store: Any) -> None:
    from langchain_core.documents import Document  # noqa: PLC0415
    from qdrant_client import models as qmodels  # noqa: PLC0415

    payload = row.payload or {}
    if row.operation == "delete":
        doc_ids = list(payload.get("doc_ids") or [])
        if not doc_ids:
            return
        vector_store.client.delete(
            collection_name=vector_store.collection_name,
            points_selector=qmodels.FilterSelector(
                filter=qmodels.Filter(must=[qmodels.FieldCondition(
                    key="metadata.doc_id", match=qmodels.MatchAny(any=doc_ids),
                )])
            ),
        )
        return

    chunks = payload.get("chunks") or []
    if not chunks:
        return
    # NEVER ingest_to_qdrant.main(): that deletes and recreates the collection. This
    # appends through the singleton the chat path already retrieves from.
    vector_store.add_documents([
        Document(page_content=c.get("page_content", ""), metadata=c.get("metadata", {}))
        for c in chunks
    ])


# ── Drain ─────────────────────────────────────────────────────────────────────

def _fail(row: QuestionBankOutbox, exc: BaseException) -> None:
    row.status = "failed"
    row.retry_count += 1
    row.last_error = f"{type(exc).__name__}: {exc}"


def sync_outbox(db: Session, limit: int = 100, client: Any | None = None,
                vector_store: Any | None = None) -> dict[str, int]:
    """Synchronise pending operations and retain failures for a later retry.

    Each backend is built lazily and only when a row needing it is present, so a queue
    of one kind never pays for the other's connection — and a failure to reach one
    backend does not fail the rows destined for the other.
    """
    from qdrant_client import models  # noqa: PLC0415

    rows = (db.query(QuestionBankOutbox)
            .filter(QuestionBankOutbox.status.in_(("pending", "failed")))
            .order_by(QuestionBankOutbox.created_at).limit(limit).all())
    result = {"synced": 0, "failed": 0, "pending": len(rows)}
    if not rows:
        _refresh_version_status(db)
        db.commit()
        return result

    backends: dict[str, Any] = {"question_unit": client, "course_chunk": vector_store}
    errors: dict[str, BaseException] = {}

    def backend_for(kind: str) -> Any:
        """Connect once per kind per drain; remember a failure instead of retrying it."""
        if kind in errors:
            raise errors[kind]
        if backends.get(kind) is None:
            try:
                backends[kind] = ensure_collection() if kind == "question_unit" else _vector_store()
            except Exception as exc:  # noqa: BLE001
                errors[kind] = exc
                raise
        return backends[kind]

    for row in rows:
        try:
            backend = backend_for(row.entity_type or "question_unit")
            row.status = "processing"
            db.flush()
            if row.entity_type == "course_chunk":
                _apply_course_chunk(row, backend)
            elif row.operation == "delete":
                backend.delete(QUESTION_COLLECTION,
                               points_selector=models.PointIdsList(points=[_point_id(row.unit_id)]))
            elif row.operation == "upsert":
                unit = db.get(QuestionUnit, row.unit_id)
                vector = _unit_vector(unit)
                if vector is None:
                    raise ValueError("unit vector is missing or has the wrong dimension")
                backend.upsert(QUESTION_COLLECTION, points=[models.PointStruct(
                    id=_point_id(row.unit_id), vector=vector, payload=dict(row.payload or {}),
                )])
                unit.vector_status = "synced"
            else:
                raise ValueError(f"unknown outbox operation '{row.operation}'")
            row.status = "synced"
            row.processed_at = _now()
            row.last_error = None
            result["synced"] += 1
        except Exception as exc:  # noqa: BLE001
            _fail(row, exc)
            result["failed"] += 1

    _refresh_version_status(db)
    db.commit()
    return result


def _refresh_version_status(db: Session) -> None:
    from . import question_repository as repo  # noqa: PLC0415

    try:
        repo.refresh_version_vector_status(db)
    except Exception:  # noqa: BLE001 — status is reporting, never a reason to fail a drain
        pass
