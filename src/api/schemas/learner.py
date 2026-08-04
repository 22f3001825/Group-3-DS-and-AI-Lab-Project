"""
api/schemas/learner.py
Pydantic request and response models for learner profile endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ── Student ───────────────────────────────────────────────────────────────────

class StudentCreate(BaseModel):
    student_id: str = Field(..., min_length=1, description="Unique student identifier")
    name: str = Field(..., min_length=1)
    email: Optional[str] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class StudentResponse(BaseModel):
    student_id: str
    name: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ── ChatSession ───────────────────────────────────────────────────────────────

class SessionCreate(BaseModel):
    title: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    student_id: Optional[str]
    title: Optional[str]
    created_at: datetime
    last_active: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message_id: str
    role: str
    content: str
    topics_detected: list[str]
    provider_used: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


# ── TopicMastery ──────────────────────────────────────────────────────────────

class TopicMasteryUpdate(BaseModel):
    topic_id: int
    topic_name: str
    new_score: float = Field(..., ge=0.0, le=1.0)


class TopicMasteryResponse(BaseModel):
    topic_id: int
    topic_name: str
    mastery_score: float
    attempts: int
    last_tested: Optional[datetime]

    class Config:
        from_attributes = True


# ── QuizAttempt ───────────────────────────────────────────────────────────────

class QuizAttemptCreate(BaseModel):
    topic_name: str
    question_text: str
    topic_id: Optional[int] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    student_answer: Optional[str] = None
    correct_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    session_id: Optional[str] = None
    source_chunks: list[str] = []


class QuizAttemptResponse(BaseModel):
    attempt_id: str
    topic_name: str
    difficulty: str
    question_text: str
    student_answer: Optional[str]
    correct_answer: Optional[str]
    is_correct: Optional[bool]
    llm_score: Optional[float]      # filled by Jibin's LLM-as-Judge
    feedback: Optional[str]         # filled by Jibin's evaluator
    attempt_time: datetime

    class Config:
        from_attributes = True
