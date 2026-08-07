"""
api/schemas/learner.py
Pydantic request and response models for learner profile, recommendations, and analytics.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, model_validator


# ── Student ───────────────────────────────────────────────────────────────────

# There is no StudentCreate. Rows are created by POST /auth/google from verified Google
# claims; a body-supplied `student_id` + `email` was an index squat waiting to happen.

class StudentUpdate(BaseModel):
    """Name only — Google owns the address that authenticates the row."""

    name: Optional[str] = None


class StudentStatusUpdate(BaseModel):
    is_active: bool


class StudentResponse(BaseModel):
    student_id: str
    name: str
    email: Optional[str]
    created_at: datetime
    picture_url: Optional[str] = None
    is_admin: bool = False
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    login_count: int = 0

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
    elo_rating: float = 0.0
    attempts: int = 0
    streak: int = 0
    chat_interactions: int = 0
    last_tested: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── QuizAttempt ───────────────────────────────────────────────────────────────

class QuizAttemptCreate(BaseModel):
    """Body of the deprecated direct-write endpoint. The outcome is graded server-side."""

    topic_name: str
    question_text: str
    topic_id: Optional[int] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    student_answer: Optional[str] = Field(
        default=None,
        description="Omit to store the question unanswered; supply it to have it graded.",
    )
    correct_answer: Optional[str] = Field(
        default=None,
        description="Required whenever student_answer is supplied — it is what the answer "
                    "is matched or judged against.",
    )
    options: list[str] = Field(
        default=[],
        description="Supply the MCQ options to have the answer graded by exact match. "
                    "Leave empty for a short answer, which is graded by the LLM judge.",
    )
    is_correct: Optional[bool] = Field(
        default=None,
        deprecated=True,
        description="Ignored. The server regrades every answer; a client-supplied verdict "
                    "is not trusted because it feeds the Elo mastery model.",
    )
    feedback: Optional[str] = Field(
        default=None,
        description="Optional explanation of the correct answer. Passed to the judge as "
                    "grader notes for a short answer, and stored as feedback for an MCQ.",
    )
    session_id: Optional[str] = None
    source_chunks: list[str] = []


class QuizAttemptResponse(BaseModel):
    attempt_id: str
    topic_id: Optional[int] = None
    topic_name: str
    difficulty: str
    question_text: str
    options: list[str] = []
    student_answer: Optional[str]
    correct_answer: Optional[str]
    is_correct: Optional[bool]
    llm_score: Optional[float]
    feedback: Optional[str]
    reason: Optional[str] = None
    attempt_time: datetime

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def _withhold_ungraded_answers(self):
        """Never return the answer for a question that has not been answered yet.

        Rows are persisted at generation time, so without this the answer and the
        explanation for a live question would be one GET away.
        """
        if self.is_correct is None:
            self.correct_answer = None
            self.feedback = None
        return self


# ── Personalized Quiz Generation ──────────────────────────────────────────────

class QuizGenerateRequest(BaseModel):
    topic_id: Optional[int] = Field(
        None, description="Override targeting. Omit to quiz the weakest identified area."
    )
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    count: int = Field(3, ge=1, le=5)
    question_type: str = Field("mcq", pattern="^(mcq|short_answer)$")


class GeneratedQuestion(BaseModel):
    """What the client is allowed to see. No correct answer, no explanation."""
    attempt_id: str
    question_text: str
    options: list[str] = []
    question_type: str = "mcq"
    topic_id: Optional[int] = None
    topic_name: str
    week: int = 0
    difficulty: str
    reason: str
    status: str = ""
    unmet_prerequisites: list[str] = []


class AttemptedTopic(BaseModel):
    topic_id: int
    topic_name: str
    week: int = 0
    attempts: int = 0


class QuizReadinessResponse(BaseModel):
    """Whether the personalized quiz is available yet, and how far off it is.

    Thresholds come from `src/config.py`. `attempted_topics` is the pool the
    personalized quiz draws from — it never leaves this list.
    """
    ready: bool
    attempts_completed: int
    required_attempts: int
    remaining_attempts: int
    topics_attempted: int
    required_topics: int
    remaining_topics: int
    attempted_topics: list[AttemptedTopic] = []


class QuizAnswerRequest(BaseModel):
    student_answer: str = Field(..., min_length=1)


class QuizSource(BaseModel):
    doc_id: str
    label: str = ""
    chunk_index: Optional[int] = None


class MasteryDelta(BaseModel):
    before: Optional[float] = None
    after: Optional[float] = None
    elo: Optional[float] = None
    streak: Optional[int] = None
    attempts: Optional[int] = None


class QuizAnswerResponse(BaseModel):
    attempt_id: str
    is_correct: bool
    llm_score: Optional[float] = None
    correct_answer: Optional[str] = None
    explanation: str = ""
    feedback: str = ""
    judge_provider_used: str = "none"
    sources: list[QuizSource] = []
    mastery: MasteryDelta


# ── Recommendation Engine Schemas ─────────────────────────────────────────────

class EvaluatedTopic(BaseModel):
    topic_id: int
    topic_name: str
    week: int
    lecture_ref: str = ""
    description: str = ""
    prerequisites: list[int] = []
    effective_score: float
    raw_score: float
    elo_rating: float
    attempts: int
    streak: int
    chat_interactions: int
    days_since_tested: Optional[int] = None
    status: str
    has_prerequisite_gap: bool = False
    unmet_prerequisites: list[str] = []
    priority: float = 0.0
    suggested_actions: list[str] = []


class StudyPlanItem(EvaluatedTopic):
    llm_advice: str = ""


class RecommendationResponse(BaseModel):
    student_id: str
    overall_mastery_pct: int
    total_topics_tested: int
    total_topics: int
    coverage_pct: int
    study_plan: list[StudyPlanItem]
    strengths: list[EvaluatedTopic]
    decaying_topics: list[EvaluatedTopic]
    all_topics: list[EvaluatedTopic]
    llm_provider_used: str = "none"


class WeekMasteryOverview(BaseModel):
    week: int
    average_mastery_pct: int
    topics_tested: int
    total_topics: int
    topics: list[EvaluatedTopic]


class LearnerProfileResponse(BaseModel):
    student: StudentResponse
    overall_mastery_pct: int
    total_topics_tested: int
    total_topics: int
    coverage_pct: int
    total_quizzes_taken: int
    quiz_accuracy_pct: int
    weeks: list[WeekMasteryOverview]
    recent_quiz_attempts: list[QuizAttemptResponse]
