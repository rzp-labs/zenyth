"""Test orchestrator execution with phase handler registry.

This test validates Open/Closed Principle - orchestrator extensible via registry.
Tests integration between orchestrator and phase registry.
"""

import pytest
from tests.fixtures.orchestration_mocks import TestPhaseHandler

from zenyth.core.types import SPARCPhase, WorkflowResult
from zenyth.orchestration.registry import PhaseHandlerRegistry


@pytest.mark.asyncio()
async def test_orchestration_integration_execute_with_phase_registry(orchestrator_with_mocks):
    """Test orchestrator execution with phase handler registry."""
    # Set up phase registry with test handlers
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, TestPhaseHandler, "specification")
    registry.register(SPARCPhase.ARCHITECTURE, TestPhaseHandler, "architecture")

    # Set the phase registry using the public setter method
    orchestrator_with_mocks.set_phase_registry(registry)

    result = await orchestrator_with_mocks.execute("Build authentication system")

    # Should have executed phases via registry
    assert isinstance(result, WorkflowResult)
    assert result.task == "Build authentication system"
