"""Test that SPARCOrchestrator class can be instantiated with dependencies.

This test validates basic class structure and dependency injection following DIP.
Tests basic orchestrator instantiation with mock dependencies.
"""

from zenyth.orchestration import SPARCOrchestrator


def test_sparc_orchestrator_exists() -> None:
    """Test that SPARCOrchestrator class can be instantiated with dependencies."""
    # Mock dependencies - should be injected following DIP
    mock_llm = "mock_llm_provider"
    mock_tool_registry = "mock_tool_registry"
    mock_state_manager = "mock_state_manager"

    # This should fail - constructor should actually store dependencies
    orchestrator = SPARCOrchestrator(
        llm_provider=mock_llm,
        tool_registry=mock_tool_registry,
        state_manager=mock_state_manager,
    )

    # Should store all dependencies (will fail with current pass implementation)
    assert orchestrator.llm_provider == mock_llm
    assert orchestrator.tool_registry == mock_tool_registry
    assert orchestrator.state_manager == mock_state_manager
