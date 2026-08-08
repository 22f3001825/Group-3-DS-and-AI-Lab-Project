"""
api/schemas/chat.py
Pydantic request and response models for chat endpoints.
"""
from __future__ import annotations
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class ChatTurn(BaseModel):
    """One earlier message in the conversation, supplied by the client."""
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=8000)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Student's question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
    # No student_id. Identity is the bearer token's, so a client cannot write into
    # another learner's history by naming them.
    session_id: Optional[str] = Field(default=None, description="Optional session ID to continue a conversation")
    # Short-term memory for follow-up questions, oldest first. This cap is only a payload
    # guard — `rag_pipeline.format_history` trims to CHAT_MEMORY_TURNS and condenses each
    # answer to its Direct Answer section before anything reaches the prompt.
    history: list[ChatTurn] = Field(
        default_factory=list,
        max_length=20,
        description="Recent conversation turns, oldest first; used only to resolve follow-ups",
    )


class SourceChunk(BaseModel):
    text: str
    metadata: dict[str, Any]


class RelatedQuestion(BaseModel):
    """A canonical sibling of something the student just retrieved."""
    unit_id: str
    cluster_id: Optional[int] = None
    title: str
    source_type: str
    week: int
    member_count: int = 1


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    provider_used: str
    fallback_used: bool
    session_id: Optional[str] = None
    message_id: Optional[str] = None
    # Defaulted, so every existing client keeps working and a missing question bank is
    # indistinguishable from "nothing related" rather than being an error.
    related_questions: list[RelatedQuestion] = []


class RetrieveRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrieveResponse(BaseModel):
    question: str
    chunks: list[SourceChunk]
