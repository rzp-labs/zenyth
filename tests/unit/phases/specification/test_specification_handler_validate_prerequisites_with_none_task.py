"""Test prerequisite validation fails with None task.

This test validates robust validation following defensive programming
and Dependency Inversion Principle.
"""

from zenyth.core.types import PhaseContext
from zenyth.phases.specification import SpecificationHandler


def test_specification_handler_validate_prerequisites_with_none_task() -> None:
    """Test prerequisite validation fails with None task.

    Validates robust validation following defensive programming
    and Dependency Inversion Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session",
        task_description=None,
        previous_phases=[],
        global_artifacts={},
    )

    # Should fail validation with None task description
    result = handler.validate_prerequisites(context)
    assert result is False
