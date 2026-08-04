"""
api/schemas/chat.py
Pydantic request and response models for chat endpoints.
"""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Student's question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
    student_id: Optional[str] = Field(default=None, description="Optional student ID for saving history")
    session_id: Optional[str] = Field(default=None, description="Optional session ID to continue a conversation")


class SourceChunk(BaseModel):
    text: str
    metadata: dict[str, Any]


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    provider_used: str
    fallback_used: bool
    session_id: Optional[str] = None
    message_id: Optional[str] = None


class RetrieveRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrieveResponse(BaseModel):
    question: str
    chunks: list[SourceChunk]
