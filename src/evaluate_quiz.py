"""Personalized Quiz Evaluation (Milestone 1, Objective 6 — §3.5 targets).

Reports two things the milestone asks for, and is explicit about what each one can and
cannot support:

  1. Relevance to identified weak areas (target ≥ 80%).
     Asking "did we quiz a gap topic" is circular — the generator selects from the gap
     list, so it is 100% by construction. The honest question is whether the *question*
     genuinely tests the named topic and is answerable from the chunks it cites, so that
     is what the judge scores.

  2. Pre/post revision improvement (target ≥ 15%).
     Adaptive difficulty makes post-intervention questions harder by construction, so a
     naked accuracy delta would measure the ladder rather than the learning. Reported as
     difficulty-controlled accuracy (medium items only) plus a mastery delta.

Run from the repo root:
    python src/evaluate_quiz.py --count 30
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from sqlalchemy.orm import Session

from src.api.dependencies import get_retriever
from src.api.services import quiz_service
from src.api.services.recommendation_service import find_topic, load_taxonomy
from src.database import crud
from src.database.models import QuizAttempt, TopicRecommendationEvent
from src.database.session import Base, SessionLocal, engine
from src.rag_pipeline import (
    _build_provider_queue, create_llm, extract_text_from_response,
)

load_dotenv()

EVAL_STUDENT = "eval_quiz_bot"
DIFFICULTY_CYCLE = ("easy", "medium", "hard")
MIN_ATTEMPTS_PER_SIDE = 3
RELEVANCE_THRESHOLD = 0.8


# ── Judge selection ───────────────────────────────────────────────────────────

def select_judge() -> dict:
    """Pin the judge as far from the generator as the configuration allows.

    Candidates are ordered by decreasing independence: another provider first, then
    another model on the generator's own provider, and — only if nothing else answers —
    the generator's own model. The harness runs either way; the report always states
    which rung it ended up on, so a reader never assumes independence it did not have.
    """
    queue = _build_provider_queue()
    if not queue:
        raise RuntimeError("No LLM API keys configured — cannot run the judge.")

    gen_provider, gen_models, _ = queue[0]
    gen_model = gen_models[0]

    candidates: list[dict[str, str]] = []
    for provider, models, keys in queue:
        if not keys:
            continue
        for model in models:
            if provider == gen_provider and model == gen_model:
                continue
            candidates.append({
                "judge_provider": provider,
                "judge_model": model,
                "judge_key": keys[0],
                "independence": ("cross-provider" if provider != gen_provider
                                 else "cross-model (same provider)"),
            })
    candidates.append({
        "judge_provider": gen_provider,
        "judge_model": gen_model,
        "judge_key": queue[0][2][0],
        "independence": "none (same model as the generator)",
    })

    judge = {
        "generator_provider": gen_provider,
        "generator_model": gen_model,
        "candidates": candidates,
        "cursor": 0,
        **candidates[0],
    }
    return judge


def _advance_judge(judge: dict) -> bool:
    """Step down to the next candidate after a failure. False when exhausted."""
    judge["cursor"] += 1
    if judge["cursor"] >= len(judge["candidates"]):
        return False
    judge.update(judge["candidates"][judge["cursor"]])
    print(f"[Judge] Falling back to {judge['judge_provider']}/{judge['judge_model']} "
          f"(independence: {judge['independence']}).")
    return True


def run_judge(judge: dict, question: dict, context: str) -> dict[str, float]:
    """Score one generated question, stepping down the candidate list on failure."""
    options_block = "\n".join(f"  - {o}" for o in question["options"])
    prompt = f"""You are auditing questions generated for an IIT Madras BS MLT course quiz.

Named topic: {question['topic_name']} (Week {question['week']})
Question: {question['question_text']}
Options:
{options_block}
Marked-correct option: {question['correct_answer']}

Course material the question cites:
<context>
{context}
</context>

Score each criterion from 0.0 to 1.0:
1. tests_topic: does the question actually test the named topic (not an adjacent or
   generic one)?
