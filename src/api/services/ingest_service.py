"""
api/services/ingest_service.py
Admin content authoring: draft -> review -> commit.

THE PHASE BOUNDARY IS THE WRITE BOUNDARY, and neither phase writes a file. A draft is
one row in `question_content_drafts` — its markdown, its metadata, its analysis and, for
`pdf`, the uploaded bytes. `commit()` is the only function that changes anything outside
that row, and what it changes is the database plus a queue of Qdrant work. Abandoning a
review costs a `DELETE`, not a rollback of three stores.

Three draft constructors, one shared tail:

    extract(pdf, meta)      ─┐
    create_draft(md, meta)  ─┼─→ [ analyse · collide · stage ] → reanalyse()* → commit()
    compose(questions, meta)─┘

They differ only in how the markdown comes into being. Everything after that — the
chunk/unit analysis, the collision check, the draft record, the validation and the
commit — is identical, so no origin can skip a guard that the others enforce.

Why the review step exists: PDF text extraction is the one step here whose output is
both likely to be wrong and expensive when it is. `pymupdf4llm` on a two-column exam
paper or a scanned photocopy produces plausible-looking, silently mangled output. The
`paste` and `compose` origins keep the review for a different reason — their text is
not a machine's guess, but what happens *to* it is still opaque, and an author who
cannot see the 384-char chunk boundaries will write a question whose options land in a
different chunk from its statement.

COMMIT IS ONE DATABASE TRANSACTION. The committed markdown becomes a `question_documents`
row (it used to be a file under `data/cleaned/`), the bank is rebuilt into a new version,
the upload record is written, and the Qdrant work — both the new course chunks and the
bank's unit vectors — is queued in the outbox. Nothing reaches a vector store until that
transaction commits, so a Qdrant outage leaves retryable work rather than a contribution
that is half applied. `data/cleaned/` and `data/splits/` stay read-only pipeline input.

IMPORTING `process_dataset` IS NOT SAFE AT MODULE SCOPE. It constructs an EasyOCR
Reader at import time (process_dataset.py:25), which would load — and on a fresh machine
download — the detection and recognition models into the API process whether or not OCR
is ever requested. It is imported lazily inside the request, and OCR itself is done here
rather than through `extract_text_ocr`, which needs a path on disk and writes
`temp_ocr_<n>.png` into the current working directory.
"""
from __future__ import annotations

import re
import threading
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from sqlalchemy.orm import Session

from ... import question_intelligence as qi
from ...config import (
    QI_ADMIN_DEFAULT_SOURCE, QI_ADMIN_SOURCE_TYPES, QI_CLUSTER_DISTANCE,
    QI_DUPLICATE_THRESHOLD, QI_MARKDOWN_MAX_CHARS, QI_REQUIRE_TOPIC_IDS,
    QI_STAGING_MAX_PENDING, QI_STAGING_TTL_HOURS, QI_TOKEN_GUARD,
    QI_UPLOAD_MAX_PAGES,
)
from ...database.models import QuestionContentDraft, QuestionDocument, QuestionUpload
from ...prepare_rag_splits import extract_week, resolve_topic_ids, split_document
from .question_service import invalidate_question_bank
from . import question_repository as question_repo
from .question_vector_service import sync_outbox
from .recommendation_service import find_topic

ROOT_DIR = Path(__file__).resolve().parents[3]
CLEANED_DIR = ROOT_DIR / "data" / "cleaned"

# OCR is serialised: the EasyOCR reader is a single shared object and a large scan can
# take minutes. Serialising is acceptable — such files belong in the offline pipeline.
_OCR_LOCK = threading.Lock()
_OCR_READER: Any = None

# The bank is rebuilt under a lock. A multi-worker deployment would need real locking;
# same caveat `_RECOMMENDATION_CACHE` already carries.
_BANK_LOCK = threading.Lock()
_DRAFT_LOCK = threading.Lock()

# Delimiter tokens the quiz prompt uses to fence retrieved chunks. Admin text reaches
# quiz prompts through the same retrieval path as everything else.
_DELIMITER_RE = re.compile(r"</?context[^>]*>|<\|", re.IGNORECASE)


