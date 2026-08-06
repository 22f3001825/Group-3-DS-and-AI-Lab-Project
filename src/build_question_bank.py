"""
build_question_bank.py
Builds the AI Question Intelligence repository (Milestone 1, Objective 8).

Run from the repo root, matching every other script's path convention:

    python src/build_question_bank.py                 # parse → embed (or reuse cache) → build → store
    python src/build_question_bank.py --refresh       # force re-embed, ignoring the cache
    python src/build_question_bank.py --thresholds    # print the per-source sweep, write nothing
    python src/build_question_bank.py --ensure-index  # create the metadata.doc_id payload index
    python src/build_question_bank.py --skip-sync     # build, but leave vectors queued

The live Qdrant collection is never read, rewritten or re-embedded here. `--ensure-index`
is the one subcommand that touches Qdrant at all, and it touches *schema* rather than
data: it adds a keyword index over existing payloads without modifying, re-embedding or
reordering a single point. It lives here rather than in the API so that creating an index
is a deliberate operator action rather than something a request handler does on the fly.

Writes:
  the database  — a new active `question_bank_versions` row with its units, groups,
                  clusters, chunk links, embeddings and queued Qdrant work
  reports/question_intelligence_report.md the build report

No data artifact is written. The bank JSON and `unit_vectors.npy` this script used to
produce are gone: units and their vectors live in `question_units`, and the embedding
cache they doubled as is now keyed by `text_hash` in the same table. Use
`python src/export_question_bank.py` if a portable copy is wanted.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    from src import question_intelligence as qi
    from src.config import (
        QI_ASKED_SOURCE_TYPES, QI_CLUSTER_DISTANCE, QI_DUPLICATE_THRESHOLD,
        QI_MIN_COMMON_DOUBT_SIZE, QI_SOURCE_TYPES, QI_TOKEN_GUARD,
    )
except ModuleNotFoundError:  # pragma: no cover - import shim
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import question_intelligence as qi
    from src.config import (
        QI_ASKED_SOURCE_TYPES, QI_CLUSTER_DISTANCE, QI_DUPLICATE_THRESHOLD,
        QI_MIN_COMMON_DOUBT_SIZE, QI_SOURCE_TYPES, QI_TOKEN_GUARD,
    )

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT_DIR / "reports" / "question_intelligence_report.md"
COLLECTION_NAME = "mlt_course_bot"


# ── Embedding cache ───────────────────────────────────────────────────────────

def embed_with_cache(db, units: list[dict], refresh: bool) -> np.ndarray:
    """Embed, reusing vectors already stored for identical text.

    The cache is `question_units.vector`, keyed by `text_hash` (the model plus the exact
    text embedded) — the same rows the API serves from, rather than a `.npy` beside
    them. A few hundred units is seconds, but a rebuild during threshold calibration
    happens often enough that paying it every time is needless.
    """
    from src.api.services.question_repository import cached_vectors, embedding_cache_stats

    if not refresh:
        counts = embedding_cache_stats(db, units)
        print(f"[embed] {counts['cached']} of {counts['units']} units cached; "
              f"embedding {counts['to_embed']} with {qi.EMBED_MODEL} ...")
    else:
        print(f"[embed] re-embedding all {len(units)} units with {qi.EMBED_MODEL} ...")
    return cached_vectors(db, units, refresh=refresh)


# ── Qdrant payload index ──────────────────────────────────────────────────────

def ensure_payload_index() -> int:
    """Create the keyword payload index on metadata.doc_id. Idempotent.

    `replace=true` on the admin commit path deletes superseded points with a filter on
    metadata.doc_id, and that filter does not work on the live collection today —
    quiz_service already documents Qdrant answering 400 and silently skipping context
    widening because of it. A delete cannot silently skip, so this is a hard
    prerequisite. Creating it also turns the quiz generator's hard-tier widening back on.
    """
    from dotenv import load_dotenv
    from qdrant_client import QdrantClient
    from src.api.dependencies import _normalize_url

    load_dotenv()
    url = _normalize_url(os.getenv("QDRANT_URL", ""))
    if not url:
        print("QDRANT_URL is not set. Add it to your .env file.")
        return 1

    client = QdrantClient(url=url, api_key=os.getenv("QDRANT_API_KEY"))
    schema = client.get_collection(COLLECTION_NAME).payload_schema or {}
    if "metadata.doc_id" in schema:
        print(f"[index] metadata.doc_id already indexed ({schema['metadata.doc_id']}). Nothing to do.")
        return 0

    print(f"[index] creating keyword payload index on metadata.doc_id in '{COLLECTION_NAME}' ...")
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.doc_id",
        field_schema="keyword",
    )
    schema = client.get_collection(COLLECTION_NAME).payload_schema or {}
    ok = "metadata.doc_id" in schema
    print("[index] done." if ok else "[index] index not visible after creation — check Qdrant.")
    return 0 if ok else 1


# ── Report ────────────────────────────────────────────────────────────────────

def write_report(bank: dict, warnings: list[str]) -> None:
    stats = bank["stats"]
    clusters = sorted(bank["clusters"], key=lambda c: (-c["asked_count"], -c["member_count"]))
    unit_by_id = {u["unit_id"]: u for u in bank["units"]}

    lines = [
        "# Question Intelligence — Build Report",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        f"schema v{bank['schema_version']} · embeddings `{bank['embed_model']}`_",
        "",
        "## Thresholds",
        "",
        f"- `QI_DUPLICATE_THRESHOLD` = {bank['thresholds']['duplicate_threshold']} (cosine similarity)",
        f"- Discriminative-token guard: **{'on' if bank['thresholds'].get('token_guard') else 'off'}** "
        "(duplicates must also agree on numerals and polarity words)",
        f"- `QI_CLUSTER_DISTANCE` = {bank['thresholds']['cluster_distance']} (cosine distance, average linkage)",
        "",
        "## Corpus",
        "",
        "| Metric | Value |",
        "|---|--:|",
        f"| Question units parsed | {stats['unit_count']} |",
        f"| Distinct doubts (canonicals) | {stats['canonical_count']} |",
        f"| Units folded into a duplicate group | {stats['duplicate_count']} |",
        f"| Duplicate rate | {stats['duplicate_rate']:.1%} |",
        f"| Clusters | {stats['cluster_count']} |",
        f"| Clusters fit to display | {stats['displayable_clusters']} |",
        f"| Singleton clusters | {stats['singleton_clusters']} |",
        f"| Admin-authored units | {stats['admin_authored_units']} |",
        "",
        "### By source type",
        "",
        "| Source | Units | Canonicals | Duplicate rate |",
        "|---|--:|--:|--:|",
    ]
    for source, entry in sorted(stats["by_source"].items()):
        rate = 1 - (entry["canonical"] / entry["units"]) if entry["units"] else 0.0
        lines.append(f"| `{source}` | {entry['units']} | {entry['canonical']} | {rate:.1%} |")

    lines += [
        "",
        "## Most common doubts",
        "",
        "Ranked by **`asked_count`** — how many times a doubt was asked — not by",
        "`canonical_count`. Deduplication is exactly what collapses the repetition this",
        "ranking is trying to surface, so ranking by distinct doubts would invert it.",
        "",
        f"`asked_count` counts members from {', '.join(f'`{s}`' for s in QI_ASKED_SOURCE_TYPES)} "
        "only. `PYQ` is excluded because its unit boundaries come from the OCR's",
        "`[Extracted Question]` markers rather than from the printed paper: one question",
        "routinely yields eight units, and ranking on `member_count` put that scan at the",
        "top of \"most asked\" with nobody having asked it.",
        "",
        f"Clusters shown have `asked_count` ≥ {QI_MIN_COMMON_DOUBT_SIZE}.",
        "",
        "| # | Cluster | Asked | Members | Distinct | Weeks | Sources |",
        "|--:|---|--:|--:|--:|---|---|",
    ]
    ranked = [c for c in clusters if c["asked_count"] >= QI_MIN_COMMON_DOUBT_SIZE][:10]
    for rank, cluster in enumerate(ranked, start=1):
        title = cluster["title"].replace("|", "\\|")[:80]
        weeks = ", ".join(str(w) for w in cluster["weeks"])
        sources = ", ".join(f"`{s}`" for s in cluster["sources"])
        lines.append(
            f"| {rank} | {title} | {cluster['asked_count']} | {cluster['member_count']} | "
            f"{cluster['canonical_count']} | {weeks} | {sources} |"
        )
    if not ranked:
        lines.append("| — | _no cluster reached the minimum asked count_ | | | | | |")

    lines += [
        "",
        "## Limitations",
        "",
        "These are properties of the approach, not oversights, and the numbers above should",
        "be read with them in mind.",
        "",
        "- **Concept tagging is week-granular for the existing corpus.** `topic_tags` are",
        "  assigned per week, so clusters are labelled from the parsed question text rather",
        "  than mapped to taxonomy IDs. Content added through the admin path can carry",
        "  explicit topic IDs; "
        f"{stats['admin_authored_units']} of {stats['unit_count']} units currently do.",
        "- **PYQ text is OCR output and only partly usable.** Question boundaries are not",
        "  recoverable, so each extracted block is one unit. Its recurring scaffolding is",
        "  stripped before embedding — left in, it is identical across documents and would",
        "  make unrelated PYQ questions score as near-duplicates.",
        "- **The forum input is absent, not merely stale.** `data/cleaned/discourse/` is an",
        "  empty directory and no chunk in any split carries `source_type == \"discourse\"`,",
        "  so every number here covers a narrower corpus than Milestone 1 §2.2.8 describes.",
        "  A TA can paste a thread in through the admin path; there is no scraper.",
    ]
    if warnings:
        lines += ["", "## Warnings", ""]
        lines += [f"- {w}" for w in warnings]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Threshold sweep printing ──────────────────────────────────────────────────

def print_thresholds(units: list[dict], vectors: np.ndarray) -> None:
    from collections import Counter

    counts = Counter(u["source_type"] for u in units)
    print("\n-- Parsed unit counts (check these before trusting any metric) --")
    for source, count in sorted(counts.items()):
        with_options = sum(1 for u in units if u["source_type"] == source and u["options"])
        with_answer = sum(1 for u in units if u["source_type"] == source and u["answer"])
        print(f"  {source:<10} {count:>4} units   ({with_options} with options, {with_answer} with an answer)")
    print(f"  {'TOTAL':<10} {len(units):>4}")

    report = qi.describe_thresholds(vectors, units)
    for source, entry in report.items():
        label = "POOLED" if source == "__pooled__" else source
        sim = entry["similarity"]
        print(f"\n-- {label}: {entry['n_units']} units, {entry['n_pairs']} pairs --")
        print(f"  cosine  mean={sim['mean']}  p50={sim['p50']}  p90={sim['p90']}  "
              f"p99={sim['p99']}  max={sim['max']}")
        print("  thresh   edges  groups  grouped  largest")
        for row in entry["sweep"]:
            print(f"  {row['threshold']:<7} {row['edges']:>6} {row['groups']:>7} "
                  f"{row['grouped_units']:>8} {row['largest_group']:>8}")
    print("\nSet QI_DUPLICATE_THRESHOLD in src/config.py from these curves, per source if they")
    print("disagree. A PYQ column that is uniformly high means the boilerplate strip missed")
    print("something - check src/question_intelligence.py:strip_pyq_boilerplate.")

    print("\n-- Cluster distance cut (average linkage over canonicals) --")
    print("  cut    clusters  singletons  largest  second  median")
    for row in qi.describe_cluster_distances(vectors, units, QI_DUPLICATE_THRESHOLD):
        print(f"  {row['cut']:<6} {row['clusters']:>8} {row['singletons']:>11} "
              f"{row['largest']:>8} {row['second']:>7} {row['median']:>7}")
    print("\nWatch 'largest': average linkage chains, so one step past the usable cut it grows")
    print("explosively and the biggest cluster becomes a topic blob spanning every week rather")
    print("than a group of related doubts. Pick the largest cut before that happens.\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Build the question intelligence bank.")
    parser.add_argument("--refresh", action="store_true", help="force re-parse and re-embed")
    parser.add_argument("--thresholds", action="store_true", help="print the per-source sweep, write nothing")
    parser.add_argument("--ensure-index", action="store_true", help="create the metadata.doc_id payload index")
    parser.add_argument("--skip-sync", action="store_true",
                        help="leave the new vectors queued in the outbox instead of pushing them")
    parser.add_argument("--duplicate-threshold", type=float, default=None,
                        help="override the per-source thresholds with one value")
    parser.add_argument("--cluster-distance", type=float, default=QI_CLUSTER_DISTANCE)
    args = parser.parse_args()

    if args.ensure_index:
        return ensure_payload_index()

    # Runtime persistence is relational, so the build needs a session from the start:
    # the embedding cache lives in `question_units`, and admin-contributed documents are
    # rows rather than files. Opening it here keeps a CLI build and an API rebuild
    # reading exactly the same two inputs.
    from src.api.services.question_repository import (  # noqa: PLC0415
        document_chunk_index, document_units_input, persist_bank,
    )
    from src.api.services.question_vector_service import sync_outbox  # noqa: PLC0415
    from src.database.migrations import run_migrations  # noqa: PLC0415
    from src.database.session import Base, SessionLocal, engine  # noqa: PLC0415

    Base.metadata.create_all(bind=engine)
    run_migrations(engine)

    with SessionLocal() as db:
        documents = document_units_input(db)
        print(f"[parse] reading {', '.join(QI_SOURCE_TYPES)} from {qi.CLEANED_DIR} "
              f"plus {len(documents)} stored documents ...")
        units = qi.parse_question_units(source_types=QI_SOURCE_TYPES, extra_documents=documents)
        if not units:
            print("No question units parsed. Check data/cleaned/ — nothing to build.")
            return 1
        print(f"[parse] {len(units)} question units")

        vectors = embed_with_cache(db, units, refresh=args.refresh)

        if args.thresholds:
            print_thresholds(units, vectors)
            return 0

        print("[map] linking units to retrieval chunks ...")
        chunks = qi.load_chunk_index() + document_chunk_index(db)
        qi.map_units_to_chunks(units, chunks)
        warnings = qi.assert_unit_index_sane(units, chunks)
        for warning in warnings:
            print(f"[warn] {warning}")

        threshold = args.duplicate_threshold if args.duplicate_threshold is not None else QI_DUPLICATE_THRESHOLD
        print(f"[build] deduplicating at {threshold} and clustering at {args.cluster_distance} ...")
        bank = qi.build_bank(
            units, vectors,
            duplicate_threshold=threshold,
            cluster_distance=args.cluster_distance,
            use_token_guard=QI_TOKEN_GUARD,
        )
        version = persist_bank(db, bank, vectors)
        db.commit()
        sync = sync_outbox(db, limit=10_000) if not args.skip_sync else {"synced": 0, "failed": 0}

    write_report(bank, warnings)

    stats = bank["stats"]
    print(f"[done] {stats['unit_count']} units -> {stats['canonical_count']} distinct doubts "
          f"-> {stats['cluster_count']} clusters (duplicate rate {stats['duplicate_rate']:.1%})")
    print(f"       database version {version.version_id}")
    print(f"       vectors: {sync['synced']} synced, {sync['failed']} failed "
          f"(retry: python src/sync_question_vectors.py)")
    print(f"       {REPORT_PATH.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
