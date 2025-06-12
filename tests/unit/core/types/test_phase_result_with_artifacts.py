"""Test PhaseResult with artifacts information.

This test validates that PhaseResult properly stores and provides access to
complex artifacts including nested dictionaries.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_with_artifacts() -> None:
    """Test PhaseResult with artifacts information."""
    artifacts = {"document": "Test document content", "metadata": {"status": "complete"}}
    result = PhaseResult(phase_name="specification", artifacts=artifacts)
    assert result.artifacts == artifacts
    assert result.artifacts["document"] == "Test document content"
