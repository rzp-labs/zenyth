"""Test stream_chat edge cases for better coverage."""

import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio()
async def test_stream_chat_handles_malformed_json(httpx_mock):
    """Test stream_chat skips malformed JSON lines."""
    # Mock a streaming response with malformed JSON
    response_content = (
        b'data: {"content": "Hello", "metadata": {"chunk_index": 0}}\n\n'
        b"data: {malformed json here\n\n"  # This will cause JSONDecodeError
        b'data: {"content": " world", "metadata": {"chunk_index": 1}}\n\n'
        b"data: [DONE]\n\n"
    )

    httpx_mock.add_response(headers={"content-type": "text/event-stream"}, content=response_content)

    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    # Collect all streamed responses
    responses = []
    async for chunk in provider.stream_chat("Tell me a story"):
        responses.append(chunk)

    # Should skip the malformed line and continue
    assert len(responses) == 2
    assert responses[0].content == "Hello"
    assert responses[1].content == " world"
