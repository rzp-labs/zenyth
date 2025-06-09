"""Mock implementations for testing Zenyth orchestration components.

This module provides controllable mock implementations of external dependencies
like LLM providers and MCP servers. These mocks enable comprehensive unit testing
of orchestration logic without requiring real external services, following the
Dependency Inversion Principle (DIP) by implementing the same interfaces as
production components.

The mock implementations are designed for deterministic testing scenarios while
maintaining the same behavioral contracts as their production counterparts.
This ensures that code tested with mocks will work correctly with real services.

Key Design Principles:
    - Implement the same interfaces as production components (LSP compliance)
    - Provide configurable, predictable behavior for test scenarios
    - Enable introspection for verifying call patterns and arguments
    - Support both success and failure simulation for robust error testing
    - Maintain thread-safety for concurrent test execution

Available Mock Classes:
    MockLLMProvider: Simulates LLM text generation with configurable responses
    MockMCPServer: Simulates MCP server tool execution with controlled outcomes

Examples:
    Basic LLM mock usage::

        mock_llm = MockLLMProvider(responses=["Hello, world!", "How can I help?"])
        response1 = await mock_llm.generate("greeting")  # Returns "Hello, world!"
        response2 = await mock_llm.generate("question")  # Returns "How can I help?"

    Error simulation::

        mock_llm = MockLLMProvider(responses=["success"], errors=["API timeout"])
        # First call succeeds, second raises exception

    Call tracking::

        mock_llm = MockLLMProvider(responses=["response"])
        await mock_llm.generate("test prompt", temperature=0.7)
        assert mock_llm.call_count == 1
        assert "temperature" in mock_llm.last_kwargs

Note:
    Mock implementations should only be used in test environments. Production
    code should always use real service implementations through dependency
    injection to ensure proper system behavior and integration testing.
"""

from .llm_provider import MockLLMProvider

__all__ = ["MockLLMProvider"]
