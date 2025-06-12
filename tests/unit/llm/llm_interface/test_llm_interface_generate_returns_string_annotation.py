"""Test LLM interface generate method has string return annotation.

This test validates that the LLMInterface protocol's generate method is
properly annotated to return a string type.
"""

import inspect

from zenyth.core.interfaces import LLMInterface


def test_llm_interface_generate_returns_string_annotation() -> None:
    """Test LLM interface generate method has string return annotation."""
    sig = inspect.signature(LLMInterface.generate)
    assert sig.return_annotation is str
