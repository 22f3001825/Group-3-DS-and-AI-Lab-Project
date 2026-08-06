"""Import a legacy file-backed question bank into the database-backed store.

LEGACY PATH. Nothing in the running system produces `data/question_bank/` any more —
builds write a database version, and `export_question_bank.py` is how a portable copy
is made. This script exists for a checkout that still has the old artifact, and for
`--verify`, which compares such an artifact against what the database now holds.

Usage:
    python src/migrate_question_bank_to_db.py
    python src/migrate_question_bank_to_db.py --sync-vectors
    python src/migrate_question_bank_to_db.py --replace
    python src/migrate_question_bank_to_db.py --verify
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from src import question_intelligence as qi
    from src.api.services.question_repository import persist_bank
    from src.api.services.question_vector_service import sync_outbox
    from src.database.models import (
        QuestionContentDraft, QuestionEvaluationLabel, QuestionUpload,
    )
    from src.database.session import Base, SessionLocal, engine
except ModuleNotFoundError:  # direct `python src/...py`
    import sys
    ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(ROOT))
    from src import question_intelligence as qi
    from src.api.services.question_repository import persist_bank
    from src.api.services.question_vector_service import sync_outbox
    from src.database.models import (
        QuestionContentDraft, QuestionEvaluationLabel, QuestionUpload,
    )
    from src.database.session import Base, SessionLocal, engine


def _load_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _import_labels(db) -> int:
    labels = _load_json(qi.BANK_DIR / "dedup_seed_labels.json", {})
    imported = 0
    for pair_key, label in labels.items():
        if db.get(QuestionEvaluationLabel, pair_key):
            continue
        db.add(QuestionEvaluationLabel(
            pair_key=pair_key,
            metric_kind=label.get("kind", "duplicate"),
            label=bool(label.get("label")), source=label.get("source", "legacy"),
            note=label.get("note"),
        ))
        imported += 1
    return imported


def _import_uploads(db) -> int:
    entries = _load_json(qi.BANK_DIR / "uploads.json", [])
    imported = 0
    for entry in entries if isinstance(entries, list) else []:
        draft_id = str(entry.get("draft_id") or entry.get("upload_id") or "")
        if not draft_id or db.query(QuestionUpload).filter(QuestionUpload.draft_id == draft_id).first():
            continue
        if not db.get(QuestionContentDraft, draft_id):
            db.add(QuestionContentDraft(
                draft_id=draft_id, origin=entry.get("origin", "legacy"), status="committed",
                filename=entry.get("filename"), original_markdown="", metadata_json=entry.get("resolved_metadata", {}),
                preview_json={}, committed_at=None,
            ))
            db.flush()
        db.add(QuestionUpload(
            draft_id=draft_id, resolved_metadata=entry.get("resolved_metadata", {}), result_json=entry,
        ))
        imported += 1
    return imported


def _verify(db, bank: dict) -> int:
    """Compare a legacy artifact against the active database bank.

    Parity, checked rather than assumed: unit/canonical/duplicate/cluster counts and
    per-cluster membership. Reports every mismatch instead of stopping at the first.
    """
    from src.api.services.question_repository import load_bank_for_evaluation

    try:
        live, _ = load_bank_for_evaluation(db)
    except LookupError as exc:
        print(f"[verify] {exc}")
        return 1

    problems: list[str] = []
    file_units = {u["unit_id"] for u in bank.get("units", [])}
    live_units = {u["unit_id"] for u in live["units"]}
    if file_units != live_units:
        only_file = sorted(file_units - live_units)[:5]
        only_db = sorted(live_units - file_units)[:5]
        problems.append(f"unit sets differ: {len(file_units)} in file, {len(live_units)} in db "
                        f"(file-only e.g. {only_file}; db-only e.g. {only_db})")

    def canonical(units):
        return {u["unit_id"] for u in units if u.get("is_canonical")}

    if canonical(bank.get("units", [])) != canonical(live["units"]):
        problems.append("canonical members differ")

    def membership(clusters):
        return sorted(sorted(c.get("member_unit_ids", [])) for c in clusters)

    if membership(bank.get("clusters", [])) != membership(live["clusters"]):
        problems.append(f"cluster membership differs: {len(bank.get('clusters', []))} clusters in "
                        f"file, {len(live['clusters'])} in db")

    for problem in problems:
        print(f"[verify] MISMATCH: {problem}")
    if not problems:
        print(f"[verify] parity holds: {len(live_units)} units, {len(live['clusters'])} clusters.")
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate the legacy question-bank files to SQLite/PostgreSQL.")
    parser.add_argument("--sync-vectors", action="store_true", help="also drain the Qdrant outbox")
    parser.add_argument("--replace", action="store_true", help="create a new active DB bank version even if one exists")
    parser.add_argument("--dry-run", action="store_true", help="validate inputs and print counts without writing")
    parser.add_argument("--verify", action="store_true",
                        help="compare the legacy artifact with the active database bank and exit")
    args = parser.parse_args()

    if not qi.BANK_PATH.exists():
        print(f"No legacy bank artifact at {qi.BANK_PATH}.")
        print("Builds are database-backed now: `python src/build_question_bank.py` writes a "
              "version, and `python src/export_question_bank.py --bank` writes this file.")
        return 1
    bank, vectors = qi.load_bank()
    print(f"[read] {len(bank.get('units', []))} units, {len(bank.get('clusters', []))} clusters")

    if args.verify:
        with SessionLocal() as db:
            return _verify(db, bank)

    if args.dry_run:
        print(f"[dry-run] {len(vectors)} vectors would be queued for Qdrant.")
        return 0

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        from src.api.services.question_repository import active_version
        if active_version(db) and not args.replace:
            print("An active database-backed bank already exists. Use --replace to import a new version.")
            return 0
        version = persist_bank(db, bank, vectors)
        labels = _import_labels(db)
        uploads = _import_uploads(db)
        db.commit()
        print(f"[done] imported version {version.version_id}; queued {len(bank.get('units', []))} Qdrant upserts")
        print(f"       imported {labels} evaluation labels and {uploads} upload records")
        if args.sync_vectors:
            result = sync_outbox(db)
            print(f"[qdrant] {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
