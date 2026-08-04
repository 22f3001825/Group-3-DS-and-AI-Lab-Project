"""
api/main.py
FastAPI application entry point for the MLT Course RAG Assistant (Milestone 5).

Start with:
    uvicorn src.api.main:app --reload --port 8000

Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..database.session import Base, engine
from .routers.chat import router as chat_router
from .routers.learner import router as learner_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup (safe to run repeatedly — no-op if tables exist)."""
    Base.metadata.create_all(bind=engine)
    print("[Startup] SQLite tables ready.")
    yield
    print("[Shutdown] MLT RAG API shutting down.")


app = FastAPI(
    title="MLT Course RAG Assistant API",
    description=(
        "REST API for the IIT Madras MLT Course AI Assistant. "
        "Exposes the RAG pipeline, learner profile management, "
        "topic taxonomy, and chat history."
    ),
    version="5.0.0",
    lifespan=lifespan,
)

# Allow frontend (served from any origin during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
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
