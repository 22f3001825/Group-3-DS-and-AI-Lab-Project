"""
api/services/llm_settings_service.py
The admin-set LLM provider hierarchy: stored, described, and published to the pipeline.

`rag_pipeline` decides which backend answers a request, and it knows nothing about the
database on purpose — it is imported by evaluation scripts and by `build_question_bank`
that have no app around them. So the link runs the other way: `install()` hands it a
resolver, this module answers that resolver from `app_settings`, and the pipeline keeps
its environment-only behaviour everywhere the API is not running.

**Why the read is cached.** The resolver is called once per LLM call, and a deployment can
run several uvicorn workers — each with its own process memory — so an in-process variable
updated by whichever worker served the PUT would leave the others on the old order until
restart. Reading the row instead makes the database the single source of truth for every
worker; the TTL keeps that from becoming a SQLite read per generated answer. The cost is
that a worker which did not serve the change picks it up within `_CACHE_TTL_SECONDS`
rather than instantly, which for a preference is the right trade.

**Requests in flight are never re-routed.** Nothing here reaches into a running call:
`generate_llm_response` snapshots the queue before its first attempt, so a save lands on
the next request. See the note in `rag_pipeline._build_provider_queue`.
"""
from __future__ import annotations

import os
import threading
import time
from typing import Any, Iterable, Optional

from sqlalchemy.orm import Session

from src import llm_judge
from src.database.models import AppSetting
from src.database.session import SessionLocal
from src.rag_pipeline import (
    GEMINI_MODELS, GROQ_MODELS, PROVIDER_IDS, PROVIDER_LABELS, env_provider_order,
    get_gemini_api_keys, get_groq_api_keys, get_local_api_keys, get_local_base_url,
    get_local_models, normalize_provider_order, set_provider_order_resolver,
)

SETTING_KEY = "llm_provider_order"

# How long a worker may serve a stale order. Short enough that "change it and try again"
# works as an operator expects, long enough that a burst of quiz grading does not turn
# into a read per graded answer.
_CACHE_TTL_SECONDS = 5.0

# Guards the two cache fields together — they are read as a pair, and a torn read would
# hand out an order with someone else's expiry.
_cache_lock = threading.Lock()
_cached_order: Optional[list[str]] = None
_cached_at: float = 0.0


class InvalidProviderOrderError(ValueError):
    """The submitted order is not a permutation of the known providers."""


# ── Stored value ──────────────────────────────────────────────────────────────

def _row(db: Session) -> Optional[AppSetting]:
    return db.get(AppSetting, SETTING_KEY)


def stored_order(db: Session) -> Optional[list[str]]:
    """The saved hierarchy, or None when no admin has ever set one.

    None is a meaningful answer, not an error: it is what makes `LLM_PROVIDER` still the
    control on a deployment nobody has configured through the UI.
    """
    row = _row(db)
    if row is None:
        return None
    value = row.value
    if isinstance(value, dict):          # tolerate {"order": [...]} written by hand
        value = value.get("order")
    if not isinstance(value, (list, tuple)) or not value:
        return None
    return normalize_provider_order(value)


def effective_order(db: Session) -> list[str]:
    """What the pipeline will actually use: the saved order, else the environment's."""
    return stored_order(db) or env_provider_order()


def set_order(db: Session, order: Iterable[str], updated_by: Optional[str] = None) -> list[str]:
    """Persist a new hierarchy and publish it. Returns the normalized order stored.

    Validation is strict about what it was *sent* — an unknown id is a client bug and is
    rejected rather than silently dropped — while what is *stored* is completed to the
    full catalogue, so a provider added later still has a defined rank.
    """
    submitted = [str(p or "").strip().lower() for p in (order or [])]
    if not submitted:
        raise InvalidProviderOrderError("Send the providers in the order you want them tried.")

    unknown = [p for p in submitted if p not in PROVIDER_IDS]
    if unknown:
        raise InvalidProviderOrderError(
            f"Unknown provider(s): {', '.join(sorted(set(unknown)))}. "
            f"Known providers are: {', '.join(PROVIDER_IDS)}."
        )
    if len(set(submitted)) != len(submitted):
        raise InvalidProviderOrderError("Each provider may appear only once in the order.")

    normalized = normalize_provider_order(submitted)

    row = _row(db)
    if row is None:
        row = AppSetting(key=SETTING_KEY, value=normalized, updated_by=updated_by)
        db.add(row)
    else:
        row.value = normalized
        row.updated_by = updated_by
    db.commit()

    _publish(normalized)
    return normalized


