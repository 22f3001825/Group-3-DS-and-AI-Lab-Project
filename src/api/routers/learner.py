"""
api/routers/learner.py
Learner profile, recommendation engine, and knowledge analytics endpoints.

**Identity comes from the bearer token, never from the URL.** Every `{student_id}`
handler depends on `get_current_student` and opens with `assert_self_or_admin`, which
returns the id to actually use — so the path parameter is a claim that has to match, and
`"me"` is the idiomatic way to address yourself. Admins may address anyone.

The endpoints below no longer auto-create students. `crud.get_or_create_student` is kept
for `src/evaluate_quiz.py`, a CLI harness with synthetic ids and nothing to authenticate,
but a *request* can only reach a row that a Google login created.

`GET /topics` and `GET /topics/week/{week}` stay public: static course taxonomy, no
learner data, and keeping them open avoids a chicken-and-egg on the login page.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...database.session import get_db
from ...database import crud
from ...database.models import Student
from ..dependencies import assert_self_or_admin, get_current_student, get_retriever, require_admin
from ..schemas.learner import (
    GeneratedQuestion, LearnerProfileResponse, MessageResponse, QuizAnswerRequest,
    QuizAnswerResponse, QuizAttemptCreate, QuizAttemptResponse, QuizGenerateRequest,
    QuizReadinessResponse, RecommendationResponse, SessionCreate, SessionResponse,
    StudentResponse, StudentStatusUpdate, StudentUpdate, TopicMasteryResponse,
    TopicMasteryUpdate, WeekMasteryOverview,
)
from ..services import quiz_service
from ..services.recommendation_service import (
    analyze_knowledge_state, generate_study_plan, get_week_by_week_mastery,
    invalidate_recommendation_cache, load_taxonomy,
)

router = APIRouter(tags=["Learner"])


# ── Student ───────────────────────────────────────────────────────────────────

# `POST /learner` is gone deliberately. It took `student_id` and `email` from the body,
# which under Google identity is an endpoint for squatting the unique-email index at an
# arbitrary id — anyone who knew a victim's address could permanently block their first
# login by colliding with it. Admin-gating would not have fixed that, because there is no
# legitimate caller: rows are created by `/auth/google` from verified Google claims.

@router.get("/learner/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db),
                current: Student = Depends(get_current_student)):
    student_id = assert_self_or_admin(student_id, current)
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.put("/learner/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, body: StudentUpdate, db: Session = Depends(get_db),
                   current: Student = Depends(get_current_student)):
    """Name only. Google owns the address that authenticates the row, so `email` is not
    editable here — accepting one would be the same index squat one step removed."""
    student_id = assert_self_or_admin(student_id, current)
    student = crud.update_student(db, student_id, body.name)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.patch("/learner/{student_id}/status", response_model=StudentResponse)
def set_student_status(student_id: str, body: StudentStatusUpdate,
                       db: Session = Depends(get_db),
                       _: Any = Depends(require_admin)):
    """Activate or deactivate an account. The writer for `is_active`.

    Deactivation is refused at sign-in *and* at every request, so it takes effect
    immediately rather than at token expiry. Nothing the student produced is deleted.
    """
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return crud.set_student_active(db, student_id, body.is_active)


# ── Topic Mastery ─────────────────────────────────────────────────────────────

@router.get("/learner/{student_id}/mastery", response_model=list[TopicMasteryResponse])
def get_mastery(student_id: str, db: Session = Depends(get_db),
                current: Student = Depends(get_current_student)):
    """Returns all topic mastery rows sorted weakest first."""
    student_id = assert_self_or_admin(student_id, current)
    return crud.get_topic_mastery_for_student(db, student_id)


@router.put("/learner/{student_id}/mastery", response_model=TopicMasteryResponse)
def update_mastery(student_id: str, body: TopicMasteryUpdate, db: Session = Depends(get_db),
                   current: Student = Depends(get_current_student)):
    student_id = assert_self_or_admin(student_id, current)
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
    current: Student = Depends(get_current_student),
):
    """Generate personalized study recommendations with state-fingerprint caching."""
    student_id = assert_self_or_admin(student_id, current)
    return generate_study_plan(db, student_id, top_n=top_n, force_refresh=force_refresh)


@router.get("/learner/{student_id}/profile", response_model=LearnerProfileResponse)
def get_learner_profile(student_id: str, db: Session = Depends(get_db),
                        current: Student = Depends(get_current_student)):
    """Get complete learner profile with overall stats, week heatmaps, and quiz history."""
    student_id = assert_self_or_admin(student_id, current)
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
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
def create_session(student_id: str, body: SessionCreate, db: Session = Depends(get_db),
                   current: Student = Depends(get_current_student)):
    student_id = assert_self_or_admin(student_id, current)
    return crud.create_chat_session(db, student_id=student_id, title=body.title)


@router.get("/learner/{student_id}/sessions", response_model=list[SessionResponse])
def list_sessions(student_id: str, db: Session = Depends(get_db),
                  current: Student = Depends(get_current_student)):
    student_id = assert_self_or_admin(student_id, current)
    return crud.get_sessions_for_student(db, student_id)


@router.get("/session/{session_id}/history", response_model=list[MessageResponse])
def get_history(session_id: str, db: Session = Depends(get_db),
                current: Student = Depends(get_current_student)):
    """A session's transcript, for its owner (or an admin).

    This endpoint had no ownership check of any kind: a session id was the whole
    credential, and ids are sequential-ish UUIDs handed out in every chat response.
    """
    session = crud.get_chat_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.student_id != current.student_id and not current.is_admin:
        # 404, not 403: whether a session id exists is itself information, and the caller
        # has no legitimate way to know either way.
        raise HTTPException(status_code=404, detail="Session not found.")
    return crud.get_session_history(db, session_id)


# ── Quiz Attempts ─────────────────────────────────────────────────────────────

@router.get("/learner/{student_id}/quiz/readiness", response_model=QuizReadinessResponse)
def get_quiz_readiness(student_id: str, db: Session = Depends(get_db),
                       current: Student = Depends(get_current_student)):
    """Is the personalized quiz available to this student yet, and if not, how far off?

    Thresholds live in `src/config.py`. `attempted_topics` is the pool the personalized
    quiz draws from.
    """
    student_id = assert_self_or_admin(student_id, current)
    return quiz_service.personalization_readiness(db, student_id)


@router.post("/learner/{student_id}/quiz/generate", response_model=list[GeneratedQuestion])
def generate_quiz(
    student_id: str,
    body: QuizGenerateRequest,
    db: Session = Depends(get_db),
    retriever=Depends(get_retriever),
    current: Student = Depends(get_current_student),
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
    student_id = assert_self_or_admin(student_id, current)
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
    current: Student = Depends(get_current_student),
):
    """Grade one generated question and feed the outcome back into the learner profile.

    `grade_attempt` already refuses an attempt belonging to someone else; pinning the path
    parameter to the token is what finally makes that check mean something.
    """
    student_id = assert_self_or_admin(student_id, current)
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
def create_quiz_attempt(student_id: str, body: QuizAttemptCreate, db: Session = Depends(get_db),
                        current: Student = Depends(get_current_student)):
    """Deprecated direct-write path — the client supplies the question, the server grades it.

    Prefer POST /learner/{id}/quiz/generate + /quiz/{attempt_id}/answer, which also keeps the
    answer server-side until the student has committed to one. This endpoint remains for
    callers that already hold a question, but `body.is_correct` is **ignored**: the outcome is
    recomputed here through the same `quiz_service.grade_answer` every other quiz uses, so a
    client can no longer post a verdict of its own into the Elo mastery model.

    Grading follows the answer's shape — `options` present means MCQ and exact matching,
    absent means short answer and the LLM judge. An attempt with no `student_answer` is
    stored unanswered and moves no mastery.
    """
    student_id = assert_self_or_admin(student_id, current)

    answer = (body.student_answer or "").strip()
    graded = None
    if answer:
        if not (body.correct_answer or "").strip():
            raise HTTPException(
                status_code=400,
                detail="correct_answer is required when student_answer is supplied — the "
                       "server grades the attempt and will not accept a client verdict.",
            )
        try:
            graded = quiz_service.grade_answer(
                body.question_text, body.options, body.correct_answer, answer,
                body.feedback or "",
            )
        except quiz_service.InvalidAnswerError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except quiz_service.JudgeUnavailableError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    attempt = crud.add_quiz_attempt(
        db,
        student_id=student_id,
        topic_name=body.topic_name,
        question_text=body.question_text,
        topic_id=body.topic_id,
        difficulty=body.difficulty,
        student_answer=body.student_answer,
        correct_answer=body.correct_answer,
        is_correct=graded["is_correct"] if graded else None,
        session_id=body.session_id,
        source_chunks=body.source_chunks,
        options=body.options,
        feedback=graded["feedback"] if graded else body.feedback,
    )
    if graded is not None:
        attempt.llm_score = graded["llm_score"]
        db.commit()
        db.refresh(attempt)
        # Elo with the attempt's own difficulty and, for a judged short answer, the
        # continuous score — so partial credit moves mastery proportionally.
        if body.topic_id is not None:
            crud.update_topic_mastery_elo(
                db,
                student_id=student_id,
                topic_id=body.topic_id,
                topic_name=body.topic_name,
                is_correct=graded["is_correct"],
                difficulty=body.difficulty,
                outcome=graded["outcome"],
            )
    invalidate_recommendation_cache(student_id)
    return attempt


@router.get("/learner/{student_id}/quiz", response_model=list[QuizAttemptResponse])
def get_quiz_history(
    student_id: str,
    include_pending: bool = Query(False, description="Include generated-but-unanswered questions"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current: Student = Depends(get_current_student),
):
    """Answered attempts only by default — pending questions are not attempts yet.

    Even with include_pending=true the response model blanks correct_answer and
    feedback on ungraded rows, so a live question's answer never leaks here.
    """
    student_id = assert_self_or_admin(student_id, current)
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
