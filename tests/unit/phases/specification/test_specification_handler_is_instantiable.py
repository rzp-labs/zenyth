"""Test that SpecificationHandler can be instantiated.

This test validates proper concrete implementation following
Open/Closed Principle - extension without modification.
"""

from zenyth.phases.base import PhaseHandler
from zenyth.phases.specification import SpecificationHandler


def test_specification_handler_is_instantiable() -> None:
    """Test that SpecificationHandler can be instantiated.

    Validates proper concrete implementation following
    Open/Closed Principle - extension without modification.
    """
    # Should be able to create instance without error
    handler = SpecificationHandler()
    assert isinstance(handler, SpecificationHandler)
    assert isinstance(handler, PhaseHandler)
