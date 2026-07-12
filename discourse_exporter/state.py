from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ExportState:
    topics: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "ExportState":
        if not path.exists():
            return cls()
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _preserve_corrupt_file(path)
            return cls()
        return cls(topics=payload.get("topics", {}))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"topics": self.topics}
        _atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

    def topic_needs_fetch(self, topic_summary: dict[str, Any]) -> bool:
        topic_id = str(topic_summary["id"])
        return self.topics.get(topic_id) != self._signature(topic_summary)

    def mark_topic(self, topic_summary: dict[str, Any]) -> None:
        self.topics[str(topic_summary["id"])] = self._signature(topic_summary)

    def _signature(self, topic_summary: dict[str, Any]) -> dict[str, Any]:
        keys = (
            "bumped_at",
            "last_posted_at",
            "posts_count",
            "highest_post_number",
            "reply_count",
            "updated_at",
        )
        return {key: topic_summary.get(key) for key in keys if key in topic_summary}


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="") as handle:
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
