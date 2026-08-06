"""
evaluate_question_intelligence.py
Measures the question bank against Milestone 1 §3.5:

    Deduplication Precision >= 85%   and   Cluster F1 Score >= 80%

Run from the repo root, after `python src/build_question_bank.py`:

    python src/evaluate_question_intelligence.py --pairs 60

Both metrics are reported PER SOURCE TYPE and then pooled. `faq` units are topic
explainers ("Question/Topic: Ensemble Techniques" followed by prose), not questions a
student asked — so "are these the same doubt?" measures something genuinely different
there than it does over `pq`, and a single pooled figure averages two behaviours into
one uninterpretable number.

Two statistical points that decide whether the numbers mean anything:

  - Cluster F1 is estimated from a STRATIFIED sample with Horvitz-Thompson inverse
    probability weights. An unweighted stratified sample is not an unbiased estimate of
    population pairwise F1, and this design is deliberately heavy on hard negatives, so
    unweighted numbers would flatter it.
  - The pair population is restricted to pairs above a stated COSINE FLOOR, printed in
    the report. Without it, ~n^2/2 pairs sit in the random cross-cluster stratum, each
    sampled pair carries a weight on the order of 10^4, and a single judge false
    positive moves estimated recall by tens of points. Pairs below the floor are assumed
    non-duplicates by construction — a real assumption, so it is stated rather than
    buried. A bootstrap confidence interval is published beside every point estimate.

Judged verdicts are cached in the `question_evaluation_labels` table, keyed by the sorted
unit-id pair, so re-runs are free, reproducible without API keys, and the gold set grows
over time. `invoke_judge` returning None means UNGRADED: such a pair is dropped from the
denominator, never counted as a disagreement — and a metric with nothing judged is
reported as NOT MEASURED rather than as 0%. `--require-judge` makes that a hard failure
instead of a published caveat.
"""
from __future__ import annotations

import argparse
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    from src import question_intelligence as qi
    from src.api.services import question_repository as repo
    from src.config import QI_CLUSTER_DISTANCE, QI_DUPLICATE_THRESHOLD
    from src.database.models import QuestionEvaluationLabel
    from src.database.session import SessionLocal
    from src.llm_judge import NoJudgeAvailableError, invoke_judge, new_session
except ModuleNotFoundError:  # pragma: no cover - import shim
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import question_intelligence as qi
    from src.api.services import question_repository as repo
    from src.config import QI_CLUSTER_DISTANCE, QI_DUPLICATE_THRESHOLD
    from src.database.models import QuestionEvaluationLabel
    from src.database.session import SessionLocal
    from src.llm_judge import NoJudgeAvailableError, invoke_judge, new_session

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT_DIR / "reports" / "question_intelligence_metrics.md"

DEDUP_TARGET = 0.85
CLUSTER_F1_TARGET = 0.80

# Pairs below this cosine similarity are assumed non-duplicates and excluded from the
# evaluated population. See the module docstring for why an unbounded population makes
# the recall estimator unusable.
COSINE_FLOOR = 0.55

BOOTSTRAP_ROUNDS = 2000


# ── Label cache ───────────────────────────────────────────────────────────────

class LabelStore:
    """A dict-shaped view over `question_evaluation_labels`.

    Reads are served from one query taken at start-up; writes go straight to the
    session and are committed by `flush()`. The dict interface is deliberate — the two
    evaluators use `.get(key)` and `store[key] = {...}` and should not care that the
    gold set is now a table rather than a JSON file a run could clobber.
    """

    def __init__(self, db):
        self.db = db
        self._rows: dict[str, dict] = {}
        for row in db.query(QuestionEvaluationLabel).all():
            self._rows[row.pair_key] = {
                "label": bool(row.label),
                "source": row.source,
                "kind": row.metric_kind,
                "pair": row.pair_key.split("|", 1),
            }

    def get(self, key: str):
        return self._rows.get(key)

    def __contains__(self, key: str) -> bool:
        return key in self._rows

    def __len__(self) -> int:
        return len(self._rows)

    def __setitem__(self, key: str, value: dict) -> None:
        self._rows[key] = value
        row = self.db.get(QuestionEvaluationLabel, key)
        if row is None:
            row = QuestionEvaluationLabel(pair_key=key)
            self.db.add(row)
        row.metric_kind = value.get("kind", "duplicate")
        row.label = bool(value.get("label"))
        row.source = value.get("source", "judge")
        row.note = value.get("note")

    def flush(self) -> None:
        self.db.commit()


