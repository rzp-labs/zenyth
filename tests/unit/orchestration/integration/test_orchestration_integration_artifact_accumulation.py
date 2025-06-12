"""Test orchestrator accumulates artifacts across phases.

This test validates artifact management and workflow state preservation.
Tests that artifacts from each phase are preserved in final result.
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
async def test_orchestration_integration_artifact_accumulation() -> None:
    """Test orchestrator accumulates artifacts across phases."""
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with test handlers that produce different artifacts
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))
    registry.register(SPARCPhase.ARCHITECTURE, lambda: TestPhaseHandler("architecture"))

    orchestrator.set_phase_registry(registry)

    result = await orchestrator.execute("Test artifact accumulation")

    # Final result should contain artifacts from all phases
    assert "specification_artifact" in result.artifacts
    assert "architecture_artifact" in result.artifacts
    assert result.artifacts["specification_artifact"] == "Result from specification"
    assert result.artifacts["architecture_artifact"] == "Result from architecture"
