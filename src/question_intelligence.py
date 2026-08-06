"""
question_intelligence.py
AI Question Intelligence Module — Milestone 1, Objective 8.

Deduplicates, clusters and maintains a repository of the course's questions and common
doubts. Pure functions plus a markdown parser, a markdown *writer* and an embedder; no
FastAPI and no DB. Imported by src/build_question_bank.py, the evaluation harness and
the API's question/ingest services.

Three things about the design that are easy to get wrong:

  1. The bank is built by PARSING THE SOURCES, not by reading vectors out of Qdrant.
     A retrieval chunk is a 384-char fragment, so a question is routinely split from
     its own options; parsing `data/cleaned/` yields whole questions instead. The live
     collection is never read, never rewritten and never re-embedded by this module.

  2. `canonical_count` and `member_count` are different numbers and must not be
     collapsed into one `size`. Clustering runs over canonicals, so a doubt asked five
     times contributes ONE canonical — while "which doubts are common?" is asking
     exactly how many times it was asked. Ranking by canonical_count inverts the
     result that deduplication just produced.

  3. The pq parser has an inverse, `render_question_markdown`. Admin-composed questions
     are rendered by the same module that parses them, so a hand-authored question
     cannot fail to land in the bank for want of the right heading level.

Threshold defaults live in src/config.py and should be set from `--thresholds` output
rather than guessed; the three sources behave differently enough that a single pooled
histogram hides what you most need to see.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Optional

import numpy as np

# `src` has no __init__.py, so it is an implicit namespace package: the absolute form
# works when the API imports this, the fallback when a script runs from src/ directly.
# Same shim llm_judge.py uses, for the same reason.
try:
    from src.prepare_rag_splits import extract_week, resolve_topic_ids, split_frontmatter
    from src.config import (
        QI_ASKED_SOURCE_TYPES, QI_MIN_DISPLAY_MEMBERS, QI_MIN_TITLE_READABILITY,
    )
except ModuleNotFoundError:  # pragma: no cover - import shim
    from prepare_rag_splits import (  # type: ignore[no-redef]
        extract_week, resolve_topic_ids, split_frontmatter,
    )
    from config import (  # type: ignore[no-redef]
        QI_ASKED_SOURCE_TYPES, QI_MIN_DISPLAY_MEMBERS, QI_MIN_TITLE_READABILITY,
    )

ROOT_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = ROOT_DIR / "data" / "cleaned"
SPLITS_DIR = ROOT_DIR / "data" / "splits"
# LEGACY IMPORT ONLY. Runtime persistence is relational: units, vectors, drafts, uploads
# and evaluation labels all live in the database, and nothing in the API or the build CLI
# reads or writes these paths. They exist so `migrate_question_bank_to_db.py` can still
# import a bank produced before the cutover, and so `export_question_bank.py` has a
# conventional place to write when an operator explicitly asks for a portable copy.
BANK_DIR = ROOT_DIR / "data" / "question_bank"
BANK_PATH = BANK_DIR / "question_bank.json"
VECTORS_PATH = BANK_DIR / "unit_vectors.npy"

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
SCHEMA_VERSION = 1

# Source types that carry questions at all. Anything else contributes retrieval chunks
# and no bank units — by design, not by accident.
_PROSE_SOURCES = {"notes", "transcripts", "kartik_sir_notes", "MLT Weekly Notes"}


# ── Header cleaning ───────────────────────────────────────────────────────────

_HEADER_JUNK_RE = re.compile(r"</?u>|</?b>|</?i>|[*_`]", re.IGNORECASE)
_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF←-⇿⬀-⯿]"
)


def clean_header(line: str) -> str:
    """Strip markdown decoration from a heading so it can be matched and displayed.

    Headers in this corpus arrive as `### **Statement**`, `## **<u>Question: 1</u>**`
    and `## Question/Topic: 📚 Topics Covered in Week 1` — leading hashes, bold markers,
    underline tags and emoji all have to come off before anything is stored or shown.
    """
    text = line.strip()
    text = re.sub(r"^#{1,6}\s*", "", text)
    text = _HEADER_JUNK_RE.sub("", text)
    text = _EMOJI_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def _is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s", line))


# ── PYQ boilerplate ───────────────────────────────────────────────────────────
# Every OCR'd PYQ block repeats the same scaffolding, and it is IDENTICAL ACROSS
# DOCUMENTS. Left in, BGE-small scores two unrelated PYQ questions as near-identical on
# the strength of it — the single largest threat to the deduplication precision target,
# and invisible until you read the text. `Typa` / `McO` are the OCR's rendering of
# "Type" / "MCQ".

_PYQ_BOILERPLATE_RE = re.compile(
    r"^\s*(?:"
    r"\[Extracted Question\]"
    r"|View\s+Solutions?\s*\(\d+\)"
    r"|Total\s+Marks?\s*[.:]?"
    r"|Marks?\s*[.:]?\s*\d*"
    r"|\d+\.\d{2}"
    r"|Typa|Type|Iype|ype|McO|MCQ|MSQ|NAT|SA"
    r"|Partial\s+Marking"
    r"|Accepted\s+Answers?"
    r"|Yes|No"
    r")\s*$",
    re.IGNORECASE,
)

# Fragments that survive *inline* rather than on their own line, because the OCR joined
# them onto the question text. Measured against the corpus: leaving these in does two
# kinds of damage — they pad the embedded text with strings identical across documents,
# and their numerals (question ids, mark totals) show up as spurious differences to the
# numeral guard below, which then vetoes genuine duplicates.
_PYQ_INLINE_NOISE = [
    re.compile(r"Question\s*\d{1,3}\s*:?\s*\d{6,}", re.IGNORECASE),   # "Question 4 640653738035"
    re.compile(r"\bTotal\s+Marks?\s*[.:]?\s*\d*\.?\d*", re.IGNORECASE),
    re.compile(r"\bView\s+(?:Parent\s+QN|Solutions?)\s*\(?\d*\)?", re.IGNORECASE),
    re.compile(r"\bParent\s+QN\b", re.IGNORECASE),
    re.compile(r"\bAnswer\s*\(Numeric\)\s*:?", re.IGNORECASE),
    re.compile(r"\b\d\.\d{2}\s*\|\s*(?:Type|Typa|Iype)\b", re.IGNORECASE),
    re.compile(r"\b(?:Typa|Iype)\b", re.IGNORECASE),
]


def strip_pyq_boilerplate(text: str) -> str:
    """Remove the recurring OCR scaffolding from an extracted PYQ block.

    This is the single largest threat to the deduplication precision target, and it is
    invisible until you read the text. Every extracted block repeats the same
    scaffolding — `[Extracted Question]`, `Question 2 : 640653738030`, `View Solutions
    (0)`, `Total Mark .`, `4.00`, `Typa`, `McO` (the OCR's rendering of "Type" and
    "MCQ") — it is a large fraction of a short unit, and it is IDENTICAL ACROSS
    DIFFERENT DOCUMENTS. Left in, BGE-small scores two unrelated PYQ questions as
    near-identical on the strength of it alone.
    """
    kept = []
    for raw in (text or "").splitlines():
        line = raw.lstrip("> ").strip()
        if not line:
            continue
        if _PYQ_BOILERPLATE_RE.match(line):
            continue
        for pattern in _PYQ_INLINE_NOISE:
            line = pattern.sub(" ", line)
        line = re.sub(r"\s{2,}", " ", line).strip(" |")
        if line:
            kept.append(line)
    return "\n".join(kept).strip()


# ── Unit model ────────────────────────────────────────────────────────────────

def _make_unit(source_type: str, stem: str, index: int, *, title: str, text: str,
               week: int, source_file: str, options: Optional[list[str]] = None,
               answer: str = "", solution: str = "", origin: str = "corpus") -> dict:
    return {
        "unit_id": f"{source_type}/{stem}#{index}",
        "source_type": source_type,
        "week": week,
        "source_file": source_file,
        "title": title,
        "text": text,
        "options": options or [],
        "answer": answer,
        "solution": solution,
        "origin": origin,
        "chunk_doc_ids": [],
    }


# ── Parsers ───────────────────────────────────────────────────────────────────
# Three source shapes, three parsers behind one interface. The dispatch is keyed on
# source type with a `discourse` slot reserved, so forum content is picked up by adding
# one function if a scraper ever lands.

_QUESTION_MARKER_RE = re.compile(r"^Question[\s:._\-–—]*(\d+)", re.IGNORECASE)
_COMMON_DATA_RE = re.compile(r"^Common\s+Data\s+for\s+questions?", re.IGNORECASE)
_SECTION_NAMES = {"statement", "options", "answer", "solution"}
_OPTION_LABEL_RE = re.compile(r"^\(([a-z])\)$", re.IGNORECASE)


def _looks_like_question_marker(line: str) -> tuple[bool, str]:
    """A question boundary is a heading OR a bare bold line, at any level.

    Both forms occur in the corpus — `## **<u>Question: 1</u>**` in most weeks and a
    bare `**<u>Question-1</u>**` paragraph in others, with week 5 using `#` for the
    question and `##` for its sections. Matching on the cleaned text rather than the
    heading depth is what makes one parser handle all of them.
    """
    stripped = line.strip()
    if not (_is_heading(stripped) or (stripped.startswith("**") and stripped.endswith("**"))):
        return False, ""
    cleaned = clean_header(stripped)
    if _QUESTION_MARKER_RE.match(cleaned) or _COMMON_DATA_RE.match(cleaned):
        return True, cleaned
    return False, ""


def _section_of(line: str) -> Optional[str]:
    if not _is_heading(line):
        return None
    cleaned = clean_header(line).rstrip(":").strip().lower()
    return cleaned if cleaned in _SECTION_NAMES else None


def _parse_options(lines: list[str]) -> list[str]:
    """Turn an Options block into a list of option strings.

    Labels arrive as their own sub-heading (`#### **(a)**`) with the option text on a
    following line, so the label and its body have to be re-joined.
    """
    options: list[str] = []
    current: Optional[list[str]] = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        cleaned = clean_header(line) if _is_heading(line) else _HEADER_JUNK_RE.sub("", line).strip()
        if _OPTION_LABEL_RE.match(cleaned):
            if current is not None:
                options.append(" ".join(current).strip())
            current = []
            continue
        if current is not None:
            current.append(line)
        elif options:
            options[-1] = (options[-1] + " " + line).strip()
    if current is not None:
        options.append(" ".join(current).strip())
    return [o for o in options if o]


def _parse_pq(content: str, stem: str, week: int, source_file: str,
              source_type: str = "pq") -> list[dict]:
    """Practice sets — the clean path. Statement / Options / Answer / Solution."""
    lines = content.splitlines()
    blocks: list[tuple[str, list[str]]] = []
    title: Optional[str] = None
    buffer: list[str] = []

    for line in lines:
        is_marker, marker_title = _looks_like_question_marker(line)
        if is_marker:
            if title is not None:
                blocks.append((title, buffer))
            title, buffer = marker_title, []
            continue
        if title is not None:
            buffer.append(line)
    if title is not None:
        blocks.append((title, buffer))

    # No question markers at all — fall back to Statement-delimited blocks rather than
    # returning the whole file as one unit.
    if not blocks:
        blocks = _statement_delimited_blocks(lines)

    units: list[dict] = []
    for index, (block_title, body) in enumerate(blocks, start=1):
        sections: dict[str, list[str]] = {}
        current = "statement"
        for line in body:
            name = _section_of(line)
            if name:
                current = name
                sections.setdefault(current, [])
                continue
            sections.setdefault(current, []).append(line)

        statement = "\n".join(sections.get("statement", [])).strip()
        options = _parse_options(sections.get("options", []))
        answer = " ".join(x.strip() for x in sections.get("answer", []) if x.strip()).strip()
        solution = "\n".join(sections.get("solution", [])).strip()

        if not statement and not options:
            continue

        first = re.split(r"(?<=[.?])\s", statement.replace("\n", " ").strip(), maxsplit=1)
        display = (first[0] if first and first[0] else block_title).strip()
        units.append(_make_unit(
            source_type, stem, index,
            title=(display[:140] or block_title),
            text=statement or block_title,
            week=week, source_file=source_file,
            options=options, answer=answer, solution=solution,
        ))
    return units


def _statement_delimited_blocks(lines: list[str]) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    buffer: list[str] = []
    started = False
    for line in lines:
        if _section_of(line) == "statement":
            if started:
                blocks.append(("Question", buffer))
            started, buffer = True, [line]
            continue
        if started:
            buffer.append(line)
    if started:
        blocks.append(("Question", buffer))
    return blocks


def is_faq_furniture(title: str, body: str) -> bool:
    """True for site navigation and contact footers masquerading as FAQ sections.

    Measured, not guessed: `Need Help?` (5) and `Need Assistance?` (7) are the same
    contact footer under two titles, one per weekly FAQ file — 12 identical units that
    dedup correctly groups and that would then top the common-doubts ranking with a
    support email address. This is the FAQ analogue of the PYQ scaffolding problem, and
    the same fix applies: drop it before embedding rather than explaining it afterwards.
    """
    if _FAQ_FURNITURE_TITLE_RE.match(title.strip()):
        return True
    stripped = _EMOJI_RE.sub("", body or "").strip()
    if len(stripped) < 200 and _FAQ_NAV_RE.search(stripped):
        return True
    return False


_FAQ_FURNITURE_TITLE_RE = re.compile(
    r"^(need\s+(help|assistance)|back\s+to\s+home|contact|navigation)\b\??$", re.IGNORECASE
)
_FAQ_NAV_RE = re.compile(
    r"(back\s+to\s+home|for\s+any\s+technical\s+issues|please\s+contact)", re.IGNORECASE
)


def _parse_faq(content: str, stem: str, week: int, source_file: str,
               source_type: str = "faq") -> list[dict]:
    """Weekly FAQs — `## Question/Topic: <emoji> <name>` followed by prose.

    These are TOPIC EXPLAINERS, not questions students asked. That distinction changes
    how the metrics read, which is why the evaluation harness reports per source type
    as well as pooled.
    """
    units: list[dict] = []
    title: Optional[str] = None
    buffer: list[str] = []
    index = 0

    def flush():
        nonlocal index, title, buffer
        if title is None:
            return
        body = "\n".join(buffer).strip()
        if body and not is_faq_furniture(title, body):
            index += 1
            units.append(_make_unit(
                source_type, stem, index,
                title=title[:140], text=body,
                week=week, source_file=source_file,
            ))
        title, buffer = None, []

    for line in content.splitlines():
        if _is_heading(line):
            cleaned = clean_header(line)
            if cleaned.lower().startswith("question/topic"):
                flush()
                title = cleaned.split(":", 1)[1].strip() if ":" in cleaned else cleaned
                continue
        if title is not None:
            buffer.append(line)
    flush()
    return units


def _parse_pyq(content: str, stem: str, week: int, source_file: str,
               source_type: str = "PYQ") -> list[dict]:
    """Past papers — OCR output, so question boundaries are not recoverable.

    Splitting on `> **[Extracted Question]**` blocks and treating each as one unit is
    an honest description of what the text supports; pretending to parse statement and
    options here would manufacture structure the OCR destroyed.
    """
    units: list[dict] = []
    blocks = re.split(r"^>\s*\*\*\[Extracted Question\]\*\*\s*$", content, flags=re.MULTILINE)
    index = 0
    for block in blocks[1:]:
        body: list[str] = []
        for line in block.splitlines():
            if line.strip().startswith(">"):
                body.append(line)
            elif body:
                break
        text = strip_pyq_boilerplate("\n".join(body))
        if len(text) < 25:
            continue
        index += 1
        first = re.split(r"(?<=[.?])\s", text.replace("\n", " "), maxsplit=1)
        units.append(_make_unit(
            source_type, stem, index,
            title=(first[0] if first else text)[:140],
            text=text, week=week, source_file=source_file,
        ))
    return units


_PARSERS = {
    "pq": _parse_pq,
    "faq": _parse_faq,
    "PYQ": _parse_pyq,
    # "discourse": _parse_discourse — reserved; see module docstring.
}


def parser_for(source_type: str):
    """Return the parser for a source type, or None if it carries no questions."""
    return _PARSERS.get(source_type)


# A unit needs a minimum of actual content to be a unit at all. Measured: nine `pq`
# questions survive the PDF -> markdown conversion as the bare stem "What is the value
# of ?" — every formula, matrix and numeral in them was dropped, leaving four units in
# week 10 and five in week 8 with byte-identical text. They are not questions, and they
# are actively harmful: BGE-small scores them at 1.0 against each other, so they
# manufacture duplicate pairs that no threshold can separate. Two `faq` entries fail the
# same way (a heading whose body is the heading repeated).
#
# The bar is deliberately low. `faq/week09_faq#8` — "Upper Bound: \[ \|w^t\|^2 \leq t
# \cdot R^2 \]" — is 55 characters of real mathematics and must survive.
MIN_UNIT_CHARS = 40


def is_degenerate_unit(unit: dict) -> bool:
    """True for units carrying too little content to deduplicate or display.

    Options count as content: a short stem with four distinct options is answerable and
    distinguishable, which is exactly what the bare stems above are not.
    """
    if unit.get("options"):
        return False
    return len((unit.get("text") or "").strip()) < MIN_UNIT_CHARS


def parse_markdown(content: str, *, source_type: str, stem: str, week: int,
                   source_file: str = "") -> list[dict]:
    """Parse one document's markdown into question units."""
    parser = _PARSERS.get(source_type)
    if parser is None:
        return []
    _, body = split_frontmatter(content)
    units = parser(body, stem, week, source_file or stem, source_type)
    return [u for u in units if not is_degenerate_unit(u)]


