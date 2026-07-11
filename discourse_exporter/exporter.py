from __future__ import annotations

import csv
import hashlib
import json
import mimetypes
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import requests

from .extract import extract_topic_records
from .llm import apply_llm_result_to_post, mark_llm_not_used, post_needs_llm_fallback
from .state import ExportState


def scrape_category(
    client,
    base_url: str,
    category_path: str,
    output_dir: Path,
    state_path: Path,
    max_pages: int | None = None,
    rate_limit_seconds: float = 0.5,
    refresh_users: bool = False,
    llm_fallback: str = "off",
    llm_client=None,
    topic_retries: int = 2,
    topic_retry_delay_seconds: float = 1.0,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    image_dir = output_dir / "imgs"
    image_dir.mkdir(parents=True, exist_ok=True)

    export_path = output_dir / "discourse_export.json"
    export = _load_existing_export(export_path)
    topics_by_id = {str(topic["topic_id"]): topic for topic in export.get("topics", [])}
    posts_by_id = {str(post["post_id"]): post for post in export.get("posts", [])}
    users_by_username = {user["username"]: user for user in export.get("users", []) if user.get("username")}
    topic_errors_by_id = {
        str(error["topic_id"]): error
        for error in export.get("topic_errors", [])
        if error.get("topic_id") is not None
    }
    state = ExportState.load(state_path)

    seen_topic_ids: set[str] = set()
    for page_number, topic_summaries in enumerate(_iter_category_pages(client, category_path, max_pages)):
        print(f"Category page {page_number}: {len(topic_summaries)} topics")
        for topic_summary in topic_summaries:
            topic_id = str(topic_summary["id"])
            seen_topic_ids.add(topic_id)
            existing_topic = topic_id in topics_by_id
            if existing_topic and not state.topic_needs_fetch(topic_summary):
                continue

            try:
                topic_json = _get_json_with_retries(
                    client=client,
                    path=f"/t/{topic_id}.json",
                    topic_id=topic_id,
                    topic_retries=topic_retries,
                    retry_delay_seconds=topic_retry_delay_seconds,
                )
            except requests.exceptions.RequestException as exc:
                error_record = _topic_error_record(
                    topic_summary,
                    base_url,
                    exc,
                    attempt_count=max(0, topic_retries) + 1,
                )
                topic_errors_by_id[topic_id] = error_record
                _append_topic_error_log(output_dir / "topic_errors.jsonl", error_record)
                _append_error_log(output_dir / "error.log", error_record)
                _write_export_checkpoint(
                    output_dir=output_dir,
                    base_url=base_url,
                    category_path=category_path,
                    topics_by_id=topics_by_id,
                    posts_by_id=posts_by_id,
                    users_by_username=users_by_username,
                    topic_errors_by_id=topic_errors_by_id,
                    status="partial",
                )
                print(
                    f"Skipping topic {topic_id}: "
                    f"HTTP {error_record.get('status_code') or 'error'} {error_record.get('reason') or ''}".rstrip()
                )
                continue

            topic_record, post_records = extract_topic_records(topic_json, base_url)
            topics_by_id[topic_id] = topic_record
            topic_errors_by_id.pop(topic_id, None)

            stale_post_ids = [
                post_id
                for post_id, post in posts_by_id.items()
                if str(post.get("topic_id")) == topic_id
            ]
            for post_id in stale_post_ids:
                posts_by_id.pop(post_id, None)

            apply_llm_fallback_to_posts(
                post_records,
                llm_client=llm_client,
                mode=llm_fallback,
                audit_log_path=output_dir / "llm_fallback_log.jsonl",
            )

            for post in post_records:
                post["image_files"] = _download_post_images(client, image_dir, post)
                posts_by_id[str(post["post_id"])] = post

            state.mark_topic(topic_summary)
            state.save(state_path)
            _write_export_checkpoint(
                output_dir=output_dir,
                base_url=base_url,
                category_path=category_path,
                topics_by_id=topics_by_id,
                posts_by_id=posts_by_id,
                users_by_username=users_by_username,
                topic_errors_by_id=topic_errors_by_id,
                status="partial",
            )
            time.sleep(rate_limit_seconds)

        state.save(state_path)

    usernames = sorted(
        {
            post.get("posted_by", {}).get("username")
            for post in posts_by_id.values()
            if post.get("posted_by", {}).get("username")
        }
    )
    for username in usernames:
        if username in users_by_username and not refresh_users:
            continue
        users_by_username[username] = _fetch_user_profile(client, username)
        _write_export_checkpoint(
            output_dir=output_dir,
            base_url=base_url,
            category_path=category_path,
            topics_by_id=topics_by_id,
            posts_by_id=posts_by_id,
            users_by_username=users_by_username,
            topic_errors_by_id=topic_errors_by_id,
            status="partial",
        )
        time.sleep(rate_limit_seconds)

    export = _write_export_checkpoint(
        output_dir=output_dir,
        base_url=base_url,
        category_path=category_path,
        topics_by_id=topics_by_id,
        posts_by_id=posts_by_id,
        users_by_username=users_by_username,
        topic_errors_by_id=topic_errors_by_id,
        status="complete",
    )
    state.save(state_path)
    return export


def apply_llm_fallback_to_posts(
    posts: list[dict[str, Any]],
    llm_client,
    mode: str,
    audit_log_path: Path,
) -> None:
    if mode not in {"off", "missing", "always"}:
        raise ValueError("llm fallback mode must be one of: off, missing, always")

    if mode == "off":
        for post in posts:
            mark_llm_not_used(post)
        return

    if llm_client is None:
        raise ValueError("llm_client is required when llm fallback mode is not off")

    for post in posts:
        should_run = mode == "always" or post_needs_llm_fallback(post)
        if not should_run:
            mark_llm_not_used(post)
            continue

        source = f"topic:{post.get('topic_id')} post:{post.get('post_id')}"
        try:
            result = llm_client.extract_post(post)
            apply_llm_result_to_post(post, result, source=source)
            _append_llm_audit_log(audit_log_path, post, mode, result=result)
        except Exception as exc:
            post["llm_used"] = False
            post["llm_confidence"] = None
            post["llm_warnings"] = [f"LLM fallback failed: {exc}"]
            post["llm_source"] = source
            post["llm_fields"] = {}
            _append_llm_audit_log(audit_log_path, post, mode, error=str(exc))


def _iter_category_pages(client, category_path: str, max_pages: int | None):
    page = 0
    seen_ids: set[int] = set()
    while max_pages is None or page < max_pages:
        separator = "&" if "?" in category_path else "?"
        payload = client.get_json(f"{category_path}.json{separator}page={page}")
        topics = payload.get("topic_list", {}).get("topics") or []
        topics = [topic for topic in topics if topic.get("id") not in seen_ids]
        if not topics:
            break
        for topic in topics:
            seen_ids.add(topic["id"])
        yield topics
        page += 1


def _get_json_with_retries(
    client,
    path: str,
    topic_id: str,
    topic_retries: int,
    retry_delay_seconds: float,
) -> dict[str, Any]:
    total_attempts = max(0, topic_retries) + 1
    for attempt in range(1, total_attempts + 1):
        try:
            return client.get_json(path)
        except requests.exceptions.RequestException as exc:
            if attempt >= total_attempts:
                raise
            response = getattr(exc, "response", None)
            status_code = getattr(response, "status_code", None)
            reason = getattr(response, "reason", None)
            status = f"HTTP {status_code} {reason}".strip() if status_code else "request error"
            print(f"Retrying topic {topic_id} after {status} (attempt {attempt}/{total_attempts})")
            if retry_delay_seconds > 0:
                time.sleep(retry_delay_seconds)

    raise RuntimeError("unreachable retry loop state")


def _topic_error_record(
    topic_summary: dict[str, Any],
    base_url: str,
    exc: requests.exceptions.RequestException,
    attempt_count: int,
) -> dict[str, Any]:
    response = exc.response
    topic_id = topic_summary.get("id")
    slug = topic_summary.get("slug") or str(topic_id)
    return {
        "topic_id": topic_id,
        "thread_name": topic_summary.get("title") or "",
        "slug": slug,
        "url": f"{base_url.rstrip('/')}/t/{slug}/{topic_id}",
        "status_code": getattr(response, "status_code", None),
        "reason": getattr(response, "reason", None),
        "attempt_count": attempt_count,
        "error": str(exc),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def _append_topic_error_log(path: Path, error_record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(error_record, ensure_ascii=False) + "\n")


def _append_error_log(path: Path, error_record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_code = error_record.get("status_code") or "error"
    reason = error_record.get("reason") or ""
    status = f"HTTP {status_code} {reason}".strip()
    line = (
        f"{error_record.get('recorded_at')} | topic_id={error_record.get('topic_id')} | "
        f"attempts={error_record.get('attempt_count')} | {status} | "
        f"{error_record.get('thread_name')} | {error_record.get('url')} | {error_record.get('error')}"
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def _append_llm_audit_log(
    path: Path,
    post: dict[str, Any],
    mode: str,
    result=None,
    error: str | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "topic_id": post.get("topic_id"),
        "post_id": post.get("post_id"),
        "post_url": post.get("post_url"),
        "source": post.get("llm_source"),
        "confidence": post.get("llm_confidence"),
        "warnings": post.get("llm_warnings") or [],
        "fields": post.get("llm_fields") or {},
    }
    if error:
        entry["error"] = error
    if result is not None:
        entry["raw_response"] = result.raw
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _fetch_user_profile(client, username: str) -> dict[str, Any]:
    payload = client.get_json(f"/u/{quote(username)}.json")
    user = payload.get("user", payload)
    return {
        "username": username,
        "name": user.get("name"),
        "title": user.get("title"),
        "bio_raw": user.get("bio_raw"),
        "bio_cooked": user.get("bio_cooked"),
        "location": user.get("location"),
        "website": user.get("website"),
        "profile_view_count": user.get("profile_view_count"),
        "created_at": user.get("created_at"),
        "last_seen_at": user.get("last_seen_at"),
        "last_posted_at": user.get("last_posted_at"),
        "trust_level": user.get("trust_level"),
        "avatar_template": user.get("avatar_template"),
        "raw_profile": user,
    }


def _download_post_images(client, image_dir: Path, post: dict[str, Any]) -> list[str]:
    local_files: list[str] = []
    for index, url in enumerate(post.get("image_urls") or [], start=1):
        content, content_type = client.get_bytes(url)
        filename = _image_filename(post, index, url, content_type)
        destination = image_dir / filename
        if not destination.exists():
            destination.write_bytes(content)
        local_files.append(f"imgs/{filename}")
    return local_files


def _image_filename(post: dict[str, Any], index: int, url: str, content_type: str) -> str:
    parsed = urlparse(url)
    extension = Path(parsed.path).suffix.lower()
    if not extension:
        extension = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".bin"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    topic_id = post.get("topic_id") or "topic"
    post_id = post.get("post_id") or "post"
    return f"topic-{topic_id}-post-{post_id}-{index:02d}-{digest}{extension}"


def _write_export_checkpoint(
    output_dir: Path,
    base_url: str,
    category_path: str,
    topics_by_id: dict[str, dict[str, Any]],
    posts_by_id: dict[str, dict[str, Any]],
    users_by_username: dict[str, dict[str, Any]],
    topic_errors_by_id: dict[str, dict[str, Any]],
    status: str,
) -> dict[str, Any]:
    export = {
        "metadata": {
            "base_url": base_url,
            "category_path": category_path,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "topic_count": len(topics_by_id),
            "post_count": len(posts_by_id),
            "user_count": len(users_by_username),
            "topic_error_count": len(topic_errors_by_id),
        },
        "topics": sorted(topics_by_id.values(), key=lambda item: item["topic_id"]),
        "posts": sorted(posts_by_id.values(), key=lambda item: (item["topic_id"], item.get("post_number") or 0)),
        "users": sorted(users_by_username.values(), key=lambda item: item.get("username") or ""),
        "topic_errors": sorted(topic_errors_by_id.values(), key=lambda item: item["topic_id"]),
    }

    _write_json(output_dir / "discourse_export.json", export)
    _write_topics_csv(output_dir / "discourse_topics.csv", export["topics"])
    _write_posts_csv(output_dir / "discourse_posts.csv", export["posts"])
    _write_users_csv(output_dir / "discourse_users.csv", export["users"])
    return export


def _load_existing_export(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"topics": [], "posts": [], "users": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_topics_csv(path: Path, topics: list[dict[str, Any]]) -> None:
    fields = [
        "topic_id",
        "thread_name",
        "url",
        "created_at",
        "updated_at",
        "last_posted_at",
        "bumped_at",
        "posts_count",
        "reply_count",
        "views",
        "like_count",
        "accepted_answer_post_id",
    ]
    _write_csv(path, topics, fields)


def _write_posts_csv(path: Path, posts: list[dict[str, Any]]) -> None:
    rows = []
    for post in posts:
        posted_by = post.get("posted_by", {})
        row = {
            "topic_id": post.get("topic_id"),
            "thread_name": post.get("thread_name"),
            "post_id": post.get("post_id"),
            "post_number": post.get("post_number"),
            "post_url": post.get("post_url"),
            "username": posted_by.get("username"),
            "name": posted_by.get("name"),
            "posted_at": post.get("posted_at"),
            "updated_at": post.get("updated_at"),
            "like_count": post.get("like_count"),
            "is_solution": post.get("is_solution"),
            "content_text": post.get("content_text"),
            "image_urls": json.dumps(post.get("image_urls") or [], ensure_ascii=False),
            "image_files": json.dumps(post.get("image_files") or [], ensure_ascii=False),
            "llm_used": post.get("llm_used"),
            "llm_confidence": post.get("llm_confidence"),
            "llm_warnings": json.dumps(post.get("llm_warnings") or [], ensure_ascii=False),
            "llm_source": post.get("llm_source"),
        }
        rows.append(row)
    fields = list(rows[0].keys()) if rows else [
        "topic_id",
        "thread_name",
        "post_id",
        "post_number",
        "post_url",
        "username",
        "name",
        "posted_at",
        "updated_at",
        "like_count",
        "is_solution",
        "content_text",
        "image_urls",
        "image_files",
        "llm_used",
        "llm_confidence",
        "llm_warnings",
        "llm_source",
    ]
    _write_csv(path, rows, fields)


def _write_users_csv(path: Path, users: list[dict[str, Any]]) -> None:
    fields = [
        "username",
        "name",
        "title",
        "location",
        "website",
        "created_at",
        "last_seen_at",
        "last_posted_at",
        "trust_level",
        "profile_view_count",
    ]
    _write_csv(path, users, fields)


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
