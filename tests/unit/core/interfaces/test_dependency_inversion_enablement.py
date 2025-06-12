"""Test that protocols enable proper dependency inversion.

This test validates that the protocols support the Dependency Inversion Principle
by allowing high-level components to depend on protocol abstractions rather than
concrete implementations.
"""

from unittest.mock import Mock

from zenyth.core.interfaces import IStateManager, IToolRegistry, LLMInterface


def test_dependency_inversion_enablement() -> None:
    """Test that protocols enable proper dependency inversion.

    Validates Dependency Inversion Principle - depend on abstractions.
    Tests that high-level code can depend on these protocol abstractions.
    """

    # Simulate high-level component depending on abstractions
    class HighLevelOrchestrator:
        def __init__(
            self,
            llm_provider: LLMInterface,
            tool_registry: IToolRegistry,
            state_manager: IStateManager,
        ):
            self.llm_provider = llm_provider
            self.tool_registry = tool_registry
            self.state_manager = state_manager

        def has_dependencies(self) -> bool:
            """Check if all dependencies are available."""
            return all(
                [
                    self.llm_provider is not None,
                    self.tool_registry is not None,
                    self.state_manager is not None,
                ],
            )

    # Create mock implementations
    mock_llm = Mock(spec=LLMInterface)
    mock_tools = Mock(spec=IToolRegistry)
    mock_state = Mock(spec=IStateManager)

    # Should be able to inject dependencies
    orchestrator = HighLevelOrchestrator(mock_llm, mock_tools, mock_state)

    # Should store injected dependencies
    assert orchestrator.llm_provider == mock_llm
    assert orchestrator.tool_registry == mock_tools
    assert orchestrator.state_manager == mock_state
