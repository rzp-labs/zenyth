"""Test PhaseHandlerRegistry instantiation.

This test validates Single Responsibility - registry creation without side effects.
Tests basic registry initialization and empty state.
"""

from zenyth.orchestration.registry import PhaseHandlerRegistry


def test_phase_handler_registry_creation() -> None:
    """Test PhaseHandlerRegistry instantiation."""
    registry = PhaseHandlerRegistry()

    # Should be created successfully
    assert registry is not None
    assert isinstance(registry, PhaseHandlerRegistry)

    # Should start with empty registry
    phases = registry.list_phases()
    assert isinstance(phases, list)
    assert len(phases) == 0