def pair_key(a: str, b: str) -> str:
    return "|".join(sorted((a, b)))


# ── Judging ───────────────────────────────────────────────────────────────────

_DEDUP_RUBRIC = """You are auditing a de-duplicated question bank for a university
machine-learning course. Decide whether the two entries below are THE SAME underlying
question or doubt.

Same means: a student asking one would be fully answered by the other. Superficial
differences in wording, numbers, or formatting do not make them different. Two questions
that merely share a topic are NOT the same.

Entry A ({source_a}, week {week_a}):
{text_a}

Entry B ({source_b}, week {week_b}):
{text_b}

Reply with ONLY a JSON object, no prose:
{{"same": true or false, "confidence": 0.0 to 1.0}}"""

_CONCEPT_RUBRIC = """You are auditing the clustering of a question bank for a university
machine-learning course. Decide whether the two entries below are about THE SAME CONCEPT
and therefore belong in the same group of related doubts.

Same concept means: they concern the same specific technique, definition, or derivation
(e.g. both about the kernel trick, or both about bagging in random forests). Being from
the same week, or both being "about machine learning", is NOT enough.

Entry A ({source_a}, week {week_a}):
{text_a}

Entry B ({source_b}, week {week_b}):
{text_b}

Reply with ONLY a JSON object, no prose:
{{"same_concept": true or false, "confidence": 0.0 to 1.0}}"""


def _entry_text(unit: dict, limit: int = 700) -> str:
    parts = [unit.get("text", "")]
    if unit.get("options"):
        parts.append("Options: " + " | ".join(unit["options"]))
    return "\n".join(p for p in parts if p)[:limit]


def judge_pair(session, unit_a: dict, unit_b: dict, rubric: str, key: str) -> tuple[bool | None, str]:
    """Ask the judge one yes/no question. Returns (verdict, label); None = ungraded."""
    prompt = rubric.format(
        source_a=unit_a["source_type"], week_a=unit_a["week"], text_a=_entry_text(unit_a),
        source_b=unit_b["source_type"], week_b=unit_b["week"], text_b=_entry_text(unit_b),
    )
    parsed, label = invoke_judge(session, prompt, temperature=0.0)
    if not parsed:
        return None, label
    value = parsed.get(key)
    if isinstance(value, str):
        value = value.strip().lower() in {"true", "yes", "1"}
    if not isinstance(value, bool):
        return None, label
    return value, label


# ── Statistics ────────────────────────────────────────────────────────────────

def bootstrap_interval(values: list[float], weights: list[float] | None = None,
                       rounds: int = BOOTSTRAP_ROUNDS) -> tuple[float, float]:
    """Percentile bootstrap over a weighted mean. Empty input yields (0, 0)."""
    if not values:
        return 0.0, 0.0
    arr = np.asarray(values, dtype=float)
    wts = np.asarray(weights, dtype=float) if weights else np.ones_like(arr)
    rng = np.random.default_rng(20260806)
    means = []
    n = len(arr)
    for _ in range(rounds):
        idx = rng.integers(0, n, n)
        total = wts[idx].sum()
        means.append(float((arr[idx] * wts[idx]).sum() / total) if total else 0.0)
    return round(float(np.percentile(means, 2.5)), 4), round(float(np.percentile(means, 97.5)), 4)


def _fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _verdict(value: float, target: float, judged: int) -> str:
    if judged == 0:
        return "not measured"
    return "MET" if value >= target else "below target"


def _measured(value: float, judged: int) -> str:
    """A percentage, or an em dash when nothing was judged.

    Printing `0.0%` next to a `≥ 80%` target for a metric that was never measured is
    the one reporting failure this harness must not commit: it reads as a catastrophic
    result rather than as an absent one.
    """
    return _fmt_pct(value) if judged else "—"


