"""Test orchestrator validates required dependencies are provided.

This test validates defensive programming and clear error reporting.
Tests that missing dependencies are detected early.
"""

import pytest

from zenyth.orchestration.orchestrator import SPARCOrchestrator


def test_orchestration_integration_validate_dependencies() -> None:
    """Test orchestrator validates required dependencies are provided."""
    # Should reject None dependencies
    with pytest.raises(ValueError, match=r".*dependencies.*"):
        SPARCOrchestrator(None, None, None)
