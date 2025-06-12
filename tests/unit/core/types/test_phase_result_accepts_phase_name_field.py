"""Test PhaseResult accepts phase_name field.

This test validates that PhaseResult properly accepts and stores the phase_name
field, which is a required field for phase result tracking.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_accepts_phase_name_field() -> None:
    """Test PhaseResult accepts phase_name field."""
    result = PhaseResult(phase_name="specification")
    assert result.phase_name == "specification"
