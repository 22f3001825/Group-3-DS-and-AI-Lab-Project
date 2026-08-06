"""
api/dependencies.py
Shared FastAPI dependencies — most importantly the Qdrant retriever singleton.

The retriever is created ONCE at application startup and reused across all requests,
matching the exact same setup used in run_rag.py and evaluate_rag.py.
"""
from __future__ import annotations

import os
import secrets
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from fastapi import Header, HTTPException
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
def _build_vector_store() -> Any:
    """Build and cache the Qdrant vector store. Called once on first request.

    Split out of `_build_retriever` so the admin ingest path can call `add_documents()`
    on the SAME singleton the chat path retrieves from: same dense + sparse models,
    already resident, so an uploaded document is embedded by the existing flow into the
    existing named vectors rather than by a second, parallel code path.
    """
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
    print("[Startup] Vector store ready.")
    return qdrant


@lru_cache(maxsize=1)
def _build_retriever() -> Any:
    """Build and cache the Qdrant retriever. Derived from the vector-store singleton."""
    retriever = _build_vector_store().as_retriever(search_kwargs={"k": 10})
    print("[Startup] Retriever ready.")
    return retriever


def get_retriever() -> Any:
    """FastAPI Depends() dependency — returns the cached retriever."""
    return _build_retriever()


def get_vector_store() -> Any:
    """FastAPI Depends() dependency — returns the cached vector store."""
    return _build_vector_store()


def doc_id_payload_index_state() -> bool | None:
    """Whether `metadata.doc_id` is indexed in the live collection — or None if unknown.

    `replace=true` deletes superseded points with a filter on that field, and without
    the index Qdrant answers 400. `quiz_service._fetch_chunks_by_doc_id` swallows that
    because context widening is optional; a delete cannot, so the commit path checks
    here first and returns 503 naming the flag that creates it.

    The three-way answer matters: an unreachable Qdrant is *unknown*, not *absent*, and
    a commit must not refuse with a misleading "create the index" message during an
    outage. Queued work is the right answer there.
    """
    try:
        client = _build_vector_store().client
        schema = client.get_collection(COLLECTION_NAME).payload_schema or {}
        return "metadata.doc_id" in schema
    except Exception:  # noqa: BLE001
        return None




# ── Admin access ──────────────────────────────────────────────────────────────
# There is no auth anywhere else in this system — `student_id` comes straight off the
# URL path and every /learner/* handler auto-creates students. Rather than pretend
# otherwise, admin is a single shared secret, and this docstring says so plainly.

def admin_token_configured() -> bool:
    return bool((os.getenv("ADMIN_TOKEN") or "").strip())


def require_admin(x_admin_token: str = Header(default="")) -> str:
    """Gate every admin endpoint on a shared secret from `.env`.

    An UNCONFIGURED deployment is closed, not wide open: with `ADMIN_TOKEN` unset this
    returns 503 rather than allowing the request. That covers the whole admin surface
    including draft creation, not just the commit — an unauthenticated extract would let
    anyone burn OCR minutes and fill the staging directory.

    A staging record carries no per-admin identity; the shared secret is the whole
    model, so any admin can review, edit or discard any pending draft.
    """
    configured = (os.getenv("ADMIN_TOKEN") or "").strip()
    if not configured:
        raise HTTPException(
            status_code=503,
            detail="Admin features are disabled: set ADMIN_TOKEN in .env and restart the API.",
        )
    if not secrets.compare_digest(x_admin_token or "", configured):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Admin-Token header.")
    return configured
