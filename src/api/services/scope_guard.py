"""
api/services/scope_guard.py
The out-of-syllabus check on /chat, decided by measurement rather than by instruction.

`rag_pipeline.build_prompt` has always carried an OUT-OF-SCOPE RULE. It is a sentence in a
prompt, and a sentence in a prompt is the thing a jailbreak is for; when it loses, the
model's contract is a six-section answer with a Worked Example. This module answers the
same question with two numbers, before any LLM is reachable:

  topic_score   max cosine between the question and the 48 taxonomy topic vectors.
  corpus_score  cosine between the question and the nearest chunk in the collection.

**Three-way, and only the confident end refuses.** `in_scope` and `uncertain` both go on to
generate — the difference between them is only what gets reported. That asymmetry is the
whole safety argument: a mis-set floor costs the behaviour that existed before this module,
never a refused student. Detection rate and false-positive rate are therefore separate
metrics in `src/evaluate_scope_guard.py`, because tightening one loosens the other.

**Fail open, always** — the same rule `rerank_service` states. No vector store, an
unreachable Qdrant, an empty taxonomy, a raising probe: all `uncertain`. This module must
never be the reason a chat request fails.

`embed`, `nearest_topic` and `probe` arrive as callables rather than being constructed
here, matching how `rerank` is injected into `answer_question`. That keeps the policy
testable with three lambdas — `tests/test_scope_guard.py` reaches no network, no database
and no model — and keeps this file free of any import that would build a vector store or
load an embedding model. `rag_service` holds the real implementations.

No LLM is consulted anywhere in this file.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Optional

try:
    from src.config import (
        SCOPE_CORPUS_FLOOR, SCOPE_CORPUS_HARD_FLOOR, SCOPE_GUARD_ENABLED,
        SCOPE_MAX_QUESTION_CHARS, SCOPE_TOPIC_FLOOR, SCOPE_TOPIC_HARD_FLOOR,
    )
except ModuleNotFoundError:  # same import shim the rest of this package uses
    from config import (  # type: ignore
        SCOPE_CORPUS_FLOOR, SCOPE_CORPUS_HARD_FLOOR, SCOPE_GUARD_ENABLED,
        SCOPE_MAX_QUESTION_CHARS, SCOPE_TOPIC_FLOOR, SCOPE_TOPIC_HARD_FLOOR,
    )

IN_SCOPE = "in_scope"
UNCERTAIN = "uncertain"
OUT_OF_SCOPE = "out_of_scope"

# Types the injected callables must satisfy.
#   Embed:        text            -> a unit-length query vector (or None if unavailable)
#   NearestTopic: query vector    -> (topic name or None, cosine) for the closest taxonomy entry
#   Probe:        query vector, k -> cosine of the k nearest chunks, best first
Embed = Callable[[str], Any]
NearestTopic = Callable[[Any], tuple[Optional[str], float]]
Probe = Callable[[Any, int], list[float]]

_WS_RE = re.compile(r"\s+")


def _clean(question: Optional[str]) -> str:
    """Flatten and cap the question before it is embedded.

    Capping is not cosmetic. A short question embeds to roughly where its subject lives; a
    question with three pages of unrelated padding stapled to it embeds to wherever the
    padding is, which is precisely how a scope check gets talked around.
    """
    return _WS_RE.sub(" ", (question or "").strip())[:SCOPE_MAX_QUESTION_CHARS]


def _verdict(verdict: str, reason: str, topic_score: Optional[float] = None,
             corpus_score: Optional[float] = None,
             top_topic: Optional[str] = None) -> dict[str, Any]:
    """`corpus_score: None` means *not measured* — either the probe was skipped as
    unnecessary or nothing was scored at all. It is never rounded to 0.0, which would read
    as "no corpus support whatsoever" and is the opposite of what a skip means."""
    return {
        "verdict": verdict,
        "reason": reason,
        "topic_score": None if topic_score is None else round(float(topic_score), 4),
        "corpus_score": None if corpus_score is None else round(float(corpus_score), 4),
        "top_topic": top_topic,
    }


def score_question(question: str, embed: Embed, nearest_topic: NearestTopic,
                   probe: Probe, probe_k: int,
                   skip_probe_above: Optional[float] = None,
                   ) -> tuple[float, Optional[float], Optional[str]]:
    """`(topic_score, corpus_score, top_topic_name)` for one question.

    One `embed` call feeds both signals — it is the only local cost, and embedding the same
    question twice to score it two ways would double it.

    `skip_probe_above` short-circuits the Qdrant round trip. The taxonomy signal is a
    matrix multiply against 48 resident vectors and costs microseconds; the corpus probe is
    a network call to Qdrant Cloud and costs most of the guard's wall time. When the topic
    score alone already clears the in-scope floor, no corpus score can change the verdict,
    so the call is not made and `corpus_score` comes back **None** — "not probed", which is
    not the same as "scored zero" and must not be rendered as one. Pass None to always
    probe, which is what the evaluation harness does: it needs both scores for every query
    regardless of what the verdict would have been.

    Raises whatever the callables raise. `classify` is what turns a failure into
    `uncertain`; keeping this one honest means the harness can tell "scored low" from
    "could not be scored".
    """
    vector = embed(question)
    if vector is None:
        raise RuntimeError("no query embedding available")

    topic_name, topic_score = nearest_topic(vector)
    topic_score = float(topic_score)

    if skip_probe_above is not None and topic_score >= skip_probe_above:
        return topic_score, None, topic_name

    scores = probe(vector, probe_k) or []
    return topic_score, max((float(s) for s in scores), default=0.0), topic_name


def classify(question: str, embed: Embed, nearest_topic: NearestTopic, probe: Probe,
             probe_k: int) -> dict[str, Any]:
    """Decide whether `question` is about this course. Never raises.

    Returns `{verdict, reason, topic_score, corpus_score, top_topic}` where `verdict` is
    one of `in_scope` / `uncertain` / `out_of_scope`. Only `out_of_scope` is a refusal;
    the caller treats the other two identically.
    """
    if not SCOPE_GUARD_ENABLED:
        return _verdict(UNCERTAIN, "scope guard disabled")

    cleaned = _clean(question)
    if not cleaned:
        return _verdict(UNCERTAIN, "empty question")

    try:
        topic_score, probed, top_topic = score_question(
            cleaned, embed, nearest_topic, probe, probe_k,
            skip_probe_above=SCOPE_TOPIC_FLOOR)
    except Exception as exc:  # noqa: BLE001
        # Fail open. A guard that 500s the chat endpoint when Qdrant hiccups is worse than
        # the prompt-only behaviour it replaced.
        print(f"  [Scope] Not scored, passing through — {type(exc).__name__}: {exc}", flush=True)
        return _verdict(UNCERTAIN, f"not scored ({type(exc).__name__})")

    if probed is None:
        # The probe was skipped because the taxonomy score already settled it. Say so,
        # rather than reporting a corpus score of 0.0 that was never measured.
        return _verdict(IN_SCOPE, "clears the taxonomy floor; corpus not probed",
                        topic_score, None, top_topic)
    corpus_score = probed

    # The soft floors decide the reported LABEL and nothing else — a question over either
    # of them is confidently in scope. Whether anything is refused is settled entirely by
    # the two hard floors below, so raising these cannot turn a student away.
    if topic_score >= SCOPE_TOPIC_FLOOR or corpus_score >= SCOPE_CORPUS_FLOOR:
        return _verdict(IN_SCOPE, "clears a relevance floor",
                        topic_score, corpus_score, top_topic)

    # `and`, not `or`. The two signals fail in different directions: a question phrased in
    # nothing like taxonomy language scores low on topic and high on corpus, and one about
    # a thinly-covered topic does the reverse. Either floor acting alone would refuse a
    # real question; requiring both is what keeps the false-positive rate at zero.
    if topic_score < SCOPE_TOPIC_HARD_FLOOR and corpus_score < SCOPE_CORPUS_HARD_FLOOR:
        return _verdict(OUT_OF_SCOPE, "no taxonomy or corpus support",
                        topic_score, corpus_score, top_topic)

    return _verdict(UNCERTAIN, "weak but present support",
                    topic_score, corpus_score, top_topic)


def is_refusal(scope: Optional[dict[str, Any]]) -> bool:
    """One place that decides what a refusal looks like, so no call site re-spells it."""
    return bool(scope) and scope.get("verdict") == OUT_OF_SCOPE
