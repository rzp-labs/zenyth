"""Test that PhaseHandler is an abstract base class.

This test validates Open/Closed Principle - base class is closed for modification
but open for extension through concrete implementations.
"""

import pytest

from zenyth.phases.base import PhaseHandler


def test_phase_handler_is_abstract() -> None:
    """Test that PhaseHandler is an abstract base class."""
    # PhaseHandler should be abstract and not instantiable
    with pytest.raises(TypeError):
        PhaseHandler()
