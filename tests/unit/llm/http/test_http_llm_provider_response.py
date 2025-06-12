"""Test HTTP response handling and request formatting."""

import json
import httpx
import pytest

from zenyth.llm import HTTPLLMProvider


@pytest.mark.asyncio()
async def test_generate_extracts_content_from_json_response(httpx_mock):
    """Test that generate extracts 'content' field from JSON response."""
    httpx_mock.add_response(json={"content": "The answer is 42"})

    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    result = await provider.generate("What is the meaning of life?")

    assert result == "The answer is 42"


@pytest.mark.asyncio()
async def test_generate_sends_correct_json_payload(httpx_mock):
    """Test that generate sends the prompt in correct JSON format."""
    httpx_mock.add_response(json={"content": "response"})

    provider = HTTPLLMProvider(base_url="http://test.example.com")
    await provider.generate("Test prompt", temperature=0.5, max_tokens=100)

    # Check the request that was made
    request = httpx_mock.get_request()

    # Check JSON payload
    json_data = json.loads(request.content)

    assert json_data["prompt"] == "Test prompt"
    assert json_data["temperature"] == 0.5
    assert json_data["max_tokens"] == 100
