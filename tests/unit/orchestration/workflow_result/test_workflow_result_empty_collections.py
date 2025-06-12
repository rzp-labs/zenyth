"""Test WorkflowResult with empty collections for optional fields.

This test validates proper default field behavior and interface robustness.
"""

from zenyth.core.types import WorkflowResult


def test_workflow_result_empty_collections() -> None:
    """Test WorkflowResult with empty collections for optional fields."""
    result = WorkflowResult(
        success=True,
        task="Empty workflow test",
        phases_completed=[],
        artifacts={},
        metadata={},
    )

    assert result.phases_completed == []
    assert result.artifacts == {}
    assert result.metadata == {}
    assert len(result.phases_completed) == 0
    assert len(result.artifacts) == 0
    assert len(result.metadata) == 0
