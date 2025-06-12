"""Test WorkflowResult with only required fields.

This test validates default field behavior and minimal interface compliance.
"""

from zenyth.core.types import WorkflowResult


def test_workflow_result_minimal_creation() -> None:
    """Test WorkflowResult with only required fields."""
    result = WorkflowResult(success=True, task="Simple task")

    assert result.success is True
    assert result.task == "Simple task"
    assert result.phases_completed == []
    assert result.artifacts == {}
    assert result.error is None
    assert result.metadata == {}
