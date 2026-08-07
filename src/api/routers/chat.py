"""
api/routers/chat.py
Chat and retrieval endpoints with automated learner topic exploration tracking.

POST /chat     — full RAG: retrieve + LLM answer, persist to DB & track topics
POST /retrieve — retrieve only (no LLM), for debugging

Both handlers require a signed-in student, and `student_id` comes from the token rather
than the request body. One consequence is worth stating: persistence used to be opt-in
(the client chose whether to send an id), and is now unconditional. Every answered
question is recorded and every detected topic increments `chat_interactions` — which is
what makes the "explored" signal on the Progress page reflect actual use.
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_student, get_retriever
from ...database.models import Student
from ..schemas.chat import (
    ChatRequest, ChatResponse, RelatedQuestion, RetrieveRequest, RetrieveResponse, SourceChunk,
)
from ..services.rag_service import run_rag, run_retrieve_only
from ..services.recommendation_service import find_topic
from ..services import question_service
from ...database.session import get_db
from ...database import crud

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    retriever: Any = Depends(get_retriever),
    db: Session = Depends(get_db),
    current: Student = Depends(get_current_student),
) -> ChatResponse:
    """
    Full RAG endpoint.
    - Retrieves relevant chunks from Qdrant (hybrid dense+sparse search)
    - Generates a structured answer via Gemini / Groq with multi-key failover
    - Persists the exchange to the DB and records topic exploration for learner profile

    `request.history` carries the client's recent turns so follow-up questions resolve; only
    the current question is persisted, exactly as before.
    """
    student_id = current.student_id
    try:
        result = run_rag(
            request.question,
            retriever,
            top_k=request.top_k,
            history=[turn.model_dump() for turn in request.history],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {exc}")

    session_id: Optional[str] = request.session_id
    message_id: Optional[str] = None

    # A continued session must belong to the caller; otherwise this would be a way to
    # append messages to someone else's transcript by guessing an id.
    if session_id:
        session = crud.get_chat_session(db, session_id)
        if not session or (session.student_id != student_id and not current.is_admin):
            raise HTTPException(status_code=404, detail="Session not found.")
    else:
        session = crud.create_chat_session(db, student_id=student_id)
        session_id = session.session_id

    crud.add_chat_message(
        db,
        session_id=session_id,
        role="user",
        content=request.question,
        student_id=student_id,
    )
    assistant_msg = crud.add_chat_message(
        db,
        session_id=session_id,
        role="assistant",
        content=result["answer"],
        student_id=student_id,
        topics_detected=result["topics_detected"],
        provider_used=result["provider_used"],
    )
    message_id = assistant_msg.message_id

    # Auto-track topics explored in chat — the "explored" signal the recommender reads.
    for t_name in result.get("topics_detected", []):
        matched = find_topic(t_name)
        if matched:
            crud.record_chat_topic_interaction(
                db,
                student_id=student_id,
                topic_id=matched["id"],
                topic_name=matched["name"],
            )

    # "Students also asked" — canonical siblings of the chunks that were just retrieved.
    # Wrapped because a missing or broken question bank must never take the chat path
    # down: the answer is the product, this is a garnish.
    related: list[RelatedQuestion] = []
    try:
        doc_ids = [s["metadata"].get("doc_id", "") for s in result["sources"]]
        related = [RelatedQuestion(**r) for r in question_service.related_to_doc_ids(db, doc_ids)]
    except Exception:  # noqa: BLE001
        related = []

    return ChatResponse(
        answer=result["answer"],
        sources=[SourceChunk(**s) for s in result["sources"]],
        provider_used=result["provider_used"],
        fallback_used=result["fallback_used"],
        session_id=session_id,
        message_id=message_id,
        related_questions=related,
    )


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_only(
    request: RetrieveRequest,
    retriever: Any = Depends(get_retriever),
    _: Student = Depends(get_current_student),
) -> RetrieveResponse:
    """
    Debug endpoint — retrieves chunks without calling the LLM.
    Useful for inspecting what context will be passed to the model.
    """
    try:
        chunks = run_retrieve_only(request.question, retriever, top_k=request.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {exc}")

    return RetrieveResponse(
        question=request.question,
        chunks=[SourceChunk(**c) for c in chunks],
    )
