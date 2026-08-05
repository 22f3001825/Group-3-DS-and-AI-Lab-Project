"""
api/routers/learner.py
Learner profile, recommendation engine, and knowledge analytics endpoints.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...database.session import get_db
from ...database import crud
from ..dependencies import get_retriever
from ..schemas.learner import (
    GeneratedQuestion, LearnerProfileResponse, MessageResponse, QuizAnswerRequest,
    QuizAnswerResponse, QuizAttemptCreate, QuizAttemptResponse, QuizGenerateRequest,
    QuizReadinessResponse, RecommendationResponse, SessionCreate, SessionResponse,
    StudentCreate, StudentResponse, StudentUpdate, TopicMasteryResponse,
    TopicMasteryUpdate, WeekMasteryOverview,
)
from ..services import quiz_service
from ..services.recommendation_service import (
    analyze_knowledge_state, generate_study_plan, get_week_by_week_mastery,
    invalidate_recommendation_cache, load_taxonomy,
)

router = APIRouter(tags=["Learner"])


# ── Student ───────────────────────────────────────────────────────────────────

@router.post("/learner", response_model=StudentResponse, status_code=201)
def create_student(body: StudentCreate, db: Session = Depends(get_db)):
    if crud.get_student(db, body.student_id):
        raise HTTPException(status_code=409, detail="Student ID already exists.")
    return crud.create_student(db, body.student_id, body.name, body.email)


@router.get("/learner/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        # Automatically initialize student profile for seamless UX
        student = crud.create_student(db, student_id=student_id, name=f"Student {student_id[:6]}")
    return student


@router.put("/learner/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, body: StudentUpdate, db: Session = Depends(get_db)):
    student = crud.update_student(db, student_id, body.name, body.email)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


# ── Topic Mastery ─────────────────────────────────────────────────────────────

@router.get("/learner/{student_id}/mastery", response_model=list[TopicMasteryResponse])
def get_mastery(student_id: str, db: Session = Depends(get_db)):
    """Returns all topic mastery rows sorted weakest first."""
    student = crud.get_or_create_student(db, student_id)
    return crud.get_topic_mastery_for_student(db, student_id)


@router.put("/learner/{student_id}/mastery", response_model=TopicMasteryResponse)
def update_mastery(student_id: str, body: TopicMasteryUpdate, db: Session = Depends(get_db)):
    student = crud.get_or_create_student(db, student_id)
    is_correct = body.new_score >= 0.5
    res = crud.update_topic_mastery_elo(
        db, student_id, body.topic_id, body.topic_name, is_correct
    )
    invalidate_recommendation_cache(student_id)
    return res


# ── Recommendations & Gap Analysis ────────────────────────────────────────────

@router.get("/learner/{student_id}/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    student_id: str,
    top_n: int = 5,
    force_refresh: bool = Query(False, description="Force LLM study plan regeneration"),
    db: Session = Depends(get_db),
):
    """Generate personalized study recommendations with state-fingerprint caching."""
    crud.get_or_create_student(db, student_id)
    return generate_study_plan(db, student_id, top_n=top_n, force_refresh=force_refresh)


@router.get("/learner/{student_id}/profile", response_model=LearnerProfileResponse)
def get_learner_profile(student_id: str, db: Session = Depends(get_db)):
    """Get complete learner profile with overall stats, week heatmaps, and quiz history."""
    student = crud.get_or_create_student(db, student_id)
    analysis = analyze_knowledge_state(db, student_id)
    weeks_data = get_week_by_week_mastery(db, student_id)
    quiz_history = crud.get_quiz_history(db, student_id, limit=20)

    # Lifetime totals, not the last-20 window, and generated-but-unanswered questions
    # count in neither the numerator nor the denominator.
    total_quizzes, correct_quizzes = crud.get_quiz_stats(db, student_id)
    accuracy_pct = int(round(correct_quizzes / max(1, total_quizzes) * 100)) if total_quizzes > 0 else 0

    return {
        "student": student,
        "overall_mastery_pct": analysis["overall_mastery_pct"],
        "total_topics_tested": analysis["topics_tested"],
        "total_topics": analysis["total_topics"],
        "coverage_pct": analysis["coverage_pct"],
        "total_quizzes_taken": total_quizzes,
        "quiz_accuracy_pct": accuracy_pct,
        "weeks": weeks_data,
        "recent_quiz_attempts": quiz_history,
    }


# ── Chat Sessions ─────────────────────────────────────────────────────────────

@router.post("/learner/{student_id}/session", response_model=SessionResponse, status_code=201)
def create_session(student_id: str, body: SessionCreate, db: Session = Depends(get_db)):
    crud.get_or_create_student(db, student_id)
    return crud.create_chat_session(db, student_id=student_id, title=body.title)


@router.get("/learner/{student_id}/sessions", response_model=list[SessionResponse])
def list_sessions(student_id: str, db: Session = Depends(get_db)):
    crud.get_or_create_student(db, student_id)
    return crud.get_sessions_for_student(db, student_id)


@router.get("/session/{session_id}/history", response_model=list[MessageResponse])
def get_history(session_id: str, db: Session = Depends(get_db)):
    session = crud.get_chat_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return crud.get_session_history(db, session_id)


# ── Quiz Attempts ─────────────────────────────────────────────────────────────

@router.get("/learner/{student_id}/quiz/readiness", response_model=QuizReadinessResponse)
def get_quiz_readiness(student_id: str, db: Session = Depends(get_db)):
    """Is the personalized quiz available to this student yet, and if not, how far off?

    Thresholds live in `src/config.py`. `attempted_topics` is the pool the personalized
    quiz draws from.
    """
    crud.get_or_create_student(db, student_id)
    return quiz_service.personalization_readiness(db, student_id)


@router.post("/learner/{student_id}/quiz/generate", response_model=list[GeneratedQuestion])
def generate_quiz(
    student_id: str,
    body: QuizGenerateRequest,
    db: Session = Depends(get_db),
    retriever=Depends(get_retriever),
):
    """Generate grounded questions for this student.

    With `topic_id` this is the topic-wise quiz — any topic, always available. Without
    it this is the personalized path, which unlocks only once the student has practised
    enough (see `src/config.py`) and then targets the weakest of the topics they have
    already attempted. Questions are persisted unanswered; the response carries no
    correct answer and no explanation.

    Plain `def`, not `async def`: retrieval and the LLM call are blocking, so FastAPI
    must run this in its threadpool rather than on the event loop.
    """
    crud.get_or_create_student(db, student_id)
    try:
        return quiz_service.generate_quiz(
            db,
            student_id,
            retriever,
            topic_id=body.topic_id,
            difficulty=body.difficulty,
            count=body.count,
            question_type=body.question_type,
        )
    except quiz_service.TopicNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except quiz_service.PersonalizationNotReadyError as exc:
        # Structured detail so the client can tell this 409 from the already-graded one
        # and render progress instead of a bare refusal.
        raise HTTPException(
            status_code=409,
            detail={"code": "personalization_not_ready", "message": str(exc), **exc.readiness},
        ) from exc
    except quiz_service.QuizGenerationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/learner/{student_id}/quiz/{attempt_id}/answer", response_model=QuizAnswerResponse)
def answer_quiz_question(
    student_id: str,
    attempt_id: str,
    body: QuizAnswerRequest,
    db: Session = Depends(get_db),
):
    """Grade one generated question and feed the outcome back into the learner profile."""
    try:
        return quiz_service.grade_attempt(db, student_id, attempt_id, body.student_answer)
    except quiz_service.AttemptNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except crud.AlreadyGradedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except quiz_service.InvalidAnswerError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except quiz_service.JudgeUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/learner/{student_id}/quiz", response_model=QuizAttemptResponse, status_code=201,
             deprecated=True)
def create_quiz_attempt(student_id: str, body: QuizAttemptCreate, db: Session = Depends(get_db)):
    """Deprecated direct-write path — the client supplies its own question and outcome.

    Use POST /learner/{id}/quiz/generate + /quiz/{attempt_id}/answer instead: this
    endpoint trusts a client-side grade, which is how fabricated outcomes reached the
    Elo model in the first place.
    """
    crud.get_or_create_student(db, student_id)
    attempt = crud.add_quiz_attempt(
        db,
        student_id=student_id,
        topic_name=body.topic_name,
        question_text=body.question_text,
        topic_id=body.topic_id,
        difficulty=body.difficulty,
        student_answer=body.student_answer,
        correct_answer=body.correct_answer,
        is_correct=body.is_correct,
        session_id=body.session_id,
        source_chunks=body.source_chunks,
    )
    # Auto-update mastery score via Elo
    if body.is_correct is not None and body.topic_id is not None:
        crud.update_topic_mastery_elo(
            db,
            student_id=student_id,
            topic_id=body.topic_id,
            topic_name=body.topic_name,
            is_correct=body.is_correct,
        )
    invalidate_recommendation_cache(student_id)
    return attempt


@router.get("/learner/{student_id}/quiz", response_model=list[QuizAttemptResponse])
def get_quiz_history(
    student_id: str,
    include_pending: bool = Query(False, description="Include generated-but-unanswered questions"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Answered attempts only by default — pending questions are not attempts yet.

    Even with include_pending=true the response model blanks correct_answer and
    feedback on ungraded rows, so a live question's answer never leaks here.
    """
    crud.get_or_create_student(db, student_id)
    return crud.get_quiz_history(db, student_id, limit=limit, answered_only=not include_pending)


# ── Topic Taxonomy ────────────────────────────────────────────────────────────

@router.get("/topics", response_model=list[dict])
def get_all_topics():
    """Returns the full topic taxonomy including DAG prerequisites and lecture refs."""
    return load_taxonomy()


@router.get("/topics/week/{week}", response_model=list[dict])
def get_topics_for_week(week: int):
    """Returns topics for a specific week."""
    taxonomy = load_taxonomy()
    result = [t for t in taxonomy if t["week"] == week]
    if not result:
        raise HTTPException(status_code=404, detail=f"No topics found for week {week}.")
    return result
