import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from discourse_exporter.llm import (
    LLMConfig,
    MissingLLMConfigError,
    OpenAICompatibleLLMClient,
    apply_llm_result_to_post,
    build_post_fallback_messages,
    normalize_llm_response,
)


class FakeLLMResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "confidence": 0.9,
                                "fields": {},
                                "warnings": [],
                            }
                        )
                    }
                }
            ]
        }


class FakeLLMSession:
    def __init__(self):
        self.last_json = None

    def post(self, url, headers, json, timeout):
        self.last_json = json
        return FakeLLMResponse()


class LLMTests(unittest.TestCase):
    def test_config_reads_required_env_names(self):
        env = {
            "LLM_BASE_URL": "http://localhost:8317/v1",
            "LLM_MODEL": "xxx",
            "LLM_API_KEY": "secret",
        }

        config = LLMConfig.from_env(env)

        self.assertEqual(config.base_url, "http://localhost:8317/v1")
        self.assertEqual(config.model, "xxx")
        self.assertEqual(config.api_key, "secret")
        self.assertEqual(config.chat_completions_url, "http://localhost:8317/v1/chat/completions")

    def test_config_requires_all_env_names(self):
        with self.assertRaises(MissingLLMConfigError) as caught:
            LLMConfig.from_env({"LLM_BASE_URL": "http://localhost:8317/v1"})

        self.assertIn("LLM_MODEL", str(caught.exception))
        self.assertIn("LLM_API_KEY", str(caught.exception))

    def test_config_reads_file_first_and_falls_back_to_env(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "llm_config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "LLM_BASE_URL": "http://localhost:8317/v1",
                        "LLM_MODEL": "file-model",
                    }
                ),
                encoding="utf-8",
            )

            config = LLMConfig.from_file_then_env(
                config_path,
                {
                    "LLM_BASE_URL": "http://env.example/v1",
                    "LLM_MODEL": "env-model",
                    "LLM_API_KEY": "env-key",
                },
            )

        self.assertEqual(config.base_url, "http://localhost:8317/v1")
        self.assertEqual(config.model, "file-model")
        self.assertEqual(config.api_key, "env-key")

    def test_config_supports_lowercase_file_keys(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "llm_config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "base_url": "http://localhost:8317/v1",
                        "model": "file-model",
                        "api_key": "file-key",
                    }
                ),
                encoding="utf-8",
            )

            config = LLMConfig.from_file_then_env(config_path, {})

        self.assertEqual(config.base_url, "http://localhost:8317/v1")
        self.assertEqual(config.model, "file-model")
        self.assertEqual(config.api_key, "file-key")

    def test_config_uses_env_when_file_is_missing(self):
        config = LLMConfig.from_file_then_env(
            Path("missing-llm-config.json"),
            {
                "LLM_BASE_URL": "http://localhost:8317/v1",
                "LLM_MODEL": "env-model",
                "LLM_API_KEY": "env-key",
            },
        )

        self.assertEqual(config.model, "env-model")

    def test_prompt_explicitly_forbids_making_up_data(self):
        post = {
            "thread_name": "Thread title",
            "content_html": "<p>Known content</p>",
            "content_text": "Known content",
            "posted_by": {"username": "alice"},
        }

        messages = build_post_fallback_messages(post)
        combined = "\n".join(message["content"] for message in messages)

        self.assertIn("Do not make up data", combined)
        self.assertIn("If a value is not present in the supplied evidence, return null", combined)
        self.assertIn("Every non-null field must include evidence", combined)

    def test_llm_request_omits_temperature_for_models_that_reject_it(self):
        session = FakeLLMSession()
        client = OpenAICompatibleLLMClient(
            LLMConfig(
                base_url="http://localhost:8317/v1",
                model="model-that-rejects-temperature",
                api_key="secret",
            ),
            session=session,
        )

        client.extract_post({"content_text": "known"})

        self.assertNotIn("temperature", session.last_json)
        self.assertEqual(session.last_json["model"], "model-that-rejects-temperature")

    def test_normalize_rejects_non_null_fields_without_evidence(self):
        raw = {
            "confidence": 0.7,
            "fields": {
                "content_text": {"value": "Recovered text", "evidence": "Recovered text"},
                "posted_at": {"value": "2026-01-01T00:00:00Z", "evidence": ""},
                "username": {"value": "invented_user"},
            },
            "warnings": ["partial extraction"],
        }

        normalized = normalize_llm_response(raw)

        self.assertEqual(normalized.fields["content_text"]["value"], "Recovered text")
        self.assertNotIn("posted_at", normalized.fields)
        self.assertNotIn("username", normalized.fields)
        self.assertIn("Rejected posted_at because it had a value but no evidence.", normalized.warnings)
        self.assertIn("Rejected username because it had a value but no evidence.", normalized.warnings)

    def test_apply_llm_result_fills_only_missing_post_fields(self):
        post = {
            "thread_name": "Primary title",
            "content_text": "",
            "posted_at": None,
            "like_count": 4,
            "image_urls": [],
            "posted_by": {"username": None},
        }
        result = normalize_llm_response(
            {
                "confidence": 0.8,
                "fields": {
                    "thread_name": {"value": "LLM title", "evidence": "LLM title"},
                    "content_text": {"value": "Recovered body", "evidence": "Recovered body"},
                    "posted_at": {"value": "2026-01-01T00:00:00Z", "evidence": "Jan 1"},
                    "like_count": {"value": 99, "evidence": "99 likes"},
                    "username": {"value": "alice", "evidence": "alice"},
                    "image_urls": {"value": ["https://example.test/a.png"], "evidence": "a.png"},
                },
                "warnings": [],
            }
        )

        apply_llm_result_to_post(post, result, source="test-source")

        self.assertEqual(post["thread_name"], "Primary title")
        self.assertEqual(post["content_text"], "Recovered body")
        self.assertEqual(post["posted_at"], "2026-01-01T00:00:00Z")
        self.assertEqual(post["like_count"], 4)
        self.assertEqual(post["posted_by"]["username"], "alice")
        self.assertEqual(post["image_urls"], ["https://example.test/a.png"])
        self.assertTrue(post["llm_used"])
        self.assertEqual(post["llm_confidence"], 0.8)
        self.assertEqual(post["llm_source"], "test-source")


if __name__ == "__main__":
    unittest.main()
