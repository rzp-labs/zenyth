"""Test LLM interface defines generate method.

This test validates that the LLMInterface protocol includes the generate
method, which is the core method for text generation in the system.
"""

from zenyth.core.interfaces import LLMInterface


def test_llm_interface_has_generate_method() -> None:
    """Test LLM interface defines generate method."""
    assert hasattr(LLMInterface, "generate")
