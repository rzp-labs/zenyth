"""Test that MockLLMProvider accepts and ignores kwargs like real providers.

This test validates that the MockLLMProvider accepts keyword arguments
in its generate method, matching the interface of real LLM providers
that accept parameters like temperature, max_tokens, etc.
"""

import pytest

from zenyth.mocks import MockLLMProvider


@pytest.mark.asyncio()
async def test_mock_llm_accepts_kwargs() -> None:
    """Test that MockLLMProvider accepts and ignores kwargs like real providers."""
    provider = MockLLMProvider(responses=["response"])

    # Should not raise any errors with various kwargs
    result = await provider.generate("prompt", temperature=0.7, max_tokens=100, model="gpt-4")
    assert result == "response"