def parse_question_units(cleaned_dir: Path | None = None,
                         source_types: Iterable[str] = ("faq", "pq", "PYQ", "discourse"),
                         extra_documents: Iterable[dict] | None = None,
                         ) -> list[dict]:
    """Emit one unit per question over the corpus **and** the database's own documents.

    Two inputs, deliberately: `data/cleaned/<source_type>/*.md` is the offline pipeline's
    output and stays read-only, while `extra_documents` carries admin-contributed content
    that now lives in `question_documents` rather than in a file. Each entry is
    `{markdown, source_type, stem, week, source_file}` — the same four values the file
    walk derives from a path — so both go through one parser and neither can drift.

    A database document wins on stem collision: `question_documents.stem` is unique and
    a document that replaced a corpus file must not be parsed twice.
    """
    cleaned_dir = Path(cleaned_dir or CLEANED_DIR)
    documents = list(extra_documents or [])
    db_stems = {d["stem"] for d in documents}

    units: list[dict] = []
    for source_type in source_types:
        folder = cleaned_dir / source_type
        if not folder.is_dir():
            continue
        for md_file in sorted(folder.glob("*.md")):
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            if not content.strip():
                continue
            stem = md_file.stem.replace(" ", "_")
            if stem in db_stems:
                continue
            units.extend(parse_markdown(
                content,
                source_type=source_type,
                stem=stem,
                week=extract_week(md_file),
                source_file=f"{source_type}/{md_file.name}",
            ))

    for document in documents:
        content = document.get("markdown") or ""
        if not content.strip():
            continue
        units.extend(parse_markdown(
            content,
            source_type=document["source_type"],
            stem=document["stem"],
            week=int(document.get("week") or 0),
            source_file=document.get("source_file") or f"{document['source_type']}/{document['stem']}.md",
        ))
    return units


