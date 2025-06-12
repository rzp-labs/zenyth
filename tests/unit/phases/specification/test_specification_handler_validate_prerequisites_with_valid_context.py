"""Test prerequisite validation with valid context.

This test validates proper validation logic following
Single Responsibility Principle.
"""

from zenyth.core.types import PhaseContext
from zenyth.phases.specification import SpecificationHandler


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
