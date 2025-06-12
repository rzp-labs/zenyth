"""Test that validate_prerequisites has correct signature.

This test validates interface contract for prerequisite validation
following Dependency Inversion Principle.
"""

from typing import Dict, Any
from zenyth.core.types import PhaseContext, PhaseResult
from zenyth.phases.base import PhaseHandler


class ValidationHandler(PhaseHandler):
    """Test handler with instance-based validation rules."""
    
    def __init__(self, validation_rules: Dict[str, Any]) -> None:
        self.validation_rules = validation_rules

    async def execute(self, context: PhaseContext) -> PhaseResult:
        # Use instance state to determine phase name
        phase_name = f"test-{len(self.validation_rules)}"
        return PhaseResult(
            phase_name=phase_name,
            artifacts={},
            next_phase=None,
            metadata={},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        return all(
            getattr(context, field, None) == expected
            for field, expected in self.validation_rules.items()
        )


def test_phase_handler_validate_prerequisites_signature() -> None:
    """Test that validate_prerequisites has correct signature."""
    handler = ValidationHandler({"session_id": "test-session"})
    context = PhaseContext(
        session_id="test-session",
        task_description="test task",
        previous_phases=[],
        global_artifacts={},
    )

    # Should return boolean
    result = handler.validate_prerequisites(context)
    assert isinstance(result, bool)
