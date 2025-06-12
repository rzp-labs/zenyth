"""Test PhaseResult accepts artifacts field.

This test validates that PhaseResult properly accepts and stores the artifacts
field, which contains phase execution outputs.
"""

from zenyth.core.types import PhaseResult


def test_phase_result_accepts_artifacts_field() -> None:
    """Test PhaseResult accepts artifacts field."""
    artifacts = {"document": "test output"}
    result = PhaseResult(phase_name="specification", artifacts=artifacts)
    assert result.artifacts == artifacts
