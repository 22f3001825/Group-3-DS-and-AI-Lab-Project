"""Milestone 4 — Experiment Configuration Module.

Defines every tuneable knob in the RAG pipeline as a structured
configuration so experiments are reproducible and easy to compare.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import json
from pathlib import Path


# ── Single Experiment Configuration ───────────────────────────────────────────

@dataclass
class ExperimentConfig:
    """One fully-specified RAG pipeline configuration."""

    # Identity
    name: str                            # Human-readable label, e.g. "baseline"
    description: str = ""

    # Chunking
    chunk_size: int = 384
    chunk_overlap: int = 50

    # Embedding
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dim: int = 384

    # Retrieval
    retrieval_mode: str = "hybrid"       # "dense" | "sparse" | "hybrid"
    top_k: int = 5
    use_reranker: bool = False
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    reranker_top_n: int = 5              # How many to keep after reranking
    reranker_candidate_k: int = 20       # How many to fetch before reranking

    # Generation
    temperature: float = 0.2
    prompt_style: str = "structured"     # "structured" | "concise" | "cot" | "few_shot"

    # Qdrant
    collection_name: str = ""            # Auto-generated if empty
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None

    def __post_init__(self):
        if not self.collection_name:
            # Collection name is based ONLY on parameters that affect what is
            # stored in Qdrant: chunk_size, overlap, embedding_model, retrieval_mode.
            # Parameters that only affect query-time behaviour (top_k, temperature,
            # prompt_style, use_reranker) do NOT get a new collection — they reuse
            # whichever collection has the same chunk/embed/mode settings.
            mode_short = self.retrieval_mode[:3]
            embed_short = self.embedding_model.split("/")[-1].replace("-", "")[:10]
            self.collection_name = (
                f"exp_c{self.chunk_size}_o{self.chunk_overlap}"
                f"_{embed_short}_{mode_short}"
            )

    def needs_reingestion(self, existing_collections: list[str]) -> bool:
        """Return True if this config's collection does not yet exist in Qdrant."""
        return self.collection_name not in existing_collections

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ── Experiment Result ─────────────────────────────────────────────────────────

@dataclass
class ExperimentResult:
    """Stores metrics for one completed experiment run."""

    config: ExperimentConfig
    # Retrieval metrics (averaged across eval set)
    precision_at_5: float = 0.0
    recall_at_5: float = 0.0
    mrr_at_5: float = 0.0
    recall_at_10: float = 0.0
    # Generation metrics (averaged across eval set)
    faithfulness: float = 0.0
    answer_relevance: float = 0.0
    context_precision: float = 0.0
    # Per-query details
    per_query_results: list[dict] = field(default_factory=list)
    # Meta
    total_time_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)

    def summary_dict(self) -> dict[str, Any]:
        return {
            "experiment": self.config.name,
            "config": self.config.to_dict(),
            "metrics": {
                "precision_at_5": round(self.precision_at_5, 4),
                "recall_at_5": round(self.recall_at_5, 4),
                "mrr_at_5": round(self.mrr_at_5, 4),
                "recall_at_10": round(self.recall_at_10, 4),
                "faithfulness": round(self.faithfulness, 4),
                "answer_relevance": round(self.answer_relevance, 4),
                "context_precision": round(self.context_precision, 4),
            },
            "total_time_seconds": round(self.total_time_seconds, 2),
            "errors": self.errors,
            "per_query_results": self.per_query_results,
        }


# ── Pre-defined Experiment Grid ──────────────────────────────────────────────

def get_baseline_config() -> ExperimentConfig:
    """The current production configuration (Milestone 3 settings)."""
    return ExperimentConfig(
        name="baseline",
        description="Milestone 3 default: chunk=384, bge-small, hybrid, top_k=5, temp=0.2",
        chunk_size=384,
        chunk_overlap=50,
        embedding_model="BAAI/bge-small-en-v1.5",
        embedding_dim=384,
        retrieval_mode="hybrid",
        top_k=5,
        temperature=0.2,
        prompt_style="structured",
    )


