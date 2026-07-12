from __future__ import annotations

import inspect
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

import httpx


ALLOWED_FIELDS = {
    "thread_name",
    "content_text",
    "posted_at",
    "updated_at",
    "username",
    "like_count",
    "is_solution",
    "image_urls",
}


class MissingLLMConfigError(RuntimeError):
    pass


class LLMFallbackError(RuntimeError):
    pass


@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    model: str
    api_key: str
    timeout_seconds: int = 90

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "LLMConfig":
        env = env or os.environ
        missing = [name for name in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY") if not env.get(name)]
        if missing:
            raise MissingLLMConfigError(
                "Missing LLM environment variable(s): "
                + ", ".join(missing)
                + ". Set LLM_BASE_URL, LLM_MODEL, and LLM_API_KEY."
            )
        return cls(
            base_url=env["LLM_BASE_URL"].rstrip("/"),
            model=env["LLM_MODEL"],
            api_key=env["LLM_API_KEY"],
        )

    @classmethod
    def from_file_then_env(
        cls,
        config_path: Path | None,
        env: Mapping[str, str] | None = None,
    ) -> "LLMConfig":
        env = env or os.environ
        file_values = _read_llm_config_file(config_path)
        merged = {
            "LLM_BASE_URL": file_values.get("LLM_BASE_URL") or env.get("LLM_BASE_URL"),
            "LLM_MODEL": file_values.get("LLM_MODEL") or env.get("LLM_MODEL"),
            "LLM_API_KEY": file_values.get("LLM_API_KEY") or env.get("LLM_API_KEY"),
        }
        return cls.from_env(merged)

    @property
    def chat_completions_url(self) -> str:
        return f"{self.base_url}/chat/completions"


@dataclass
class NormalizedLLMResult:
    fields: dict[str, dict[str, Any]] = field(default_factory=dict)
    confidence: float | None = None
    warnings: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


class OpenAICompatibleLLMClient:
    def __init__(self, config: LLMConfig, session: Any | None = None):
        self.config = config
        self.session = session
        self._owns_session = session is None

    @classmethod
    def from_env(cls) -> "OpenAICompatibleLLMClient":
        return cls(LLMConfig.from_env())

    @classmethod
    def from_file_then_env(cls, config_path: Path | None = None) -> "OpenAICompatibleLLMClient":
        return cls(LLMConfig.from_file_then_env(config_path))

    async def aclose(self) -> None:
        if self._owns_session and self.session is not None:
            close = getattr(self.session, "aclose", None)
            if close is not None:
                result = close()
                if inspect.isawaitable(result):
                    await result
            self.session = None

    async def extract_post(self, post: dict[str, Any]) -> NormalizedLLMResult:
        payload = {
            "model": self.config.model,
            "messages": build_post_fallback_messages(post),
        }
        response = self._session().post(
            self.config.chat_completions_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response = await _maybe_await(response)
        response.raise_for_status()
        content = _extract_message_content(response.json())
        return normalize_llm_response(_parse_json_content(content))

    def _session(self) -> Any:
        if self.session is None:
            self.session = httpx.AsyncClient()
        return self.session


def build_post_fallback_messages(post: dict[str, Any]) -> list[dict[str, str]]:
    evidence = {
        "thread_name": post.get("thread_name"),
        "post_url": post.get("post_url"),
        "posted_by": post.get("posted_by"),
        "posted_at": post.get("posted_at"),
        "updated_at": post.get("updated_at"),
        "like_count": post.get("like_count"),
        "is_solution": post.get("is_solution"),
        "content_html": _truncate(post.get("content_html") or "", 16000),
        "content_text": _truncate(post.get("content_text") or "", 8000),
        "image_urls": post.get("image_urls") or [],
    }
    system = (
        "You extract metadata from authenticated Discourse post evidence. "
        "Do not make up data. "
        "Use only the supplied evidence. "
        "If a value is not present in the supplied evidence, return null for scalar fields and [] for lists. "
        "Every non-null field must include evidence copied from, or directly pointing to, the supplied evidence. "
        "If evidence is missing or ambiguous, leave the value null and add a warning. "
        "Return JSON only."
    )
    user = {
        "task": "Recover missing or verify existing post metadata without fabricating anything.",
        "allowed_fields": sorted(ALLOWED_FIELDS),
        "required_output_schema": {
            "confidence": "number between 0 and 1, or null",
            "fields": {
                "field_name": {
                    "value": "the extracted value, null, or []",
                    "evidence": "short evidence string from the supplied evidence; required for every non-null/non-empty value",
                }
            },
            "warnings": ["short warning strings"],
        },
        "evidence": evidence,
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
    ]


def normalize_llm_response(raw: dict[str, Any]) -> NormalizedLLMResult:
    result = NormalizedLLMResult(raw=raw)
    result.confidence = _normalize_confidence(raw.get("confidence"))
    result.warnings.extend(str(item) for item in raw.get("warnings") or [])

    fields = raw.get("fields") or {}
    if not isinstance(fields, dict):
        result.warnings.append("Ignored LLM fields because `fields` was not an object.")
        return result

    for field_name, field_payload in fields.items():
        if field_name not in ALLOWED_FIELDS:
            result.warnings.append(f"Rejected {field_name} because it is not an allowed field.")
            continue

        if isinstance(field_payload, dict):
            value = field_payload.get("value")
            evidence = field_payload.get("evidence")
        else:
            value = field_payload
            evidence = None

        if _has_value(value) and not _has_value(evidence):
            result.warnings.append(f"Rejected {field_name} because it had a value but no evidence.")
            continue

        result.fields[field_name] = {"value": value, "evidence": evidence}

    return result


def apply_llm_result_to_post(post: dict[str, Any], result: NormalizedLLMResult, source: str) -> None:
    post["llm_used"] = True
    post["llm_confidence"] = result.confidence
    post["llm_warnings"] = result.warnings
    post["llm_source"] = source
    post["llm_fields"] = result.fields

    _fill_if_missing(post, "thread_name", result)
    _fill_if_missing(post, "content_text", result)
    _fill_if_missing(post, "posted_at", result)
    _fill_if_missing(post, "updated_at", result)
    _fill_if_missing(post, "image_urls", result)

    if _missing(post.get("like_count")):
        _assign_field(post, "like_count", result)
    if _missing(post.get("is_solution")):
        _assign_field(post, "is_solution", result)

    posted_by = post.setdefault("posted_by", {})
    username_payload = result.fields.get("username")
    if _missing(posted_by.get("username")) and username_payload:
        posted_by["username"] = username_payload.get("value")


def mark_llm_not_used(post: dict[str, Any]) -> None:
    post.setdefault("llm_used", False)
    post.setdefault("llm_confidence", None)
    post.setdefault("llm_warnings", [])
    post.setdefault("llm_source", None)
    post.setdefault("llm_fields", {})


def post_needs_llm_fallback(post: dict[str, Any]) -> bool:
    posted_by = post.get("posted_by") or {}
    return any(
        [
            _missing(post.get("thread_name")),
            _missing(post.get("content_text")),
            _missing(post.get("posted_at")),
            _missing(posted_by.get("username")),
        ]
    )


async def _maybe_await(value):
    if inspect.isawaitable(value):
        return await value
    return value


def _fill_if_missing(post: dict[str, Any], field_name: str, result: NormalizedLLMResult) -> None:
    if _missing(post.get(field_name)):
        _assign_field(post, field_name, result)


def _assign_field(target: dict[str, Any], field_name: str, result: NormalizedLLMResult) -> None:
    field_payload = result.fields.get(field_name)
    if field_payload:
        target[field_name] = field_payload.get("value")


def _missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def _has_value(value: Any) -> bool:
    return not _missing(value)


def _normalize_confidence(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, min(1.0, number))


def _extract_message_content(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMFallbackError("LLM response did not include choices[0].message.content.") from exc


def _parse_json_content(content: str) -> dict[str, Any]:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if not match:
            raise LLMFallbackError("LLM response was not valid JSON.")
        payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise LLMFallbackError("LLM response JSON must be an object.")
    return payload


def _truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + "\n[truncated]"


def _read_llm_config_file(config_path: Path | None) -> dict[str, str]:
    if config_path is None or not config_path.exists():
        return {}
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise MissingLLMConfigError(f"LLM config file must be a JSON object: {config_path}")

    aliases = {
        "LLM_BASE_URL": ("LLM_BASE_URL", "base_url", "baseUrl", "llm_base_url"),
        "LLM_MODEL": ("LLM_MODEL", "model", "llm_model"),
        "LLM_API_KEY": ("LLM_API_KEY", "api_key", "apiKey", "llm_api_key"),
    }
    values: dict[str, str] = {}
    for canonical, keys in aliases.items():
        for key in keys:
            value = payload.get(key)
            if value:
                values[canonical] = str(value)
                break
    return values
