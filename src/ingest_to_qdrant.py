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

def main():
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
    main()
