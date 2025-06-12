"""Test that PhaseResult is immutable after creation.

This test validates that PhaseResult enforces immutability by raising
AttributeError when attempting to modify any field after initialization.
"""

import pytest

from zenyth.core.types import PhaseResult


def test_phase_result_immutable() -> None:
    """Test that PhaseResult is immutable after creation."""
    result = PhaseResult(phase_name="specification")

    # Should raise AttributeError when trying to modify
    with pytest.raises(AttributeError):
        result.phase_name = "architecture"
