"""Milestone 4 — Ingestion Helper.

Handles chunking and Qdrant ingestion for any ExperimentConfig.
Each config gets its own collection in the local Qdrant instance.

Key functions:
  collection_exists(config) → bool
  ingest_config_to_qdrant(config) → bool
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.experiment_config import ExperimentConfig


def collection_exists(config: ExperimentConfig) -> bool:
    """Return True if the Qdrant collection for this config already exists."""
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(url=config.qdrant_url)
        collections = [c.name for c in client.get_collections().collections]
        return config.collection_name in collections
    except Exception as e:
        print(f"  [Qdrant] Could not check collection: {e}")
        return False


def _chunk_documents(config: ExperimentConfig) -> list:
    """Re-chunk the cleaned corpus with the given chunk_size and overlap.

    Returns a list of LangChain Documents.
    """
    import re
    from langchain_text_splitters import (
        MarkdownHeaderTextSplitter,
        RecursiveCharacterTextSplitter,
    )
    from langchain_core.documents import Document

    cleaned_dir = ROOT_DIR / "data" / "cleaned"

    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("### Timestamp:", "timestamp"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=True,
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    def extract_week(filepath: Path) -> int:
        match = re.search(r"(?i)week[\s_-]*0*(\d+)", str(filepath))
        return int(match.group(1)) if match else 0

    def extract_source_type(filepath: Path) -> str:
        try:
            rel = filepath.relative_to(cleaned_dir)
            return rel.parts[0]
        except ValueError:
            return "unknown"

    documents = []
    for md_file in cleaned_dir.rglob("*.md"):
        if md_file.is_dir():
            continue
        content = md_file.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            continue

        week = extract_week(md_file)
        source = extract_source_type(md_file)
        doc_id = md_file.stem.replace(" ", "_")

        md_splits = markdown_splitter.split_text(content)
        chunks = text_splitter.split_documents(md_splits)

        for i, chunk in enumerate(chunks):
            chunk.metadata["week"] = week
            chunk.metadata["source_type"] = source
            chunk.metadata["doc_id"] = f"{doc_id}_chunk_{i}"
            documents.append(chunk)

    print(f"  [Chunk] {len(documents)} chunks (size={config.chunk_size}, overlap={config.chunk_overlap})")
    return documents


def ingest_config_to_qdrant(config: ExperimentConfig) -> bool:
    """Chunk + embed + ingest for a given ExperimentConfig.

    Returns True on success, False on failure.
    """
    try:
        from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
        from qdrant_client import QdrantClient
        from qdrant_client.http.exceptions import UnexpectedResponse
    except ImportError as e:
        print(f"  [Ingest] Missing dependency: {e}")
        return False

    # Map retrieval_mode string to enum
    mode_map = {
        "hybrid": RetrievalMode.HYBRID,
        "dense": RetrievalMode.DENSE,
        "sparse": RetrievalMode.SPARSE,
    }
    retrieval_mode = mode_map.get(config.retrieval_mode, RetrievalMode.HYBRID)

    try:
        client = QdrantClient(url=config.qdrant_url)

        # Drop existing collection for clean re-run
        existing = [c.name for c in client.get_collections().collections]
        if config.collection_name in existing:
            print(f"  [Ingest] Dropping existing collection '{config.collection_name}'...")
            client.delete_collection(config.collection_name)

        print(f"  [Ingest] Loading embedding model: {config.embedding_model}...")
        dense_embeddings = FastEmbedEmbeddings(model_name=config.embedding_model)

        # Sparse only used in hybrid and sparse modes
        sparse_embeddings = None
        if config.retrieval_mode in ("hybrid", "sparse"):
            sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

        # Chunk documents with this config's settings
        docs = _chunk_documents(config)
        if not docs:
            print("  [Ingest] No documents found — check data/cleaned/")
            return False

        print(f"  [Ingest] Uploading {len(docs)} chunks to '{config.collection_name}'...")

        qdrant_kwargs = {
            "url": config.qdrant_url,
            "collection_name": config.collection_name,
            "retrieval_mode": retrieval_mode,
        }
        if config.qdrant_api_key:
            qdrant_kwargs["api_key"] = config.qdrant_api_key

        if sparse_embeddings and config.retrieval_mode in ("hybrid", "sparse"):
            qdrant_kwargs["sparse_embedding"] = sparse_embeddings

        QdrantVectorStore.from_documents(
            docs,
            embedding=dense_embeddings,
            **qdrant_kwargs,
        )

        print(f"  [Ingest] ✓ Done — {len(docs)} chunks in '{config.collection_name}'")
        return True

    except Exception as e:
        print(f"  [Ingest] ERROR: {type(e).__name__}: {e}")
        return False
