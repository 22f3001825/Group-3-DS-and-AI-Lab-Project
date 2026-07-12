import json
import tempfile
import unittest
from pathlib import Path

from discourse_exporter.exporter import scrape_category


class UserProfileFailureClient:
    def get_json(self, path):
        if path == "/c/courses/mlt-kb/32.json?page=0":
            return {
                "topic_list": {
                    "topics": [
                        {
                            "id": 300,
                            "slug": "checkpoint-topic",
                            "title": "Checkpoint topic",
                            "bumped_at": "2026-01-01T00:00:00.000Z",
                            "posts_count": 1,
                        }
                    ]
                }
            }
        if path == "/c/courses/mlt-kb/32.json?page=1":
            return {"topic_list": {"topics": []}}
        if path == "/t/300.json":
            return {
                "id": 300,
                "slug": "checkpoint-topic",
                "title": "Checkpoint topic",
                "post_stream": {
                    "posts": [
                        {
                            "id": 301,
                            "post_number": 1,
                            "username": "alice",
                            "created_at": "2026-01-01T00:00:00.000Z",
                            "cooked": "<p>Persist me early</p>",
                        }
                    ]
                },
            }
        if path == "/u/alice.json":
            raise RuntimeError("profile fetch interrupted")
        raise AssertionError(f"Unexpected path: {path}")

    def get_bytes(self, path):
        raise AssertionError(f"Unexpected bytes path: {path}")


class ExporterIncrementalTests(unittest.TestCase):
    def test_export_files_are_written_after_topic_before_user_profiles_finish(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"

            export_result = scrape_category(
                client=UserProfileFailureClient(),
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=output_dir,
                state_path=Path(temp_dir) / "state.json",
                rate_limit_seconds=0,
            )

            export_path = output_dir / "discourse_export.json"
            posts_csv_path = output_dir / "discourse_posts.csv"
            self.assertTrue(export_path.exists())
            self.assertTrue(posts_csv_path.exists())

            export = json.loads(export_path.read_text(encoding="utf-8"))
            self.assertEqual(export["metadata"]["topic_count"], 1)
            self.assertEqual(export["metadata"]["post_count"], 1)
            self.assertEqual(export["topics"][0]["topic_id"], 300)
            self.assertEqual(export["posts"][0]["content_text"], "Persist me early")
            self.assertEqual(export["metadata"]["status"], "complete")
            self.assertEqual(export["metadata"]["profile_error_count"], 1)
            self.assertEqual(export["profile_errors"][0]["username"], "alice")
            self.assertEqual(export_result["metadata"]["profile_error_count"], 1)
            self.assertTrue((output_dir / "profile_errors.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
