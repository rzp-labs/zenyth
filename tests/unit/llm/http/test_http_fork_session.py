"""Test fork_session HTTP implementation."""

import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio
async def test_fork_session_makes_http_post_request(httpx_mock):
    """Test fork_session makes HTTP POST request to correct endpoint."""
    httpx_mock.add_response(
        json={
            "session_id": "session-fork-123",
            "parent_session_id": "session-abc123",
            "name": "test-fork",
            "created_at": "2024-01-01T00:00:00Z",
        }
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    forked_id = await provider.fork_session("session-abc123", name="test-fork")

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "http://localhost:3001/v1/sessions/session-abc123/fork"

    # Verify request payload
    import json

    json_data = json.loads(request.content)
    assert json_data["name"] == "test-fork"

    # Verify response
    assert isinstance(forked_id, str)
    assert forked_id == "session-fork-123"


@pytest.mark.asyncio
async def test_fork_session_without_name(httpx_mock):
    """Test fork_session works without a name parameter."""
    httpx_mock.add_response(
        json={
            "session_id": "session-fork-456",
            "parent_session_id": "session-abc123",
        }
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    forked_id = await provider.fork_session("session-abc123")

    # Verify request payload has no name
    requests = httpx_mock.get_requests()
    import json

    json_data = json.loads(requests[0].content)
    assert "name" not in json_data or json_data["name"] is None

    assert forked_id == "session-fork-456"
