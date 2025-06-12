"""Test that MockLLMProvider implements LLMInterface protocol.

This test validates that the MockLLMProvider correctly implements the
LLMInterface protocol, ensuring it can be used as a drop-in replacement
for real LLM providers in tests.
"""

from zenyth.core.interfaces import LLMInterface
from zenyth.mocks import MockLLMProvider


def test_mock_llm_implements_interface() -> None:
    """Test that MockLLMProvider implements LLMInterface protocol."""
    provider = MockLLMProvider(responses=["test"])
    assert isinstance(provider, LLMInterface)
