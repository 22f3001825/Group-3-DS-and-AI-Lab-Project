"""Prepare an authenticated Discourse export for privacy-aware RAG ingestion.

The raw export remains untouched. This module writes cleaned, quarantined, and
thread-level JSONL artifacts that retain post-level provenance without indexing
profile data or usernames.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString


DEFAULT_MIN_CHARACTERS = 40
DEFAULT_NEAR_DUPLICATE_THRESHOLD = 0.92
MAX_PRIMARY_REPLIES = 5
DISCUSSION_POSTS_PER_DOCUMENT = 4
MINHASH_SEEDS = tuple(range(12))
ATTACHMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".zip", ".csv"}
ACKNOWLEDGEMENT_RE = re.compile(
    r"^(thanks|thank you|ok|okay|got it|noted|resolved|same doubt|following|bump)[!. ]*$",
    flags=re.IGNORECASE,
)
TOKEN_RE = re.compile(r"[a-z0-9_+#.-]+", flags=re.IGNORECASE)
WEEK_RE = re.compile(r"\bweek\s*[-_:]?\s*(1[0-2]|[1-9])\b", flags=re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    root_dir = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Clean a Discourse JSON export into thread-aware RAG documents.")
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to the raw discourse_export.json produced by the authenticated scraper.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root_dir / "data" / "cleaned" / "discourse",
        help="Directory for generated private cleaning artifacts.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=root_dir / "reports",
        help="Directory for the shareable cleaning summary (no post content or profile data).",
    )
    parser.add_argument("--min-characters", type=int, default=DEFAULT_MIN_CHARACTERS)
    parser.add_argument("--near-duplicate-threshold", type=float, default=DEFAULT_NEAR_DUPLICATE_THRESHOLD)
    return parser.parse_args()


def load_export(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("topics"), list) or not isinstance(payload.get("posts"), list):
        raise ValueError("Input must be a Discourse export with top-level topics and posts lists.")
    return payload


def clean_export(
    export: dict[str, Any],
    min_characters: int = DEFAULT_MIN_CHARACTERS,
    near_duplicate_threshold: float = DEFAULT_NEAR_DUPLICATE_THRESHOLD,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    topics_by_id = {str(topic.get("topic_id")): topic for topic in export.get("topics", [])}
    candidate_posts: list[dict[str, Any]] = []
    quarantined: list[dict[str, Any]] = []

    for post in export.get("posts", []):
        record, reason = clean_post(post, topics_by_id.get(str(post.get("topic_id"))), min_characters)
        if record is None:
            quarantined.append(quarantine_record(post, reason or "unusable_post"))
        else:
            candidate_posts.append(record)

    retained_posts, duplicate_records = deduplicate_posts(candidate_posts, near_duplicate_threshold)
    quarantined.extend(duplicate_records)
    thread_documents, attachment_records = assemble_thread_documents(retained_posts, topics_by_id)

    topic_coverage = {
        "topics_in_export": len(topics_by_id),
        "topics_with_retained_posts": len({post["topic_id"] for post in retained_posts}),
        "topics_without_retained_posts": len(set(topics_by_id) - {post["topic_id"] for post in retained_posts}),
        "stream_count_mismatches": [
            str(topic_id)
            for topic_id, topic in topics_by_id.items()
            if topic.get("stream_post_count") is not None
            and topic.get("exported_post_count") is not None
            and topic.get("stream_post_count") != topic.get("exported_post_count")
        ],
    }
    report = {
        "input": {
            "topics": len(export.get("topics", [])),
            "posts": len(export.get("posts", [])),
            "users_not_indexed": len(export.get("users", [])),
            "topic_errors": len(export.get("topic_errors", [])),
            "profile_errors": len(export.get("profile_errors", [])),
        },
        "output": {
            "retained_posts": len(retained_posts),
            "quarantined_posts": len(quarantined),
            "thread_documents": len(thread_documents),
            "attachments": len(attachment_records),
        },
        "quarantine_reasons": dict(sorted(Counter(item["reason"] for item in quarantined).items())),
        "content_types": dict(sorted(Counter(post["content_type"] for post in retained_posts).items())),
        "confidence_flags": dict(sorted(Counter(post["confidence_flag"] for post in retained_posts).items())),
        "author_roles": dict(sorted(Counter(post["author_role"] for post in retained_posts).items())),
        "topic_coverage": topic_coverage,
    }
    return retained_posts, quarantined, thread_documents, {"report": report, "attachments": attachment_records}


def clean_post(post: dict[str, Any], topic: dict[str, Any] | None, min_characters: int) -> tuple[dict[str, Any] | None, str | None]:
    raw_post = post.get("raw_post") or {}
    if raw_post.get("post_type") not in (None, 1):
        return None, "system_post"

    text, links, attachments = clean_html(post.get("content_html") or "")
    if not text:
        text = normalize_text(post.get("content_text") or "")
    if not text:
        return None, "empty_after_cleaning"
    if is_low_value_text(text, min_characters):
        return None, "low_value_or_acknowledgement"

    thread_name = str(post.get("thread_name") or topic.get("thread_name") if topic else post.get("thread_name") or "")
    author_role = classify_author_role(post.get("posted_by") or {})
    content_type = classify_content_type(post, text, thread_name, author_role, links)
    confidence_flag = "verified" if post.get("is_solution") or author_role == "staff" else "community"
    topic_id = str(post.get("topic_id"))
    week = detect_week(f"{thread_name}\n{text}")

    record = {
        "post_id": str(post.get("post_id")),
        "topic_id": topic_id,
        "thread_name": thread_name,
        "thread_url": post.get("thread_url") or (topic or {}).get("url"),
        "post_url": post.get("post_url"),
        "post_number": post.get("post_number") or 0,
        "created_at": post.get("posted_at"),
        "updated_at": post.get("updated_at"),
        "text": text,
        "canonical_text": canonicalize(text),
        "content_type": content_type,
        "confidence_flag": confidence_flag,
        "author_role": author_role,
        "is_solution": bool(post.get("is_solution")),
        "like_count": int(post.get("like_count") or 0),
        "week": week,
        "links": links,
        "attachments": attachments,
        "image_urls": post.get("image_urls") or [],
        "image_files": post.get("image_files") or [],
    }
    return record, None


def clean_html(html: str) -> tuple[str, list[dict[str, str]], list[dict[str, str]]]:
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.select("blockquote, .quote, .quote-controls, .onebox, .embedded-posts, script, style, noscript"):
        element.decompose()
    for element in soup.find_all("pre"):
        code = element.get_text("\n", strip=True)
        element.replace_with(NavigableString(f"\n```\n{code}\n```\n"))

    links: list[dict[str, str]] = []
    attachments: list[dict[str, str]] = []
    for anchor in soup.find_all("a"):
        href = str(anchor.get("href") or "").strip()
        if not href:
            continue
        label = normalize_text(anchor.get_text(" ", strip=True)) or href
        record = {"url": href, "label": label}
        if is_attachment(href):
            attachments.append({**record, "kind": "attachment"})
        else:
            links.append(record)

    for image in soup.find_all("img"):
        image.decompose()
    return normalize_text(soup.get_text("\n")), unique_records(links), unique_records(attachments)


def normalize_text(value: str) -> str:
    text = value.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t ]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def canonicalize(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.lower()))


def is_low_value_text(text: str, min_characters: int) -> bool:
    compact = " ".join(text.split())
    return len(compact) < min_characters or bool(ACKNOWLEDGEMENT_RE.fullmatch(compact))


def classify_author_role(posted_by: dict[str, Any]) -> str:
    evidence = " ".join(
        str(posted_by.get(key) or "")
        for key in ("title", "primary_group_name", "flair_name")
    ).lower()
    staff_terms = ("staff", "support", "instructor", "faculty", "teaching", "moderator", "admin", "ta", "tutor")
    return "staff" if any(term in evidence for term in staff_terms) else "student"


def classify_content_type(
    post: dict[str, Any], text: str, thread_name: str, author_role: str, links: list[dict[str, str]]
) -> str:
    combined = f"{thread_name}\n{text}".lower()
    if post.get("is_solution"):
        return "accepted_solution"
    if author_role == "staff":
        return "staff_explanation"
    if any(term in combined for term in ("resource", "lecture", "notes", "slides", "assignment link")) and links:
        return "resource"
    if any(term in combined for term in ("announcement", "deadline", "maintenance", "registration")):
        return "announcement"
    if "?" in text or any(term in combined for term in ("doubt", "how do", "what is", "why does", "clarification")):
        return "question"
    return "community_answer"


def detect_week(text: str) -> int | None:
    match = WEEK_RE.search(text)
    return int(match.group(1)) if match else None


def is_attachment(url: str) -> bool:
    path = urlparse(url).path.lower()
    return Path(path).suffix in ATTACHMENT_EXTENSIONS or "/uploads/" in path


def unique_records(records: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, str]] = []
    for record in records:
        key = (record.get("url", ""), record.get("label", ""))
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique


def deduplicate_posts(
    records: list[dict[str, Any]], near_duplicate_threshold: float
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    retained: list[dict[str, Any]] = []
    quarantined: list[dict[str, Any]] = []
    exact_seen: dict[str, dict[str, Any]] = {}
    buckets: dict[tuple[int, ...], list[dict[str, Any]]] = defaultdict(list)

    for record in sorted(records, key=quality_sort_key):
        canonical = record["canonical_text"]
        existing = exact_seen.get(canonical)
        if existing is not None:
            quarantined.append(quarantine_record(record, "exact_duplicate", duplicate_of=existing["post_id"]))
            continue

        shingles = token_shingles(canonical)
        signature = minhash_signature(shingles)
        near_match = find_near_duplicate(shingles, signature, buckets, near_duplicate_threshold)
        if near_match is not None:
            quarantined.append(quarantine_record(record, "near_duplicate", duplicate_of=near_match["post_id"]))
            continue

        record.pop("canonical_text")
        record["dedupe"] = {"status": "retained", "method": "none"}
        record["_shingles"] = shingles
        record["_signature"] = signature
        retained.append(record)
        exact_seen[canonical] = record
        for band in signature_bands(signature):
            buckets[band].append(record)

    for record in retained:
        record.pop("_shingles", None)
        record.pop("_signature", None)
    return sorted(retained, key=lambda item: (int(item["topic_id"]), item["post_number"])), quarantined


def quality_sort_key(record: dict[str, Any]) -> tuple[int, int, int, int, str]:
    authority = 2 if record["is_solution"] else 1 if record["author_role"] == "staff" else 0
    return (-authority, -record["like_count"], -len(record["text"]), int(record["topic_id"]), record["post_id"])


def token_shingles(text: str, size: int = 3) -> set[str]:
    tokens = TOKEN_RE.findall(text)
    if len(tokens) < size:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[index : index + size]) for index in range(len(tokens) - size + 1)}


def minhash_signature(shingles: set[str]) -> tuple[int, ...]:
    if not shingles:
        return tuple(0 for _ in MINHASH_SEEDS)
    return tuple(min(stable_hash(f"{seed}:{shingle}") for shingle in shingles) for seed in MINHASH_SEEDS)


def stable_hash(value: str) -> int:
    return int.from_bytes(hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest(), "big")


def signature_bands(signature: tuple[int, ...], band_size: int = 3) -> Iterable[tuple[int, ...]]:
    for index in range(0, len(signature), band_size):
        yield signature[index : index + band_size]


def find_near_duplicate(
    shingles: set[str],
    signature: tuple[int, ...],
    buckets: dict[tuple[int, ...], list[dict[str, Any]]],
    threshold: float,
) -> dict[str, Any] | None:
    candidates: dict[str, dict[str, Any]] = {}
    for band in signature_bands(signature):
        for candidate in buckets.get(band, []):
            candidates[candidate["post_id"]] = candidate
    for candidate in candidates.values():
        candidate_shingles = candidate["_shingles"]
        union = shingles | candidate_shingles
        similarity = len(shingles & candidate_shingles) / len(union) if union else 1.0
        if similarity >= threshold:
            return candidate
    return None


def quarantine_record(post: dict[str, Any], reason: str, duplicate_of: str | None = None) -> dict[str, Any]:
    record = {
        "post_id": str(post.get("post_id")),
        "topic_id": str(post.get("topic_id")),
        "post_url": post.get("post_url"),
        "reason": reason,
    }
    if duplicate_of:
        record["duplicate_of_post_id"] = duplicate_of
    return record


def assemble_thread_documents(
    posts: list[dict[str, Any]], topics_by_id: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for post in posts:
        grouped[post["topic_id"]].append(post)

    documents: list[dict[str, Any]] = []
    attachment_records: list[dict[str, Any]] = []
    for topic_id, topic_posts in sorted(grouped.items(), key=lambda item: int(item[0])):
        topic_posts.sort(key=lambda post: post["post_number"])
        topic = topics_by_id.get(topic_id, {})
        opening_post = next((post for post in topic_posts if post["post_number"] == 1), topic_posts[0])
        replies = [post for post in topic_posts if post["post_id"] != opening_post["post_id"]]
        primary_replies = select_primary_replies(replies)
        selected = [opening_post, *primary_replies]
        selected_ids = {post["post_id"] for post in selected}
        title = topic.get("thread_name") or opening_post["thread_name"]
        week = opening_post["week"] or detect_week(title)
        confidence = "verified" if any(post["confidence_flag"] == "verified" for post in selected) else "community"
        core_document = make_thread_document(
            doc_id=f"discourse-topic-{topic_id}-core",
            topic_id=topic_id,
            title=title,
            opening_post=opening_post,
            posts=selected,
            week=week,
            confidence=confidence,
            content_kind="question_answer" if replies else "discussion",
            segment_index=0,
        )
        documents.append(core_document)
        attachment_records.extend(attachment_manifest_records(core_document))

        remaining = [post for post in replies if post["post_id"] not in selected_ids]
        for segment_index, segment_posts in enumerate(chunked(remaining, DISCUSSION_POSTS_PER_DOCUMENT), start=1):
            document = make_thread_document(
                doc_id=f"discourse-topic-{topic_id}-discussion-{segment_index:02d}",
                topic_id=topic_id,
                title=title,
                opening_post=opening_post,
                posts=[opening_post, *segment_posts],
                week=week,
                confidence="community",
                content_kind="discussion_segment",
                segment_index=segment_index,
            )
            documents.append(document)
            attachment_records.extend(attachment_manifest_records(document))
    return documents, unique_attachment_records(attachment_records)


def select_primary_replies(replies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    solutions = [post for post in replies if post["is_solution"]]
    staff = [post for post in replies if post["author_role"] == "staff" and post not in solutions]
    community = [post for post in replies if post not in solutions and post not in staff]
    ranked_community = sorted(community, key=lambda post: (-post["like_count"], post["post_number"]))
    return (solutions + staff + ranked_community)[:MAX_PRIMARY_REPLIES]


def make_thread_document(
    doc_id: str,
    topic_id: str,
    title: str,
    opening_post: dict[str, Any],
    posts: list[dict[str, Any]],
    week: int | None,
    confidence: str,
    content_kind: str,
    segment_index: int,
) -> dict[str, Any]:
    sections = [f"# {title}", "## Opening post", opening_post["text"]]
    for post in posts:
        if post["post_id"] == opening_post["post_id"]:
            continue
        heading = "Accepted solution" if post["is_solution"] else "Staff response" if post["author_role"] == "staff" else "Discussion response"
        sections.extend([f"## {heading}", post["text"]])

    attachments = [attachment for post in posts for attachment in post["attachments"]]
    return {
        "doc_id": doc_id,
        "text": "\n\n".join(sections),
        "question_text": opening_post["text"],
        "metadata": {
            "source_type": "discourse_forum",
            "topic_id": topic_id,
            "thread_name": title,
            "thread_url": opening_post["thread_url"],
            "post_urls": [post["post_url"] for post in posts if post.get("post_url")],
            "post_ids": [post["post_id"] for post in posts],
            "week": week,
            "content_type": content_kind,
            "confidence_flag": confidence,
            "is_solved": any(post["is_solution"] for post in posts),
            "author_roles": sorted({post["author_role"] for post in posts}),
            "created_at": opening_post["created_at"],
            "updated_at": max((post["updated_at"] or "") for post in posts) or None,
            "segment_index": segment_index,
            "attachments": unique_records(attachments),
        },
    }


def attachment_manifest_records(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "doc_id": document["doc_id"],
            "topic_id": document["metadata"]["topic_id"],
            "thread_url": document["metadata"]["thread_url"],
            **attachment,
            "download_status": "not_downloaded",
        }
        for attachment in document["metadata"]["attachments"]
    ]


def unique_attachment_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, Any]] = []
    for record in records:
        key = (record["doc_id"], record["url"])
        if key not in seen:
            seen.add(key)
            result.append(record)
    return result


def chunked(values: list[dict[str, Any]], size: int) -> Iterable[list[dict[str, Any]]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    temporary_path.replace(path)


def write_report(report_dir: Path, report: dict[str, Any]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "discourse_cleaning_report.json"
    markdown_path = report_dir / "discourse_cleaning_report.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    summary = report["report"]
    markdown_path.write_text(
        "\n".join(
            [
                "# Discourse Cleaning Report",
                "",
                f"- Raw topics: {summary['input']['topics']}",
                f"- Raw posts: {summary['input']['posts']}",
                f"- Retained posts: {summary['output']['retained_posts']}",
                f"- Quarantined posts: {summary['output']['quarantined_posts']}",
                f"- Thread-level RAG documents: {summary['output']['thread_documents']}",
                f"- Attachment links discovered: {summary['output']['attachments']}",
                "",
                "## Quarantine Reasons",
                "",
                *[f"- {reason}: {count}" for reason, count in summary["quarantine_reasons"].items()],
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    export = load_export(args.input)
    posts, quarantined, documents, extra = clean_export(
        export,
        min_characters=max(1, args.min_characters),
        near_duplicate_threshold=args.near_duplicate_threshold,
    )
    write_jsonl(args.output_dir / "posts_cleaned.jsonl", posts)
    write_jsonl(args.output_dir / "quarantined_posts.jsonl", quarantined)
    write_jsonl(args.output_dir / "threads_for_rag.jsonl", documents)
    write_jsonl(args.output_dir / "attachments_manifest.jsonl", extra["attachments"])
    write_report(args.report_dir, extra)
    print(json.dumps(extra["report"]["output"], indent=2))
    print(f"Cleaned forum artifacts: {args.output_dir}")


if __name__ == "__main__":
    main()
