"""
database/crud.py
All CRUD (Create, Read, Update, Delete) operations for the learner profile system.
Each function takes a db: Session argument — no session management inside these functions.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from .models import ChatMessage, ChatSession, QuizAttempt, Student, TopicMastery


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Student ───────────────────────────────────────────────────────────────────

def create_student(db: Session, student_id: str, name: str, email: Optional[str] = None) -> Student:
    student = Student(student_id=student_id, name=name, email=email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student(db: Session, student_id: str) -> Optional[Student]:
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    return db.query(Student).filter(Student.email == email).first()


def update_student(db: Session, student_id: str, name: Optional[str] = None,
                   email: Optional[str] = None) -> Optional[Student]:
    student = get_student(db, student_id)
    if not student:
        return None
    if name is not None:
        student.name = name
    if email is not None:
        student.email = email
    db.commit()
    db.refresh(student)
    return student


# ── ChatSession ───────────────────────────────────────────────────────────────

def create_chat_session(db: Session, student_id: Optional[str] = None,
                        title: Optional[str] = None) -> ChatSession:
    session = ChatSession(student_id=student_id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_chat_session(db: Session, session_id: str) -> Optional[ChatSession]:
    return db.query(ChatSession).filter(ChatSession.session_id == session_id).first()


def get_sessions_for_student(db: Session, student_id: str,
                              limit: int = 20) -> list[ChatSession]:
    return (
        db.query(ChatSession)
        .filter(ChatSession.student_id == student_id)
        .order_by(ChatSession.last_active.desc())
        .limit(limit)
        .all()
    )


def touch_session(db: Session, session_id: str) -> None:
    """Update last_active timestamp for a session."""
    session = get_chat_session(db, session_id)
    if session:
        session.last_active = _now()
        db.commit()


# ── ChatMessage ───────────────────────────────────────────────────────────────

def add_chat_message(
    db: Session,
    session_id: str,
    role: str,
    content: str,
    student_id: Optional[str] = None,
    topics_detected: Optional[list[str]] = None,
    provider_used: Optional[str] = None,
) -> ChatMessage:
    msg = ChatMessage(
        session_id=session_id,
        student_id=student_id,
        role=role,
        content=content,
        topics_detected=topics_detected or [],
        provider_used=provider_used,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    touch_session(db, session_id)
    return msg


def get_session_history(db: Session, session_id: str,
                        limit: int = 50) -> list[ChatMessage]:
    """Return messages in chronological order — Jibin uses this for conversation memory."""
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.timestamp.asc())
        .limit(limit)
        .all()
    )


# ── TopicMastery ──────────────────────────────────────────────────────────────

def upsert_topic_mastery(
    db: Session,
    student_id: str,
    topic_id: int,
    topic_name: str,
    new_score: float,
) -> TopicMastery:
    """Insert or update mastery score for a student-topic pair.
    Uses weighted running average so one bad quiz doesn't crash the score.
    """
    existing = (
        db.query(TopicMastery)
        .filter(TopicMastery.student_id == student_id, TopicMastery.topic_id == topic_id)
        .first()
    )
    if existing:
        # Weighted average: 70% history, 30% new score
        existing.mastery_score = round(0.7 * existing.mastery_score + 0.3 * new_score, 4)
        existing.attempts += 1
        existing.last_tested = _now()
        existing.updated_at = _now()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        mastery = TopicMastery(
            student_id=student_id,
            topic_id=topic_id,
            topic_name=topic_name,
            mastery_score=new_score,
            attempts=1,
            last_tested=_now(),
        )
        db.add(mastery)
        db.commit()
        db.refresh(mastery)
        return mastery


def get_topic_mastery_for_student(db: Session, student_id: str) -> list[TopicMastery]:
    """All topic mastery rows for a student, sorted weakest first.
    Mayank's recommendation engine calls this to find knowledge gaps.
    """
    return (
        db.query(TopicMastery)
        .filter(TopicMastery.student_id == student_id)
        .order_by(TopicMastery.mastery_score.asc())
        .all()
    )


def get_weak_topics(db: Session, student_id: str, threshold: float = 0.4,
                    limit: int = 5) -> list[TopicMastery]:
    """Topics where mastery_score < threshold — direct input for Mayank's gap detection."""
    return (
        db.query(TopicMastery)
        .filter(TopicMastery.student_id == student_id,
                TopicMastery.mastery_score < threshold)
        .order_by(TopicMastery.mastery_score.asc())
        .limit(limit)
        .all()
    )


# ── QuizAttempt ───────────────────────────────────────────────────────────────

def add_quiz_attempt(
    db: Session,
    student_id: str,
    topic_name: str,
    question_text: str,
    topic_id: Optional[int] = None,
    difficulty: str = "medium",
    student_answer: Optional[str] = None,
    correct_answer: Optional[str] = None,
    is_correct: Optional[bool] = None,
    session_id: Optional[str] = None,
    source_chunks: Optional[list[str]] = None,
) -> QuizAttempt:
    attempt = QuizAttempt(
        student_id=student_id,
        session_id=session_id,
        topic_id=topic_id,
        topic_name=topic_name,
        difficulty=difficulty,
        question_text=question_text,
        student_answer=student_answer,
        correct_answer=correct_answer,
        is_correct=is_correct,
        source_chunks=source_chunks or [],
        # llm_score and feedback left NULL — Jibin fills these
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def update_quiz_evaluation(
    db: Session,
    attempt_id: str,
    llm_score: float,
    feedback: str,
    is_correct: Optional[bool] = None,
) -> Optional[QuizAttempt]:
    """Jibin's LLM-as-Judge calls this to store evaluation results."""
    attempt = db.query(QuizAttempt).filter(QuizAttempt.attempt_id == attempt_id).first()
    if not attempt:
        return None
    attempt.llm_score = llm_score
    attempt.feedback = feedback
    if is_correct is not None:
        attempt.is_correct = is_correct
    db.commit()
    db.refresh(attempt)
    return attempt


def get_quiz_history(db: Session, student_id: str,
                     limit: int = 50) -> list[QuizAttempt]:
    return (
        db.query(QuizAttempt)
        .filter(QuizAttempt.student_id == student_id)
        .order_by(QuizAttempt.attempt_time.desc())
        .limit(limit)
        .all()
    )
