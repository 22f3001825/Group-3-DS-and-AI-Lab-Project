"""
api/services/topic_vectors.py
The 48 taxonomy topics as vectors, embedded once per process.

Two features need "how close is this text to anything this course teaches?", and they need
the *same* answer:

  - `socratic_service.shortlist_topics` — which concept is the student's highlighted
    question about, so the panel can name it and pick lecture segments.
  - `scope_guard` — is a chat question about this course at all, so an off-syllabus one can
    be refused in code rather than by asking the model nicely.

Sharing one matrix is not just tidiness. The embedding pass is 48 documents through
BGE-small, and an `@lru_cache` in each consumer would run it twice and hold two copies of
the same float32 array for the life of the process.

**This is a module rather than a helper inside `socratic_service` because of an import
cycle.** `socratic_service` imports `rag_service.clean_lecture_title` at module level, and
`rag_service` is what wires the scope guard into the chat path — so
`rag_service → scope_guard → socratic_service → rag_service` would not import. Nothing here
imports either of them: only the taxonomy loader, plus `dependencies` from inside a function
body so that importing this module never constructs a vector store.

Vectors come from the vector store's OWN FastEmbed instance, so topic vectors live in the
space the chunks were embedded into and no second model is loaded. Cached because the
taxonomy only changes when `topic_taxonomy.json` does, which needs a restart anyway.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Optional

from .recommendation_service import load_taxonomy


def topic_document(topic: dict[str, Any]) -> str:
    """The text stood in for a topic when it is embedded.

    Name + description + aliases, because a one-word name embeds poorly: "PCA" alone is
    close to any three-letter acronym, whereas "PCA. Linear dimensionality reduction
    technique maximizing variance along orthogonal principal axes. Principal Component
    Analysis ..." sits where the lecture chunks about it sit.
    """
    aliases = " ".join(topic.get("aliases", []) or [])
    return f"{topic.get('name', '')}. {topic.get('description', '')} {aliases}".strip()


@lru_cache(maxsize=1)
def topic_matrix() -> tuple[tuple[int, ...], Any]:
    """`(topic_ids, L2-normalised matrix)` — or `((), None)` if the taxonomy is empty.

    Rows are unit vectors, so a dot product with a unit query vector IS cosine similarity;
    every caller relies on that rather than normalising again.
    """
    import numpy as np  # noqa: PLC0415

    from ..dependencies import _build_vector_store  # noqa: PLC0415

    topics = load_taxonomy()
    if not topics:
        return (), None
    embeddings = _build_vector_store().embeddings
    matrix = np.asarray(embeddings.embed_documents([topic_document(t) for t in topics]),
                        dtype="float32")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    matrix = matrix / np.clip(norms, 1e-9, None)
    return tuple(t["id"] for t in topics), matrix


def embed_query(text: str) -> Any:
    """The query side of the same space: a unit-length float32 vector.

    Separate from `topic_scores` because the scope guard needs the raw vector twice — once
    against this matrix and once against Qdrant — and embedding it twice would double the
    only part of the guard that costs anything.
    """
    import numpy as np  # noqa: PLC0415

    from ..dependencies import _build_vector_store  # noqa: PLC0415

    vector = np.asarray(_build_vector_store().embeddings.embed_query(text), dtype="float32")
    return vector / max(float(np.linalg.norm(vector)), 1e-9)


def topic_scores(query_vector: Any) -> tuple[tuple[int, ...], Any]:
    """`(topic_ids, cosine scores)` for an already-normalised query vector.

    Takes a vector rather than text so a caller that already has one does not pay for a
    second `embed_query`. Returns `((), None)` when there is no taxonomy to score against.
    """
    ids, matrix = topic_matrix()
    if matrix is None:
        return (), None
    return ids, matrix @ query_vector


def best_topic(query_vector: Any) -> tuple[Optional[dict[str, Any]], float]:
    """The single closest topic and its cosine, for callers that want the max and no more."""
    ids, scores = topic_scores(query_vector)
    if scores is None or not len(scores):
        return None, 0.0

    best_index = int(scores.argmax())
    by_id = {t["id"]: t for t in load_taxonomy()}
    return by_id.get(ids[best_index]), float(scores[best_index])
