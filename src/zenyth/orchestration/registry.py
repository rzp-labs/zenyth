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
        """
        Initializes an empty registry for phase handlers.
        """
        self._handlers: dict[SPARCPhase, tuple[Any, str]] = {}

    def register(
        self, phase: SPARCPhase, handler_class: type[PhaseHandler] | Any, name: str = ""
    ) -> None:
        """
        Registers a handler implementation or factory for a specific orchestration phase.
        
        Args:
            phase: The SPARCPhase enum value representing the orchestration phase.
            handler_class: The PhaseHandler subclass or a callable factory that produces a PhaseHandler instance.
            name: An optional name to associate with the handler.
        """
        self._handlers[phase] = (handler_class, name)

    def get_handler(self, phase: SPARCPhase) -> PhaseHandler:
        """
        Retrieves an instance of the handler registered for the specified SPARC phase.
        
        Attempts to instantiate the handler using a registered factory function, with a provided name, with the phase value, or with no arguments, in that order. Raises a ValueError if no handler is registered or if instantiation fails.
        
        Args:
            phase: The SPARCPhase enum value for which to retrieve the handler.
        
        Returns:
            An instance of PhaseHandler associated with the given phase.
        
        Raises:
            ValueError: If no handler is registered for the phase or if instantiation fails.
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
        """
        Returns a list of all phases that have registered handlers.
        
        Returns:
            A list of SPARCPhase values for which handlers are registered.
        """
        return list(self._handlers.keys())
