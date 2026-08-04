"""
database/models.py
SQLAlchemy ORM models for the MLT learner profile system.

Tables:
  - Student        : core identity
  - ChatSession    : groups messages (Jibin's conversation memory)
  - ChatMessage    : every Q&A exchange
  - TopicMastery   : per-student per-topic score (Mayank's recommendation engine)
  - QuizAttempt    : every quiz attempt (Jibin's quiz eval + LLM-as-Judge)
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey,
    Integer, String, Text, UniqueConstraint, JSON,
)
from sqlalchemy.orm import relationship

from .session import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


# ── Student ───────────────────────────────────────────────────────────────────

class Student(Base):
    __tablename__ = "students"

    student_id  = Column(String, primary_key=True, default=_uuid)
    name        = Column(String(255), nullable=False)
    email       = Column(String(255), unique=True, nullable=True)
    created_at  = Column(DateTime, default=_now, nullable=False)

    # Relationships
    sessions        = relationship("ChatSession",  back_populates="student", cascade="all, delete-orphan")
    topic_masteries = relationship("TopicMastery", back_populates="student", cascade="all, delete-orphan")
    quiz_attempts   = relationship("QuizAttempt",  back_populates="student", cascade="all, delete-orphan")


# ── ChatSession ───────────────────────────────────────────────────────────────

class ChatSession(Base):
    """Groups a set of messages into one conversation.
    Jibin's conversation memory loads ChatMessages from a given session_id.
    """
    __tablename__ = "chat_sessions"

    session_id  = Column(String, primary_key=True, default=_uuid)
    student_id  = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=True)
    title       = Column(String(255), nullable=True)   # optional label
    created_at  = Column(DateTime, default=_now, nullable=False)
    last_active = Column(DateTime, default=_now, onupdate=_now, nullable=False)

    student  = relationship("Student",     back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan",
                            order_by="ChatMessage.timestamp")


# ── ChatMessage ───────────────────────────────────────────────────────────────

class ChatMessage(Base):
    """Every single Q&A exchange stored for history and memory.
    topics_detected is populated by matching returned source chunk topic_tags.
    """
    __tablename__ = "chat_messages"

    message_id      = Column(String, primary_key=True, default=_uuid)
    session_id      = Column(String, ForeignKey("chat_sessions.session_id", ondelete="CASCADE"), nullable=False)
    student_id      = Column(String, ForeignKey("students.student_id",  ondelete="SET NULL"),  nullable=True)
    role            = Column(String(20), nullable=False)   # 'user' | 'assistant'
    content         = Column(Text, nullable=False)
    topics_detected = Column(JSON, default=list)           # e.g. ["Logistic Regression", "SVM"]
    provider_used   = Column(String(100), nullable=True)   # e.g. "gemini/gemini-2.0-flash"
    timestamp       = Column(DateTime, default=_now, nullable=False)

    session = relationship("ChatSession", back_populates="messages")


# ── TopicMastery ──────────────────────────────────────────────────────────────

class TopicMastery(Base):
    """Per-student per-topic performance score.
    Mayank's knowledge gap detection and recommendation engine query this table directly.
    mastery_score: 0.0 = never attempted / very weak, 1.0 = fully mastered.
    """
    __tablename__ = "topic_mastery"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    student_id    = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    topic_id      = Column(Integer, nullable=False)   # matches id in topic_taxonomy.json
    topic_name    = Column(String(255), nullable=False)
    mastery_score = Column(Float, default=0.5, nullable=False)   # 0.0–1.0
    attempts      = Column(Integer, default=0, nullable=False)
    last_tested   = Column(DateTime, nullable=True)
    updated_at    = Column(DateTime, default=_now, onupdate=_now, nullable=False)

    student = relationship("Student", back_populates="topic_masteries")

    __table_args__ = (
        UniqueConstraint("student_id", "topic_id", name="uq_student_topic"),
    )


# ── QuizAttempt ───────────────────────────────────────────────────────────────

class QuizAttempt(Base):
    """Every quiz attempt.
    llm_score and feedback are left NULL by Milestone 5 — Jibin (Person 5) fills them
    when implementing LLM-as-Judge quiz evaluation.
    source_chunks stores which Qdrant doc_ids were used to generate the question.
    """
    __tablename__ = "quiz_attempts"

    attempt_id     = Column(String, primary_key=True, default=_uuid)
    student_id     = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    session_id     = Column(String, ForeignKey("chat_sessions.session_id", ondelete="SET NULL"), nullable=True)
    topic_id       = Column(Integer, nullable=True)
    topic_name     = Column(String(255), nullable=False)
    difficulty     = Column(String(20), default="medium")  # easy | medium | hard
    question_text  = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=True)
    correct_answer = Column(Text, nullable=True)
    is_correct     = Column(Boolean, nullable=True)
    llm_score      = Column(Float, nullable=True)   # filled by Jibin's LLM-as-Judge
    feedback       = Column(Text, nullable=True)    # filled by Jibin's evaluator
    source_chunks  = Column(JSON, default=list)     # list of doc_id strings used
    attempt_time   = Column(DateTime, default=_now, nullable=False)

    student = relationship("Student", back_populates="quiz_attempts")
