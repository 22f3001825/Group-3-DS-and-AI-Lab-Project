from __future__ import annotations

import asyncio
import csv
import hashlib
import inspect
import io
import json
import mimetypes
import os
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode, urlparse

import httpx

from .extract import extract_topic_records
from .llm import apply_llm_result_to_post, mark_llm_not_used, post_needs_llm_fallback
from .state import ExportState


DEFAULT_AUXILIARY_RETRIES = 2
CHECKPOINT_EVERY_ITEMS = 10
CHECKPOINT_INTERVAL_SECONDS = 5.0
POSTS_PER_STREAM_REQUEST = 20


@dataclass
class CheckpointTracker:
    pending_items: int = 0
    last_snapshot_at: float = field(default_factory=time.monotonic)

    def record_change(self) -> None:
        self.pending_items += 1

    def should_snapshot(self) -> bool:
        return (
            self.pending_items >= CHECKPOINT_EVERY_ITEMS
            or time.monotonic() - self.last_snapshot_at >= CHECKPOINT_INTERVAL_SECONDS
        )

    def mark_snapshot(self) -> None:
        self.pending_items = 0
        self.last_snapshot_at = time.monotonic()


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
    max_concurrent_requests: int = 10,
) -> dict[str, Any]:
    return asyncio.run(
        scrape_category_async(
            client=client,
            base_url=base_url,
            category_path=category_path,
            output_dir=output_dir,
            state_path=state_path,
            max_pages=max_pages,
            rate_limit_seconds=rate_limit_seconds,
            refresh_users=refresh_users,
            llm_fallback=llm_fallback,
            llm_client=llm_client,
            topic_retries=topic_retries,
            topic_retry_delay_seconds=topic_retry_delay_seconds,
            max_concurrent_requests=max_concurrent_requests,
        )
    )