class IngestError(RuntimeError):
    """Recoverable, admin-facing failure. Carries an HTTP status and a message."""

    def __init__(self, status_code: int, message: str, code: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.code = code


# ── Metadata resolution ───────────────────────────────────────────────────────

def slugify(title: str) -> str:
    """Derive a file stem the same way `prepare_rag_splits` does, so the online and
    offline doc_ids agree."""
    cleaned = re.sub(r"[^\w\s.-]", "", (title or "").strip())
    cleaned = re.sub(r"\s+", "_", cleaned).strip("._-")
    return cleaned[:120]


def resolve_metadata(meta: dict, *, origin: str, filename: str = "") -> dict:
    """Validate the metadata block and compute what will actually be written.

    Every field is re-validated on every request that carries one — including the
    commit. A validator that only ran at draft creation would be bypassed by editing
    the commit payload.
    """
    title = (meta.get("title") or "").strip()
    if not title and origin == "pdf" and filename:
        title = Path(filename).stem
    if not title:
        raise IngestError(400, "title is required (there is no filename to fall back on).",
                          "missing_title")

    stem = slugify(title)
    if not stem:
        raise IngestError(400, f"title {title!r} does not slugify to a usable file stem.",
                          "bad_title")

    source_type = (meta.get("source_type") or QI_ADMIN_DEFAULT_SOURCE).strip()
    if source_type not in QI_ADMIN_SOURCE_TYPES:
        allowed = ", ".join(sorted(QI_ADMIN_SOURCE_TYPES))
        raise IngestError(400, f"source_type must be one of: {allowed}.", "bad_source_type")

    implied = QI_ADMIN_SOURCE_TYPES[source_type]
    content_kind = (meta.get("content_kind") or implied).strip()
    if content_kind not in ("questions", "prose"):
        raise IngestError(400, "content_kind must be 'questions' or 'prose'.", "bad_content_kind")
    if content_kind == "questions" and implied != "questions":
        raise IngestError(
            400,
            f"source_type '{source_type}' holds prose; question content belongs in "
            + " or ".join(s for s, k in QI_ADMIN_SOURCE_TYPES.items() if k == "questions")
            + ".",
            "kind_source_mismatch",
        )

    week = meta.get("week")
    if week is None and origin == "pdf" and filename:
        week = extract_week(Path(filename))
    try:
        week = int(week or 0)
    except (TypeError, ValueError):
        raise IngestError(400, "week must be an integer (0 means 'any week').", "bad_week")
    if not 0 <= week <= 52:
        raise IngestError(400, "week must be between 0 and 52.", "bad_week")

    topic_ids: list[int] = []
    unknown: list[Any] = []
    for raw in meta.get("topic_ids") or []:
        try:
            tid = int(raw)
        except (TypeError, ValueError):
            unknown.append(raw)
            continue
        if find_topic(tid):
            if tid not in topic_ids:
                topic_ids.append(tid)
        else:
            unknown.append(raw)
    if unknown:
        raise IngestError(400, f"unknown topic_ids: {unknown}", "bad_topic_ids")
    if QI_REQUIRE_TOPIC_IDS and not topic_ids:
        raise IngestError(400, "topic_ids are required (QI_REQUIRE_TOPIC_IDS is on).",
                          "missing_topic_ids")

    return {
        "title": title,
        "stem": stem,
        "source_type": source_type,
        "content_kind": content_kind,
        "week": week,
        "topic_ids": topic_ids,
        "topic_tags": resolve_topic_ids(topic_ids),
        "lecture_ref": (meta.get("lecture_ref") or None),
        "source_note": (meta.get("source_note") or None),
    }


# ── Text validation ───────────────────────────────────────────────────────────

def validate_markdown(text: str) -> str:
    """Validate admin-authored text. Validated, never transformed.

    `clean_markdown_content` is deliberately NOT re-run here: it exists to repair
    machine output, and running it over text a human wrote or corrected would silently
    undo the correction the review step exists to make. The bytes the admin approved are
    the bytes that get stored and chunked.
    """
    if not text or not text.strip():
        raise IngestError(400, "The document is empty.", "empty_markdown")
    if len(text) > QI_MARKDOWN_MAX_CHARS:
        raise IngestError(
            400,
            f"The document is {len(text):,} characters; the limit is {QI_MARKDOWN_MAX_CHARS:,}.",
            "markdown_too_long",
        )
    # A delimiter token would let uploaded text break out of the <context> fencing the
    # quiz prompt relies on. `quiz_service` defends itself by DROPPING such a chunk;
    # here the better answer is to name the line, because an admin can fix it and
    # silently stripping text a human just approved is the invisible mutation the review
    # step exists to eliminate.
    for number, line in enumerate(text.splitlines(), start=1):
        if _DELIMITER_RE.search(line):
            raise IngestError(
                400,
                f"Line {number} contains a reserved delimiter token "
                f"(<context …> or <|). Remove it: {line.strip()[:120]}",
                "delimiter_token",
            )
    return text


# ── Draft records ─────────────────────────────────────────────────────────────

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _naive(value: Optional[datetime]) -> Optional[datetime]:
    """SQLite drops tzinfo on write, so compare everything as naive UTC."""
    if value is None:
        return None
    return value.replace(tzinfo=None) if value.tzinfo else value


def _iso(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def _load_draft(db: Session, draft_id: str) -> QuestionContentDraft:
    row = db.get(QuestionContentDraft, draft_id)
    if row is None:
        raise IngestError(404, f"No staged draft {draft_id!r}.", "unknown_draft")
    return row


def _draft_meta(row: QuestionContentDraft) -> dict:
    """The draft as the preview builder wants it."""
    stored = dict(row.metadata_json or {})
    analysis = dict(row.analysis_json or {})
    return {
        "draft_id": row.draft_id,
        "origin": row.origin,
        "status": row.status,
        "filename": row.filename,
        "resolved": stored.get("resolved") or {},
        "pages": analysis.get("pages"),
        "ocr_used": bool(analysis.get("ocr_used")),
        "cleaning_stats": analysis.get("cleaning_stats"),
        "created_at": _iso(row.created_at) or "",
        "expires_at": _iso(row.expires_at),
    }


def _draft_markdown(row: QuestionContentDraft) -> str:
    """The text as last seen by the admin, falling back to the extraction."""
    return row.edited_markdown if row.edited_markdown is not None else row.original_markdown


def sweep_drafts(db: Session) -> int:
    """Delete expired drafts. Called on the way in, so there is no background task.

    Reclaims the PDF blob with the row — the reason the size ceiling is
    QI_UPLOAD_MAX_MB × QI_STAGING_MAX_PENDING rather than unbounded.
    """
    now = _naive(_now())
    expired = (db.query(QuestionContentDraft)
               .filter(QuestionContentDraft.status == "staged",
                       QuestionContentDraft.expires_at.isnot(None),
                       QuestionContentDraft.expires_at < now).all())
    for row in expired:
        db.delete(row)
    if expired:
        db.commit()
    return len(expired)


def list_drafts(db: Session) -> list[dict]:
    rows = (db.query(QuestionContentDraft)
            .filter(QuestionContentDraft.status != "committed")
            .order_by(QuestionContentDraft.created_at.desc()).all())
    out = []
    for row in rows:
        resolved = (row.metadata_json or {}).get("resolved", {})
        out.append({
            "draft_id": row.draft_id,
            "origin": row.origin,
            "status": row.status,
            "filename": row.filename,
            "title": resolved.get("title", ""),
            "source_type": resolved.get("source_type", ""),
            "week": resolved.get("week", 0),
            "created_at": _iso(row.created_at) or "",
            "expires_at": _iso(row.expires_at),
        })
    return out


def discard_draft(db: Session, draft_id: str) -> None:
    row = _load_draft(db, draft_id)
    if row.status == "committed":
        raise IngestError(409, "This draft has already been committed.", "already_committed")
    db.delete(row)
    db.commit()


def _allocate_draft(db: Session) -> str:
    with _DRAFT_LOCK:
        sweep_drafts(db)
        pending = (db.query(QuestionContentDraft)
                   .filter(QuestionContentDraft.status == "staged").count())
        if pending >= QI_STAGING_MAX_PENDING:
            raise IngestError(
                429,
                f"{pending} drafts are already open (limit {QI_STAGING_MAX_PENDING}). "
                "Commit or discard some first.",
                "too_many_drafts",
            )
        return uuid.uuid4().hex[:16]


# ── Collision check ───────────────────────────────────────────────────────────

def check_collision(db: Session, stem: str, source_type: str) -> dict:
    """Does this stem already exist — on disk, or as a database document?

    `doc_id` has no directory component, so a stem must be unique across every source.
    Both stores are checked: the corpus tree under `data/cleaned/` is still real content
    an admin could collide with, and `question_documents` holds everything contributed
    since. Checking only the tree (as this did while commits wrote files) would stop
    detecting an admin-vs-admin collision the moment content moved into the database.

    A cross-source collision is refused outright: `replace=true` authorises replacing
    your own earlier upload, never overwriting a transcript.
    """
    document = question_repo.document_by_stem(db, stem)
    if document:
        same_source = document.source_type == source_type
        return {
            "collides": True,
            "existing_path": f"db:question_documents/{document.source_type}/{document.stem}",
            "same_source": same_source,
            "replaceable": same_source,
        }

    if not CLEANED_DIR.exists():
        return {"collides": False, "existing_path": None, "same_source": False, "replaceable": False}
    for path in CLEANED_DIR.rglob("*.md"):
        if path.stem.replace(" ", "_") != stem:
            continue
        same_source = path.parent.name == source_type
        return {
            "collides": True,
            "existing_path": str(path.relative_to(ROOT_DIR)).replace("\\", "/"),
            "same_source": same_source,
            "replaceable": same_source,
        }
    return {"collides": False, "existing_path": None, "same_source": False, "replaceable": False}


# ── Analysis (shared by every origin, and by re-analysis) ─────────────────────

def analyse(markdown: str, resolved: dict) -> dict:
    """Dry-run the downstream stages. Pure: nothing is written and nothing is embedded.

    Splitting and parsing are text operations, which is what makes re-analysis cheap
    enough to run on every edit.
    """
    chunks = split_document(
        markdown,
        week=resolved["week"],
        source_type=resolved["source_type"],
        doc_id=resolved["stem"],
        topic_ids=resolved["topic_ids"],
        origin="admin",
    )
    chunk_preview = [
        {
            "doc_id": c.metadata.get("doc_id", ""),
            "index": i,
            "char_count": len(c.page_content),
            "text": c.page_content,
        }
        for i, c in enumerate(chunks)
    ]

    units = qi.parse_markdown(
        markdown,
        source_type=resolved["source_type"],
        stem=resolved["stem"],
        week=resolved["week"],
        source_file=f"{resolved['source_type']}/{resolved['stem']}.md",
    )
    unit_preview = [
        {
            "title": u.get("title", ""),
            "text": u.get("text", "")[:400],
            "option_count": len(u.get("options") or []),
            "has_answer": bool(u.get("answer")),
        }
        for u in units
    ]

    warnings: list[str] = []
    if resolved["content_kind"] == "questions" and not units:
        warnings.append(
            "No question units parsed. The markdown does not carry the structure the "
            "parser needs (## Question N / ### Statement / ### Options / ### Answer). "
            "Committing will add retrieval chunks but nothing to the question bank."
        )
    if markdown.lstrip().startswith("---"):
        warnings.append(
            "The document begins with a frontmatter-like block. Metadata comes from the "
            "form, not the body; this block will be treated as ordinary text."
        )

    return {"chunks": chunks, "chunk_preview": chunk_preview,
            "unit_preview": unit_preview, "units": units, "warnings": warnings}


def _preview_payload(db: Session, meta: dict, markdown: str,
                     extra_warnings: Optional[list[str]] = None) -> dict:
    resolved = meta["resolved"]
    analysis = analyse(markdown, resolved)
    collision = check_collision(db, resolved["stem"], resolved["source_type"])

    warnings = list(analysis["warnings"]) + list(extra_warnings or [])
    if collision["collides"] and not collision["same_source"]:
        warnings.append(
            f"'{resolved['stem']}' already exists at "
            f"{collision['existing_path']}. A cross-source collision cannot be replaced — "
            "rename this document."
        )
    elif collision["collides"]:
        warnings.append(
            f"'{resolved['stem']}' already exists at {collision['existing_path']}. "
            "Commit will need 'replace existing'."
        )

    return {
        "draft_id": meta["draft_id"],
        "origin": meta["origin"],
        "status": meta.get("status", "staged"),
        "filename": meta.get("filename"),
        "markdown": markdown,
        "char_count": len(markdown),
        "pages": meta.get("pages"),
        "ocr_used": bool(meta.get("ocr_used")),
        "cleaning_stats": meta.get("cleaning_stats"),
        "resolved_metadata": {
            "title": resolved["title"],
            "stem": resolved["stem"],
            "source_type": resolved["source_type"],
            "content_kind": resolved["content_kind"],
            "week": resolved["week"],
            "topic_ids": resolved["topic_ids"],
            "topic_tags": resolved["topic_tags"],
            "lecture_ref": resolved.get("lecture_ref"),
        },
        "chunk_preview": analysis["chunk_preview"],
        "unit_preview": analysis["unit_preview"],
        "collision": collision,
        "warnings": warnings,
        "expires_at": meta.get("expires_at"),
    }


def _preview_summary(payload: dict) -> dict:
    """What is worth keeping on the row: the verdict, not a second copy of the text."""
    return {
        "chunk_count": len(payload.get("chunk_preview") or []),
        "unit_count": len(payload.get("unit_preview") or []),
        "char_count": payload.get("char_count", 0),
        "collision": payload.get("collision"),
        "warnings": payload.get("warnings", []),
        "resolved_metadata": payload.get("resolved_metadata", {}),
    }


def _stage(db: Session, draft_id: str, *, origin: str, markdown: str, resolved: dict,
           filename: Optional[str] = None, pages: Optional[int] = None,
           ocr_used: bool = False, cleaning_stats: Optional[dict] = None,
           composed: Optional[list[dict]] = None, source_blob: Optional[bytes] = None,
           source_media_type: Optional[str] = None) -> dict:
    """Persist the draft row and return the preview.

    In the database rather than a process-local dict: a `--reload` between draft and
    commit would otherwise lose a twenty-minute OCR run — or a long piece of typing.
    """
    created = _naive(_now())
    row = QuestionContentDraft(
        draft_id=draft_id,
        origin=origin,
        status="staged",
        filename=filename,
        original_markdown=markdown,
        edited_markdown=None,
        metadata_json={"resolved": resolved},
        preview_json={},
        analysis_json={"pages": pages, "ocr_used": ocr_used, "cleaning_stats": cleaning_stats},
        # Nothing reads this today; a future "edit this question" feature needs the
        # fields rather than the rendering, and they are free now and unrecoverable later.
        composed_json=composed,
        source_blob=source_blob,
        source_media_type=source_media_type,
        created_at=created,
        expires_at=created + timedelta(hours=QI_STAGING_TTL_HOURS),
    )
    db.add(row)
    db.flush()
    payload = _preview_payload(db, _draft_meta(row), markdown)
    row.preview_json = _preview_summary(payload)
    db.commit()
    return payload


# ── Phase A, origin `pdf` ─────────────────────────────────────────────────────

def _load_process_dataset():
    """Import process_dataset lazily. See the module docstring for why."""
    try:
        from ... import process_dataset  # noqa: PLC0415
        return process_dataset
    except Exception as exc:  # noqa: BLE001
        raise IngestError(503, f"PDF processing is unavailable: {type(exc).__name__}: {exc}",
                          "processing_unavailable") from exc


def _ocr_pages(doc: Any) -> str:
    """OCR an open PDF in memory, one page at a time.

    `process_dataset.extract_text_ocr` is deliberately not used: it takes a path we no
    longer have, writes `temp_ocr_<n>.png` into the current working directory (two
    concurrent extracts race on the same filename), and returns a sentinel STRING rather
    than raising when EasyOCR is missing — which, ingested blindly, becomes a chunk in
    Qdrant. Rendering to bytes and reading them back removes all three.
    """
    global _OCR_READER

    try:
        import easyocr  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        raise IngestError(503, "OCR is not available on this server (EasyOCR is not installed).",
                          "ocr_unavailable") from exc

    if _OCR_READER is None:
        try:
            _OCR_READER = easyocr.Reader(["en"], gpu=False, verbose=False)
        except Exception as exc:  # noqa: BLE001
            raise IngestError(503, f"OCR is not available on this server ({type(exc).__name__}).",
                              "ocr_unavailable") from exc

    pages: list[str] = []
    for number in range(len(doc)):
        pixmap = doc.load_page(number).get_pixmap(dpi=150)
        lines = _OCR_READER.readtext(pixmap.tobytes("png"), detail=0)
        pages.append(f"## Page {number + 1}\n\n" + "\n".join(lines))
    return "\n\n".join(pages)


def extract(db: Session, pdf_bytes: bytes, filename: str, meta: dict,
            allow_ocr: bool = False) -> dict:
    """Origin `pdf`: parse an uploaded PDF into an editable draft.

    The bytes are opened from memory and stored on the draft row, so a re-extract does
    not need a re-upload and nothing lands on disk. They are dropped at commit.
    """
    resolved = resolve_metadata(meta, origin="pdf", filename=filename)
    draft_id = _allocate_draft(db)

    try:
        import fitz  # noqa: PLC0415
        import pymupdf4llm  # noqa: PLC0415
    except ImportError as exc:
        raise IngestError(503, "pymupdf4llm is not installed on the server.",
                          "pymupdf_missing") from exc

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        pages = len(doc)
        if pages > QI_UPLOAD_MAX_PAGES:
            raise IngestError(
                400,
                f"{pages} pages exceeds the {QI_UPLOAD_MAX_PAGES}-page limit. "
                "Large scans belong in the offline pipeline.",
                "too_many_pages",
            )

        raw = pymupdf4llm.to_markdown(doc=doc, page_chunks=False, write_images=False)
        process_dataset = _load_process_dataset()
        text = process_dataset.clean_markdown(raw or "")

        ocr_used = False
        if not text.strip() and allow_ocr:
            with _OCR_LOCK:
                ocr_text = _ocr_pages(doc)
            text = process_dataset.clean_markdown(ocr_text)
            ocr_used = True
        # Without allow_ocr an empty text layer is not an error: the empty pane is the
        # signal, and the admin can re-run with OCR or supply the text by hand.

    from ... import clean_dataset  # noqa: PLC0415
    cleaned, stats = clean_dataset.clean_markdown_content(text)

    warnings: list[str] = []
    if not cleaned.strip():
        warnings.append(
            "No text could be extracted from this PDF. It is probably a scan — "
            "re-upload with 'allow OCR', or paste the text instead."
            if not allow_ocr else
            "OCR produced no usable text from this PDF."
        )
        cleaned = cleaned or ""

    payload = _stage(db, draft_id, origin="pdf", markdown=cleaned, resolved=resolved,
                     filename=filename, pages=pages, ocr_used=ocr_used,
                     cleaning_stats=stats, source_blob=pdf_bytes,
                     source_media_type="application/pdf")
    payload["warnings"] = warnings + payload["warnings"]
    return payload


# ── Phase A, origins `paste` and `compose` ────────────────────────────────────

def create_draft(db: Session, markdown: str, meta: dict) -> dict:
    """Origin `paste`. Never touches `process_dataset`, so EasyOCR stays unimported."""
    resolved = resolve_metadata(meta, origin="paste")
    # Validated up front rather than at commit: there is no extraction to blame, so an
    # error here is the admin's to fix now rather than after they have finished editing.
    validate_markdown(markdown)
    draft_id = _allocate_draft(db)
    return _stage(db, draft_id, origin="paste", markdown=markdown, resolved=resolved)


def compose(db: Session, questions: list[dict], meta: dict) -> dict:
    """Origin `compose`: structured questions rendered into the canonical markdown.

    The renderer is the inverse of the `pq` parser and lives in the same module, so a
    composed question cannot fail to land in the bank for want of the right heading
    level. Validation mirrors `quiz_service.grade_answer`: options non-empty means MCQ,
    and the answer must be one of them — a question failing that would be unanswerable
    at grading time, so it is refused at authoring time instead.
    """
    resolved = resolve_metadata(meta, origin="compose")
    if resolved["content_kind"] != "questions":
        raise IngestError(
            400,
            f"Composed questions cannot be filed as '{resolved['source_type']}' "
            "(that source holds prose).",
            "kind_source_mismatch",
        )

    errors = qi.validate_composed_questions(questions)
    if errors:
        raise IngestError(400, "; ".join(errors), "invalid_questions")

    markdown = qi.render_question_markdown(questions)
    validate_markdown(markdown)
    draft_id = _allocate_draft(db)
    return _stage(db, draft_id, origin="compose", markdown=markdown, resolved=resolved,
                  composed=questions)


# ── Review ────────────────────────────────────────────────────────────────────

def reanalyse(db: Session, draft_id: str, markdown: str,
              meta_override: Optional[dict] = None) -> dict:
    """Re-run the analysis over edited text and metadata. Writes no content.

    The edit itself is kept on the draft row, so a browser crash mid-review does not
    lose the corrections. Metadata is editable here, not just at creation, because the
    preview is frequently what reveals the right value: a `pq` draft that parses to 0
    units and reads like OCR output is a `PYQ`.
    """
    row = _load_draft(db, draft_id)
    if row.status == "committed":
        raise IngestError(409, "This draft has already been committed.", "already_committed")

    meta = _draft_meta(row)
    if meta_override:
        meta["resolved"] = resolve_metadata(meta_override, origin=row.origin,
                                            filename=row.filename or "")

    payload = _preview_payload(db, meta, markdown)
    row.edited_markdown = markdown
    row.metadata_json = {"resolved": meta["resolved"]}
    row.preview_json = _preview_summary(payload)
    db.commit()
    return payload


def get_draft(db: Session, draft_id: str) -> dict:
    row = _load_draft(db, draft_id)
    return _preview_payload(db, _draft_meta(row), _draft_markdown(row))


# ── Phase B: commit ───────────────────────────────────────────────────────────

def _existing_doc_ids(db: Session, stem: str) -> list[str]:
    """The doc_ids currently in the collection for this stem.

    A database document knows exactly what it emitted, which is the point of recording
    `chunk_doc_ids`. Only fall back to the splits index for a corpus stem — admin chunks
    were never written to `data/splits/`, so deriving them from there (as this used to)
    always returned nothing and made `replace=true` duplicate the document instead of
    superseding it.
    """
    document = question_repo.document_by_stem(db, stem)
    if document:
        return list(document.chunk_doc_ids or [])
    try:
        chunks = qi.load_chunk_index()
    except Exception:  # noqa: BLE001
        return []
    prefix = f"{stem}_chunk_"
    return [c["doc_id"] for c in chunks if c["doc_id"].startswith(prefix)]


def _rebuild_bank_rows(db: Session, *, refresh_vectors: bool = False) -> dict:
    """Re-parse, re-embed and persist the bank. The CALLER owns the transaction.

    A full rebuild rather than an incremental assignment: it makes the database one
    coherent, versioned snapshot, and at a few hundred units with a vector cache the
    cost is dominated by parsing rather than embedding.
    """
    from ...config import QI_SOURCE_TYPES  # noqa: PLC0415

    sources = tuple(dict.fromkeys(tuple(QI_SOURCE_TYPES) + tuple(QI_ADMIN_SOURCE_TYPES)))
    units = qi.parse_question_units(
        source_types=sources,
        extra_documents=question_repo.document_units_input(db),
    )
    if not units:
        return {}
    vectors = question_repo.cached_vectors(db, units, refresh=refresh_vectors)
    qi.map_units_to_chunks(
        units,
        qi.load_chunk_index() + question_repo.document_chunk_index(db),
    )
    bank = qi.build_bank(units, vectors, duplicate_threshold=QI_DUPLICATE_THRESHOLD,
                         cluster_distance=QI_CLUSTER_DISTANCE, use_token_guard=QI_TOKEN_GUARD)
    question_repo.persist_bank(db, bank, vectors)
    return bank


def _upsert_document(db: Session, resolved: dict, markdown: str, chunks: list[Any],
                     draft_id: str) -> QuestionDocument:
    """Store the approved bytes and the doc_ids they produced. Supersedes any prior."""
    previous = question_repo.document_by_stem(db, resolved["stem"])
    if previous:
        previous.status = "superseded"
        previous.superseded_at = _naive(_now())
        db.flush()

    document = QuestionDocument(
        stem=resolved["stem"],
        source_type=resolved["source_type"],
        content_kind=resolved["content_kind"],
        week=resolved["week"],
        title=resolved["title"],
        markdown=markdown,
        frontmatter={
            "week": resolved["week"],
            "source_type": resolved["source_type"],
            "content_kind": resolved["content_kind"],
            "topic_ids": resolved["topic_ids"],
            "lecture_ref": resolved.get("lecture_ref"),
            "origin": "admin",
        },
        topic_ids=resolved["topic_ids"],
        topic_tags=resolved["topic_tags"],
        lecture_ref=resolved.get("lecture_ref"),
        chunk_doc_ids=[c.metadata.get("doc_id", "") for c in chunks],
        origin="admin",
        status="active",
        draft_id=draft_id,
    )
    db.add(document)
    db.flush()
    return document


def commit(draft_id: str, markdown: str, vector_store: Any, db: Session,
           meta_override: Optional[dict] = None, replace: bool = False) -> dict:
    """Every irreversible step, in one transaction.

    Order inside it: supersede the previous document, store this one, queue the chunk
    delete and append, rebuild the bank, write the upload record, mark the draft
    committed. One `db.commit()` decides all of it, and the Qdrant work is queued rather
    than performed — so there is no window in which vectors exist for a contribution the
    database does not record, or vice versa.

    A double-clicked commit is refused twice over: the status check below catches the
    ordinary case, and `question_uploads.draft_id` is unique, so two concurrent requests
    cannot both produce an upload record even if both read `staged`.
    """
    row = _load_draft(db, draft_id)
    if row.status == "committed":
        raise IngestError(409, "This draft has already been committed.", "already_committed")
    if row.status == "committing":
        raise IngestError(
            409,
            "A commit for this draft is already in progress. If the server restarted "
            "mid-commit, discard the draft and re-create it — nothing was written.",
            "commit_in_progress",
        )

    expires = _naive(row.expires_at)
    if expires and expires < _naive(_now()):
        raise IngestError(410, "This draft expired. Re-create it to commit.", "draft_expired")

    resolved = (resolve_metadata(meta_override, origin=row.origin, filename=row.filename or "")
                if meta_override else (row.metadata_json or {}).get("resolved") or {})
    if not resolved:
        raise IngestError(400, "This draft has no resolved metadata.", "missing_metadata")
    markdown = validate_markdown(markdown)

    collision = check_collision(db, resolved["stem"], resolved["source_type"])
    if collision["collides"]:
        if not collision["same_source"]:
            raise IngestError(
                409,
                f"'{resolved['stem']}' already exists at {collision['existing_path']}, "
                "a different source type. doc_ids carry no directory, so this would "
                "collide with that document's chunks. Rename this one.",
                "cross_source_collision",
            )
        if not replace:
            raise IngestError(
                409,
                f"'{resolved['stem']}' already exists at {collision['existing_path']}. "
                "Re-submit with replace=true to supersede it.",
                "stem_collision",
            )

    superseded = _existing_doc_ids(db, resolved["stem"]) if (collision["collides"] and replace) else []
    if superseded:
        from ..dependencies import doc_id_payload_index_state  # noqa: PLC0415
        if doc_id_payload_index_state() is False:
            raise IngestError(
                503,
                "Replacing requires a keyword payload index on metadata.doc_id, which "
                "this collection does not have. Run: "
                "python src/build_question_bank.py --ensure-index",
                "missing_payload_index",
            )
        # An UNKNOWN state (Qdrant unreachable) is not a refusal: the delete is queued
        # like everything else, and the drain reports whatever Qdrant says later.

    original = row.original_markdown
    edited = markdown != original

    row.status = "committing"
    try:
        # The same call the preview made, over the same text.
        chunks = split_document(
            markdown,
            week=resolved["week"],
            source_type=resolved["source_type"],
            doc_id=resolved["stem"],
            topic_ids=resolved["topic_ids"],
            origin="admin",
        )

        document = _upsert_document(db, resolved, markdown, chunks, draft_id)
        question_repo.queue_course_chunk_delete(db, stem=resolved["stem"], doc_ids=superseded)
        question_repo.queue_course_chunks(db, stem=resolved["stem"], chunks=chunks)

        units = qi.parse_markdown(
            markdown,
            source_type=resolved["source_type"],
            stem=resolved["stem"],
            week=resolved["week"],
            source_file=f"{resolved['source_type']}/{resolved['stem']}.md",
        )
        with _BANK_LOCK:
            bank = _rebuild_bank_rows(db)

        warnings: list[str] = []
        if resolved["content_kind"] == "questions" and not units:
            warnings.append("No question units parsed: the chunks are searchable but the bank gained nothing.")

        result = {
            "draft_id": draft_id,
            "origin": row.origin,
            "filename": row.filename,
            "resolved_metadata": {
                "title": resolved["title"], "stem": resolved["stem"],
                "source_type": resolved["source_type"], "content_kind": resolved["content_kind"],
                "week": resolved["week"], "topic_ids": resolved["topic_ids"],
                "topic_tags": resolved["topic_tags"], "lecture_ref": resolved.get("lecture_ref"),
            },
            "pages": (row.analysis_json or {}).get("pages"),
            "ocr_used": bool((row.analysis_json or {}).get("ocr_used")),
            "edited": edited,
            "chars_added": max(0, len(markdown) - len(original)),
            "chars_removed": max(0, len(original) - len(markdown)),
            "chunks_added": len(chunks),
            "document_id": document.document_id,
            "warnings": warnings,
            "units_classified": len(units),
            "duplicates_matched": sum(1 for unit in units if not unit.get("is_canonical", True)),
            "clusters_joined": 0,
            "clusters_created": len((bank or {}).get("clusters", [])),
        }

        db.add(QuestionUpload(
            draft_id=draft_id,
            document_id=document.document_id,
            resolved_metadata=result["resolved_metadata"],
            result_json={**result, "source_note": resolved.get("source_note"),
                         "created_at": _iso(row.created_at)},
            replaced=bool(superseded),
            superseded_chunks=len(superseded),
            chars_added=result["chars_added"],
            chars_removed=result["chars_removed"],
            committed_at=_naive(_now()),
        ))

        row.status = "committed"
        row.committed_at = _naive(_now())
        row.edited_markdown = markdown
        row.metadata_json = {"resolved": resolved}
        row.last_error = None
        # The PDF has done its job: the approved markdown is the record from here.
        row.source_blob = None
        db.commit()
    except Exception as exc:
        db.rollback()
        # Nothing was applied — the draft goes back to reviewable rather than stranded.
        fresh = db.get(QuestionContentDraft, draft_id)
        if fresh is not None and fresh.status == "committing":
            fresh.status = "staged"
            fresh.last_error = f"{type(exc).__name__}: {exc}"
            db.commit()
        raise

    invalidate_question_bank()
    # Best effort, and deliberately after the commit: a Qdrant outage leaves queued work
    # and a reported failure, not a lost contribution.
    sync = sync_outbox(db, vector_store=vector_store)
    result["vector_sync"] = sync
    if sync.get("failed"):
        result["warnings"].append(
            f"{sync['failed']} vector operations could not be synchronised and remain "
            "queued. Retry from the admin sync panel or run: python src/sync_question_vectors.py"
        )
    return result


def list_uploads(db: Session) -> list[dict]:
    """The contribution history, newest first."""
    rows = (db.query(QuestionUpload)
            .order_by(QuestionUpload.committed_at.desc()).all())
    out = []
    for row in rows:
        entry = dict(row.result_json or {})
        entry.update({
            "upload_id": row.upload_id,
            "draft_id": row.draft_id,
            "document_id": row.document_id,
            "resolved_metadata": row.resolved_metadata or {},
            "replaced": bool(row.replaced),
            "superseded_chunks": row.superseded_chunks,
            "chars_added": row.chars_added,
            "chars_removed": row.chars_removed,
            "committed_at": _iso(row.committed_at),
        })
        out.append(entry)
    return out


def rebuild_bank(db: Session, refresh_vectors: bool = False) -> dict:
    """Full re-cluster — the drift escape hatch.

    Reads the corpus tree and every active `question_documents` row, so an admin
    contribution survives a rebuild without ever having been a file.
    """
    with _BANK_LOCK:
        bank = _rebuild_bank_rows(db, refresh_vectors=refresh_vectors)
        if not bank:
            db.rollback()
            raise IngestError(503, "No question units found to rebuild from.", "nothing_to_rebuild")
    db.commit()
    invalidate_question_bank()
    sync_outbox(db)
    return bank["stats"]
