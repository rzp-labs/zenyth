"""Test HTTP error handling."""

import httpx
import pytest

from zenyth.llm import HTTPLLMProvider
from zenyth.llm.http_provider import MissingContentFieldError, MissingSessionIdFieldError


@pytest.mark.asyncio()
async def test_generate_handles_missing_content_field(httpx_mock):
    """Test that generate handles response without 'content' field gracefully."""
    # Mock a response without 'content' field
    httpx_mock.add_response(json={"error": "Invalid response", "status": "failed"})

    provider = HTTPLLMProvider(base_url="http://test.example.com")

    # This will fail because response doesn't have 'content' field
    with pytest.raises(MissingContentFieldError):
        await provider.generate("Test")


@pytest.mark.asyncio()
async def test_generate_handles_server_errors(httpx_mock):
    """Test generate method handles HTTP server errors properly."""
    httpx_mock.add_response(status_code=503, json={"error": "Service unavailable"})
    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await provider.generate("Test")
    assert exc_info.value.response.status_code == 503


@pytest.mark.asyncio()
async def test_complete_chat_handles_missing_content(httpx_mock):
    """Test complete_chat handles missing content field."""
    httpx_mock.add_response(json={"model": "test", "usage": {}})
    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    with pytest.raises(MissingContentFieldError):
        await provider.complete_chat("Test")


@pytest.mark.asyncio()
async def test_create_session_handles_missing_session_id(httpx_mock):
    """Test create_session handles missing session_id field."""
    httpx_mock.add_response(json={"created_at": "2024-01-01T00:00:00Z"})
    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    with pytest.raises(MissingSessionIdFieldError):
        await provider.create_session()


@pytest.mark.asyncio()
async def test_complete_chat_with_session_handles_missing_content(httpx_mock):
    """Test complete_chat_with_session handles missing content field."""
    httpx_mock.add_response(json={"session_id": "test-123", "model": "test"})
    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    with pytest.raises(MissingContentFieldError):
        await provider.complete_chat_with_session("test-123", "Test prompt")
