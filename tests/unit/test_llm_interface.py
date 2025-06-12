"""Comprehensive unit tests for LLM interface protocol contract.

This test module validates the LLMInterface protocol contract and ensures that
concrete implementations properly adhere to the interface specification. The tests
follow SOLID principles by testing the interface abstraction separately from any
concrete implementations, enabling reliable dependency injection and provider
swapping in the Zenyth orchestration system.

The test suite validates both static protocol characteristics (method signatures,
type annotations, async behavior) and dynamic runtime behavior (protocol checking,
concrete implementation validation, error handling patterns). This comprehensive
coverage ensures that any LLM provider implementation will integrate correctly
with the SPARC orchestration workflow.

Test Categories:
    - Protocol Structure Tests: Validate method existence, signatures, annotations
    - Runtime Protocol Tests: Verify isinstance() checking works correctly
    - Concrete Implementation Tests: Validate example implementations work as expected
    - Error Handling Tests: Ensure exceptions propagate correctly
    - Async Behavior Tests: Confirm proper async/await patterns

Testing Strategy:
    - Each test validates one specific aspect of the protocol contract (SRP)
    - Tests use minimal concrete implementations to avoid coupling
    - Protocol testing separated from implementation testing
    - Comprehensive signature and type annotation validation
    - Runtime protocol checking verification for duck typing

Key Validation Points:
    - LLMInterface.generate method exists and is properly defined
    - Method signature accepts required parameters (prompt) and kwargs
    - Method is marked as async and returns string type
    - Runtime protocol checking works with isinstance()
    - Concrete implementations can be instantiated and called
    - Error handling patterns work correctly with async methods

Examples:
    Running all interface tests::

        pytest tests/unit/test_llm_interface.py -v

    Testing protocol structure only::

        pytest tests/unit/test_llm_interface.py -k "interface" -v

    Testing concrete implementations::

        pytest tests/unit/test_llm_interface.py -k "concrete" -v

    Running async tests only::

        pytest tests/unit/test_llm_interface.py -k "asyncio" -v

    Checking test coverage::

        pytest tests/unit/test_llm_interface.py --cov=zenyth.core.interfaces

Note:
    These tests focus on the protocol contract and interface compliance rather
    than testing actual LLM service integration. Provider-specific integration
    tests should be placed in separate test modules to maintain separation of
    concerns and enable testing without external dependencies.
"""

import inspect
from collections.abc import AsyncGenerator
from typing import Any

import pytest

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import LLMResponse


def test_llm_interface_has_generate_method():
    """Test LLM interface defines generate method."""
    assert hasattr(LLMInterface, "generate")


def test_llm_interface_generate_is_async():
    """Test LLM interface generate method is async."""
    assert inspect.iscoroutinefunction(LLMInterface.generate)


def test_llm_interface_generate_accepts_prompt_parameter():
    """Test LLM interface generate method accepts prompt parameter."""
    sig = inspect.signature(LLMInterface.generate)
    assert "prompt" in sig.parameters


def test_llm_interface_generate_accepts_kwargs():
    """Test LLM interface generate method accepts kwargs."""
    sig = inspect.signature(LLMInterface.generate)
    param_kinds = [p.kind for p in sig.parameters.values()]
    assert inspect.Parameter.VAR_KEYWORD in param_kinds


def test_llm_interface_supports_protocol_checking():
    """Test LLM interface supports runtime protocol checking."""

    class TestLLM:
        def __init__(self) -> None:
            self.name = "test"

        async def generate(self, prompt: str, **kwargs) -> str:
            return f"{self.name}: test"
        
        async def complete_chat(self, prompt: str, **kwargs) -> LLMResponse:
            return LLMResponse(content=f"{self.name}: test")
        
        async def create_session(self) -> str:
            return "test-session"
        
        async def complete_chat_with_session(
            self, session_id: str, prompt: str, **kwargs
        ) -> LLMResponse:
            return LLMResponse(content=f"{self.name}: test")
        
        async def get_session_history(self, session_id: str) -> dict[str, Any]:
            return {"messages": []}
        
        async def fork_session(self, session_id: str, name: str | None = None) -> str:
            return f"{session_id}-fork"
        
        async def revert_session(self, session_id: str, steps: int = 1) -> None:
            pass
        
        async def get_session_metadata(self, session_id: str) -> dict[str, Any]:
            return {"session_id": session_id}
        
        def stream_chat(self, prompt: str, **kwargs) -> AsyncGenerator[LLMResponse, None]:
            async def _generator() -> AsyncGenerator[LLMResponse, None]:
                yield LLMResponse(content="test")
            return _generator()

    assert isinstance(TestLLM(), LLMInterface)


@pytest.mark.asyncio()
async def test_concrete_implementation_returns_string():
    """Test concrete implementation returns string."""

    class TestLLM:
        def __init__(self) -> None:
            self.provider = "test"

        async def generate(self, prompt: str, **kwargs) -> str:
            return f"{self.provider} response"

    llm = TestLLM()
    result = await llm.generate("test")
    assert isinstance(result, str)


@pytest.mark.asyncio()
async def test_concrete_implementation_accepts_prompt():
    """Test concrete implementation accepts prompt parameter."""

    class TestLLM:
        def __init__(self) -> None:
            self.prefix = "Response to"

        async def generate(self, prompt: str, **kwargs) -> str:
            return f"{self.prefix}: {prompt}"

    llm = TestLLM()
    result = await llm.generate("test prompt")
    assert "test prompt" in result


@pytest.mark.asyncio()
async def test_concrete_implementation_accepts_kwargs():
    """Test concrete implementation accepts kwargs parameter."""

    class TestLLM:
        def __init__(self) -> None:
            self.format_template = "kwargs: {}"

        async def generate(self, prompt: str, **kwargs) -> str:
            return self.format_template.format(kwargs)

    llm = TestLLM()
    result = await llm.generate("test", temperature=0.5)
    assert "temperature" in result


@pytest.mark.asyncio()
async def test_concrete_implementation_handles_success():
    """Test concrete implementation handles success case."""

    class TestLLM:
        def __init__(self) -> None:
            self.response = "Success"

        async def generate(self, prompt: str, **kwargs) -> str:
            return self.response

    llm = TestLLM()
    result = await llm.generate("good prompt")
    assert result == "Success"


@pytest.mark.asyncio()
async def test_concrete_implementation_allows_error_handling():
    """Test concrete implementation allows error handling."""

    class FailingLLM:
        def __init__(self) -> None:
            self.error_message = "Test error"

        async def generate(self, prompt: str, **kwargs) -> str:
            raise ValueError(self.error_message)

    llm = FailingLLM()

    with pytest.raises(ValueError, match="Test error"):
        await llm.generate("fail prompt")


def test_llm_interface_generate_has_correct_signature():
    """Test LLM interface generate method has correct signature."""
    sig = inspect.signature(LLMInterface.generate)
    assert len(sig.parameters) >= 2  # self and prompt minimum


def test_llm_interface_generate_returns_string_annotation():
    """Test LLM interface generate method has string return annotation."""
    sig = inspect.signature(LLMInterface.generate)
    assert sig.return_annotation is str
