"""Test LLM interface generate method has correct signature.

This test validates that the LLMInterface protocol's generate method has
the correct signature with the required number of parameters.
"""

import inspect

from zenyth.core.interfaces import LLMInterface


def test_llm_interface_generate_has_correct_signature() -> None:
    """Test LLM interface generate method has correct signature."""
    sig = inspect.signature(LLMInterface.generate)
    assert len(sig.parameters) >= 2  # self and prompt minimum
