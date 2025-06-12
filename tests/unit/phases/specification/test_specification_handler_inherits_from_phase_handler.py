"""Test that SpecificationHandler properly inherits from PhaseHandler.

This test validates Liskov Substitution Principle - concrete implementation
must be substitutable for base class contract.
"""

from zenyth.phases.base import PhaseHandler
from zenyth.phases.specification import SpecificationHandler


def test_specification_handler_inherits_from_phase_handler() -> None:
    """Test that SpecificationHandler properly inherits from PhaseHandler.

    Validates Liskov Substitution Principle - concrete implementation
    must be substitutable for base class contract.
    """
    # SpecificationHandler should inherit from PhaseHandler
    assert issubclass(SpecificationHandler, PhaseHandler)
    assert PhaseHandler in SpecificationHandler.__mro__
