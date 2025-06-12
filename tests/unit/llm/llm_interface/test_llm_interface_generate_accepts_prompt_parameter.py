"""Test LLM interface generate method accepts prompt parameter.

This test validates that the LLMInterface protocol's generate method
signature includes a 'prompt' parameter for providing input text.
"""

import inspect

from zenyth.core.interfaces import LLMInterface


def test_llm_interface_generate_accepts_prompt_parameter() -> None:
    """Test LLM interface generate method accepts prompt parameter."""
    sig = inspect.signature(LLMInterface.generate)
    assert "prompt" in sig.parameters
