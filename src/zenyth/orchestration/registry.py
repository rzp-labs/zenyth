"""Phase Handler Registry for SPARC Orchestration System.

Provides phase handler registration and retrieval following SOLID principles
for extensible orchestration architecture.
"""

from typing import Any

from zenyth.core.types import SPARCPhase
from zenyth.phases.base import PhaseHandler


class HandlerNotRegisteredError(ValueError):
    """Raised when no handler is registered for a requested phase."""

    def __init__(self, phase: SPARCPhase) -> None:
        """Initialize with the missing phase."""
        self.phase = phase
        super().__init__(f"No handler registered for phase: {phase}")


class PhaseHandlerRegistry:
    """Registry for managing phase handler implementations.

    Implements Open/Closed Principle - open for extension via registration,
    closed for modification of core registry logic.
    """

    def __init__(self) -> None:
        """Initialize empty phase handler registry."""
        self._handlers: dict[SPARCPhase, tuple[Any, str]] = {}

    def register(
        self,
        phase: SPARCPhase,
        handler_class: type[PhaseHandler] | Any,
        name: str = "",
    ) -> None:
        """Register a phase handler for given phase.

        Args:
            phase: SPARC phase enum value
            handler_class: PhaseHandler implementation class or callable factory
            name: Optional name for the handler
        """
        self._handlers[phase] = (handler_class, name)

    def get_handler(self, phase: SPARCPhase) -> PhaseHandler:
        """Get handler instance for given phase.

        Supports three explicit handler types with clear instantiation patterns:

        1. **Factory Functions**: Callable that returns handler instance
           - Example: `lambda: TestPhaseHandler("spec")`
           - Use case: Pre-configured test handlers

        2. **Named Constructor Handlers**: Classes requiring phase name
           - Example: `MockPhaseHandler`, `TestPhaseHandler`
           - Constructor signature: `__init__(self, phase_name: str, ...)`

        3. **Standard Phase Handlers**: Classes with no-args or optional args
           - Example: `SpecificationHandler`, `ArchitectureHandler`
           - Constructor signature: `__init__(self, optional_strategies=None)`

        SOLID Principles Alignment:
            - Single Responsibility: Focused solely on handler instantiation
            - Open/Closed: Closed for modification, extensible via registration
            - Liskov Substitution: Returns handlers honoring PhaseHandler contract
            - Interface Segregation: Minimal focused interface for handler creation
            - Dependency Inversion: Returns abstractions, not concrete implementations

        Args:
            phase: SPARC phase enum value

        Returns:
            PhaseHandler instance for the phase

        Raises:
            ValueError: If no handler registered for phase or instantiation fails
        """
        if phase not in self._handlers:
            raise HandlerNotRegisteredError(phase)

        handler_class, name = self._handlers[phase]

        # Pattern 1: Factory Function (lambda or callable returning handler)
        if callable(handler_class) and not hasattr(handler_class, "__bases__"):
            try:
                return handler_class()  # type: ignore[no-any-return]
            except Exception as e:
                msg = f"Factory function failed for phase {phase}: {e}"
                raise ValueError(msg) from e

        # Pattern 2: Named Constructor Handler (requires phase name parameter)
        if name:
            try:
                return handler_class(name)  # type: ignore[no-any-return]
            except Exception as e:
                msg = f"Named constructor failed for phase {phase} with name '{name}': {e}"
                raise ValueError(msg) from e

        # Pattern 3: Standard Phase Handler (no-args or optional dependencies)
        # First try with phase value for backward compatibility with MockPhaseHandler
        try:
            return handler_class(phase.value)  # type: ignore[no-any-return]
        except Exception:
            # If phase value fails, try no-args constructor
            try:
                return handler_class()  # type: ignore[no-any-return]
            except Exception as e:
                msg = f"Standard constructor failed for phase {phase}: {e}. "
                msg += "Ensure handler has no-args constructor or register with factory function."
                raise ValueError(msg) from e

    def list_phases(self) -> list[SPARCPhase]:
        """List all registered phases.

        Returns:
            List of registered SPARCPhase values
        """
        return list(self._handlers.keys())
