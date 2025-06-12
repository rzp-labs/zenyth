"""Test PhaseResult detects inequality correctly.

This test validates that PhaseResult instances with different field values
are correctly identified as not equal using the != operator.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_detects_inequality() -> None:
    """Test PhaseResult detects inequality correctly."""
    result1 = PhaseResult(phase_name="specification")
    result2 = PhaseResult(phase_name="architecture")
    assert result1 != result2
