"""Test orchestrator validates phase prerequisites before execution.

This test validates fail-fast approach and prerequisite checking.
Tests that invalid contexts are rejected before expensive operations.
"""

import pytest
from tests.fixtures.orchestration_mocks import (
    MockLLMProvider,
    MockStateManager,
    MockToolRegistry,
    TestPhaseHandler,
)

from zenyth.core.types import SPARCPhase
from zenyth.orchestration.orchestrator import SPARCOrchestrator
from zenyth.orchestration.registry import PhaseHandlerRegistry


@pytest.mark.asyncio()
async def test_orchestration_integration_prerequisite_validation() -> None:
    """Test orchestrator validates phase prerequisites before execution."""
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with handler that validates prerequisites
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))

    orchestrator.set_phase_registry(registry)

    # Test with invalid task (empty string)
    result = await orchestrator.execute("")

    # Should fail due to prerequisite validation
    assert result.success is False
    assert result.error is not None
    assert "prerequisite" in result.error.lower() or "validation" in result.error.lower()
