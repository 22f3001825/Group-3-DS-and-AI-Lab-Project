import json
import unittest

from src.build_discourse_evaluation import build_queries
from src.clean_discourse_export import clean_export


class DiscourseCleanerTests(unittest.TestCase):
    def sample_export(self):
        return {
            "topics": [
                {
                    "topic_id": 10,
                    "thread_name": "Week 4 kernel PCA doubt",
                    "url": "https://forum.test/t/10",
                    "stream_post_count": 4,
                    "exported_post_count": 4,
                }
            ],
            "posts": [
                {
                    "topic_id": 10,
                    "post_id": 101,
                    "post_number": 1,
                    "thread_name": "Week 4 kernel PCA doubt",
                    "thread_url": "https://forum.test/t/10",
                    "post_url": "https://forum.test/t/10/1",
                    "posted_at": "2026-01-01T00:00:00Z",
                    "content_html": "<p>How should I interpret the kernel PCA projection for the Week 4 assignment?</p>",
                    "posted_by": {"username": "student"},
                    "like_count": 1,
                    "is_solution": False,
                },
                {
                    "topic_id": 10,
                    "post_id": 102,
                    "post_number": 2,
                    "thread_name": "Week 4 kernel PCA doubt",
                    "thread_url": "https://forum.test/t/10",
                    "post_url": "https://forum.test/t/10/2",
                    "posted_at": "2026-01-01T01:00:00Z",
                    "content_html": "<blockquote>quoted question</blockquote><p>Use the kernel matrix and center it first.</p><a href='https://forum.test/uploads/guide.pdf'>Guide</a>",
                    "posted_by": {"username": "staff_member", "primary_group_name": "course_support"},
                    "like_count": 4,
                    "is_solution": True,
                },
                {
                    "topic_id": 10,
                    "post_id": 103,
                    "post_number": 3,
                    "thread_name": "Week 4 kernel PCA doubt",
                    "thread_url": "https://forum.test/t/10",
                    "post_url": "https://forum.test/t/10/3",
                    "content_html": "<p>Use the kernel matrix and center it first.</p><a href='https://forum.test/uploads/guide.pdf'>Guide</a>",
                    "posted_by": {"username": "other"},
                    "like_count": 0,
                    "is_solution": False,
                },
                {
                    "topic_id": 10,
                    "post_id": 104,
                    "post_number": 4,
                    "thread_name": "Week 4 kernel PCA doubt",
                    "thread_url": "https://forum.test/t/10",
                    "post_url": "https://forum.test/t/10/4",
                    "content_html": "<p>Thanks!</p>",
                    "posted_by": {"username": "student"},
                    "like_count": 0,
                    "is_solution": False,
                },
            ],
            "users": [{"username": "student", "bio_raw": "private profile"}],
        }

    def test_cleaner_removes_quotes_pii_noise_and_duplicates(self):
        posts, quarantined, documents, extra = clean_export(self.sample_export())

        self.assertEqual(len(posts), 2)
        self.assertIn("exact_duplicate", {record["reason"] for record in quarantined})
        self.assertIn("low_value_or_acknowledgement", {record["reason"] for record in quarantined})
        self.assertNotIn("staff_member", json.dumps(posts))
        self.assertNotIn("quoted question", posts[1]["text"])
        self.assertEqual(posts[1]["author_role"], "staff")
        self.assertEqual(posts[1]["confidence_flag"], "verified")
        self.assertEqual(posts[1]["attachments"][0]["kind"], "attachment")
        self.assertEqual(extra["report"]["output"]["thread_documents"], 1)
        self.assertIn("Accepted solution", documents[0]["text"])

    def test_evaluation_queries_are_topic_isolated(self):
        chunks = [
            {
                "text": "Question and answer",
                "metadata": {
                    "source_type": "discourse_forum",
                    "doc_id": "discourse-topic-10-core",
                    "chunk_id": "discourse-topic-10-core_chunk_000",
                    "topic_id": "10",
                    "question_text": "How should I interpret kernel PCA?",
                    "confidence_flag": "verified",
                    "thread_url": "https://forum.test/t/10",
                },
            }
        ]

        queries, report = build_queries(chunks)

        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0]["gold_chunk_ids"], ["discourse-topic-10-core_chunk_000"])
        self.assertEqual(report["topic_leakage_check"], "passed")


if __name__ == "__main__":
    unittest.main()
