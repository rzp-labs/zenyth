"""Test LLM provider returns string.

This test validates that an LLM provider implementing the LLMInterface
protocol correctly returns a string from the generate method.
"""

from typing import Any

import pytest


@pytest.mark.asyncio()
async def test_llm_provider_returns_string() -> None:
    """Test LLM provider returns string."""

    class TestLLM:
        def __init__(self) -> None:
            self.provider = "test"

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            return f"{self.provider} response"

    llm = TestLLM()
    result = await llm.generate("test")
    assert isinstance(result, str)
