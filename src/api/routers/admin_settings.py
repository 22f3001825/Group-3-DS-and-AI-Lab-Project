"""
api/routers/admin_settings.py
Runtime switches an administrator controls from the admin panel.

One switch today: cross-encoder reranking. The reranker runs on its own EC2 instance
(`infra/reranker/`) because the API host has no memory to spare for it, so "is it on" and
"can we reach it" are genuinely different questions — which is why there is a test probe
here as well as a toggle.

Every endpoint is gated by `require_admin`, the same dependency the authoring surface in
`routers/questions.py` uses.
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import require_admin
from ..services import rerank_service
from ...config import RERANK_DEFAULT_ENABLED, RERANK_SETTING_KEY
from ...database import crud
from ...database.models import AppSetting
from ...database.session import get_db

router = APIRouter(prefix="/admin/settings", tags=["Admin settings"])


class RerankerSetting(BaseModel):
    enabled: bool
    # False when RERANKER_URL/RERANKER_API_KEY are missing from the API's environment. The
    # UI uses this to explain why switching the toggle on would change nothing, rather
    # than letting an admin flip it and wonder why results look the same.
    endpoint_configured: bool
    last_error: Optional[str] = None
    updated_by_email: Optional[str] = None


class RerankerUpdate(BaseModel):
    enabled: bool


class ProbeResult(BaseModel):
    ok: bool
    detail: str
    latency_ms: Optional[float] = None


def _current(db: Session) -> RerankerSetting:
    row = db.query(AppSetting).filter(AppSetting.key == RERANK_SETTING_KEY).first()
    raw = row.value if row else ("true" if RERANK_DEFAULT_ENABLED else "false")

    return RerankerSetting(
        enabled=str(raw).strip().lower() == "true",
        endpoint_configured=rerank_service.endpoint_configured(),
        last_error=rerank_service.last_error(),
        updated_by_email=row.updated_by_email if row else None,
    )


@router.get("/reranker", response_model=RerankerSetting)
def get_reranker(db: Session = Depends(get_db),
                 _: Any = Depends(require_admin)) -> RerankerSetting:
    """Current state of the reranking toggle, plus why it might not be doing anything."""
    return _current(db)


@router.put("/reranker", response_model=RerankerSetting)
def set_reranker(body: RerankerUpdate,
                 db: Session = Depends(get_db),
                 admin: Any = Depends(require_admin)) -> RerankerSetting:
    """Switch reranking on or off for every user, immediately.

    `admin` is the `Student` on the bearer path and None on the `X-Admin-Token` path,
    which carries no identity — hence `getattr` rather than an attribute access, and a
    nullable column behind it.
    """
    crud.set_app_setting(
        db,
        RERANK_SETTING_KEY,
        "true" if body.enabled else "false",
        updated_by_email=getattr(admin, "email", None),
    )

    # Drop this worker's cached copy so the change is visible on the next request rather
    # than up to RERANK_SETTING_TTL_S later. Other workers still wait out their own TTL —
    # a bounded, documented delay, not a correctness problem.
    rerank_service.invalidate()

    return _current(db)


@router.post("/reranker/test", response_model=ProbeResult)
def test_reranker(_: Any = Depends(require_admin)) -> ProbeResult:
    """Probe the reranker's /health endpoint.

    Deliberately independent of the toggle: the point is to confirm the endpoint works
    BEFORE switching it on, instead of discovering a bad URL from a log line after every
    student request has quietly fallen back to retrieval order.
    """
    result = rerank_service.probe()
    return ProbeResult(
        ok=bool(result.get("ok")),
        detail=str(result.get("detail", "")),
        latency_ms=result.get("latency_ms"),
    )
