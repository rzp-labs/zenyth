"""Test for LLM interface contract."""

import inspect

import pytest

from zenyth.core.interfaces import LLMInterface


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
        async def generate(self, prompt: str, **kwargs) -> str:
            return "test"

    assert isinstance(TestLLM(), LLMInterface)


@pytest.mark.asyncio()
async def test_concrete_implementation_returns_string():
    """Test concrete implementation returns string."""

    class TestLLM:
        async def generate(self, prompt: str, **kwargs) -> str:
            return "test response"

    llm = TestLLM()
    result = await llm.generate("test")
    assert isinstance(result, str)


@pytest.mark.asyncio()
async def test_concrete_implementation_accepts_prompt():
    """Test concrete implementation accepts prompt parameter."""

    class TestLLM:
        async def generate(self, prompt: str, **kwargs) -> str:
            return f"Response to: {prompt}"

    llm = TestLLM()
    result = await llm.generate("test prompt")
    assert "test prompt" in result


@pytest.mark.asyncio()
async def test_concrete_implementation_accepts_kwargs():
    """Test concrete implementation accepts kwargs parameter."""

    class TestLLM:
        async def generate(self, prompt: str, **kwargs) -> str:
            return f"kwargs: {kwargs}"

    llm = TestLLM()
    result = await llm.generate("test", temperature=0.5)
    assert "temperature" in result


@pytest.mark.asyncio()
async def test_concrete_implementation_handles_success():
    """Test concrete implementation handles success case."""

    class TestLLM:
        async def generate(self, prompt: str, **kwargs) -> str:
            return "Success"

    llm = TestLLM()
    result = await llm.generate("good prompt")
    assert result == "Success"


@pytest.mark.asyncio()
async def test_concrete_implementation_allows_error_handling():
    """Test concrete implementation allows error handling."""

    class FailingLLM:
        async def generate(self, prompt: str, **kwargs) -> str:
            raise ValueError("Test error")

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
