"""Comprehensive unit tests for Zenyth core data types.

This test module validates the behavior, immutability, and contract compliance
of the fundamental data structures used throughout the Zenyth SPARC orchestration
system. Each test follows the Single Responsibility Principle (SRP) by testing
exactly one behavioral aspect of the target classes.

The tests ensure that PhaseResult and SessionContext maintain their contracts
for immutability, field validation, equality comparison, and string representation.
These guarantees are critical for reliable orchestration and debugging in
homelab environments where data integrity and audit trails are essential.

Test Organization:
    - PhaseResult tests: Validate success/failure result containers
    - SessionContext tests: Validate session state management
    - Immutability tests: Ensure frozen dataclass behavior
    - Equality tests: Verify comparison operations
    - Representation tests: Check string formatting

Testing Strategy:
    - Each test validates one specific behavior (SRP compliance)
    - Tests are independent and can run in any order
    - Clear test naming describes expected behavior
    - Comprehensive coverage of all field combinations
    - Edge cases and boundary conditions included

Examples:
    Running all core type tests::

        pytest tests/unit/test_core_types.py -v

    Running specific test categories::

        pytest tests/unit/test_core_types.py -k "phase_result" -v
        pytest tests/unit/test_core_types.py -k "session_context" -v
        pytest tests/unit/test_core_types.py -k "immutable" -v

    Checking test coverage::

        pytest tests/unit/test_core_types.py --cov=zenyth.core.types
"""

import pytest

from zenyth.core.types import PhaseResult, SessionContext


def test_phase_result_accepts_phase_name_field() -> None:
    """Test PhaseResult accepts phase_name field."""

    result = PhaseResult(phase_name="specification")
    assert result.phase_name == "specification"


def test_phase_result_accepts_artifacts_field() -> None:
    """Test PhaseResult accepts artifacts field."""

    artifacts = {"document": "test output"}
    result = PhaseResult(phase_name="specification", artifacts=artifacts)
    assert result.artifacts == artifacts


def test_phase_result_stores_metadata_when_provided() -> None:
    """Test PhaseResult stores metadata field when provided."""

    metadata = {"duration": 1.5, "tokens": 100}
    result = PhaseResult(phase_name="specification", metadata=metadata)
    assert result.metadata == metadata


def test_phase_result_defaults_next_phase_to_none() -> None:
    """Test PhaseResult defaults next_phase to None when not provided."""

    result = PhaseResult(phase_name="specification")
    assert result.next_phase is None


def test_phase_result_stores_metadata_when_provided_updated() -> None:
    """Test PhaseResult stores metadata field when provided."""

    metadata = {"duration": 1.5}
    result = PhaseResult(phase_name="specification", metadata=metadata)
    assert result.metadata == metadata


def test_phase_result_defaults_metadata_to_empty_dict() -> None:
    """Test PhaseResult defaults metadata to empty dict when not provided."""

    result = PhaseResult(phase_name="specification")
    assert result.metadata == {}


def test_phase_result_provides_string_representation() -> None:
    """Test PhaseResult provides string representation."""

    result = PhaseResult(phase_name="specification")
    assert str(result) is not None
    assert len(str(result)) > 0


def test_phase_result_string_contains_phase_name() -> None:
    """Test PhaseResult string representation contains phase name."""

    result = PhaseResult(phase_name="specification")
    assert "specification" in str(result)


def test_phase_result_supports_equality_comparison() -> None:
    """Test PhaseResult supports equality comparison."""

    result1 = PhaseResult(phase_name="specification")
    result2 = PhaseResult(phase_name="specification")
    assert result1 == result2


def test_phase_result_detects_inequality() -> None:
    """Test PhaseResult detects inequality correctly."""

    result1 = PhaseResult(phase_name="specification")
    result2 = PhaseResult(phase_name="architecture")
    assert result1 != result2


def test_phase_result_prevents_field_modification() -> None:
    """Test PhaseResult prevents modification of fields after creation."""

    result = PhaseResult(phase_name="specification")

    with pytest.raises(AttributeError):
        result.phase_name = "architecture"


def test_session_context_accepts_session_id_field() -> None:
    """Test SessionContext accepts session_id field."""

    context = SessionContext(session_id="test-session", task="test")
    assert context.session_id == "test-session"


def test_session_context_accepts_task_field() -> None:
    """Test SessionContext accepts task field."""

    context = SessionContext(session_id="test", task="test task")
    assert context.task == "test task"


def test_session_context_stores_artifacts_when_provided() -> None:
    """Test SessionContext stores artifacts field when provided."""

    artifacts = {"spec": "requirement"}
    context = SessionContext(session_id="test", task="test", artifacts=artifacts)
    assert context.artifacts == artifacts


