"""Mock LLM provider implementation for testing orchestration components.

This module provides a controllable mock implementation of the LLMInterface
protocol, enabling deterministic testing of SPARC phase execution without
requiring real LLM service connections. The mock provider supports configurable
response sequences, error simulation, and comprehensive call tracking.

The implementation follows the Liskov Substitution Principle (LSP) by maintaining
the exact same behavioral contract as production LLM providers while providing
additional introspection capabilities for testing validation.

Design Rationale:
    - Configurable response sequences enable testing various LLM output scenarios
    - Call tracking allows verification of prompt patterns and parameter usage
    - Error simulation supports testing error handling and retry logic
    - Thread-safe implementation supports concurrent test execution
    - Immutable configuration after construction prevents test interference

Examples:
    Basic usage with response cycling::

        mock = MockLLMProvider(responses=["spec done", "arch complete"])
        result1 = await mock.generate("create spec")      # "spec done"
        result2 = await mock.generate("design arch")      # "arch complete"
        result3 = await mock.generate("another spec")     # "spec done" (cycles)

    Call introspection::

        mock = MockLLMProvider(responses=["response"])
        await mock.generate("test prompt", temperature=0.5, max_tokens=100)

        assert mock.call_count == 1
        assert mock.prompts == ["test prompt"]
        assert mock.last_kwargs["temperature"] == 0.5

    Error simulation::

        mock = MockLLMProvider(responses=[], should_raise=True)
        with pytest.raises(RuntimeError):
            await mock.generate("prompt")

Thread Safety:
    The MockLLMProvider is thread-safe for concurrent test execution. Internal
    state is protected by async-safe operations, and response cycling uses
    atomic modulo arithmetic to prevent race conditions.
"""

from collections.abc import AsyncGenerator
from typing import Any

from zenyth.core.types import LLMResponse


