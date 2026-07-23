"""Interactive CLI for running the RAG pipeline with Qdrant-backed retrieval."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

try:
    from src.rag_pipeline import answer_question
except ModuleNotFoundError:  # pragma: no cover - fallback for direct script execution
    from rag_pipeline import answer_question


load_dotenv()


def normalize_qdrant_url(url: str) -> str:
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
COLLECTION_NAME = "mlt_course_bot"

if not QDRANT_URL:
    raise ValueError("Missing QDRANT_URL in your .env file.")

print("Loading embedding models...")
dense_embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

print("Connecting to Qdrant...")
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=dense_embeddings,
    sparse_embedding=sparse_embeddings,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name=COLLECTION_NAME,
    retrieval_mode=RetrievalMode.HYBRID,
)

retriever = qdrant.as_retriever(search_kwargs={"k": 3})

print("\nRAG assistant ready. Type 'exit' to quit.\n")
while True:
    question = input("Ask a question: ").strip()
    if not question or question.lower() in {"exit", "quit"}:
        break

    try:
        result = answer_question(question, retriever)
    except Exception as exc:  # pragma: no cover - interactive CLI fallback
        print(f"\nError: {exc}\n")
        continue

    print("\nAnswer:\n")
    print(result["answer"])
    print("\nSources:")
    for idx, doc in enumerate(result["sources"], start=1):
        week = doc.metadata.get("week", "unknown")
        source_type = doc.metadata.get("source_type", "unknown")
        print(f"{idx}. {source_type} | Week {week}")
        print(doc.page_content[:220].replace("\n", " ") + "...\n")
