"""
Test actual behavior of HTTPLLMProvider beyond stub responses.

Following TDD principles: ONE test at a time, testing behavior not implementation.
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio()
async def test_generate_returns_different_responses_for_different_prompts(httpx_mock):
    """Test that generate returns contextually appropriate responses.

    Current implementation returns "test response" for everything.
    This test expects the response to vary based on the prompt.

    This is testing BEHAVIOR, not implementation details.
    """
    # Mock different responses for different prompts
    httpx_mock.add_response(json={"content": "4"}, match_json={"prompt": "What is 2+2?"})
    httpx_mock.add_response(
        json={"content": "Paris"}, match_json={"prompt": "What is the capital of France?"}
    )

    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    response1 = await provider.generate("What is 2+2?")
    response2 = await provider.generate("What is the capital of France?")

    # Responses should be different for different questions
    assert response1 != response2
    assert response1 == "4"
    assert response2 == "Paris"


@pytest.mark.asyncio()
async def test_generate_raises_error_when_service_unavailable():
    """Test that generate raises an error when HTTP service is unavailable."""
    provider = HTTPLLMProvider(base_url="http://localhost:9999")

    with pytest.raises(httpx.ConnectError):
        await provider.generate("Test prompt")
