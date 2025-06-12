"""Test suite for SpecificationHandler phase implementation.

Tests the concrete implementation of specification phase following
SOLID principles and PhaseHandler contract compliance.
"""

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.phases.base import PhaseHandler
from zenyth.phases.specification import SpecificationHandler


def test_specification_handler_inherits_from_phase_handler() -> None:
    """Test that SpecificationHandler properly inherits from PhaseHandler.

    Validates Liskov Substitution Principle - concrete implementation
    must be substitutable for base class contract.
    """
    # SpecificationHandler should inherit from PhaseHandler
    assert issubclass(SpecificationHandler, PhaseHandler)
    assert PhaseHandler in SpecificationHandler.__mro__


def test_specification_handler_is_instantiable() -> None:
    """Test that SpecificationHandler can be instantiated.

    Validates proper concrete implementation following
    Open/Closed Principle - extension without modification.
    """
    # Should be able to create instance without error
    handler = SpecificationHandler()
    assert isinstance(handler, SpecificationHandler)
    assert isinstance(handler, PhaseHandler)


async def test_specification_handler_execute_returns_phase_result() -> None:
    """Test that execute method returns proper PhaseResult.

    Validates interface contract compliance and return type
    following Liskov Substitution Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session",
        task_description="Create user authentication system",
        previous_phases=[],
        global_artifacts={},
    )

    # Execute should return PhaseResult
    result = await handler.execute(context)
    assert isinstance(result, PhaseResult)
    assert result.phase_name == SPARCPhase.SPECIFICATION.value


async def test_specification_handler_execute_with_task_context() -> None:
    """Test execute method with realistic task context.

    Validates Single Responsibility Principle - focused on
    specification phase logic only.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="spec-test-session",
        task_description="Build REST API for user management",
        previous_phases=[],
        global_artifacts={"project_type": "web_api"},
    )

    result = await handler.execute(context)

    # Should produce specification artifacts
    assert result.phase_name == SPARCPhase.SPECIFICATION.value
    assert isinstance(result.artifacts, dict)
    assert isinstance(result.metadata, dict)


def test_specification_handler_validate_prerequisites_with_valid_context() -> None:
    """Test prerequisite validation with valid context.

    Validates proper validation logic following
    Single Responsibility Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session",
        task_description="Implement user authentication",
        previous_phases=[],
        global_artifacts={},
    )

    # Should validate successfully with task description
    result = handler.validate_prerequisites(context)
    assert result is True


def test_specification_handler_validate_prerequisites_with_empty_task() -> None:
    """Test prerequisite validation fails with empty task.

    Validates proper error handling and validation logic
    following Dependency Inversion Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session", task_description="", previous_phases=[], global_artifacts={}
    )

    # Should fail validation with empty task description
    result = handler.validate_prerequisites(context)
    assert result is False


def test_specification_handler_validate_prerequisites_with_none_task() -> None:
    """Test prerequisite validation fails with None task.

    Validates robust validation following defensive programming
    and Dependency Inversion Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session", task_description=None, previous_phases=[], global_artifacts={}
    )

    # Should fail validation with None task description
    result = handler.validate_prerequisites(context)
    assert result is False


async def test_specification_handler_execute_preserves_session_id() -> None:
    """Test that execute preserves session context.

    Validates context preservation following state management
    best practices and Interface Segregation Principle.
    """
    handler = SpecificationHandler()
    session_id = "preserve-session-test"
    context = PhaseContext(
        session_id=session_id,
        task_description="Test session preservation",
        previous_phases=[],
        global_artifacts={},
    )

    result = await handler.execute(context)

    # Should preserve session context in metadata
    assert "session_id" in result.metadata
    assert result.metadata["session_id"] == session_id
