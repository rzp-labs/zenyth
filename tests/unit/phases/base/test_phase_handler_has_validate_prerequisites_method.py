"""Test that PhaseHandler defines validate_prerequisites method.

This test validates Single Responsibility Principle - separate validation
logic from execution logic.
"""

from zenyth.phases.base import PhaseHandler


def test_phase_handler_has_validate_prerequisites_method() -> None:
    """Test that PhaseHandler defines validate_prerequisites method."""
    # PhaseHandler should define validate_prerequisites as abstract method
    assert hasattr(PhaseHandler, "validate_prerequisites")
    assert hasattr(PhaseHandler.validate_prerequisites, "__isabstractmethod__")
    assert PhaseHandler.validate_prerequisites.__isabstractmethod__ is True