# ── Markdown writer — the inverse of `_parse_pq` ──────────────────────────────

def render_question_markdown(questions: list[dict], start: int = 1) -> str:
    """Render structured questions into the exact shape `_parse_pq` reads.

    This is why an admin-composed question cannot fail to parse: the renderer and the
    parser live in one module and are round-tripped in verification. Asking an admin to
    reproduce this markup by hand would make authoring a formatting exercise with a
    silent failure mode — a near-miss yields chunks that retrieve fine and no unit.
    """
    out: list[str] = ["# **Practice**", ""]
    for offset, question in enumerate(questions):
        number = start + offset
        statement = (question.get("statement") or "").strip()
        options = [str(o).strip() for o in (question.get("options") or []) if str(o).strip()]
        answer = (question.get("answer") or "").strip()
        solution = (question.get("solution") or "").strip()

        out += [f"## **<u>Question {number}</u>**", "", "### **Statement**", "", statement, ""]
        if options:
            out += ["### **Options**", ""]
            for i, option in enumerate(options):
                out += [f"#### **({chr(ord('a') + i)})**", "", option, ""]
        out += ["### **Answer**", "", answer, ""]
        if solution:
            out += ["### **Solution**", "", solution, ""]
    return "\n".join(out).strip() + "\n"


def validate_composed_questions(questions: list[dict]) -> list[str]:
    """Return a list of human-readable errors, empty when the batch is authorable.

    The MCQ rules mirror `quiz_service.grade_answer` exactly: options non-empty means
    MCQ, and the submission must match one of the served options. A question whose
    answer is not among its options would be unanswerable at grading time, so it is
    refused at authoring time instead of shipping.
    """
    errors: list[str] = []
    if not questions:
        return ["at least one question is required"]
    for i, question in enumerate(questions):
        label = f"question {i + 1}"
        statement = (question.get("statement") or "").strip()
        options = [str(o).strip() for o in (question.get("options") or []) if str(o).strip()]
        answer = (question.get("answer") or "").strip()
        if not statement:
            errors.append(f"{label}: statement is empty")
        if not answer:
            errors.append(f"{label}: answer is empty")
        if options:
            if len(options) < 2:
                errors.append(f"{label}: an MCQ needs at least two options")
            if len(set(o.lower() for o in options)) != len(options):
                errors.append(f"{label}: options must be distinct")
            if answer and answer.lower() not in {o.lower() for o in options}:
                errors.append(f"{label}: answer must be one of the options")
    return errors


