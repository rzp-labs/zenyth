"""Test creating failed WorkflowResult with error information.

This test validates proper error state representation and immutability.
"""

from zenyth.core.types import PhaseResult, WorkflowResult


def test_workflow_result_creation_failed() -> None:
    """Test creating failed WorkflowResult with error information."""
    phases = [PhaseResult(phase_name="specification", artifacts={"spec": "partial"})]

    result = WorkflowResult(
        success=False,
        task="Complex implementation",
        phases_completed=phases,
        artifacts={"partial_work": "incomplete"},
        error="Architecture phase failed due to complexity",
        metadata={"failure_phase": "architecture", "retry_possible": True},
    )

    assert result.success is False
    assert result.task == "Complex implementation"
    assert result.error == "Architecture phase failed due to complexity"
    assert result.metadata["failure_phase"] == "architecture"
    assert result.metadata["retry_possible"] is True
