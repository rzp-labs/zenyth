"""Test prerequisite validation with valid context.

This test validates that handler correctly accepts valid input without raising exception.

SOLID Assessment:
- SRP: Validation focused solely on prerequisite checking
- LSP: Must implement validation contract from PhaseHandler
"""

from zenyth.core.types import PhaseContext
from zenyth.phases.pseudocode import PseudocodeHandler


def test_pseudocode_handler_validate_prerequisites_with_valid_context() -> None:
    """Test prerequisite validation with valid context.

    Validates that handler correctly accepts valid input without raising exception.

    SOLID Assessment:
    - SRP: Validation focused solely on prerequisite checking
    - LSP: Must implement validation contract from PhaseHandler
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="valid-session",
        task_description="Implement authentication system",
        previous_phases=[],
        global_artifacts={},
    )

    # Should validate successfully and return True
    result = handler.validate_prerequisites(context)
    assert result is True