async def scrape_category_async(
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
    max_concurrent_requests: int = 10,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    image_dir = output_dir / "imgs"
    image_dir.mkdir(parents=True, exist_ok=True)

    request_semaphore = asyncio.Semaphore(max(1, max_concurrent_requests))
    write_lock = asyncio.Lock()

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
    profile_errors_by_username = {
        str(error["username"]): error
        for error in export.get("profile_errors", [])
        if error.get("username")
    }
    state = ExportState.load(state_path)
    checkpoint_tracker = CheckpointTracker()

    page_number = 0
    async for topic_summaries in _iter_category_pages_async(client, category_path, max_pages, request_semaphore):
        print(f"Category page {page_number}: {len(topic_summaries)} topics")
        pending_topics = []
        for topic_summary in topic_summaries:
            topic_id = str(topic_summary["id"])
            existing_topic = topic_id in topics_by_id
            if existing_topic and not state.topic_needs_fetch(topic_summary):
                continue
            pending_topics.append(topic_summary)

        await _bounded_map(
            pending_topics,
            lambda topic_summary: _process_topic(
                client=client,
                base_url=base_url,
                category_path=category_path,
                output_dir=output_dir,
                image_dir=image_dir,
                state_path=state_path,
                topic_summary=topic_summary,
                topics_by_id=topics_by_id,
                posts_by_id=posts_by_id,
                users_by_username=users_by_username,
                topic_errors_by_id=topic_errors_by_id,
                profile_errors_by_username=profile_errors_by_username,
                state=state,
                checkpoint_tracker=checkpoint_tracker,
                llm_fallback=llm_fallback,
                llm_client=llm_client,
                topic_retries=topic_retries,
                topic_retry_delay_seconds=topic_retry_delay_seconds,
                rate_limit_seconds=rate_limit_seconds,
                request_semaphore=request_semaphore,
                write_lock=write_lock,
                max_in_flight=max_concurrent_requests,
            ),
            max_in_flight=max_concurrent_requests,
        )

        async with write_lock:
            state.save(state_path)
            _write_export_checkpoint(
                output_dir=output_dir,
                base_url=base_url,
                category_path=category_path,
                topics_by_id=topics_by_id,
                posts_by_id=posts_by_id,
                users_by_username=users_by_username,
                topic_errors_by_id=topic_errors_by_id,
                profile_errors_by_username=profile_errors_by_username,
                status="partial",
            )
            checkpoint_tracker.mark_snapshot()
        page_number += 1

    usernames = sorted(
        {
            post.get("posted_by", {}).get("username")
            for post in posts_by_id.values()
            if post.get("posted_by", {}).get("username")
        }
    )
    pending_usernames = [
        username for username in usernames if refresh_users or username not in users_by_username
    ]
    await _bounded_map(
        pending_usernames,
        lambda username: _process_user_profile(
            client=client,
            username=username,
            output_dir=output_dir,
            base_url=base_url,
            category_path=category_path,
            topics_by_id=topics_by_id,
            posts_by_id=posts_by_id,
            users_by_username=users_by_username,
            topic_errors_by_id=topic_errors_by_id,
            profile_errors_by_username=profile_errors_by_username,
            checkpoint_tracker=checkpoint_tracker,
            rate_limit_seconds=rate_limit_seconds,
            request_semaphore=request_semaphore,
            write_lock=write_lock,
        ),
        max_in_flight=max_concurrent_requests,
    )

    async with write_lock:
        export = _write_export_checkpoint(
            output_dir=output_dir,
            base_url=base_url,
            category_path=category_path,
            topics_by_id=topics_by_id,
            posts_by_id=posts_by_id,
            users_by_username=users_by_username,
            topic_errors_by_id=topic_errors_by_id,
            profile_errors_by_username=profile_errors_by_username,
            status="complete",
        )
        state.save(state_path)
    return export


async def _process_topic(
    client,
    base_url: str,
    category_path: str,
    output_dir: Path,
    image_dir: Path,
    state_path: Path,
    topic_summary: dict[str, Any],
    topics_by_id: dict[str, dict[str, Any]],
    posts_by_id: dict[str, dict[str, Any]],
    users_by_username: dict[str, dict[str, Any]],
    topic_errors_by_id: dict[str, dict[str, Any]],
    profile_errors_by_username: dict[str, dict[str, Any]],
    state: ExportState,
    checkpoint_tracker: CheckpointTracker,
    llm_fallback: str,
    llm_client,
    topic_retries: int,
    topic_retry_delay_seconds: float,
    rate_limit_seconds: float,
    request_semaphore: asyncio.Semaphore,
    write_lock: asyncio.Lock,
    max_in_flight: int,
) -> None:
    topic_id = str(topic_summary["id"])
    try:
        topic_json = await _get_complete_topic_json_async(
            client=client,
            topic_id=topic_id,
            topic_retries=topic_retries,
            retry_delay_seconds=topic_retry_delay_seconds,
            request_semaphore=request_semaphore,
        )
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        error_record = _topic_error_record(
            topic_summary,
            base_url,
            exc,
            attempt_count=max(0, topic_retries) + 1,
        )
        async with write_lock:
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
                profile_errors_by_username=profile_errors_by_username,
                status="partial",
            )
            _append_jsonl(output_dir / "topic_journal.jsonl", {"status": "error", **error_record})
            checkpoint_tracker.record_change()
        print(
            f"Skipping topic {topic_id}: "
            f"HTTP {error_record.get('status_code') or 'error'} {error_record.get('reason') or ''}".rstrip()
        )
        if rate_limit_seconds > 0:
            await asyncio.sleep(rate_limit_seconds)
        return

    topic_record, post_records = extract_topic_records(topic_json, base_url)

    await apply_llm_fallback_to_posts_async(
        post_records,
        llm_client=llm_client,
        mode=llm_fallback,
        audit_log_path=output_dir / "llm_fallback_log.jsonl",
        request_semaphore=request_semaphore,
        write_lock=write_lock,
        max_in_flight=max_in_flight,
    )

    await _bounded_map(
        post_records,
        lambda post: _attach_post_images(
            client,
            output_dir,
            image_dir,
            post,
            request_semaphore,
            write_lock,
            max_in_flight,
        ),
        max_in_flight=max_in_flight,
    )

    async with write_lock:
        topics_by_id[topic_id] = topic_record
        topic_errors_by_id.pop(topic_id, None)

        stale_post_ids = [
            post_id
            for post_id, post in posts_by_id.items()
            if str(post.get("topic_id")) == topic_id
        ]
        for post_id in stale_post_ids:
            posts_by_id.pop(post_id, None)

        for post in post_records:
            posts_by_id[str(post["post_id"])] = post

        state.mark_topic(topic_summary)
        state.save(state_path)
        _append_jsonl(
            output_dir / "topic_journal.jsonl",
            {"status": "complete", "topic": topic_record, "posts": post_records},
        )
        checkpoint_tracker.record_change()
        if checkpoint_tracker.should_snapshot():
            _write_export_checkpoint(
                output_dir=output_dir,
                base_url=base_url,
                category_path=category_path,
                topics_by_id=topics_by_id,
                posts_by_id=posts_by_id,
                users_by_username=users_by_username,
                topic_errors_by_id=topic_errors_by_id,
                profile_errors_by_username=profile_errors_by_username,
                status="partial",
            )
            checkpoint_tracker.mark_snapshot()

    if rate_limit_seconds > 0:
        await asyncio.sleep(rate_limit_seconds)


