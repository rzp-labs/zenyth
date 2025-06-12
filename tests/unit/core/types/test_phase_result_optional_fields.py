"""Test PhaseResult with optional fields.

This test validates that PhaseResult properly defaults all optional fields
when only the required phase_name is provided.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_optional_fields() -> None:
    """Test PhaseResult with optional fields."""
    result = PhaseResult(phase_name="specification")
    assert result.next_phase is None
    assert result.metadata == {}
    assert result.artifacts == {}
