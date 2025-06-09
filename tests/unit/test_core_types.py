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


def test_phase_result_accepts_success_field():
    """Test PhaseResult accepts success field."""

    result = PhaseResult(success=True, output="test")
    assert result.success is True


def test_phase_result_accepts_output_field():
    """Test PhaseResult accepts output field."""

    result = PhaseResult(success=True, output="test output")
    assert result.output == "test output"


def test_phase_result_stores_error_when_provided():
    """Test PhaseResult stores error field when provided."""

    result = PhaseResult(success=False, output="", error="Test error")
    assert result.error == "Test error"


def test_phase_result_defaults_error_to_none():
    """Test PhaseResult defaults error to None when not provided."""

    result = PhaseResult(success=True, output="test")
    assert result.error is None


def test_phase_result_stores_metadata_when_provided():
    """Test PhaseResult stores metadata field when provided."""

    metadata = {"duration": 1.5}
    result = PhaseResult(success=True, output="test", metadata=metadata)
    assert result.metadata == metadata


def test_phase_result_defaults_metadata_to_empty_dict():
    """Test PhaseResult defaults metadata to empty dict when not provided."""

    result = PhaseResult(success=True, output="test")
    assert result.metadata == {}


def test_phase_result_provides_string_representation():
    """Test PhaseResult provides string representation."""

    result = PhaseResult(success=True, output="test")
    assert str(result) is not None
    assert len(str(result)) > 0


def test_phase_result_string_contains_success_status():
    """Test PhaseResult string representation contains success status."""

    result = PhaseResult(success=True, output="test")
    assert "success=True" in str(result)


def test_phase_result_supports_equality_comparison():
    """Test PhaseResult supports equality comparison."""

    result1 = PhaseResult(success=True, output="test")
    result2 = PhaseResult(success=True, output="test")
    assert result1 == result2


def test_phase_result_detects_inequality():
    """Test PhaseResult detects inequality correctly."""

    result1 = PhaseResult(success=True, output="test")
    result2 = PhaseResult(success=False, output="test")
    assert result1 != result2


def test_phase_result_prevents_field_modification():
    """Test PhaseResult prevents modification of fields after creation."""

    result = PhaseResult(success=True, output="test")

    with pytest.raises(AttributeError):
        result.success = False


def test_session_context_accepts_session_id_field():
    """Test SessionContext accepts session_id field."""

    context = SessionContext(session_id="test-session", task="test")
    assert context.session_id == "test-session"


def test_session_context_accepts_task_field():
    """Test SessionContext accepts task field."""

    context = SessionContext(session_id="test", task="test task")
    assert context.task == "test task"


def test_session_context_stores_artifacts_when_provided():
    """Test SessionContext stores artifacts field when provided."""

    artifacts = {"spec": "requirement"}
    context = SessionContext(session_id="test", task="test", artifacts=artifacts)
    assert context.artifacts == artifacts


def test_session_context_defaults_artifacts_to_empty_dict():
    """Test SessionContext defaults artifacts to empty dict when not provided."""

    context = SessionContext(session_id="test", task="test")
    assert context.artifacts == {}


def test_session_context_stores_metadata_when_provided():
    """Test SessionContext stores metadata field when provided."""

    metadata = {"start_time": "2024-01-01"}
    context = SessionContext(session_id="test", task="test", metadata=metadata)
    assert context.metadata == metadata


def test_session_context_defaults_metadata_to_empty_dict():
    """Test SessionContext defaults metadata to empty dict when not provided."""

    context = SessionContext(session_id="test", task="test")
    assert context.metadata == {}


def test_session_context_supports_equality_comparison():
    """Test SessionContext supports equality comparison."""

    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task1")
    assert context1 == context2


def test_session_context_detects_inequality():
    """Test SessionContext detects inequality correctly."""

    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task2")
    assert context1 != context2


def test_session_context_prevents_field_modification():
    """Test SessionContext prevents modification of fields after creation."""

    context = SessionContext(session_id="test", task="test")

    with pytest.raises(AttributeError):
        context.session_id = "modified"


def test_phase_result_with_error():
    """Test PhaseResult with error information."""

    result = PhaseResult(success=False, output="", error="Test error message")
    assert result.success is False
    assert not result.output
    assert result.error == "Test error message"


def test_phase_result_with_metadata():
    """Test PhaseResult with metadata."""

    metadata = {"duration": 1.5, "tokens_used": 150}
    result = PhaseResult(success=True, output="test", metadata=metadata)
    assert result.metadata == metadata
    assert result.metadata["duration"] == 1.5


def test_phase_result_optional_fields():
    """Test PhaseResult with optional fields."""

    result = PhaseResult(success=True, output="test")
    assert result.error is None
    assert result.metadata == {}


def test_phase_result_str_representation():
    """Test PhaseResult string representation."""

    result = PhaseResult(success=True, output="test output")
    str_repr = str(result)
    assert "success=True" in str_repr
    assert "test output" in str_repr


def test_phase_result_equality():
    """Test PhaseResult equality comparison."""

    result1 = PhaseResult(success=True, output="test")
    result2 = PhaseResult(success=True, output="test")
    result3 = PhaseResult(success=False, output="test")

    assert result1 == result2
    assert result1 != result3


def test_phase_result_immutable():
    """Test that PhaseResult is immutable after creation."""

    result = PhaseResult(success=True, output="test")

    # Should raise AttributeError when trying to modify
    with pytest.raises(AttributeError):
        result.success = False


def test_session_context_initialization():
    """Test SessionContext initialization with required fields."""

    context = SessionContext(session_id="test-session", task="test task")
    assert context.session_id == "test-session"
    assert context.task == "test task"


def test_session_context_with_artifacts():
    """Test SessionContext with artifacts storage."""

    artifacts = {"spec": "requirement doc", "code": "implementation"}
    context = SessionContext(session_id="test", task="test", artifacts=artifacts)
    assert context.artifacts == artifacts
    assert context.artifacts["spec"] == "requirement doc"


def test_session_context_with_metadata():
    """Test SessionContext with metadata."""

    metadata = {"start_time": "2024-01-01", "user": "test_user"}
    context = SessionContext(session_id="test", task="test", metadata=metadata)
    assert context.metadata == metadata
    assert context.metadata["user"] == "test_user"


def test_session_context_optional_fields():
    """Test SessionContext with optional fields."""

    context = SessionContext(session_id="test", task="test")
    assert context.artifacts == {}
    assert context.metadata == {}


def test_session_context_immutable():
    """Test that SessionContext is immutable after creation."""

    context = SessionContext(session_id="test", task="test")

    # Should raise AttributeError when trying to modify
    with pytest.raises(AttributeError):
        context.session_id = "modified"


def test_session_context_equality():
    """Test SessionContext equality comparison."""

    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task1")
    context3 = SessionContext(session_id="test", task="task2")

    assert context1 == context2
    assert context1 != context3
