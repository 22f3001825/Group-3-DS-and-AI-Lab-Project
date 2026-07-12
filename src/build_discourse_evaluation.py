"""Create topic-level retrieval evaluation queries from verified forum Q&A."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


def load_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def split_for_topic(topic_id: str) -> str:
    bucket = int(hashlib.sha256(topic_id.encode("utf-8")).hexdigest()[:8], 16) % 100
    if bucket < 70:
        return "train"
    if bucket < 85:
        return "validation"
    return "test"


def build_queries(chunks: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    chunks_by_document: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for chunk in chunks:
        metadata = chunk.get("metadata") or {}
        if metadata.get("source_type") != "discourse_forum":
            continue
        chunks_by_document[str(metadata.get("doc_id"))].append(chunk)

    queries: list[dict[str, Any]] = []
    for doc_id, document_chunks in sorted(chunks_by_document.items()):
        metadata = document_chunks[0]["metadata"]
        if not doc_id.endswith("-core") or metadata.get("confidence_flag") != "verified":
            continue
        question = str(metadata.get("question_text") or "").strip()
        topic_id = str(metadata.get("topic_id") or "")
        if not topic_id or len(question) < 20:
            continue
        queries.append(
            {
                "query_id": f"discourse-question-{topic_id}",
                "query": question,
                "split": split_for_topic(topic_id),
                "source_type": "discourse_forum",
                "topic_id": topic_id,
                "gold_doc_id": doc_id,
                "gold_chunk_ids": [chunk["metadata"]["chunk_id"] for chunk in document_chunks],
                "thread_url": metadata.get("thread_url"),
                "confidence_flag": metadata.get("confidence_flag"),
            }
        )

    topic_ids = [query["topic_id"] for query in queries]
    if len(topic_ids) != len(set(topic_ids)):
        raise ValueError("A topic appears in multiple evaluation queries; topic-level isolation was violated.")
    report = {
        "queries": len(queries),
        "splits": dict(sorted(Counter(query["split"] for query in queries).items())),
        "topic_leakage_check": "passed",
    }
    return queries, report


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    temporary_path.replace(path)


def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent
    input_path = root_dir / "data" / "splits" / "discourse_chunks.jsonl"
    output_dir = root_dir / "data" / "evaluation"
    if not input_path.exists():
        raise FileNotFoundError("Forum chunks not found. Run src/prepare_rag_splits.py first.")
    queries, report = build_queries(load_jsonl(input_path))
    write_jsonl(output_dir / "discourse_queries.jsonl", queries)
    (output_dir / "discourse_evaluation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
