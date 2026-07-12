import tempfile
import unittest
from pathlib import Path

import httpx

from discourse_exporter.exporter import scrape_category


def forbidden_error():
    request = httpx.Request("GET", "https://discourse.onlinedegree.iitm.ac.in/t/207920.json")
    response = httpx.Response(403, request=request)
    return httpx.HTTPStatusError("403 Client Error: Forbidden", request=request, response=response)


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
                raise forbidden_error()
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


class LongTopicAndBrokenImageClient:
    def __init__(self):
        self.additional_posts_requested = []

    def get_json(self, path):
        if path == "/c/courses/mlt-kb/32.json?page=0":
            return {
                "topic_list": {
                    "topics": [
                        {
                            "id": 400,
                            "slug": "long-topic",
                            "title": "Long topic",
                            "bumped_at": "2026-01-01T00:00:00.000Z",
                            "posts_count": 3,
                        }
                    ]
                }
            }
        if path == "/c/courses/mlt-kb/32.json?page=1":
            return {"topic_list": {"topics": []}}
        if path == "/t/400.json":
            return {
                "id": 400,
                "slug": "long-topic",
                "title": "Long topic",
                "post_stream": {
                    "stream": [1, 2, 3],
                    "posts": [
                        {
                            "id": 1,
                            "post_number": 1,
                            "username": "alice",
                            "created_at": "2026-01-01T00:00:00.000Z",
                            "cooked": '<p>First</p><img src="https://cdn.example.test/broken.png">',
                        }
                    ],
                },
            }
        if path.startswith("/t/400/posts.json?"):
            self.additional_posts_requested.append(path)
            return {
                "post_stream": {
                    "posts": [
                        {
                            "id": 2,
                            "post_number": 2,
                            "username": "bob",
                            "created_at": "2026-01-02T00:00:00.000Z",
                            "cooked": "<p>Second</p>",
                        },
                        {
                            "id": 3,
                            "post_number": 3,
                            "username": "carol",
                            "created_at": "2026-01-03T00:00:00.000Z",
                            "cooked": "<p>Third</p>",
                        },
                    ]
                }
            }
        if path.startswith("/u/"):
            username = path.removeprefix("/u/").removesuffix(".json")
            return {"user": {"username": username}}
        raise AssertionError(f"Unexpected JSON path: {path}")

    def get_bytes(self, path):
        raise forbidden_error()


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

    def test_long_topic_fetches_missing_posts_and_image_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            client = LongTopicAndBrokenImageClient()

            export = scrape_category(
                client=client,
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=output_dir,
                state_path=Path(temp_dir) / "state.json",
                rate_limit_seconds=0,
                topic_retry_delay_seconds=0,
            )

            self.assertEqual(export["metadata"]["post_count"], 3)
            self.assertEqual([post["post_id"] for post in export["posts"]], [1, 2, 3])
            self.assertEqual(len(client.additional_posts_requested), 1)
            self.assertEqual(len(export["posts"][0]["image_errors"]), 1)
            self.assertTrue((output_dir / "image_errors.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
