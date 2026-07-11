import tempfile
import unittest
from pathlib import Path

import requests

from discourse_exporter.exporter import scrape_category


class FakeResponse:
    status_code = 403
    reason = "Forbidden"
    text = "forbidden"


class TopicFetchFailureClient:
    def __init__(self, failures_before_success=None):
        self.bytes_requests = []
        self.topic_207920_attempts = 0
        self.failures_before_success = failures_before_success

    def get_json(self, path):
        if path == "/c/courses/mlt-kb/32.json?page=0":
            return {
                "topic_list": {
                    "topics": [
                        {
                            "id": 207920,
                            "slug": "restricted-topic",
                            "title": "Restricted topic",
                            "bumped_at": "2026-01-01T00:00:00.000Z",
                            "posts_count": 1,
                        },
                        {
                            "id": 207921,
                            "slug": "open-topic",
                            "title": "Open topic",
                            "bumped_at": "2026-01-02T00:00:00.000Z",
                            "posts_count": 1,
                        },
                    ]
                }
            }
        if path == "/c/courses/mlt-kb/32.json?page=1":
            return {"topic_list": {"topics": []}}
        if path == "/t/207920.json":
            self.topic_207920_attempts += 1
            if self.failures_before_success is None or self.topic_207920_attempts <= self.failures_before_success:
                raise requests.exceptions.HTTPError("403 Client Error: Forbidden", response=FakeResponse())
            return {
                "id": 207920,
                "slug": "restricted-topic",
                "title": "Restricted topic",
                "post_stream": {
                    "posts": [
                        {
                            "id": 2,
                            "post_number": 1,
                            "username": "bob",
                            "created_at": "2026-01-01T00:00:00.000Z",
                            "cooked": "<p>Recovered after retry</p>",
                        }
                    ]
                },
            }
        if path == "/t/207921.json":
            return {
                "id": 207921,
                "slug": "open-topic",
                "title": "Open topic",
                "post_stream": {
                    "posts": [
                        {
                            "id": 1,
                            "post_number": 1,
                            "username": "alice",
                            "created_at": "2026-01-02T00:00:00.000Z",
                            "cooked": "<p>Visible body</p>",
                        }
                    ]
                },
            }
        if path == "/u/alice.json":
            return {"user": {"username": "alice", "name": "Alice"}}
        if path == "/u/bob.json":
            return {"user": {"username": "bob", "name": "Bob"}}
        raise AssertionError(f"Unexpected JSON path: {path}")

    def get_bytes(self, path):
        raise AssertionError(f"Unexpected bytes path: {path}")


class ExporterErrorTests(unittest.TestCase):
    def test_forbidden_topic_is_retried_then_recorded_and_scrape_continues(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            state_path = Path(temp_dir) / "state.json"
            client = TopicFetchFailureClient()

            export = scrape_category(
                client=client,
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=output_dir,
                state_path=state_path,
                rate_limit_seconds=0,
                topic_retries=2,
                topic_retry_delay_seconds=0,
            )

            self.assertEqual(client.topic_207920_attempts, 3)
            self.assertEqual(export["metadata"]["topic_count"], 1)
            self.assertEqual(export["metadata"]["topic_error_count"], 1)
            self.assertEqual(export["topics"][0]["topic_id"], 207921)
            self.assertEqual(export["topic_errors"][0]["topic_id"], 207920)
            self.assertEqual(export["topic_errors"][0]["status_code"], 403)
            self.assertEqual(export["topic_errors"][0]["attempt_count"], 3)
            self.assertIn("HTTP 403 Forbidden", (output_dir / "error.log").read_text(encoding="utf-8"))

    def test_forbidden_topic_succeeds_after_retry_without_error_log(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            state_path = Path(temp_dir) / "state.json"
            client = TopicFetchFailureClient(failures_before_success=1)

            export = scrape_category(
                client=client,
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=output_dir,
                state_path=state_path,
                rate_limit_seconds=0,
                topic_retries=2,
                topic_retry_delay_seconds=0,
            )

            self.assertEqual(client.topic_207920_attempts, 2)
            self.assertEqual(export["metadata"]["topic_count"], 2)
            self.assertEqual(export["metadata"]["topic_error_count"], 0)
            self.assertFalse((output_dir / "error.log").exists())


if __name__ == "__main__":
    unittest.main()
