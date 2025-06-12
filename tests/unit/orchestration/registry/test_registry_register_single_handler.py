"""Test registering a single phase handler.

This test validates Open/Closed Principle - registry open for extension via registration.
Tests basic registration functionality with SPARCPhase enum.
"""

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.orchestration.registry import PhaseHandlerRegistry
from zenyth.phases.base import PhaseHandler


class MockPhaseHandler(PhaseHandler):
    """Mock phase handler for testing registry functionality."""

    def __init__(self, phase_name: str):
        self.phase_name = phase_name
        self.execute_called = False
        self.validate_called = False
        self.call_count = 0

    async def execute(self, context: PhaseContext) -> PhaseResult:
        self.execute_called = True
        return PhaseResult(
            phase_name=self.phase_name,
            artifacts={f"{self.phase_name}_output": f"test_result_{self.call_count}"},
            metadata={"handler_type": "mock", "call_count": self.call_count},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        self.validate_called = True
        self.call_count += 1
        return context.task_description is not None


def test_phase_handler_registry_register_single_handler() -> None:
    """Test registering a single phase handler."""
    registry = PhaseHandlerRegistry()
    handler_class = MockPhaseHandler

    # Should be able to register handler
    registry.register(SPARCPhase.SPECIFICATION, handler_class)

    # Should be able to list registered phases
    phases = registry.list_phases()
    assert SPARCPhase.SPECIFICATION in phases
    assert len(phases) == 1