# ── Embedding ─────────────────────────────────────────────────────────────────

def unit_embedding_text(unit: dict) -> str:
    """The text a unit is embedded from. PYQ is boilerplate-stripped at parse time."""
    parts = [unit.get("title", ""), unit.get("text", "")]
    parts.extend(unit.get("options") or [])
    return "\n".join(p for p in parts if p).strip()


def unit_text_hash(unit: dict) -> str:
    """Cache key for a unit's embedding: the model plus the exact text embedded.

    Keyed on the text rather than on `unit_id` so that re-parsing, renumbering or moving
    a question to a different file reuses the vector, and so that *editing* it cannot.
    """
    payload = f"{EMBED_MODEL}\x1f{unit_embedding_text(unit)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def embed_units(units: list[dict], model_name: str = EMBED_MODEL) -> np.ndarray:
    """Embed units with the SAME model and class the live collection was built with.

    Matching `dependencies.py` and `ingest_to_qdrant.py` means the bank's vector space
    is the collection's, so a query embedded by either side is comparable. Weights are
    already on disk; a few hundred units is a local run of seconds.
    """
    from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

    if not units:
        return np.zeros((0, 384), dtype=np.float32)
    embedder = FastEmbedEmbeddings(model_name=model_name)
    vectors = embedder.embed_documents([unit_embedding_text(u) for u in units])
    return np.asarray(vectors, dtype=np.float32)


def l2_normalise(vectors: np.ndarray) -> np.ndarray:
    if vectors.size == 0:
        return vectors
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


# ── Deduplication ─────────────────────────────────────────────────────────────

# ── The discriminative-token guard ────────────────────────────────────────────
# Cosine similarity alone does not separate duplicates from non-duplicates in this
# corpus, and the reason is specific rather than general. Measured on a hand-labelled
# seed batch, `faq` reaches 100% precision at 0.95 while `PYQ` is stuck near 50% at
# EVERY threshold from 0.93 to 0.97 — raising the bar just loses recall without gaining
# precision.
#
# The PYQ false positives all share one shape: a past paper asks the same templated
# question several times over, varying only a numeral or a polarity word, and the whole
# meaning lives in exactly the token a dense embedding is least sensitive to.
#
#     "...becomes smoother with INCREASING value of k"   cos 0.976
#     "...becomes smoother with DECREASING value of k"   <- the opposite claim
#
#     "Find the value of c + d"        vs  "Find the value of a + c + e"
#     "P(xtest [0 1 0] | y=1) = 0.0156" vs "P(xtest [1 0] | y=1) = 0.057"
#
# So the edge test is dense similarity AND lexical agreement on the tokens that carry
# the difference. On the seed batch this vetoes 7 of 7 PYQ false positives while
# keeping 3 of 5 true ones — precision 50% -> 100%, at a cost in recall that is worth
# paying for a metric whose target is precision.

_NUMERAL_RE = re.compile(r"(?<![\w.])\d{1,5}(?:\.\d+)?(?![\w])")

# Antonym pairs whose members are near-identical in embedding space and opposite in
# meaning. Only pairs that actually occur in course questions.
_POLARITY_PAIRS = (
    ("increas", "decreas"),
    ("higher", "lower"),
    ("larger", "smaller"),
    ("maximiz", "minimiz"),
    ("more", "less"),
    ("with", "without"),
    ("odd", "even"),
    ("row", "column"),
)


def discriminative_signature(text: str) -> tuple[frozenset[str], frozenset[str]]:
    """The numerals and polarity markers a duplicate claim has to agree on."""
    lowered = (text or "").lower()
    numerals = frozenset(_NUMERAL_RE.findall(lowered))
    polarity = frozenset(
        f"{i}{'a' if term == pair[0] else 'b'}"
        for i, pair in enumerate(_POLARITY_PAIRS)
        for term in pair
        if term in lowered
    )
    return numerals, polarity


