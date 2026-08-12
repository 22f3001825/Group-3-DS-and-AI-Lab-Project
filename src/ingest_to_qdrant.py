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
try:
    from src.config import course_collection_name
except ModuleNotFoundError:  # run as `python src/<name>.py`, so src/ is sys.path[0]
    from config import course_collection_name

COLLECTION_NAME = course_collection_name()

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


def ensure_payload_indexes(client) -> list[str]:
    """Create the keyword payload indexes the filtered read paths need.

    Called at the end of `main()` rather than left as a manual step, because this script
    recreates the collection from scratch — a re-ingest that forgot them would silently
    break two features at once:

    - `metadata.source_type` backs the Socratic transcript-only retriever. Qdrant answers
      400 on a filtered search over an unindexed field, and the caller sees an exception
      rather than an empty result — so the layer fails *open* if this is missing, which is
      why it is created here and asserted in verification.
    - `metadata.doc_id` backs `quiz_service._fetch_chunks_by_doc_id` (hard-tier context
      widening) and the `replace=true` delete in the admin ingest path. The former
      degrades silently without it; the latter refuses to run.

    Returns the fields it created. Idempotent: an existing index is left alone.
    """
    from qdrant_client import models as qmodels

    created: list[str] = []
    try:
        schema = client.get_collection(COLLECTION_NAME).payload_schema or {}
    except Exception as exc:  # noqa: BLE001
        print(f"  [Index] Could not read payload schema ({type(exc).__name__}) — skipping.")
        return created

    for field in ("metadata.source_type", "metadata.doc_id"):
        if field in schema:
            print(f"  [Index] {field} already indexed.")
            continue
        try:
            client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field,
                field_schema=qmodels.PayloadSchemaType.KEYWORD,
            )
            created.append(field)
            print(f"  [Index] Created keyword index on {field}.")
        except Exception as exc:  # noqa: BLE001
            print(f"  [Index] FAILED to create {field}: {type(exc).__name__}: {exc}")
    return created


def main(force: bool = False, collection: str | None = None):
    """Ingest `data/splits/` into `collection`, recreating it.

    `collection` defaults to whatever `QDRANT_COLLECTION` says is live. Passing a
    *different* name is the non-destructive path: the new collection is built and indexed
    alongside the running one, nothing is deleted, and the cutover is a `.env` edit plus a
    restart — with the previous collection still sitting there as the rollback.
    """
    global COLLECTION_NAME
    if collection:
        COLLECTION_NAME = collection

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

    print("\nEnsuring payload indexes...")
    ensure_payload_indexes(qdrant.client)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest data/splits/ into Qdrant.")
    parser.add_argument("--force", action="store_true",
                        help="ingest even if admin documents are unexported")
    parser.add_argument("--collection", default=None,
                        help="target collection (default: $QDRANT_COLLECTION, else "
                             "mlt_course_bot). Give a NEW name to build alongside the "
                             "live one instead of replacing it.")
    args = parser.parse_args()
    main(force=args.force, collection=args.collection)
