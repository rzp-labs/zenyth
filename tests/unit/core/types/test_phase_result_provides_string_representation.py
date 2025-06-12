"""Test PhaseResult provides string representation.

This test validates that PhaseResult provides a valid string representation
when converted to string, ensuring it's not None and has content.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_provides_string_representation() -> None:
    """Test PhaseResult provides string representation."""
    result = PhaseResult(phase_name="specification")
    assert str(result) is not None
    assert len(str(result)) > 0
