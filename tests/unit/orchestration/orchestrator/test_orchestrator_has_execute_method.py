"""Test that SPARCOrchestrator has async execute method with correct signature.

This test validates the main orchestration interface following Single Responsibility
Principle - orchestrator's sole responsibility is workflow execution.
"""

import inspect
from unittest.mock import Mock

from zenyth.orchestration import SPARCOrchestrator


def test_sparc_orchestrator_has_execute_method() -> None:
    """Test that SPARCOrchestrator has async execute method with correct signature."""
    # Create mock dependencies for testing
    mock_llm = Mock()
    mock_tools = Mock()
    mock_state = Mock()
    orchestrator = SPARCOrchestrator(
        llm_provider=mock_llm,
        tool_registry=mock_tools,
        state_manager=mock_state,
    )

    # Should have async execute method that accepts task and returns result
    assert hasattr(orchestrator, "execute")
    assert callable(orchestrator.execute)

    # Method should be async (coroutine)
    assert inspect.iscoroutinefunction(orchestrator.execute)
