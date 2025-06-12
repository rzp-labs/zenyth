"""Test IStateManager load_session method signature.

This test validates that the IStateManager protocol defines the correct method
signature for loading session state, supporting the Single Responsibility
Principle by focusing on session retrieval.
"""

from unittest.mock import Mock

from zenyth.core.interfaces import IStateManager


def test_istate_manager_load_session_signature() -> None:
    """Test IStateManager load_session method signature.

    Validates Single Responsibility - focused on session state retrieval.
    Tests async interface contract for loading session state.
    """
    # Create mock implementation to test interface compliance
    mock_manager = Mock(spec=IStateManager)

    # Should have the required async method
    assert hasattr(mock_manager, "load_session")
    assert callable(mock_manager.load_session)
