"""Unit tests for HTTPLLMProvider implementation.

This test module validates the HTTPLLMProvider concrete implementation following
TDD principles. Tests focus on behavior and protocol compliance rather than
implementation details.

SOLID Principles Alignment:
- SRP: Each test validates one specific aspect of provider behavior
- OCP: Tests validate interface compliance without depending on internals
- LSP: Tests ensure HTTPLLMProvider is substitutable for LLMInterface
- ISP: Tests focus only on the required interface methods
- DIP: Tests depend on LLMInterface abstraction for protocol checking
"""

import pytest

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import LLMResponse
from zenyth.llm import HTTPLLMProvider


def test_http_provider_implements_llm_interface():
    """Test HTTPLLMProvider implements LLMInterface protocol.

    This test validates that HTTPLLMProvider satisfies the LLMInterface
    protocol contract, enabling it to be used wherever LLMInterface is expected.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    assert isinstance(provider, LLMInterface)


@pytest.mark.asyncio
async def test_http_provider_generate_returns_string():
    """Test HTTPLLMProvider.generate returns a string response.

    This test validates that the generate method returns actual content
    rather than empty string.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    result = await provider.generate("Hello, world!")
    assert isinstance(result, str)
    assert len(result) > 0


# Should return non-empty response


def test_http_provider_init_requires_base_url():
    """Test HTTPLLMProvider requires base_url for initialization.

    This test validates that the provider needs configuration to know
    where to send HTTP requests.
    """
    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        HTTPLLMProvider()  # Should fail without base_url


@pytest.mark.asyncio
async def test_http_provider_complete_chat_returns_llm_response():
    """Test HTTPLLMProvider.complete_chat returns LLMResponse.

    This test validates that complete_chat returns a proper LLMResponse
    with content and metadata.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    response = await provider.complete_chat("What is 2+2?")

    assert isinstance(response, LLMResponse)
    assert isinstance(response.content, str)
    assert len(response.content) > 0
    assert isinstance(response.metadata, dict)


def test_http_provider_normalizes_base_url():
    """Test HTTPLLMProvider normalizes the base URL.

    This test validates that the provider removes trailing slashes
    from the base URL for consistent API calls.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001/")
    assert provider.base_url == "http://localhost:3001"


@pytest.mark.asyncio
async def test_http_provider_create_session_returns_session_id():
    """Test HTTPLLMProvider.create_session returns a session ID.

    This test validates that create_session returns a non-empty string
    that can be used to identify the session.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()

    assert isinstance(session_id, str)
    assert len(session_id) > 0
    assert session_id != ""


@pytest.mark.asyncio
async def test_http_provider_complete_chat_with_session():
    """Test HTTPLLMProvider.complete_chat_with_session returns LLMResponse.

    This test validates that complete_chat_with_session maintains session context
    and returns proper response.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()
    response = await provider.complete_chat_with_session(session_id, "What is 2+2?")

    assert isinstance(response, LLMResponse)
    assert isinstance(response.content, str)
    assert len(response.content) > 0
    assert response.content != ""


@pytest.mark.asyncio
async def test_http_provider_get_session_history():
    """Test HTTPLLMProvider.get_session_history returns session data.

    This test validates that get_session_history returns a dictionary
    with session messages and metadata.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()
    history = await provider.get_session_history(session_id)

    assert isinstance(history, dict)
    assert "messages" in history
    assert isinstance(history["messages"], list)


@pytest.mark.asyncio
async def test_http_provider_fork_session():
    """Test HTTPLLMProvider.fork_session creates a new session.

    This test validates that fork_session returns a new session ID
    different from the original.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    original_session = await provider.create_session()
    forked_session = await provider.fork_session(original_session, name="test-fork")

    assert isinstance(forked_session, str)
    assert len(forked_session) > 0
    assert forked_session != original_session


@pytest.mark.asyncio
async def test_http_provider_revert_session():
    """Test HTTPLLMProvider.revert_session doesn't raise exception.

    This test validates that revert_session can be called without error.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()

    # Should not raise any exception
    await provider.revert_session(session_id, steps=2)
    assert True  # If we get here, no exception was raised


@pytest.mark.asyncio
async def test_http_provider_get_session_metadata():
    """Test HTTPLLMProvider.get_session_metadata returns metadata.

    This test validates that get_session_metadata returns a dictionary
    with session information.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()
    metadata = await provider.get_session_metadata(session_id)

    assert isinstance(metadata, dict)
    assert "session_id" in metadata
    assert metadata["session_id"] == session_id


@pytest.mark.asyncio
async def test_http_provider_stream_chat():
    """Test HTTPLLMProvider.stream_chat returns async generator.

    This test validates that stream_chat can be called and yields responses.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    # Get the generator
    generator = await provider.stream_chat("Hello")

    # Collect all streamed responses
    responses = []
    async for chunk in generator:
        responses.append(chunk)

    assert len(responses) > 0
    assert responses[0] is not None
