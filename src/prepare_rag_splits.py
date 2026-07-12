"""Create token-aware RAG chunks for course documents and cleaned forum threads."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


CHUNK_SIZE_TOKENS = 384
CHUNK_OVERLAP_TOKENS = 58
FORUM_CONTEXT_MAX_TOKENS = 72


def extract_week(filepath: Path) -> int:
    match = re.search(r"(?i)week[\s_-]*0*(\d+)", str(filepath))
    return int(match.group(1)) if match else 0


def extract_source_type(filepath: Path, base_dir: Path) -> str:
    try:
        return filepath.relative_to(base_dir).parts[0]
    except ValueError:
        return "unknown"


def tokenizer() -> tiktoken.Encoding:
    return tiktoken.get_encoding("cl100k_base")


def token_length(text: str, encoding: tiktoken.Encoding | None = None) -> int:
    return len((encoding or tokenizer()).encode(text))


def trim_to_tokens(text: str, max_tokens: int, encoding: tiktoken.Encoding) -> str:
    tokens = encoding.encode(text)
    return encoding.decode(tokens[:max_tokens]).strip()


def build_splitter(chunk_size: int = CHUNK_SIZE_TOKENS) -> RecursiveCharacterTextSplitter:
    encoding = tokenizer()
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=min(CHUNK_OVERLAP_TOKENS, max(0, chunk_size - 1)),
        length_function=lambda text: token_length(text, encoding),
        separators=["\n\n", "\n", " ", ""],
    )


def load_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def chunk_markdown_documents(cleaned_dir: Path) -> tuple[dict[str, list[dict[str, Any]]], int]:
    headers_to_split_on = [("#", "h1"), ("##", "h2"), ("### Timestamp:", "timestamp")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=True)
    text_splitter = build_splitter()
    splits: dict[str, list[dict[str, Any]]] = {"train": [], "val": [], "test": []}
    documents_processed = 0

    for md_file in sorted(cleaned_dir.rglob("*.md")):
        relative_path = md_file.relative_to(cleaned_dir)
        if any(part.lower().startswith("discourse") for part in relative_path.parts):
            continue
        content = md_file.read_text(encoding="utf-8")
        if not content.strip():
            continue
        documents_processed += 1
        week = extract_week(md_file)
        source_type = extract_source_type(md_file, cleaned_dir)
        source_id = relative_path.with_suffix("").as_posix().replace("/", "_").replace(" ", "_")
        split_name = "train" if not week or week <= 8 else "val" if week <= 10 else "test"

        structural_documents = markdown_splitter.split_text(content)
        chunks = text_splitter.split_documents(structural_documents)
        for index, chunk in enumerate(chunks):
            metadata = {
                **chunk.metadata,
                "doc_id": source_id,
                "chunk_id": f"{source_id}_chunk_{index:03d}",
                "chunk_index": index,
                "source_type": source_type,
                "week": week or None,
                "source_path": relative_path.as_posix(),
                "token_count": token_length(chunk.page_content),
                "confidence_flag": "verified",
            }
            splits[split_name].append({"text": chunk.page_content, "metadata": metadata})
    return splits, documents_processed


def chunk_forum_documents(thread_documents: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    encoding = tokenizer()
    chunks: list[dict[str, Any]] = []
    for document in thread_documents:
        metadata = dict(document.get("metadata") or {})
        doc_id = str(document["doc_id"])
        question = trim_to_tokens(str(document.get("question_text") or ""), FORUM_CONTEXT_MAX_TOKENS, encoding)
        title = trim_to_tokens(str(metadata.get("thread_name") or "Forum thread"), 20, encoding)
        prefix = f"Forum thread: {title}\nOpening question: {question}".strip()
        available_tokens = max(128, CHUNK_SIZE_TOKENS - token_length(prefix, encoding) - 8)
        content = str(document.get("text") or "").strip()
        parts = [content] if token_length(content, encoding) <= CHUNK_SIZE_TOKENS else build_splitter(available_tokens).split_text(content)

        for index, part in enumerate(parts):
            chunk_text = part if len(parts) == 1 else f"{prefix}\n\n{part}".strip()
            if token_length(chunk_text, encoding) > CHUNK_SIZE_TOKENS:
                chunk_text = trim_to_tokens(chunk_text, CHUNK_SIZE_TOKENS, encoding)
            chunk_metadata = {
                **metadata,
                "doc_id": doc_id,
                "chunk_id": f"{doc_id}_chunk_{index:03d}",
                "chunk_index": index,
                "token_count": token_length(chunk_text, encoding),
                "question_text": question,
            }
            chunks.append({"text": chunk_text, "metadata": chunk_metadata})
    return chunks


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    temporary_path.replace(path)


def main() -> None:
    root_dir = Path(__file__).resolve().parent.parent
    cleaned_dir = root_dir / "data" / "cleaned"
    splits_dir = root_dir / "data" / "splits"
    reports_dir = root_dir / "reports"
    forum_documents_path = cleaned_dir / "discourse" / "threads_for_rag.jsonl"

    splits, markdown_document_count = chunk_markdown_documents(cleaned_dir)
    forum_chunks = chunk_forum_documents(load_jsonl(forum_documents_path))
    for split_name, records in splits.items():
        write_jsonl(splits_dir / f"{split_name}_chunks.jsonl", records)
    write_jsonl(splits_dir / "discourse_chunks.jsonl", forum_chunks)

    report = {
        "markdown_documents_processed": markdown_document_count,
        "markdown_chunks": {name: len(records) for name, records in splits.items()},
        "forum_thread_documents": len(load_jsonl(forum_documents_path)),
        "forum_chunks": len(forum_chunks),
        "chunk_size_tokens": CHUNK_SIZE_TOKENS,
        "chunk_overlap_tokens": CHUNK_OVERLAP_TOKENS,
    }
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "chunking_report.md").write_text(
        "\n".join(
            [
                "# Chunking & Splitting Report",
                "",
                f"- Markdown documents processed: {markdown_document_count}",
                f"- Train chunks: {len(splits['train'])}",
                f"- Validation chunks: {len(splits['val'])}",
                f"- Test chunks: {len(splits['test'])}",
                f"- Forum chunks: {len(forum_chunks)}",
                f"- Chunk size: {CHUNK_SIZE_TOKENS} tokens",
                f"- Overlap: {CHUNK_OVERLAP_TOKENS} tokens",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
