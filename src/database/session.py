"""
database/session.py
SQLite engine and session factory for the MLT learner profile database.
"""
import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DB lives at project root so it persists across runs.
#
# `MLT_DB_PATH` overrides that, and exists for exactly one reason: in a container the
# repo root is an image layer, so the default would put every student, quiz attempt and
# the whole question bank inside something that is thrown away on the next deploy. The
# deployment points this at a mounted volume. Unset — which is every local run — the
# path is byte-identical to what it has always been.
_DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "mlt_learner.db"
DB_PATH = Path(os.getenv("MLT_DB_PATH") or _DEFAULT_DB_PATH)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    # check_same_thread: needed for SQLite + FastAPI threads.
    # timeout: how long a writer waits on SQLite's file lock before raising
    #   "database is locked". The default is 5s, which is short once real HTTP traffic
    #   overlaps a quiz write with a recommendation read.
    connect_args={"check_same_thread": False, "timeout": 30},
    echo=False,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, _connection_record):
    """WAL so a reader never blocks the writer, and vice versa.

    Without it the single-file DB serialises every request that touches it — with one
    uvicorn worker and a threadpool underneath, that is the whole API. WAL is a property
    of the database file, not the connection, so this is set once and persists.
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
    finally:
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


def get_db():
    """FastAPI dependency that yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
