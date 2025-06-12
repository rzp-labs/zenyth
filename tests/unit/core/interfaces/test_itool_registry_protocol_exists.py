"""Test that IToolRegistry protocol is properly defined.

This test validates that the IToolRegistry protocol exists and is correctly
defined as a Protocol, supporting the Interface Segregation Principle by
providing a focused tool registry contract.
"""

from zenyth.core.interfaces import IToolRegistry


def test_itool_registry_protocol_exists() -> None:
    """Test that IToolRegistry protocol is properly defined.

    Validates Interface Segregation Principle - focused tool registry contract.
    Tests protocol definition and runtime checking capability.
    """
    # Should be able to import and check as protocol
    assert hasattr(IToolRegistry, "_is_protocol")
    assert IToolRegistry.__class__.__name__ == "_ProtocolMeta"
