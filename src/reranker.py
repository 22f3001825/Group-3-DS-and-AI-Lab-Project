"""Milestone 4 — Cross-Encoder Reranker Module.

Fetches a wide candidate set from the retriever, then re-scores each
document using a cross-encoder model for much more accurate relevance
ranking.  The cross-encoder sees (query, document) pairs jointly, which
is fundamentally more powerful than bi-encoder similarity.

Typical usage:
    reranker = CrossEncoderReranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
    reranked = reranker.rerank(query, candidate_docs, top_n=5)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_core.documents import Document


@dataclass
class ScoredDocument:
    """A document with its cross-encoder relevance score."""
    document: Document
    score: float


class CrossEncoderReranker:
    """Re-ranks retrieved documents using a cross-encoder model via sentence-transformers."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None  # Lazy-loaded

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
            except ImportError:
                raise RuntimeError(
                    "Install sentence-transformers for reranking: "
                    "pip install sentence-transformers"
                )
            print(f"  [Reranker] Loading cross-encoder: {self.model_name}...")
            self._model = CrossEncoder(self.model_name)
            print(f"  [Reranker] Model loaded successfully.")

    def rerank(
        self,
        query: str,
        documents: list[Document],
        top_n: int = 5,
    ) -> list[Document]:
        """Re-rank documents by cross-encoder score and return top_n.

        Args:
            query:     The user's question.
            documents: Candidate documents from the initial retrieval.
            top_n:     Number of documents to return after reranking.

        Returns:
            A list of the top_n most relevant documents, sorted by score.
        """
        if not documents:
            return []

        self._load_model()

        # Build (query, doc_text) pairs for the cross-encoder
        pairs = [(query, doc.page_content) for doc in documents]

        # Score all pairs
        scores = self._model.predict(pairs)

        # Combine scores with documents
        scored_docs = [
            ScoredDocument(document=doc, score=float(score))
            for doc, score in zip(documents, scores)
        ]

        # Sort by score descending and take top_n
        scored_docs.sort(key=lambda x: x.score, reverse=True)
        top_docs = scored_docs[:top_n]

        # Log scores for debugging
        print(f"  [Reranker] Scores (top {top_n} of {len(documents)} candidates):")
        for i, sd in enumerate(top_docs, 1):
            preview = sd.document.page_content[:60].replace("\n", " ")
            print(f"    [{i}] score={sd.score:.4f} | {preview}...")

        return [sd.document for sd in top_docs]
