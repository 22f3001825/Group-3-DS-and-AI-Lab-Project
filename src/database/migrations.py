"""
database/migrations.py
Ordered, idempotent schema migrations for `mlt_learner.db`.

`Base.metadata.create_all()` creates NEW tables but never alters an existing one, so
every column added to a table that is already in someone's database needs a migration.
This module is the one place that happens.

Why not Alembic: it wants a version directory, an env.py and an offline/online split for
a single-file SQLite database that ships with the repo. The contract here is smaller and
matches what the codebase already did by hand — an ordered list of steps, each recorded
once in `schema_migrations`, each safe to re-run. Migrations 0001 and 0002 are the two
`PRAGMA table_info` blocks that used to live inline in `api/main.py:init_db`, moved
verbatim so an existing database sees no change in behaviour.

Rules for adding one:
  - append, never renumber or edit an applied migration;
  - make the step itself idempotent (check before you add), so a database that was
    hand-patched before this module existed converges instead of erroring;
  - additive only. SQLite cannot drop or retype a column without a table rebuild, and a
    rebuild of a live table is not something a startup hook should attempt.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine


def _table_exists(conn: Connection, table: str) -> bool:
    row = conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:t"), {"t": table}
    ).fetchone()
    return row is not None


def _columns(conn: Connection, table: str) -> set[str]:
    if not _table_exists(conn, table):
        return set()
    return {row[1] for row in conn.execute(text(f"PRAGMA table_info({table})")).fetchall()}


def _add_column(conn: Connection, table: str, column: str, ddl: str) -> None:
    """Add a column when the table exists and the column does not.

    A missing table is not an error: `create_all` will have created it with the column
    already present, which is exactly the fresh-database case.
    """
    existing = _columns(conn, table)
    if not existing or column in existing:
        return
    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))


# ── The migrations ────────────────────────────────────────────────────────────

def _m0001_topic_mastery_elo(conn: Connection) -> None:
    _add_column(conn, "topic_mastery", "elo_rating", "FLOAT DEFAULT 0.0")
    _add_column(conn, "topic_mastery", "streak", "INTEGER DEFAULT 0")
    _add_column(conn, "topic_mastery", "chat_interactions", "INTEGER DEFAULT 0")


def _m0002_quiz_attempt_generation(conn: Connection) -> None:
    _add_column(conn, "quiz_attempts", "options", "JSON")
    _add_column(conn, "quiz_attempts", "reason", "VARCHAR(32)")


def _m0003_drafts_hold_their_own_bytes(conn: Connection) -> None:
    """The draft row becomes the whole draft — no staging directory beside it."""
    _add_column(conn, "question_content_drafts", "source_blob", "BLOB")
    _add_column(conn, "question_content_drafts", "source_media_type", "VARCHAR(64)")
    _add_column(conn, "question_content_drafts", "edited_markdown", "TEXT")
    _add_column(conn, "question_content_drafts", "analysis_json", "JSON")
    _add_column(conn, "question_content_drafts", "composed_json", "JSON")


def _m0004_upload_audit_columns(conn: Connection) -> None:
    """Sortable audit columns, so the admin list does not unpack JSON to filter."""
    _add_column(conn, "question_uploads", "replaced", "BOOLEAN DEFAULT 0")
    _add_column(conn, "question_uploads", "superseded_chunks", "INTEGER DEFAULT 0")
    _add_column(conn, "question_uploads", "chars_added", "INTEGER DEFAULT 0")
    _add_column(conn, "question_uploads", "chars_removed", "INTEGER DEFAULT 0")
    _add_column(conn, "question_uploads", "document_id", "VARCHAR(36)")


def _m0005_unit_vectors_in_the_database(conn: Connection) -> None:
    """Vectors live on the unit, not in a .npy file and not only in an outbox payload."""
    _add_column(conn, "question_units", "vector", "BLOB")
    _add_column(conn, "question_units", "text_hash", "VARCHAR(64)")


def _m0006_version_vector_status(conn: Connection) -> None:
    _add_column(conn, "question_bank_versions", "vector_status", "VARCHAR(20) DEFAULT 'pending'")


def _m0007_outbox_entity_type(conn: Connection) -> None:
    """Course chunks join unit vectors in the same durable queue."""
    _add_column(conn, "question_bank_outbox", "entity_type",
                "VARCHAR(20) DEFAULT 'question_unit'")
    if _columns(conn, "question_bank_outbox"):
        conn.execute(text("UPDATE question_bank_outbox SET entity_type='question_unit' "
                          "WHERE entity_type IS NULL"))


def _m0008_documents_unique_per_active_stem(conn: Connection) -> None:
    """One ACTIVE document per stem, not one row per stem, ever.

    The first shape of `question_documents` made `stem` unique at the column level,
    which makes `replace=true` impossible: superseding keeps the old row for audit and
    its stem with it, so the replacement insert violates the constraint. SQLite cannot
    drop a column-level constraint, so the table is rebuilt — safe here because the
    replacement shipped before any deployment could hold rows, and refused outright if
    one somehow does.
    """
    if not _table_exists(conn, "question_documents"):
        return
    ddl = (conn.execute(text(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='question_documents'"
    )).scalar() or "")
    if "UNIQUE" in ddl.upper():
        rows = conn.execute(text("SELECT COUNT(*) FROM question_documents")).scalar() or 0
        if rows:
            raise RuntimeError(
                f"question_documents holds {rows} row(s) under the old unique-stem shape. "
                "Export them (python src/export_question_bank.py --documents), delete the "
                "table, and re-run so the partial unique index can be created."
            )
        from .models import QuestionDocument  # noqa: PLC0415

        conn.execute(text("DROP TABLE question_documents"))
        QuestionDocument.__table__.create(bind=conn)
        return

    conn.execute(text(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_question_documents_active_stem "
        "ON question_documents (stem) WHERE status = 'active'"
    ))


def _m0009_students_google_identity(conn: Connection) -> None:
    """Google profile claims, the admin flag, the active flag and login stats.

    The backfill is guarded rather than unconditional. `tests/test_ingest_lifecycle.py`
    builds its temp database with `create_all` and *then* runs migrations, so every
    column below already exists and `_add_column` no-ops — but a bare UPDATE would still
    run and rewrite rows the test just wrote. Snapshot the columns first and only touch
    the ones this migration genuinely added.
    """
    before = _columns(conn, "students")
    if not before:
        return  # fresh database: create_all made the table with these columns already

    _add_column(conn, "students", "given_name", "VARCHAR(255)")
    _add_column(conn, "students", "family_name", "VARCHAR(255)")
    _add_column(conn, "students", "picture_url", "VARCHAR(512)")
    _add_column(conn, "students", "email_verified", "BOOLEAN NOT NULL DEFAULT 0")
    _add_column(conn, "students", "hosted_domain", "VARCHAR(255)")
    _add_column(conn, "students", "is_admin", "BOOLEAN NOT NULL DEFAULT 0")
    _add_column(conn, "students", "is_active", "BOOLEAN NOT NULL DEFAULT 1")
    _add_column(conn, "students", "last_login_at", "DATETIME")
    _add_column(conn, "students", "login_count", "INTEGER NOT NULL DEFAULT 0")
    _add_column(conn, "students", "updated_at", "DATETIME")

    # SQLite's ADD COLUMN ... DEFAULT already fills existing rows, so this only catches a
    # database that was hand-patched with a nullable version of the same column.
    for column, value in (("email_verified", "0"), ("is_admin", "0"),
                          ("is_active", "1"), ("login_count", "0")):
        if column not in before:
            conn.execute(text(f"UPDATE students SET {column} = {value} WHERE {column} IS NULL"))


def _m0010_socratic_sessions_and_events(conn: Connection) -> None:
    """Tables for the Chrome extension's Socratic path.

    Unlike 0001-0009 these are whole tables, not columns, so on a fresh database
    `create_all` has already made them and this is a no-op. It exists for the databases
    that predate the feature, and it creates them through the SQLAlchemy models rather
    than hand-written DDL so the two definitions cannot drift.
    """
    from .models import SocraticEvent, SocraticSession  # noqa: PLC0415

    for model in (SocraticSession, SocraticEvent):
        if not _table_exists(conn, model.__tablename__):
            model.__table__.create(bind=conn)


def _m0011_app_settings(conn: Connection) -> None:
    """The runtime-settings table behind the admin LLM provider hierarchy.

    A whole table like 0010, so this is a no-op on a fresh database that `create_all`
    already served, and created from the model for the same anti-drift reason. No seed
    row: an absent `llm_provider_order` means "nobody has chosen", which the settings
    service answers from `LLM_PROVIDER` — writing a default here instead would freeze
    today's environment value into the database on upgrade.
    """
    from .models import AppSetting  # noqa: PLC0415

    if not _table_exists(conn, AppSetting.__tablename__):
        AppSetting.__table__.create(bind=conn)


MIGRATIONS: list[tuple[str, str, Callable[[Connection], None]]] = [
    ("0001", "topic_mastery: elo_rating, streak, chat_interactions", _m0001_topic_mastery_elo),
    ("0002", "quiz_attempts: options, reason", _m0002_quiz_attempt_generation),
    ("0003", "question_content_drafts: blob, edited markdown, analysis", _m0003_drafts_hold_their_own_bytes),
    ("0004", "question_uploads: audit columns", _m0004_upload_audit_columns),
    ("0005", "question_units: vector, text_hash", _m0005_unit_vectors_in_the_database),
    ("0006", "question_bank_versions: vector_status", _m0006_version_vector_status),
    ("0007", "question_bank_outbox: entity_type", _m0007_outbox_entity_type),
    ("0008", "question_documents: unique stem per ACTIVE row", _m0008_documents_unique_per_active_stem),
    ("0009", "students: google profile, admin flag, login stats", _m0009_students_google_identity),
    ("0010", "socratic_sessions + socratic_events", _m0010_socratic_sessions_and_events),
    ("0011", "app_settings: admin-set runtime settings", _m0011_app_settings),
]


# ── Runner ────────────────────────────────────────────────────────────────────

def _ensure_ledger(conn: Connection) -> None:
    conn.execute(text(
        "CREATE TABLE IF NOT EXISTS schema_migrations ("
        " migration_id VARCHAR(16) PRIMARY KEY,"
        " description TEXT,"
        " applied_at TIMESTAMP)"
    ))


def applied_migrations(conn: Connection) -> set[str]:
    _ensure_ledger(conn)
    return {row[0] for row in conn.execute(text("SELECT migration_id FROM schema_migrations")).fetchall()}


def run_migrations(engine: Engine) -> list[str]:
    """Apply every unapplied migration in order. Returns the ids applied this run.

    Each migration commits on its own. A failure is reported and stops the run rather
    than being swallowed: a half-migrated database that keeps serving is worse than a
    startup that says which step failed.
    """
    applied: list[str] = []
    with engine.connect() as conn:
        done = applied_migrations(conn)
        for migration_id, description, step in MIGRATIONS:
            if migration_id in done:
                continue
            step(conn)
            conn.execute(
                text("INSERT INTO schema_migrations (migration_id, description, applied_at) "
                     "VALUES (:i, :d, :a)"),
                {"i": migration_id, "d": description, "a": datetime.now(timezone.utc)},
            )
            conn.commit()
            applied.append(migration_id)
    return applied
