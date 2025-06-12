"""Test PhaseResult equality comparison.

This test validates that PhaseResult equality comparison works correctly
for instances with the same and different field values.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_equality() -> None:
    """Test PhaseResult equality comparison."""
    result1 = PhaseResult(phase_name="specification", artifacts={"doc": "test"})
    result2 = PhaseResult(phase_name="specification", artifacts={"doc": "test"})
    result3 = PhaseResult(phase_name="architecture", artifacts={"doc": "test"})

    assert result1 == result2
    assert result1 != result3
