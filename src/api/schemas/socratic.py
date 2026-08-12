"""
api/schemas/socratic.py
Request and response models for the Socratic Study Companion.

**There is no field for an answer anywhere in this file, and that is deliberate** — the
schema half of L3. `AnalyzeResponse` carries a concept, segments and a guiding question;
`AttemptResponse` carries a diagnosis and a next question. A model that decided to emit a
solution has nowhere to put it: the service whitelists keys before constructing these, and
FastAPI's `response_model` drops anything extra on the way out.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    selection: str = Field(..., description="The text the student highlighted.")
    options: list[str] = Field(default_factory=list,
                               description="Answer choices offered on the page, if any.")
    page_url: Optional[str] = Field(default=None, description="Where they were reading.")
    source_kind: str = Field(default="selection", description="selection | capture")


class TopicCard(BaseModel):
    topic_id: int
    name: str
    week: int = 0
    description: str = ""
    lecture_ref: str = ""
    score: float = 0.0


class SegmentCard(BaseModel):
    """One stretch of one lecture. `description` is the model's signpost, or None.

    `start`/`end` are `MM:SS` for display; `start_sec` drives the `?t=` deep link. `end`
    is None on a lecture's final section — the corpus does not record durations, and a
    fabricated end time would be a citation to something that may not exist.
    """

    segment_ref: str
    lecture_id: str
    title: str
    week: int = 0
    start: Optional[str] = None
    end: Optional[str] = None
    start_sec: Optional[int] = None
    end_sec: Optional[int] = None
    deep_link: Optional[str] = None
    doc_ids: list[str] = Field(default_factory=list)
    description: Optional[str] = None


class RelatedQuestion(BaseModel):
    """A Question Bank neighbour — the agreed substitute for the Discourse slot.

    Title and cluster only. The unit's `answer` and `solution` columns are read on the
    server to build the L4 denylist and are never serialised into this model.
    """

    unit_id: Optional[str] = None
    cluster_id: Optional[Any] = None
    title: str = ""
    source_type: str = ""
    week: int = 0
    member_count: int = 1


class PolicyInfo(BaseModel):
    source: str = "model"            # model | deterministic
    verdict: str = "clean"           # clean | blocked_regenerated | blocked_fallback
    provider_used: str = "none"
    denylist_size: int = 0


class AnalyzeResponse(BaseModel):
    session_id: str
    concept: Optional[TopicCard] = None
    alternatives: list[TopicCard] = Field(default_factory=list)
    segments: list[SegmentCard] = Field(default_factory=list)
    coverage: str = "ok"             # ok | no_transcript
    related_questions: list[RelatedQuestion] = Field(default_factory=list)
    why_this_concept: str = ""
    guiding_question: str = ""
    watch_out_for: str = ""
    hint_level: int = 1
    max_hint_level: int = 3
    policy: PolicyInfo = Field(default_factory=PolicyInfo)


class HintResponse(BaseModel):
    hint_level: int
    hint: str
    max_hint_level: int


class AttemptRequest(BaseModel):
    student_answer: str = Field(..., description="The student's own reasoning.")


class AttemptResponse(BaseModel):
    verdict: str                     # on_track | partially_correct | off_track
    first_error: str = ""
    why: str = ""
    concept_to_revisit: str = ""
    next_guiding_question: str = ""
    judge: str = ""
    guard_verdict: str = "clean"


class SocraticEventOut(BaseModel):
    kind: str
    payload: dict[str, Any] = Field(default_factory=dict)
    guard_verdict: Optional[str] = None
    provider_used: Optional[str] = None
    created_at: Optional[datetime] = None


class SessionReplay(BaseModel):
    session_id: str
    created_at: Optional[datetime] = None
    selection: str = ""
    topic_id: Optional[int] = None
    hint_level: int = 1
    max_hint_level: int = 3
    coverage: str = "ok"
    policy: dict[str, Any] = Field(default_factory=dict)
    events: list[SocraticEventOut] = Field(default_factory=list)


class TranscribeResponse(BaseModel):
    text: str = ""
    options: list[str] = Field(default_factory=list)
    provider_used: str = "none"
