"""Test WorkflowResult containing multiple PhaseResult objects.

This test validates Dependency Inversion - depends on PhaseResult abstraction.
Tests composition over inheritance pattern.
"""

from zenyth.core.types import PhaseResult, WorkflowResult


def test_workflow_result_with_phase_results() -> None:
    """Test WorkflowResult containing multiple PhaseResult objects."""
    phase1 = PhaseResult(
        phase_name="specification",
        artifacts={"requirements": "User auth requirements"},
        metadata={"duration": 45.2},
    )

    phase2 = PhaseResult(
        phase_name="architecture",
        artifacts={"design": "Component architecture"},
        next_phase="completion",
        metadata={"duration": 67.8},
    )

    phase3 = PhaseResult(
        phase_name="completion",
        artifacts={"code": "Authentication implementation"},
        metadata={"duration": 112.5},
    )

    result = WorkflowResult(
        success=True,
        task="Build authentication system",
        phases_completed=[phase1, phase2, phase3],
        artifacts={
            "specification_document": phase1.artifacts["requirements"],
            "architecture_design": phase2.artifacts["design"],
            "implementation_code": phase3.artifacts["code"],
        },
        metadata={
            "total_duration": 225.5,
            "phases_executed": 3,
            "session_id": "auth-workflow-001",
        },
    )

    assert len(result.phases_completed) == 3
    assert result.phases_completed[0].phase_name == "specification"
    assert result.phases_completed[1].phase_name == "architecture"
    assert result.phases_completed[2].phase_name == "completion"
    assert result.metadata["phases_executed"] == 3
    assert result.metadata["total_duration"] == 225.5
