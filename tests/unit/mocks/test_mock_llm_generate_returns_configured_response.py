"""Test that generate method returns the configured response.

This test validates that the MockLLMProvider's generate method returns
the configured response, allowing predictable behavior in tests.
"""

import pytest

from zenyth.mocks import MockLLMProvider


@pytest.mark.asyncio()
async def test_mock_llm_generate_returns_configured_response() -> None:
    """Test that generate method returns the configured response."""
    expected_response = "Mock generated response"
    provider = MockLLMProvider(responses=[expected_response])

    result = await provider.generate("test prompt")
    assert result == expected_response
