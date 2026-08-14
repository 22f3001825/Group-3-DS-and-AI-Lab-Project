"""
api/routers/settings.py
Admin-only runtime settings. Today: the LLM provider hierarchy.

Both endpoints sit behind `require_admin`, the same gate as the authoring surface — an
identified admin (`Student.is_admin`, read from the row on every request) or the shared
`X-Admin-Token`, and 503 when neither is configured so an unconfigured deployment is
closed rather than open. The read is admin-gated too: it enumerates which providers are
reachable and which environment variables are missing, which is deployment shape and not
something a student endpoint should describe.

Plain `def`, like the auth and questions routers: the settings row is a blocking SQLite
read and belongs in FastAPI's threadpool.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import require_admin
from ..schemas.settings import LLMProviderOrder, UpdateProviderOrderRequest
from ..services import llm_settings_service
from ...database.session import get_db

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])


def _actor(admin: Any) -> str:
    """Who to record. `require_admin` returns None for the shared-token path, which has
    no identity by construction — naming it as the token is more honest than a blank."""
    if admin is None:
        return "admin-token"
    return getattr(admin, "email", None) or getattr(admin, "student_id", "") or "admin"


@router.get("/llm-providers", response_model=LLMProviderOrder)
def get_llm_providers(db: Session = Depends(get_db),
                      _: Any = Depends(require_admin)) -> LLMProviderOrder:
    """The hierarchy in force, and the state of every provider it names."""
    return LLMProviderOrder(**llm_settings_service.describe(db))


@router.put("/llm-providers", response_model=LLMProviderOrder)
def set_llm_providers(request: UpdateProviderOrderRequest,
                      db: Session = Depends(get_db),
                      admin: Any = Depends(require_admin)) -> LLMProviderOrder:
    """Set the order every user's next request follows.

    Deployment-wide by design — there is one queue, and the point of the setting is that a
    course team can move traffic off a rate-limited provider for everybody at once.
    Requests already generating an answer finish on the provider they started with; the
    new order applies from the next one.

    400 for an unknown or repeated provider id. A provider that is not configured is NOT
    an error: ranking it is how a deployment prepares for a key it is about to add, and it
    is simply skipped until then.
    """
    try:
        llm_settings_service.set_order(db, request.order, updated_by=_actor(admin))
    except llm_settings_service.InvalidProviderOrderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return LLMProviderOrder(**llm_settings_service.describe(db))
