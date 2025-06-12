"""Test that orchestrator properly stores injected dependencies.

This test validates Dependency Inversion Principle implementation - high-level
orchestration logic depends on abstractions, not concretions.
"""

from zenyth.orchestration import SPARCOrchestrator


def test_sparc_orchestrator_dependency_injection() -> None:
    """Test that orchestrator properly stores injected dependencies."""
    mock_llm = "mock_llm_provider"
    mock_tools = "mock_tool_registry"
    mock_state = "mock_state_manager"

    orchestrator = SPARCOrchestrator(
        llm_provider=mock_llm,
        tool_registry=mock_tools,
        state_manager=mock_state,
    )

    # Should store dependencies for use in orchestration
    assert orchestrator.llm_provider == mock_llm
    assert orchestrator.tool_registry == mock_tools
    assert orchestrator.state_manager == mock_state
