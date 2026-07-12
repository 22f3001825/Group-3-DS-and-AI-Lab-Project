"""
ingest_to_qdrant.py
Ingests processed JSON-L chunks into Qdrant Cloud.
Uses FastEmbed for Dense (BGE-small) and Sparse (BM25) vector generation.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from qdrant_client import QdrantClient

# Load environment variables (API Key and URL)
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Missing QDRANT_URL or QDRANT_API_KEY in .env file.")

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
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    
    # Check if collection exists; if so, recreate it for a fresh ingestion
    collections = client.get_collections().collections
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
    qdrant = QdrantVectorStore.from_documents(
        docs,
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME,
        retrieval_mode=RetrievalMode.HYBRID
    )
    
    print(f"\nSuccess! {len(docs)} chunks successfully ingested into Qdrant Cloud!")

if __name__ == "__main__":
    main()
