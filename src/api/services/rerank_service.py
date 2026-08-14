"""
api/services/rerank_service.py
Optional cross-encoder reranking of retrieved chunks.

Every retrieval path in this application funnels through `select()`. That is the point:
reranking is a switch an admin flips at runtime, and a switch is only trustworthy if
"off" is provably identical to the behaviour that existed before the switch was added.
With the toggle off, `select()` is `docs[:top_n]` — the exact expression it replaced at
`rag_pipeline.py` and `rag_service.py`.

The service it calls runs on a separate EC2 instance (`infra/reranker/`) because the API
host is a t3.micro with no room for a second model in-process.

FAIL OPEN, ALWAYS. A reranker that is down, slow, unreachable, misconfigured or returning
nonsense must cost the student a slightly worse chunk ordering and nothing else. Every
failure path here ends in `docs[:top_n]`. This module must never be the reason a chat
request fails — which is also why the toggle is worth having: turning it off is a
complete, instant retreat to the previous behaviour.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Optional

import requests
from langchain_core.documents import Document
from sqlalchemy.orm import Session

try:
    from src.config import (
        RERANK_API_KEY, RERANK_DEFAULT_ENABLED, RERANK_ENDPOINT_URL,
        RERANK_SETTING_KEY, RERANK_SETTING_TTL_S, RERANK_TIMEOUT_S,
    )
except ModuleNotFoundError:  # same import shim the rest of this package uses
    from config import (  # type: ignore
        RERANK_API_KEY, RERANK_DEFAULT_ENABLED, RERANK_ENDPOINT_URL,
        RERANK_SETTING_KEY, RERANK_SETTING_TTL_S, RERANK_TIMEOUT_S,
    )

from ...database import crud

# ── Toggle cache ──────────────────────────────────────────────────────────────
# Reading `app_settings` on every retrieval would add a SELECT to the critical path of
# every chat message. The value changes roughly never, so it is cached for a few seconds.
#
# The lock guards the tuple swap only. Uvicorn serves requests on a thread pool, so two
# threads can race here; the worst outcome without the lock is a duplicated read, but the
# lock is cheap and makes `invalidate()` unambiguous.
_lock = threading.Lock()
_cached: Optional[tuple[bool, float]] = None   # (enabled, expires_at monotonic)

# Surfaced by the admin endpoint so an operator can see WHY reranking is silently doing
# nothing without going to the server logs.
_last_error: Optional[str] = None


def invalidate() -> None:
    """Drop the cached toggle. Called by the admin PUT so the change lands immediately."""
    global _cached
    with _lock:
        _cached = None


def endpoint_configured() -> bool:
    """True when this process has somewhere to send a rerank request."""
    return bool(RERANK_ENDPOINT_URL and RERANK_API_KEY)


def last_error() -> Optional[str]:
    """Most recent failure, for the admin panel. None once a call has succeeded."""
    return _last_error


def is_enabled(db: Session) -> bool:
    """Whether reranking should run, honouring both configuration and the admin toggle.

    An unconfigured endpoint wins over the toggle. Someone can switch reranking on in a
    deployment that has no reranker; that must be a no-op, not an error on every message.
    """
    if not endpoint_configured():
        return False

    global _cached
    now = time.monotonic()

    with _lock:
        if _cached is not None and _cached[1] > now:
            return _cached[0]

    try:
        raw = crud.get_app_setting(db, RERANK_SETTING_KEY,
                                   "true" if RERANK_DEFAULT_ENABLED else "false")
        enabled = str(raw).strip().lower() == "true"
    except Exception:  # noqa: BLE001
        # A database hiccup must not decide retrieval policy. Fall back to the compiled-in
        # default rather than propagating: this function is called from the request path.
        enabled = RERANK_DEFAULT_ENABLED

    with _lock:
        _cached = (enabled, now + RERANK_SETTING_TTL_S)
    return enabled


# ── The reranker call ─────────────────────────────────────────────────────────

def _score(query: str, texts: list[str], top_n: int) -> Optional[list[int]]:
    """POST to the reranker and return document indices, best first.

    Returns None on any failure, which the caller reads as "keep the existing order".
    """
    global _last_error

    try:
        response = requests.post(
            f"{RERANK_ENDPOINT_URL}/rerank",
            json={"query": query, "documents": texts, "top_n": top_n},
            headers={"Authorization": f"Bearer {RERANK_API_KEY}"},
            timeout=RERANK_TIMEOUT_S,
        )
        response.raise_for_status()
        payload = response.json()

        indices = [int(item["index"]) for item in payload["results"]]
    except Exception as exc:  # noqa: BLE001
        _last_error = f"{type(exc).__name__}: {exc}"
        print(f"  [Rerank] Falling back to retrieval order — {_last_error}", flush=True)
        return None

    # Trust nothing about the shape of the response. An out-of-range index would raise an
    # IndexError deep inside the caller's list comprehension, turning a cosmetic feature
    # into a 500 on the chat endpoint.
    if any(i < 0 or i >= len(texts) for i in indices):
        _last_error = "reranker returned an out-of-range index"
        print(f"  [Rerank] Falling back to retrieval order — {_last_error}", flush=True)
        return None

    _last_error = None
    return indices


def select(db: Session, query: str, docs: list[Document], top_n: int) -> list[Document]:
    """Choose the `top_n` documents to use, reranking them first if that is switched on.

    This is the ONLY entry point. Call it everywhere a retrieval result used to be sliced,
    so that one toggle governs every path and no call site can drift.

    Args:
        db:     session used to read the toggle (and nothing else).
        query:  the text the documents were retrieved for.
        docs:   candidates in retrieval order, longer than `top_n` for reranking to help.
        top_n:  how many to return.

    Returns:
        At most `top_n` documents. Reranked when enabled and reachable; otherwise the
        first `top_n` in the order they arrived.
    """
    if not docs:
        return []

    # The path that must be indistinguishable from pre-feature behaviour.
    if not is_enabled(db):
        return docs[:top_n]

    # Reranking a list no longer than `top_n` still earns its keep: it cannot drop a
    # chunk, but it re-orders one, and position within the prompt matters — a model
    # attends more to what it reads first. Only a single document is a genuine no-op.
    if len(docs) < 2:
        return docs[:top_n]

    indices = _score(query, [doc.page_content for doc in docs], top_n)
    if indices is None:
        return docs[:top_n]

    return [docs[i] for i in indices][:top_n]


def probe() -> dict[str, Any]:
    """Check the reranker is reachable, for the admin panel's "Test connection" button.

    Exists so an admin can find out the endpoint is wrong BEFORE switching the toggle on
    and discovering it from a log line nobody reads. Hits `/health`, which needs no
    credentials, so a 401 here specifically means the URL is pointing at something that
    is not this service.
    """
    if not RERANK_ENDPOINT_URL:
        return {"ok": False, "detail": "RERANKER_URL is not set in the API's environment."}
    if not RERANK_API_KEY:
        return {"ok": False, "detail": "RERANKER_API_KEY is not set in the API's environment."}

    started = time.perf_counter()
    try:
        response = requests.get(f"{RERANK_ENDPOINT_URL}/health", timeout=RERANK_TIMEOUT_S)
        response.raise_for_status()
        body = response.json()
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
        }

    return {
        "ok": body.get("status") == "ok",
        "detail": f"model={body.get('model')} warm={body.get('warm')}",
        "latency_ms": round((time.perf_counter() - started) * 1000, 1),
    }
