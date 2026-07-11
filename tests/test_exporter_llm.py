import json
import tempfile
import unittest
from pathlib import Path

from discourse_exporter.exporter import apply_llm_fallback_to_posts
from discourse_exporter.llm import normalize_llm_response


class FakeLLMClient:
    def __init__(self):
        self.calls = []

    def extract_post(self, post):
        self.calls.append(post["post_id"])
        return normalize_llm_response(
            {
                "confidence": 0.6,
                "fields": {
                    "content_text": {"value": "Recovered", "evidence": "Recovered"},
                },
                "warnings": ["used fallback"],
            }
        )


class ExporterLLMTests(unittest.TestCase):
    def test_missing_mode_only_calls_llm_for_incomplete_posts_and_logs_result(self):
        posts = [
            {"post_id": 1, "topic_id": 10, "thread_name": "T", "posted_at": "2026", "content_text": "", "posted_by": {"username": "alice"}},
            {"post_id": 2, "topic_id": 10, "thread_name": "T", "posted_at": "2026", "content_text": "Complete", "posted_by": {"username": "bob"}},
        ]
        llm_client = FakeLLMClient()

        with tempfile.TemporaryDirectory() as temp_dir:
            audit_log = Path(temp_dir) / "llm_fallback_log.jsonl"

            apply_llm_fallback_to_posts(posts, llm_client, mode="missing", audit_log_path=audit_log)

            self.assertEqual(llm_client.calls, [1])
            self.assertEqual(posts[0]["content_text"], "Recovered")
            self.assertTrue(posts[0]["llm_used"])
            self.assertFalse(posts[1]["llm_used"])

            log_entries = [json.loads(line) for line in audit_log.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(log_entries[0]["post_id"], 1)
            self.assertEqual(log_entries[0]["fields"]["content_text"]["value"], "Recovered")


if __name__ == "__main__":
    unittest.main()
