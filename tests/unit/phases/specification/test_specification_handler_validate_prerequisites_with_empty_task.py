"""Test prerequisite validation fails with empty task.

This test validates proper error handling and validation logic
following Dependency Inversion Principle.
"""

from zenyth.core.types import PhaseContext
from zenyth.phases.specification import SpecificationHandler


def test_specification_handler_validate_prerequisites_with_empty_task() -> None:
    """Test prerequisite validation fails with empty task.

    Validates proper error handling and validation logic
    following Dependency Inversion Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session",
        task_description="",
        previous_phases=[],
        global_artifacts={},
    )

    # Should fail validation with empty task description
    result = handler.validate_prerequisites(context)
    assert result is False
