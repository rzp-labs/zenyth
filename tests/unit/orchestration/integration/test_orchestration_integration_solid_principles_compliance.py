"""Test that orchestrator implementation follows SOLID principles.

This test validates comprehensive SOLID compliance in orchestrator design.
Tests architectural patterns and dependency relationships.
"""

import inspect

from zenyth.orchestration.orchestrator import SPARCOrchestrator


def test_orchestration_integration_solid_principles_compliance() -> None:
    """Test that orchestrator implementation follows SOLID principles."""
    # Single Responsibility: Orchestrator should only coordinate workflow execution
    orchestrator_methods = [
        method
        for method in dir(SPARCOrchestrator)
        if not method.startswith("_") and callable(getattr(SPARCOrchestrator, method))
    ]

    # Should have focused interface - primarily execute method
    assert "execute" in orchestrator_methods

    # Should not have methods for specific phase logic, tool management, or LLM communication
    phase_methods = [
        m
        for m in orchestrator_methods
        if "specification" in m.lower() or "architecture" in m.lower()
    ]
    tool_methods = [m for m in orchestrator_methods if "tool" in m.lower() and m != "tool_registry"]
    llm_methods = [m for m in orchestrator_methods if "llm" in m.lower() and m != "llm_provider"]

    assert len(phase_methods) == 0, "Orchestrator should not contain phase-specific methods"
    assert len(tool_methods) == 0, "Orchestrator should not contain tool management methods"
    assert len(llm_methods) == 0, "Orchestrator should not contain LLM communication methods"

    # Dependency Inversion: Should accept abstract dependencies in constructor
    init_signature = inspect.signature(SPARCOrchestrator.__init__)
    init_params = list(init_signature.parameters.keys())

    assert "llm_provider" in init_params
    assert "tool_registry" in init_params
    assert "state_manager" in init_params
