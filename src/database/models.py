"""
database/models.py
SQLAlchemy ORM models for the MLT learner profile system.

Tables:
  - Student        : core identity
  - ChatSession    : groups messages (conversation memory)
  - ChatMessage    : every Q&A exchange
  - TopicMastery   : per-student per-topic Elo & mastery tracking (recommendation engine)
  - QuizAttempt    : every quiz attempt (quiz eval + LLM-as-Judge)
  - TopicRecommendationEvent : first time a topic entered a student's study plan
                     (the pre/post split point for the quiz improvement metric)
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey,
    Integer, String, Text, UniqueConstraint, JSON, Index,
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
    """Groups a set of messages into one conversation."""
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
    """Per-student per-topic performance score based on Pelánek (2016) Elo Knowledge Tracing.
    
    Attributes:
      - elo_rating        : Continuous skill rating (0.0 = neutral/average, >0 = stronger, <0 = weaker)
      - mastery_score     : Sigmoid-mapped score [0.0, 1.0]
      - attempts          : Total quiz question attempts on this topic
      - streak            : Current consecutive correct answers streak
      - chat_interactions : Number of times this topic was explored in chat
      - last_tested       : Timestamp of last quiz attempt
    """
    __tablename__ = "topic_mastery"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    student_id        = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    topic_id          = Column(Integer, nullable=False)   # matches id in topic_taxonomy.json
    topic_name        = Column(String(255), nullable=False)
    elo_rating        = Column(Float, default=0.0, nullable=False)
    mastery_score     = Column(Float, default=0.5, nullable=False)   # 0.0–1.0
    attempts          = Column(Integer, default=0, nullable=False)
    streak            = Column(Integer, default=0, nullable=False)
    chat_interactions = Column(Integer, default=0, nullable=False)
    last_tested       = Column(DateTime, nullable=True)
    updated_at        = Column(DateTime, default=_now, onupdate=_now, nullable=False)

    student = relationship("Student", back_populates="topic_masteries")

    __table_args__ = (
        UniqueConstraint("student_id", "topic_id", name="uq_student_topic"),
    )


# ── QuizAttempt ───────────────────────────────────────────────────────────────

class QuizAttempt(Base):
    """Every quiz attempt.

    Rows are created UNANSWERED at generation time (student_answer / is_correct NULL)
    and graded later by POST /learner/{id}/quiz/{attempt_id}/answer.

    llm_score and feedback store LLM-as-Judge evaluation results; at generation time
    feedback carries the question's explanation, which grading passes back through.
    source_chunks stores which Qdrant doc_ids the question was generated from.
    options holds the shuffled MCQ option texts as served (empty for short answer) —
    it is what makes re-serving a stored question, validating a submitted answer, and
    the correct-option position check possible.
    """
    __tablename__ = "quiz_attempts"

    attempt_id     = Column(String, primary_key=True, default=_uuid)
    student_id     = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    session_id     = Column(String, ForeignKey("chat_sessions.session_id", ondelete="SET NULL"), nullable=True)
    topic_id       = Column(Integer, nullable=True)
    topic_name     = Column(String(255), nullable=False)
    difficulty     = Column(String(20), default="medium")  # easy | medium | hard
    question_text  = Column(Text, nullable=False)
    options        = Column(JSON, default=list)     # shuffled option texts; [] for short answer
    student_answer = Column(Text, nullable=True)
    correct_answer = Column(Text, nullable=True)
    is_correct     = Column(Boolean, nullable=True)
    llm_score      = Column(Float, nullable=True)   # filled by LLM-as-Judge
    feedback       = Column(Text, nullable=True)    # explanation at generation, judge feedback after
    source_chunks  = Column(JSON, default=list)     # list of doc_id strings used
    reason         = Column(String(32), nullable=True)  # weak|developing|decaying|selected|cached
    attempt_time   = Column(DateTime, default=_now, nullable=False)

    student = relationship("Student", back_populates="quiz_attempts")


# ── TopicRecommendationEvent ──────────────────────────────────────────────────

class TopicRecommendationEvent(Base):
    """First time a topic appeared in a student's study plan.

    Written by recommendation_service.generate_study_plan(). Deliberately a separate
    table rather than a TopicMastery column: mastery rows do not exist for untested,
    unchatted topics — exactly the ones a first recommendation covers — so writing the
    timestamp there would create rows and self-invalidate the recommendation cache
    through get_student_state_fingerprint().
    """
    __tablename__ = "topic_recommendation_events"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    student_id           = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    topic_id             = Column(Integer, nullable=False)
    topic_name           = Column(String(255), nullable=False)
    first_recommended_at = Column(DateTime, default=_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "topic_id", name="uq_student_topic_recommendation"),
    )


# ── Question Intelligence ───────────────────────────────────────────────────
# SQLite (and, unchanged, PostgreSQL through SQLAlchemy) is the authority for the
# question graph. Qdrant stores only embeddings and filter payloads; it is reconciled
# through QuestionBankOutbox and is never the sole record of a unit or a draft.

class QuestionBankVersion(Base):
    __tablename__ = "question_bank_versions"

    version_id = Column(String(36), primary_key=True, default=_uuid)
    status = Column(String(20), nullable=False, default="active")  # building|active|superseded|failed
    embedding_model = Column(String(255), nullable=False)
    thresholds = Column(JSON, default=dict, nullable=False)
    source_summary = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=_now, nullable=False)
    completed_at = Column(DateTime, nullable=True)


class DuplicateGroup(Base):
    __tablename__ = "question_duplicate_groups"

    duplicate_group_id = Column(String(64), primary_key=True)
    canonical_unit_id = Column(String(255), nullable=True, unique=True)
    bank_version_id = Column(String(36), ForeignKey("question_bank_versions.version_id"), nullable=False)
    created_at = Column(DateTime, default=_now, nullable=False)


class ConceptCluster(Base):
    __tablename__ = "question_concept_clusters"

    cluster_id = Column(String(64), primary_key=True)
    bank_version_id = Column(String(36), ForeignKey("question_bank_versions.version_id"), nullable=False)
    title = Column(Text, nullable=False)
    medoid_unit_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=_now, nullable=False)
    updated_at = Column(DateTime, default=_now, onupdate=_now, nullable=False)

    __table_args__ = (Index("ix_question_clusters_version", "bank_version_id"),)


class QuestionUnit(Base):
    __tablename__ = "question_units"

    unit_id = Column(String(255), primary_key=True)
    bank_version_id = Column(String(36), ForeignKey("question_bank_versions.version_id"), nullable=False)
    source_type = Column(String(64), nullable=False)
    source_file = Column(String(512), nullable=False)
    doc_stem = Column(String(255), nullable=False)
    week = Column(Integer, nullable=False, default=0)
    title = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, default=list, nullable=False)
    answer = Column(Text, default="", nullable=False)
    solution = Column(Text, default="", nullable=False)
    origin = Column(String(32), default="corpus", nullable=False)
    is_canonical = Column(Boolean, default=False, nullable=False)
    duplicate_group_id = Column(String(64), ForeignKey("question_duplicate_groups.duplicate_group_id"), nullable=True)
    cluster_id = Column(String(64), ForeignKey("question_concept_clusters.cluster_id"), nullable=True)
    vector_status = Column(String(20), default="pending", nullable=False)  # pending|synced|failed
    created_at = Column(DateTime, default=_now, nullable=False)

    __table_args__ = (
        Index("ix_question_units_source_week", "source_type", "week"),
        Index("ix_question_units_cluster", "cluster_id"),
        Index("ix_question_units_group", "duplicate_group_id"),
    )


class QuestionUnitChunk(Base):
    __tablename__ = "question_unit_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_id = Column(String(255), ForeignKey("question_units.unit_id", ondelete="CASCADE"), nullable=False)
    doc_id = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint("unit_id", "doc_id", name="uq_question_unit_chunk"),
        Index("ix_question_unit_chunks_doc_id", "doc_id"),
    )


class ClusterMember(Base):
    __tablename__ = "question_cluster_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cluster_id = Column(String(64), ForeignKey("question_concept_clusters.cluster_id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(String(255), ForeignKey("question_units.unit_id", ondelete="CASCADE"), nullable=False)
    ordinal = Column(Integer, default=0, nullable=False)

    __table_args__ = (UniqueConstraint("cluster_id", "unit_id", name="uq_question_cluster_member"),)


class QuestionContentDraft(Base):
    __tablename__ = "question_content_drafts"

    draft_id = Column(String(64), primary_key=True)
    origin = Column(String(16), nullable=False)
    status = Column(String(20), nullable=False, default="staged")
    filename = Column(String(512), nullable=True)
    original_markdown = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict, nullable=False)
    preview_json = Column(JSON, default=dict, nullable=False)
    artifact_path = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=_now, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    committed_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)

    __table_args__ = (Index("ix_question_drafts_status_expiry", "status", "expires_at"),)


class QuestionUpload(Base):
    __tablename__ = "question_uploads"

    upload_id = Column(String(36), primary_key=True, default=_uuid)
    draft_id = Column(String(64), ForeignKey("question_content_drafts.draft_id"), nullable=False, unique=True)
    resolved_metadata = Column(JSON, default=dict, nullable=False)
    result_json = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=_now, nullable=False)
    committed_at = Column(DateTime, default=_now, nullable=False)


class QuestionEvaluationLabel(Base):
    __tablename__ = "question_evaluation_labels"

    pair_key = Column(String(600), primary_key=True)
    metric_kind = Column(String(32), nullable=False)
    label = Column(Boolean, nullable=False)
    source = Column(String(32), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_now, nullable=False)
    updated_at = Column(DateTime, default=_now, onupdate=_now, nullable=False)


class QuestionBankOutbox(Base):
    __tablename__ = "question_bank_outbox"

    outbox_id = Column(String(36), primary_key=True, default=_uuid)
    operation = Column(String(16), nullable=False)  # upsert|delete
    unit_id = Column(String(255), nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending|processing|synced|failed
    retry_count = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_now, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    __table_args__ = (Index("ix_question_outbox_status_created", "status", "created_at"),)