def _measured_ci(ci: list[float], judged: int) -> str:
    return f"{_fmt_pct(ci[0])}–{_fmt_pct(ci[1])}" if judged else "—"


# ── Deduplication precision ───────────────────────────────────────────────────

def evaluate_dedup(bank: dict, vectors: np.ndarray, labels: dict, sample_size: int,
                   session, rng: random.Random) -> dict:
    """Sample flagged duplicate pairs and ask whether they are the same doubt."""
    units = bank["units"]
    by_id = {u["unit_id"]: u for u in units}
    groups: dict[int, list[str]] = {}
    for unit in units:
        if unit.get("dup_group_id") is not None:
            groups.setdefault(unit["dup_group_id"], []).append(unit["unit_id"])

    flagged: list[tuple[str, str]] = []
    for members in groups.values():
        if len(members) < 2:
            continue
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                flagged.append((members[i], members[j]))

    rng.shuffle(flagged)
    sample = flagged[:sample_size]

    results: dict[str, list[int]] = {}
    ungraded = 0
    judge_label = "cache"
    for a, b in sample:
        key = pair_key(a, b)
        cached = labels.get(key)
        if cached is not None:
            verdict = cached["label"]
        else:
            if session is None:
                ungraded += 1
                continue
            verdict, judge_label = judge_pair(session, by_id[a], by_id[b], _DEDUP_RUBRIC, "same")
            if verdict is None:
                ungraded += 1
                continue
            labels[key] = {"label": verdict, "source": "judge",
                           "pair": [a, b], "kind": "duplicate"}
        # A cross-source pair is attributed to both sources; there is no single
        # "source" for a pq/PYQ duplicate and dropping such pairs would remove exactly
        # the cross-source matches the module exists to find.
        for source in {by_id[a]["source_type"], by_id[b]["source_type"]}:
            results.setdefault(source, []).append(1 if verdict else 0)
        results.setdefault("pooled", []).append(1 if verdict else 0)

    report = {"flagged_pairs": len(flagged), "sampled": len(sample),
              "ungraded": ungraded, "judge": judge_label, "by_source": {}}
    for source, outcomes in sorted(results.items()):
        low, high = bootstrap_interval([float(o) for o in outcomes])
        report["by_source"][source] = {
            "judged": len(outcomes),
            "agreements": sum(outcomes),
            "precision": round(sum(outcomes) / len(outcomes), 4) if outcomes else 0.0,
            "ci": [low, high],
        }
    return report


# ── Cluster pairwise F1 ───────────────────────────────────────────────────────

def _strata(bank: dict, vectors: np.ndarray, rng: random.Random, per_stratum: int):
    """Build the three sampling strata over pairs above the cosine floor.

    within            — pairs the clustering put together (drives precision)
    nearest_cross     — the closest pairs it separated (the hard negatives; drives recall)
    random_cross      — everything else it separated, so the population is covered
    """
    units = bank["units"]
    index = {u["unit_id"]: i for i, u in enumerate(units)}
    canonicals = [u for u in units if u.get("is_canonical")]
    rows = [index[u["unit_id"]] for u in canonicals]
    normalised = qi.l2_normalise(vectors[rows])
    similarity = normalised @ normalised.T
    n = len(canonicals)

    within: list[tuple[int, int, float]] = []
    cross: list[tuple[int, int, float]] = []
    for i in range(n):
        for j in range(i + 1, n):
            score = float(similarity[i, j])
            if score < COSINE_FLOOR:
                continue
            if canonicals[i]["cluster_id"] == canonicals[j]["cluster_id"]:
                within.append((i, j, score))
            else:
                cross.append((i, j, score))

    cross.sort(key=lambda t: -t[2])
    split = min(len(cross), max(per_stratum * 4, 200))
    nearest, remainder = cross[:split], cross[split:]

    def take(population, size):
        pool = list(population)
        rng.shuffle(pool)
        return pool[:size]

    return canonicals, {
        "within": {"population": len(within), "sample": take(within, per_stratum)},
        "nearest_cross": {"population": len(nearest), "sample": take(nearest, per_stratum)},
        "random_cross": {"population": len(remainder), "sample": take(remainder, per_stratum)},
    }


