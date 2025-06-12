"""Test revert_session HTTP implementation."""

import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio
async def test_revert_session_makes_http_delete_request(httpx_mock):
    """Test revert_session makes HTTP DELETE request to correct endpoint."""
    httpx_mock.add_response(json={"success": True, "messages_removed": 2})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    await provider.revert_session("session-abc123", steps=2)

    # Verify HTTP request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "DELETE"
    assert str(request.url) == "http://localhost:3001/v1/sessions/session-abc123/messages"

    # Verify request payload
    import json

    json_data = json.loads(request.content)
    assert json_data["steps"] == 2


@pytest.mark.asyncio
async def test_revert_session_with_default_steps(httpx_mock):
    """Test revert_session uses default steps value of 1."""
    httpx_mock.add_response(json={"success": True, "messages_removed": 1})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    await provider.revert_session("session-abc123")

    # Verify request payload has steps=1
    requests = httpx_mock.get_requests()
    import json

    json_data = json.loads(requests[0].content)
    assert json_data["steps"] == 1
