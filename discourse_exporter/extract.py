from __future__ import annotations

import re
from html import unescape
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup


LIKE_ACTION_ID = 2


def extract_image_sources(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html or "", "html.parser")
    urls: list[str] = []

    for image in soup.find_all("img"):
        for attr in ("src", "data-src", "data-original-src"):
            value = image.get(attr)
            if value:
                _append_unique(urls, urljoin(base_url, value))

        srcset = image.get("srcset")
        if srcset:
            for src in _parse_srcset(srcset):
                _append_unique(urls, urljoin(base_url, src))

    return urls


def like_count_from_post(post: dict[str, Any]) -> int:
    if isinstance(post.get("like_count"), int):
        return post["like_count"]
    for action in post.get("actions_summary") or []:
        if action.get("id") == LIKE_ACTION_ID:
            return int(action.get("count") or 0)
    return 0


def is_solution_post(post: dict[str, Any], topic: dict[str, Any]) -> bool:
    explicit_flags = (
        post.get("accepted_answer"),
        post.get("is_accepted_answer"),
        post.get("is_solution"),
        post.get("solution"),
    )
    if any(flag is True for flag in explicit_flags):
        return True

    post_id = post.get("id")
    post_number = post.get("post_number")
    solution_post_ids = {
        topic.get("accepted_answer_post_id"),
        topic.get("solution_post_id"),
        topic.get("solved_post_id"),
    }
    solution_post_numbers = {
        topic.get("accepted_answer"),
        topic.get("solution_post_number"),
    }
    return post_id in solution_post_ids or post_number in solution_post_numbers


def extract_topic_records(topic: dict[str, Any], base_url: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    topic_id = topic["id"]
    slug = topic.get("slug") or str(topic_id)
    url = f"{base_url.rstrip('/')}/t/{slug}/{topic_id}"
    posts = topic.get("post_stream", {}).get("posts") or []

    topic_record = {
        "topic_id": topic_id,
        "thread_name": topic.get("title") or "",
        "slug": slug,
        "url": url,
        "created_at": topic.get("created_at"),
        "updated_at": topic.get("updated_at"),
        "last_posted_at": topic.get("last_posted_at"),
        "bumped_at": topic.get("bumped_at"),
        "posts_count": topic.get("posts_count"),
        "reply_count": topic.get("reply_count"),
        "views": topic.get("views"),
        "like_count": topic.get("like_count"),
        "accepted_answer_post_id": topic.get("accepted_answer_post_id"),
        "accepted_answer_post_number": topic.get("accepted_answer"),
    }

    post_records = [_post_record(topic_record, topic, post, base_url) for post in posts]
    return topic_record, post_records


def cooked_to_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def _post_record(
    topic_record: dict[str, Any],
    topic: dict[str, Any],
    post: dict[str, Any],
    base_url: str,
) -> dict[str, Any]:
    cooked = post.get("cooked") or ""
    post_number = post.get("post_number")
    post_url = f"{topic_record['url']}/{post_number}" if post_number else topic_record["url"]
    return {
        "topic_id": topic_record["topic_id"],
        "thread_name": topic_record["thread_name"],
        "thread_url": topic_record["url"],
        "post_id": post.get("id"),
        "post_number": post_number,
        "post_url": post_url,
        "posted_by": {
            "user_id": post.get("user_id"),
            "username": post.get("username"),
            "display_username": post.get("display_username"),
            "name": post.get("name"),
            "title": post.get("user_title"),
            "primary_group_name": post.get("primary_group_name"),
            "flair_name": post.get("flair_name"),
            "avatar_template": post.get("avatar_template"),
        },
        "posted_at": post.get("created_at"),
        "updated_at": post.get("updated_at"),
        "version": post.get("version"),
        "like_count": like_count_from_post(post),
        "is_solution": is_solution_post(post, topic),
        "content_html": cooked,
        "content_text": cooked_to_text(cooked),
        "image_urls": extract_image_sources(cooked, base_url),
        "image_files": [],
        "raw_post": post,
    }


def _parse_srcset(srcset: str) -> list[str]:
    urls: list[str] = []
    for candidate in srcset.split(","):
        parts = candidate.strip().split()
        if parts:
            urls.append(parts[0])
    return urls


def _append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)
