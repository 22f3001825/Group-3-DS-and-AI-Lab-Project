"""
services/embeddings.py
────────────────────────────────────────────────────────────
Generates sentence embeddings using sentence-transformers.
Model is loaded once and cached globally.
"""

import numpy as np
from config import Config

_model = None


def load_model():
    """Lazily load the sentence-transformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(Config.EMBEDDING_MODEL)
        except ImportError:
            raise RuntimeError(
                "sentence-transformers not installed. Run: pip install sentence-transformers"
            )
    return _model


def embed_chunks(texts: list) -> np.ndarray:
    """
    Embed a list of text strings.
    Returns float32 numpy array of shape (N, embedding_dim).
    """
    if not texts:
        return np.array([])
    model = load_model()
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True,
                              convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype("float32")


def embed_query(query: str) -> np.ndarray:
    """Embed a single query string for retrieval."""
    model = load_model()
    vec = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)
    return vec.astype("float32")
