"""
api/main.py
FastAPI application entry point for the MLT Course RAG Assistant.

Start with:
    uvicorn src.api.main:app --reload --port 8000
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..database.migrations import run_migrations
from ..database.session import Base, engine
from .routers.auth import router as auth_router
from .routers.chat import router as chat_router
from .routers.learner import router as learner_router
from .routers.questions import router as questions_router
from .services.auth_service import cors_origins


def init_db():
    """Create new tables, then apply schema migrations to existing ones.

    The hand-rolled `PRAGMA table_info` blocks that used to live here are migrations
    0001 and 0002 in `database/migrations.py`; every later column add is numbered
    alongside them, so there is one ordered, recorded path for schema change.
    """
    Base.metadata.create_all(bind=engine)
    applied = run_migrations(engine)
    if applied:
        print(f"[Startup] applied schema migrations: {', '.join(applied)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("[Startup] SQLite tables and schema ready.")
    yield
    print("[Shutdown] MLT RAG API shutting down.")


app = FastAPI(
    title="MLT Course RAG Assistant API",
    description=(
        "REST API for the IIT Madras MLT Course AI Assistant. "
        "Exposes the RAG pipeline, learner profile management, "
        "topic taxonomy, recommendations, and chat history."
    ),
    version="5.0.0",
    lifespan=lifespan,
)

# Allow the frontend — named origins, not `*`.
#
# `allow_credentials=False` is correct rather than a downgrade: the session token travels
# in an Authorization header, not a cookie, so the browser never needs to be told to send
# credentials cross-origin. Headers are enumerated for the same reason `*` went: a wildcard
# there is what let any page on the internet script this API in a logged-in user's browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Admin-Token"],
)

# Register routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(learner_router)
app.include_router(questions_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "MLT Course RAG Assistant",
        "milestone": 5,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
