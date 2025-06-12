"""Test retrieving handler for unregistered phase.

This test validates proper error handling for missing phase mappings.
Tests registry robustness and clear error reporting.
"""

import pytest

from zenyth.core.types import SPARCPhase
from zenyth.orchestration.registry import PhaseHandlerRegistry


def test_phase_handler_registry_get_unregistered_handler() -> None:
    """Test retrieving handler for unregistered phase."""
    registry = PhaseHandlerRegistry()

    # Should raise appropriate error for unregistered phase
    with pytest.raises(ValueError, match="No handler registered for phase"):
        registry.get_handler(SPARCPhase.SPECIFICATION)
