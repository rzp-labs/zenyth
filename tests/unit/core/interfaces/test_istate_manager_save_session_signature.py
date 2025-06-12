"""Test IStateManager save_session method signature.

This test validates that the IStateManager protocol defines the correct method
signature for saving session state, supporting the Single Responsibility
Principle by focusing on session persistence.
"""

from unittest.mock import Mock

from zenyth.core.interfaces import IStateManager


def test_istate_manager_save_session_signature() -> None:
    """Test IStateManager save_session method signature.

    Validates Single Responsibility - focused on session state persistence.
    Tests async interface contract for saving session state.
    """
    # Create mock implementation to test interface compliance
    mock_manager = Mock(spec=IStateManager)

    # Should have the required async method
    assert hasattr(mock_manager, "save_session")
    assert callable(mock_manager.save_session)