async def _process_user_profile(
    client,
    username: str,
    output_dir: Path,
    base_url: str,
    category_path: str,
    topics_by_id: dict[str, dict[str, Any]],
    posts_by_id: dict[str, dict[str, Any]],
    users_by_username: dict[str, dict[str, Any]],
    topic_errors_by_id: dict[str, dict[str, Any]],
    profile_errors_by_username: dict[str, dict[str, Any]],
    checkpoint_tracker: CheckpointTracker,
    rate_limit_seconds: float,
    request_semaphore: asyncio.Semaphore,
    write_lock: asyncio.Lock,
) -> None:
    try:
        profile = await _fetch_user_profile_async(client, username, request_semaphore)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        error_record = _profile_error_record(base_url, username, exc, DEFAULT_AUXILIARY_RETRIES + 1)
        async with write_lock:
            profile_errors_by_username[username] = error_record
            _append_jsonl(output_dir / "profile_errors.jsonl", error_record)
            _append_error_log(output_dir / "error.log", error_record)
            _append_jsonl(output_dir / "profile_journal.jsonl", {"status": "error", **error_record})
            checkpoint_tracker.record_change()
        print(f"Skipping profile {username}: {error_record.get('error')}")
        return

    async with write_lock:
        users_by_username[username] = profile
        profile_errors_by_username.pop(username, None)
        _append_jsonl(output_dir / "profile_journal.jsonl", {"status": "complete", "user": profile})
        checkpoint_tracker.record_change()
        if checkpoint_tracker.should_snapshot():
            _write_export_checkpoint(
                output_dir=output_dir,
                base_url=base_url,
                category_path=category_path,
                topics_by_id=topics_by_id,
                posts_by_id=posts_by_id,
                users_by_username=users_by_username,
                topic_errors_by_id=topic_errors_by_id,
                profile_errors_by_username=profile_errors_by_username,
                status="partial",
            )
            checkpoint_tracker.mark_snapshot()
    if rate_limit_seconds > 0:
        await asyncio.sleep(rate_limit_seconds)


def apply_llm_fallback_to_posts(
    posts: list[dict[str, Any]],
    llm_client,
    mode: str,
    audit_log_path: Path,
) -> None:
    asyncio.run(
        apply_llm_fallback_to_posts_async(
            posts=posts,
            llm_client=llm_client,
            mode=mode,
            audit_log_path=audit_log_path,
        )
    )


