"""Test PhaseResult with metadata.

This test validates that PhaseResult properly stores metadata with multiple
fields and provides access to individual metadata values.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_with_metadata_detailed() -> None:
    """Test PhaseResult with metadata."""
    metadata = {"duration": 1.5, "tokens_used": 150}
    result = PhaseResult(phase_name="specification", metadata=metadata)
    assert result.metadata == metadata
    assert result.metadata["duration"] == 1.5
