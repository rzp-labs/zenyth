"""Test suite for PhaseHandler base class.

Tests the abstract base class contract that all phase implementations must follow.
Following Interface Segregation Principle with focused, testable interfaces.
"""

from abc import ABC

import pytest

from zenyth.core.types import PhaseContext, PhaseResult
from zenyth.phases.base import PhaseHandler


def test_phase_handler_is_abstract() -> None:
    """Test that PhaseHandler is an abstract base class.

    Validates Open/Closed Principle - base class is closed for modification
    but open for extension through concrete implementations.
    """
    # PhaseHandler should be abstract and not instantiable
    with pytest.raises(TypeError):
        PhaseHandler()


def test_phase_handler_has_execute_method() -> None:
    """Test that PhaseHandler defines execute method contract.

    Validates Interface Segregation Principle - focused interface
    for phase execution responsibility only.
    """
    # PhaseHandler should define execute as abstract method
    assert hasattr(PhaseHandler, "execute")
    assert hasattr(PhaseHandler.execute, "__isabstractmethod__")
    assert PhaseHandler.execute.__isabstractmethod__ is True


def test_phase_handler_has_validate_prerequisites_method() -> None:
    """Test that PhaseHandler defines validate_prerequisites method.

    Validates Single Responsibility Principle - separate validation
    logic from execution logic.
    """
    # PhaseHandler should define validate_prerequisites as abstract method
    assert hasattr(PhaseHandler, "validate_prerequisites")
    assert hasattr(PhaseHandler.validate_prerequisites, "__isabstractmethod__")
    assert PhaseHandler.validate_prerequisites.__isabstractmethod__ is True


async def test_phase_handler_execute_signature() -> None:
    """Test that execute method has correct async signature.

    Validates Liskov Substitution Principle - all implementations
    must honor this exact signature contract.
    """

    # Create a minimal test handler using lambda-like approach
    def create_test_handler():
        class ConcreteHandler(PhaseHandler):
            def __init__(self, result_phase: str = "test"):
                self.result_phase = result_phase

            async def execute(self, context: PhaseContext) -> PhaseResult:
                return PhaseResult(
                    phase_name=self.result_phase, artifacts={}, next_phase=None, metadata={}
                )

            def validate_prerequisites(self, context: PhaseContext) -> bool:
                return len(context.session_id) > 0 and self.result_phase is not None

        return ConcreteHandler()

    handler = create_test_handler()
    context = PhaseContext(
        session_id="test-session",
        task_description="test task",
        previous_phases=[],
        global_artifacts={},
    )

    # Should return PhaseResult
    result = await handler.execute(context)
    assert isinstance(result, PhaseResult)


def test_phase_handler_validate_prerequisites_signature() -> None:
    """Test that validate_prerequisites has correct signature.

    Validates interface contract for prerequisite validation
    following Dependency Inversion Principle.
    """

    # Create a test handler with meaningful instance state
    def create_validation_handler():
        class ValidationHandler(PhaseHandler):
            def __init__(self, validation_rules: dict):
                self.validation_rules = validation_rules

            async def execute(self, context: PhaseContext) -> PhaseResult:
                # Use instance state to determine phase name
                phase_name = f"test-{len(self.validation_rules)}"
                return PhaseResult(
                    phase_name=phase_name, artifacts={}, next_phase=None, metadata={}
                )

            def validate_prerequisites(self, context: PhaseContext) -> bool:
                return all(
                    getattr(context, field, None) == expected
                    for field, expected in self.validation_rules.items()
                )

        return ValidationHandler({"session_id": "test-session"})

    handler = create_validation_handler()
    context = PhaseContext(
        session_id="test-session",
        task_description="test task",
        previous_phases=[],
        global_artifacts={},
    )

    # Should return boolean
    result = handler.validate_prerequisites(context)
    assert isinstance(result, bool)


def test_phase_handler_inheritance() -> None:
    """Test that PhaseHandler properly inherits from ABC.

    Validates proper abstract base class setup following
    Open/Closed Principle for extensibility.
    """
    # PhaseHandler should inherit from ABC
    assert issubclass(PhaseHandler, ABC)
    assert ABC in PhaseHandler.__mro__
