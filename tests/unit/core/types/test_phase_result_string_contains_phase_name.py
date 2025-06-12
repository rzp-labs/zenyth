"""Test PhaseResult string representation contains phase name.

This test validates that PhaseResult's string representation includes
the phase name for debugging and logging purposes.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_string_contains_phase_name() -> None:
    """Test PhaseResult string representation contains phase name."""
    result = PhaseResult(phase_name="specification")
    assert "specification" in str(result)
