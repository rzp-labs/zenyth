"""Test get_session_history HTTP implementation."""

import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio
async def test_get_session_history_makes_http_get_request(httpx_mock):
    """Test get_session_history makes HTTP GET request to correct endpoint."""
    httpx_mock.add_response(
        json={
            "messages": [
                {"role": "user", "content": "What is 2+2?"},
                {"role": "assistant", "content": "The answer is 4"},
            ],
            "session_id": "session-abc123",
            "created_at": "2024-01-01T00:00:00Z",
            "message_count": 2,
        }
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    history = await provider.get_session_history("session-abc123")

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "GET"
    assert str(request.url) == "http://localhost:3001/v1/sessions/session-abc123/history"

    # Verify response
    assert isinstance(history, dict)
    assert "messages" in history
    assert len(history["messages"]) == 2
    assert history["session_id"] == "session-abc123"
    assert history["message_count"] == 2
