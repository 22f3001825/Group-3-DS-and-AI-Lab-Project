import asyncio
import tempfile
import unittest
from pathlib import Path

from discourse_exporter.exporter import scrape_category


class AsyncConcurrencyClient:
    def __init__(self, topic_count=0, profile_count=0, image_count=0):
        self.topic_count = topic_count
        self.profile_count = profile_count
        self.image_count = image_count
        self.active = 0
        self.max_active = 0
        self.active_by_kind = {"topic": 0, "profile": 0, "image": 0}
        self.max_active_by_kind = {"topic": 0, "profile": 0, "image": 0}

    async def get_json(self, path):
        if path == "/c/courses/mlt-kb/32.json?page=0":
            return {
                "topic_list": {
                    "topics": [
                        {
                            "id": topic_id,
                            "slug": f"topic-{topic_id}",
                            "title": f"Topic {topic_id}",
                            "bumped_at": "2026-01-01T00:00:00.000Z",
                            "posts_count": 1,
                        }
                        for topic_id in range(1, self.topic_count + 1)
                    ]
                }
            }
        if path == "/c/courses/mlt-kb/32.json?page=1":
            return {"topic_list": {"topics": []}}
        if path.startswith("/t/"):
            topic_id = int(path.split("/")[2].split(".")[0])
            await self._track("topic")
            return self._topic_payload(topic_id)
        if path.startswith("/u/"):
            username = path.removeprefix("/u/").removesuffix(".json")
            await self._track("profile")
            return {"user": {"username": username, "name": username.title()}}
        raise AssertionError(f"Unexpected JSON path: {path}")

    async def get_bytes(self, url):
        await self._track("image")
        return b"fake image", "image/png"

    async def _track(self, kind):
        self.active += 1
        self.active_by_kind[kind] += 1
        self.max_active = max(self.max_active, self.active)
        self.max_active_by_kind[kind] = max(self.max_active_by_kind[kind], self.active_by_kind[kind])
        try:
            await asyncio.sleep(0.01)
        finally:
            self.active_by_kind[kind] -= 1
            self.active -= 1

    def _topic_payload(self, topic_id):
        if self.profile_count:
            posts = [
                {
                    "id": 1000 + index,
                    "post_number": index + 1,
                    "username": f"user{index}",
                    "created_at": "2026-01-01T00:00:00.000Z",
                    "cooked": f"<p>Profile post {index}</p>",
                }
                for index in range(self.profile_count)
            ]
        elif self.image_count:
            images = "".join(f'<img src="https://cdn.example.test/{index}.png">' for index in range(self.image_count))
            posts = [
                {
                    "id": 2000,
                    "post_number": 1,
                    "created_at": "2026-01-01T00:00:00.000Z",
                    "cooked": f"<p>Image post</p>{images}",
                }
            ]
        else:
            posts = [
                {
                    "id": 3000 + topic_id,
                    "post_number": 1,
                    "created_at": "2026-01-01T00:00:00.000Z",
                    "cooked": f"<p>Topic post {topic_id}</p>",
                }
            ]
        return {
            "id": topic_id,
            "slug": f"topic-{topic_id}",
            "title": f"Topic {topic_id}",
            "post_stream": {"posts": posts},
        }


class ExporterAsyncConcurrencyTests(unittest.TestCase):
    def test_topic_json_fetches_run_concurrently_with_ten_request_cap(self):
        client = AsyncConcurrencyClient(topic_count=25)

        with tempfile.TemporaryDirectory() as temp_dir:
            export = scrape_category(
                client=client,
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=Path(temp_dir) / "out",
                state_path=Path(temp_dir) / "state.json",
                rate_limit_seconds=0,
            )

        self.assertEqual(export["metadata"]["topic_count"], 25)
        self.assertGreater(client.max_active_by_kind["topic"], 1)
        self.assertLessEqual(client.max_active, 10)

    def test_image_downloads_run_concurrently_with_ten_request_cap(self):
        client = AsyncConcurrencyClient(topic_count=1, image_count=15)

        with tempfile.TemporaryDirectory() as temp_dir:
            export = scrape_category(
                client=client,
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=Path(temp_dir) / "out",
                state_path=Path(temp_dir) / "state.json",
                rate_limit_seconds=0,
            )

        self.assertEqual(len(export["posts"][0]["image_files"]), 15)
        self.assertGreater(client.max_active_by_kind["image"], 1)
        self.assertLessEqual(client.max_active, 10)

    def test_user_profiles_run_concurrently_with_ten_request_cap(self):
        client = AsyncConcurrencyClient(topic_count=1, profile_count=18)

        with tempfile.TemporaryDirectory() as temp_dir:
            export = scrape_category(
                client=client,
                base_url="https://discourse.onlinedegree.iitm.ac.in",
                category_path="/c/courses/mlt-kb/32",
                output_dir=Path(temp_dir) / "out",
                state_path=Path(temp_dir) / "state.json",
                rate_limit_seconds=0,
            )

        self.assertEqual(export["metadata"]["user_count"], 18)
        self.assertGreater(client.max_active_by_kind["profile"], 1)
        self.assertLessEqual(client.max_active, 10)


if __name__ == "__main__":
    unittest.main()
