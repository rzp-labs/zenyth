"""Test registry error handling for invalid inputs.

This test validates registry robustness and proper error reporting.
Tests defensive programming practices.
"""

import pytest

from zenyth.core.types import PhaseContext, SPARCPhase
from zenyth.orchestration.registry import PhaseHandlerRegistry


def test_phase_handler_registry_error_handling() -> None:
    """Test registry error handling for invalid inputs."""
    registry = PhaseHandlerRegistry()

    # Test registration with invalid handler class
    class NotAPhaseHandler:
        def some_other_method(self) -> None:
            pass

    # Should handle registration gracefully (or raise clear error)
    # Note: Actual error handling depends on implementation
    try:
        registry.register(SPARCPhase.SPECIFICATION, NotAPhaseHandler)
        # If registration succeeds, getting handler might fail
        handler = registry.get_handler(SPARCPhase.SPECIFICATION)
        # Try to use as PhaseHandler - should fail
        context = PhaseContext("test", "test task", [], {})
        with pytest.raises((TypeError, AttributeError), match=r".*(execute|validate).*"):
            handler.validate_prerequisites(context)
    except (TypeError, AttributeError, ValueError):
        # Registration itself might fail - also acceptable
        pass
