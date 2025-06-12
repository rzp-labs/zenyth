"""Test LLM interface generate method is async.

This test validates that the LLMInterface protocol's generate method is
defined as an async method, ensuring proper asynchronous operation.
"""

import inspect

from zenyth.core.interfaces import LLMInterface


def test_llm_interface_generate_is_async() -> None:
    """Test LLM interface generate method is async."""
    assert inspect.iscoroutinefunction(LLMInterface.generate)
