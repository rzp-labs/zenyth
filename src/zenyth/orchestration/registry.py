"""Phase Handler Registry for SPARC Orchestration System.

Provides phase handler registration and retrieval following SOLID principles
for extensible orchestration architecture.
"""

from typing import Any

from zenyth.core.types import SPARCPhase
from zenyth.phases.base import PhaseHandler


class PhaseHandlerRegistry:
    """Registry for managing phase handler implementations.

    Implements Open/Closed Principle - open for extension via registration,
    closed for modification of core registry logic.
    """

    def __init__(self) -> None:
        """Initialize empty phase handler registry."""
        self._handlers: dict[SPARCPhase, tuple[Any, str]] = {}

    def register(
        self, phase: SPARCPhase, handler_class: type[PhaseHandler] | Any, name: str = ""
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
            ValueError: If no handler registered for phase
        """
        if phase not in self._handlers:
            raise ValueError(f"No handler registered for phase: {phase}")  # noqa: TRY003

        handler_class, name = self._handlers[phase]

        # Handle callable factories (lambda functions) vs direct class references
        if callable(handler_class) and not hasattr(handler_class, "__bases__"):
            # This is a lambda factory function - call it directly
            return handler_class()  # type: ignore[no-any-return]

        # This is a class - try different instantiation strategies
        try:
            # Try instantiation with name if provided (for MockPhaseHandler compatibility)
            if name:
                return handler_class(name)  # type: ignore[no-any-return]
            # Try with phase value for MockPhaseHandler compatibility
            return handler_class(phase.value)  # type: ignore[no-any-return]
        except TypeError:
            # Fallback to no-args instantiation (for standard PhaseHandler subclasses)
            try:
                return handler_class()  # type: ignore[no-any-return]
            except TypeError as e:
                msg = f"Cannot instantiate handler for phase {phase}: {e}"
                raise ValueError(msg) from e

    def list_phases(self) -> list[SPARCPhase]:
        """List all registered phases.

        Returns:
            List of registered SPARCPhase values
        """
        return list(self._handlers.keys())
