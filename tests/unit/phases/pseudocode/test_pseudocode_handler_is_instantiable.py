"""Test that PseudocodeHandler can be instantiated.

This test validates proper concrete implementation following
Open/Closed Principle - extension without modification.

SOLID Assessment:
- OCP: Handler instantiable without modifying base class
- SRP: Test focused solely on instantiation validation
"""

from zenyth.phases.base import PhaseHandler
from zenyth.phases.pseudocode import PseudocodeHandler


def test_pseudocode_handler_is_instantiable() -> None:
    """Test that PseudocodeHandler can be instantiated.

    Validates proper concrete implementation following
    Open/Closed Principle - extension without modification.

    SOLID Assessment:
    - OCP: Handler instantiable without modifying base class
    - SRP: Test focused solely on instantiation validation
    """
    # Should be able to create instance without error
    handler = PseudocodeHandler()
    assert isinstance(handler, PseudocodeHandler)
    assert isinstance(handler, PhaseHandler)
