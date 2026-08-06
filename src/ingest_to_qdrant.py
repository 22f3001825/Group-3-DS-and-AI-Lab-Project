"""
ingest_to_qdrant.py
Ingests processed JSON-L chunks into Qdrant Cloud.
Uses FastEmbed for Dense (BGE-small) and Sparse (BM25) vector generation.
"""

import os
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

# Load environment variables (API Key and URL)
load_dotenv()


def normalize_qdrant_url(url: str) -> str:
    """Normalize common Qdrant URLs to the API endpoint form."""
    cleaned = url.strip()
    if not cleaned:
        return ""

    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        if "/collections" in cleaned:
            cleaned = cleaned.split("/collections")[0]
        if cleaned.endswith("/api"):
            cleaned = cleaned[:-4]
        if cleaned.endswith("/v1"):
            cleaned = cleaned[:-3]
        if cleaned.endswith("/dashboard"):
            cleaned = cleaned[:-10]
        if cleaned.endswith("/"):
            cleaned = cleaned[:-1]
        if "cloud.qdrant.io" in cleaned and ":6333" not in cleaned:
            cleaned = f"{cleaned}:6333"
    return cleaned

QDRANT_URL = normalize_qdrant_url(os.getenv("QDRANT_URL", ""))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL:
    raise ValueError("Missing QDRANT_URL in .env file.")

ROOT_DIR = Path(__file__).resolve().parent.parent
SPLITS_DIR = ROOT_DIR / "data" / "splits"
COLLECTION_NAME = "mlt_course_bot"

def load_chunks() -> list[Document]:
    """Loads all train, val, and test JSONL chunks into LangChain Documents."""
    documents = []
    
    for split_name in ["train_chunks.jsonl", "val_chunks.jsonl", "test_chunks.jsonl"]:
        filepath = SPLITS_DIR / split_name
        if not filepath.exists():
            print(f"Warning: {filepath} not found. Skipping.")
            continue
            
        print(f"Loading {split_name}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                doc = Document(
                    page_content=data['text'],
                    metadata=data['metadata']
                )
                documents.append(doc)
                
    print(f"Loaded a total of {len(documents)} chunks.")
    return documents

def check_unexported_documents() -> list[str]:
    """Admin-contributed documents that exist only in the database.

    This script DELETES and recreates the collection, and it ingests `data/splits/`
    only. Admin content lives in `question_documents` and its chunks were appended
    directly, so anything not exported to `data/cleaned/` (and re-split) would be
    silently dropped by this run. Returning a non-empty list is a hard stop.
    """
    try:
        from src.api.services import question_repository as repo
        from src.database.session import SessionLocal
    except Exception:  # noqa: BLE001 — a stripped-down checkout can still ingest
        return []

    try:
        with SessionLocal() as db:
            return repo.documents_missing_from_disk(db, ROOT_DIR / "data" / "cleaned")
    except Exception:  # noqa: BLE001 — no database yet is not a blocker
        return []


def main(force: bool = False):
    missing = check_unexported_documents()
    if missing and not force:
        print(f"REFUSING TO RUN: {len(missing)} admin-contributed document(s) exist only in the")
        print("database, and this script deletes and recreates the collection — they would be lost:")
        for stem in missing[:10]:
            print(f"  - {stem}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
        print("\nExport them first, then re-split:")
        print("  python src/export_question_bank.py --documents")
        print("  python src/prepare_rag_splits.py")
        print("Or re-run with --force to ingest without them.")
        return

    print("Initialize Qdrant Client...")
    client_kwargs: dict[str, Any] = {"url": QDRANT_URL}
    if QDRANT_API_KEY:
        client_kwargs["api_key"] = QDRANT_API_KEY

    client = QdrantClient(**client_kwargs)

    try:
        collections = client.get_collections().collections
    except UnexpectedResponse as exc:
        print(f"Unable to reach Qdrant at {QDRANT_URL}: {exc}")
        print("Please verify that the URL is correct and that the server is running.")
        print("If you are using local Qdrant, try http://localhost:6333")
        return

    # Check if collection exists; if so, recreate it for a fresh ingestion
    if any(c.name == COLLECTION_NAME for c in collections):
        print(f"Collection '{COLLECTION_NAME}' already exists. Recreating it...")
        client.delete_collection(COLLECTION_NAME)
        
    print("Loading embedding models (this may download weights on first run)...")
    dense_embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
    
    print("Loading chunks from disk...")
    docs = load_chunks()
    
    if not docs:
        print("No chunks to ingest! Exiting.")
        return

    print("Connecting to Qdrant Cloud and generating embeddings...")
    print("This will take a few minutes as it vectorizes all 4,600+ chunks locally before uploading.")
    
    # LangChain's QdrantVectorStore handles the batching and upload automatically
    qdrant_kwargs: dict[str, Any] = {
        "url": QDRANT_URL,
        "collection_name": COLLECTION_NAME,
        "retrieval_mode": RetrievalMode.HYBRID,
        "timeout": 120,
        "batch_size": 32,
    }
    if QDRANT_API_KEY:
        qdrant_kwargs["api_key"] = QDRANT_API_KEY

    qdrant = QdrantVectorStore.from_documents(
        docs,
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        **qdrant_kwargs,
    )
    
    print(f"\nSuccess! {len(docs)} chunks successfully ingested into Qdrant Cloud!")

if __name__ == "__main__":
    import sys

    main(force="--force" in sys.argv)
