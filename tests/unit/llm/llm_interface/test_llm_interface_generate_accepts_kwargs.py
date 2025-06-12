"""Test LLM interface generate method accepts kwargs.

This test validates that the LLMInterface protocol's generate method
accepts keyword arguments, allowing for flexible parameter passing.
"""

import inspect

from zenyth.core.interfaces import LLMInterface


def test_llm_interface_generate_accepts_kwargs() -> None:
    """Test LLM interface generate method accepts kwargs."""
    sig = inspect.signature(LLMInterface.generate)
    param_kinds = [p.kind for p in sig.parameters.values()]
    assert inspect.Parameter.VAR_KEYWORD in param_kinds
