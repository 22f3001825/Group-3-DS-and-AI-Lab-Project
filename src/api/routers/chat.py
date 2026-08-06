"""
api/routers/chat.py
Chat and retrieval endpoints with automated learner topic exploration tracking.

POST /chat     — full RAG: retrieve + LLM answer, optionally persist to DB & track topics
POST /retrieve — retrieve only (no LLM), for debugging
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_retriever
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
) -> ChatResponse:
    """
    Full RAG endpoint.
    - Retrieves relevant chunks from Qdrant (hybrid dense+sparse search)
    - Generates a structured answer via Gemini / Groq with multi-key failover
    - Persists the exchange to the DB and records topic exploration for learner profile

    `request.history` carries the client's recent turns so follow-up questions resolve; only
    the current question is persisted, exactly as before.
    """
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

    # Persist to DB if student_id is provided
    if request.student_id:
        crud.get_or_create_student(db, request.student_id)

        # Auto-create session if none given
        if not session_id:
            session = crud.create_chat_session(db, student_id=request.student_id)
            session_id = session.session_id

        # Save user message
        crud.add_chat_message(
            db,
            session_id=session_id,
            role="user",
            content=request.question,
            student_id=request.student_id,
        )
        # Save assistant message
        assistant_msg = crud.add_chat_message(
            db,
            session_id=session_id,
            role="assistant",
            content=result["answer"],
            student_id=request.student_id,
            topics_detected=result["topics_detected"],
            provider_used=result["provider_used"],
        )
        message_id = assistant_msg.message_id

        # Auto-track topics explored in chat
        for t_name in result.get("topics_detected", []):
            matched = find_topic(t_name)
            if matched:
                crud.record_chat_topic_interaction(
                    db,
                    student_id=request.student_id,
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
