"""Test orchestrator handles phase execution errors gracefully.

This test validates error handling and graceful degradation.
Tests that workflow failures are properly reported.
"""

import pytest
from tests.fixtures.orchestration_mocks import (
    MockLLMProvider,
    MockStateManager,
    MockToolRegistry,
    TestPhaseHandler,
)

from zenyth.core.types import SPARCPhase, WorkflowResult
from zenyth.orchestration.orchestrator import SPARCOrchestrator
from zenyth.orchestration.registry import PhaseHandlerRegistry


@pytest.mark.asyncio()
async def test_orchestration_integration_error_handling() -> None:
    """Test orchestrator handles phase execution errors gracefully."""
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with failing handler
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))
    registry.register(
        SPARCPhase.ARCHITECTURE,
        lambda: TestPhaseHandler("architecture", should_fail=True),
    )

    orchestrator.set_phase_registry(registry)

    result = await orchestrator.execute("Test error handling")

    # Should return failed WorkflowResult
    assert isinstance(result, WorkflowResult)
    assert result.success is False
    assert result.error is not None
    assert "architecture phase failed" in result.error.lower()

    # Should contain phases that completed before failure
    assert len(result.phases_completed) == 1
    assert result.phases_completed[0].phase_name == "specification"
