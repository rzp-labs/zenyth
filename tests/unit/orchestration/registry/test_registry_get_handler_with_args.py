"""Test retrieving handler that requires constructor arguments.

This test validates registry can handle handlers with initialization parameters.
Tests dependency injection pattern through registry.
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


def test_phase_handler_registry_get_handler_with_args() -> None:
    """Test retrieving handler that requires constructor arguments."""
    registry = PhaseHandlerRegistry()

    # Register handler class that takes constructor args
    registry.register(SPARCPhase.ARCHITECTURE, MockPhaseHandler, "architecture")

    # Should be able to get handler with args
    handler = registry.get_handler(SPARCPhase.ARCHITECTURE)
    assert handler is not None
    assert handler.phase_name == "architecture"
