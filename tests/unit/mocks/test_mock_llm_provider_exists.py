"""Test that MockLLMProvider class can be instantiated.

This test validates that the MockLLMProvider class exists and can be
instantiated with a list of responses, following the TDD red-green cycle.
"""

from zenyth.mocks import MockLLMProvider


def test_mock_llm_provider_exists() -> None:
    """Test that MockLLMProvider class can be instantiated."""
    # This test should FAIL initially - driving TDD red phase
    provider = MockLLMProvider(responses=["test response"])
    assert provider is not None
