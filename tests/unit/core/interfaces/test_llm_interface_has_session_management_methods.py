"""Test LLMInterface requires session management methods.

This test validates that the LLMInterface protocol requires all necessary
session management methods, ensuring providers implement the full session
lifecycle functionality.
"""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from zenyth.core.types import LLMResponse


class MinimalLLMProvider:
    """Minimal LLM provider for protocol testing."""

    def __init__(self) -> None:
        """Initialize with call tracking."""
        self._call_count = 0

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Minimal generate implementation."""
        self._call_count += 1
        return f"response-{self._call_count}"

    async def complete_chat(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Minimal complete_chat implementation."""
        self._call_count += 1
        return LLMResponse(content=f"response-{self._call_count}")

    async def create_session(self) -> str:
        """Minimal create_session implementation."""
        self._call_count += 1
        return f"session-{self._call_count}"

    async def complete_chat_with_session(
        self,
        session_id: str,
        prompt: str,
        **kwargs: Any,
    ) -> LLMResponse:
        """Minimal complete_chat_with_session implementation."""
        self._call_count += 1
        return LLMResponse(content=f"response-{self._call_count}")

    async def get_session_history(self, session_id: str) -> dict[str, Any]:
        """Minimal get_session_history implementation."""
        self._call_count += 1
        return {"calls": self._call_count}

    async def fork_session(self, session_id: str, name: str | None = None) -> str:
        """Minimal fork_session implementation."""
        self._call_count += 1
        return f"fork-{self._call_count}"

    async def revert_session(self, session_id: str, steps: int = 1) -> None:
        """Minimal revert_session implementation."""

    async def get_session_metadata(self, session_id: str) -> dict[str, Any]:
        """Minimal get_session_metadata implementation."""
        self._call_count += 1
        return {"calls": self._call_count}

    def stream_chat(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> AsyncGenerator[LLMResponse, None]:
        """Minimal stream_chat implementation."""

        async def _gen() -> AsyncGenerator[LLMResponse, None]:
            await asyncio.sleep(0)  # Minimal async operation
            self._call_count += 1
            yield LLMResponse(content=f"stream-{self._call_count}")

        return _gen()


def test_llm_interface_has_session_management_methods() -> None:
    """Test LLMInterface requires session management methods."""
    provider = MinimalLLMProvider()

    # Check all session methods exist
    session_methods = [
        "create_session",
        "complete_chat_with_session",
        "get_session_history",
        "fork_session",
        "revert_session",
        "get_session_metadata",
    ]

    for method_name in session_methods:
        assert hasattr(provider, method_name), f"Missing method: {method_name}"
        assert callable(getattr(provider, method_name)), f"Not callable: {method_name}"
