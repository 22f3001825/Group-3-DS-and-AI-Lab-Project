"""Database repository for AI Question Intelligence.

SQLite/PostgreSQL owns the question graph.  Qdrant is synchronised by the outbox but
is deliberately not queried for relationship data: a vector-store outage must not
erase a student's ability to browse already-classified questions.

It also owns everything the feature *produces*: unit embeddings (`QuestionUnit.vector`),
admin-contributed content (`QuestionDocument`) and the pending Qdrant work that carries
both to the vector store. Nothing here reads or writes a file.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable, Optional

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ... import question_intelligence as qi
# Thresholds arrive as arguments (the service owns policy), but this one is definitional
# rather than tunable-per-call: it says what "asked" MEANS, and a caller that could pass
# a different set could make two endpoints disagree about the same cluster.
from ...config import QI_ASKED_SOURCE_TYPES
from ...database.models import (
    ClusterMember, ConceptCluster, DuplicateGroup, QuestionBankOutbox,
    QuestionBankVersion, QuestionDocument, QuestionUnit, QuestionUnitChunk,
)

VECTOR_DTYPE = np.float32


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
        # Members that represent somebody asking, as opposed to a scan boundary — this
        # is the number the "N asked" label and the common-doubts ranking use.
        "asked_count": sum(1 for u in units if u.source_type in QI_ASKED_SOURCE_TYPES),
        "weeks": sorted({u.week for u in units}),
        "sources": sorted({u.source_type for u in units}),
        "medoid_unit_id": row.medoid_unit_id,
    }


def stats(db: Session, min_member_count: int = 1,
          min_readability: float = 0.0) -> dict[str, Any]:
    version = require_active_version(db)
    units = db.query(QuestionUnit).filter(QuestionUnit.bank_version_id == version.version_id).all()
    clusters = db.query(ConceptCluster).filter(ConceptCluster.bank_version_id == version.version_id).all()
    canonical_count = sum(1 for unit in units if unit.is_canonical)
    by_source: dict[str, dict[str, int]] = {}
    for source, count in Counter(unit.source_type for unit in units).items():
        source_units = [u for u in units if u.source_type == source]
        by_source[source] = {"units": count, "canonical": sum(1 for u in source_units if u.is_canonical)}
    cluster_sizes = Counter(unit.cluster_id for unit in units if unit.cluster_id)
    cluster_asked = Counter(unit.cluster_id for unit in units
                            if unit.cluster_id and unit.source_type in QI_ASKED_SOURCE_TYPES)
    return {
        "unit_count": len(units),
        "canonical_count": canonical_count,
        "duplicate_count": len(units) - canonical_count,
        "duplicate_rate": (len(units) - canonical_count) / len(units) if units else 0.0,
        "cluster_count": len(clusters),
        # How many of those a student can actually browse, under the same rule
        # list_clusters applies. Shown alongside cluster_count, never instead of it —
        # the header stat and the list below it disagreed before this existed.
        "displayable_clusters": sum(
            1 for row in clusters
            if qi.is_displayable_cluster(
                {"title": row.title,
                 "member_count": cluster_sizes.get(row.cluster_id, 0),
                 "asked_count": cluster_asked.get(row.cluster_id, 0)},
                min_members=min_member_count, min_readability=min_readability)
        ),
        "singleton_clusters": sum(1 for size in cluster_sizes.values() if size == 1),
        "largest_member_count": max(cluster_sizes.values(), default=0),
        "admin_authored_units": sum(1 for unit in units if unit.origin == "admin"),
        "by_source": by_source,
        "thresholds": version.thresholds or {},
        "generated_from": version.embedding_model,
        "vector_status": effective_vector_status(db, version),
    }


def list_clusters(db: Session, week: Optional[int], source_type: Optional[str],
                  min_member_count: int, limit: int,
                  min_readability: float = 0.0) -> list[dict[str, Any]]:
    """Browsable clusters. `min_member_count` and `min_readability` are display gates —
    they hide nothing from `get_cluster`, search, or the quiz generator."""
    version = require_active_version(db)
    rows = db.query(ConceptCluster).filter(ConceptCluster.bank_version_id == version.version_id).all()
    result = []
    for row in rows:
        value = _cluster_summary(db, row)
        if not qi.is_displayable_cluster(value, min_members=min_member_count,
                                         min_readability=min_readability):
            continue
        if week is not None and week not in value["weeks"]:
            continue
        if source_type and source_type not in value["sources"]:
            continue
        result.append(value)
    # Asked first: a cluster three students asked about outranks a longer one assembled
    # from a single scan, which sorting on member_count alone got backwards.
    return sorted(result, key=lambda c: (-c["asked_count"], -c["member_count"],
                                         -c["canonical_count"]))[:limit]


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


def common_doubts(db: Session, min_size: int, limit: int,
                  min_readability: float = 0.0) -> list[dict[str, Any]]:
    """Ranked by `asked_count`, and gated on it too.

    `min_size` is applied to asked_count rather than member_count, which is what keeps a
    PYQ-only cluster out of "most-asked" entirely: its members are one scanned question
    split by the OCR, so it was asked once at most and has no claim on the ranking.
    """
    clusters = list_clusters(db, None, None, 1, 10_000, min_readability)
    ranked = [c for c in clusters if c["asked_count"] >= min_size]
    return sorted(ranked, key=lambda c: (-c["asked_count"], -len(c["sources"]),
                                         -c["canonical_count"]))[:limit]


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

    The version is active for *relational* reads the moment those rows commit — browsing
    clusters must not wait on, or be taken down by, a vector store. `vector_status`
    records whether Qdrant has caught up, and per-unit `vector_status` is what any
    similarity feature filters on.
    """
    for version in db.query(QuestionBankVersion).filter(QuestionBankVersion.status == "active"):
        version.status = "superseded"
    version = QuestionBankVersion(
        status=status,
        embedding_model=bank.get("embed_model", "BAAI/bge-small-en-v1.5"),
        thresholds=bank.get("thresholds", {}),
        source_summary=bank.get("stats", {}),
        vector_status="pending",
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
        row.text_hash = qi.unit_text_hash(unit)
        if len(vectors) > position:
            row.vector = np.asarray(vectors[position], dtype=VECTOR_DTYPE).tobytes()
        db.add(row)
        for doc_id in unit.get("chunk_doc_ids") or []:
            db.add(QuestionUnitChunk(unit_id=row.unit_id, doc_id=doc_id))
        # The payload carries the filterable facts only. The vector is read from the unit
        # at drain time, so a synced row does not keep a second copy of every embedding
        # and a re-sync needs no embedding run.
        db.add(QuestionBankOutbox(
            operation="upsert", entity_type="question_unit", unit_id=row.unit_id, payload={
                "unit_id": row.unit_id, "bank_version_id": version.version_id,
                "source_type": row.source_type, "week": row.week, "cluster_id": row.cluster_id,
                "duplicate_group_id": row.duplicate_group_id, "is_canonical": row.is_canonical,
                "origin": row.origin,
            }))
        if row.is_canonical:
            group_rows[old_group].canonical_unit_id = row.unit_id
        if row.cluster_id:
            db.add(ClusterMember(cluster_id=row.cluster_id, unit_id=row.unit_id, ordinal=position))
    return version


# ── Embedding cache ───────────────────────────────────────────────────────────

def cached_vectors(db: Session, units: list[dict], *, refresh: bool = False) -> np.ndarray:
    """Embed `units`, reusing vectors already stored for identical text.

    This replaces the `data/question_bank/unit_vectors.npy` cache. Keyed by
    `qi.unit_text_hash` — the embedding model plus the exact text embedded — so a
    rebuild that re-parses the same corpus embeds nothing, and an edited question
    embeds only itself.
    """
    if not units:
        return np.zeros((0, 384), dtype=VECTOR_DTYPE)

    hashes = [qi.unit_text_hash(unit) for unit in units]
    known: dict[str, np.ndarray] = {}
    if not refresh:
        # Chunked IN(): SQLite caps host parameters at 999 and a corpus rebuild asks
        # about every unit at once.
        unique = list(dict.fromkeys(hashes))
        for start in range(0, len(unique), 500):
            batch = unique[start:start + 500]
            for row in (db.query(QuestionUnit.text_hash, QuestionUnit.vector)
                        .filter(QuestionUnit.text_hash.in_(batch),
                                QuestionUnit.vector.isnot(None))):
                if row.text_hash not in known and row.vector:
                    known[row.text_hash] = np.frombuffer(row.vector, dtype=VECTOR_DTYPE)

    missing = [i for i, h in enumerate(hashes) if h not in known]
    if missing:
        fresh = qi.embed_units([units[i] for i in missing])
        for slot, index in enumerate(missing):
            known[hashes[index]] = np.asarray(fresh[slot], dtype=VECTOR_DTYPE)

    return np.vstack([known[h] for h in hashes]).astype(VECTOR_DTYPE)


def embedding_cache_stats(db: Session, units: list[dict]) -> dict[str, int]:
    """How much of a rebuild the cache would serve. Reporting only.

    Counts distinct texts, not units: two identical questions in different files share
    one embedding and are one cache entry.
    """
    unique = list({qi.unit_text_hash(unit) for unit in units})
    if not unique:
        return {"units": 0, "cached": 0, "to_embed": 0}
    cached = 0
    for start in range(0, len(unique), 500):
        cached += (db.query(func.count(func.distinct(QuestionUnit.text_hash)))
                   .filter(QuestionUnit.text_hash.in_(unique[start:start + 500]),
                           QuestionUnit.vector.isnot(None)).scalar() or 0)
    return {"units": len(units), "cached": cached, "to_embed": max(0, len(unique) - cached)}


# ── Admin-contributed documents ───────────────────────────────────────────────

def active_documents(db: Session) -> list[QuestionDocument]:
    return (db.query(QuestionDocument)
            .filter(QuestionDocument.status == "active")
            .order_by(QuestionDocument.stem).all())


def document_by_stem(db: Session, stem: str) -> Optional[QuestionDocument]:
    return (db.query(QuestionDocument)
            .filter(QuestionDocument.stem == stem,
                    QuestionDocument.status == "active").first())


def document_units_input(db: Session) -> list[dict[str, Any]]:
    """Rows shaped for `qi.parse_question_units(extra_documents=...)`."""
    return [{
        "markdown": row.markdown,
        "source_type": row.source_type,
        "stem": row.stem,
        "week": row.week,
        "source_file": f"{row.source_type}/{row.stem}.md",
    } for row in active_documents(db)]


def document_chunk_index(db: Session) -> list[dict[str, Any]]:
    """Chunk index entries for admin documents, in `qi.load_chunk_index()`'s shape.

    Admin chunks are in Qdrant but were never written to `data/splits/*.jsonl`, so the
    unit→chunk mapping would not see them. Re-splitting here is pure text work over the
    same `split_document` the commit used, which is what keeps the doc_ids identical.
    """
    from ...prepare_rag_splits import split_document  # noqa: PLC0415

    out: list[dict[str, Any]] = []
    for row in active_documents(db):
        for chunk in split_document(row.markdown, week=row.week, source_type=row.source_type,
                                    doc_id=row.stem, topic_ids=row.topic_ids or None,
                                    origin=row.origin):
            out.append({
                "doc_id": chunk.metadata.get("doc_id", ""),
                "source_type": row.source_type,
                "text": chunk.page_content,
            })
    return out


def document_stems(db: Session) -> set[str]:
    return {row.stem for row in db.query(QuestionDocument.stem)
            .filter(QuestionDocument.status == "active")}


def documents_missing_from_disk(db: Session, cleaned_dir: Any) -> list[str]:
    """Active documents that have no counterpart under `data/cleaned/`.

    Used by `ingest_to_qdrant.py`, which deletes and recreates the collection: anything
    in this list would be silently dropped by an offline re-ingest, so the script refuses
    until `export_question_bank.py --documents` has run.
    """
    from pathlib import Path  # noqa: PLC0415

    root = Path(cleaned_dir)
    return [row.stem for row in active_documents(db)
            if not (root / row.source_type / f"{row.stem}.md").exists()]


def units_for_export(db: Session, version: QuestionBankVersion) -> list[dict[str, Any]]:
    """Bank units in the portable JSON shape, each carrying its raw vector bytes."""
    rows = (db.query(QuestionUnit)
            .filter(QuestionUnit.bank_version_id == version.version_id)
            .order_by(QuestionUnit.unit_id).all())
    doc_map: dict[str, list[str]] = {}
    for link in db.query(QuestionUnitChunk):
        doc_map.setdefault(link.unit_id, []).append(link.doc_id)
    out = []
    for row in rows:
        value = _unit(row, doc_map.get(row.unit_id, []))
        value["source_file"] = row.source_file
        value["_vector"] = row.vector
        out.append(value)
    return out


def load_bank_for_evaluation(db: Session) -> tuple[dict[str, Any], np.ndarray]:
    """The active bank in the in-memory shape the evaluation harness works over.

    Replaces `qi.load_bank()`: the harness reads the same rows the API serves, so a
    metric can never describe a bank artifact that has drifted from what is live.
    """
    version = require_active_version(db)
    units = units_for_export(db, version)
    vectors = (np.vstack([
        np.frombuffer(u["_vector"], dtype=VECTOR_DTYPE) if u.get("_vector")
        else np.zeros(384, dtype=VECTOR_DTYPE)
        for u in units
    ]) if units else np.zeros((0, 384), dtype=VECTOR_DTYPE))
    for unit in units:
        unit.pop("_vector", None)
    bank = {
        "schema_version": qi.SCHEMA_VERSION,
        "embed_model": version.embedding_model,
        "thresholds": version.thresholds or {},
        "stats": version.source_summary or {},
        "units": units,
        "clusters": clusters_for_export(db, version),
    }
    return bank, vectors


def clusters_for_export(db: Session, version: QuestionBankVersion) -> list[dict[str, Any]]:
    rows = (db.query(ConceptCluster)
            .filter(ConceptCluster.bank_version_id == version.version_id)
            .order_by(ConceptCluster.cluster_id).all())
    out = []
    for row in rows:
        summary = _cluster_summary(db, row)
        members = (db.query(QuestionUnit.unit_id)
                   .filter(QuestionUnit.cluster_id == row.cluster_id).all())
        summary["member_unit_ids"] = [_public_id(m.unit_id) for m in members]
        out.append(summary)
    return out


# ── Outbox ────────────────────────────────────────────────────────────────────

def queue_course_chunks(db: Session, *, stem: str, chunks: Iterable[Any]) -> int:
    """Queue an append of course chunks to the retrieval collection.

    Chunk writes go through the outbox for the same reason unit vectors do: the database
    transaction is the commit, and a vector store that is down must leave recoverable
    work rather than a half-applied contribution or a failed request that already wrote
    part of it.
    """
    payload = [{"page_content": c.page_content, "metadata": dict(c.metadata)} for c in chunks]
    if not payload:
        return 0
    db.add(QuestionBankOutbox(operation="upsert", entity_type="course_chunk",
                              unit_id=stem, payload={"chunks": payload}))
    return len(payload)


def queue_course_chunk_delete(db: Session, *, stem: str, doc_ids: list[str]) -> int:
    if not doc_ids:
        return 0
    db.add(QuestionBankOutbox(operation="delete", entity_type="course_chunk",
                              unit_id=stem, payload={"doc_ids": list(doc_ids)}))
    return len(doc_ids)


def effective_vector_status(db: Session, version: Optional[QuestionBankVersion] = None) -> str:
    """Vector sync state computed from the rows, not read from the stored column.

    The column is written by a drain, so a version built before it existed — or one
    whose queue was cleared by another process — would otherwise keep reporting a stale
    `pending` while every unit is in fact synced. Reporting derives; the column caches.
    """
    version = version or active_version(db)
    if not version:
        return "pending"
    pending = (db.query(func.count(QuestionUnit.unit_id))
               .filter(QuestionUnit.bank_version_id == version.version_id,
                       QuestionUnit.vector_status != "synced").scalar() or 0)
    if pending == 0:
        return "synced"
    failed = (db.query(func.count(QuestionBankOutbox.outbox_id))
              .filter(QuestionBankOutbox.status == "failed").scalar() or 0)
    return "degraded" if failed else "pending"


def outbox_status(db: Session) -> dict[str, Any]:
    """Counts by status plus the oldest unfinished item — what an admin needs to see."""
    counts = {status: count for status, count in
              db.query(QuestionBankOutbox.status, func.count(QuestionBankOutbox.outbox_id))
              .group_by(QuestionBankOutbox.status).all()}
    unfinished = (db.query(QuestionBankOutbox)
                  .filter(QuestionBankOutbox.status.in_(("pending", "failed", "processing")))
                  .order_by(QuestionBankOutbox.created_at).first())
    failed = (db.query(QuestionBankOutbox)
              .filter(QuestionBankOutbox.status == "failed")
              .order_by(QuestionBankOutbox.created_at.desc()).first())
    version = active_version(db)
    return {
        "pending": counts.get("pending", 0) + counts.get("processing", 0),
        "failed": counts.get("failed", 0),
        "synced": counts.get("synced", 0),
        "oldest_unfinished_at": unfinished.created_at.isoformat() if unfinished else None,
        "last_error": failed.last_error if failed else None,
        "active_version_id": version.version_id if version else None,
        "active_version_vector_status": effective_vector_status(db, version) if version else None,
        "units_pending_vectors": (db.query(func.count(QuestionUnit.unit_id))
                                  .filter(QuestionUnit.bank_version_id == version.version_id,
                                          QuestionUnit.vector_status != "synced").scalar()
                                  if version else 0),
    }


def refresh_version_vector_status(db: Session) -> Optional[str]:
    """Write the computed status back onto the active version. Caller commits."""
    version = active_version(db)
    if not version:
        return None
    version.vector_status = effective_vector_status(db, version)
    return version.vector_status
