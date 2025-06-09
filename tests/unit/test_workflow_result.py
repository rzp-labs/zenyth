"""Test suite for WorkflowResult dataclass implementation.

Tests the immutable result container for complete SPARC workflow execution outcomes,
validating data integrity, immutability, and proper SOLID principles implementation.

SOLID Principles Alignment:
    - Single Responsibility: WorkflowResult has one clear purpose - containing workflow outcomes
    - Open/Closed: Immutable dataclass is closed for modification, extensible through composition
    - Liskov Substitution: N/A (dataclass, not inheritance hierarchy)
    - Interface Segregation: Focused data container without methods, clean interface
    - Dependency Inversion: Depends on abstract PhaseResult, not concrete implementations
"""

from dataclasses import FrozenInstanceError

import pytest

from zenyth.core.types import PhaseResult, WorkflowResult


def test_workflow_result_creation_successful() -> None:
    """Test creating successful WorkflowResult with all fields.

    Validates Single Responsibility - WorkflowResult solely contains workflow data.
    Tests immutability following Open/Closed principle (closed for modification).
    """
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


def test_workflow_result_creation_failed() -> None:
    """Test creating failed WorkflowResult with error information.

    Validates proper error state representation and immutability.
    """
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


def test_workflow_result_minimal_creation() -> None:
    """Test WorkflowResult with only required fields.

    Validates default field behavior and minimal interface compliance.
    """
    result = WorkflowResult(success=True, task="Simple task")

    assert result.success is True
    assert result.task == "Simple task"
    assert result.phases_completed == []
    assert result.artifacts == {}
    assert result.error is None
    assert result.metadata == {}


def test_workflow_result_immutability() -> None:
    """Test that WorkflowResult is immutable after creation.

    Validates Open/Closed principle - closed for modification after creation.
    Ensures thread-safety and data integrity in concurrent environments.
    """
    result = WorkflowResult(success=True, task="Test task", artifacts={"test": "data"})

    # Should not be able to modify any attributes
    with pytest.raises(
        (AttributeError, FrozenInstanceError), match=r"can't set attribute|cannot assign to field"
    ):
        result.success = False

    with pytest.raises(
        (AttributeError, FrozenInstanceError), match=r"can't set attribute|cannot assign to field"
    ):
        result.task = "Modified task"


def test_workflow_result_with_phase_results() -> None:
    """Test WorkflowResult containing multiple PhaseResult objects.

    Validates Dependency Inversion - depends on PhaseResult abstraction.
    Tests composition over inheritance pattern.
    """
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
        metadata={"total_duration": 225.5, "phases_executed": 3, "session_id": "auth-workflow-001"},
    )

    assert len(result.phases_completed) == 3
    assert result.phases_completed[0].phase_name == "specification"
    assert result.phases_completed[1].phase_name == "architecture"
    assert result.phases_completed[2].phase_name == "completion"
    assert result.metadata["phases_executed"] == 3
    assert result.metadata["total_duration"] == 225.5


def test_workflow_result_empty_collections() -> None:
    """Test WorkflowResult with empty collections for optional fields.

    Validates proper default field behavior and interface robustness.
    """
    result = WorkflowResult(
        success=True, task="Empty workflow test", phases_completed=[], artifacts={}, metadata={}
    )

    assert result.phases_completed == []
    assert result.artifacts == {}
    assert result.metadata == {}
    assert len(result.phases_completed) == 0
    assert len(result.artifacts) == 0
    assert len(result.metadata) == 0


def test_workflow_result_type_annotations() -> None:
    """Test that WorkflowResult has proper type annotations.

    Validates type safety and enables static analysis tools.
    """
    # Verify field types through annotations
    annotations = WorkflowResult.__annotations__
    assert annotations["success"] is bool
    assert annotations["task"] is str
    assert "list" in str(annotations["phases_completed"])
    assert "dict" in str(annotations["artifacts"])
    assert "str | None" in str(annotations["error"]) or "Optional" in str(annotations["error"])
    assert "dict" in str(annotations["metadata"])


def test_workflow_result_string_representation() -> None:
    """Test WorkflowResult string representation for debugging.

    Validates that the dataclass provides useful string representation.
    """
    result = WorkflowResult(success=True, task="String repr test", metadata={"test": "value"})

    result_str = str(result)
    assert "WorkflowResult" in result_str
    assert "success=True" in result_str
    assert "String repr test" in result_str
