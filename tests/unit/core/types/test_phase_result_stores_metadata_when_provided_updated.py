"""Test PhaseResult stores metadata field when provided (updated version).

This test validates that PhaseResult properly accepts and stores metadata
with a single field when provided during initialization.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_stores_metadata_when_provided_updated() -> None:
    """Test PhaseResult stores metadata field when provided."""
    metadata = {"duration": 1.5}
    result = PhaseResult(phase_name="specification", metadata=metadata)
    assert result.metadata == metadata