async def apply_llm_fallback_to_posts_async(
    posts: list[dict[str, Any]],
    llm_client,
    mode: str,
    audit_log_path: Path,
    request_semaphore: asyncio.Semaphore | None = None,
    write_lock: asyncio.Lock | None = None,
    max_in_flight: int = 10,
) -> None:
    if mode not in {"off", "missing", "always"}:
        raise ValueError("llm fallback mode must be one of: off, missing, always")

    if mode == "off":
        for post in posts:
            mark_llm_not_used(post)
        return

    if llm_client is None:
        raise ValueError("llm_client is required when llm fallback mode is not off")

    request_semaphore = request_semaphore or asyncio.Semaphore(10)
    write_lock = write_lock or asyncio.Lock()
    await _bounded_map(
        posts,
        lambda post: _apply_llm_fallback_to_post(
            post, llm_client, mode, audit_log_path, request_semaphore, write_lock
        ),
        max_in_flight=max_in_flight,
    )


async def _apply_llm_fallback_to_post(
    post: dict[str, Any],
    llm_client,
    mode: str,
    audit_log_path: Path,
    request_semaphore: asyncio.Semaphore,
    write_lock: asyncio.Lock,
) -> None:
    should_run = mode == "always" or post_needs_llm_fallback(post)
    if not should_run:
        mark_llm_not_used(post)
        return

    source = f"topic:{post.get('topic_id')} post:{post.get('post_id')}"
    try:
        result = await _llm_extract_post(llm_client, post, request_semaphore)
        apply_llm_result_to_post(post, result, source=source)
        async with write_lock:
            _append_llm_audit_log(audit_log_path, post, mode, result=result)
    except Exception as exc:
        post["llm_used"] = False
        post["llm_confidence"] = None
        post["llm_warnings"] = [f"LLM fallback failed: {exc}"]
        post["llm_source"] = source
        post["llm_fields"] = {}
        async with write_lock:
            _append_llm_audit_log(audit_log_path, post, mode, error=str(exc))


async def _iter_category_pages_async(
    client,
    category_path: str,
    max_pages: int | None,
    request_semaphore: asyncio.Semaphore,
):
    page = 0
    seen_ids: set[int] = set()
    while max_pages is None or page < max_pages:
        separator = "&" if "?" in category_path else "?"
        payload = await _get_json_with_retries_async(
            client=client,
            path=f"{category_path}.json{separator}page={page}",
            resource_label=f"category page {page}",
            retries=DEFAULT_AUXILIARY_RETRIES,
            retry_delay_seconds=1.0,
            request_semaphore=request_semaphore,
        )
        topics = payload.get("topic_list", {}).get("topics") or []
        topics = [topic for topic in topics if topic.get("id") not in seen_ids]
        if not topics:
            break
        for topic in topics:
            seen_ids.add(topic["id"])
        yield topics
        page += 1


