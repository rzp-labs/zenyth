"""Test PhaseResult prevents modification of fields after creation.

This test validates that PhaseResult is immutable (frozen dataclass) and
raises AttributeError when attempting to modify fields after initialization.
"""

import pytest

from zenyth.core.types import PhaseResult


def test_phase_result_prevents_field_modification() -> None:
    """Test PhaseResult prevents modification of fields after creation."""
    result = PhaseResult(phase_name="specification")

    with pytest.raises(AttributeError):
        result.phase_name = "architecture"
