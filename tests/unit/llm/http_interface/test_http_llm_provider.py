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

from collections.abc import Mapping

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


@pytest.mark.asyncio()
async def test_http_provider_generate_returns_string(httpx_mock):
    """Test HTTPLLMProvider.generate returns a string response.

    This test validates that the generate method returns actual content
    rather than empty string.
    """
    # Mock the HTTP response
    httpx_mock.add_response(json={"content": "test response"})

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


@pytest.mark.asyncio()
async def test_http_provider_complete_chat_returns_llm_response(httpx_mock):
    """Test HTTPLLMProvider.complete_chat returns LLMResponse.

    This test validates that complete_chat returns a proper LLMResponse
    with content and metadata.
    """
    # Mock the HTTP response
    httpx_mock.add_response(
        json={
            "content": "4",
            "model": "test",
            "usage": {"prompt_tokens": 5, "completion_tokens": 1},
        },
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    response = await provider.complete_chat("What is 2+2?")

    assert isinstance(response, LLMResponse)
    assert isinstance(response.content, str)
    assert len(response.content) > 0
    assert isinstance(response.metadata, Mapping)
    assert response.metadata["model"] == "test"


def test_http_provider_normalizes_base_url():
    """Test HTTPLLMProvider normalizes the base URL.

    This test validates that the provider removes trailing slashes
    from the base URL for consistent API calls.
    """
    provider = HTTPLLMProvider(base_url="http://localhost:3001/")
    assert provider.base_url == "http://localhost:3001"


@pytest.mark.asyncio()
async def test_http_provider_create_session_returns_session_id(httpx_mock):
    """Test HTTPLLMProvider.create_session returns a session ID.

    This test validates that create_session returns a non-empty string
    that can be used to identify the session.
    """
    # Mock the HTTP response
    httpx_mock.add_response(json={"session_id": "session-123"})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()

    assert isinstance(session_id, str)
    assert len(session_id) > 0
    assert session_id  # Non-empty string check


# Non-empty string check


@pytest.mark.asyncio()
async def test_http_provider_complete_chat_with_session(httpx_mock):
    """Test HTTPLLMProvider.complete_chat_with_session returns LLMResponse.

    This test validates that complete_chat_with_session maintains session context
    and returns proper response.
    """
    # Mock the HTTP response
    httpx_mock.add_response(json={"content": "4", "model": "test", "session_id": "session-123"})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = "session-123"
    response = await provider.complete_chat_with_session(session_id, "What is 2+2?")

    assert isinstance(response, LLMResponse)
    assert isinstance(response.content, str)
    assert response.metadata["session_id"] == session_id


# Non-empty string check


@pytest.mark.asyncio()
async def test_http_provider_get_session_history(httpx_mock):
    """Test HTTPLLMProvider.get_session_history returns session data.

    This test validates that get_session_history returns a dictionary
    with session messages and metadata.
    """
    # Mock the HTTP response
    httpx_mock.add_response(
        json={
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
            "session_id": "session-123",
        },
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = "session-123"
    history = await provider.get_session_history(session_id)

    assert isinstance(history, dict)
    assert "messages" in history
    assert isinstance(history["messages"], list)
    assert len(history["messages"]) == 2


@pytest.mark.asyncio()
async def test_http_provider_fork_session(httpx_mock):
    """Test HTTPLLMProvider.fork_session creates a new session.

    This test validates that fork_session returns a new session ID
    different from the original.
    """
    # Mock the HTTP response
    httpx_mock.add_response(json={"session_id": "session-123-fork-test-fork"})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    original_session = "session-123"
    forked_session = await provider.fork_session(original_session, name="test-fork")

    assert isinstance(forked_session, str)
    assert len(forked_session) > 0
    assert forked_session == "session-123-fork-test-fork"


@pytest.mark.asyncio()
async def test_http_provider_revert_session(httpx_mock):
    """Test HTTPLLMProvider.revert_session doesn't raise exception.

    This test validates that revert_session can be called without error.
    """
    # Mock the HTTP response
    httpx_mock.add_response(json={"success": True})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = "session-123"

    # Should not raise any exception
    await provider.revert_session(session_id, steps=2)
    assert True  # If we get here, no exception was raised


# If we get here, no exception was raised


@pytest.mark.asyncio()
async def test_http_provider_get_session_metadata(httpx_mock):
    """Test HTTPLLMProvider.get_session_metadata returns metadata.

    This test validates that get_session_metadata returns a dictionary
    with session information.
    """
    # Mock the HTTP response
    httpx_mock.add_response(
        json={
            "session_id": "session-123",
            "created_at": "2024-01-01T00:00:00Z",
            "message_count": 5,
        },
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = "session-123"
    metadata = await provider.get_session_metadata(session_id)

    assert isinstance(metadata, dict)
    assert "session_id" in metadata
    assert metadata["session_id"] == session_id
    assert metadata["message_count"] == 5


@pytest.mark.asyncio()
async def test_http_provider_stream_chat(httpx_mock):
    """Test HTTPLLMProvider.stream_chat returns async generator.

    This test validates that stream_chat can be called and yields responses.
    """
    # Mock the streaming response
    response_content = (
        b'data: {"content": "Hello", "metadata": {"chunk_index": 0}}\n\n'
        b'data: {"content": " world", "metadata": {"chunk_index": 1}}\n\n'
        b"data: [DONE]\n\n"
    )

    httpx_mock.add_response(headers={"content-type": "text/event-stream"}, content=response_content)

    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    # Collect all streamed responses
    responses = []
    async for chunk in provider.stream_chat("Hello"):
        responses.append(chunk)

    assert len(responses) > 0
    assert responses[0] is not None
    assert isinstance(responses[0], LLMResponse)
    assert responses[0].content == "Hello"
    assert responses[1].content == " world"
