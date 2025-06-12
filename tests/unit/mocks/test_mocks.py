"""Test suite for mock implementations used in testing Zenyth components.

This module validates the behavior of mock classes that simulate external
dependencies like LLM providers and MCP servers. These mocks are essential
for unit testing orchestration logic without requiring real external services.

Following TDD methodology, these tests drive the implementation of mock
classes that adhere to the same interfaces as production components while
providing predictable, controllable behavior for testing scenarios.

Test Strategy:
    - Verify mocks implement the same protocols as production classes
    - Test configurable response sequences and behaviors
    - Validate call tracking and introspection capabilities
    - Ensure mocks can simulate both success and failure scenarios
    - Test thread-safety for concurrent test execution

Examples:
    Running mock tests::

        pytest tests/unit/test_mocks.py -v

    Running with coverage::

        pytest tests/unit/test_mocks.py --cov=zenyth.mocks --cov-report=term-missing
"""

from zenyth.core.interfaces import LLMInterface
from zenyth.mocks import MockLLMProvider


def test_mock_llm_provider_exists() -> None:
    """Test that MockLLMProvider class can be instantiated."""
    # This test should FAIL initially - driving TDD red phase
    provider = MockLLMProvider(responses=["test response"])
    assert provider is not None


def test_mock_llm_implements_interface() -> None:
    """Test that MockLLMProvider implements LLMInterface protocol."""
    provider = MockLLMProvider(responses=["test"])
    assert isinstance(provider, LLMInterface)


async def test_mock_llm_generate_returns_configured_response() -> None:
    """Test that generate method returns the configured response."""
    expected_response = "Mock generated response"
    provider = MockLLMProvider(responses=[expected_response])

    result = await provider.generate("test prompt")
    assert result == expected_response


async def test_mock_llm_cycles_through_responses() -> None:
    """Test that MockLLMProvider cycles through multiple responses."""
    responses = ["response 1", "response 2", "response 3"]
    provider = MockLLMProvider(responses=responses)

    # First cycle through all responses
    for expected in responses:
        result = await provider.generate("prompt")
        assert result == expected

    # Should cycle back to the first response
    result = await provider.generate("prompt")
    assert result == responses[0]


async def test_mock_llm_tracks_call_count() -> None:
    """Test that MockLLMProvider tracks the number of generate calls."""
    provider = MockLLMProvider(responses=["response"])

    assert provider.call_count == 0

    await provider.generate("prompt 1")
    assert provider.call_count == 1

    await provider.generate("prompt 2")
    assert provider.call_count == 2


async def test_mock_llm_accepts_kwargs() -> None:
    """Test that MockLLMProvider accepts and ignores kwargs like real providers."""
    provider = MockLLMProvider(responses=["response"])

    # Should not raise any errors with various kwargs
    result = await provider.generate("prompt", temperature=0.7, max_tokens=100, model="gpt-4")
    assert result == "response"