def tokens_conflict(text_a: str, text_b: str) -> bool:
    """True when two texts disagree on a numeral or a polarity word.

    Asymmetry is deliberate: a numeral present in one and absent from the other is a
    conflict, because in a templated question the numeral IS the question.
    """
    nums_a, pol_a = discriminative_signature(text_a)
    nums_b, pol_b = discriminative_signature(text_b)
    if nums_a != nums_b:
        return True
    return pol_a != pol_b


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def resolve_threshold(threshold, source_type: str) -> float:
    """Per-source thresholds, because the sources genuinely disagree.

    Accepts a float (one threshold for everything) or a mapping keyed by source type
    with an optional `default`.
    """
    if isinstance(threshold, dict):
        return float(threshold.get(source_type, threshold.get("default", 0.95)))
    return float(threshold)


def build_duplicate_groups(vectors: np.ndarray, units: list[dict],
                           threshold, use_token_guard: bool = True,
                           ) -> tuple[list[list[int]], list[int]]:
    """Group near-duplicate units and pick a canonical member for each group.

    There is NO adjacency guard, and that is a consequence of parsing the sources: an
    earlier design derived units from retrieval chunks, where `chunk_overlap=50` made
    consecutive chunks share text by construction and score as duplicates. Parsed
    question units have no splitter overlap, so a guard would have nothing to reject —
    and the precision metric stops being an artifact of one.

    Canonical = the group MEDOID (highest mean cosine to the rest, ties broken by
    longer text), so the representative is the most central phrasing of the doubt
    rather than an accident of file order.
    """
    n = len(units)
    if n == 0:
        return [], []
    normalised = l2_normalise(vectors)
    similarity = normalised @ normalised.T

    uf = _UnionFind(n)
    # An edge needs to clear the *stricter* of the two units' thresholds, so a cautious
    # source cannot be dragged into a group by a permissive one.
    per_unit = [resolve_threshold(threshold, u.get("source_type", "")) for u in units]
    lowest = min(per_unit) if per_unit else 1.0
    for i, j in np.argwhere(similarity >= lowest):
        i, j = int(i), int(j)
        if i >= j:
            continue
        if similarity[i, j] < max(per_unit[i], per_unit[j]):
            continue
        if use_token_guard and tokens_conflict(units[i].get("text", ""), units[j].get("text", "")):
            continue
        uf.union(i, j)

    grouped: dict[int, list[int]] = {}
    for idx in range(n):
        grouped.setdefault(uf.find(idx), []).append(idx)

    groups: list[list[int]] = []
    canonicals: list[int] = []
    for members in sorted(grouped.values(), key=lambda m: m[0]):
        if len(members) == 1:
            best = members[0]
        else:
            sub = similarity[np.ix_(members, members)]
            # Exclude the self-similarity term so a group of two is not a tie by construction.
            centrality = (sub.sum(axis=1) - np.diag(sub)) / max(len(members) - 1, 1)
            best_rank = max(
                range(len(members)),
                key=lambda k: (float(centrality[k]), len(units[members[k]].get("text", ""))),
            )
            best = members[best_rank]
        groups.append(members)
        canonicals.append(best)
    return groups, canonicals


# ── Clustering ────────────────────────────────────────────────────────────────

def average_linkage_clusters(vectors: np.ndarray, cut_distance: float) -> list[int]:
    """Average-linkage agglomerative clustering, cut at `cut_distance` (cosine).

    Hand-rolled in numpy rather than adding scikit-learn for one function call. Average
    linkage over single linkage because single linkage chains — one bridging pair merges
    two unrelated concepts — and over k-means because the number of distinct doubts is
    not known in advance. O(n^2) is instant at these sizes.
    """
    n = len(vectors)
    if n == 0:
        return []
    if n == 1:
        return [0]

    normalised = l2_normalise(vectors)
    distance = 1.0 - (normalised @ normalised.T)
    np.fill_diagonal(distance, np.inf)

    sizes = np.ones(n, dtype=np.float64)
    active = np.ones(n, dtype=bool)
    assignment = list(range(n))
    members: dict[int, list[int]] = {i: [i] for i in range(n)}

    while active.sum() > 1:
        masked = np.where(np.outer(active, active), distance, np.inf)
        np.fill_diagonal(masked, np.inf)
        flat = int(np.argmin(masked))
        a, b = divmod(flat, n)
        if not np.isfinite(masked[a, b]) or masked[a, b] > cut_distance:
            break

        # Lance–Williams update for average linkage: the merged cluster's distance to
        # every other cluster is the size-weighted mean of its parts'.
        merged = (sizes[a] * distance[a, :] + sizes[b] * distance[b, :]) / (sizes[a] + sizes[b])
        distance[a, :] = merged
        distance[:, a] = merged
        distance[a, a] = np.inf
        sizes[a] += sizes[b]
        active[b] = False
        members[a].extend(members.pop(b))

    for cluster_id, root in enumerate(np.flatnonzero(active)):
        for idx in members[int(root)]:
            assignment[idx] = cluster_id
    return assignment