# ── Publication to the pipeline ───────────────────────────────────────────────

def _publish(order: Optional[list[str]]) -> None:
    """Seed this worker's cache with a known-current order and drop dependent caches.

    The judge ladder is derived from the provider queue and cached for the life of the
    process (`llm_judge._CANDIDATE_CACHE`), so without this reset a reordering would move
    the generator but leave grading on the old ladder until restart. Judge *sessions*
    already handed out keep their own list, which is the in-flight guarantee again.
    """
    global _cached_order, _cached_at
    with _cache_lock:
        _cached_order = order
        _cached_at = time.monotonic()
    llm_judge.reset_candidate_cache()


def _resolve_order() -> Optional[list[str]]:
    """The resolver `rag_pipeline` calls. Cached; None means "no admin preference"."""
    global _cached_order, _cached_at

    now = time.monotonic()
    with _cache_lock:
        if _cached_at and (now - _cached_at) < _CACHE_TTL_SECONDS:
            return _cached_order

    db = SessionLocal()
    try:
        order = stored_order(db)
    finally:
        db.close()

    with _cache_lock:
        previous = _cached_order
        _cached_order = order
        _cached_at = time.monotonic()

    # A worker that did not serve the PUT learns about it here, and its judge ladder has
    # to go the same way the writer's did.
    if previous != order:
        llm_judge.reset_candidate_cache()
    return order


def install() -> None:
    """Point `rag_pipeline` at this module. Called once, from the API's lifespan."""
    set_provider_order_resolver(_resolve_order)


def invalidate_cache() -> None:
    """Force the next resolve to hit the database — for tests, and after a direct write."""
    global _cached_order, _cached_at
    with _cache_lock:
        _cached_order = None
        _cached_at = 0.0


# ── Description for the settings UI ───────────────────────────────────────────

def _provider_facts(name: str) -> dict[str, Any]:
    """Everything the UI needs to explain one provider's state, without exposing a key."""
    if name == "gemini":
        keys, models, detail = get_gemini_api_keys(), GEMINI_MODELS, "GEMINI_API_KEY / GOOGLE_API_KEY"
    elif name == "groq":
        keys, models, detail = get_groq_api_keys(), GROQ_MODELS, "GROQ_API_KEY"
    else:
        base_url = get_local_base_url()
        keys = get_local_api_keys() if base_url else []
        models = get_local_models()
        detail = base_url or "LOCAL_LLM_BASE_URL"

    return {
        "id": name,
        "label": PROVIDER_LABELS.get(name, name),
        "models": list(models),
        "configured": bool(keys),
        "key_count": len(keys),
        # Never the key itself — only what an operator would have to go and set.
        "config_hint": detail,
    }


def describe(db: Session) -> dict[str, Any]:
    """The whole settings payload: the order in force, plus why each provider is where it is.

    `providers` is returned in hierarchy order, so the client can render the list without
    re-sorting it and the two can never disagree about what "first" means.
    """
    saved = stored_order(db)
    order = saved or env_provider_order()
    row = _row(db)

    return {
        "order": order,
        "providers": [_provider_facts(p) for p in order],
        "source": "admin" if saved else "environment",
        "env_default": (os.getenv("LLM_PROVIDER") or "gemini").strip().lower(),
        "updated_at": row.updated_at if (row is not None and saved) else None,
        "updated_by": row.updated_by if (row is not None and saved) else None,
    }