async def _get_json_with_retries_async(
    client,
    path: str,
    resource_label: str,
    retries: int,
    retry_delay_seconds: float,
    request_semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    total_attempts = max(0, retries) + 1
    for attempt in range(1, total_attempts + 1):
        try:
            return await _client_get_json(client, path, request_semaphore)
        except httpx.HTTPError as exc:
            if attempt >= total_attempts or not _should_retry(exc):
                raise
            status_code, reason = _response_status(exc)
            status = f"HTTP {status_code} {reason}".strip() if status_code else "request error"
            print(f"Retrying {resource_label} after {status} (attempt {attempt}/{total_attempts})")
            await asyncio.sleep(_retry_delay_seconds(exc, retry_delay_seconds, attempt))

    raise RuntimeError("unreachable retry loop state")


async def _get_complete_topic_json_async(
    client,
    topic_id: str,
    topic_retries: int,
    retry_delay_seconds: float,
    request_semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    topic = await _get_json_with_retries_async(
        client=client,
        path=f"/t/{topic_id}.json",
        resource_label=f"topic {topic_id}",
        retries=topic_retries,
        retry_delay_seconds=retry_delay_seconds,
        request_semaphore=request_semaphore,
    )
    post_stream = topic.get("post_stream") or {}
    loaded_posts = post_stream.get("posts") or []
    stream_ids = post_stream.get("stream") or [post.get("id") for post in loaded_posts]
    loaded_ids = {post.get("id") for post in loaded_posts}
    missing_ids = [post_id for post_id in stream_ids if post_id not in loaded_ids]

    for post_ids in _chunked(missing_ids, POSTS_PER_STREAM_REQUEST):
        query = urlencode([("post_ids[]", post_id) for post_id in post_ids])
        payload = await _get_json_with_retries_async(
            client=client,
            path=f"/t/{topic_id}/posts.json?{query}",
            resource_label=f"topic {topic_id} posts",
            retries=topic_retries,
            retry_delay_seconds=retry_delay_seconds,
            request_semaphore=request_semaphore,
        )
        extra_posts = payload.get("post_stream", {}).get("posts") or payload.get("posts") or []
        loaded_posts.extend(extra_posts)

    posts_by_id = {post.get("id"): post for post in loaded_posts if post.get("id") is not None}
    ordered_ids = list(dict.fromkeys(stream_ids))
    post_stream["posts"] = [posts_by_id[post_id] for post_id in ordered_ids if post_id in posts_by_id]
    post_stream["stream"] = ordered_ids
    topic["post_stream"] = post_stream
    return topic


def _chunked(values: list[Any], chunk_size: int) -> list[list[Any]]:
    return [values[index : index + chunk_size] for index in range(0, len(values), chunk_size)]


def _should_retry(exc: httpx.HTTPError) -> bool:
    response = getattr(exc, "response", None)
    if response is None:
        return True
    status_code = response.status_code
    return status_code in {403, 408, 425, 429} or status_code >= 500


def _retry_delay_seconds(exc: httpx.HTTPError, base_delay: float, attempt: int) -> float:
    response = getattr(exc, "response", None)
    retry_after = response.headers.get("retry-after") if response is not None else None
    if retry_after:
        try:
            return max(0.0, float(retry_after))
        except ValueError:
            pass
    if base_delay <= 0:
        return 0.0
    return base_delay * (2 ** (attempt - 1)) + random.uniform(0, base_delay / 4)


def _topic_error_record(
    topic_summary: dict[str, Any],
    base_url: str,
    exc: Exception,
    attempt_count: int,
) -> dict[str, Any]:
    topic_id = topic_summary.get("id")
    slug = topic_summary.get("slug") or str(topic_id)
    status_code, reason = _response_status(exc)
    return {
        "topic_id": topic_id,
        "thread_name": topic_summary.get("title") or "",
        "slug": slug,
        "url": f"{base_url.rstrip('/')}/t/{slug}/{topic_id}",
        "status_code": status_code,
        "reason": reason,
        "attempt_count": attempt_count,
        "error": str(exc),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def _profile_error_record(base_url: str, username: str, exc: Exception, attempt_count: int) -> dict[str, Any]:
    status_code, reason = _response_status(exc)
    return {
        "resource_type": "profile",
        "username": username,
        "url": f"{base_url.rstrip('/')}/u/{quote(username)}",
        "status_code": status_code,
        "reason": reason,
        "attempt_count": attempt_count,
        "error": str(exc),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def _response_status(exc: Exception) -> tuple[int | None, str | None]:
    response = getattr(exc, "response", None)
    return (
        getattr(response, "status_code", None),
        getattr(response, "reason_phrase", None) or getattr(response, "reason", None),
    )


def _append_topic_error_log(path: Path, error_record: dict[str, Any]) -> None:
    _append_jsonl(path, error_record)


def _append_jsonl(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _append_error_log(path: Path, error_record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_code = error_record.get("status_code") or "error"
    reason = error_record.get("reason") or ""
    status = f"HTTP {status_code} {reason}".strip()
    identifier = error_record.get("topic_id") or error_record.get("username") or "unknown"
    resource_type = error_record.get("resource_type") or "topic"
    line = (
        f"{error_record.get('recorded_at')} | {resource_type}={identifier} | "
        f"attempts={error_record.get('attempt_count')} | {status} | "
        f"{error_record.get('thread_name') or ''} | {error_record.get('url')} | {error_record.get('error')}"
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())


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
    _append_jsonl(path, entry)


async def _fetch_user_profile_async(
    client,
    username: str,
    request_semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    payload = await _get_json_with_retries_async(
        client=client,
        path=f"/u/{quote(username)}.json",
        resource_label=f"profile {username}",
        retries=DEFAULT_AUXILIARY_RETRIES,
        retry_delay_seconds=1.0,
        request_semaphore=request_semaphore,
    )
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


async def _attach_post_images(
    client,
    output_dir: Path,
    image_dir: Path,
    post: dict[str, Any],
    request_semaphore: asyncio.Semaphore,
    write_lock: asyncio.Lock,
    max_in_flight: int,
) -> None:
    image_files, image_errors = await _download_post_images_async(
        client,
        output_dir,
        image_dir,
        post,
        request_semaphore,
        write_lock,
        max_in_flight,
    )
    post["image_files"] = image_files
    post["image_errors"] = image_errors


async def _download_post_images_async(
    client,
    output_dir: Path,
    image_dir: Path,
    post: dict[str, Any],
    request_semaphore: asyncio.Semaphore,
    write_lock: asyncio.Lock,
    max_in_flight: int,
) -> tuple[list[str], list[dict[str, Any]]]:
    image_requests = list(enumerate(post.get("image_urls") or [], start=1))
    results = await _bounded_map(
        image_requests,
        lambda item: _download_single_image(
            client,
            output_dir,
            image_dir,
            post,
            item[0],
            item[1],
            request_semaphore,
            write_lock,
        ),
        max_in_flight=max_in_flight,
    )
    image_files = [result["file"] for result in results if result.get("file")]
    image_errors = [result["error"] for result in results if result.get("error")]
    return image_files, image_errors


async def _download_single_image(
    client,
    output_dir: Path,
    image_dir: Path,
    post: dict[str, Any],
    index: int,
    url: str,
    request_semaphore: asyncio.Semaphore,
    write_lock: asyncio.Lock,
) -> dict[str, Any]:
    try:
        content, content_type = await _get_bytes_with_retries_async(
            client=client,
            url=url,
            resource_label=f"image for topic {post.get('topic_id')} post {post.get('post_id')}",
            retries=DEFAULT_AUXILIARY_RETRIES,
            retry_delay_seconds=1.0,
            request_semaphore=request_semaphore,
        )
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        status_code, reason = _response_status(exc)
        error_record = {
            "resource_type": "image",
            "topic_id": post.get("topic_id"),
            "post_id": post.get("post_id"),
            "url": url,
            "status_code": status_code,
            "reason": reason,
            "attempt_count": DEFAULT_AUXILIARY_RETRIES + 1,
            "error": str(exc),
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        async with write_lock:
            _append_jsonl(output_dir / "image_errors.jsonl", error_record)
            _append_error_log(output_dir / "error.log", error_record)
        return {"file": None, "error": error_record}

    filename = _image_filename(post, index, url, content_type)
    destination = image_dir / filename
    async with write_lock:
        if not destination.exists():
            _atomic_write_bytes(destination, content)
    return {"file": f"imgs/{filename}", "error": None}


def _image_filename(post: dict[str, Any], index: int, url: str, content_type: str) -> str:
    parsed = urlparse(url)
    extension = Path(parsed.path).suffix.lower()
    if not extension:
        extension = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".bin"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    topic_id = post.get("topic_id") or "topic"
    post_id = post.get("post_id") or "post"
    return f"topic-{topic_id}-post-{post_id}-{index:02d}-{digest}{extension}"


async def _client_get_json(client, path: str, request_semaphore: asyncio.Semaphore) -> dict[str, Any]:
    async with request_semaphore:
        return await _maybe_await(client.get_json(path))


async def _client_get_bytes(client, url: str, request_semaphore: asyncio.Semaphore) -> tuple[bytes, str]:
    async with request_semaphore:
        return await _maybe_await(client.get_bytes(url))


async def _get_bytes_with_retries_async(
    client,
    url: str,
    resource_label: str,
    retries: int,
    retry_delay_seconds: float,
    request_semaphore: asyncio.Semaphore,
) -> tuple[bytes, str]:
    total_attempts = max(0, retries) + 1
    for attempt in range(1, total_attempts + 1):
        try:
            return await _client_get_bytes(client, url, request_semaphore)
        except httpx.HTTPError as exc:
            if attempt >= total_attempts or not _should_retry(exc):
                raise
            status_code, reason = _response_status(exc)
            status = f"HTTP {status_code} {reason}".strip() if status_code else "request error"
            print(f"Retrying {resource_label} after {status} (attempt {attempt}/{total_attempts})")
            await asyncio.sleep(_retry_delay_seconds(exc, retry_delay_seconds, attempt))


async def _llm_extract_post(llm_client, post: dict[str, Any], request_semaphore: asyncio.Semaphore):
    async with request_semaphore:
        return await _maybe_await(llm_client.extract_post(post))


async def _maybe_await(value):
    if inspect.isawaitable(value):
        return await value
    return value


async def _bounded_map(items: list[Any], operation, max_in_flight: int) -> list[Any]:
    if not items:
        return []

    iterator = iter(enumerate(items))
    pending: set[asyncio.Task] = set()
    results: list[Any] = [None] * len(items)

    async def run_one(index: int, item: Any) -> tuple[int, Any]:
        return index, await operation(item)

    def start_next() -> bool:
        try:
            index, item = next(iterator)
        except StopIteration:
            return False
        pending.add(asyncio.create_task(run_one(index, item)))
        return True

    for _ in range(min(max(1, max_in_flight), len(items))):
        start_next()

    try:
        while pending:
            completed, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in completed:
                index, result = task.result()
                results[index] = result
                start_next()
    except BaseException:
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        raise
    return results


def _write_export_checkpoint(
    output_dir: Path,
    base_url: str,
    category_path: str,
    topics_by_id: dict[str, dict[str, Any]],
    posts_by_id: dict[str, dict[str, Any]],
    users_by_username: dict[str, dict[str, Any]],
    topic_errors_by_id: dict[str, dict[str, Any]],
    profile_errors_by_username: dict[str, dict[str, Any]],
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
            "profile_error_count": len(profile_errors_by_username),
        },
        "topics": sorted(topics_by_id.values(), key=lambda item: item["topic_id"]),
        "posts": sorted(posts_by_id.values(), key=lambda item: (item["topic_id"], item.get("post_number") or 0)),
        "users": sorted(users_by_username.values(), key=lambda item: item.get("username") or ""),
        "topic_errors": sorted(topic_errors_by_id.values(), key=lambda item: item["topic_id"]),
        "profile_errors": sorted(profile_errors_by_username.values(), key=lambda item: item["username"]),
    }

    _write_json(output_dir / "discourse_export.json", export)
    _write_topics_csv(output_dir / "discourse_topics.csv", export["topics"])
    _write_posts_csv(output_dir / "discourse_posts.csv", export["posts"])
    _write_users_csv(output_dir / "discourse_users.csv", export["users"])
    return export


def _load_existing_export(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"topics": [], "posts": [], "users": [], "topic_errors": [], "profile_errors": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        _preserve_corrupt_file(path)
        return {"topics": [], "posts": [], "users": [], "topic_errors": [], "profile_errors": []}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2))


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
        "stream_post_count",
        "exported_post_count",
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
            "image_errors": json.dumps(post.get("image_errors") or [], ensure_ascii=False),
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
        "image_errors",
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
    content = io.StringIO(newline="")
    writer = csv.DictWriter(content, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    _atomic_write_text(path, content.getvalue(), encoding="utf-8-sig")


def _atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    _atomic_write_bytes(path, content.encode(encoding))


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary_path.open("wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink(missing_ok=True)


def _preserve_corrupt_file(path: Path) -> Path:
    preserved_path = path.with_name(f"{path.stem}.corrupt-{uuid.uuid4().hex[:8]}{path.suffix}")
    os.replace(path, preserved_path)
    return preserved_path