class MockLLMProvider:
    """Mock implementation of LLMInterface for deterministic testing.

    Provides a controllable LLM provider that cycles through pre-configured
    responses, tracks all method calls, and supports error simulation. This
    enables comprehensive testing of orchestration logic without external
    service dependencies.

    The mock maintains the exact same interface contract as production LLM
    providers while adding introspection capabilities essential for test
    validation and debugging.

    Attributes:
        responses: List of responses to cycle through for generate() calls.
                  Cannot be empty unless should_raise is True.
        call_count: Number of times generate() has been called. Read-only.
        prompts: List of all prompts passed to generate() calls. Read-only.
        last_kwargs: Keyword arguments from the most recent generate() call.
                    Empty dict if no calls made yet. Read-only.

    Args:
        responses: Sequence of string responses to return from generate() calls.
                  The mock will cycle through this list indefinitely. Must not
                  be empty unless should_raise is True.
        should_raise: If True, all generate() calls will raise RuntimeError
                     instead of returning responses. Useful for testing error
                     handling paths. Defaults to False.

    Raises:
        ValueError: If responses list is empty and should_raise is False.
        RuntimeError: During generate() calls if should_raise is True.

    Examples:
        Simple response cycling::

            mock = MockLLMProvider(responses=["Hello", "World"])
            result1 = await mock.generate("prompt1")  # "Hello"
            result2 = await mock.generate("prompt2")  # "World"
            result3 = await mock.generate("prompt3")  # "Hello" (cycles back)

        Call tracking verification::

            mock = MockLLMProvider(responses=["test"])
            await mock.generate("What is Python?", temperature=0.7)

            assert mock.call_count == 1
            assert mock.prompts[0] == "What is Python?"
            assert mock.last_kwargs["temperature"] == 0.7

        Error testing::

            mock = MockLLMProvider(responses=[], should_raise=True)
            with pytest.raises(RuntimeError, match="Mock LLM configured to raise"):
                await mock.generate("any prompt")

        Complex test scenario::

            # Simulate a conversation with varying responses
            mock = MockLLMProvider(responses=[
                "I'll help you create a specification.",
                "Here's the architecture design:",
                "Implementation completed successfully."
            ])

            # Test a full SPARC workflow
            spec_result = await mock.generate("Create user auth spec")
            arch_result = await mock.generate("Design the architecture")
            impl_result = await mock.generate("Implement the solution")

            assert "specification" in spec_result
            assert "architecture" in arch_result
            assert "completed" in impl_result
            assert mock.call_count == 3

    Note:
        The MockLLMProvider is designed for unit testing only. It should never
        be used in production code. Always use dependency injection to provide
        real LLM implementations in production environments.

        Response cycling uses modulo arithmetic, so calling generate() more times
        than there are responses will loop back to the beginning of the list.
        This enables testing long-running workflows with finite response sets.
    """

    def __init__(self, responses: list[str], should_raise: bool = False):
        """Initialize mock LLM provider with configurable responses.

        Args:
            responses: List of string responses to cycle through. Must not be
                      empty unless should_raise is True.
            should_raise: If True, generate() calls raise RuntimeError instead
                         of returning responses.

        Raises:
            ValueError: If responses is empty and should_raise is False.
        """
        if not responses and not should_raise:
            msg = "responses list cannot be empty unless should_raise is True"
            raise ValueError(msg)

        self._responses = responses.copy()  # Defensive copy
        self._should_raise = should_raise
        self._call_count = 0
        self._prompts: list[str] = []
        self._last_kwargs: dict[str, Any] = {}

    @property
    def responses(self) -> list[str]:
        """Get the configured response sequence."""
        return self._responses.copy()  # Return defensive copy

    @property
    def call_count(self) -> int:
        """Get the number of times generate() has been called."""
        return self._call_count

    @property
    def prompts(self) -> list[str]:
        """Get all prompts that have been passed to generate()."""
        return self._prompts.copy()  # Return defensive copy

    @property
    def last_kwargs(self) -> dict[str, Any]:
        """Get the keyword arguments from the most recent generate() call."""
        return self._last_kwargs.copy()  # Return defensive copy

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate a mock response from the configured response sequence.

        Cycles through the pre-configured responses list, returning each response
        in order and wrapping back to the beginning when all responses have been
        used. Tracks the call for introspection and testing verification.

        Args:
            prompt: The input prompt (tracked but not processed).
            **kwargs: Additional parameters (tracked but not processed).

        Returns:
            The next response from the configured sequence.

        Raises:
            RuntimeError: If should_raise was set to True during initialization.

        Note:
            This method maintains the same signature as the LLMInterface protocol
            but provides deterministic, testable behavior instead of actual LLM
            text generation.
        """
        if self._should_raise:
            msg = "Mock LLM configured to raise errors for testing"
            raise RuntimeError(msg)

        # Track call details for test verification
        self._call_count += 1
        self._prompts.append(prompt)
        self._last_kwargs = kwargs.copy()

        # Cycle through responses using modulo arithmetic
        response_index = (self._call_count - 1) % len(self._responses)
        return self._responses[response_index]
    
    async def complete_chat(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Generate a mock chat completion response."""
        response = await self.generate(prompt, **kwargs)
        return LLMResponse(content=response, metadata={"mock": True})
    
    async def create_session(self) -> str:
        """Create a mock session ID."""
        self._call_count += 1
        return f"mock-session-{self._call_count}"
    
    async def complete_chat_with_session(
        self, session_id: str, prompt: str, **kwargs: Any
    ) -> LLMResponse:
        """Generate a mock chat completion within a session."""
        response = await self.generate(prompt, **kwargs)
        return LLMResponse(
            content=response, 
            metadata={"session_id": session_id, "mock": True}
        )
    
    async def get_session_history(self, session_id: str) -> dict[str, Any]:
        """Get mock session history."""
        return {
            "session_id": session_id,
            "messages": [{"role": "user", "content": p} for p in self._prompts],
            "mock": True
        }
    
    async def fork_session(self, session_id: str, name: str | None = None) -> str:
        """Fork a mock session."""
        fork_name = name or "default"
        return f"{session_id}-fork-{fork_name}"
    
    async def revert_session(self, session_id: str, steps: int = 1) -> None:
        """Mock session reversion (no-op)."""
        # Mock implementation - just track the call
        _ = (session_id, steps)
    
    async def get_session_metadata(self, session_id: str) -> dict[str, Any]:
        """Get mock session metadata."""
        return {
            "session_id": session_id,
            "created_at": "2024-01-01T00:00:00Z",
            "message_count": len(self._prompts),
            "mock": True
        }
    
    def stream_chat(self, prompt: str, **kwargs: Any) -> AsyncGenerator[LLMResponse, None]:
        """Stream mock chat responses."""
        async def _generator() -> AsyncGenerator[LLMResponse, None]:
            # Track the call
            self._call_count += 1
            self._prompts.append(prompt)
            self._last_kwargs = kwargs.copy()
            
            # Generate response chunks
            if self._should_raise:
                raise RuntimeError("Mock LLM configured to raise errors for testing")
                
            response_index = (self._call_count - 1) % len(self._responses)
            response = self._responses[response_index]
            
            # Split response into chunks for streaming
            words = response.split()
            for i, word in enumerate(words):
                yield LLMResponse(
                    content=word + (" " if i < len(words) - 1 else ""),
                    metadata={"chunk_index": i, "mock": True}
                )
        
        return _generator()
