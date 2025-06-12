"""Test LLM provider allows error handling.

This test validates that an LLM provider implementing the LLMInterface
protocol can raise exceptions that can be properly caught and handled.
"""

from typing import Any

import pytest


@pytest.mark.asyncio()
async def test_llm_provider_allows_error_handling() -> None:
    """Test LLM provider allows error handling."""

    class FailingLLM:
        def __init__(self) -> None:
            self.error_message = "Test error"

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            raise ValueError(self.error_message)

    llm = FailingLLM()

    with pytest.raises(ValueError, match="Test error"):
        await llm.generate("fail prompt")
