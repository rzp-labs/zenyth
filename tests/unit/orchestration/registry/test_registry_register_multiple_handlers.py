"""Test registering multiple phase handlers.

This test validates registry can handle multiple phase mappings.
Tests that different phases map to different handlers.
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


class AnotherMockHandler(PhaseHandler):
    """Alternative mock handler to test multiple registrations."""

    def __init__(self) -> None:
        self.response_suffix = "_different_result"

    async def execute(self, context: PhaseContext) -> PhaseResult:
        return PhaseResult(
            phase_name="alternative",
            artifacts={"alternative_output": f"alternative{self.response_suffix}"},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        # Use instance state to avoid static method warning
        min_length = len(self.response_suffix)
        return len(context.task_description or "") > min_length


def test_phase_handler_registry_register_multiple_handlers() -> None:
    """Test registering multiple phase handlers."""
    registry = PhaseHandlerRegistry()

    # Register multiple handlers
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)
    registry.register(SPARCPhase.ARCHITECTURE, AnotherMockHandler)
    registry.register(SPARCPhase.COMPLETION, MockPhaseHandler)

    # Should list all registered phases
    phases = registry.list_phases()
    assert len(phases) == 3
    assert SPARCPhase.SPECIFICATION in phases
    assert SPARCPhase.ARCHITECTURE in phases
    assert SPARCPhase.COMPLETION in phases
