import tempfile
import unittest
from pathlib import Path

from discourse_exporter.state import ExportState


class StateTests(unittest.TestCase):
    def test_topic_needs_fetch_until_marked_with_same_signature(self):
        state = ExportState()
        topic = {
            "id": 123,
            "bumped_at": "2026-01-03T00:00:00.000Z",
            "last_posted_at": "2026-01-03T00:00:00.000Z",
            "posts_count": 2,
            "highest_post_number": 2,
        }

        self.assertTrue(state.topic_needs_fetch(topic))
        state.mark_topic(topic)
        self.assertFalse(state.topic_needs_fetch(topic))

        changed_topic = dict(topic)
        changed_topic["posts_count"] = 3
        self.assertTrue(state.topic_needs_fetch(changed_topic))

    def test_state_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "state.json"
            state = ExportState()
            state.mark_topic({"id": 1, "bumped_at": "a", "posts_count": 1})
            state.save(path)

            loaded = ExportState.load(path)

            self.assertFalse(loaded.topic_needs_fetch({"id": 1, "bumped_at": "a", "posts_count": 1}))
            self.assertTrue(loaded.topic_needs_fetch({"id": 1, "bumped_at": "b", "posts_count": 1}))


if __name__ == "__main__":
    unittest.main()
