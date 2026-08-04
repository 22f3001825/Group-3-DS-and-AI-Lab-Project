"""
api/routers/chat.py
Chat and retrieval endpoints.

POST /chat     — full RAG: retrieve + LLM answer, optionally persist to DB
POST /retrieve — retrieve only (no LLM), for debugging
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_retriever
from ..schemas.chat import ChatRequest, ChatResponse, RetrieveRequest, RetrieveResponse, SourceChunk
from ..services.rag_service import run_rag, run_retrieve_only
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
    - Generates a structured answer via Gemini (falls back to Groq)
    - Optionally persists the exchange to the DB if student_id is provided
    """
    try:
        result = run_rag(request.question, retriever, top_k=request.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {exc}")

    session_id: Optional[str] = request.session_id
    message_id: Optional[str] = None

    # Persist to DB only if a student_id was provided
    if request.student_id:
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

    return ChatResponse(
        answer=result["answer"],
        sources=[SourceChunk(**s) for s in result["sources"]],
        provider_used=result["provider_used"],
        fallback_used=result["fallback_used"],
        session_id=session_id,
        message_id=message_id,
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