def evaluate_clusters(bank: dict, vectors: np.ndarray, labels: dict, per_stratum: int,
                      session, rng: random.Random) -> dict:
    canonicals, strata = _strata(bank, vectors, rng, per_stratum)

    judged: dict[str, list[tuple[bool, bool]]] = {}   # stratum -> [(same_concept, clustered_together)]
    ungraded = 0
    judge_label = "cache"

    for name, stratum in strata.items():
        outcomes: list[tuple[bool, bool]] = []
        for i, j, _score in stratum["sample"]:
            unit_a, unit_b = canonicals[i], canonicals[j]
            key = pair_key(unit_a["unit_id"], unit_b["unit_id"])
            cached = labels.get(key)
            if cached is not None and cached.get("kind") == "concept":
                verdict = cached["label"]
            else:
                if session is None:
                    ungraded += 1
                    continue
                verdict, judge_label = judge_pair(session, unit_a, unit_b, _CONCEPT_RUBRIC, "same_concept")
                if verdict is None:
                    ungraded += 1
                    continue
                labels[key] = {"label": verdict, "source": "judge",
                               "pair": [unit_a["unit_id"], unit_b["unit_id"]], "kind": "concept"}
            outcomes.append((bool(verdict), name == "within"))
        judged[name] = outcomes

    # Horvitz-Thompson: each sampled pair stands for (stratum population / sampled count)
    # pairs in the population. Without this the hard-negative-heavy design would be read
    # as if it were a uniform sample.
    weights = {
        name: (strata[name]["population"] / len(judged[name])) if judged[name] else 0.0
        for name in strata
    }

    tp = fp = fn = 0.0
    tp_terms: list[float] = []
    tp_weights: list[float] = []
    for name, outcomes in judged.items():
        weight = weights[name]
        for same_concept, clustered in outcomes:
            if clustered and same_concept:
                tp += weight
            elif clustered and not same_concept:
                fp += weight
            elif not clustered and same_concept:
                fn += weight
            tp_terms.append(1.0 if (clustered and same_concept) else 0.0)
            tp_weights.append(weight)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    # Bootstrap the whole estimator, resampling within strata so the weights stay valid.
    rng_np = np.random.default_rng(20260806)
    f1_draws: list[float] = []
    for _ in range(400):
        b_tp = b_fp = b_fn = 0.0
        for name, outcomes in judged.items():
            if not outcomes:
                continue
            weight = weights[name]
            idx = rng_np.integers(0, len(outcomes), len(outcomes))
            for k in idx:
                same_concept, clustered = outcomes[int(k)]
                if clustered and same_concept:
                    b_tp += weight
                elif clustered and not same_concept:
                    b_fp += weight
                elif not clustered and same_concept:
                    b_fn += weight
        b_p = b_tp / (b_tp + b_fp) if (b_tp + b_fp) else 0.0
        b_r = b_tp / (b_tp + b_fn) if (b_tp + b_fn) else 0.0
        f1_draws.append((2 * b_p * b_r / (b_p + b_r)) if (b_p + b_r) else 0.0)

    return {
        "cosine_floor": COSINE_FLOOR,
        "population": {name: strata[name]["population"] for name in strata},
        "sampled": {name: len(judged[name]) for name in judged},
        "weights": {name: round(w, 1) for name, w in weights.items()},
        "ungraded": ungraded,
        "judge": judge_label,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "f1_ci": [round(float(np.percentile(f1_draws, 2.5)), 4),
                  round(float(np.percentile(f1_draws, 97.5)), 4)] if f1_draws else [0.0, 0.0],
    }


# ── Report ────────────────────────────────────────────────────────────────────

def _cluster_judged(clusters: dict) -> int:
    return sum(clusters.get("sampled", {}).values())


