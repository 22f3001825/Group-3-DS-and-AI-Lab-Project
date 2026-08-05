"""
api/services/rag_service.py
Adapter between FastAPI and the RAG pipeline with lecture timestamp & citation enrichment.
"""
from __future__ import annotations

import re
from typing import Any

from langchain_core.documents import Document

try:
    from src.rag_pipeline import answer_question
except ModuleNotFoundError:
    from rag_pipeline import answer_question  # type: ignore


def clean_lecture_title(doc_id: str, h1: str | None = None) -> str:
    """Format doc_id or h1 into a human-readable lecture title."""
    if h1 and h1.strip() and not h1.strip().lower().startswith("chunk"):
        return h1.strip()
    
    if not doc_id:
        return "Course Material"

    # Remove chunk suffixes like '_chunk_3' or '.md'
    clean = re.sub(r"(_chunk_\d+|\.docx|\.md|\.pdf)", "", doc_id, flags=re.IGNORECASE)
    clean = clean.replace("_", " ").replace("-", " ").strip()
    return clean.title() if clean else "Course Lecture"


def extract_timestamp(doc: Document) -> str | None:
    """Extract timestamp from metadata or document text."""
    # 1. Check metadata
    if doc.metadata.get("timestamp"):
        return str(doc.metadata["timestamp"]).strip()

    # 2. Check text for patterns like (Refer Slide Time: 04:22) or ### Timestamp: 04:22
    match = re.search(r"(?:Slide Time|Timestamp)[:\s]+(\d{1,2}:\d{2})", doc.page_content, re.IGNORECASE)
    if match:
        return match.group(1)

    return None


def doc_to_dict(doc: Document) -> dict[str, Any]:
    """Convert a LangChain Document to a JSON-serialisable dict with citation navigation."""
    meta = dict(doc.metadata)
    doc_id = meta.get("doc_id", "")
    h1 = meta.get("h1", "")
    week = meta.get("week")
    source_type = meta.get("source_type", "transcript")
    timestamp = extract_timestamp(doc)
    lecture_title = clean_lecture_title(doc_id, h1)

    week_str = f"Week {week}" if week is not None else "General"
    time_str = f" [{timestamp}]" if timestamp else ""
    formatted_ref = f"{week_str}: {lecture_title}{time_str}"

    enriched_meta = {
        **meta,
        "lecture_title": lecture_title,
        "timestamp": timestamp,
        "formatted_ref": formatted_ref,
        "source_type": source_type,
    }

    return {
        "text": doc.page_content,
        "metadata": enriched_meta,
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


def run_rag(
    question: str,
    retriever: Any,
    top_k: int = 5,
    history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Call answer_question() and return a fully serialisable result dict.

    Args:
        history: recent {'role', 'content'} turns, oldest first. Trimmed and condensed by
                 `rag_pipeline.format_history`; affects the prompt only, not retrieval.

    Returns:
        answer        : str
        sources       : list[dict]   (serialised Documents with enriched metadata)
        provider_used : str
        fallback_used : bool
        topics_detected: list[str]  (for DB storage)
        raw_sources   : list[Document]
    """
    result = answer_question(question, retriever, top_k=top_k, history=history)

    serialised_sources = [doc_to_dict(doc) for doc in result["sources"]]
    topics = extract_topics_from_sources(result["sources"])

    return {
        "answer":          result["answer"],
        "sources":         serialised_sources,
        "provider_used":   result["provider_used"],
        "fallback_used":   result["fallback_used"],
        "topics_detected": topics,
        "raw_sources":     result["sources"],
    }


def run_retrieve_only(question: str, retriever: Any, top_k: int = 5) -> list[dict[str, Any]]:
    """Retrieve chunks without calling the LLM. Debug endpoint only."""
    docs: list[Document] = retriever.invoke(question)[:top_k]
    return [doc_to_dict(doc) for doc in docs]
