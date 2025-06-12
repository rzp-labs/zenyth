"""Test that PhaseHandler properly inherits from ABC.

This test validates proper abstract base class setup following
Open/Closed Principle for extensibility.
"""

from abc import ABC

from zenyth.phases.base import PhaseHandler


def test_phase_handler_inheritance() -> None:
    """Test that PhaseHandler properly inherits from ABC."""
    # PhaseHandler should inherit from ABC
    assert issubclass(PhaseHandler, ABC)
    assert ABC in PhaseHandler.__mro__
