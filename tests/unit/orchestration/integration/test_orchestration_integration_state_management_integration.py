"""Test orchestrator integrates with state manager for session persistence.

This test validates state management integration and session handling.
Tests that workflow state is properly saved and retrievable.
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
async def test_orchestration_integration_state_management_integration() -> None:
    """Test orchestrator integrates with state manager for session persistence."""
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up minimal registry
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))

    orchestrator.set_phase_registry(registry)

    result = await orchestrator.execute("Test state management")

    # Should return valid WorkflowResult
    assert isinstance(result, WorkflowResult)
    assert result.task == "Test state management"

    # State manager should have been called to save session
    assert len(state_manager.save_calls) > 0

    # Should be able to retrieve saved session
    session_id = state_manager.save_calls[0]
    saved_session = await state_manager.load_session(session_id)
    assert saved_session is not None
    assert saved_session.task == "Test state management"