def assign_new_units(new_vectors: np.ndarray, bank_vectors: np.ndarray,
                     bank_units: list[dict], clusters: list[dict],
                     duplicate_threshold: float, cluster_distance: float,
                     ) -> list[dict]:
    """Classify freshly parsed units against an existing bank — not a re-clustering.

    Existing cluster IDs are preserved because the UI deep-links by cluster ID and a
    re-cluster on every contribution would make the common-doubts ranking jump around.
    Drift is handled by an explicit `--rebuild`, never silently.

    Cluster membership is decided by MEAN DISTANCE TO A CLUSTER'S CANONICAL MEMBERS,
    not by distance to a centroid: the batch clustering above merges on mean pairwise
    distance, and the two criteria disagree on elongated clusters. An incremental rule
    that disagrees with the batch rule manufactures the drift it exists to avoid.
    """
    results: list[dict] = []
    if new_vectors.size == 0:
        return results

    new_norm = l2_normalise(new_vectors)
    bank_norm = l2_normalise(bank_vectors) if bank_vectors.size else bank_vectors
    by_id = {u["unit_id"]: i for i, u in enumerate(bank_units)}
    next_cluster = (max((c["cluster_id"] for c in clusters), default=-1) + 1)

    for row in range(new_norm.shape[0]):
        vector = new_norm[row]
        outcome = {"dup_group_id": None, "is_canonical": True,
                   "cluster_id": None, "matched_unit_id": None, "new_cluster": False}

        if bank_norm.size:
            similarity = bank_norm @ vector
            best = int(np.argmax(similarity))
            if float(similarity[best]) >= duplicate_threshold:
                incumbent = bank_units[best]
                outcome["dup_group_id"] = incumbent.get("dup_group_id")
                outcome["cluster_id"] = incumbent.get("cluster_id")
                outcome["matched_unit_id"] = incumbent["unit_id"]
                # Joins the group; becomes canonical only if more central than the
                # incumbent medoid, which for a group of two is the longer text.
                outcome["is_canonical"] = False
                results.append(outcome)
                continue

        best_cluster, best_distance = None, np.inf
        for cluster in clusters:
            rows = [by_id[uid] for uid in cluster.get("member_unit_ids", []) if uid in by_id]
            rows = [r for r in rows if bank_units[r].get("is_canonical")]
            if not rows:
                continue
            mean_distance = float(np.mean(1.0 - (bank_norm[rows] @ vector)))
            if mean_distance < best_distance:
                best_cluster, best_distance = cluster["cluster_id"], mean_distance

        if best_cluster is not None and best_distance <= cluster_distance:
            outcome["cluster_id"] = best_cluster
        else:
            outcome["cluster_id"] = next_cluster
            outcome["new_cluster"] = True
            next_cluster += 1
        results.append(outcome)
    return results


# ── Titles ────────────────────────────────────────────────────────────────────

def title_readability(text: str) -> float:
    """How much of a candidate title is prose rather than OCR debris.

    PYQ titles routinely come back as `[x1 x2]| v:]) + 1 Vz (x1y1 + ...` — the OCR's
    rendering of a matrix. Such a string is a legal title and a useless label, and the
    only thing separating it from real prose is its character mix.

    Public because it is used twice and the two uses answer different questions:
    `pick_cluster_title` asks "which of these titles is least bad", which always returns
    something, and `is_displayable_cluster` asks "is the best one good enough to show",
    which is the only place that can answer no.
    """
    stripped = (text or "").strip()
    if not stripped:
        return 0.0
    letters = sum(1 for ch in stripped if ch.isalpha())
    spaces = stripped.count(" ")
    if spaces < 1:
        return 0.0
    return letters / len(stripped)


def cluster_title(unit: dict) -> str:
    """Label a cluster from a unit's parsed text.

    Titles come from the parsed unit, not from stored h1/h2 chunk metadata. Measured
    over data/splits, metadata titles are only usable for FAQ: pq's most common h2 is
    `**<u>Question-1</u>**` (a position label) and PYQ's is `Solution` or nothing at
    all, so 569 of the units would have been labelled "Question-1" or "Solution".
    """
    title = (unit.get("title") or "").strip()
    if title and not _QUESTION_MARKER_RE.match(title) and title.lower() != "solution":
        return title[:120]
    text = (unit.get("text") or "").replace("\n", " ").strip()
    if text:
        first = re.split(r"(?<=[.?])\s", text, maxsplit=1)[0]
        if first:
            return first[:120]
    return f"Week {unit.get('week', 0)} - {unit.get('source_type', 'unknown')}"


# Readable-title preference. faq headers are curated topic names, pq statements are
# clean prose, PYQ is OCR output — so a mixed cluster should not be labelled by its
# noisiest member just because that member happens to be the medoid.
_TITLE_SOURCE_RANK = {"faq": 0, "pq": 1, "PYQ": 2}


def pick_cluster_title(units_in_cluster: list[dict]) -> str:
    """Choose the most legible label available in a cluster.

    The medoid is the most *central* member, which is not the same as the best-named
    one: a cluster whose medoid is a PYQ scan would otherwise be titled with a fragment
    of a garbled matrix while a perfectly good FAQ heading sat one row below it.
    """
    if not units_in_cluster:
        return "Untitled"
    scored = sorted(
        units_in_cluster,
        key=lambda u: (
            -round(title_readability(cluster_title(u)), 2),
            _TITLE_SOURCE_RANK.get(u.get("source_type", ""), 3),
        ),
    )
    return cluster_title(scored[0])


def is_displayable_cluster(cluster: dict, *, min_members: int = QI_MIN_DISPLAY_MEMBERS,
                           min_readability: float = QI_MIN_TITLE_READABILITY) -> bool:
    """Is this cluster worth listing to a student as a "concept group"?

    Three failures the grouping itself cannot detect, because in each the clustering was
    CORRECT and the input was not:

    1. A singleton grouped nothing. It is a question with a header, and listing it under
       a heading that promises a group is a claim the bank cannot support.

    2. A cluster with no `asked` member — no faq/pq unit — is not a concept group at all.
       PYQ unit boundaries come from the OCR's `[Extracted Question]` markers, so such a
       cluster is either one printed question split into fragments that then re-grouped
       (correctly, they ARE near-identical) or several questions grouped on the exam
       scaffolding they share. Measured over the live bank, all 28 multi-member PYQ-only
       clusters were one of those two: matrix debris, four `COMPREHENSION Based on the
       above data...` groups, and `Question 19 640653852840 0 Type ...`. None was a
       concept. This is the same fact the module docstring states about PYQ boundaries,
       applied to display instead of to parsing.

    3. A cluster with an unreadable title cannot be recognised, searched for or chosen,
       whatever its membership. `title_readability` catches symbol soup; note it does NOT
       catch alphabetic debris like `Pl 1 Xtest _ test 0 Xtest_ test 0 otherwise` (0.53,
       comfortably above the floor) — rule 2 is what removes that, and the two are kept
       separate because a character ratio was never going to distinguish meaningless
       words from meaningful ones.

    Takes the summary dict — `{title, member_count, asked_count}` — rather than the units,
    so the build path and the API read path apply one rule to the same three numbers
    instead of each growing its own. Membership, embeddings and quiz grounding are
    unaffected: this decides listing only, and `get_cluster(id)` deliberately does not
    consult it so an existing deep link never 404s on a policy change.
    """
    if int(cluster.get("member_count", 0)) < min_members:
        return False
    if int(cluster.get("asked_count", 0)) < 1:
        return False
    return title_readability(cluster.get("title") or "") >= min_readability


# ── Chunk mapping ─────────────────────────────────────────────────────────────

