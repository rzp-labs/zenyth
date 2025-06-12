"""Test PhaseResult supports equality comparison.

This test validates that PhaseResult instances with the same field values
are considered equal using the == operator.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_supports_equality_comparison() -> None:
    """Test PhaseResult supports equality comparison."""
    result1 = PhaseResult(phase_name="specification")
    result2 = PhaseResult(phase_name="specification")
    assert result1 == result2
