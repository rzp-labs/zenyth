"""Test that orchestrator.execute returns proper WorkflowResult.

This test validates Single Responsibility - orchestrator coordinates workflow execution.
Tests return type compliance with WorkflowResult contract.
"""

import pytest

from zenyth.core.types import WorkflowResult


@pytest.mark.asyncio()
async def test_orchestration_integration_execute_returns_workflow_result(orchestrator_with_mocks):
    """Test that orchestrator.execute returns proper WorkflowResult."""
    result = await orchestrator_with_mocks.execute("Test task execution")

    # Should return WorkflowResult instance
    assert isinstance(result, WorkflowResult)
    assert hasattr(result, "success")
    assert hasattr(result, "task")
    assert hasattr(result, "phases_completed")
    assert hasattr(result, "artifacts")
    assert hasattr(result, "error")
    assert hasattr(result, "metadata")