def write_report(bank: dict, dedup: dict, clusters: dict) -> None:
    stats = bank["stats"]
    pooled = dedup["by_source"].get("pooled", {"precision": 0.0, "judged": 0, "ci": [0, 0]})

    lines = [
        "# Question Intelligence — Evaluation",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        f"bank schema v{bank['schema_version']} · embeddings `{bank['embed_model']}`_",
        "",
        "## Milestone 1 §3.5 targets",
        "",
        "| Metric | Target | Measured | 95% CI | Verdict |",
        "|---|--:|--:|---|---|",
        f"| Deduplication precision (pooled) | ≥ {_fmt_pct(DEDUP_TARGET)} | "
        f"{_measured(pooled['precision'], pooled['judged'])} | "
        f"{_measured_ci(pooled['ci'], pooled['judged'])} | "
        f"{_verdict(pooled['precision'], DEDUP_TARGET, pooled['judged'])} |",
        f"| Cluster pairwise F1 | ≥ {_fmt_pct(CLUSTER_F1_TARGET)} | "
        f"{_measured(clusters['f1'], _cluster_judged(clusters))} | "
        f"{_measured_ci(clusters['f1_ci'], _cluster_judged(clusters))} | "
        f"{_verdict(clusters['f1'], CLUSTER_F1_TARGET, _cluster_judged(clusters))} |",
        "",
        f"Judge independence rung: **{clusters.get('judge') or dedup.get('judge')}**. "
        "An ungraded pair is dropped from the denominator, never scored as a disagreement.",
        "",
        "## Deduplication precision, per source",
        "",
        "`faq` units are topic explainers rather than questions students asked, so "
        "\"is this a duplicate question?\" measures something different there than over "
        "`pq`. A single pooled figure averages two behaviours into one uninterpretable "
        "number, which is why the split comes first.",
        "",
        f"Flagged duplicate pairs in the bank: **{dedup['flagged_pairs']}** · "
        f"sampled **{dedup['sampled']}** · ungraded (dropped) **{dedup['ungraded']}**",
        "",
        "| Source | Judged | Agreements | Precision | 95% CI |",
        "|---|--:|--:|--:|---|",
    ]
    for source in ("pq", "faq", "PYQ", "pooled"):
        entry = dedup["by_source"].get(source)
        if not entry:
            continue
        lines.append(
            f"| `{source}` | {entry['judged']} | {entry['agreements']} | "
            f"{_fmt_pct(entry['precision'])} | {_fmt_pct(entry['ci'][0])}–{_fmt_pct(entry['ci'][1])} |"
        )

    lines += [
        "",
        "## Cluster pairwise F1",
        "",
        f"Evaluated population: pairs of canonical units with cosine similarity ≥ "
        f"**{clusters['cosine_floor']}**. Pairs below the floor are assumed "
        "non-duplicates by construction — a real assumption, stated rather than buried. "
        "Estimates use Horvitz–Thompson inverse-probability weights, because an "
        "unweighted stratified sample is not an unbiased estimate of population pairwise "
        "F1 and this design is deliberately heavy on hard negatives.",
        "",
        "| Stratum | Population | Sampled | HT weight |",
        "|---|--:|--:|--:|",
    ]
    for name in ("within", "nearest_cross", "random_cross"):
        lines.append(
            f"| {name} | {clusters['population'].get(name, 0)} | "
            f"{clusters['sampled'].get(name, 0)} | {clusters['weights'].get(name, 0)} |"
        )
    judged_pairs = _cluster_judged(clusters)
    lines += [
        "",
        (f"- Precision **{_fmt_pct(clusters['precision'])}** · "
         f"Recall **{_fmt_pct(clusters['recall'])}** · "
         f"F1 **{_fmt_pct(clusters['f1'])}** "
         f"(95% CI {_fmt_pct(clusters['f1_ci'][0])}–{_fmt_pct(clusters['f1_ci'][1])})"
         if judged_pairs else
         "- **Not measured.** No pair in any stratum received a verdict, so there is no "
         "estimate to report — not an estimate of zero. Seed labels into "
         "`question_evaluation_labels`, or re-run with a reachable judge."),
        f"- Ungraded pairs dropped: {clusters['ungraded']}",
        "",
        "## Bank under test",
        "",
        f"- {stats['unit_count']} units → {stats['canonical_count']} distinct doubts → "
        f"{stats['cluster_count']} clusters (duplicate rate {stats['duplicate_rate']:.1%})",
        f"- Thresholds: duplicate ≥ {QI_DUPLICATE_THRESHOLD} cosine, "
        f"cluster cut {QI_CLUSTER_DISTANCE} cosine distance",
        "",
        "## Limitations",
        "",
        "- **`discourse` contributes nothing.** The directory is empty and no chunk carries",
        "  that source type, so both metrics cover a narrower corpus than §2.2.8 describes —",
        "  and forum threads are precisely where near-duplicate doubts accumulate.",
        "- **PYQ is OCR output.** Its question boundaries are not recoverable, so each",
        "  extracted block is one unit and its cluster titles are frequently unusable even",
        "  when the grouping is right.",
        "- **The judge is an LLM, not ground truth.** Verdicts are cached in the",
        "  `question_evaluation_labels` table and can be hand-corrected (`source` marks a",
        "  human label); the cache is consulted first, so corrections persist and re-runs",
        "  are free and reproducible without API keys.",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the question intelligence bank.")
    parser.add_argument("--pairs", type=int, default=60, help="duplicate pairs to sample")
    parser.add_argument("--per-stratum", type=int, default=20, help="cluster pairs per stratum")
    parser.add_argument("--offline", action="store_true",
                        help="use only cached labels; make no LLM calls")
    parser.add_argument("--require-judge", action="store_true",
                        help="fail instead of publishing a report with an unmeasured metric")
    args = parser.parse_args()

    with SessionLocal() as db:
        try:
            bank, vectors = repo.load_bank_for_evaluation(db)
        except LookupError as exc:
            print(f"{exc}")
            return 1

        labels = LabelStore(db)
        print(f"[labels] {len(labels)} cached verdicts in question_evaluation_labels")
        rng = random.Random(20260806)

        session = None
        if not args.offline:
            try:
                session = new_session()
            except NoJudgeAvailableError as exc:
                if args.require_judge:
                    print(f"[judge] unavailable ({exc}); --require-judge is set, so nothing "
                          "was written.")
                    return 2
                print(f"[judge] unavailable ({exc}); falling back to cached labels only.")

        print("[dedup] sampling flagged duplicate pairs ...")
        dedup = evaluate_dedup(bank, vectors, labels, args.pairs, session, rng)

        print("[cluster] sampling stratified concept pairs ...")
        cluster_session = None
        if not args.offline:
            try:
                cluster_session = new_session()
            except NoJudgeAvailableError:
                cluster_session = None
        clusters = evaluate_clusters(bank, vectors, labels, args.per_stratum, cluster_session, rng)
        labels.flush()

    pooled = dedup["by_source"].get("pooled", {"precision": 0.0, "judged": 0})
    cluster_judged = _cluster_judged(clusters)

    if args.require_judge and (not pooled["judged"] or not cluster_judged):
        print("[abort] --require-judge: "
              f"{pooled['judged']} dedup and {cluster_judged} cluster pairs were judged. "
              "No report written — an unmeasured metric must not be published as a number.")
        return 2

    write_report(bank, dedup, clusters)

    print(f"[done] dedup precision {pooled['precision']:.1%} over {pooled['judged']} judged pairs "
          f"(target {DEDUP_TARGET:.0%})" if pooled["judged"] else
          "[done] dedup precision NOT MEASURED (no pair was judged)")
    print(f"       cluster F1 {clusters['f1']:.1%} "
          f"[{clusters['f1_ci'][0]:.1%}, {clusters['f1_ci'][1]:.1%}] (target {CLUSTER_F1_TARGET:.0%})"
          if cluster_judged else
          "       cluster F1 NOT MEASURED (no pair was judged)")
    print(f"       {REPORT_PATH.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
