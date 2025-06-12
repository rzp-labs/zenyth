"""Test that PhaseHandler defines execute method contract.

This test validates Interface Segregation Principle - focused interface
for phase execution responsibility only.
"""

from zenyth.phases.base import PhaseHandler


def test_phase_handler_has_execute_method() -> None:
    """Test that PhaseHandler defines execute method contract."""
    # PhaseHandler should define execute as abstract method
    assert hasattr(PhaseHandler, "execute")
    assert hasattr(PhaseHandler.execute, "__isabstractmethod__")
    assert PhaseHandler.execute.__isabstractmethod__ is True
