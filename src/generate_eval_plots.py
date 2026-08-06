"""Generate evaluation visualizations for Milestone 5 report."""
import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("matplotlib not found. Installing...")
    os.system(f"{sys.executable} -m pip install matplotlib")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

PLOTS_DIR = ROOT_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# ── Color palette ──────────────────────────────────────────────────────────────
BLUE   = "#4C9BE8"
GREEN  = "#56C464"
ORANGE = "#F5A623"
RED    = "#E85C5C"
PURPLE = "#9B59B6"
TEAL   = "#1ABC9C"

# ── 1. Golden Dataset Final Metrics Bar Chart ─────────────────────────────────
def plot_golden_dataset_metrics():
    metrics = {
        "Precision@5":        0.36,
        "Recall@5":           0.67,
        "MRR@5":              0.49,
        "Recall@10":          0.67,
        "Faithfulness":       0.89,
        "Answer\nRelevance":  0.99,
        "Context\nPrecision": 0.84,
    }
    colors = [BLUE, BLUE, BLUE, BLUE, GREEN, GREEN, GREEN]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(metrics.keys(), metrics.values(), color=colors, edgecolor="white",
                  linewidth=0.8, zorder=3)

    for bar, val in zip(bars, metrics.values()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Score (0.0 – 1.0)", fontsize=12)
    ax.set_title("Golden Dataset Evaluation — Final System Metrics", fontsize=14, fontweight="bold", pad=16)
    ax.axhline(0.8, color="gray", linewidth=0.8, linestyle="--", label="0.8 target", zorder=2)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    retrieval_patch = mpatches.Patch(color=BLUE,  label="Retrieval Metrics")
    generation_patch = mpatches.Patch(color=GREEN, label="Generation Metrics (LLM-Judge)")
    ax.legend(handles=[retrieval_patch, generation_patch], loc="upper right", fontsize=10)

    plt.tight_layout()
    out = PLOTS_DIR / "golden_dataset_metrics.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out.relative_to(ROOT_DIR)}")


# ── 2. Hyperparameter Experiment Comparison (from Milestone 4) ────────────────
def plot_hyperparameter_comparison():
    experiments = [
        ("Baseline\n(384, bge, hybrid, k5)",  0.825, 1.000, 0.875, 0.92),
        ("Chunk 256\n(256, bge, hybrid, k5)",  0.825, 1.000, 0.937, 0.92),
        ("Chunk 512\n(512, bge, hybrid, k5)",  0.775, 1.000, 0.875, 0.27),
        ("MiniLM\n(384, minilm, hybrid, k5)",  0.775, 1.000, 0.843, 0.92),
        ("Dense Only\n(384, bge, dense, k5)",   0.600, 1.000, 0.750, 0.92),
        ("Sparse Only\n(384, bge, sparse, k5)", 0.225, 0.750, 0.283, 0.92),
        ("Reranker\n(384, bge, hybrid+rerank)", 0.875, 1.000, 1.000, 0.92),
        ("top_k=10\n(384, bge, hybrid, k10)",   0.450, 1.000, 0.687, 0.92),
        ("Temp 0.7\n(384, bge, hybrid, k5)",    0.825, 1.000, 0.875, 0.92),
    ]

    labels   = [e[0] for e in experiments]
    p_at_5   = [e[1] for e in experiments]
    mrr      = [e[3] for e in experiments]
    faith    = [e[4] for e in experiments]

    x = np.arange(len(labels))
    width = 0.28

    fig, ax = plt.subplots(figsize=(16, 7))
    b1 = ax.bar(x - width, p_at_5, width, label="Precision@5", color=BLUE,   zorder=3)
    b2 = ax.bar(x,          mrr,    width, label="MRR@5",       color=ORANGE, zorder=3)
    b3 = ax.bar(x + width,  faith,  width, label="Faithfulness",color=GREEN,  zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8, rotation=15, ha="right")
    ax.set_ylim(0, 1.2)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Hyperparameter Experiment Comparison — Key Metrics", fontsize=14, fontweight="bold", pad=16)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out = PLOTS_DIR / "hyperparameter_comparison.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out.relative_to(ROOT_DIR)}")


# ── 3. Out-of-scope Guardrail Success Rate ────────────────────────────────────
def plot_guardrail_success():
    labels = ["Correctly\nRejected\n(5/5)", "Incorrectly\nAnswered\n(0/5)"]
    sizes  = [5, 0]  # 5 OOS correctly rejected, 0 leaked
    # Handle zero-slice pie
    fig, ax = plt.subplots(figsize=(6, 6))
    wedge_props = dict(width=0.5, edgecolor="white")
    if sizes[1] == 0:
        ax.pie([1], colors=[GREEN], wedgeprops=wedge_props, startangle=90)
        ax.text(0, 0, "5/5\n100%", ha="center", va="center", fontsize=20,
                fontweight="bold", color="white")
    else:
        ax.pie(sizes, labels=labels, colors=[GREEN, RED],
               autopct="%1.0f%%", startangle=90, wedgeprops=wedge_props)

    ax.set_title("Out-of-Scope Guardrail — Success Rate\n(5 test cases, 100% correctly rejected)",
                 fontsize=12, fontweight="bold", pad=16)
    plt.tight_layout()
    out = PLOTS_DIR / "guardrail_success_rate.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out.relative_to(ROOT_DIR)}")


# ── 4. Quiz Evaluation Metrics ────────────────────────────────────────────────
def plot_quiz_metrics():
    criteria   = ["Tests Topic", "Answerable\nFrom Context", "Exactly One\nCorrect", "Plausible\nDistractors"]
    scores     = [1.00, 1.00, 1.00, 0.80]
    colors_bar = [GREEN if s >= 0.8 else ORANGE for s in scores]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(criteria, scores, color=colors_bar, edgecolor="white", linewidth=0.8, zorder=3)
    for bar, val in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                f"{val:.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")

    ax.set_ylim(0, 1.2)
    ax.set_ylabel("LLM-Judge Score (0.0 – 1.0)", fontsize=12)
    ax.set_title("Personalized Quiz Quality — LLM-as-a-Judge Scores", fontsize=13, fontweight="bold", pad=14)
    ax.axhline(0.8, color="gray", linewidth=0.8, linestyle="--", label="0.8 threshold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out = PLOTS_DIR / "quiz_evaluation_metrics.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    print("Generating Milestone 5 visualizations...")
    plot_golden_dataset_metrics()
    plot_hyperparameter_comparison()
    plot_guardrail_success()
    plot_quiz_metrics()
    print("\nAll plots saved to plots/")
