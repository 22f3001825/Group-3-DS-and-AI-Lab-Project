"""
api/services/rag_service.py
Adapter between FastAPI and the RAG pipeline with lecture timestamp & citation enrichment.
"""
from __future__ import annotations

import re
from typing import Any

from langchain_core.documents import Document
from sqlalchemy.orm import Session

from . import rerank_service
from . import scope_guard

try:
    from src.config import SCOPE_PROBE_K
    from src.rag_pipeline import answer_question
except ModuleNotFoundError:
    from config import SCOPE_PROBE_K  # type: ignore
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


# ── The scope guardrail's two callables ───────────────────────────────────────
# `scope_guard` holds the policy and takes its inputs as functions, so the policy can be
# tested with two lambdas. These are the real implementations, and they live here because
# this is the layer that already knows about the vector store.


def _embed(question: str) -> Any:
    """Unit-length query vector, in the space the chunks were embedded into."""
    from . import topic_vectors  # noqa: PLC0415

    return topic_vectors.embed_query(question)


def _nearest_topic(vector: Any) -> tuple[str | None, float]:
    """`(topic name, cosine)` for the closest of the 48 taxonomy topics.

    Shares `topic_vectors`' one embedded matrix with `socratic_service.shortlist_topics`,
    so the taxonomy is embedded once per process rather than once per feature.
    """
    from . import topic_vectors  # noqa: PLC0415

    topic, score = topic_vectors.best_topic(vector)
    return (topic or {}).get("name"), score


def _probe(vector: Any, k: int) -> list[float]:
    """Similarity of the `k` nearest chunks to `vector`, best first.

    **Dense, by vector, on purpose.** The store is built in `RetrievalMode.HYBRID`, and
    `similarity_search_with_score` on a hybrid store fuses with RRF — a rank-reciprocal
    number that barely moves between a perfect match and a nonsense query, so thresholding
    it would produce a guard that never fires. `similarity_search_with_score_by_vector`
    goes straight at the dense vector and returns the collection's actual cosine.

    Reuses the same `_build_vector_store()` singleton as retrieval, so this costs one
    Qdrant round trip and no extra model.
    """
    from ..dependencies import _build_vector_store  # noqa: PLC0415

    hits = _build_vector_store().similarity_search_with_score_by_vector(
        list(map(float, vector)), k=k)
    return [float(score) for _doc, score in hits]


def check_scope(question: str) -> dict[str, Any]:
    """The `scope_check` callable handed to `answer_question`."""
    return scope_guard.classify(question, _embed, _nearest_topic, _probe, SCOPE_PROBE_K)


def run_rag(
    question: str,
    retriever: Any,
    top_k: int = 5,
    history: list[dict[str, Any]] | None = None,
    db: Session | None = None,
) -> dict[str, Any]:
    """Call answer_question() and return a fully serialisable result dict.

    Args:
        history: recent {'role', 'content'} turns, oldest first. Trimmed and condensed by
                 `rag_pipeline.format_history`; affects the prompt only, not retrieval.
        db:      session used only to read the reranker toggle. Optional so the offline
                 scripts that call this can keep working without one; when it is None the
                 selection is the plain `[:top_k]` it has always been.

    Returns:
        answer        : str
        sources       : list[dict]   (serialised Documents with enriched metadata)
        provider_used : str
        fallback_used : bool
        topics_detected: list[str]  (for DB storage)
        raw_sources   : list[Document]
        out_of_scope  : bool        (the guardrail refused; `answer` is the decline)
        scope         : dict        (the verdict and the two scores behind it)
    """
    # A closure, so `rag_pipeline` never learns what a Session is.
    rerank = (lambda q, docs, k: rerank_service.select(db, q, docs, k)) if db is not None else None

    result = answer_question(question, retriever, top_k=top_k, history=history,
                             rerank=rerank, scope_check=check_scope)

    serialised_sources = [doc_to_dict(doc) for doc in result["sources"]]
    topics = extract_topics_from_sources(result["sources"])
    scope = result.get("scope") or {}

    return {
        "answer":          result["answer"],
        "sources":         serialised_sources,
        "provider_used":   result["provider_used"],
        "fallback_used":   result["fallback_used"],
        "topics_detected": topics,
        "raw_sources":     result["sources"],
        "out_of_scope":    scope_guard.is_refusal(scope),
        "scope":           scope,
    }


def run_retrieve_only(question: str, retriever: Any, top_k: int = 5,
                      db: Session | None = None) -> list[dict[str, Any]]:
    """Retrieve chunks without calling the LLM. Debug endpoint only.

    Reranks when the toggle is on, so this endpoint shows what /chat would actually be
    grounded on. An inspection endpoint that quietly disagreed with the real pipeline
    would be worse than not having one.
    """
    candidates: list[Document] = retriever.invoke(question)
    docs = (rerank_service.select(db, question, candidates, top_k)
            if db is not None else candidates[:top_k])
    return [doc_to_dict(doc) for doc in docs]
