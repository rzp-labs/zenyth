"""Test that execute method has correct parameter signature.

This test validates interface contract for orchestration execution following
Interface Segregation Principle - clean, focused method signatures.
"""

import pytest

from zenyth.orchestration import SPARCOrchestrator


@pytest.mark.asyncio()
async def test_sparc_orchestrator_execute_signature() -> None:
    """Test that execute method has correct parameter signature."""
    # Provide valid mock dependencies for successful execution
    orchestrator = SPARCOrchestrator(
        llm_provider="mock_llm",
        tool_registry="mock_tools",
        state_manager="mock_state",
    )

    # Execute should accept task string and return WorkflowResult
    result = await orchestrator.execute("test task")

    # Should return some kind of result object
    assert result is not None
