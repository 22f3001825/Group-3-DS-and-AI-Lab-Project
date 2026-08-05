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
from sqlalchemy import text

from ..database.session import Base, engine
from .routers.chat import router as chat_router
from .routers.learner import router as learner_router


def init_db():
    """Create DB tables on startup and safely add any new columns to existing tables."""
    Base.metadata.create_all(bind=engine)
    
    # Safe SQLite column migration for TopicMastery
    with engine.connect() as conn:
        try:
            res = conn.execute(text("PRAGMA table_info(topic_mastery)")).fetchall()
            existing_cols = {row[1] for row in res}
            if existing_cols:
                if "elo_rating" not in existing_cols:
                    conn.execute(text("ALTER TABLE topic_mastery ADD COLUMN elo_rating FLOAT DEFAULT 0.0"))
                if "streak" not in existing_cols:
                    conn.execute(text("ALTER TABLE topic_mastery ADD COLUMN streak INTEGER DEFAULT 0"))
                if "chat_interactions" not in existing_cols:
                    conn.execute(text("ALTER TABLE topic_mastery ADD COLUMN chat_interactions INTEGER DEFAULT 0"))
                conn.commit()
        except Exception as e:
            print(f"[Startup Warning] SQLite migration check: {e}")


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

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router)
app.include_router(learner_router)


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
