"""
api/schemas/settings.py
Pydantic models for the admin runtime-settings endpoints.

The response deliberately carries more than the order: an admin ranking a provider they
have no key for would otherwise see the save succeed and nothing change, because an
unreachable provider is skipped when the queue is built. `configured` and `config_hint`
are what let the UI say so at the moment of the decision.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class LLMProviderInfo(BaseModel):
    id: str
    label: str
    models: list[str] = []
    # False means "will be skipped": no API key, or for `local`, no base URL.
    configured: bool = False
    key_count: int = 0
    # The env var or URL to go and set. Never a key, or any part of one.
    config_hint: str = ""


class LLMProviderOrder(BaseModel):
    """The hierarchy in force, most preferred first, plus where it came from."""

    order: list[str]
    providers: list[LLMProviderInfo] = []
    # `environment` means no admin has saved an order and LLM_PROVIDER is still in charge.
    source: Literal["admin", "environment"] = "environment"
    env_default: str = "gemini"
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class UpdateProviderOrderRequest(BaseModel):
    order: list[str] = Field(
        ...,
        min_length=1,
        description="Provider ids ('gemini', 'groq', 'local') in the order they should be tried.",
    )
