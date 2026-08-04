"""
api/routers/learner.py
Learner profile CRUD endpoints.

POST   /learner                           — create student
GET    /learner/{student_id}              — get student
PUT    /learner/{student_id}              — update student name/email

GET    /learner/{student_id}/mastery      — all topic mastery rows (Mayank)
PUT    /learner/{student_id}/mastery      — update a topic score

POST   /learner/{student_id}/session      — start new chat session
GET    /learner/{student_id}/sessions     — list sessions
GET    /session/{session_id}/history      — get messages in session (Jibin)

POST   /learner/{student_id}/quiz         — record quiz attempt
GET    /learner/{student_id}/quiz         — get quiz history

GET    /topics                            — full taxonomy
GET    /topics/week/{week}                — topics for a week
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database.session import get_db
from ...database import crud
from ..schemas.learner import (
    MessageResponse, QuizAttemptCreate, QuizAttemptResponse,
    SessionCreate, SessionResponse, StudentCreate, StudentResponse,
    StudentUpdate, TopicMasteryResponse, TopicMasteryUpdate,
)

router = APIRouter(tags=["Learner"])

# Load taxonomy once
_TAXONOMY_PATH = Path(__file__).resolve().parent.parent.parent / "topic_taxonomy.json"
_TAXONOMY: list[dict] = json.loads(_TAXONOMY_PATH.read_text(encoding="utf-8")) if _TAXONOMY_PATH.exists() else []


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
        raise HTTPException(status_code=404, detail="Student not found.")
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
    """Returns all topic mastery rows sorted weakest first.
    Mayank's recommendation engine calls this to find knowledge gaps.
    """
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return crud.get_topic_mastery_for_student(db, student_id)


@router.put("/learner/{student_id}/mastery", response_model=TopicMasteryResponse)
def update_mastery(student_id: str, body: TopicMasteryUpdate, db: Session = Depends(get_db)):
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return crud.upsert_topic_mastery(
        db, student_id, body.topic_id, body.topic_name, body.new_score
    )


# ── Chat Sessions ─────────────────────────────────────────────────────────────

@router.post("/learner/{student_id}/session", response_model=SessionResponse, status_code=201)
def create_session(student_id: str, body: SessionCreate, db: Session = Depends(get_db)):
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return crud.create_chat_session(db, student_id=student_id, title=body.title)


@router.get("/learner/{student_id}/sessions", response_model=list[SessionResponse])
def list_sessions(student_id: str, db: Session = Depends(get_db)):
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return crud.get_sessions_for_student(db, student_id)


@router.get("/session/{session_id}/history", response_model=list[MessageResponse])
def get_history(session_id: str, db: Session = Depends(get_db)):
    """Chronological message history for a session.
    Jibin uses this to load conversation memory before generating a reply.
    """
    session = crud.get_chat_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return crud.get_session_history(db, session_id)


# ── Quiz Attempts ─────────────────────────────────────────────────────────────

@router.post("/learner/{student_id}/quiz", response_model=QuizAttemptResponse, status_code=201)
def create_quiz_attempt(student_id: str, body: QuizAttemptCreate, db: Session = Depends(get_db)):
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
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
    # Auto-update mastery score if we know the result
    if body.is_correct is not None and body.topic_id is not None:
        score = 1.0 if body.is_correct else 0.0
        crud.upsert_topic_mastery(db, student_id, body.topic_id, body.topic_name, score)
    return attempt


@router.get("/learner/{student_id}/quiz", response_model=list[QuizAttemptResponse])
def get_quiz_history(student_id: str, db: Session = Depends(get_db)):
    if not crud.get_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return crud.get_quiz_history(db, student_id)


# ── Topic Taxonomy ────────────────────────────────────────────────────────────

@router.get("/topics", response_model=list[dict])
def get_all_topics():
    """Returns the full topic taxonomy (all 12 weeks)."""
    return _TAXONOMY


@router.get("/topics/week/{week}", response_model=list[dict])
def get_topics_for_week(week: int):
    """Returns topics for a specific week."""
    result = [t for t in _TAXONOMY if t["week"] == week]
    if not result:
        raise HTTPException(status_code=404, detail=f"No topics found for week {week}.")
    return result
