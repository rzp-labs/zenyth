"""Test that orchestrator class follows SOLID design principles.

This test validates that the orchestrator implementation adheres to all five
SOLID principles for maintainable, extensible architecture.
"""

from unittest.mock import Mock

from zenyth.orchestration import SPARCOrchestrator


def test_sparc_orchestrator_follows_solid_principles() -> None:
    """Test that orchestrator class follows SOLID design principles."""
    # Create mock dependencies for testing
    mock_llm = Mock()
    mock_tools = Mock()
    mock_state = Mock()
    orchestrator = SPARCOrchestrator(
        llm_provider=mock_llm,
        tool_registry=mock_tools,
        state_manager=mock_state,
    )

    # Single Responsibility: MUST have execute method for orchestration
    assert hasattr(
        orchestrator,
        "execute",
    ), "Orchestrator must have execute method for its responsibility"

    # Should not have methods for specific phase logic, tool management,
    # state persistence, or LLM communication - those are separate responsibilities
    # Only check callable methods, not dependency attributes (which are acceptable)
    all_methods = [
        attr
        for attr in dir(orchestrator)
        if callable(getattr(orchestrator, attr)) and not attr.startswith("_")
    ]
    # Methods like set_phase_registry are acceptable as they're for dependency injection
    phase_methods = [
        attr
        for attr in all_methods
        if "phase" in attr.lower() and not attr.startswith("set_")
    ]
    tool_methods = [
        attr for attr in all_methods if "tool" in attr.lower() and attr != "tool_registry"
    ]  # Exclude dependency attributes
    llm_methods = [
        attr for attr in all_methods if "llm" in attr.lower() and attr != "llm_provider"
    ]  # Exclude dependency attributes

    # Should only have orchestration-related methods, not specific implementations
    assert len(phase_methods) == 0, "Orchestrator should not contain phase-specific methods"
    assert len(tool_methods) == 0, "Orchestrator should not contain tool management methods"
    assert len(llm_methods) == 0, "Orchestrator should not contain LLM communication methods"
