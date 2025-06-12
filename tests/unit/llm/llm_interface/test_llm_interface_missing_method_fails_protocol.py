"""Test that missing required methods fail protocol check.

This test validates that incomplete implementations that are missing required
methods will fail the runtime protocol check, ensuring proper interface
compliance.
"""

from typing import Any

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import LLMResponse


def test_llm_interface_missing_method_fails_protocol() -> None:
    """Test that missing required methods fail protocol check."""

    class IncompleteLLM:
        """LLM missing some required methods."""

        def __init__(self) -> None:
            self._id = "incomplete"

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            return f"{self._id}-test"

        async def complete_chat(self, prompt: str, **kwargs: Any) -> LLMResponse:
            return LLMResponse(content=f"{self._id}-test")

        # Intentionally missing other required methods

    # Should NOT pass protocol check
    assert not isinstance(IncompleteLLM(), LLMInterface)