def get_experiment_grid() -> list[ExperimentConfig]:
    """Return the full Milestone 4 experiment grid.

    Organized by experiment axis so each axis is tested independently
    against the baseline, changing only one variable at a time.
    """
    baseline = get_baseline_config()
    experiments = [baseline]

    # ── Axis 1: Chunk Size ────────────────────────────────────────────────
    for cs in [256, 512, 768]:
        experiments.append(ExperimentConfig(
            name=f"chunk_{cs}",
            description=f"Chunk size = {cs} (baseline overlap=50)",
            chunk_size=cs,
            chunk_overlap=50,
        ))

    # ── Axis 2: Chunk Overlap ─────────────────────────────────────────────
    for co in [0, 100]:
        experiments.append(ExperimentConfig(
            name=f"overlap_{co}",
            description=f"Chunk overlap = {co} (baseline chunk_size=384)",
            chunk_size=384,
            chunk_overlap=co,
        ))

    # ── Axis 3: Embedding Model ──────────────────────────────────────────
    experiments.append(ExperimentConfig(
        name="embed_bge_base",
        description="Larger embedding model: bge-base (768-dim)",
        embedding_model="BAAI/bge-base-en-v1.5",
        embedding_dim=768,
    ))
    experiments.append(ExperimentConfig(
        name="embed_minilm",
        description="Alternative embedding: all-MiniLM-L6-v2 (384-dim)",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        embedding_dim=384,
    ))

    # ── Axis 4: Retrieval Mode ───────────────────────────────────────────
    experiments.append(ExperimentConfig(
        name="retrieval_dense_only",
        description="Dense-only retrieval (no BM25 sparse)",
        retrieval_mode="dense",
    ))
    experiments.append(ExperimentConfig(
        name="retrieval_sparse_only",
        description="Sparse-only retrieval (BM25 only, no semantic)",
        retrieval_mode="sparse",
    ))

    # ── Axis 5: Reranker ─────────────────────────────────────────────────
    experiments.append(ExperimentConfig(
        name="hybrid_reranker",
        description="Hybrid retrieval + cross-encoder reranker (fetch 20, keep 5)",
        use_reranker=True,
        reranker_candidate_k=20,
        reranker_top_n=5,
    ))

    # ── Axis 6: Top-K Depth ──────────────────────────────────────────────
    for k in [3, 7, 10]:
        experiments.append(ExperimentConfig(
            name=f"topk_{k}",
            description=f"top_k = {k}",
            top_k=k,
        ))

    # ── Axis 7: Temperature ──────────────────────────────────────────────
    for temp in [0.0, 0.5, 0.7]:
        experiments.append(ExperimentConfig(
            name=f"temp_{str(temp).replace('.', '_')}",
            description=f"LLM temperature = {temp}",
            temperature=temp,
        ))

    # ── Axis 8: Prompt Style ─────────────────────────────────────────────
    for style in ["concise", "cot", "few_shot"]:
        experiments.append(ExperimentConfig(
            name=f"prompt_{style}",
            description=f"Prompt style: {style}",
            prompt_style=style,
        ))

    return experiments


def get_quick_grid() -> list[ExperimentConfig]:
    """10-experiment grid covering all 6 axes for Milestone 4.

    Axis 1 — Chunking      : chunk_256, chunk_512  (vs baseline 384)
    Axis 2 — Embedding     : embed_minilm           (vs baseline bge-small)
    Axis 3 — Retrieval     : dense, sparse, reranker (vs baseline hybrid)
    Axis 4 — Top-K         : topk_10                (vs baseline 5)
    Axis 5 — Temperature   : temp_0_7               (vs baseline 0.2)
    Axis 6 — Prompt style  : prompt_cot             (vs baseline structured)

    Smart collection reuse:
      hybrid_reranker, topk_10, temp_0_7, prompt_cot all share the
      baseline collection (same chunks + embedding) → no re-ingestion.
      New ingestions needed: chunk_256, chunk_512, embed_minilm,
      retrieval_dense_only, retrieval_sparse_only (5 new collections).
    """
    return [
        # ── Reference ──────────────────────────────────────────────────────
        get_baseline_config(),

        # ── Axis 1: Chunk Size ─────────────────────────────────────────────
        ExperimentConfig(
            name="chunk_256",
            description="Smaller chunks (256 tokens) — more precise retrieval",
            chunk_size=256,
            chunk_overlap=50,
        ),
        ExperimentConfig(
            name="chunk_512",
            description="Larger chunks (512 tokens) — more context per chunk",
            chunk_size=512,
            chunk_overlap=50,
        ),

        # ── Axis 2: Embedding Model ────────────────────────────────────────
        ExperimentConfig(
            name="embed_minilm",
            description="Alternative embedding: all-MiniLM-L6-v2 (384-dim)",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            embedding_dim=384,
        ),

        # ── Axis 3: Retrieval Strategy ─────────────────────────────────────
        ExperimentConfig(
            name="retrieval_dense_only",
            description="Dense semantic search only (no BM25 keyword matching)",
            retrieval_mode="dense",
        ),
        ExperimentConfig(
            name="retrieval_sparse_only",
            description="BM25 keyword search only (no semantic/dense vectors)",
            retrieval_mode="sparse",
        ),
        ExperimentConfig(
            name="hybrid_reranker",
            description="Hybrid retrieval + cross-encoder reranker (fetch 20, keep 5)",
            retrieval_mode="hybrid",
            use_reranker=True,
            reranker_candidate_k=20,
            reranker_top_n=5,
        ),

        # ── Axis 4: Top-K Depth ────────────────────────────────────────────
        ExperimentConfig(
            name="topk_10",
            description="Retrieve top-10 chunks (more context, possibly noisier)",
            top_k=10,
        ),

        # ── Axis 5: LLM Temperature ────────────────────────────────────────
        ExperimentConfig(
            name="temp_0_7",
            description="Higher temperature (0.7) — more creative/varied answers",
            temperature=0.7,
        ),

        # ── Axis 6: Prompt Style ───────────────────────────────────────────
        ExperimentConfig(
            name="prompt_cot",
            description="Chain-of-thought prompt — LLM thinks step by step",
            prompt_style="cot",
        ),
    ]


# ── CLI preview ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Full Experiment Grid ===\n")
    for exp in get_experiment_grid():
        print(f"  {exp.name:25s} | collection: {exp.collection_name}")
    print(f"\n  Total experiments: {len(get_experiment_grid())}")

    print("\n=== Quick Grid ===\n")
    for exp in get_quick_grid():
        print(f"  {exp.name:25s} | collection: {exp.collection_name}")
    print(f"\n  Total experiments: {len(get_quick_grid())}")
