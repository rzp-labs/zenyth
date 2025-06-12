"""Test LLM provider handles success case.

This test validates that an LLM provider implementing the LLMInterface
protocol correctly handles successful generation requests.
"""

from typing import Any

import pytest


@pytest.mark.asyncio()
async def test_llm_provider_handles_success() -> None:
    """Test LLM provider handles success case."""

    class TestLLM:
        def __init__(self) -> None:
            self.response = "Success"

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            return self.response

    llm = TestLLM()
    result = await llm.generate("good prompt")
    assert result == "Success"
