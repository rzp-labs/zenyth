"""Minimal LLM interface."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMInterface(Protocol):
    """Minimal LLM contract."""

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        ...
