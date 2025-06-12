"""Test that MockLLMProvider tracks the number of generate calls.

This test validates that the MockLLMProvider maintains a call count,
which is useful for verifying the number of times the provider was
called during tests.
"""

import pytest

from zenyth.mocks import MockLLMProvider


@pytest.mark.asyncio()
async def test_mock_llm_tracks_call_count() -> None:
    """Test that MockLLMProvider tracks the number of generate calls."""
    provider = MockLLMProvider(responses=["response"])

    assert provider.call_count == 0

    await provider.generate("prompt 1")
    assert provider.call_count == 1

    await provider.generate("prompt 2")
    assert provider.call_count == 2
