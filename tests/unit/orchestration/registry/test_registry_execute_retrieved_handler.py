"""Test executing handler retrieved from registry.

This test validates complete integration between registry and handler execution.
Tests that registry provides fully functional handler instances.
"""

import pytest

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


@pytest.mark.asyncio()
async def test_phase_handler_registry_execute_retrieved_handler() -> None:
    """Test executing handler retrieved from registry."""
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler, "spec_test")

    # Get handler and create test context
    handler = registry.get_handler(SPARCPhase.SPECIFICATION)
    context = PhaseContext(
        session_id="registry-test-123",
        task_description="Test registry handler execution",
        previous_phases=[],
        global_artifacts={},
    )

    # Should be able to validate prerequisites
    assert handler.validate_prerequisites(context) is True

    # Should be able to execute handler
    result = await handler.execute(context)
    assert isinstance(result, PhaseResult)
    assert result.phase_name == "spec_test"
    assert "spec_test_output" in result.artifacts
    assert result.metadata["handler_type"] == "mock"
