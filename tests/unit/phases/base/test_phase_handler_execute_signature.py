"""Test that execute method has correct async signature.

This test validates Liskov Substitution Principle - all implementations
must honor this exact signature contract.
"""

import pytest

from zenyth.core.types import PhaseContext, PhaseResult
from zenyth.phases.base import PhaseHandler


class ConcreteHandler(PhaseHandler):
    """Test handler for signature validation."""

    def __init__(self, result_phase: str = "test") -> None:
        self.result_phase = result_phase

    async def execute(self, context: PhaseContext) -> PhaseResult:
        return PhaseResult(
            phase_name=self.result_phase,
            artifacts={},
            next_phase=None,
            metadata={},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        return len(context.session_id) > 0 and self.result_phase is not None


@pytest.mark.asyncio()
async def test_phase_handler_execute_signature() -> None:
    """Test that execute method has correct async signature."""
    handler = ConcreteHandler()
    context = PhaseContext(
        session_id="test-session",
        task_description="test task",
        previous_phases=[],
        global_artifacts={},
    )

    # Should return PhaseResult
    result = await handler.execute(context)
    assert isinstance(result, PhaseResult)
