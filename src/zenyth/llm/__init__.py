"""LLM provider implementations for Zenyth SPARC orchestration.

This module provides implementations of the LLMInterface protocol for various
language model providers, enabling SPARC phase execution with different backends.

Key Components:
    HTTPLLMProvider: HTTP-based provider using AI SDK wrapper service

Architecture:
    All providers implement the LLMInterface protocol defined in core.interfaces,
    enabling dependency injection and seamless provider switching.

Usage:
    from zenyth.llm import HTTPLLMProvider

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    response = await provider.complete_chat("What is 2+2?")
"""

from .http_provider import HTTPLLMProvider

__all__ = [
    "HTTPLLMProvider",
]