def test_session_context_defaults_artifacts_to_empty_dict() -> None:
    """Test SessionContext defaults artifacts to empty dict when not provided."""

    context = SessionContext(session_id="test", task="test")
    assert context.artifacts == {}


def test_session_context_stores_metadata_when_provided() -> None:
    """Test SessionContext stores metadata field when provided."""

    metadata = {"start_time": "2024-01-01"}
    context = SessionContext(session_id="test", task="test", metadata=metadata)
    assert context.metadata == metadata


def test_session_context_defaults_metadata_to_empty_dict() -> None:
    """Test SessionContext defaults metadata to empty dict when not provided."""

    context = SessionContext(session_id="test", task="test")
    assert context.metadata == {}


def test_session_context_supports_equality_comparison() -> None:
    """Test SessionContext supports equality comparison."""

    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task1")
    assert context1 == context2


def test_session_context_detects_inequality() -> None:
    """Test SessionContext detects inequality correctly."""

    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task2")
    assert context1 != context2


def test_session_context_prevents_field_modification() -> None:
    """Test SessionContext prevents modification of fields after creation."""

    context = SessionContext(session_id="test", task="test")

    with pytest.raises(AttributeError):
        context.session_id = "modified"


def test_phase_result_with_artifacts() -> None:
    """Test PhaseResult with artifacts information."""

    artifacts = {"document": "Test document content", "metadata": {"status": "complete"}}
    result = PhaseResult(phase_name="specification", artifacts=artifacts)
    assert result.artifacts == artifacts
    assert result.artifacts["document"] == "Test document content"


def test_phase_result_with_metadata_detailed() -> None:
    """Test PhaseResult with metadata."""

    metadata = {"duration": 1.5, "tokens_used": 150}
    result = PhaseResult(phase_name="specification", metadata=metadata)
    assert result.metadata == metadata
    assert result.metadata["duration"] == 1.5


def test_phase_result_optional_fields() -> None:
    """Test PhaseResult with optional fields."""

    result = PhaseResult(phase_name="specification")
    assert result.next_phase is None
    assert result.metadata == {}
    assert result.artifacts == {}


def test_phase_result_str_representation() -> None:
    """Test PhaseResult string representation."""

    result = PhaseResult(phase_name="specification", artifacts={"doc": "test output"})
    str_repr = str(result)
    assert "specification" in str_repr


def test_phase_result_equality() -> None:
    """Test PhaseResult equality comparison."""

    result1 = PhaseResult(phase_name="specification", artifacts={"doc": "test"})
    result2 = PhaseResult(phase_name="specification", artifacts={"doc": "test"})
    result3 = PhaseResult(phase_name="architecture", artifacts={"doc": "test"})

    assert result1 == result2
    assert result1 != result3


def test_phase_result_immutable() -> None:
    """Test that PhaseResult is immutable after creation."""

    result = PhaseResult(phase_name="specification")

    # Should raise AttributeError when trying to modify
    with pytest.raises(AttributeError):
        result.phase_name = "architecture"


def test_session_context_initialization() -> None:
    """Test SessionContext initialization with required fields."""

    context = SessionContext(session_id="test-session", task="test task")
    assert context.session_id == "test-session"
    assert context.task == "test task"


def test_session_context_with_artifacts() -> None:
    """Test SessionContext with artifacts storage."""

    artifacts = {"spec": "requirement doc", "code": "implementation"}
    context = SessionContext(session_id="test", task="test", artifacts=artifacts)
    assert context.artifacts == artifacts
    assert context.artifacts["spec"] == "requirement doc"


def test_session_context_with_metadata() -> None:
    """Test SessionContext with metadata."""

    metadata = {"start_time": "2024-01-01", "user": "test_user"}
    context = SessionContext(session_id="test", task="test", metadata=metadata)
    assert context.metadata == metadata
    assert context.metadata["user"] == "test_user"


def test_session_context_optional_fields() -> None:
    """Test SessionContext with optional fields."""

    context = SessionContext(session_id="test", task="test")
    assert context.artifacts == {}
    assert context.metadata == {}


def test_session_context_immutable() -> None:
    """Test that SessionContext is immutable after creation."""

    context = SessionContext(session_id="test", task="test")

    # Should raise AttributeError when trying to modify
    with pytest.raises(AttributeError):
        context.session_id = "modified"


def test_session_context_equality() -> None:
    """Test SessionContext equality comparison."""

    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task1")
    context3 = SessionContext(session_id="test", task="task2")

    assert context1 == context2
    assert context1 != context3
