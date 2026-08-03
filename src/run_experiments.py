"""Milestone 4 — Main Experiment Runner.

Orchestrates the full experiment grid:
  1. For each config that needs new chunking → rechunk
  2. Ingest into a dedicated local Qdrant collection
  3. Run the full evaluation suite
  4. Save per-experiment JSON log + aggregate CSV + plots

Run modes:
  python src/run_experiments.py            # full grid (20+ experiments)
  python src/run_experiments.py --quick    # 6-experiment quick grid
  python src/run_experiments.py --name baseline  # single experiment by name
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

load_dotenv()

from src.experiment_config import (
    ExperimentConfig,
    ExperimentResult,
    get_baseline_config,
    get_experiment_grid,
    get_quick_grid,
)
from src.eval_dataset import EVAL_DATASET
from src.eval_runner import run_single_evaluation
from src.ingestion_helper import ingest_config_to_qdrant, collection_exists


LOGS_DIR = ROOT_DIR / "reports" / "experiment_logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def save_result_json(result: ExperimentResult) -> Path:
    """Save per-experiment JSON log."""
    out = LOGS_DIR / f"{result.config.name}.json"
    out.write_text(json.dumps(result.summary_dict(), indent=2), encoding="utf-8")
    print(f"  [Log] Saved → {out.relative_to(ROOT_DIR)}")
    return out


def save_aggregate_csv(results: list[ExperimentResult]) -> Path:
    """Write a flat CSV comparing all experiments side-by-side."""
    out = ROOT_DIR / "reports" / "experiment_comparison.csv"
    fieldnames = [
        "experiment", "chunk_size", "chunk_overlap", "embedding_model",
        "retrieval_mode", "top_k", "use_reranker", "temperature", "prompt_style",
        "precision_at_5", "recall_at_5", "mrr_at_5", "recall_at_10",
        "faithfulness", "answer_relevance", "context_precision",
        "total_time_seconds",
    ]
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {
                "experiment": r.config.name,
                "chunk_size": r.config.chunk_size,
                "chunk_overlap": r.config.chunk_overlap,
                "embedding_model": r.config.embedding_model,
                "retrieval_mode": r.config.retrieval_mode,
                "top_k": r.config.top_k,
                "use_reranker": r.config.use_reranker,
                "temperature": r.config.temperature,
                "prompt_style": r.config.prompt_style,
                "precision_at_5": round(r.precision_at_5, 4),
                "recall_at_5": round(r.recall_at_5, 4),
                "mrr_at_5": round(r.mrr_at_5, 4),
                "recall_at_10": round(r.recall_at_10, 4),
                "faithfulness": round(r.faithfulness, 4),
                "answer_relevance": round(r.answer_relevance, 4),
                "context_precision": round(r.context_precision, 4),
                "total_time_seconds": round(r.total_time_seconds, 2),
            }
            writer.writerow(row)
    print(f"\n[CSV] Aggregate comparison → {out.relative_to(ROOT_DIR)}")
    return out


def generate_plots(results: list[ExperimentResult]) -> None:
    """Generate bar-chart comparison plots for each metric group."""
    try:
        import matplotlib
        matplotlib.use("Agg")   # non-interactive backend (no display needed)
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("[Plots] matplotlib not installed — skipping plots. Install with: pip install matplotlib")
        return

    plots_dir = ROOT_DIR / "reports" / "plots"
    plots_dir.mkdir(exist_ok=True)

    names = [r.config.name for r in results]
    colors = ["#2196F3" if r.config.name == "baseline" else "#64B5F6" for r in results]

    metric_groups = {
        "retrieval_metrics": {
            "Precision@5": [r.precision_at_5 for r in results],
            "Recall@5": [r.recall_at_5 for r in results],
            "MRR@5": [r.mrr_at_5 for r in results],
            "Recall@10": [r.recall_at_10 for r in results],
        },
        "generation_metrics": {
            "Faithfulness": [r.faithfulness for r in results],
            "Answer Relevance": [r.answer_relevance for r in results],
            "Context Precision": [r.context_precision for r in results],
        },
    }

    for group_name, metrics in metric_groups.items():
        n_metrics = len(metrics)
        fig, axes = plt.subplots(1, n_metrics, figsize=(6 * n_metrics, max(5, len(names) * 0.4 + 2)))
        if n_metrics == 1:
            axes = [axes]

        fig.suptitle(f"Milestone 4 — {group_name.replace('_', ' ').title()}", fontsize=14, fontweight="bold")

        for ax, (metric_name, values) in zip(axes, metrics.items()):
            bars = ax.barh(names, values, color=colors, edgecolor="white", height=0.6)
            ax.set_xlim(0, 1.05)
            ax.set_xlabel("Score (0–1)", fontsize=10)
            ax.set_title(metric_name, fontsize=11, fontweight="bold")
            ax.axvline(x=0.8, color="orange", linestyle="--", alpha=0.5, label="0.8 threshold")
            ax.axvline(x=0.9, color="green", linestyle="--", alpha=0.5, label="0.9 threshold")
            # Annotate values
            for bar, val in zip(bars, values):
                ax.text(val + 0.01, bar.get_y() + bar.get_height() / 2,
                        f"{val:.2f}", va="center", fontsize=8)
            ax.invert_yaxis()
            ax.grid(axis="x", alpha=0.3)
            ax.legend(fontsize=7)

        plt.tight_layout()
        plot_path = plots_dir / f"{group_name}.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[Plot] Saved → {plot_path.relative_to(ROOT_DIR)}")


def generate_markdown_report(results: list[ExperimentResult]) -> Path:
    """Auto-generate the Milestone 4 markdown report."""
    plots_dir = ROOT_DIR / "reports" / "plots"

    report = "# Milestone 4 — RAG Optimization Experiment Report\n\n"
    report += "## 1. Experiment Overview\n\n"
    report += f"Total experiments run: **{len(results)}**\n\n"

    # Summary table
    report += "## 2. Aggregate Comparison Table\n\n"
    report += (
        "| Experiment | Chunk | Embed | Mode | top_k | Rerank | Temp | Prompt "
        "| P@5 | R@5 | MRR | Faith | AnsRel | CtxPrec |\n"
    )
    report += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"

    for r in results:
        c = r.config
        report += (
            f"| {c.name} | {c.chunk_size}/{c.chunk_overlap} "
            f"| {c.embedding_model.split('/')[-1][:12]} "
            f"| {c.retrieval_mode[:6]} | {c.top_k} | {'✓' if c.use_reranker else '✗'} "
            f"| {c.temperature} | {c.prompt_style[:6]} "
            f"| {r.precision_at_5:.2f} | {r.recall_at_5:.2f} | {r.mrr_at_5:.2f} "
            f"| {r.faithfulness:.2f} | {r.answer_relevance:.2f} | {r.context_precision:.2f} |\n"
        )

    report += "\n---\n\n"

    # Best per metric
    report += "## 3. Best Configuration Per Metric\n\n"
    metric_map = {
        "Precision@5": lambda r: r.precision_at_5,
        "Recall@5": lambda r: r.recall_at_5,
        "MRR@5": lambda r: r.mrr_at_5,
        "Faithfulness": lambda r: r.faithfulness,
        "Answer Relevance": lambda r: r.answer_relevance,
        "Context Precision": lambda r: r.context_precision,
    }
    for metric_name, key_fn in metric_map.items():
        best = max(results, key=key_fn)
        report += f"- **{metric_name}**: `{best.config.name}` → **{key_fn(best):.4f}**\n"

    report += "\n---\n\n"

    # Plots
    report += "## 4. Metric Comparison Plots\n\n"
    for plot_name in ["retrieval_metrics", "generation_metrics"]:
        plot_path = plots_dir / f"{plot_name}.png"
        if plot_path.exists():
            report += f"### {plot_name.replace('_', ' ').title()}\n\n"
            report += f"![{plot_name}]({plot_path})\n\n"

    report += "\n---\n\n"

    # Full per-query breakdown for EVERY experiment
    report += "## 5. Full Per-Query Results (All Experiments)\n\n"
    report += "_Each experiment shows all query answers with complete metrics._\n\n"

    for r in results:
        c = r.config
        report += f"---\n\n### Experiment: `{c.name}`\n\n"
        report += f"> **Config**: chunk={c.chunk_size}/{c.chunk_overlap} | "
        report += f"embed={c.embedding_model.split('/')[-1]} | "
        report += f"mode={c.retrieval_mode} | top_k={c.top_k} | "
        report += f"reranker={'Yes' if c.use_reranker else 'No'} | "
        report += f"temp={c.temperature} | prompt={c.prompt_style}\n\n"

        if not r.per_query_results:
            report += "_No per-query data saved (experiment may have failed or used old code)._\n\n"
            continue

        for i, q in enumerate(r.per_query_results, 1):
            cat = q.get("category", "unknown")
            oos = q.get("is_out_of_scope", False)
            report += f"#### Q{i} [{cat}]: {q['query']}\n\n"

            # Retrieval metrics (in-scope only)
            if not oos:
                report += (
                    f"| Metric | Score |\n|---|---|\n"
                    f"| Precision@5 | {q.get('precision_at_5', 0):.2f} |\n"
                    f"| Recall@5 | {q.get('recall_at_5', 0):.2f} |\n"
                    f"| MRR@5 | {q.get('mrr_at_5', 0):.2f} |\n"
                    f"| Recall@10 | {q.get('recall_at_10', 0):.2f} |\n"
                    f"| Faithfulness | {q.get('faithfulness', 0):.2f} |\n"
                    f"| Answer Relevance | {q.get('answer_relevance', 0):.2f} |\n"
                    f"| Context Precision | {q.get('context_precision', 0):.2f} |\n\n"
                )
            else:
                report += f"_Out-of-scope query — guardrail check only._\n\n"
                report += (
                    f"| Guardrail Metric | Score |\n|---|---|\n"
                    f"| Faithfulness | {q.get('faithfulness', 0):.2f} |\n"
                    f"| Answer Relevance | {q.get('answer_relevance', 0):.2f} |\n\n"
                )

            # Full answer
            answer_text = q.get("answer", "").strip()
            if answer_text:
                report += f"**Answer:**\n```\n{answer_text}\n```\n\n"

    report += "---\n\n"

    report += "## 6. Key Findings\n\n"
    report += "_Auto-generated summary — add your narrative observations below._\n\n"

    valid = [r for r in results if not r.errors]
    if valid:
        best_overall = max(valid, key=lambda r: (
            r.faithfulness + r.answer_relevance + r.context_precision + r.precision_at_5
        ) / 4)
        report += f"- **Best overall configuration**: `{best_overall.config.name}`\n"
        baseline_r = next((r for r in results if r.config.name == "baseline"), None)
        if baseline_r and best_overall.config.name != "baseline":
            delta_faith = best_overall.faithfulness - baseline_r.faithfulness
            delta_prec = best_overall.precision_at_5 - baseline_r.precision_at_5
            report += f"- **Faithfulness improvement over baseline**: {delta_faith:+.4f}\n"
            report += f"- **Precision@5 improvement over baseline**: {delta_prec:+.4f}\n"

    out = ROOT_DIR / "reports" / "milestone4_report.md"
    out.write_text(report, encoding="utf-8")
    print(f"\n[Report] Milestone 4 markdown → {out.relative_to(ROOT_DIR)}")
    return out


# ── Main Entry Point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Milestone 4 — RAG Experiment Runner")
    parser.add_argument("--quick", action="store_true",
                        help="Run only the 6-experiment quick grid")
    parser.add_argument("--name", type=str, default=None,
                        help="Run a single experiment by name (e.g. 'baseline')")
    parser.add_argument("--skip-ingest", action="store_true",
                        help="Skip ingestion if collection already exists")
    parser.add_argument("--no-plots", action="store_true",
                        help="Skip generating plots")
    args = parser.parse_args()

    # Select experiment set
    if args.name:
        all_exps = get_experiment_grid()
        grid = [e for e in all_exps if e.name == args.name]
        if not grid:
            print(f"[Error] No experiment named '{args.name}'. Available:")
            for e in all_exps:
                print(f"  {e.name}")
            sys.exit(1)
    elif args.quick:
        grid = get_quick_grid()
    else:
        grid = get_experiment_grid()

    print(f"\n{'='*60}")
    print(f"  MILESTONE 4 — RAG EXPERIMENT RUNNER")
    print(f"  Running {len(grid)} experiment(s)")
    print(f"{'='*60}\n")

    all_results: list[ExperimentResult] = []
    total_start = time.time()

    for idx, config in enumerate(grid, 1):
        print(f"\n[{idx}/{len(grid)}] Starting: {config.name}")
        print(f"  Description: {config.description}")
        print(f"  Collection : {config.collection_name}")

        # Check if already completed
        log_path = ROOT_DIR / "reports" / "experiment_logs" / f"{config.name}.json"
        if log_path.exists():
            try:
                import json
                with open(log_path, "r") as f:
                    data = json.load(f)
                # Check if it has a non-empty answer (meaning it didn't fail due to rate limits)
                if data.get("per_query_results") and any(q.get("answer") for q in data["per_query_results"]):
                    print(f"  [Skip] Found existing successful log for '{config.name}'. Resuming from here.")
                    # Reconstruct result to add to all_results
                    result = ExperimentResult(config=config)
                    result.precision_at_5 = data["metrics"]["precision_at_5"]
                    result.recall_at_5 = data["metrics"]["recall_at_5"]
                    result.mrr_at_5 = data["metrics"]["mrr_at_5"]
                    result.recall_at_10 = data["metrics"]["recall_at_10"]
                    result.faithfulness = data["metrics"]["faithfulness"]
                    result.answer_relevance = data["metrics"]["answer_relevance"]
                    result.context_precision = data["metrics"]["context_precision"]
                    result.per_query_results = data["per_query_results"]
                    all_results.append(result)
                    continue
            except Exception:
                pass

        exp_start = time.time()

        # Step 1: Smart ingestion — skip if collection already exists
        # Configs that only differ in top_k/temperature/prompt_style share
        # the same collection as the baseline, so no re-ingestion needed.
        try:
            from qdrant_client import QdrantClient
            client = QdrantClient(url=config.qdrant_url)
            existing_collections = [c.name for c in client.get_collections().collections]
        except Exception:
            existing_collections = []

        if not config.needs_reingestion(existing_collections):
            print(f"  [Ingest] Reusing existing collection '{config.collection_name}' (no re-ingestion needed).")
        elif args.skip_ingest:
            print(f"  [Ingest] --skip-ingest flag set, skipping.")
        else:
            print(f"  [Ingest] Chunking + embedding + uploading to Qdrant...")
            ingest_success = ingest_config_to_qdrant(config)
            if not ingest_success:
                print(f"  [Ingest] FAILED — skipping evaluation for {config.name}")
                result = ExperimentResult(
                    config=config,
                    errors=["Ingestion failed"],
                    total_time_seconds=time.time() - exp_start,
                )
                all_results.append(result)
                save_result_json(result)
                continue

        # Step 2: Evaluate
        print(f"  [Eval] Running evaluation suite ({len(EVAL_DATASET)} queries)...")
        result = run_single_evaluation(config, EVAL_DATASET)
        result.total_time_seconds = time.time() - exp_start

        # Step 3: Save per-experiment log
        save_result_json(result)

        # Print quick summary
        print(f"  [Done] P@5={result.precision_at_5:.3f}  R@5={result.recall_at_5:.3f}  "
              f"MRR={result.mrr_at_5:.3f}  Faith={result.faithfulness:.3f}  "
              f"AnsRel={result.answer_relevance:.3f}  "
              f"CtxPrec={result.context_precision:.3f}  "
              f"({result.total_time_seconds:.0f}s)")

        all_results.append(result)

    # Final aggregation
    elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"  ALL EXPERIMENTS COMPLETE ({elapsed:.0f}s total)")
    print(f"{'='*60}")

    if all_results:
        save_aggregate_csv(all_results)
        if not args.no_plots:
            generate_plots(all_results)
        generate_markdown_report(all_results)

    print("\nDone! Check reports/ for all outputs.\n")


if __name__ == "__main__":
    main()
