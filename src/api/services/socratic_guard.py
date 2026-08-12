"""
api/services/socratic_guard.py
The mechanical half of the Socratic no-answer policy.

Two jobs, both deliberately dumb — no LLM is consulted anywhere in this file:

  - **Input** (`sanitise_selection`): the highlighted text arrives from a web page and is
    fully attacker-controllable. Delimiter tokens and injection phrasing are stripped
    before it is ever wrapped in a prompt.
  - **Output** (`check_leak`): before anything reaches the student, generated text is
    matched against the *known* answers pulled from `question_units`. A hit is a text
    match, not an opinion, which is what makes it un-arguable-with.

**There is no redaction here, and that is the design.** An earlier version of this feature
scrubbed `### **Answer**` sections out of retrieved chunks at request time. That layer is
gone because the Socratic path no longer reads the sources that contain them — see
`SOCRATIC_SOURCE_TYPES` in `src/config.py`. A regex that has to catch every heading
variant on every request was replaced by a filter that either applied or did not.

What that change does *not* remove is the model's own knowledge. It can still derive the
answer from a lecture transcript and state it. `check_leak` is what catches that, so it
became more load-bearing when redaction went away, not less.

Kept in its own module so it is testable without a database, a vector store or a network:
`tests/test_socratic_policy.py` imports these functions directly.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Iterable, Optional

# One sanitisation rule for the whole application. These are the same patterns the quiz
# generator applies to retrieved chunks; importing them rather than re-typing them means
# a new injection pattern is added in one place and both paths get it.
from .quiz_service import _DELIMITER_RE, _INJECTION_RE, _norm


# ── Input ─────────────────────────────────────────────────────────────────────

def sanitise_selection(text: Optional[str], max_chars: int) -> str:
    """Clean a browser selection into something safe to embed in a prompt.

    Repair-then-verify rather than reject: unlike a retrieved chunk (which can simply be
    dropped — there are nine more), the selection IS the request. Dropping it would mean
    a student whose question happens to contain the word "system:" gets a blank panel.
    So the tokens are removed and the residue is capped; the prompt then labels the whole
    block as data, and the closed-set output contract (L3) is what actually contains it.
    """
    cleaned = _DELIMITER_RE.sub(" ", text or "")
    cleaned = _INJECTION_RE.sub(" ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:max_chars]


def sanitise_options(options: Optional[Iterable[str]], max_chars: int,
                     limit: int = 8) -> list[str]:
    """Same treatment for the option list, dropping anything that cleans to nothing."""
    out: list[str] = []
    for option in list(options or [])[:limit]:
        cleaned = sanitise_selection(str(option), max_chars)
        if cleaned:
            out.append(cleaned)
    return out


def selection_hash(text: Optional[str]) -> str:
    """Stable id for a selection, so repeated attacks on one question can be grouped."""
    return hashlib.sha256(_norm(text).encode("utf-8")).hexdigest()


# ── Output: the leak check ────────────────────────────────────────────────────

# "The answer is (c)", "option c", "correct answer: c" — the shapes a model reaches for
# when it decides to be helpful. Matched against normalised text, hence lowercase only.
_ANSWER_DECLARATION_RE = re.compile(
    r"(?:the\s+)?(?:correct\s+)?answer\s*(?:is|:)\s*\(?[a-e]\)?\b"
    r"|option\s*\(?[a-e]\)?\s*(?:is\s+)?(?:correct|right|the\s+answer)"
    r"|\bchoose\s+\(?[a-e]\)?\b"
    r"|\bthe\s+answer\s+is\b",
    re.IGNORECASE,
)

# A reply that is nothing but "(c)" or "c." — the format-coercion attack's payload.
_BARE_OPTION_RE = re.compile(r"^\(?([a-e])\)?[.)]?$", re.IGNORECASE)

# Numbers carry the answer for computational questions, where the letter never appears.
_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")

# Words that are numerals-in-disguise or too common to discriminate. Without this, an
# answer containing "0" or "1" would flag every sentence mentioning a unit vector.
_TRIVIAL_NUMBERS = {"0", "1", "2", "-1", "0.0", "1.0", "2.0"}

# Minimum length before an answer string is worth substring-matching. "k" or "PCA" as an
# answer would otherwise match every reply that mentions the topic at all — a false
# positive rate that would push every response onto the deterministic fallback.
_MIN_SUBSTRING_ANSWER = 12


def _numeric_tokens(text: str) -> set[str]:
    return {t for t in _NUMBER_RE.findall(text or "") if t not in _TRIVIAL_NUMBERS}


def build_denylist(answer_rows: Iterable[dict[str, Any]]) -> list[str]:
    """Flatten `question_repository.answers_for_doc_ids` rows into strings to forbid."""
    out: list[str] = []
    for row in answer_rows or []:
        for key in ("answer", "solution"):
            value = (row.get(key) or "").strip()
            if value:
                out.append(value)
    return out


def check_leak(text: Optional[str], denylist: Iterable[str]) -> Optional[dict[str, Any]]:
    """Does `text` reveal a known answer? Returns the hit, or None when clean.

    Four independent tests, cheapest first. Any one firing is a leak:

    1. **Bare option letter** — the whole reply is "(c)". Checked first because it is the
       one shape where the text is too short for anything else to catch it.
    2. **Answer declaration** — "the answer is (c)", "option b is correct".
    3. **Verbatim answer** — the stored answer appears as a substring, normalised. Gated
       on length so a one-token answer cannot match the topic name.
    4. **Numeric overlap** — every non-trivial number in the answer also appears in the
       reply. This is what catches a computed answer stated without the letter, e.g. an
       answer of "centroids at (2.5, 3.5)" restated as prose.

    Returns a dict rather than a bool so the event row records *which* rule fired; the
    policy harness reports leak rate by rule, and a rule that never fires in production
    is a rule that should be re-examined rather than trusted.
    """
    if not text:
        return None
    normalised = _norm(text)
    if not normalised:
        return None

    stripped = normalised.strip()
    match = _BARE_OPTION_RE.match(stripped)
    if match:
        return {"rule": "bare_option", "detail": stripped}

    match = _ANSWER_DECLARATION_RE.search(normalised)
    if match:
        return {"rule": "answer_declaration", "detail": match.group(0)}

    for answer in denylist or []:
        answer_norm = _norm(answer)
        if not answer_norm:
            continue

        if len(answer_norm) >= _MIN_SUBSTRING_ANSWER and answer_norm in normalised:
            return {"rule": "verbatim_answer", "detail": answer_norm[:120]}

        wanted = _numeric_tokens(answer_norm)
        if wanted and wanted <= _numeric_tokens(normalised):
            return {"rule": "numeric_overlap", "detail": ",".join(sorted(wanted))[:120]}

    return None


def check_payload(payload: dict[str, Any], denylist: Iterable[str]) -> Optional[dict[str, Any]]:
    """Run `check_leak` over every string a response envelope carries.

    Walks nested dicts and lists rather than checking known keys, so a field added to the
    envelope later is covered by default instead of silently bypassing the guard.
    """
    def walk(node: Any, path: str) -> Optional[dict[str, Any]]:
        if isinstance(node, str):
            hit = check_leak(node, denylist)
            if hit:
                return {**hit, "field": path}
            return None
        if isinstance(node, dict):
            for key, value in node.items():
                hit = walk(value, f"{path}.{key}" if path else str(key))
                if hit:
                    return hit
            return None
        if isinstance(node, list):
            for i, value in enumerate(node):
                hit = walk(value, f"{path}[{i}]")
                if hit:
                    return hit
            return None
        return None

    return walk(payload, "")
