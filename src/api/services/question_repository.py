"""Database repository for AI Question Intelligence.

SQLite/PostgreSQL owns the question graph.  Qdrant is synchronised by the outbox but
is deliberately not queried for relationship data: a vector-store outage must not
erase a student's ability to browse already-classified questions.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ...database.models import (
    ClusterMember, ConceptCluster, DuplicateGroup, QuestionBankOutbox,
    QuestionBankVersion, QuestionUnit, QuestionUnitChunk,
)


def _public_id(value: Optional[str]) -> Optional[str]:
    return value.split(":", 1)[1] if value and ":" in value else value


def _stored_cluster_id(version: QuestionBankVersion, cluster_id: str | int) -> str:
    return f"{version.version_id}:{cluster_id}"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def active_version(db: Session) -> Optional[QuestionBankVersion]:
    return (db.query(QuestionBankVersion)
            .filter(QuestionBankVersion.status == "active")
            .order_by(QuestionBankVersion.completed_at.desc(), QuestionBankVersion.created_at.desc())
            .first())


def require_active_version(db: Session) -> QuestionBankVersion:
    version = active_version(db)
    if not version:
        raise LookupError("Question bank not built. Run: python src/migrate_question_bank_to_db.py")
    return version


def _unit(row: QuestionUnit, doc_ids: Optional[list[str]] = None) -> dict[str, Any]:
    return {
        "unit_id": _public_id(row.unit_id),
        "source_type": row.source_type,
        "week": row.week,
        "title": row.title,
        "text": row.text,
        "options": row.options or [],
        "answer": row.answer or "",
        "solution": row.solution or "",
        "origin": row.origin,
        "is_canonical": bool(row.is_canonical),
        "dup_group_id": _public_id(row.duplicate_group_id),
        "cluster_id": int(_public_id(row.cluster_id)) if _public_id(row.cluster_id) and _public_id(row.cluster_id).isdigit() else _public_id(row.cluster_id),
        "chunk_doc_ids": doc_ids if doc_ids is not None else [],
    }


def _cluster_summary(db: Session, row: ConceptCluster) -> dict[str, Any]:
    units = db.query(QuestionUnit).filter(QuestionUnit.cluster_id == row.cluster_id).all()
    canonical = [u for u in units if u.is_canonical]
    return {
        "cluster_id": int(_public_id(row.cluster_id)) if _public_id(row.cluster_id).isdigit() else _public_id(row.cluster_id),
        "title": row.title,
        "canonical_count": len(canonical),
        "member_count": len(units),
        "weeks": sorted({u.week for u in units}),
        "sources": sorted({u.source_type for u in units}),
        "medoid_unit_id": row.medoid_unit_id,
    }


def stats(db: Session) -> dict[str, Any]:
    version = require_active_version(db)
    units = db.query(QuestionUnit).filter(QuestionUnit.bank_version_id == version.version_id).all()
    clusters = db.query(ConceptCluster).filter(ConceptCluster.bank_version_id == version.version_id).all()
    canonical_count = sum(1 for unit in units if unit.is_canonical)
    by_source: dict[str, dict[str, int]] = {}
    for source, count in Counter(unit.source_type for unit in units).items():
        source_units = [u for u in units if u.source_type == source]
        by_source[source] = {"units": count, "canonical": sum(1 for u in source_units if u.is_canonical)}
    cluster_sizes = Counter(unit.cluster_id for unit in units if unit.cluster_id)
    return {
        "unit_count": len(units),
        "canonical_count": canonical_count,
        "duplicate_count": len(units) - canonical_count,
        "duplicate_rate": (len(units) - canonical_count) / len(units) if units else 0.0,
        "cluster_count": len(clusters),
        "singleton_clusters": sum(1 for size in cluster_sizes.values() if size == 1),
        "largest_member_count": max(cluster_sizes.values(), default=0),
        "admin_authored_units": sum(1 for unit in units if unit.origin == "admin"),
        "by_source": by_source,
        "thresholds": version.thresholds or {},
        "generated_from": version.embedding_model,
    }


def list_clusters(db: Session, week: Optional[int], source_type: Optional[str],
                  min_member_count: int, limit: int) -> list[dict[str, Any]]:
    version = require_active_version(db)
    rows = db.query(ConceptCluster).filter(ConceptCluster.bank_version_id == version.version_id).all()
    result = []
    for row in rows:
        value = _cluster_summary(db, row)
        if value["member_count"] < min_member_count:
            continue
        if week is not None and week not in value["weeks"]:
            continue
        if source_type and source_type not in value["sources"]:
            continue
        result.append(value)
    return sorted(result, key=lambda c: (-c["member_count"], -c["canonical_count"]))[:limit]


def get_cluster(db: Session, cluster_id: str | int) -> Optional[dict[str, Any]]:
    version = require_active_version(db)
    row = (db.query(ConceptCluster)
           .filter(ConceptCluster.bank_version_id == version.version_id,
                   ConceptCluster.cluster_id == _stored_cluster_id(version, cluster_id)).first())
    if not row:
        return None
    value = _cluster_summary(db, row)
    units = (db.query(QuestionUnit).filter(QuestionUnit.cluster_id == row.cluster_id)
             .order_by(QuestionUnit.is_canonical.desc(), QuestionUnit.unit_id).all())
    doc_map: dict[str, list[str]] = {}
    if units:
        for link in db.query(QuestionUnitChunk).filter(QuestionUnitChunk.unit_id.in_([u.unit_id for u in units])):
            doc_map.setdefault(link.unit_id, []).append(link.doc_id)
    value["members"] = [_unit(unit, doc_map.get(unit.unit_id, [])) for unit in units]
    return value


def common_doubts(db: Session, min_size: int, limit: int) -> list[dict[str, Any]]:
    clusters = list_clusters(db, None, None, min_size, 10_000)
    return sorted(clusters, key=lambda c: (-c["member_count"], -len(c["sources"]), -c["canonical_count"]))[:limit]


def related_to_doc_ids(db: Session, doc_ids: list[str], limit: int) -> list[dict[str, Any]]:
    require_active_version(db)
    if not doc_ids:
        return []
    seed_rows = (db.query(QuestionUnit).join(QuestionUnitChunk)
                 .filter(QuestionUnitChunk.doc_id.in_(doc_ids)).all())
    seed_ids = {row.unit_id for row in seed_rows}
    cluster_ids = {row.cluster_id for row in seed_rows if row.cluster_id}
    if not cluster_ids:
        return []
    groups = Counter(row.duplicate_group_id for row in db.query(QuestionUnit)
                     .filter(QuestionUnit.duplicate_group_id.isnot(None)).all())
    candidates = (db.query(QuestionUnit)
                  .filter(QuestionUnit.cluster_id.in_(cluster_ids), QuestionUnit.is_canonical.is_(True))
                  .order_by(QuestionUnit.cluster_id, QuestionUnit.unit_id).all())
    out = []
    for row in candidates:
        if row.unit_id in seed_ids:
            continue
        out.append({
            "unit_id": _public_id(row.unit_id),
            "cluster_id": int(_public_id(row.cluster_id)) if _public_id(row.cluster_id) and _public_id(row.cluster_id).isdigit() else _public_id(row.cluster_id),
            "title": row.title,
            "source_type": row.source_type,
            "week": row.week,
            "member_count": groups.get(row.duplicate_group_id, 1),
        })
        if len(out) >= limit:
            break
    return out


def canonical_doc_ids_to_drop(db: Session, doc_ids: list[str]) -> set[str]:
    if not active_version(db) or not doc_ids:
        return set()
    rows = (db.query(QuestionUnitChunk.doc_id, QuestionUnit.duplicate_group_id, QuestionUnit.is_canonical)
            .join(QuestionUnit, QuestionUnit.unit_id == QuestionUnitChunk.unit_id)
            .filter(QuestionUnitChunk.doc_id.in_(doc_ids)).all())
    grouped: dict[str, list[tuple[str, bool]]] = {}
    for doc_id, group_id, canonical in rows:
        if group_id:
            grouped.setdefault(group_id, []).append((doc_id, canonical))
    drop: set[str] = set()
    for members in grouped.values():
        canonical_docs = [doc for doc, canonical in members if canonical]
        keep = canonical_docs[0] if canonical_docs else members[0][0]
        drop.update(doc for doc, _ in members if doc != keep)
    return drop


def persist_bank(db: Session, bank: dict[str, Any], vectors: Any, *, status: str = "active") -> QuestionBankVersion:
    """Persist a fully built bank and queue its vectors atomically.

    The caller owns `db.commit()`. Existing active versions are kept for audit but marked
    superseded, making the active bank an explicit database fact rather than a filename.
    """
    for version in db.query(QuestionBankVersion).filter(QuestionBankVersion.status == "active"):
        version.status = "superseded"
    version = QuestionBankVersion(
        status=status,
        embedding_model=bank.get("embed_model", "BAAI/bge-small-en-v1.5"),
        thresholds=bank.get("thresholds", {}),
        source_summary=bank.get("stats", {}),
        completed_at=_now() if status == "active" else None,
    )
    db.add(version)
    db.flush()
    cluster_rows: dict[str, ConceptCluster] = {}
    for cluster in bank.get("clusters", []):
        key = str(cluster["cluster_id"])
        row = ConceptCluster(cluster_id=f"{version.version_id}:{key}", bank_version_id=version.version_id,
                             title=cluster.get("title", "Untitled cluster"),
                             medoid_unit_id=cluster.get("medoid_unit_id"))
        db.add(row)
        cluster_rows[key] = row
    db.flush()
    group_rows: dict[str, DuplicateGroup] = {}
    for unit in bank.get("units", []):
        group = str(unit.get("dup_group_id", unit["unit_id"]))
        if group not in group_rows:
            row = DuplicateGroup(duplicate_group_id=f"{version.version_id}:{group}", bank_version_id=version.version_id)
            db.add(row)
            group_rows[group] = row
    db.flush()
    for position, unit in enumerate(bank.get("units", [])):
        old_group = str(unit.get("dup_group_id", unit["unit_id"]))
        old_cluster = str(unit.get("cluster_id", ""))
        row = QuestionUnit(
            unit_id=f"{version.version_id}:{unit['unit_id']}", bank_version_id=version.version_id,
            source_type=unit["source_type"], source_file=unit.get("source_file", ""),
            doc_stem=unit["unit_id"].split("/", 1)[-1].split("#", 1)[0], week=int(unit.get("week", 0)),
            title=unit.get("title", ""), text=unit.get("text", ""), options=unit.get("options") or [],
            answer=unit.get("answer", ""), solution=unit.get("solution", ""), origin=unit.get("origin", "corpus"),
            is_canonical=bool(unit.get("is_canonical")), duplicate_group_id=group_rows[old_group].duplicate_group_id,
            cluster_id=cluster_rows[old_cluster].cluster_id if old_cluster in cluster_rows else None,
        )
        db.add(row)
        for doc_id in unit.get("chunk_doc_ids") or []:
            db.add(QuestionUnitChunk(unit_id=row.unit_id, doc_id=doc_id))
        vector = vectors[position].astype(float).tolist() if len(vectors) > position else []
        db.add(QuestionBankOutbox(operation="upsert", unit_id=row.unit_id, payload={
            "vector": vector, "unit_id": row.unit_id, "bank_version_id": version.version_id,
            "source_type": row.source_type, "week": row.week, "cluster_id": row.cluster_id,
            "duplicate_group_id": row.duplicate_group_id, "is_canonical": row.is_canonical, "origin": row.origin,
        }))
        if row.is_canonical:
            group_rows[old_group].canonical_unit_id = row.unit_id
        if row.cluster_id:
            db.add(ClusterMember(cluster_id=row.cluster_id, unit_id=row.unit_id, ordinal=position))
    return version
