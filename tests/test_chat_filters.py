"""Focused tests for the chatbot's Qdrant metadata-filter contract."""

from __future__ import annotations

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

try:
    from qdrant_client import models

    from src import chatbot_app
    from src.chatbot_app import ChatRequest, build_qdrant_filter, get_filter_options, retrieve
    from src.ingest_to_qdrant import ensure_filter_indexes
except ImportError:
    CHAT_DEPS_AVAILABLE = False
else:
    CHAT_DEPS_AVAILABLE = True


@unittest.skipUnless(CHAT_DEPS_AVAILABLE, "Chatbot dependencies are not installed.")
class ChatFilterTests(unittest.TestCase):
    def test_builds_combined_filter_with_unassigned_week(self) -> None:
        request = ChatRequest(
            question="How does a decision tree work?",
            weeks=[5, 4, 4],
            include_unassigned_week=True,
            source_types=["discourse_forum", "course_material"],
            confidence_flags=["verified"],
            solved_only=True,
        )

        query_filter = build_qdrant_filter(request)

        self.assertIsNotNone(query_filter)
        dumped = query_filter.model_dump(mode="json")
        self.assertEqual(dumped["must"][0]["should"][0]["key"], "metadata.week")
        self.assertEqual(dumped["must"][0]["should"][0]["match"]["any"], [4, 5])
        self.assertEqual(dumped["must"][0]["should"][1]["is_null"]["key"], "metadata.week")
        self.assertEqual(dumped["must"][1]["key"], "metadata.source_type")
        self.assertEqual(dumped["must"][2]["key"], "metadata.confidence_flag")
        self.assertEqual(dumped["must"][3]["key"], "metadata.is_solved")

    def test_rejects_invalid_week(self) -> None:
        request = ChatRequest(question="What is regression?", weeks=[13])
        with self.assertRaisesRegex(ValueError, "between 1 and 12"):
            build_qdrant_filter(request)

    def test_empty_filter_is_not_sent_to_qdrant(self) -> None:
        request = ChatRequest(question="What is overfitting?")
        self.assertIsNone(build_qdrant_filter(request))

    def test_retrieve_forwards_qdrant_filter(self) -> None:
        class FakeStore:
            def __init__(self) -> None:
                self.call: dict[str, object] | None = None

            def similarity_search(self, question: str, **kwargs: object) -> list[object]:
                self.call = {"question": question, **kwargs}
                return []

        fake_store = FakeStore()
        request = ChatRequest(question="Explain gradient descent", solved_only=True)
        with patch("src.chatbot_app.get_store", return_value=fake_store):
            result = asyncio.run(retrieve(request.question, request))

        self.assertEqual(result, [])
        self.assertEqual(fake_store.call["k"], 5)
        self.assertIsInstance(fake_store.call["filter"], models.Filter)

    def test_creates_indexes_for_filterable_payloads(self) -> None:
        class FakeClient:
            def __init__(self) -> None:
                self.calls: list[dict[str, object]] = []

            def create_payload_index(self, **kwargs: object) -> None:
                self.calls.append(kwargs)

        client = FakeClient()
        ensure_filter_indexes(client, "test_collection")

        self.assertEqual({call["field_name"] for call in client.calls}, {
            "metadata.week",
            "metadata.source_type",
            "metadata.confidence_flag",
            "metadata.is_solved",
        })
        self.assertTrue(all(call["wait"] for call in client.calls))

    def test_filter_options_are_derived_from_qdrant_payloads(self) -> None:
        class FakeClient:
            def scroll(self, **kwargs: object) -> tuple[list[SimpleNamespace], None]:
                return [
                    SimpleNamespace(
                        payload={
                            "metadata": {
                                "week": 3,
                                "source_type": "discourse_forum",
                                "confidence_flag": "verified",
                            }
                        }
                    ),
                    SimpleNamespace(
                        payload={
                            "metadata": {
                                "week": None,
                                "source_type": "course_material",
                                "confidence_flag": "review_needed",
                            }
                        }
                    ),
                ], None

        with patch.object(chatbot_app, "_filter_options", None), patch.object(
            chatbot_app, "get_client", return_value=FakeClient()
        ):
            options = get_filter_options()

        self.assertEqual(options["weeks"], [3])
        self.assertEqual(options["unassigned_week_count"], 1)
        self.assertEqual(options["source_types"], ["course_material", "discourse_forum"])
        self.assertEqual(options["confidence_flags"], ["review_needed", "verified"])
