"""Test IToolRegistry get_for_phase method signature.

This test validates that the IToolRegistry protocol defines the correct method
signature for retrieving tools based on the current SPARC phase, supporting
the Single Responsibility Principle.
"""

from unittest.mock import Mock

from zenyth.core.interfaces import IToolRegistry
from zenyth.core.types import SPARCPhase


def test_itool_registry_get_for_phase_signature() -> None:
    """Test IToolRegistry get_for_phase method signature.

    Validates Single Responsibility - focused on providing tools for phases.
    Tests interface contract definition for tool retrieval.
    """
    # Create mock implementation to test interface compliance
    mock_registry = Mock(spec=IToolRegistry)
    mock_registry.get_for_phase.return_value = ["tool1", "tool2"]

    # Should have the required method
    assert hasattr(mock_registry, "get_for_phase")
    assert callable(mock_registry.get_for_phase)

    # Test method call with SPARCPhase
    tools = mock_registry.get_for_phase(SPARCPhase.SPECIFICATION)
    assert tools == ["tool1", "tool2"]

    # Verify call was made with correct argument
    mock_registry.get_for_phase.assert_called_once_with(SPARCPhase.SPECIFICATION)
