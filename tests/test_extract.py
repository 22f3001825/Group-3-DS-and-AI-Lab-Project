import unittest

from discourse_exporter.extract import (
    extract_image_sources,
    extract_topic_records,
    is_solution_post,
    like_count_from_post,
)


BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"


class ExtractTests(unittest.TestCase):
    def test_extract_image_sources_handles_relative_absolute_and_srcset(self):
        html = """
        <p>See this</p>
        <img src="/uploads/default/original/1X/a.png">
        <img src="https://cdn.example.test/b.jpg">
        <img srcset="/uploads/small.jpg 1x, /uploads/large.jpg 2x">
        """

        urls = extract_image_sources(html, BASE_URL)

        self.assertEqual(
            urls,
            [
                "https://discourse.onlinedegree.iitm.ac.in/uploads/default/original/1X/a.png",
                "https://cdn.example.test/b.jpg",
                "https://discourse.onlinedegree.iitm.ac.in/uploads/small.jpg",
                "https://discourse.onlinedegree.iitm.ac.in/uploads/large.jpg",
            ],
        )

    def test_like_count_prefers_explicit_field_and_falls_back_to_actions_summary(self):
        self.assertEqual(like_count_from_post({"like_count": 4, "actions_summary": []}), 4)
        self.assertEqual(
            like_count_from_post({"actions_summary": [{"id": 2, "count": 7}, {"id": 3, "count": 1}]}),
            7,
        )
        self.assertEqual(like_count_from_post({}), 0)

    def test_solution_detection_checks_common_discourse_solved_fields(self):
        topic = {"accepted_answer_post_id": 20, "accepted_answer": 3}

        self.assertFalse(is_solution_post({"id": 10, "post_number": 1}, topic))
        self.assertTrue(is_solution_post({"id": 20, "post_number": 2}, topic))
        self.assertTrue(is_solution_post({"id": 30, "post_number": 3}, topic))
        self.assertTrue(is_solution_post({"id": 40, "accepted_answer": True}, topic))

    def test_extract_topic_records_preserves_thread_post_metadata(self):
        topic = {
            "id": 123,
            "title": "Week 1 Doubt",
            "slug": "week-1-doubt",
            "created_at": "2026-01-01T00:00:00.000Z",
            "last_posted_at": "2026-01-03T00:00:00.000Z",
            "accepted_answer_post_id": 20,
            "post_stream": {
                "posts": [
                    {
                        "id": 10,
                        "post_number": 1,
                        "user_id": 5,
                        "username": "alice",
                        "name": "Alice",
                        "created_at": "2026-01-01T01:00:00.000Z",
                        "updated_at": "2026-01-02T01:00:00.000Z",
                        "cooked": '<p>Hello <img src="/uploads/a.png"></p>',
                        "actions_summary": [{"id": 2, "count": 3}],
                    },
                    {
                        "id": 20,
                        "post_number": 2,
                        "user_id": 6,
                        "username": "bob",
                        "created_at": "2026-01-03T01:00:00.000Z",
                        "updated_at": None,
                        "cooked": "<p>Use Bayes rule.</p>",
                        "like_count": 5,
                    },
                ]
            },
        }

        topic_record, post_records = extract_topic_records(topic, BASE_URL)

        self.assertEqual(topic_record["thread_name"], "Week 1 Doubt")
        self.assertEqual(topic_record["url"], "https://discourse.onlinedegree.iitm.ac.in/t/week-1-doubt/123")
        self.assertEqual(len(post_records), 2)
        self.assertEqual(post_records[0]["thread_name"], "Week 1 Doubt")
        self.assertEqual(post_records[0]["posted_by"]["username"], "alice")
        self.assertEqual(post_records[0]["like_count"], 3)
        self.assertEqual(post_records[0]["image_urls"], [BASE_URL + "/uploads/a.png"])
        self.assertFalse(post_records[0]["is_solution"])
        self.assertTrue(post_records[1]["is_solution"])
        self.assertEqual(post_records[1]["content_text"], "Use Bayes rule.")


if __name__ == "__main__":
    unittest.main()