def load_chunk_index(splits_dir: Path | None = None) -> list[dict]:
    """Load every chunk from data/splits/*.jsonl as {doc_id, source_type, text}."""
    splits_dir = Path(splits_dir or SPLITS_DIR)
    chunks: list[dict] = []
    for path in sorted(splits_dir.glob("*_chunks.jsonl")):
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                meta = row.get("metadata", {})
                chunks.append({
                    "doc_id": meta.get("doc_id", ""),
                    "source_type": meta.get("source_type", ""),
                    "text": row.get("text", ""),
                })
    return chunks


_WORD_RE = re.compile(r"[a-z0-9]+")


def _shingles(text: str, size: int = 5) -> set[str]:
    words = _WORD_RE.findall((text or "").lower())
    if len(words) < size:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + size]) for i in range(len(words) - size + 1)}


def map_units_to_chunks(units: list[dict], chunks: list[dict],
                        min_overlap: int = 1) -> None:
    """Link each unit to the retrieval doc_ids whose text it overlaps, in place.

    This is the only place the two atoms — a whole question and a 384-char chunk — have
    to meet, and it is what lets the API go from a retrieved chunk back to a question
    unit for `related_questions` and the quiz dedupe.
    """
    by_source: dict[str, list[dict]] = {}
    for chunk in chunks:
        by_source.setdefault(chunk["source_type"], []).append(chunk)
    shingled = {
        source: [(c["doc_id"], _shingles(c["text"])) for c in items]
        for source, items in by_source.items()
    }

    for unit in units:
        candidates = shingled.get(unit["source_type"], [])
        if not candidates:
            unit["chunk_doc_ids"] = []
            continue
        stem = unit["unit_id"].split("/", 1)[1].split("#", 1)[0]
        target = _shingles(unit_embedding_text(unit))
        matches = [
            doc_id for doc_id, chunk_shingles in candidates
            if doc_id.startswith(f"{stem}_chunk_") and len(target & chunk_shingles) >= min_overlap
        ]
        unit["chunk_doc_ids"] = matches


def assert_unit_index_sane(units: list[dict], chunks: list[dict]) -> list[str]:
    """Warn if a unit's stem collides with a stem from another source type.

    `doc_id` has no directory component — across 9,427 chunks only 6,381 are unique —
    so `related_to_doc_ids` is sound only while the question sources' stems do not
    intersect any other source's. That is an invariant the admin upload path can break,
    which is why it is checked at load time rather than assumed.
    """
    question_stems: dict[str, str] = {}
    for unit in units:
        stem = unit["unit_id"].split("/", 1)[1].split("#", 1)[0]
        question_stems[stem] = unit["source_type"]

    warnings: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        doc_id = chunk["doc_id"]
        if "_chunk_" not in doc_id:
            continue
        stem = doc_id.rsplit("_chunk_", 1)[0]
        owner = question_stems.get(stem)
        if owner and chunk["source_type"] != owner and stem not in seen:
            seen.add(stem)
            warnings.append(
                f"stem '{stem}' exists under both '{owner}' and '{chunk['source_type']}' — "
                "related-question lookups for it are ambiguous"
            )
    return warnings


# ── Bank assembly ─────────────────────────────────────────────────────────────

def build_bank(units: list[dict], vectors: np.ndarray, *, duplicate_threshold,
               cluster_distance: float, use_token_guard: bool = True) -> dict:
    """Deduplicate, cluster and assemble the full bank artifact."""
    groups, canonicals = build_duplicate_groups(
        vectors, units, duplicate_threshold, use_token_guard=use_token_guard
    )

    for unit in units:
        unit["dup_group_id"] = None
        unit["is_canonical"] = False
    for group_id, (members, canonical) in enumerate(zip(groups, canonicals)):
        for idx in members:
            units[idx]["dup_group_id"] = group_id
        units[canonical]["is_canonical"] = True

    canonical_rows = list(canonicals)
    canonical_vectors = vectors[canonical_rows] if canonical_rows else np.zeros((0, vectors.shape[1] if vectors.size else 384), dtype=np.float32)
    assignment = average_linkage_clusters(canonical_vectors, cluster_distance)

    group_size = {group_id: len(members) for group_id, members in enumerate(groups)}
    # Counted per MEMBER, not per canonical: a duplicate group can span sources, and it is
    # the individual unit's own source type that decides whether it represents somebody
    # asking. See QI_ASKED_SOURCE_TYPES for why PYQ does not.
    group_asked = {
        group_id: sum(1 for idx in members
                      if units[idx]["source_type"] in QI_ASKED_SOURCE_TYPES)
        for group_id, members in enumerate(groups)
    }
    clusters: dict[int, dict] = {}
    for position, row in enumerate(canonical_rows):
        cluster_id = assignment[position]
        unit = units[row]
        cluster = clusters.setdefault(cluster_id, {
            "cluster_id": cluster_id,
            "title": "",
            "canonical_count": 0,
            "member_count": 0,
            "asked_count": 0,
            "weeks": [],
            "sources": [],
            "medoid_unit_id": unit["unit_id"],
            "member_unit_ids": [],
        })
        cluster["canonical_count"] += 1
        cluster["member_count"] += group_size.get(unit["dup_group_id"], 1)
        cluster["asked_count"] += group_asked.get(unit["dup_group_id"], 0)
        cluster["member_unit_ids"].append(unit["unit_id"])
        if unit["week"] not in cluster["weeks"]:
            cluster["weeks"].append(unit["week"])
        if unit["source_type"] not in cluster["sources"]:
            cluster["sources"].append(unit["source_type"])

    unit_by_id = {u["unit_id"]: u for u in units}
    for cluster in clusters.values():
        # Medoid of the cluster = the canonical with the largest duplicate group, which
        # is the phrasing the most people actually used.
        cluster["member_unit_ids"].sort(
            key=lambda uid: -group_size.get(unit_by_id[uid]["dup_group_id"], 1)
        )
        cluster["medoid_unit_id"] = cluster["member_unit_ids"][0]
        cluster["title"] = pick_cluster_title(
            [unit_by_id[uid] for uid in cluster["member_unit_ids"]]
        )
        cluster["weeks"].sort()

    for row, position in zip(canonical_rows, assignment):
        units[row]["cluster_id"] = position
    canonical_cluster = {units[row]["unit_id"]: assignment[i] for i, row in enumerate(canonical_rows)}
    for group_id, members in enumerate(groups):
        cluster_id = canonical_cluster[units[canonicals[group_id]]["unit_id"]]
        for idx in members:
            units[idx]["cluster_id"] = cluster_id

    return {
        "schema_version": SCHEMA_VERSION,
        "embed_model": EMBED_MODEL,
        "thresholds": {
            "duplicate_threshold": duplicate_threshold,
            "cluster_distance": cluster_distance,
            "token_guard": use_token_guard,
        },
        "stats": compute_stats(units, list(clusters.values())),
        "units": units,
        "clusters": sorted(clusters.values(), key=lambda c: c["cluster_id"]),
    }


