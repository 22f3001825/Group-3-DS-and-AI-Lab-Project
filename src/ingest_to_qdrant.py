"""Idempotently ingest course and cleaned Discourse chunks into Qdrant hybrid search."""

from __future__ import annotations

import argparse
import json
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models


DEFAULT_COLLECTION_NAME = "mlt_course_bot"
CHUNK_FILES = ("train_chunks.jsonl", "val_chunks.jsonl", "test_chunks.jsonl", "discourse_chunks.jsonl")
POINT_NAMESPACE = uuid.UUID("84a2bff2-c04f-4ac0-b4de-cf79d2583ec8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest RAG chunks into Qdrant without deleting existing data by default.")
    parser.add_argument("--collection", default=os.getenv("QDRANT_COLLECTION", DEFAULT_COLLECTION_NAME))
    parser.add_argument("--recreate", action="store_true", help="Delete and recreate the named collection before ingestion.")
    parser.add_argument("--batch-size", type=int, default=64)
    return parser.parse_args()


def qdrant_settings() -> tuple[str, str | None]:
    load_dotenv()
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    if not url:
        raise ValueError("Missing QDRANT_URL. Set it in .env or the container environment.")
    return url, api_key or None


def stable_point_id(chunk_id: str) -> str:
    return str(uuid.uuid5(POINT_NAMESPACE, chunk_id))


def load_chunks(splits_dir: Path) -> tuple[list[Document], list[str]]:
    documents: list[Document] = []
    point_ids: list[str] = []
    for filename in CHUNK_FILES:
        path = splits_dir / filename
        if not path.exists():
            print(f"Warning: {path} not found. Skipping.")
            continue
        print(f"Loading {filename}...")
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                data = json.loads(line)
                metadata = dict(data.get("metadata") or {})
                chunk_id = str(metadata.get("chunk_id") or f"{filename}:{line_number}")
                metadata["chunk_id"] = chunk_id
                metadata.setdefault("source_type", "unknown")
                documents.append(Document(page_content=str(data["text"]), metadata=metadata))
                point_ids.append(stable_point_id(chunk_id))
    print(f"Loaded {len(documents)} chunks.")
    return documents, point_ids


def build_embeddings() -> tuple[FastEmbedEmbeddings, FastEmbedSparse]:
    print("Loading embedding models (weights may download on the first run)...")
    return (
        FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5"),
        FastEmbedSparse(model_name="Qdrant/bm25"),
    )


def ensure_filter_indexes(client: QdrantClient, collection_name: str) -> None:
    field_schemas = {
        "metadata.week": models.PayloadSchemaType.INTEGER,
        "metadata.source_type": models.PayloadSchemaType.KEYWORD,
        "metadata.confidence_flag": models.PayloadSchemaType.KEYWORD,
        "metadata.is_solved": models.PayloadSchemaType.BOOL,
    }
    for field_name, field_schema in field_schemas.items():
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=field_schema,
            wait=True,
        )


def main() -> None:
    args = parse_args()
    root_dir = Path(__file__).resolve().parent.parent
    splits_dir = root_dir / "data" / "splits"
    url, api_key = qdrant_settings()
    documents, point_ids = load_chunks(splits_dir)
    if not documents:
        print("No chunks to ingest. Run the cleaning and chunking stages first.")
        return

    client = QdrantClient(url=url, api_key=api_key)
    collection_names = {collection.name for collection in client.get_collections().collections}
    if args.recreate and args.collection in collection_names:
        print(f"Deleting collection '{args.collection}' because --recreate was supplied.")
        client.delete_collection(args.collection)
        collection_names.remove(args.collection)

    dense_embeddings, sparse_embeddings = build_embeddings()
    if args.collection in collection_names:
        print(f"Upserting {len(documents)} chunks into existing collection '{args.collection}'.")
        store = QdrantVectorStore.from_existing_collection(
            collection_name=args.collection,
            embedding=dense_embeddings,
            sparse_embedding=sparse_embeddings,
            url=url,
            api_key=api_key,
            retrieval_mode=RetrievalMode.HYBRID,
        )
        store.add_documents(documents, ids=point_ids, batch_size=max(1, args.batch_size))
    else:
        print(f"Creating collection '{args.collection}' and inserting {len(documents)} chunks.")
        QdrantVectorStore.from_documents(
            documents,
            embedding=dense_embeddings,
            sparse_embedding=sparse_embeddings,
            url=url,
            api_key=api_key,
            collection_name=args.collection,
            retrieval_mode=RetrievalMode.HYBRID,
            ids=point_ids,
            batch_size=max(1, args.batch_size),
        )
    ensure_filter_indexes(client, args.collection)
    print(f"Ingestion complete: {len(documents)} deterministic upserts into '{args.collection}'.")


if __name__ == "__main__":
    main()
