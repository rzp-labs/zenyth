"""Test that MockLLMProvider cycles through multiple responses.

This test validates that the MockLLMProvider can be configured with multiple
responses and will cycle through them, returning to the first response after
exhausting the list.
"""

import pytest

from zenyth.mocks import MockLLMProvider


@pytest.mark.asyncio()
async def test_mock_llm_cycles_through_responses() -> None:
    """Test that MockLLMProvider cycles through multiple responses."""
    responses = ["response 1", "response 2", "response 3"]
    provider = MockLLMProvider(responses=responses)

    # First cycle through all responses
    for expected in responses:
        result = await provider.generate("prompt")
        assert result == expected

    # Should cycle back to the first response
    result = await provider.generate("prompt")
    assert result == responses[0]
