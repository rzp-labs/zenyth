"""Test complete_chat_with_session HTTP implementation."""

import pytest

from zenyth.llm import HTTPLLMProvider
from zenyth.core.types import LLMResponse


@pytest.mark.asyncio
async def test_complete_chat_with_session_makes_http_post_request(httpx_mock):
    """Test complete_chat_with_session makes HTTP POST request with session ID."""
    httpx_mock.add_response(
        json={
            "content": "Based on our previous conversation, the answer is 42",
            "model": "claude-3",
            "session_id": "session-abc123",
            "usage": {"prompt_tokens": 15, "completion_tokens": 10},
        }
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    response = await provider.complete_chat_with_session(
        "session-abc123", "What was my previous question about?"
    )

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "http://localhost:3001/v1/chat/completions"

    # Verify request payload includes session ID
    import json

    json_data = json.loads(request.content)
    assert json_data["session_id"] == "session-abc123"
    assert json_data["prompt"] == "What was my previous question about?"

    # Verify response
    assert isinstance(response, LLMResponse)
    assert response.content == "Based on our previous conversation, the answer is 42"
    assert response.metadata["session_id"] == "session-abc123"
