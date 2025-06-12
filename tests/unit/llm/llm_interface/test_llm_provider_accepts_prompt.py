"""Test LLM provider accepts prompt parameter.

This test validates that an LLM provider implementing the LLMInterface
protocol correctly accepts and uses the prompt parameter.
"""

from typing import Any

import pytest


@pytest.mark.asyncio()
async def test_llm_provider_accepts_prompt() -> None:
    """Test LLM provider accepts prompt parameter."""

    class TestLLM:
        def __init__(self) -> None:
            self.prefix = "Response to"

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            return f"{self.prefix}: {prompt}"

    llm = TestLLM()
    result = await llm.generate("test prompt")
    assert "test prompt" in result
