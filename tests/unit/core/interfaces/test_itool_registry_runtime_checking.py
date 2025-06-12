"""Test IToolRegistry runtime protocol checking.

This test validates that the IToolRegistry protocol correctly performs runtime
type checking, ensuring that implementations honor the protocol contract in
accordance with the Liskov Substitution Principle.
"""

from typing import Any

from zenyth.core.interfaces import IToolRegistry
from zenyth.core.types import SPARCPhase


def test_itool_registry_runtime_checking() -> None:
    """Test IToolRegistry runtime protocol checking.

    Validates Liskov Substitution - implementations must honor protocol contract.
    Tests that incorrect implementations are rejected at runtime.
    """

    # Create correct implementation with instance state
    class ValidToolRegistry:
        def __init__(self) -> None:
            self.tool_cache = {"default": ["tool1", "tool2"]}

        def get_for_phase(self, phase: SPARCPhase) -> list[Any]:
            return self.tool_cache.get("default", [])

    # Create incorrect implementation (missing method)
    class InvalidToolRegistry:
        def wrong_method(self) -> None:
            pass

    valid_registry = ValidToolRegistry()
    invalid_registry = InvalidToolRegistry()

    # Runtime checking should work correctly
    assert isinstance(valid_registry, IToolRegistry)
    assert not isinstance(invalid_registry, IToolRegistry)
