"""Test create_session HTTP implementation."""

import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio
async def test_create_session_makes_http_post_request(httpx_mock):
    """Test create_session makes HTTP POST request to correct endpoint."""
    httpx_mock.add_response(
        json={"session_id": "session-abc123", "created_at": "2024-01-01T00:00:00Z"}
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "http://localhost:3001/v1/sessions"

    # Verify response
    assert isinstance(session_id, str)
    assert session_id == "session-abc123"
