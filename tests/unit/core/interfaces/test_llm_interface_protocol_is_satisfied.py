"""Test that a minimal implementation satisfies LLMInterface protocol.

This test validates that the MinimalLLMProvider class correctly implements
the LLMInterface protocol, demonstrating that the protocol contract can be
satisfied by concrete implementations.
"""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import LLMResponse


class MinimalLLMProvider:
    """Minimal LLM provider for protocol testing.

    Methods don't use self because they're minimal stubs, but must be
    instance methods to satisfy the protocol contract.
    """

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


def test_llm_interface_protocol_is_satisfied() -> None:
    """Test that a minimal implementation satisfies LLMInterface protocol."""
    provider = MinimalLLMProvider()
    assert isinstance(provider, LLMInterface)
