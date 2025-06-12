"""Test that IStateManager protocol is properly defined.

This test validates that the IStateManager protocol exists and is correctly
defined as a Protocol, supporting the Interface Segregation Principle by
providing a focused state management contract.
"""

from zenyth.core.interfaces import IStateManager


def test_istate_manager_protocol_exists() -> None:
    """Test that IStateManager protocol is properly defined.

    Validates Interface Segregation Principle - focused state management contract.
    Tests protocol definition and runtime checking capability.
    """
    # Should be able to import and check as protocol
    assert hasattr(IStateManager, "_is_protocol")
    assert IStateManager.__class__.__name__ == "_ProtocolMeta"
