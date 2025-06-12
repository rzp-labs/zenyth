"""Test WorkflowResult string representation for debugging.

This test validates that the dataclass provides useful string representation.
"""

from zenyth.core.types import WorkflowResult


def test_workflow_result_string_representation() -> None:
    """Test WorkflowResult string representation for debugging."""
    result = WorkflowResult(success=True, task="String repr test", metadata={"test": "value"})

    result_str = str(result)
    assert "WorkflowResult" in result_str
    assert "success=True" in result_str
    assert "String repr test" in result_str
