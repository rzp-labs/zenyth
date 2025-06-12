"""Test creating successful WorkflowResult with all fields.

This test validates Single Responsibility - WorkflowResult solely contains workflow data.
Tests immutability following Open/Closed principle (closed for modification).
"""

from zenyth.core.types import PhaseResult, WorkflowResult


def test_workflow_result_creation_successful() -> None:
    """Test creating successful WorkflowResult with all fields."""
    phases = [
        PhaseResult(phase_name="specification", artifacts={"spec": "requirements"}),
        PhaseResult(phase_name="architecture", artifacts={"design": "system_design"}),
    ]

    result = WorkflowResult(
        success=True,
        task="Implement user authentication",
        phases_completed=phases,
        artifacts={"final_code": "auth_implementation"},
        metadata={"duration": 125.5, "session_id": "test-123"},
    )

    assert result.success is True
    assert result.task == "Implement user authentication"
    assert len(result.phases_completed) == 2
    assert result.artifacts["final_code"] == "auth_implementation"
    assert result.error is None
    assert result.metadata["duration"] == 125.5
