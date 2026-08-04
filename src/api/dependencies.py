"""
api/dependencies.py
Shared FastAPI dependencies — most importantly the Qdrant retriever singleton.

The retriever is created ONCE at application startup and reused across all requests,
matching the exact same setup used in run_rag.py and evaluate_rag.py.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode

load_dotenv()

COLLECTION_NAME = "mlt_course_bot"


def _normalize_url(url: str) -> str:
    cleaned = url.strip()
    if not cleaned:
        return ""
    for suffix in ("/collections", "/api", "/v1", "/dashboard"):
        if suffix in cleaned:
            cleaned = cleaned.split(suffix)[0]
    if cleaned.endswith("/"):
        cleaned = cleaned[:-1]
    if "cloud.qdrant.io" in cleaned and ":6333" not in cleaned:
        cleaned = f"{cleaned}:6333"
    return cleaned


@lru_cache(maxsize=1)
def _build_retriever() -> Any:
    """Build and cache the Qdrant retriever. Called once on first request."""
    qdrant_url = _normalize_url(os.getenv("QDRANT_URL", ""))
    qdrant_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url:
        raise RuntimeError("QDRANT_URL is not set. Add it to your .env file.")

    print("[Startup] Loading embedding models (BGE-small + BM25)...")
    dense  = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    sparse = FastEmbedSparse(model_name="Qdrant/bm25")

    print(f"[Startup] Connecting to Qdrant collection '{COLLECTION_NAME}'...")
    qdrant = QdrantVectorStore.from_existing_collection(
        embedding=dense,
        sparse_embedding=sparse,
        url=qdrant_url,
        api_key=qdrant_key,
        collection_name=COLLECTION_NAME,
        retrieval_mode=RetrievalMode.HYBRID,
    )
    retriever = qdrant.as_retriever(search_kwargs={"k": 10})
    print("[Startup] Retriever ready.")
    return retriever


def get_retriever() -> Any:
    """FastAPI Depends() dependency — returns the cached retriever."""
    return _build_retriever()
