"""Test LLM interface supports runtime protocol checking.

This test validates that the LLMInterface protocol supports runtime type
checking with isinstance(), allowing verification that implementations
properly satisfy the protocol.
"""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import LLMResponse


class TestLLMWithState:
    """Test LLM that uses instance state to verify protocol allows it."""

    def __init__(self) -> None:
        self.name = "test"
        self.call_count = 0

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        self.call_count += 1
        return f"{self.name}: response {self.call_count}"

    async def complete_chat(self, prompt: str, **kwargs: Any) -> LLMResponse:
        return LLMResponse(content=f"{self.name}: test")

    async def create_session(self) -> str:
        self.call_count += 1
        return f"{self.name}-session-{self.call_count}"

    async def complete_chat_with_session(
        self,
        session_id: str,
        prompt: str,
        **kwargs: Any,
    ) -> LLMResponse:
        return LLMResponse(content=f"{self.name}: test")

    async def get_session_history(self, session_id: str) -> dict[str, Any]:
        self.call_count += 1
        return {"messages": [], "provider": self.name, "calls": self.call_count}

    async def fork_session(self, session_id: str, name: str | None = None) -> str:
        self.call_count += 1
        fork_name = name or f"fork-{self.call_count}"
        return f"{session_id}-{fork_name}"

    async def revert_session(self, session_id: str, steps: int = 1) -> None:
        pass

    async def get_session_metadata(self, session_id: str) -> dict[str, Any]:
        self.call_count += 1
        return {
            "session_id": session_id,
            "provider": self.name,
            "access_count": self.call_count,
        }

    def stream_chat(self, prompt: str, **kwargs: Any) -> AsyncGenerator[LLMResponse, None]:
        async def _generator() -> AsyncGenerator[LLMResponse, None]:
            await asyncio.sleep(0)  # Minimal async operation
            self.call_count += 1
            yield LLMResponse(content=f"{self.name}: chunk {self.call_count}")

        return _generator()


def test_llm_interface_supports_protocol_checking() -> None:
    """Test LLM interface supports runtime protocol checking."""
    # Instance should implement protocol
    provider = TestLLMWithState()
    assert isinstance(provider, LLMInterface)
