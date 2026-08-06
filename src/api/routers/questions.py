"""
api/routers/questions.py
Question Intelligence — read endpoints plus the admin authoring path.

Read endpoints are open (the Doubts page is for students and instructors alike). Every
authoring endpoint is admin-gated by `require_admin`, which returns 503 when ADMIN_TOKEN
is unset so an unconfigured deployment is closed rather than wide open.

There are three ways to create a draft and exactly ONE way to commit it. Two of the
three make a single-shot path tempting — the admin wrote the text, so what is there to
review? — but a bypass on `paste` is still a bypass, and one committer is what keeps the
validation, the collision check and the append semantics in a single place that no
origin can skip.

All handlers are plain `def` rather than `async def`, so FastAPI runs the blocking
parse/split/embed work in its threadpool — the same reasoning that made the two quiz
handlers plain `def` while the chat handlers occupy the event loop.
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from ..dependencies import get_retriever, get_vector_store, require_admin
from ..schemas.questions import (
    BankStats, ClusterDetail, ClusterSummary, CommitRequest, ComposeDraftRequest,
    CreateDraftRequest, DraftPreview, PreviewRequest, QuestionUnit, StagedDraft,
    SyncStatus, UploadResult,
)
from ..services import ingest_service, question_repository, question_service
from ..services.question_service import QuestionBankUnavailableError
from ..services.question_vector_service import sync_outbox
from ...config import QI_MIN_DISPLAY_MEMBERS, QI_UPLOAD_MAX_MB
from ...database.session import get_db

router = APIRouter(prefix="/questions", tags=["Question Intelligence"])

_BANK_MISSING = (
    "The question bank has not been built. Run: python src/build_question_bank.py"
)


def _unavailable(exc: QuestionBankUnavailableError) -> HTTPException:
    return HTTPException(status_code=503, detail=str(exc) or _BANK_MISSING)


def _ingest_error(exc: ingest_service.IngestError) -> HTTPException:
    return HTTPException(
        status_code=exc.status_code,
        detail={"code": exc.code, "message": exc.message} if exc.code else exc.message,
    )


# ── Read side ─────────────────────────────────────────────────────────────────

@router.get("/stats", response_model=BankStats)
def get_stats(db: Session = Depends(get_db)) -> BankStats:
    try:
        return BankStats(**question_service.get_stats(db))
    except QuestionBankUnavailableError as exc:
        raise _unavailable(exc)


@router.get("/clusters", response_model=list[ClusterSummary])
def list_clusters(
    week: Optional[int] = Query(default=None, ge=0, le=52),
    source_type: Optional[str] = Query(default=None),
    min_member_count: int = Query(default=QI_MIN_DISPLAY_MEMBERS, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[ClusterSummary]:
    """Browsable concept groups.

    Two clusters are withheld from this list and only this list: singletons (they grouped
    nothing) and clusters whose title is OCR debris (they cannot be read). Pass
    `min_member_count=1` to see the singletons; the readability gate is not overridable
    here, and neither gate affects `/clusters/{id}`, `/search` or quiz generation.
    """
    try:
        rows = question_service.list_clusters(db, week, source_type, min_member_count, limit)
    except QuestionBankUnavailableError as exc:
        raise _unavailable(exc)
    return [ClusterSummary(**r) for r in rows]


@router.get("/common-doubts", response_model=list[ClusterSummary])
def common_doubts(limit: int = Query(default=10, ge=1, le=50),
                  db: Session = Depends(get_db)) -> list[ClusterSummary]:
    """Clusters ranked by how many TIMES a doubt was asked (`asked_count`).

    Not `member_count`: PYQ members are OCR-split fragments of one printed question, so
    counting them here reported scanner behaviour as demand.
    """
    try:
        rows = question_service.common_doubts(db, limit)
    except QuestionBankUnavailableError as exc:
        raise _unavailable(exc)
    return [ClusterSummary(**r) for r in rows]


@router.get("/search", response_model=list[QuestionUnit])
def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=50),
    retriever: Any = Depends(get_retriever),
    db: Session = Depends(get_db),
) -> list[QuestionUnit]:
    try:
        hits = question_service.search(db, q, retriever, limit)
    except QuestionBankUnavailableError as exc:
        raise _unavailable(exc)
    return [QuestionUnit(**h) for h in hits]


@router.get("/clusters/{cluster_id}", response_model=ClusterDetail)
def get_cluster(cluster_id: int, db: Session = Depends(get_db)) -> ClusterDetail:
    try:
        cluster = question_service.get_cluster(db, cluster_id)
    except QuestionBankUnavailableError as exc:
        raise _unavailable(exc)
    if not cluster:
        raise HTTPException(status_code=404, detail=f"No cluster {cluster_id}.")
    return ClusterDetail(**cluster)


# ── Phase A: three ways to create a draft ─────────────────────────────────────

@router.post("/extract", response_model=DraftPreview)
def extract_pdf(
    file: UploadFile = File(...),
    title: str = Form(default=""),
    source_type: str = Form(default=""),
    content_kind: Optional[str] = Form(default=None),
    week: Optional[int] = Form(default=None),
    topic_ids: str = Form(default=""),
    lecture_ref: Optional[str] = Form(default=None),
    source_note: Optional[str] = Form(default=None),
    allow_ocr: bool = Form(default=False),
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
) -> DraftPreview:
    """Origin `pdf`. Writes one draft row and nothing else — no file, anywhere.

    `replace` is deliberately not a parameter here: it authorises a delete, so it
    belongs to the commit rather than to the draft.
    """
    if (file.content_type or "") not in ("application/pdf", "application/x-pdf", "") \
            and not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are accepted here.")

    payload = file.file.read()
    if len(payload) > QI_UPLOAD_MAX_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File is {len(payload) / 1024 / 1024:.1f} MB; the limit is {QI_UPLOAD_MAX_MB} MB.",
        )

    meta = {
        "title": title, "source_type": source_type, "content_kind": content_kind,
        "week": week, "lecture_ref": lecture_ref, "source_note": source_note,
        "topic_ids": [t for t in (topic_ids or "").split(",") if t.strip()],
    }
    try:
        return DraftPreview(**ingest_service.extract(
            db, payload, file.filename or "upload.pdf", meta, allow_ocr=allow_ocr))
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)


@router.post("/drafts", response_model=DraftPreview)
def create_text_draft(request: CreateDraftRequest,
                      db: Session = Depends(get_db),
                      _: str = Depends(require_admin)) -> DraftPreview:
    """Origin `paste`. No file handling, and `process_dataset` is never imported."""
    try:
        return DraftPreview(**ingest_service.create_draft(
            db, request.markdown, request.metadata.model_dump()))
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)


@router.post("/drafts/compose", response_model=DraftPreview)
def create_composed_draft(request: ComposeDraftRequest,
                          db: Session = Depends(get_db),
                          _: str = Depends(require_admin)) -> DraftPreview:
    """Origin `compose`. Fields in, canonical question markdown out."""
    try:
        return DraftPreview(**ingest_service.compose(
            db, [q.model_dump() for q in request.questions], request.metadata.model_dump()))
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)


# ── Review and Phase B ────────────────────────────────────────────────────────

@router.get("/staged", response_model=list[StagedDraft])
def list_staged(db: Session = Depends(get_db),
                _: str = Depends(require_admin)) -> list[StagedDraft]:
    return [StagedDraft(**d) for d in ingest_service.list_drafts(db)]


@router.get("/staged/{draft_id}", response_model=DraftPreview)
def get_staged(draft_id: str, db: Session = Depends(get_db),
               _: str = Depends(require_admin)) -> DraftPreview:
    """Lets a review survive a browser refresh, an API restart, or another machine."""
    try:
        return DraftPreview(**ingest_service.get_draft(db, draft_id))
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)


@router.post("/staged/{draft_id}/preview", response_model=DraftPreview)
def preview_staged(draft_id: str, request: PreviewRequest,
                   db: Session = Depends(get_db),
                   _: str = Depends(require_admin)) -> DraftPreview:
    """Re-analyse edited text and metadata. No PDF parse, no OCR, no embedding.

    The edit is kept on the draft row, so the review survives a crash; nothing about
    the corpus, the collection or the bank changes here.
    """
    try:
        return DraftPreview(**ingest_service.reanalyse(
            db, draft_id, request.markdown,
            request.metadata.model_dump() if request.metadata else None))
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)


@router.post("/staged/{draft_id}/commit", response_model=UploadResult)
def commit_staged(draft_id: str, request: CommitRequest,
                  vector_store: Any = Depends(get_vector_store),
                  db: Session = Depends(get_db),
                  _: str = Depends(require_admin)) -> UploadResult:
    """The only endpoint that changes stored content, and it does so in one transaction."""
    try:
        return UploadResult(**ingest_service.commit(
            draft_id, request.markdown, vector_store, db,
            request.metadata.model_dump() if request.metadata else None,
            replace=request.replace))
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)


@router.delete("/staged/{draft_id}")
def delete_staged(draft_id: str, db: Session = Depends(get_db),
                  _: str = Depends(require_admin)) -> dict:
    """Discard a review. This one call is the whole rollback for Phase A."""
    try:
        ingest_service.discard_draft(db, draft_id)
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)
    return {"draft_id": draft_id, "status": "discarded"}


# ── History, sync and rebuild ─────────────────────────────────────────────────

@router.get("/uploads")
def list_uploads(db: Session = Depends(get_db),
                 _: str = Depends(require_admin)) -> list[dict]:
    """Contribution history, from `question_uploads`."""
    return ingest_service.list_uploads(db)


@router.get("/sync", response_model=SyncStatus)
def sync_status(db: Session = Depends(get_db),
                _: str = Depends(require_admin)) -> SyncStatus:
    """Outbox health.

    A relational commit succeeds even when Qdrant is unreachable, which is the right
    trade — but only if the resulting queue is visible somewhere other than the logs.
    """
    return SyncStatus(**question_repository.outbox_status(db))


@router.post("/sync", response_model=SyncStatus)
def run_sync(limit: int = Query(default=500, ge=1, le=5000),
             db: Session = Depends(get_db),
             _: str = Depends(require_admin)) -> SyncStatus:
    """Drain the outbox now. Idempotent; failures stay queued with their last error."""
    sync_outbox(db, limit=limit)
    return SyncStatus(**question_repository.outbox_status(db))


@router.post("/rebuild", response_model=BankStats)
def rebuild(refresh_vectors: bool = Query(default=False),
            db: Session = Depends(get_db),
            _: str = Depends(require_admin)) -> BankStats:
    """Full re-cluster — the drift escape hatch. Cluster IDs are NOT preserved.

    Reads the corpus tree and every stored document. `refresh_vectors=true` bypasses the
    embedding cache, which is only needed if the embedding model itself changed.
    """
    try:
        stats = ingest_service.rebuild_bank(db, refresh_vectors=refresh_vectors)
    except ingest_service.IngestError as exc:
        raise _ingest_error(exc)
    stats = dict(stats)
    stats.setdefault("thresholds", {})
    stats.setdefault("generated_from", "")
    stats.setdefault("vector_status", "pending")
    return BankStats(**stats)
