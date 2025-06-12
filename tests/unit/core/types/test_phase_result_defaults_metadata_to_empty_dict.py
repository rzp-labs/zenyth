"""Test PhaseResult defaults metadata to empty dict when not provided.

This test validates that PhaseResult properly defaults the optional metadata
field to an empty dictionary when not explicitly provided during initialization.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_defaults_metadata_to_empty_dict() -> None:
    """Test PhaseResult defaults metadata to empty dict when not provided."""
    result = PhaseResult(phase_name="specification")
    assert result.metadata == {}
