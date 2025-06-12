"""Test that retrieved handlers comply with PhaseHandler contract.

This test validates Liskov Substitution - all handlers are substitutable.
Tests that registry ensures contract compliance.
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


def test_phase_handler_registry_handler_contract_compliance() -> None:
    """Test that retrieved handlers comply with PhaseHandler contract."""
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)

    handler = registry.get_handler(SPARCPhase.SPECIFICATION)

    # Should have required PhaseHandler methods
    assert hasattr(handler, "execute")
    assert hasattr(handler, "validate_prerequisites")
    assert callable(handler.execute)
    assert callable(handler.validate_prerequisites)
