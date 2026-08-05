"""
llm_judge.py
Shared LLM-as-a-Judge machinery (Milestone 4).

One judge, three callers:
  - `api/services/quiz_service.judge_short_answer` — grades a student's free-text answer live.
  - `evaluate_quiz.run_judge`                      — audits generated quiz questions.
  - `evaluate_rag.run_llm_judge`                   — scores RAG generation quality.

Each caller brings its own rubric prompt and decides what to do with the result. Everything
else — which model judges, in what order, what happens when one fails, and how a JSON score
object is pulled out of the reply — lives here, so there is exactly one grading system to
reason about.

**Independence is the point.** A model grading its own output scores itself generously, so the
candidate ladder is ordered by decreasing independence: another provider first, then another
model on the generator's own provider, and — only if nothing else answers — the generator's own
model. Callers can read `session.independence` and say which rung they ended up on rather than
claiming an independence they did not have.

This module is deliberately **print-free**: it is imported by the API, where stdout chatter per
graded answer is noise. `invoke_judge` reports failures through the optional `on_fallback`
callback; the evaluation scripts pass a printer, the API does not.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional

try:
    from src.rag_pipeline import (
        _build_provider_queue, _classify_error, create_llm, extract_text_from_response,
    )
except ModuleNotFoundError as _exc:  # pragma: no cover - import shim
    # Only fall back when `src` itself is not on the path (a script run from inside src/).
    # A missing third-party dependency also raises ModuleNotFoundError, and retrying the
    # import would report it as "No module named 'rag_pipeline'" — hiding the real cause.
    if _exc.name not in ("src", "src.rag_pipeline"):
        raise
    from rag_pipeline import (  # type: ignore[no-redef]
        _build_provider_queue, _classify_error, create_llm, extract_text_from_response,
    )


CROSS_PROVIDER = "cross-provider"
CROSS_MODEL = "cross-model (same provider)"
NO_INDEPENDENCE = "none (same model as the generator)"

# Non-greedy: judges are asked for a flat score object, and a greedy match would swallow
# trailing prose on a chatty reply.
_JSON_RE = re.compile(r"\{.*?\}", re.DOTALL)


class NoJudgeAvailableError(RuntimeError):
    """No LLM API keys are configured, so no judge can be constructed at all."""


@dataclass(frozen=True)
class JudgeCandidate:
    """One rung of the ladder: a specific model, on a specific key, at a known independence."""

    provider: str
    model: str
    api_key: str
    independence: str

    @property
    def label(self) -> str:
        return f"{self.provider}/{self.model}"


@dataclass
class JudgeSession:
    """A cursor over the candidate ladder for **one** judging call.

    Mutable by design — `advance()` burns the current candidate. Never share a session
    across calls: a transient failure would permanently demote every later grade. Get a
    fresh one from `new_session()` each time.
    """

    candidates: list[JudgeCandidate]
    cursor: int = 0

    @property
    def current(self) -> JudgeCandidate:
        return self.candidates[self.cursor]

    @property
    def label(self) -> str:
        return self.current.label

    @property
    def independence(self) -> str:
        return self.current.independence

    def advance(self) -> bool:
        """Step down to the next candidate. False once the ladder is exhausted."""
        self.cursor += 1
        return self.cursor < len(self.candidates)


# ── Candidate ladder ──────────────────────────────────────────────────────────

# Built once per process: the ladder depends only on the environment's key pools, and
# rebuilding it per graded answer would re-scan the whole key namespace. The *list* is
# cached, never a session — see JudgeSession.
_CANDIDATE_CACHE: dict[bool, list[JudgeCandidate]] = {}

# (provider, model) pairs that failed for a reason that cannot fix itself: a rejected key,
# or a model the provider has retired. Without this, a misconfigured deployment pays for
# every dead rung on *every* graded answer — measured at five wasted round-trips per grade
# with an invalid Gemini key and the two decommissioned Groq models still in GROQ_MODELS.
# Rate limits and transient errors are deliberately NOT recorded here; those come back.
_DEAD_CANDIDATES: set[tuple[str, str]] = set()

# Substrings that mean "this model is gone", which _classify_error files under 'other'
# because it is a request-shaped 400 rather than an auth failure.
_RETIRED_MODEL_MARKERS = ("decommission", "model_not_found", "does not exist",
                          "is not found", "no longer supported", "has been deprecated")


def _is_permanent_failure(exc: Exception) -> bool:
    """Will retrying this candidate later plausibly succeed? Permanent failures are pruned."""
    if _classify_error(exc) == "auth":
        return True
    text = str(exc).lower()
    return any(marker in text for marker in _RETIRED_MODEL_MARKERS)


def generator_identity() -> tuple[str, str]:
    """The (provider, model) that `generate_llm_response` would actually use.

    This is the thing a judge is trying to be independent of: the head of the provider
    queue, which is what the failover loop reaches for first.
    """
    queue = _build_provider_queue()
    if not queue:
        raise NoJudgeAvailableError("No LLM API keys configured — cannot identify a generator.")
    provider, models, _ = queue[0]
    return provider, models[0]


def build_candidates(prefer_independence: bool = True) -> list[JudgeCandidate]:
    """Every reachable (provider, model, key), ordered by decreasing independence.

    With `prefer_independence=False` the generator's own model leads instead — faster in
    the common case, but it is self-grading, and the caller should say so.
    """
    queue = _build_provider_queue()
    if not queue:
        raise NoJudgeAvailableError("No LLM API keys configured — cannot run the judge.")

    gen_provider, gen_models, gen_keys = queue[0]
    gen_model = gen_models[0]
    generator = JudgeCandidate(gen_provider, gen_model, gen_keys[0], NO_INDEPENDENCE)

    others: list[JudgeCandidate] = []
    for provider, models, keys in queue:
        if not keys:
            continue
        for model in models:
            if provider == gen_provider and model == gen_model:
                continue
            others.append(JudgeCandidate(
                provider=provider,
                model=model,
                api_key=keys[0],
                independence=CROSS_PROVIDER if provider != gen_provider else CROSS_MODEL,
            ))

    # Sort by independence, not by the provider queue's order. The queue leads with the
    # *generator's* provider, so walking it directly would try the generator's siblings
    # before reaching another provider — the opposite of what independence asks for, and
    # the reason the ladder previously opened with two decommissioned Groq models.
    # `sorted` is stable, so preference order within a provider is preserved.
    others.sort(key=lambda c: 0 if c.independence == CROSS_PROVIDER else 1)

    # The generator's own model is always kept as the last rung: a degraded grade that
    # declares itself degraded beats refusing to grade at all.
    return [*others, generator] if prefer_independence else [generator, *others]


def new_session(prefer_independence: bool = True) -> JudgeSession:
    """A fresh cursor over the (cached) candidate ladder, minus anything known to be dead.

    Fresh every call on purpose: a candidate that hit a rate limit once must be tried again
    next time, or one bad minute would silently demote every later grade in the process.
    Only permanent failures are remembered, and the last rung always survives the filter so
    the ladder can never be pruned to nothing.
    """
    candidates = _CANDIDATE_CACHE.get(prefer_independence)
    if candidates is None:
        candidates = build_candidates(prefer_independence)
        _CANDIDATE_CACHE[prefer_independence] = candidates

    live = [c for c in candidates if (c.provider, c.model) not in _DEAD_CANDIDATES]
    return JudgeSession(candidates=live or [candidates[-1]])


def reset_candidate_cache() -> None:
    """Drop the cached ladder and the dead list — for tests, or after keys change."""
    _CANDIDATE_CACHE.clear()
    _DEAD_CANDIDATES.clear()


# ── Invocation ────────────────────────────────────────────────────────────────

def invoke_judge(
    session: JudgeSession,
    prompt: str,
    temperature: float = 0.0,
    on_fallback: Optional[Callable[[JudgeCandidate, Exception], None]] = None,
) -> tuple[Optional[dict[str, Any]], str]:
    """Run one rubric prompt through the ladder.

    Returns `(parsed_json_object, label)`. The **raw parsed object** is returned rather than
    a score dict because callers need more than numbers out of it — the short-answer grader
    also reads a `feedback` string. Use `clamp_scores` for the numeric part.

    `(None, label)` means the judge could not produce a usable verdict: every candidate
    raised, or the last reply carried no parseable JSON object. Callers must treat that as
    "ungraded", never as a zero — a fabricated score corrupts the mastery model silently.
    """
    text = ""
    while True:
        candidate = session.current
        try:
            llm = create_llm(
                model_name=candidate.model,
                provider=candidate.provider,
                api_key=candidate.api_key,
                temperature=temperature,
            )
            text = extract_text_from_response(llm.invoke(prompt))
            break
        except Exception as exc:  # noqa: BLE001 — any provider failure steps down the ladder
            if _is_permanent_failure(exc):
                _DEAD_CANDIDATES.add((candidate.provider, candidate.model))
            if on_fallback:
                on_fallback(candidate, exc)
            if not session.advance():
                return None, candidate.label

    label = session.label
    match = _JSON_RE.search(text.replace("\n", " "))
    if not match:
        return None, label
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None, label
    if not isinstance(parsed, dict):
        return None, label
    return parsed, label


def clamp_scores(parsed: Optional[dict[str, Any]], keys: Iterable[str]) -> dict[str, float]:
    """Pull the requested keys out of a judge reply as floats in [0, 1].

    A missing or non-numeric key becomes 0.0. That default is only safe because the caller
    has already established the judge *replied* — `invoke_judge` returning None is the
    "could not grade" signal, and this function is not a substitute for checking it.
    """
    out: dict[str, float] = {}
    for key in keys:
        try:
            out[key] = min(1.0, max(0.0, float((parsed or {}).get(key, 0.0))))
        except (TypeError, ValueError):
            out[key] = 0.0
    return out