def compute_stats(units: list[dict], clusters: list[dict]) -> dict:
    by_source: dict[str, dict] = {}
    for unit in units:
        entry = by_source.setdefault(unit["source_type"], {"units": 0, "canonical": 0})
        entry["units"] += 1
        entry["canonical"] += 1 if unit.get("is_canonical") else 0

    canonical_total = sum(1 for u in units if u.get("is_canonical"))
    asserted = sum(1 for u in units if u.get("origin") == "admin")
    return {
        "unit_count": len(units),
        "canonical_count": canonical_total,
        "duplicate_count": len(units) - canonical_total,
        "duplicate_rate": round((len(units) - canonical_total) / len(units), 4) if units else 0.0,
        "cluster_count": len(clusters),
        "singleton_clusters": sum(1 for c in clusters if c["canonical_count"] == 1),
        # What a student can actually browse. Reported next to cluster_count rather than
        # replacing it: the gap between the two IS the finding — most of the bank groups
        # nothing or cannot be labelled — and hiding it behind one number buries it.
        "displayable_clusters": sum(1 for c in clusters if is_displayable_cluster(c)),
        "largest_member_count": max((c["member_count"] for c in clusters), default=0),
        "admin_authored_units": asserted,
        "by_source": by_source,
    }


# ── Threshold calibration ─────────────────────────────────────────────────────

def describe_thresholds(vectors: np.ndarray, units: list[dict],
                        sweep: Iterable[float] = (0.85, 0.88, 0.90, 0.92, 0.93, 0.95, 0.97),
                        ) -> dict[str, Any]:
    """Edge counts and group-size distributions per source type across a sweep.

    Reported PER SOURCE, never pooled: `pq` is clean parsed prose, `faq` is topic
    explainers, and `PYQ` is OCR output whose residual noise inflates similarity. One
    threshold chosen off a pooled curve would be set by whichever source has the most
    units.
    """
    report: dict[str, Any] = {}
    sources = sorted({u["source_type"] for u in units})
    for source in list(sources) + ["__pooled__"]:
        rows = [i for i, u in enumerate(units)
                if source == "__pooled__" or u["source_type"] == source]
        if len(rows) < 2:
            continue
        normalised = l2_normalise(vectors[rows])
        similarity = normalised @ normalised.T
        upper = similarity[np.triu_indices(len(rows), k=1)]
        entry = {
            "n_units": len(rows),
            "n_pairs": int(upper.size),
            "similarity": {
                "mean": round(float(upper.mean()), 4),
                "p50": round(float(np.percentile(upper, 50)), 4),
                "p90": round(float(np.percentile(upper, 90)), 4),
                "p99": round(float(np.percentile(upper, 99)), 4),
                "max": round(float(upper.max()), 4),
            },
            "sweep": [],
        }
        subset = [units[i] for i in rows]
        for threshold in sweep:
            groups, _ = build_duplicate_groups(vectors[rows], subset, threshold)
            sizes = [len(g) for g in groups]
            entry["sweep"].append({
                "threshold": threshold,
                "edges": int((upper >= threshold).sum()),
                "groups": len(groups),
                "grouped_units": sum(s for s in sizes if s > 1),
                "largest_group": max(sizes) if sizes else 0,
            })
        report[source] = entry
    return report


def describe_cluster_distances(vectors: np.ndarray, units: list[dict],
                               duplicate_threshold: float,
                               sweep: Iterable[float] = (0.12, 0.15, 0.18, 0.20, 0.25, 0.30, 0.35),
                               ) -> list[dict[str, Any]]:
    """Cluster counts and the largest cluster across a cut sweep, over canonicals.

    Needed for the same reason the duplicate sweep is: the cut has to be read off this
    corpus, not assumed. Mean pairwise cosine distance here is ~0.39, so a cut anywhere
    near it merges almost everything through chaining — the diagnostic is `largest`,
    which grows explosively one step before the cut becomes useless.
    """
    groups, canonicals = build_duplicate_groups(vectors, units, duplicate_threshold)
    canonical_vectors = vectors[canonicals] if canonicals else vectors[:0]
    rows: list[dict[str, Any]] = []
    for cut in sweep:
        assignment = average_linkage_clusters(canonical_vectors, cut)
        if not assignment:
            continue
        sizes: dict[int, int] = {}
        for cluster_id in assignment:
            sizes[cluster_id] = sizes.get(cluster_id, 0) + 1
        counts = sorted(sizes.values(), reverse=True)
        rows.append({
            "cut": cut,
            "clusters": len(counts),
            "singletons": sum(1 for c in counts if c == 1),
            "largest": counts[0] if counts else 0,
            "second": counts[1] if len(counts) > 1 else 0,
            "median": int(np.median(counts)) if counts else 0,
        })
    return rows


# ── Persistence ───────────────────────────────────────────────────────────────

def save_bank(bank: dict, vectors: np.ndarray, bank_path: Path | None = None,
              vectors_path: Path | None = None) -> None:
    """Write the bank atomically so a crashed write cannot leave a half-parsed JSON."""
    bank_path = Path(bank_path or BANK_PATH)
    vectors_path = Path(vectors_path or VECTORS_PATH)
    bank_path.parent.mkdir(parents=True, exist_ok=True)

    tmp = bank_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(bank_path)

    # Written through a handle: np.save() appends ".npy" to any path that lacks it,
    # so a "…npy.tmp" target would silently become "…npy.tmp.npy" and never be renamed.
    tmp_vectors = vectors_path.with_name(vectors_path.name + ".tmp")
    with open(tmp_vectors, "wb") as handle:
        np.save(handle, vectors.astype(np.float32))
    tmp_vectors.replace(vectors_path)


def load_bank(bank_path: Path | None = None,
              vectors_path: Path | None = None) -> tuple[dict, np.ndarray]:
    bank_path = Path(bank_path or BANK_PATH)
    vectors_path = Path(vectors_path or VECTORS_PATH)
    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    vectors = np.load(vectors_path) if vectors_path.exists() else np.zeros((0, 384), dtype=np.float32)
    return bank, vectors
