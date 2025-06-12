"""Test complete_chat HTTP implementation."""

import pytest

from zenyth.core.types import LLMResponse
from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio()
async def test_complete_chat_makes_http_post_request(httpx_mock):
    """Test complete_chat makes HTTP POST request to correct endpoint."""
    httpx_mock.add_response(
        json={
            "content": "The answer is 42",
            "model": "claude-3",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    response = await provider.complete_chat("What is the meaning of life?")

    # Verify response structure
    assert isinstance(response, LLMResponse)
    assert response.content == "The answer is 42"
    assert response.metadata["model"] == "claude-3"

    # Verify HTTP request was made (get_requests returns list)
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "http://localhost:3001/v1/chat/completions"
