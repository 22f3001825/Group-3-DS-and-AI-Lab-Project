"""
api/services/ingest_service.py
Admin content authoring: draft -> review -> commit.

THE PHASE BOUNDARY IS THE WRITE BOUNDARY. Draft creation touches only
`data/raw/uploads/staging/<draft_id>/`. `commit()` is the only function in this module
that writes `data/cleaned/`, appends to Qdrant, or rewrites the question bank. Abandoning
a review costs a directory, not a rollback of three stores.

Three draft constructors, one shared tail:

    extract(pdf, meta)      ─┐
    create_draft(md, meta)  ─┼─→ [ analyse · collide · stage ] → reanalyse()* → commit()
    compose(questions, meta)─┘

They differ only in how the markdown comes into being. Everything after that — the
chunk/unit analysis, the collision check, the staging record, the validation and the
commit — is identical, so no origin can skip a guard that the others enforce.

Why the review step exists: PDF text extraction is the one step here whose output is
both likely to be wrong and expensive when it is. `pymupdf4llm` on a two-column exam
paper or a scanned photocopy produces plausible-looking, silently mangled output. The
`paste` and `compose` origins keep the review for a different reason — their text is
not a machine's guess, but what happens *to* it is still opaque, and an author who
cannot see the 384-char chunk boundaries will write a question whose options land in a
different chunk from its statement.

IMPORTING `process_dataset` IS NOT SAFE AT MODULE SCOPE. It constructs an EasyOCR
Reader at import time (process_dataset.py:25), which would load — and on a fresh machine
download — the detection and recognition models into the API process whether or not OCR
is ever requested. It is imported lazily inside the request, and `extract_text_ocr` is
resolved only inside the `allow_ocr` branch.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import threading
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import numpy as np
from sqlalchemy.orm import Session

from ... import question_intelligence as qi
from ...config import (
    QI_ADMIN_DEFAULT_SOURCE, QI_ADMIN_SOURCE_TYPES, QI_CLUSTER_DISTANCE,
    QI_DUPLICATE_THRESHOLD, QI_MARKDOWN_MAX_CHARS, QI_REQUIRE_TOPIC_IDS,
    QI_STAGING_DIR, QI_STAGING_MAX_PENDING, QI_STAGING_TTL_HOURS, QI_TOKEN_GUARD,
    QI_UPLOAD_MAX_PAGES,
)
from ...prepare_rag_splits import extract_week, render_frontmatter, resolve_topic_ids, split_document
from .question_service import invalidate_question_bank
from . import question_repository as question_repo
from .question_vector_service import sync_outbox
from .recommendation_service import find_topic

ROOT_DIR = Path(__file__).resolve().parents[3]
CLEANED_DIR = ROOT_DIR / "data" / "cleaned"
UPLOADS_DIR = ROOT_DIR / "data" / "raw" / "uploads"
STAGING_DIR = ROOT_DIR / QI_STAGING_DIR
MANIFEST_PATH = qi.BANK_DIR / "uploads.json"

# OCR is serialised: extract_text_ocr writes `temp_ocr_{n}.png` into the CURRENT WORKING
# DIRECTORY and shares a module-level EasyOCR reader, so two concurrent extracts in
# FastAPI's threadpool would race on both. Serialising is acceptable — OCR on a large
# scan takes minutes and such files belong in the offline pipeline.
_OCR_LOCK = threading.Lock()

# The bank is rewritten under a lock and replaced atomically. A multi-worker deployment
# would need real locking; same caveat `_RECOMMENDATION_CACHE` already carries.
_BANK_LOCK = threading.Lock()
_STAGING_LOCK = threading.Lock()

_OCR_SENTINEL = "*OCR unavailable or skipped.*"

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
    the bytes that get written and chunked.
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


# ── Staging ───────────────────────────────────────────────────────────────────

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _staging_path(draft_id: str) -> Path:
    return STAGING_DIR / draft_id


def _read_meta(draft_id: str) -> dict:
    path = _staging_path(draft_id) / "meta.json"
    if not path.exists():
        raise IngestError(404, f"No staged draft {draft_id!r}.", "unknown_draft")
    return json.loads(path.read_text(encoding="utf-8"))


def _write_meta(draft_id: str, meta: dict) -> None:
    path = _staging_path(draft_id) / "meta.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def sweep_staging() -> int:
    """Delete expired drafts. Called on the way in, so there is no background task."""
    removed = 0
    if not STAGING_DIR.exists():
        return 0
    for entry in STAGING_DIR.iterdir():
        if not entry.is_dir():
            continue
        try:
            meta = json.loads((entry / "meta.json").read_text(encoding="utf-8"))
            expires = datetime.fromisoformat(meta["expires_at"])
        except Exception:  # noqa: BLE001
            continue
        if expires < _now():
            shutil.rmtree(entry, ignore_errors=True)
            removed += 1
    return removed


def list_drafts() -> list[dict]:
    out: list[dict] = []
    if not STAGING_DIR.exists():
        return out
    for entry in sorted(STAGING_DIR.iterdir()):
        if not entry.is_dir():
            continue
        try:
            meta = json.loads((entry / "meta.json").read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        resolved = meta.get("resolved", {})
        out.append({
            "draft_id": meta["draft_id"],
            "origin": meta.get("origin", "paste"),
            "status": meta.get("status", "staged"),
            "filename": meta.get("filename"),
            "title": resolved.get("title", ""),
            "source_type": resolved.get("source_type", ""),
            "week": resolved.get("week", 0),
            "created_at": meta.get("created_at", ""),
            "expires_at": meta.get("expires_at"),
        })
    out.sort(key=lambda d: d["created_at"], reverse=True)
    return out


def discard_draft(draft_id: str) -> None:
    path = _staging_path(draft_id)
    if not path.exists():
        raise IngestError(404, f"No staged draft {draft_id!r}.", "unknown_draft")
    shutil.rmtree(path, ignore_errors=True)


def _allocate_draft() -> str:
    with _STAGING_LOCK:
        sweep_staging()
        pending = [d for d in list_drafts() if d["status"] == "staged"]
        if len(pending) >= QI_STAGING_MAX_PENDING:
            raise IngestError(
                429,
                f"{len(pending)} drafts are already open (limit {QI_STAGING_MAX_PENDING}). "
                "Commit or discard some first.",
                "too_many_drafts",
            )
        draft_id = uuid.uuid4().hex[:16]
        _staging_path(draft_id).mkdir(parents=True, exist_ok=True)
        return draft_id


# ── Collision check ───────────────────────────────────────────────────────────

def check_collision(stem: str, source_type: str) -> dict:
    """Does this stem already exist under data/cleaned/?

    Checked against the FILESYSTEM, not against the question bank. `doc_id` has no
    directory component, and the bank holds only question sources — so an admin
    uploading `Lecture_1.pdf` as `pq` would pass a bank check cleanly and then write
    chunks whose doc_ids collide with the existing transcript chunks in the collection.
    A cross-source collision is refused outright: `replace=true` authorises replacing
    your own earlier upload, never overwriting a transcript.
    """
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


def _preview_payload(meta: dict, markdown: str, extra_warnings: Optional[list[str]] = None) -> dict:
    resolved = meta["resolved"]
    analysis = analyse(markdown, resolved)
    collision = check_collision(resolved["stem"], resolved["source_type"])

    warnings = list(analysis["warnings"]) + list(extra_warnings or [])
    if collision["collides"] and not collision["same_source"]:
        warnings.append(
            f"'{resolved['stem']}' already exists under "
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


def _stage(draft_id: str, *, origin: str, markdown: str, resolved: dict,
           filename: Optional[str] = None, pages: Optional[int] = None,
           ocr_used: bool = False, cleaning_stats: Optional[dict] = None,
           composed: Optional[list[dict]] = None) -> dict:
    """Persist the staging record and return the preview.

    On disk rather than in a process-local dict: a `--reload` between draft and commit
    would otherwise lose a twenty-minute OCR run — or a long piece of typing.
    """
    created = _now()
    meta = {
        "draft_id": draft_id,
        "origin": origin,
        "status": "staged",
        "filename": filename,
        "resolved": resolved,
        "pages": pages,
        "ocr_used": ocr_used,
        "cleaning_stats": cleaning_stats,
        "created_at": created.isoformat(),
        "expires_at": (created + timedelta(hours=QI_STAGING_TTL_HOURS)).isoformat(),
    }
    path = _staging_path(draft_id)
    path.mkdir(parents=True, exist_ok=True)
    # The pre-edit draft, kept for the audit trail and for "restore original".
    (path / "original.md").write_text(markdown, encoding="utf-8")
    if composed is not None:
        # Nothing reads this today; a future "edit this question" feature needs the
        # fields rather than the rendering, and they are free now and unrecoverable later.
        (path / "composed.json").write_text(
            json.dumps(composed, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_meta(draft_id, meta)
    return _preview_payload(meta, markdown)


# ── Phase A, origin `pdf` ─────────────────────────────────────────────────────

def _load_process_dataset():
    """Import process_dataset lazily. See the module docstring for why."""
    try:
        from ... import process_dataset  # noqa: PLC0415
        return process_dataset
    except Exception as exc:  # noqa: BLE001
        raise IngestError(503, f"PDF processing is unavailable: {type(exc).__name__}: {exc}",
                          "processing_unavailable") from exc


def extract(pdf_bytes: bytes, filename: str, meta: dict, allow_ocr: bool = False) -> dict:
    """Origin `pdf`: parse an uploaded PDF into an editable draft. Writes only to staging."""
    resolved = resolve_metadata(meta, origin="pdf", filename=filename)
    draft_id = _allocate_draft()
    staging = _staging_path(draft_id)

    try:
        source_pdf = staging / "source.pdf"
        source_pdf.write_bytes(pdf_bytes)

        try:
            import fitz  # noqa: PLC0415
            import pymupdf4llm  # noqa: PLC0415
        except ImportError as exc:
            raise IngestError(503, "pymupdf4llm is not installed on the server.",
                              "pymupdf_missing") from exc

        with fitz.open(str(source_pdf)) as doc:
            pages = len(doc)
        if pages > QI_UPLOAD_MAX_PAGES:
            raise IngestError(
                400,
                f"{pages} pages exceeds the {QI_UPLOAD_MAX_PAGES}-page limit. "
                "Large scans belong in the offline pipeline.",
                "too_many_pages",
            )

        raw = pymupdf4llm.to_markdown(doc=str(source_pdf), page_chunks=False, write_images=False)
        process_dataset = _load_process_dataset()
        text = process_dataset.clean_markdown(raw or "")

        ocr_used = False
        if not text.strip():
            if not allow_ocr:
                # Not an error: the empty pane is the signal, and the admin can now
                # re-run with OCR or supply the text by hand.
                text = ""
            else:
                with _OCR_LOCK:
                    # Resolved only inside this branch — an OCR-free deployment must
                    # never pay for EasyOCR.
                    ocr_text = process_dataset.extract_text_ocr(source_pdf)
                if ocr_text.strip() == _OCR_SENTINEL:
                    # extract_text_ocr RETURNS this string rather than raising; ingested
                    # blindly it would become a chunk in Qdrant.
                    raise IngestError(503, "OCR is not available on this server (EasyOCR failed to load).",
                                      "ocr_unavailable")
                text = process_dataset.clean_markdown(ocr_text)
                ocr_used = True

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

        payload = _stage(draft_id, origin="pdf", markdown=cleaned, resolved=resolved,
                         filename=filename, pages=pages, ocr_used=ocr_used,
                         cleaning_stats=stats)
        payload["warnings"] = warnings + payload["warnings"]
        return payload
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


# ── Phase A, origins `paste` and `compose` ────────────────────────────────────

def create_draft(markdown: str, meta: dict) -> dict:
    """Origin `paste`. Never touches `process_dataset`, so EasyOCR stays unimported."""
    resolved = resolve_metadata(meta, origin="paste")
    # Validated up front rather than at commit: there is no extraction to blame, so an
    # error here is the admin's to fix now rather than after they have finished editing.
    validate_markdown(markdown)
    draft_id = _allocate_draft()
    try:
        return _stage(draft_id, origin="paste", markdown=markdown, resolved=resolved)
    except Exception:
        shutil.rmtree(_staging_path(draft_id), ignore_errors=True)
        raise


def compose(questions: list[dict], meta: dict) -> dict:
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
    draft_id = _allocate_draft()
    try:
        return _stage(draft_id, origin="compose", markdown=markdown, resolved=resolved,
                      composed=questions)
    except Exception:
        shutil.rmtree(_staging_path(draft_id), ignore_errors=True)
        raise


# ── Review ────────────────────────────────────────────────────────────────────

def reanalyse(draft_id: str, markdown: str, meta_override: Optional[dict] = None) -> dict:
    """Re-run the analysis over edited text and metadata. Writes nothing.

    Metadata is editable here, not just at creation, because the preview is frequently
    what reveals the right value: a `pq` draft that parses to 0 units and reads like OCR
    output is a `PYQ`.
    """
    meta = _read_meta(draft_id)
    if meta.get("status") == "committed":
        raise IngestError(409, "This draft has already been committed.", "already_committed")
    if meta_override:
        meta = dict(meta)
        meta["resolved"] = resolve_metadata(meta_override, origin=meta["origin"],
                                            filename=meta.get("filename", ""))
    return _preview_payload(meta, markdown)


def get_draft(draft_id: str) -> dict:
    meta = _read_meta(draft_id)
    markdown = (_staging_path(draft_id) / "original.md").read_text(encoding="utf-8")
    return _preview_payload(meta, markdown)


# ── Phase B: commit ───────────────────────────────────────────────────────────

def _write_manifest_entry(entry: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict] = []
    if MANIFEST_PATH.exists():
        try:
            existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing = []
    existing.append(entry)
    tmp = MANIFEST_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(MANIFEST_PATH)


def _delete_points_by_doc_id(vector_store: Any, doc_ids: list[str]) -> None:
    from qdrant_client import models as qmodels  # noqa: PLC0415

    if not doc_ids:
        return
    vector_store.client.delete(
        collection_name=vector_store.collection_name,
        points_selector=qmodels.FilterSelector(
            filter=qmodels.Filter(must=[
                qmodels.FieldCondition(
                    key="metadata.doc_id",
                    match=qmodels.MatchAny(any=doc_ids),
                )
            ])
        ),
    )


def _existing_doc_ids(stem: str) -> list[str]:
    """doc_ids previously written for this stem, read from the splits index."""
    try:
        chunks = qi.load_chunk_index()
    except Exception:  # noqa: BLE001
        return []
    prefix = f"{stem}_chunk_"
    return [c["doc_id"] for c in chunks if c["doc_id"].startswith(prefix)]


def _classify_into_bank(db: Session, units: list[dict]) -> dict:
    """Rebuild the database-backed bank and queue vectors for its own Qdrant collection.

    The legacy JSON/NumPy artifact is deliberately not read or written here.  A rebuild
    is currently the safe incremental policy: it makes the database one coherent,
    versioned snapshot and keeps the old source files as course content only.
    """
    result = {"units_classified": 0, "duplicates_matched": 0,
              "clusters_joined": 0, "clusters_created": 0}
    with _BANK_LOCK:
        from ...config import QI_SOURCE_TYPES  # noqa: PLC0415
        sources = tuple(dict.fromkeys(tuple(QI_SOURCE_TYPES) + tuple(QI_ADMIN_SOURCE_TYPES)))
        all_units = qi.parse_question_units(source_types=sources)
        if not all_units:
            return result
        vectors = qi.embed_units(all_units)
        qi.map_units_to_chunks(all_units, qi.load_chunk_index())
        bank = qi.build_bank(all_units, vectors, duplicate_threshold=QI_DUPLICATE_THRESHOLD,
                             cluster_distance=QI_CLUSTER_DISTANCE, use_token_guard=QI_TOKEN_GUARD)
        question_repo.persist_bank(db, bank, vectors)
        result["units_classified"] = len(units)
        result["duplicates_matched"] = sum(1 for unit in units if not unit.get("is_canonical", True))
        result["clusters_created"] = len(bank["clusters"])
    db.commit()
    sync_outbox(db)
    invalidate_question_bank()
    return result


def commit(draft_id: str, markdown: str, vector_store: Any, db: Session,
           meta_override: Optional[dict] = None, replace: bool = False) -> dict:
    """Every irreversible step, in one place.

    Failure between the filesystem write and the bank rewrite leaves partial state, and
    this does not pretend otherwise: there is no transaction spanning a file, a Qdrant
    append and a JSON rewrite. The ordering makes the cheapest recovery the likeliest —
    `data/cleaned/` first (idempotent), Qdrant second (guarded by the collision check and
    recoverable with `replace=true`), the bank last (rebuildable from scratch). The
    staged record stays `staged` until the end, so a crash mid-commit leaves the draft
    re-committable rather than lost.
    """
    meta = _read_meta(draft_id)
    if meta.get("status") == "committed":
        # Also what makes a double-clicked commit safe: add_documents appends with fresh
        # point IDs and has no upsert-by-doc_id, so without this the second click would
        # duplicate every vector.
        raise IngestError(409, "This draft has already been committed.", "already_committed")

    expires = datetime.fromisoformat(meta["expires_at"])
    if expires < _now():
        raise IngestError(410, "This draft expired. Re-create it to commit.", "draft_expired")

    resolved = (resolve_metadata(meta_override, origin=meta["origin"],
                                 filename=meta.get("filename", ""))
                if meta_override else meta["resolved"])
    markdown = validate_markdown(markdown)

    collision = check_collision(resolved["stem"], resolved["source_type"])
    if collision["collides"]:
        if not collision["same_source"]:
            raise IngestError(
                409,
                f"'{resolved['stem']}' already exists under {collision['existing_path']}, "
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

    superseded = _existing_doc_ids(resolved["stem"]) if (collision["collides"] and replace) else []
    if superseded:
        from ..dependencies import has_doc_id_payload_index  # noqa: PLC0415
        if not has_doc_id_payload_index():
            raise IngestError(
                503,
                "Replacing requires a keyword payload index on metadata.doc_id, which "
                "this collection does not have. Run: "
                "python src/build_question_bank.py --ensure-index",
                "missing_payload_index",
            )

    original = (_staging_path(draft_id) / "original.md").read_text(encoding="utf-8")
    edited = markdown != original

    # C3 — write the frontmatter block plus the approved bytes. The frontmatter is what
    # makes an offline `prepare_rag_splits` run reproduce these chunks WITH their
    # asserted topic tags rather than silently regenerating week-derived ones.
    front = render_frontmatter({
        "week": resolved["week"],
        "source_type": resolved["source_type"],
        "content_kind": resolved["content_kind"],
        "topic_ids": resolved["topic_ids"],
        "lecture_ref": resolved.get("lecture_ref"),
        "origin": "admin",
    })
    target_dir = CLEANED_DIR / resolved["source_type"]
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{resolved['stem']}.md"
    target.write_text(front + markdown, encoding="utf-8")

    # C4 — the same call the preview made, over the same text.
    chunks = split_document(
        markdown,
        week=resolved["week"],
        source_type=resolved["source_type"],
        doc_id=resolved["stem"],
        topic_ids=resolved["topic_ids"],
        origin="admin",
    )

    # C5 — append through the singleton the chat path already uses. NEVER
    # ingest_to_qdrant.main(): that deletes and recreates the collection, which from a
    # request handler would destroy every chunk of course material in it.
    if superseded:
        _delete_points_by_doc_id(vector_store, superseded)
    if chunks:
        vector_store.add_documents(chunks)

    # C6 — classify into the bank.
    units = qi.parse_markdown(
        markdown,
        source_type=resolved["source_type"],
        stem=resolved["stem"],
        week=resolved["week"],
        source_file=f"{resolved['source_type']}/{resolved['stem']}.md",
    )
    classification = _classify_into_bank(db, units)

    warnings: list[str] = []
    if resolved["content_kind"] == "questions" and not units:
        warnings.append("No question units parsed: the chunks are searchable but the bank gained nothing.")

    # C7 — finalise. For `pdf`, promote the source out of staging; `paste` and `compose`
    # have no raw artifact and none is invented — the cleaned file IS the source.
    staged_pdf = _staging_path(draft_id) / "source.pdf"
    if staged_pdf.exists():
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(staged_pdf, UPLOADS_DIR / f"{resolved['stem']}.pdf")
        shutil.copy2(_staging_path(draft_id) / "original.md",
                     UPLOADS_DIR / f"{resolved['stem']}.extracted.md")

    meta["status"] = "committed"
    meta["committed_at"] = _now().isoformat()
    meta["resolved"] = resolved
    _write_meta(draft_id, meta)

    result = {
        "draft_id": draft_id,
        "origin": meta["origin"],
        "filename": meta.get("filename"),
        "resolved_metadata": {
            "title": resolved["title"], "stem": resolved["stem"],
            "source_type": resolved["source_type"], "content_kind": resolved["content_kind"],
            "week": resolved["week"], "topic_ids": resolved["topic_ids"],
            "topic_tags": resolved["topic_tags"], "lecture_ref": resolved.get("lecture_ref"),
        },
        "pages": meta.get("pages"),
        "ocr_used": bool(meta.get("ocr_used")),
        "edited": edited,
        "chars_added": max(0, len(markdown) - len(original)),
        "chars_removed": max(0, len(original) - len(markdown)),
        "chunks_added": len(chunks),
        "cleaned_path": str(target.relative_to(ROOT_DIR)).replace("\\", "/"),
        "warnings": warnings,
        **classification,
    }
    _write_manifest_entry({
        **result,
        "created_at": meta.get("created_at"),
        "committed_at": meta["committed_at"],
        "source_note": resolved.get("source_note"),
        "replaced": bool(superseded),
        "superseded_chunks": len(superseded),
    })
    return result


def load_manifest() -> list[dict]:
    if not MANIFEST_PATH.exists():
        return []
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []


def rebuild_bank(db: Session) -> dict:
    """Full re-cluster from data/cleaned/ — the drift escape hatch.

    Everything an admin has committed is on disk under data/cleaned/ with its metadata
    in frontmatter, so this reproduces the whole bank including asserted topic tags.
    """
    with _BANK_LOCK:
        from ...config import QI_SOURCE_TYPES  # noqa: PLC0415

        sources = tuple(dict.fromkeys(tuple(QI_SOURCE_TYPES) + tuple(QI_ADMIN_SOURCE_TYPES)))
        units = qi.parse_question_units(source_types=sources)
        if not units:
            raise IngestError(503, "No question units found to rebuild from.", "nothing_to_rebuild")
        vectors = qi.embed_units(units)
        chunks = qi.load_chunk_index()
        qi.map_units_to_chunks(units, chunks)
        bank = qi.build_bank(units, vectors,
                             duplicate_threshold=QI_DUPLICATE_THRESHOLD,
                             cluster_distance=QI_CLUSTER_DISTANCE,
                             use_token_guard=QI_TOKEN_GUARD)
        question_repo.persist_bank(db, bank, vectors)
    db.commit()
    sync_outbox(db)
    invalidate_question_bank()
    return bank["stats"]
