"""Test orchestrator properly stores injected dependencies.

This test validates Dependency Inversion Principle - orchestrator depends on abstractions.
Tests that constructor properly stores all required dependencies.
"""

from zenyth.orchestration.orchestrator import SPARCOrchestrator


def test_orchestration_integration_dependency_injection(mock_dependencies):
    """Test orchestrator properly stores injected dependencies."""
    llm_provider, tool_registry, state_manager = mock_dependencies

    orchestrator = SPARCOrchestrator(
        llm_provider=llm_provider,
        tool_registry=tool_registry,
        state_manager=state_manager,
    )

    # Should store all injected dependencies
    assert orchestrator.llm_provider == llm_provider
    assert orchestrator.tool_registry == tool_registry
    assert orchestrator.state_manager == state_manager
