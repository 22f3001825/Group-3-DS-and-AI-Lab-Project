"""
api/services/rag_service.py
Thin adapter between FastAPI and the existing RAG pipeline.

Rules:
  - answer_question() is NEVER modified.
  - This file only serializes Document objects (not JSON-serialisable by default)
    into plain dicts, and extracts topic_tags from source metadata for DB storage.
"""
from __future__ import annotations

from typing import Any

from langchain_core.documents import Document

try:
    from src.rag_pipeline import answer_question
except ModuleNotFoundError:
    from rag_pipeline import answer_question  # type: ignore


def doc_to_dict(doc: Document) -> dict[str, Any]:
    """Convert a LangChain Document to a JSON-serialisable dict."""
    return {
        "text": doc.page_content,
        "metadata": dict(doc.metadata),
    }


def extract_topics_from_sources(sources: list[Document]) -> list[str]:
    """Collect unique topic_tags from retrieved source chunks.
    Used to populate ChatMessage.topics_detected in the DB.
    """
    seen: set[str] = set()
    topics: list[str] = []
    for doc in sources:
        tags = doc.metadata.get("topic_tags", [])
        if isinstance(tags, list):
            for tag in tags:
                if tag not in seen:
                    seen.add(tag)
                    topics.append(tag)
    return topics


def run_rag(question: str, retriever: Any, top_k: int = 5) -> dict[str, Any]:
    """Call answer_question() and return a fully serialisable result dict.

    Returns:
        answer        : str
        sources       : list[dict]   (serialised Documents)
        provider_used : str
        fallback_used : bool
        topics_detected: list[str]  (for DB storage)
        raw_sources   : list[Document]  (kept for any internal use)
    """
    result = answer_question(question, retriever, top_k=top_k)

    serialised_sources = [doc_to_dict(doc) for doc in result["sources"]]
    topics = extract_topics_from_sources(result["sources"])

    return {
        "answer":          result["answer"],
        "sources":         serialised_sources,
        "provider_used":   result["provider_used"],
        "fallback_used":   result["fallback_used"],
        "topics_detected": topics,
        "raw_sources":     result["sources"],   # kept internally, not sent to client
    }


def run_retrieve_only(question: str, retriever: Any, top_k: int = 5) -> list[dict[str, Any]]:
    """Retrieve chunks without calling the LLM. Debug endpoint only."""
    docs: list[Document] = retriever.invoke(question)[:top_k]
    return [doc_to_dict(doc) for doc in docs]
