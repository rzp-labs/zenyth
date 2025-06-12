"""Test that list_phases returns consistent results.

This test validates Interface Segregation - focused query interface.
Tests registry state consistency and proper enumeration.
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


def test_phase_handler_registry_list_phases_consistency() -> None:
    """Test that list_phases returns consistent results."""
    registry = PhaseHandlerRegistry()

    # Initially empty
    assert len(registry.list_phases()) == 0

    # Add phases and verify listing
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)
    phases = registry.list_phases()
    assert len(phases) == 1
    assert SPARCPhase.SPECIFICATION in phases

    registry.register(SPARCPhase.ARCHITECTURE, AnotherMockHandler)
    phases = registry.list_phases()
    assert len(phases) == 2
    assert SPARCPhase.SPECIFICATION in phases
    assert SPARCPhase.ARCHITECTURE in phases

    # Order should be consistent
    phases1 = registry.list_phases()
    phases2 = registry.list_phases()
    assert phases1 == phases2
