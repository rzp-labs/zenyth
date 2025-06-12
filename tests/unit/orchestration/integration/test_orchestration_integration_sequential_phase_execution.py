"""Test orchestrator executes phases sequentially with context passing.

This test validates workflow coordination and context preservation between phases.
Tests that phase results are properly passed to subsequent phases.
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
async def test_orchestration_integration_sequential_phase_execution() -> None:
    """Test orchestrator executes phases sequentially with context passing."""
    # Create orchestrator with real phase registry
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with multiple phases
    registry = PhaseHandlerRegistry()
    spec_handler = TestPhaseHandler("specification")
    arch_handler = TestPhaseHandler("architecture")
    comp_handler = TestPhaseHandler("completion")

    registry.register(SPARCPhase.SPECIFICATION, lambda: spec_handler)
    registry.register(SPARCPhase.ARCHITECTURE, lambda: arch_handler)
    registry.register(SPARCPhase.COMPLETION, lambda: comp_handler)

    orchestrator.set_phase_registry(registry)

    # Execute workflow
    result = await orchestrator.execute("Multi-phase workflow test")

    # Should return valid WorkflowResult
    assert isinstance(result, WorkflowResult)
    assert result.task == "Multi-phase workflow test"

    # All handlers should have been called
    assert spec_handler.execute_called
    assert arch_handler.execute_called
    assert comp_handler.execute_called

    # Context should have been passed between phases
    assert spec_handler.context_received is not None
    assert arch_handler.context_received is not None
    assert comp_handler.context_received is not None

    # Later phases should see artifacts from earlier phases
    assert len(arch_handler.context_received.global_artifacts) > 0
    assert len(comp_handler.context_received.global_artifacts) >= 2
