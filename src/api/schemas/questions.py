"""
api/schemas/questions.py
Pydantic models for the Question Intelligence endpoints.

`ContentMetadata` is the one metadata contract, shared by all three draft origins
(`pdf` / `paste` / `compose`) and by both phases (draft creation and commit). One model
validated in one place: a validator that only ran on the first request would be
trivially bypassed by editing the second.
"""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from ...config import QI_ADMIN_DEFAULT_SOURCE


# ── Read side ─────────────────────────────────────────────────────────────────

class QuestionUnit(BaseModel):
    unit_id: str
    source_type: str
    week: int
    title: str
    text: str
    options: list[str] = []
    answer: str = ""
    solution: str = ""
    origin: str = "corpus"
    is_canonical: bool = False
    dup_group_id: Optional[int] = None
    cluster_id: Optional[int] = None
    chunk_doc_ids: list[str] = []


class ClusterSummary(BaseModel):
    cluster_id: int
    title: str
    # Three counts, never collapsed into one `size`. `canonical_count` is how many
    # DISTINCT doubts the cluster holds; `member_count` is every unit in it; `asked_count`
    # is the subset of those that represents somebody asking. The common-doubts ranking
    # uses asked_count — deduplication is precisely what removes the repetition that
    # ranking exists to surface, and member_count over-counts it from the other side by
    # treating each OCR fragment of a past paper as another asking.
    canonical_count: int
    member_count: int
    asked_count: int = 0
    weeks: list[int] = []
    sources: list[str] = []
    medoid_unit_id: Optional[str] = None


class ClusterDetail(ClusterSummary):
    members: list[QuestionUnit] = []


class BankStats(BaseModel):
    unit_count: int
    canonical_count: int
    duplicate_count: int
    duplicate_rate: float
    cluster_count: int
    # Clusters that pass the display gates (grouped something, and can be labelled).
    # cluster_count stays reported next to it: the gap is a property of the corpus.
    displayable_clusters: int = 0
    singleton_clusters: int
    largest_member_count: int
    admin_authored_units: int
    by_source: dict[str, Any] = {}
    thresholds: dict[str, Any] = {}
    generated_from: str = ""
    # Relational reads never wait on Qdrant, so the bank can be fully browsable while
    # its vectors are still catching up. Reported rather than hidden.
    vector_status: str = "pending"


class RelatedQuestion(BaseModel):
    """A canonical sibling of something the student just retrieved."""
    unit_id: str
    cluster_id: Optional[int] = None
    title: str
    source_type: str
    week: int
    member_count: int = 1


# ── Authoring: metadata ───────────────────────────────────────────────────────

class ContentMetadata(BaseModel):
    """The metadata every draft carries, whatever produced it.

    A PDF can guess at some of this from its filename; pasted and composed content
    cannot guess at any of it, which is what forces the contract to be explicit.
    """
    title: str = Field(..., min_length=1, max_length=200,
                       description="Becomes the file stem and the doc_id prefix")
    source_type: str = Field(default=QI_ADMIN_DEFAULT_SOURCE,
                             description="Destination folder under data/cleaned/")
    content_kind: Optional[Literal["questions", "prose"]] = Field(
        default=None, description="Defaults to whatever the source type implies")
    week: int = Field(default=0, ge=0, le=52,
                      description="0 is a wildcard that matches every topic filter, not 'unknown'")
    topic_ids: list[int] = Field(default_factory=list,
                                 description="Taxonomy IDs; resolved to topic names in chunk metadata")
    lecture_ref: Optional[str] = Field(default=None, max_length=200)
    source_note: Optional[str] = Field(default=None, max_length=500,
                                       description="Provenance for the manifest; never embedded")


