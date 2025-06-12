"""Test get_session_metadata HTTP implementation."""

import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio
async def test_get_session_metadata_makes_http_get_request(httpx_mock):
    """Test get_session_metadata makes HTTP GET request to correct endpoint."""
    httpx_mock.add_response(
        json={
            "session_id": "session-abc123",
            "created_at": "2024-01-01T00:00:00Z",
            "message_count": 5,
            "model": "claude-3",
            "total_tokens": 1500,
            "parent_session_id": None,
        }
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    metadata = await provider.get_session_metadata("session-abc123")

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "GET"
    assert str(request.url) == "http://localhost:3001/v1/sessions/session-abc123/metadata"

    # Verify response
    assert isinstance(metadata, dict)
    assert metadata["session_id"] == "session-abc123"
    assert metadata["message_count"] == 5
    assert metadata["model"] == "claude-3"
