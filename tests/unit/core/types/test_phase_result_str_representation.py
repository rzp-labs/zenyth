"""Test PhaseResult string representation.

This test validates that PhaseResult's string representation includes
the phase name when artifacts are present.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_str_representation() -> None:
    """Test PhaseResult string representation."""
    result = PhaseResult(phase_name="specification", artifacts={"doc": "test output"})
    str_repr = str(result)
    assert "specification" in str_repr
