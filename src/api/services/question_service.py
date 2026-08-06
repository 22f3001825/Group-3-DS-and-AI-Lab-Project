"""Database-backed read service for AI Question Intelligence.

SQLite/PostgreSQL is authoritative. The small in-process cache below holds only
serialised endpoint responses and is keyed by active bank version; clearing it is safe.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Optional

from sqlalchemy.orm import Session

from ...config import (
    QI_MIN_COMMON_DOUBT_SIZE, QI_MIN_DISPLAY_MEMBERS, QI_MIN_TITLE_READABILITY,
)
from . import question_repository as repo

_LOCK = threading.Lock()
_CACHE: dict[tuple[Any, ...], tuple[float, Any]] = {}
_TTL_SECONDS = 30.0


class QuestionBankUnavailableError(RuntimeError):
    """No active database-backed question bank is available."""


def invalidate_question_bank() -> None:
    """Discard derived response cache after a successful database transaction."""
    with _LOCK:
        _CACHE.clear()


def _version_key(db: Session) -> str:
    try:
        return repo.require_active_version(db).version_id
    except LookupError as exc:
        raise QuestionBankUnavailableError(str(exc)) from exc


def _cached(db: Session, key: tuple[Any, ...], factory: Any) -> Any:
    version = _version_key(db)
    cache_key = (version, *key)
    now = time.monotonic()
    with _LOCK:
        hit = _CACHE.get(cache_key)
        if hit and now - hit[0] < _TTL_SECONDS:
            return hit[1]
    try:
        value = factory()
    except LookupError as exc:
        raise QuestionBankUnavailableError(str(exc)) from exc
    with _LOCK:
        _CACHE[cache_key] = (now, value)
    return value


def bank_is_available(db: Session) -> bool:
    try:
        _version_key(db)
        return True
    except QuestionBankUnavailableError:
        return False


def get_stats(db: Session) -> dict[str, Any]:
    return _cached(db, ("stats",),
                   lambda: repo.stats(db, QI_MIN_DISPLAY_MEMBERS, QI_MIN_TITLE_READABILITY))


def list_clusters(db: Session, week: Optional[int] = None, source_type: Optional[str] = None,
                  min_member_count: int = QI_MIN_DISPLAY_MEMBERS,
                  limit: int = 50) -> list[dict[str, Any]]:
    """The browsable list. The readability gate is policy, not a caller's choice: a
    caller allowed to turn it off would put unlabelled clusters back on the page."""
    return _cached(db, ("clusters", week, source_type, min_member_count, limit),
                   lambda: repo.list_clusters(db, week, source_type, min_member_count,
                                              limit, QI_MIN_TITLE_READABILITY))


def get_cluster(db: Session, cluster_id: int | str) -> Optional[dict[str, Any]]:
    return _cached(db, ("cluster", str(cluster_id)), lambda: repo.get_cluster(db, cluster_id))


def common_doubts(db: Session, limit: int = 10) -> list[dict[str, Any]]:
    return _cached(db, ("common", limit),
                   lambda: repo.common_doubts(db, QI_MIN_COMMON_DOUBT_SIZE, limit,
                                              QI_MIN_TITLE_READABILITY))


def related_to_doc_ids(db: Session, doc_ids: list[str], limit: int = 5) -> list[dict[str, Any]]:
    try:
        return repo.related_to_doc_ids(db, doc_ids, limit)
    except LookupError as exc:
        raise QuestionBankUnavailableError(str(exc)) from exc


def search(db: Session, query: str, retriever: Any, limit: int = 10) -> list[dict[str, Any]]:
    _version_key(db)
    try:
        docs = retriever.invoke(query)
    except Exception as exc:  # noqa: BLE001
        raise QuestionBankUnavailableError(f"Retrieval failed: {type(exc).__name__}") from exc
    doc_ids = [doc.metadata.get("doc_id", "") for doc in (docs or [])]
    # Related units include canonical siblings. Search should return the units directly
    # mapped to retrieval hits; the repository's cluster detail supplies the full graph.
    rows = repo.related_to_doc_ids(db, doc_ids, limit)
    return rows


def canonical_doc_ids_to_drop(db: Session, doc_ids: list[str]) -> set[str]:
    try:
        return repo.canonical_doc_ids_to_drop(db, doc_ids)
    except Exception:  # Question intelligence must never break quiz generation.
        return set()


def load_warnings(db: Session) -> list[str]:
    _version_key(db)
    return []
