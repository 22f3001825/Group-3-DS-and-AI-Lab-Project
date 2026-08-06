"""Retry durable Question Intelligence vector operations in Qdrant."""
from __future__ import annotations

try:
    from src.api.services.question_vector_service import sync_outbox
    from src.database.session import SessionLocal
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.api.services.question_vector_service import sync_outbox
    from src.database.session import SessionLocal


if __name__ == "__main__":
    with SessionLocal() as session:
        print(sync_outbox(session, limit=10_000))
