"""Test LLM provider accepts kwargs parameter.

This test validates that an LLM provider implementing the LLMInterface
protocol correctly accepts and processes keyword arguments.
"""

from typing import Any

import pytest


@pytest.mark.asyncio()
async def test_llm_provider_accepts_kwargs() -> None:
    """Test LLM provider accepts kwargs parameter."""

    class TestLLM:
        def __init__(self) -> None:
            self.format_template = "kwargs: {}"

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            return self.format_template.format(kwargs)

    llm = TestLLM()
    result = await llm.generate("test", temperature=0.5)
    assert "temperature" in result
