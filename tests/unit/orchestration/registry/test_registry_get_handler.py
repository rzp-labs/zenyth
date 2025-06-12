"""Test retrieving registered phase handler.

This test validates Dependency Inversion - registry depends on PhaseHandler abstraction.
Tests that retrieved handlers implement the PhaseHandler contract.
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


def test_phase_handler_registry_get_handler() -> None:
    """Test retrieving registered phase handler."""
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)

    # Should be able to get registered handler
    handler = registry.get_handler(SPARCPhase.SPECIFICATION)

    # Should return instance of registered handler class
    assert handler is not None
    assert isinstance(handler, PhaseHandler)
    assert isinstance(handler, MockPhaseHandler)
