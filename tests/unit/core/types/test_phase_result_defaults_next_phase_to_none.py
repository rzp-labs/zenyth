"""Test PhaseResult defaults next_phase to None when not provided.

This test validates that PhaseResult properly defaults the optional next_phase
field to None when not explicitly provided during initialization.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_defaults_next_phase_to_none() -> None:
    """Test PhaseResult defaults next_phase to None when not provided."""
    result = PhaseResult(phase_name="specification")
    assert result.next_phase is None
