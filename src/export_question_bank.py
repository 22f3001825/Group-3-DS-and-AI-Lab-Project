"""
export_question_bank.py
Write the database-backed question bank out as files — on request, never automatically.

Runtime persistence is relational: the API and the build CLI keep units, vectors,
drafts, uploads and contributed documents in the database, and nothing reads these
exports back except the offline pipeline. This script exists for two jobs:

    python src/export_question_bank.py --documents   # stored documents → data/cleaned/
    python src/export_question_bank.py --bank        # a portable JSON copy of the bank
    python src/export_question_bank.py --all

`--documents` is the one that matters operationally. Admin-contributed content no longer
lands in `data/cleaned/`, so an offline `prepare_rag_splits.py` + `ingest_to_qdrant.py`
run — which DELETES and recreates the collection — would drop every contribution that is
not in the tree. Exporting first puts them back, frontmatter and all, so the rebuilt
collection carries them with their asserted topic tags. `ingest_to_qdrant.py` refuses to
run while any active document is unexported, so this is a checked prerequisite rather
than a remembered one.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

try:
    from src import question_intelligence as qi
    from src.api.services import question_repository as repo
    from src.database.session import SessionLocal
    from src.prepare_rag_splits import render_frontmatter
except ModuleNotFoundError:  # pragma: no cover - import shim
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import question_intelligence as qi
    from src.api.services import question_repository as repo
    from src.database.session import SessionLocal
    from src.prepare_rag_splits import render_frontmatter

ROOT_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = ROOT_DIR / "data" / "cleaned"


def export_documents(db, dry_run: bool = False) -> list[Path]:
    """Write every active document to data/cleaned/<source_type>/<stem>.md."""
    written: list[Path] = []
    for row in repo.active_documents(db):
        target = CLEANED_DIR / row.source_type / f"{row.stem}.md"
        front = render_frontmatter(dict(row.frontmatter or {}))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(front + row.markdown, encoding="utf-8")
        written.append(target)
    return written


def export_bank(db, dry_run: bool = False) -> tuple[int, int]:
    """Write a portable JSON + vectors copy of the active bank version."""
    version = repo.require_active_version(db)
    units = repo.units_for_export(db, version)
    clusters = repo.clusters_for_export(db, version)
    payload = {
        "schema_version": qi.SCHEMA_VERSION,
        "bank_version_id": version.version_id,
        "embed_model": version.embedding_model,
        "thresholds": version.thresholds or {},
        "stats": version.source_summary or {},
        "units": units,
        "clusters": clusters,
    }
    vectors = np.vstack([
        np.frombuffer(u.pop("_vector"), dtype=np.float32) if u.get("_vector")
        else np.zeros(384, dtype=np.float32)
        for u in units
    ]) if units else np.zeros((0, 384), dtype=np.float32)

    if not dry_run:
        qi.BANK_DIR.mkdir(parents=True, exist_ok=True)
        qi.BANK_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        with open(qi.VECTORS_PATH, "wb") as handle:
            np.save(handle, vectors.astype(np.float32))
    return len(units), len(clusters)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export the database-backed question bank.")
    parser.add_argument("--documents", action="store_true", help="write stored documents to data/cleaned/")
    parser.add_argument("--bank", action="store_true", help="write a portable bank JSON + vectors")
    parser.add_argument("--all", action="store_true", help="both of the above")
    parser.add_argument("--dry-run", action="store_true", help="report what would be written")
    args = parser.parse_args()

    if not (args.documents or args.bank or args.all):
        parser.print_help()
        return 1

    with SessionLocal() as db:
        if args.documents or args.all:
            written = export_documents(db, dry_run=args.dry_run)
            verb = "would write" if args.dry_run else "wrote"
            print(f"[documents] {verb} {len(written)} file(s) under data/cleaned/")
            for path in written:
                print(f"            {path.relative_to(ROOT_DIR)}")
            if written and not args.dry_run:
                print("[documents] re-run prepare_rag_splits.py before ingest_to_qdrant.py "
                      "so the new chunks carry their asserted topic tags.")
        if args.bank or args.all:
            try:
                units, clusters = export_bank(db, dry_run=args.dry_run)
            except LookupError as exc:
                print(f"[bank] {exc}")
                return 1
            verb = "would export" if args.dry_run else "exported"
            print(f"[bank] {verb} {units} units and {clusters} clusters to "
                  f"{qi.BANK_PATH.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