class ComposedQuestion(BaseModel):
    """One authored question. `options` empty means short answer — the same
    shape-not-flag rule `quiz_service.grade_answer` uses to route grading."""
    statement: str = Field(..., min_length=1)
    options: list[str] = Field(default_factory=list)
    answer: str = Field(..., min_length=1)
    solution: Optional[str] = None
    marks: Optional[float] = None


# ── Authoring: requests ───────────────────────────────────────────────────────

class CreateDraftRequest(BaseModel):
    markdown: str = Field(..., min_length=1)
    metadata: ContentMetadata


class ComposeDraftRequest(BaseModel):
    questions: list[ComposedQuestion] = Field(..., min_length=1)
    metadata: ContentMetadata


class PreviewRequest(BaseModel):
    markdown: str = Field(..., min_length=1)
    metadata: Optional[ContentMetadata] = None


class CommitRequest(BaseModel):
    markdown: str = Field(..., min_length=1)
    metadata: Optional[ContentMetadata] = None
    replace: bool = False


# ── Authoring: responses ──────────────────────────────────────────────────────

class ChunkPreview(BaseModel):
    """A chunk the commit *would* create. Shown so a bad split is visible as a chunk
    that ends mid-question, rather than discovered after ingestion."""
    doc_id: str
    index: int
    char_count: int
    text: str


class UnitPreview(BaseModel):
    title: str
    text: str
    option_count: int = 0
    has_answer: bool = False


class ResolvedMetadata(BaseModel):
    """What will actually be written, after defaults and taxonomy resolution.

    Shown instead of the submitted values because the two differ whenever a default
    fires, and the admin should approve the stored values rather than the typed ones.
    """
    title: str
    stem: str
    source_type: str
    content_kind: str
    week: int
    topic_ids: list[int] = []
    topic_tags: list[str] = []
    lecture_ref: Optional[str] = None


class CollisionInfo(BaseModel):
    collides: bool = False
    existing_path: Optional[str] = None
    same_source: bool = False
    # A cross-source collision is refused outright: `replace=true` authorises replacing
    # your own earlier upload, never overwriting a transcript that happens to share a stem.
    replaceable: bool = False


class DraftPreview(BaseModel):
    draft_id: str
    origin: Literal["pdf", "paste", "compose"]
    status: str = "staged"
    filename: Optional[str] = None
    markdown: str
    char_count: int
    pages: Optional[int] = None
    ocr_used: bool = False
    cleaning_stats: Optional[dict[str, Any]] = None
    resolved_metadata: ResolvedMetadata
    chunk_preview: list[ChunkPreview] = []
    unit_preview: list[UnitPreview] = []
    collision: CollisionInfo = CollisionInfo()
    warnings: list[str] = []
    expires_at: Optional[str] = None


class StagedDraft(BaseModel):
    draft_id: str
    origin: str
    status: str
    filename: Optional[str] = None
    title: str
    source_type: str
    week: int
    created_at: str
    expires_at: Optional[str] = None


class UploadResult(BaseModel):
    draft_id: str
    origin: str
    filename: Optional[str] = None
    resolved_metadata: ResolvedMetadata
    pages: Optional[int] = None
    ocr_used: bool = False
    edited: bool = False
    chars_added: int = 0
    chars_removed: int = 0
    chunks_added: int = 0
    units_classified: int = 0
    duplicates_matched: int = 0
    clusters_joined: int = 0
    clusters_created: int = 0
    # The stored document, which replaced `cleaned_path`: committed content is a
    # `question_documents` row now, not a file under data/cleaned/.
    document_id: str = ""
    vector_sync: dict[str, Any] = {}
    warnings: list[str] = []


class SyncStatus(BaseModel):
    """Outbox health. `failed` above zero is the one thing an operator must not miss."""
    pending: int = 0
    failed: int = 0
    synced: int = 0
    oldest_unfinished_at: Optional[str] = None
    last_error: Optional[str] = None
    active_version_id: Optional[str] = None
    active_version_vector_status: Optional[str] = None
    units_pending_vectors: int = 0
