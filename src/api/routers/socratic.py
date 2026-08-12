"""
api/routers/socratic.py
The Chrome extension's endpoints. Five handlers, one policy.

**Every handler is a plain `def`, not `async def`.** They make blocking calls — a Qdrant
round trip, one or two LLM invocations — so declaring them `async` would occupy the event
loop for the whole request. FastAPI runs plain `def` handlers in its threadpool, which is
what the two quiz handlers already do for the same reason. `chat.py` is the counterexample,
not the model to copy.

Ownership is uniform and deliberately quiet: a session belonging to someone else **404s**
rather than 403s, matching `GET /session/{id}/history`. Whether a session id exists is
itself information the caller has no legitimate way to have.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ...config import SOCRATIC_CAPTURE_MAX_MB
from ...database.models import Student
from ...database.session import get_db
from ..dependencies import get_current_student, get_retriever, get_transcript_retriever
from ..schemas.socratic import (
    AnalyzeRequest, AnalyzeResponse, AttemptRequest, AttemptResponse, HintResponse,
    SessionReplay, TranscribeResponse,
)
from ..services import socratic_service as service

router = APIRouter(prefix="/socratic", tags=["Socratic"])


def _resolve(db: Session, session_id: str, current: Student):
    try:
        return service.get_session(db, session_id, current.student_id,
                                   is_admin=bool(current.is_admin))
    except service.SocraticSessionNotFound:
        raise HTTPException(status_code=404, detail="Session not found.") from None


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(body: AnalyzeRequest,
            db: Session = Depends(get_db),
            current: Student = Depends(get_current_student),
            transcript_retriever=Depends(get_transcript_retriever),
            course_retriever=Depends(get_retriever)):
    """A highlighted question → concept, lecture segments, one guiding question.

    Two retrievers are injected on purpose. `transcript_retriever` is the only one whose
    text reaches the model (L2). `course_retriever` is unfiltered and its results are
    never shown to anyone — they exist to build the L4 answer denylist and the
    related-questions links. Wiring both here rather than constructing one inside the
    service keeps the singletons and their caches in `dependencies`.

    Never 503s on a model outage: generation failure falls back to a taxonomy-built card,
    and `policy.source` reports which path ran.
    """
    try:
        return service.analyze(
            db,
            student_id=current.student_id,
            selection=body.selection,
            options=body.options,
            transcript_retriever=transcript_retriever,
            course_retriever=course_retriever,
            page_url=body.page_url,
            source_kind=body.source_kind,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{session_id}/hint", response_model=HintResponse)
def next_hint(session_id: str,
              db: Session = Depends(get_db),
              current: Student = Depends(get_current_student)):
    """Step the hint ladder up one tier. No model is consulted (L5)."""
    session = _resolve(db, session_id, current)
    try:
        return service.advance_hint(db, session)
    except service.HintLadderExhausted:
        raise HTTPException(
            status_code=409,
            detail={"code": "hint_ladder_exhausted",
                    "message": "There is no further hint. Try writing out your reasoning "
                               "and submitting it for review."},
        ) from None
    except service.AttemptRequired:
        raise HTTPException(
            status_code=409,
            detail={"code": "attempt_required",
                    "message": "Submit an attempt first — the last hint is built from "
                               "your own reasoning."},
        ) from None


@router.post("/{session_id}/attempt", response_model=AttemptResponse)
def submit_attempt(session_id: str, body: AttemptRequest,
                   db: Session = Depends(get_db),
                   current: Student = Depends(get_current_student),
                   course_retriever=Depends(get_retriever)):
    """Review the student's reasoning; name the first wrong step, never the answer.

    503 when no judge is reachable. An ungraded attempt can be retried; a fabricated
    diagnosis teaches the student something false, so it is never invented.
    """
    session = _resolve(db, session_id, current)
    try:
        return service.record_attempt(db, session, body.student_answer, course_retriever)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except service.FeedbackUnavailable as exc:
        raise HTTPException(
            status_code=503,
            detail=f"No reviewer is reachable right now (last tried: {exc}). "
                   f"Your attempt was not lost — try again shortly.",
        ) from exc


@router.get("/{session_id}", response_model=SessionReplay)
def replay_session(session_id: str,
                   db: Session = Depends(get_db),
                   current: Student = Depends(get_current_student)):
    """Everything this session emitted, oldest first."""
    return service.replay(db, _resolve(db, session_id, current))


@router.post("/transcribe", response_model=TranscribeResponse)
def transcribe(file: UploadFile = File(...),
               current: Student = Depends(get_current_student)):
    """Read a question out of a cropped screenshot — the PDF path.

    Authenticated like everything else: an open endpoint here would let anyone burn the
    project's Gemini quota one image at a time.
    """
    from ...rag_pipeline import OCRUnavailableError, transcribe_image  # noqa: PLC0415

    data = file.file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty upload.")
    if len(data) > SOCRATIC_CAPTURE_MAX_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"Image is larger than {SOCRATIC_CAPTURE_MAX_MB} MB. Crop more tightly.",
        )

    try:
        text, provider = transcribe_image(data, file.content_type or "image/png")
    except OCRUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    # Split trailing "(a) ..." lines off as options so the panel can show them, and so
    # `analyze` receives the same shape it gets from a DOM adapter.
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    options, statement = [], []
    for line in lines:
        if len(line) < 200 and line[:1] in "([abcdeABCDE" and (
                line[:4].lower().strip("([)]. ") in list("abcde")):
            options.append(line)
        else:
            statement.append(line)
    return TranscribeResponse(text=" ".join(statement) or text,
                              options=options, provider_used=provider)
