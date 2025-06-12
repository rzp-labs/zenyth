"""This module provides HTTPLLMProvider for AI SDK wrapper integration.

SOLID Principles Alignment:
- SRP: Single responsibility of HTTP communication with LLM service
- OCP: Implements LLMInterface protocol without modifying core abstractions
- LSP: Fully substitutable for any LLMInterface implementation
- ISP: Depends only on minimal LLMInterface protocol
- DIP: Depends on LLMInterface abstraction, not concrete implementations
"""

import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import LLMResponse


class MissingContentFieldError(ValueError):
    """Raised when API response is missing required 'content' field."""

    def __init__(self, received_fields: list[str]) -> None:
        """Initialize with the fields that were received."""
        super().__init__(
            f"Invalid API response: missing 'content' field. Received: {received_fields}",
        )


class MissingSessionIdFieldError(ValueError):
    """Raised when API response is missing required 'session_id' field."""

    def __init__(self, received_fields: list[str]) -> None:
        """Initialize with the fields that were received."""
        super().__init__(
            f"Invalid API response: missing 'session_id' field. Received: {received_fields}",
        )


class HTTPLLMProvider(LLMInterface):
    """Minimal stub for HTTP-based LLM provider."""

    def __init__(self, base_url: str) -> None:
        """Initialize the provider.

        Args:
            base_url: The base URL for the HTTP API service
        """
        self.base_url = base_url.rstrip("/")

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text response from the given prompt.

        Minimal implementation to satisfy LLMInterface protocol.
        """
        # Minimal HTTP implementation to pass tests
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/completions",
                json={"prompt": prompt, **kwargs},
            )
            response.raise_for_status()
            data = response.json()

            if "content" not in data:
                raise MissingContentFieldError(list(data.keys()))

            return str(data["content"])

    async def complete_chat(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Generate chat completion response from the given prompt."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={"prompt": prompt, **kwargs},
            )
            response.raise_for_status()
            data = response.json()

            if "content" not in data:
                raise MissingContentFieldError(list(data.keys()))

            return LLMResponse(
                content=data["content"],
                metadata={
                    "model": data.get("model", "unknown"),
                    "usage": data.get("usage", {}),
                },
            )

    async def create_session(self) -> str:
        """Create a new conversation session."""
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/v1/sessions", json={})
            response.raise_for_status()
            data = response.json()

            if "session_id" not in data:
                raise MissingSessionIdFieldError(list(data.keys()))

            return str(data["session_id"])

    async def complete_chat_with_session(
        self,
        session_id: str,
        prompt: str,
        **kwargs: Any,
    ) -> LLMResponse:
        """Generate chat completion within an existing session."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={"session_id": session_id, "prompt": prompt, **kwargs},
            )
            response.raise_for_status()
            data = response.json()

            if "content" not in data:
                raise MissingContentFieldError(list(data.keys()))

            return LLMResponse(
                content=data["content"],
                metadata={
                    "model": data.get("model", "unknown"),
                    "session_id": data.get("session_id", session_id),
                    "usage": data.get("usage", {}),
                },
            )

    async def get_session_history(self, session_id: str) -> dict[str, Any]:
        """Retrieve conversation history for a session."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/v1/sessions/{session_id}/history")
            response.raise_for_status()
            data = response.json()
            return dict(data)

    async def fork_session(self, session_id: str, name: str | None = None) -> str:
        """Create a branched session from an existing session."""
        async with httpx.AsyncClient() as client:
            payload = {}
            if name is not None:
                payload["name"] = name

            response = await client.post(
                f"{self.base_url}/v1/sessions/{session_id}/fork",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            if "session_id" not in data:
                raise MissingSessionIdFieldError(list(data.keys()))

            return str(data["session_id"])

    async def revert_session(self, session_id: str, steps: int = 1) -> None:
        """Remove messages from session history."""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                "DELETE",
                f"{self.base_url}/v1/sessions/{session_id}/messages",
                json={"steps": steps},
            )
            response.raise_for_status()

    async def get_session_metadata(self, session_id: str) -> dict[str, Any]:
        """Get metadata and statistics for a session."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/v1/sessions/{session_id}/metadata")
            response.raise_for_status()
            data = response.json()
            return dict(data)

    async def stream_chat(self, prompt: str, **kwargs: Any) -> AsyncGenerator[LLMResponse, None]:
        """Stream chat completion responses in real-time."""
        async with (
            httpx.AsyncClient() as client,
            client.stream(
                "POST",
                f"{self.base_url}/v1/chat/completions/stream",
                json={"prompt": prompt, "stream": True, **kwargs},
            ) as response,
        ):
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix
                    if data_str == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                        yield LLMResponse(
                            content=data["content"],
                            metadata=data.get("metadata", {}),
                        )
                    except json.JSONDecodeError:
                        # Skip malformed lines
                        continue
