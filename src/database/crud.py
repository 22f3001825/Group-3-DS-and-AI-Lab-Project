"""
database/crud.py
All CRUD (Create, Read, Update, Delete) operations for the learner profile system.
Each function takes a db: Session argument — no session management inside these functions.
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import (
    ChatMessage, ChatSession, QuizAttempt, Student, TopicMastery,
    TopicRecommendationEvent,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


class AlreadyGradedError(Exception):
    """Raised when a quiz attempt that already carries an outcome is graded again.

    Re-grading would re-run the Elo update and double-count the attempt, which is the
    same corruption class as feeding fabricated outcomes into the model.
    """


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


def get_or_create_student(db: Session, student_id: str, name: str = "Student") -> Student:
    """Auto-create by id. NOT for request paths — identity comes from the Google token.

    Kept for `src/evaluate_quiz.py`, which invents a synthetic student per run and has
    nothing to authenticate. Every API handler that used to call this now resolves the
    student through `assert_self_or_admin` instead, so an unknown id 404s rather than
    silently minting a profile.
    """
    student = get_student(db, student_id)
    if not student:
        student = create_student(db, student_id=student_id, name=name)
    return student


def set_student_active(db: Session, student_id: str, is_active: bool) -> Optional[Student]:
    """The writer behind PATCH /learner/{id}/status. Nothing the student produced is touched."""
    student = get_student(db, student_id)
    if not student:
        return None
    student.is_active = is_active
    student.updated_at = _now()
    db.commit()
    db.refresh(student)
    return student


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
    """Return messages in chronological order."""
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.timestamp.asc())
        .limit(limit)
        .all()
    )


# ── TopicMastery & Knowledge Tracing ──────────────────────────────────────────

# Item-difficulty term (Pelánek 2016). An `easy` item is worth less when answered
# correctly and costs more when missed; a `hard` item the reverse. `medium` is offset 0,
# so every pre-existing caller keeps today's exact arithmetic.
_DIFFICULTY_OFFSET: dict[str, float] = {"easy": -100.0, "medium": 0.0, "hard": 100.0}


def update_topic_mastery_elo(
    db: Session,
    student_id: str,
    topic_id: int,
    topic_name: str,
    is_correct: bool,
    difficulty: str = "medium",
    outcome: Optional[float] = None,
) -> TopicMastery:
    """Update student topic mastery using the Pelánek (2016) Elo rating algorithm.

    Formula:
      Expected = 1 / (1 + 10^(-(R - d) / 400))     d = item difficulty offset
      K = max(16, 64 / (1 + 0.1 * attempts))
      R_new = R_old + K * (Outcome - Expected)
      Mastery = 1 / (1 + 10^(-R_new / 400))

    Args:
      difficulty: 'easy' | 'medium' | 'hard' — sets the item difficulty offset d.
      outcome:    Optional continuous outcome in [0, 1] (LLM-as-Judge score for a
                  short answer). Defaults to the binary is_correct.
    """
    existing = (
        db.query(TopicMastery)
        .filter(TopicMastery.student_id == student_id, TopicMastery.topic_id == topic_id)
        .first()
    )

    if outcome is None:
        actual = 1.0 if is_correct else 0.0
    else:
        actual = min(1.0, max(0.0, float(outcome)))

    d = _DIFFICULTY_OFFSET.get((difficulty or "medium").lower(), 0.0)

    if existing:
        current_elo = existing.elo_rating or 0.0
        attempts = existing.attempts or 0

        # Dynamic learning rate K (shrinks with experience for stability)
        K = max(16.0, 64.0 / (1.0 + 0.1 * attempts))

        # Expected score against item difficulty
        expected = 1.0 / (1.0 + math.pow(10.0, -(current_elo - d) / 400.0))

        # Elo rating update
        new_elo = round(current_elo + K * (actual - expected), 4)

        # Map Elo to continuous mastery probability in [0.0, 1.0]
        new_mastery = round(1.0 / (1.0 + math.pow(10.0, -new_elo / 400.0)), 4)

        existing.elo_rating = new_elo
        existing.mastery_score = new_mastery
        existing.attempts = attempts + 1
        existing.streak = (existing.streak + 1) if is_correct else 0
        existing.last_tested = _now()
        existing.updated_at = _now()

        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Initial attempt starting from neutral Elo (0.0) with K=64
        K = 64.0
        expected = 1.0 / (1.0 + math.pow(10.0, d / 400.0))
        init_elo = round(0.0 + K * (actual - expected), 4)
        init_mastery = round(1.0 / (1.0 + math.pow(10.0, -init_elo / 400.0)), 4)

        mastery = TopicMastery(
            student_id=student_id,
            topic_id=topic_id,
            topic_name=topic_name,
            elo_rating=init_elo,
            mastery_score=init_mastery,
            attempts=1,
            streak=1 if is_correct else 0,
            chat_interactions=0,
            last_tested=_now(),
        )
        db.add(mastery)
        db.commit()
        db.refresh(mastery)
        return mastery


def record_chat_topic_interaction(
    db: Session,
    student_id: str,
    topic_id: int,
    topic_name: str,
) -> TopicMastery:
    """Record that a student explored a topic in chat.
    
    If the topic is untested, initializes a baseline record with 0.0 Elo (0.50 mastery).
    Increments the chat_interactions counter.
    """
    existing = (
        db.query(TopicMastery)
        .filter(TopicMastery.student_id == student_id, TopicMastery.topic_id == topic_id)
        .first()
    )
    if existing:
        existing.chat_interactions = (existing.chat_interactions or 0) + 1
        existing.updated_at = _now()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        mastery = TopicMastery(
            student_id=student_id,
            topic_id=topic_id,
            topic_name=topic_name,
            elo_rating=0.0,
            mastery_score=0.5,
            attempts=0,
            streak=0,
            chat_interactions=1,
            last_tested=None,
        )
        db.add(mastery)
        db.commit()
        db.refresh(mastery)
        return mastery


def upsert_topic_mastery(
    db: Session,
    student_id: str,
    topic_id: int,
    topic_name: str,
    new_score: float,
) -> TopicMastery:
    """Backward-compatible helper: Updates mastery score and maps to Elo."""
    is_correct = new_score >= 0.5
    return update_topic_mastery_elo(db, student_id, topic_id, topic_name, is_correct)


def get_topic_mastery_for_student(db: Session, student_id: str) -> list[TopicMastery]:
    """All topic mastery rows for a student, sorted weakest first."""
    return (
        db.query(TopicMastery)
        .filter(TopicMastery.student_id == student_id)
        .order_by(TopicMastery.mastery_score.asc())
        .all()
    )


def get_weak_topics(db: Session, student_id: str, threshold: float = 0.4,
                    limit: int = 5) -> list[TopicMastery]:
    """Topics where mastery_score < threshold — direct input for gap detection."""
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
    options: Optional[list[str]] = None,
    feedback: Optional[str] = None,
    reason: Optional[str] = None,
) -> QuizAttempt:
    """Create a quiz attempt row.

    Generated-but-unanswered questions are created here with student_answer and
    is_correct left NULL; `feedback` carries the question's explanation until grading.
    """
    attempt = QuizAttempt(
        student_id=student_id,
        session_id=session_id,
        topic_id=topic_id,
        topic_name=topic_name,
        difficulty=difficulty,
        question_text=question_text,
        options=options or [],
        student_answer=student_answer,
        correct_answer=correct_answer,
        is_correct=is_correct,
        feedback=feedback,
        source_chunks=source_chunks or [],
        reason=reason,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def get_quiz_attempt(db: Session, attempt_id: str) -> Optional[QuizAttempt]:
    return db.query(QuizAttempt).filter(QuizAttempt.attempt_id == attempt_id).first()


def update_quiz_evaluation(
    db: Session,
    attempt_id: str,
    llm_score: float,
    feedback: str,
    is_correct: Optional[bool] = None,
    student_answer: Optional[str] = None,
    outcome: Optional[float] = None,
    allow_regrade: bool = False,
) -> Optional[QuizAttempt]:
    """Store quiz evaluation results and update topic mastery accordingly.

    Raises AlreadyGradedError if the attempt already carries an outcome — a second
    call would re-run the Elo update and double-count the attempt. Pass
    allow_regrade=True only when the mastery side-effect is deliberately repeated.

    The Elo update uses the attempt's own difficulty, so a correct hard answer moves
    mastery further than a correct easy one.
    """
    attempt = db.query(QuizAttempt).filter(QuizAttempt.attempt_id == attempt_id).first()
    if not attempt:
        return None
    if attempt.is_correct is not None and not allow_regrade:
        raise AlreadyGradedError(f"Quiz attempt {attempt_id} has already been graded.")

    attempt.llm_score = llm_score
    attempt.feedback = feedback
    if student_answer is not None:
        attempt.student_answer = student_answer
    if is_correct is not None:
        attempt.is_correct = is_correct

    # If topic_id is known, update mastery
    if attempt.topic_id is not None and is_correct is not None:
        update_topic_mastery_elo(
            db,
            student_id=attempt.student_id,
            topic_id=attempt.topic_id,
            topic_name=attempt.topic_name,
            is_correct=is_correct,
            difficulty=attempt.difficulty or "medium",
            outcome=outcome,
        )

    db.commit()
    db.refresh(attempt)
    return attempt


def get_quiz_history(db: Session, student_id: str,
                     limit: int = 50,
                     answered_only: bool = True) -> list[QuizAttempt]:
    """Most recent quiz attempts, newest first.

    answered_only excludes generated-but-unanswered rows: those are not attempts yet
    and must not appear in history or in accuracy statistics.
    """
    q = db.query(QuizAttempt).filter(QuizAttempt.student_id == student_id)
    if answered_only:
        q = q.filter(QuizAttempt.is_correct.isnot(None))
    return q.order_by(QuizAttempt.attempt_time.desc()).limit(limit).all()


def get_quiz_stats(db: Session, student_id: str) -> tuple[int, int]:
    """Lifetime (answered_total, correct_total) — not windowed, unlike get_quiz_history."""
    total = (
        db.query(func.count(QuizAttempt.attempt_id))
        .filter(QuizAttempt.student_id == student_id,
                QuizAttempt.is_correct.isnot(None))
        .scalar()
        or 0
    )
    correct = (
        db.query(func.count(QuizAttempt.attempt_id))
        .filter(QuizAttempt.student_id == student_id,
                QuizAttempt.is_correct.is_(True))
        .scalar()
        or 0
    )
    return int(total), int(correct)


def get_attempts_for_topic(db: Session, student_id: str, topic_id: int,
                           limit: int = 20,
                           answered_only: bool = False) -> list[QuizAttempt]:
    """Recent attempts on one topic — used for the near-duplicate question check."""
    q = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id,
        QuizAttempt.topic_id == topic_id,
    )
    if answered_only:
        q = q.filter(QuizAttempt.is_correct.isnot(None))
    return q.order_by(QuizAttempt.attempt_time.desc()).limit(limit).all()


def get_topic_ids_answered_since(db: Session, student_id: str,
                                 hours: int = 24) -> set[int]:
    """Topic ids this student has *answered* within the window (generated rows excluded)."""
    cutoff = _now() - timedelta(hours=hours)
    rows = (
        db.query(QuizAttempt.topic_id)
        .filter(QuizAttempt.student_id == student_id,
                QuizAttempt.is_correct.isnot(None),
                QuizAttempt.attempt_time >= cutoff,
                QuizAttempt.topic_id.isnot(None))
        .distinct()
        .all()
    )
    return {r[0] for r in rows}


def get_reusable_questions(db: Session, student_id: str,
                           topic_ids: Optional[list[int]] = None,
                           not_seen_days: int = 7,
                           limit: int = 10) -> list[QuizAttempt]:
    """Previously generated questions that can be re-served to this student.

    A question is reusable when it has stored options and a correct answer, and the
    same question text has not been served to this student within not_seen_days.
    Scoped to one student's own history by design — no cross-student question bank.
    """
    q = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id,
        QuizAttempt.correct_answer.isnot(None),
    )
    if topic_ids:
        q = q.filter(QuizAttempt.topic_id.in_(topic_ids))
    candidates = q.order_by(QuizAttempt.attempt_time.desc()).limit(200).all()

    cutoff = _now() - timedelta(days=not_seen_days)
    recent_texts = set()
    for row in candidates:
        served = row.attempt_time
        if served is not None and served.tzinfo is None:
            served = served.replace(tzinfo=timezone.utc)
        if served is not None and served >= cutoff:
            recent_texts.add((row.question_text or "").strip().lower())

    seen: set[str] = set()
    out: list[QuizAttempt] = []
    for row in candidates:
        key = (row.question_text or "").strip().lower()
        if not row.options or key in recent_texts or key in seen:
            continue
        seen.add(key)
        out.append(row)
        if len(out) >= limit:
            break
    return out


# ── TopicRecommendationEvent ──────────────────────────────────────────────────

def record_recommendation_event(db: Session, student_id: str, topic_id: int,
                                topic_name: str) -> TopicRecommendationEvent:
    """Stamp the first time a topic entered this student's study plan (idempotent)."""
    existing = (
        db.query(TopicRecommendationEvent)
        .filter(TopicRecommendationEvent.student_id == student_id,
                TopicRecommendationEvent.topic_id == topic_id)
        .first()
    )
    if existing:
        return existing
    event = TopicRecommendationEvent(
        student_id=student_id,
        topic_id=topic_id,
        topic_name=topic_name,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_recommendation_events(db: Session,
                              student_id: Optional[str] = None) -> list[TopicRecommendationEvent]:
    q = db.query(TopicRecommendationEvent)
    if student_id:
        q = q.filter(TopicRecommendationEvent.student_id == student_id)
    return q.order_by(TopicRecommendationEvent.first_recommended_at.asc()).all()
