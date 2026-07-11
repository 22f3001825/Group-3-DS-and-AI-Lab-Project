from __future__ import annotations

import json
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
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(topics=payload.get("topics", {}))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"topics": self.topics}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

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
