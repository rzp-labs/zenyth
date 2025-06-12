"""Test stream_chat HTTP implementation."""

import json

import pytest

from zenyth.core.types import LLMResponse
from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio()
async def test_stream_chat_makes_http_post_request_with_streaming(httpx_mock):
    """Test stream_chat makes HTTP POST request with streaming enabled."""
    # Mock a streaming response with multiple chunks
    response_content = (
        b'data: {"content": "Hello", "metadata": {"chunk_index": 0}}\n\n'
        b'data: {"content": " world", "metadata": {"chunk_index": 1}}\n\n'
        b'data: {"content": "!", "metadata": {"chunk_index": 2}}\n\n'
        b"data: [DONE]\n\n"
    )

    httpx_mock.add_response(headers={"content-type": "text/event-stream"}, content=response_content)

    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    # Collect all streamed responses
    responses = []
    async for chunk in provider.stream_chat("Tell me a story"):
        responses.append(chunk)

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "http://localhost:3001/v1/chat/completions/stream"

    # Verify request payload
    json_data = json.loads(request.content)
    assert json_data["prompt"] == "Tell me a story"
    assert json_data["stream"] is True

    # Verify responses
    assert len(responses) == 3
    assert all(isinstance(r, LLMResponse) for r in responses)
    assert responses[0].content == "Hello"
    assert responses[1].content == " world"
    assert responses[2].content == "!"
    assert responses[0].metadata["chunk_index"] == 0
    assert responses[1].metadata["chunk_index"] == 1
    assert responses[2].metadata["chunk_index"] == 2
