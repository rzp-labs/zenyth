"""Test prerequisite validation with empty task description.

This test validates that handler correctly rejects invalid input by raising exception.

SOLID Assessment:
- SRP: Test focused solely on empty task validation
- DIP: Validation logic independent of concrete implementations
"""

import pytest

from zenyth.core.exceptions import ValidationError
from zenyth.core.types import PhaseContext
from zenyth.phases.pseudocode import PseudocodeHandler


def test_pseudocode_handler_validate_prerequisites_with_empty_task() -> None:
    """Test prerequisite validation with empty task description.

    Validates that handler correctly rejects invalid input by raising exception.

    SOLID Assessment:
    - SRP: Test focused solely on empty task validation
    - DIP: Validation logic independent of concrete implementations
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="empty-task-session",
        task_description="",
        previous_phases=[],
        global_artifacts={},
    )

    # Should raise ValidationError with empty task
    with pytest.raises(ValidationError, match="Task description empty"):
        handler.validate_prerequisites(context)
