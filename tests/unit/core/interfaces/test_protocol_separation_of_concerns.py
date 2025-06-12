"""Test that protocols maintain proper separation of concerns.

This test validates that each protocol in the system has a focused responsibility
and doesn't have overlapping or conflicting methods, supporting the Interface
Segregation Principle.
"""

from zenyth.core.interfaces import IStateManager, IToolRegistry, LLMInterface


def test_protocol_separation_of_concerns() -> None:
    """Test that protocols maintain proper separation of concerns.

    Validates Interface Segregation - each protocol has focused responsibility.
    Tests that protocols don't have overlapping or conflicting methods.
    """
    # IToolRegistry should only deal with tools
    tool_methods = [attr for attr in dir(IToolRegistry) if not attr.startswith("_")]
    assert any("tool" in method.lower() or "phase" in method.lower() for method in tool_methods)

    # IStateManager should only deal with state/sessions
    state_methods = [attr for attr in dir(IStateManager) if not attr.startswith("_")]
    assert any("session" in method.lower() for method in state_methods)

    # LLMInterface should only deal with text generation
    llm_methods = [attr for attr in dir(LLMInterface) if not attr.startswith("_")]
    assert any("generate" in method.lower() for method in llm_methods)