2. answerable_from_context: could a student answer it from the cited material alone,
   without outside knowledge?
3. exactly_one_correct: is the marked option correct AND the only correct option?
4. distractors_plausible: are the wrong options specific and tempting, rather than
   absurd or obviously off-topic?

Return ONLY a JSON object:
{{"tests_topic": 0.0, "answerable_from_context": 0.0, "exactly_one_correct": 0.0, "distractors_plausible": 0.0}}"""

    text = ""
    while True:
        try:
            llm = create_llm(
                model_name=judge["judge_model"],
                provider=judge["judge_provider"],
                api_key=judge["judge_key"],
                temperature=0.0,
            )
            text = extract_text_from_response(llm.invoke(prompt))
            break
        except Exception as exc:  # noqa: BLE001
            print(f"  [Judge] FAILED {judge['judge_provider']}/{judge['judge_model']} "
                  f"({type(exc).__name__}: {str(exc)[:110]})")
            if not _advance_judge(judge):
                return {}

    match = re.search(r"\{.*?\}", text.replace("\n", " "), re.DOTALL)
    if not match:
        return {}
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}

    out: dict[str, float] = {}
    for key in ("tests_topic", "answerable_from_context", "exactly_one_correct",
                "distractors_plausible"):
        try:
            out[key] = min(1.0, max(0.0, float(parsed.get(key, 0.0))))
        except (TypeError, ValueError):
            out[key] = 0.0
    return out


# ── Sampling ──────────────────────────────────────────────────────────────────

def sample_questions(db: Session, retriever, count: int, student_id: str) -> list[dict]:
    """Generate a spread of questions across topics and difficulties."""
    taxonomy = load_taxonomy()
    crud.get_or_create_student(db, student_id)

    step = max(1, len(taxonomy) // max(1, count))
    picks = [taxonomy[i] for i in range(0, len(taxonomy), step)][:count]

    sampled: list[dict] = []
    for i, topic in enumerate(picks):
        difficulty = DIFFICULTY_CYCLE[i % len(DIFFICULTY_CYCLE)]
        print(f"[{i + 1}/{len(picks)}] {topic['name']} ({difficulty})...")
        try:
            generated = quiz_service.generate_quiz(
                db, student_id, retriever,
                topic_id=topic["id"], difficulty=difficulty, count=1,
            )
        except quiz_service.QuizGenerationError as exc:
            print(f"    skipped: {exc}")
            continue

        for item in generated:
            row = crud.get_quiz_attempt(db, item["attempt_id"])
            if row is None or row.reason == "cached":
                # Re-serves are real questions but not evidence about generation quality.
                continue
            sampled.append({
                "attempt_id": row.attempt_id,
                "topic_id": row.topic_id,
                "topic_name": row.topic_name,
                "week": item["week"],
                "difficulty": row.difficulty,
                "question_text": row.question_text,
                "options": list(row.options or []),
                "correct_answer": row.correct_answer,
                "source_chunks": list(row.source_chunks or []),
            })
    return sampled


def fetch_context(retriever, question: dict) -> tuple[str, list[str]]:
    """Recover the text of the chunks a question cites.

    Looking the payload up by doc_id needs a keyword index the live collection does not
    have, so the cited chunks are recovered by re-running the retrieval they came from —
    the query is deterministic, so the same doc_ids come back.

    Returns (context_text, source_types_of_cited_chunks). The second value is what the
    exam-grounding check reads; it is empty when the chunks could not be recovered.
    """
    cited = list(question.get("source_chunks") or [])
    topic = find_topic(question["topic_id"]) if question.get("topic_id") else None
    if topic:
        target = {
            "topic_name": topic["name"],
            "description": topic.get("description", ""),
            "aliases": topic.get("aliases", []),
            "week": topic.get("week", 0),
        }
        try:
            chunks = quiz_service.select_chunks_for_topic(retriever, target, question["difficulty"])
        except quiz_service.QuizGenerationError:
            chunks = []
        by_id = {c["doc_id"]: c for c in chunks}
        blocks = [f'[{doc_id}]\n{by_id[doc_id]["text"]}' for doc_id in cited if doc_id in by_id]
        if blocks:
            types = [by_id[doc_id]["source_type"] for doc_id in cited if doc_id in by_id]
            return "\n\n".join(blocks), types

    direct = quiz_service._fetch_chunks_by_doc_id(retriever, cited)
    return ("\n\n".join(f'[{c["doc_id"]}]\n{c["text"]}' for c in direct),
            [c["source_type"] for c in direct])


# ── Structural checks (no judge needed) ───────────────────────────────────────

def structural_checks(sampled: list[dict]) -> dict:
    """Cheap checks the judge cannot fake, including the position-bias regression test.

    The old placeholder generator always put the correct answer at index 0. This
    distribution is only computable because the served options are persisted.
    """
    positions = Counter()
    grounded = 0
    four_distinct = 0
    exam_grounded = 0
    types_known = 0
    for q in sampled:
        if q["source_chunks"]:
            grounded += 1
        options = q["options"]
        if len(options) == 4 and len({o.strip().lower() for o in options}) == 4:
            four_distinct += 1
        try:
            positions[options.index(q["correct_answer"])] += 1
        except ValueError:
            positions["missing"] += 1

        # Did the question cite the course's own assessment material? Retrieval ranks
        # pq/PYQ chunks first, so this is the direct measure of whether that landed.
        cited_types = q.get("cited_source_types") or []
        if cited_types:
            types_known += 1
            if any(t in quiz_service._EXAM_SOURCE_RANK for t in cited_types):
                exam_grounded += 1

    total = max(1, len(sampled))
    return {
        "n": len(sampled),
        "grounded_pct": round(grounded / total * 100, 1),
        "well_formed_pct": round(four_distinct / total * 100, 1),
        "exam_grounded_pct": (round(exam_grounded / types_known * 100, 1) if types_known else None),
        "exam_grounded_n": exam_grounded,
        "source_types_known": types_known,
        "position_distribution": {
            str(k): round(v / total * 100, 1) for k, v in sorted(positions.items(), key=str)
        },
    }


# ── Pre/post improvement ──────────────────────────────────────────────────────

def _replay_elo(attempts: list[QuizAttempt]) -> float:
    """Replay the Elo update over an ordered attempt list.

    Mastery history is not stored, so 'mastery before the intervention' is reconstructed
    by replaying the same arithmetic crud.update_topic_mastery_elo applies, including the
    item-difficulty offset.
    """
    elo = 0.0
    for i, a in enumerate(attempts):
        k = max(16.0, 64.0 / (1.0 + 0.1 * i))
        d = crud._DIFFICULTY_OFFSET.get((a.difficulty or "medium").lower(), 0.0)
        expected = 1.0 / (1.0 + math.pow(10.0, -(elo - d) / 400.0))
        actual = a.llm_score if a.llm_score is not None else (1.0 if a.is_correct else 0.0)
        elo += k * (min(1.0, max(0.0, actual)) - expected)
    return elo


def _mastery(elo: float) -> float:
    return 1.0 / (1.0 + math.pow(10.0, -elo / 400.0))


def prepost_analysis(db: Session) -> dict:
    """Split each (student, topic) on the first time the topic was recommended."""
    events = db.query(TopicRecommendationEvent).all()
    pre_medium: list[bool] = []
    post_medium: list[bool] = []
    mastery_deltas: list[float] = []
    pairs = 0

    for ev in events:
        attempts = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.student_id == ev.student_id,
                    QuizAttempt.topic_id == ev.topic_id,
                    QuizAttempt.is_correct.isnot(None))
            .order_by(QuizAttempt.attempt_time.asc())
            .all()
        )
        cutoff = ev.first_recommended_at
        if cutoff is not None and cutoff.tzinfo is not None:
            cutoff = cutoff.replace(tzinfo=None)

        before = [a for a in attempts if a.attempt_time and a.attempt_time < cutoff]
        after = [a for a in attempts if a.attempt_time and a.attempt_time >= cutoff]
        if len(before) < MIN_ATTEMPTS_PER_SIDE or len(after) < MIN_ATTEMPTS_PER_SIDE:
            continue

        pairs += 1
        pre_medium += [bool(a.is_correct) for a in before if (a.difficulty or "") == "medium"]
        post_medium += [bool(a.is_correct) for a in after if (a.difficulty or "") == "medium"]
        mastery_deltas.append(_mastery(_replay_elo(attempts)) - _mastery(_replay_elo(before)))

    def pct(values: list[bool]) -> float | None:
        return round(sum(values) / len(values) * 100, 1) if values else None

    pre, post = pct(pre_medium), pct(post_medium)
    return {
        "pairs": pairs,
        "pre_medium_accuracy_pct": pre,
        "post_medium_accuracy_pct": post,
        "medium_accuracy_delta_pct": (round(post - pre, 1) if pre is not None and post is not None else None),
        "pre_medium_n": len(pre_medium),
        "post_medium_n": len(post_medium),
        "mean_mastery_delta_pct": (
            round(sum(mastery_deltas) / len(mastery_deltas) * 100, 1) if mastery_deltas else None
        ),
    }


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(judge: dict, sampled: list[dict], scores: list[dict],
                 structural: dict, prepost: dict, judged_rows: list[tuple[dict, dict]]) -> str:
    def avg(key: str) -> float:
        values = [s[key] for s in scores if key in s]
        return sum(values) / len(values) if values else 0.0

    relevant = [s for s in scores if s.get("tests_topic", 0.0) >= RELEVANCE_THRESHOLD]
    relevance_pct = round(len(relevant) / max(1, len(scores)) * 100, 1)

    lines = [
        "# Personalized Quiz Evaluation (Milestone 1, Objective 6)",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Judge configuration",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| generator_provider (nominal) | `{judge['generator_provider']}` |",
        f"| generator_model (nominal) | `{judge['generator_model']}` |",
        f"| judge_provider | `{judge['judge_provider']}` |",
        f"| judge_model | `{judge['judge_model']}` |",
        f"| independence | **{judge['independence']}** |",
        "",
        "The generator fields are the *first choice* in the failover queue; a rate limit or",
        "auth failure during generation can rotate the actual provider, which the row does not",
        "record. Read the independence field as an upper bound.",
        "",
        "## 1. Relevance to identified weak areas (§3.5 target ≥ 80%)",
        "",
        f"**Relevance: {relevance_pct}%** — share of sampled questions the judge scored ≥ "
        f"{RELEVANCE_THRESHOLD:.1f} on *does this actually test the named topic*.",
        "",
        "Measuring 'did we quiz a gap topic' would be circular: targeting reads the gap list,",
        "so that number is 100% by construction. This measures question quality instead.",
        "",
    ]

    if judge["independence"].startswith("none"):
        lines += [
            "> **Read this number with care.** No independent judge was reachable, so the model",
            "> that wrote these questions also graded them. A model marking its own work is",
            "> biased upward and the scores below are an upper bound, not a measurement. Restore",
            "> a working second provider (or a second model on the same provider) and re-run",
            "> before quoting this figure.",
            "",
        ]

    lines += [
        "| Criterion | Mean (0-1) |",
        "|---|---:|",
        f"| tests_topic | {avg('tests_topic'):.2f} |",
        f"| answerable_from_context | {avg('answerable_from_context'):.2f} |",
        f"| exactly_one_correct | {avg('exactly_one_correct'):.2f} |",
        f"| distractors_plausible | {avg('distractors_plausible'):.2f} |",
        f"| questions judged | {len(scores)} of {len(sampled)} sampled |",
        "",
        "## 2. Structural checks (no judge involved)",
        "",
        "| Check | Value |",
        "|---|---:|",
        f"| questions with non-empty `source_chunks` | {structural['grounded_pct']}% |",
        f"| questions with 4 distinct options | {structural['well_formed_pct']}% |",
        (f"| questions citing the course's own exam material (`pq`/`PYQ`) | "
         f"{structural['exam_grounded_pct']}% "
         f"({structural['exam_grounded_n']} of {structural['source_types_known']} resolvable) |"
         if structural["exam_grounded_pct"] is not None else
         "| questions citing the course's own exam material (`pq`/`PYQ`) | _not resolvable_ |"),
        "",
        "Retrieval ranks `pq` (practice sets) then `PYQ` (past papers) ahead of explanatory sources,",
        "and the prompt labels them `source=\"past_exam\"` with an instruction to match their style",
        "without reproducing them. The last row is whether that actually reached the generator.",
        "",
        "**Correct-option position distribution** (expect ~25% per slot — this is the direct",
        "regression test against the old placeholder generator, whose answer was always A):",
        "",
        "| Slot | Share |",
        "|---|---:|",
    ]
    for slot, share in structural["position_distribution"].items():
        label = {"0": "A", "1": "B", "2": "C", "3": "D"}.get(slot, slot)
        lines.append(f"| {label} | {share}% |")

    lines += [
        "",
        "## 3. Pre/post revision improvement (§3.5 target ≥ 15%)",
        "",
        "Split point: the first time a topic entered the student's study plan",
        "(`topic_recommendation_events`). Adaptive difficulty makes later questions harder by",
        "construction, so the primary number holds item difficulty constant and the secondary",
        "number is difficulty-aware by design.",
        "",
    ]

    if prepost["pairs"] == 0:
        lines += [
            f"**Insufficient data.** No (student, topic) pair yet has ≥ {MIN_ATTEMPTS_PER_SIDE} "
            "graded attempts on both sides of its first recommendation. This metric only becomes "
            "meaningful after real usage — run a seeded demo session before reporting it.",
            "",
        ]
    else:
        lines += [
            "| Measure | Before | After | Delta |",
            "|---|---:|---:|---:|",
            f"| Primary — accuracy on `medium` items only | "
            f"{prepost['pre_medium_accuracy_pct']}% (n={prepost['pre_medium_n']}) | "
            f"{prepost['post_medium_accuracy_pct']}% (n={prepost['post_medium_n']}) | "
            f"{prepost['medium_accuracy_delta_pct']} pts |",
            f"| Secondary — mastery delta (Elo replay) | — | — | "
            f"{prepost['mean_mastery_delta_pct']} pts |",
            "",
            f"Based on {prepost['pairs']} (student, topic) pair(s) with at least "
            f"{MIN_ATTEMPTS_PER_SIDE} graded attempts on each side.",
            "",
        ]

    lines += [
        "## 4. Stated limitation — gap-detection precision is not reported",
        "",
        "§3.5 also asks for Knowledge Gap Detection Precision ≥ 80% 'validated against actual",
        "quiz performance'. Under gap-only targeting that measurement is circular: every question",
        "is drawn from a flagged topic, so quiz performance can never contradict the flag. Testing",
        "it honestly needs control questions on topics the engine did *not* flag, which is a",
        "targeting-policy change rather than a reporting change. It is deliberately left",
        "unreported rather than reported as a number that cannot fail.",
        "",
        "## 5. Sampled questions",
        "",
    ]

    for q, score in judged_rows:
        lines += [
            f"### {q['topic_name']} — Week {q['week']} — `{q['difficulty']}`",
            "",
            f"> {q['question_text']}",
            "",
        ]
        for i, opt in enumerate(q["options"]):
            marker = " **(marked correct)**" if opt == q["correct_answer"] else ""
            lines.append(f"{'ABCD'[i] if i < 4 else i}. {opt}{marker}")
        lines += [
            "",
            f"Sources: {', '.join(f'`{s}`' for s in q['source_chunks']) or '_none_'}",
            "",
            "Judge: " + (", ".join(f"{k}={v:.2f}" for k, v in score.items()) if score else "_not scored_"),
            "",
            "---",
            "",
        ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate personalized quiz generation.")
    parser.add_argument("--count", type=int, default=30, help="questions to sample")
    parser.add_argument("--student", default=None,
                        help="student id to generate against (default: a fresh per-run id, so "
                             "the no-repeat rule does not shrink the sample on a second run)")
    parser.add_argument("--skip-generation", action="store_true",
                        help="score stored questions instead of generating new ones "
                             "(pass --student to say whose)")
    args = parser.parse_args()
    student_id = args.student or (
        EVAL_STUDENT if args.skip_generation
        else f"{EVAL_STUDENT}_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}"
    )

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        judge = select_judge()
        print(f"[Judge] {judge['judge_provider']}/{judge['judge_model']} "
              f"({judge['independence']})")

        retriever = get_retriever()

        print(f"[Eval] Student: {student_id}")

        if args.skip_generation:
            rows = crud.get_quiz_history(db, student_id, limit=args.count, answered_only=False)
            sampled = [{
                "attempt_id": r.attempt_id, "topic_id": r.topic_id,
                "topic_name": r.topic_name,
                "week": (find_topic(r.topic_id) or {}).get("week", 0) if r.topic_id else 0,
                "difficulty": r.difficulty, "question_text": r.question_text,
                "options": list(r.options or []), "correct_answer": r.correct_answer,
                "source_chunks": list(r.source_chunks or []),
            } for r in rows if r.options and r.reason != "cached"]
        else:
            sampled = sample_questions(db, retriever, args.count, student_id)

        if not sampled:
            print("No questions to evaluate.")
            return

        print(f"\n[Judge] Scoring {len(sampled)} questions...")
        scores: list[dict] = []
        judged_rows: list[tuple[dict, dict]] = []
        for i, q in enumerate(sampled, start=1):
            context, cited_types = fetch_context(retriever, q)
            q["cited_source_types"] = cited_types
            score = run_judge(judge, q, context) if context else {}
            if score:
                scores.append(score)
            judged_rows.append((q, score))
            print(f"  [{i}/{len(sampled)}] {q['topic_name']}: "
                  + (", ".join(f"{k}={v:.1f}" for k, v in score.items()) if score else "not scored"))

        structural = structural_checks(sampled)
        prepost = prepost_analysis(db)

        report = build_report(judge, sampled, scores, structural, prepost, judged_rows)
        reports_dir = ROOT_DIR / "reports"
        reports_dir.mkdir(exist_ok=True)
        report_file = reports_dir / "quiz_evaluation_metrics.md"
        report_file.write_text(report, encoding="utf-8")

        relevant = sum(1 for s in scores if s.get("tests_topic", 0.0) >= RELEVANCE_THRESHOLD)
        # Console output stays ASCII — the Windows console codepage cannot encode the
        # symbols the markdown report uses.
        print("\n" + "=" * 52)
        print(" QUIZ EVALUATION COMPLETE ")
        print("=" * 52)
        print(f"   Relevance (tests_topic >= {RELEVANCE_THRESHOLD}): "
              f"{round(relevant / max(1, len(scores)) * 100, 1)}%  (target >= 80%)")
        print(f"   Grounded questions              : {structural['grounded_pct']}%")
        print(f"   Citing pq/PYQ exam material     : "
              f"{structural['exam_grounded_pct']}%"
              if structural["exam_grounded_pct"] is not None
              else "   Citing pq/PYQ exam material     : not resolvable")
        print(f"   Correct-option positions        : {structural['position_distribution']}")
        print(f"   Judge independence              : {judge['independence']}")
        if prepost["pairs"]:
            print(f"   Medium-item accuracy delta      : {prepost['medium_accuracy_delta_pct']} pts")
            print(f"   Mastery delta                   : {prepost['mean_mastery_delta_pct']} pts")
        else:
            print("   Pre/post improvement            : insufficient data (see report)")
        print("=" * 52)
        print(f"\n Report saved to: {report_file.relative_to(ROOT_DIR)}\n")
    finally:
        db.close()


if __name__ == "__main__":
    main()
