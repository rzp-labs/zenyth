"""Test that PseudocodeHandler properly inherits from PhaseHandler.

This test validates Liskov Substitution Principle - concrete implementation
must be substitutable for base class contract.

SOLID Assessment:
- LSP: PseudocodeHandler must honor PhaseHandler contract exactly
- SRP: Test has single responsibility - inheritance validation
"""

from zenyth.phases.base import PhaseHandler
from zenyth.phases.pseudocode import PseudocodeHandler


def test_pseudocode_handler_inherits_from_phase_handler() -> None:
    """Test that PseudocodeHandler properly inherits from PhaseHandler.

    Validates Liskov Substitution Principle - concrete implementation
    must be substitutable for base class contract.

    SOLID Assessment:
    - LSP: PseudocodeHandler must honor PhaseHandler contract exactly
    - SRP: Test has single responsibility - inheritance validation
    """
    # PseudocodeHandler should inherit from PhaseHandler
    assert issubclass(PseudocodeHandler, PhaseHandler)
    assert PhaseHandler in PseudocodeHandler.__mro__
