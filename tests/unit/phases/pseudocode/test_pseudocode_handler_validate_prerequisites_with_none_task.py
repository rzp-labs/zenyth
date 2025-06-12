"""Test prerequisite validation with None task description.

This test validates that handler correctly handles null input by raising exception.

SOLID Assessment:
- SRP: Test focused solely on null task validation
- LSP: Consistent validation behavior across all handlers
"""

import pytest

from zenyth.core.exceptions import ValidationError
from zenyth.core.types import PhaseContext
from zenyth.phases.pseudocode import PseudocodeHandler


def test_pseudocode_handler_validate_prerequisites_with_none_task() -> None:
    """Test prerequisite validation with None task description.

    Validates that handler correctly handles null input by raising exception.

    SOLID Assessment:
    - SRP: Test focused solely on null task validation
    - LSP: Consistent validation behavior across all handlers
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="none-task-session",
        task_description=None,
        previous_phases=[],
        global_artifacts={},
    )

    # Should raise ValidationError with None task
    with pytest.raises(ValidationError, match="Task description required"):
        handler.validate_prerequisites(context)
