"""Test suite for PhaseHandlerRegistry implementation.

Tests the registry pattern for mapping SPARC phases to handler implementations,
validating plugin architecture and SOLID principles compliance.

SOLID Principles Alignment:
    - Single Responsibility: Registry solely manages phase-to-handler mapping
    - Open/Closed: Closed for modification, open for extension via registration
    - Liskov Substitution: All registered handlers must honor PhaseHandler contract
    - Interface Segregation: Focused registry interface without unrelated methods
    - Dependency Inversion: Registry depends on PhaseHandler abstraction
"""

import pytest

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.orchestration.registry import PhaseHandlerRegistry
from zenyth.phases.base import PhaseHandler


class MockPhaseHandler(PhaseHandler):
    """Mock phase handler for testing registry functionality.

    Follows Liskov Substitution Principle by honoring PhaseHandler contract.
    """

    def __init__(self, phase_name: str):
        """
        Initializes a MockPhaseHandler with a given phase name.
        
        Args:
            phase_name: The name of the phase this handler is associated with.
        """
        self.phase_name = phase_name
        self.execute_called = False
        self.validate_called = False
        self.call_count = 0

    async def execute(self, context: PhaseContext) -> PhaseResult:
        """
        Executes the mock phase handler and returns a PhaseResult with test artifacts and metadata.
        
        Args:
            context: The phase execution context.
        
        Returns:
            A PhaseResult containing mock artifacts and metadata, including the handler type and call count.
        """
        self.execute_called = True
        return PhaseResult(
            phase_name=self.phase_name,
            artifacts={f"{self.phase_name}_output": f"test_result_{self.call_count}"},
            metadata={"handler_type": "mock", "call_count": self.call_count},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        """
        Checks if the phase prerequisites are met based on the provided context.
        
        Returns True if the context's task description is not None; otherwise, returns False.
        """
        self.validate_called = True
        self.call_count += 1
        return context.task_description is not None


class AnotherMockHandler(PhaseHandler):
    """Alternative mock handler to test multiple registrations.

    Validates that different handlers can be registered and retrieved.
    """

    def __init__(self) -> None:
        """
        Initializes the handler with a predefined response suffix for result differentiation.
        """
        self.response_suffix = "_different_result"

    async def execute(self, context: PhaseContext) -> PhaseResult:
        """
        Executes the handler for the "alternative" phase and returns the result.
        
        Args:
            context: The phase execution context.
        
        Returns:
            A PhaseResult containing artifacts with an alternative output string.
        """
        return PhaseResult(
            phase_name="alternative",
            artifacts={"alternative_output": f"alternative{self.response_suffix}"},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        # Use instance state to avoid static method warning
        """
        Checks if the task description length exceeds the required minimum.
        
        Returns:
            True if the length of the task description is greater than the length of the handler's response suffix; otherwise, False.
        """
        min_length = len(self.response_suffix)
        return len(context.task_description or "") > min_length


def test_phase_handler_registry_creation() -> None:
    """
    Tests that a PhaseHandlerRegistry can be instantiated and is initially empty.
    
    Asserts that the registry is created successfully and contains no registered phases upon initialization.
    """
    registry = PhaseHandlerRegistry()

    # Should be created successfully
    assert registry is not None
    assert isinstance(registry, PhaseHandlerRegistry)

    # Should start with empty registry
    phases = registry.list_phases()
    assert isinstance(phases, list)
    assert len(phases) == 0


def test_phase_handler_registry_register_single_handler() -> None:
    """
    Tests that a single handler can be registered for a SPARC phase and is listed correctly.
    
    Ensures the registry supports extension by allowing new handler registrations.
    """
    registry = PhaseHandlerRegistry()
    handler_class = MockPhaseHandler

    # Should be able to register handler
    registry.register(SPARCPhase.SPECIFICATION, handler_class)

    # Should be able to list registered phases
    phases = registry.list_phases()
    assert SPARCPhase.SPECIFICATION in phases
    assert len(phases) == 1


def test_phase_handler_registry_register_multiple_handlers() -> None:
    """Test registering multiple phase handlers.

    Validates registry can handle multiple phase mappings.
    Tests that different phases map to different handlers.
    """
    registry = PhaseHandlerRegistry()

    # Register multiple handlers
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)
    registry.register(SPARCPhase.ARCHITECTURE, AnotherMockHandler)
    registry.register(SPARCPhase.COMPLETION, MockPhaseHandler)

    # Should list all registered phases
    phases = registry.list_phases()
    assert len(phases) == 3
    assert SPARCPhase.SPECIFICATION in phases
    assert SPARCPhase.ARCHITECTURE in phases
    assert SPARCPhase.COMPLETION in phases


def test_phase_handler_registry_get_handler() -> None:
    """
    Tests retrieval of a registered phase handler from the registry.
    
    Asserts that the returned handler is an instance of both the registered class and the PhaseHandler interface.
    """
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)

    # Should be able to get registered handler
    handler = registry.get_handler(SPARCPhase.SPECIFICATION)

    # Should return instance of registered handler class
    assert handler is not None
    assert isinstance(handler, PhaseHandler)
    assert isinstance(handler, MockPhaseHandler)


def test_phase_handler_registry_get_handler_with_args() -> None:
    """
    Tests that the registry can retrieve a handler requiring constructor arguments.
    
    Ensures that handlers registered with initialization parameters are correctly instantiated and returned by the registry.
    """
    registry = PhaseHandlerRegistry()

    # Register handler class that takes constructor args
    registry.register(SPARCPhase.ARCHITECTURE, MockPhaseHandler, "architecture")

    # Should be able to get handler with args
    handler = registry.get_handler(SPARCPhase.ARCHITECTURE)
    assert handler is not None
    assert handler.phase_name == "architecture"


def test_phase_handler_registry_get_unregistered_handler() -> None:
    """
    Tests that retrieving a handler for an unregistered phase raises a ValueError.
    
    Ensures the registry provides clear error reporting when a handler has not been registered for a requested phase.
    """
    registry = PhaseHandlerRegistry()

    # Should raise appropriate error for unregistered phase
    with pytest.raises(ValueError, match="No handler registered for phase"):
        registry.get_handler(SPARCPhase.SPECIFICATION)


def test_phase_handler_registry_overwrite_registration() -> None:
    """Test overwriting existing phase registration.

    Validates registry handles registration updates correctly.
    Tests that later registrations replace earlier ones.
    """
    registry = PhaseHandlerRegistry()

    # Register initial handler
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)
    initial_handler = registry.get_handler(SPARCPhase.SPECIFICATION)
    assert isinstance(initial_handler, MockPhaseHandler)

    # Register different handler for same phase
    registry.register(SPARCPhase.SPECIFICATION, AnotherMockHandler)
    new_handler = registry.get_handler(SPARCPhase.SPECIFICATION)
    assert isinstance(new_handler, AnotherMockHandler)
    assert not isinstance(new_handler, MockPhaseHandler)


def test_phase_handler_registry_handler_contract_compliance() -> None:
    """
    Verifies that handlers retrieved from the registry implement the required PhaseHandler interface methods.
    
    Asserts that each handler provides callable `execute` and `validate_prerequisites` methods, ensuring contract compliance.
    """
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)

    handler = registry.get_handler(SPARCPhase.SPECIFICATION)

    # Should have required PhaseHandler methods
    assert hasattr(handler, "execute")
    assert hasattr(handler, "validate_prerequisites")
    assert callable(handler.execute)
    assert callable(handler.validate_prerequisites)


@pytest.mark.asyncio()
async def test_phase_handler_registry_execute_retrieved_handler() -> None:
    """
    Executes a handler retrieved from the registry and verifies its integration.
    
    Ensures that a handler obtained from the registry can validate prerequisites and execute successfully, returning a valid PhaseResult with expected artifacts and metadata.
    """
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler, "spec_test")

    # Get handler and create test context
    handler = registry.get_handler(SPARCPhase.SPECIFICATION)
    context = PhaseContext(
        session_id="registry-test-123",
        task_description="Test registry handler execution",
        previous_phases=[],
        global_artifacts={},
    )

    # Should be able to validate prerequisites
    assert handler.validate_prerequisites(context) is True

    # Should be able to execute handler
    result = await handler.execute(context)
    assert isinstance(result, PhaseResult)
    assert result.phase_name == "spec_test"
    assert "spec_test_output" in result.artifacts
    assert result.metadata["handler_type"] == "mock"


def test_phase_handler_registry_list_phases_consistency() -> None:
    """
    Tests that the PhaseHandlerRegistry's list_phases method consistently returns accurate and ordered phase listings after registrations.
    
    Ensures the registry's phase enumeration remains stable and reflects the current state.
    """
    registry = PhaseHandlerRegistry()

    # Initially empty
    assert len(registry.list_phases()) == 0

    # Add phases and verify listing
    registry.register(SPARCPhase.SPECIFICATION, MockPhaseHandler)
    phases = registry.list_phases()
    assert len(phases) == 1
    assert SPARCPhase.SPECIFICATION in phases

    registry.register(SPARCPhase.ARCHITECTURE, AnotherMockHandler)
    phases = registry.list_phases()
    assert len(phases) == 2
    assert SPARCPhase.SPECIFICATION in phases
    assert SPARCPhase.ARCHITECTURE in phases

    # Order should be consistent
    phases1 = registry.list_phases()
    phases2 = registry.list_phases()
    assert phases1 == phases2


def test_phase_handler_registry_thread_safety_simulation() -> None:
    """
    Simulates concurrent-like registrations and retrievals to verify registry consistency.
    
    Registers multiple handlers for different phases, then asserts all handlers are retrievable
    and the registry accurately lists all registered phases, ensuring robustness under simulated load.
    """
    registry = PhaseHandlerRegistry()

    # Simulate concurrent registrations
    phases_to_register = [
        (SPARCPhase.SPECIFICATION, MockPhaseHandler),
        (SPARCPhase.ARCHITECTURE, AnotherMockHandler),
        (SPARCPhase.COMPLETION, MockPhaseHandler),
        (SPARCPhase.VALIDATION, AnotherMockHandler),
    ]

    # Register all phases
    for phase, handler_class in phases_to_register:
        registry.register(phase, handler_class)

    # Verify all registrations are accessible
    for phase, expected_class in phases_to_register:
        handler = registry.get_handler(phase)
        assert isinstance(handler, expected_class)

    # Verify complete listing
    all_phases = registry.list_phases()
    assert len(all_phases) == 4
    for phase, _ in phases_to_register:
        assert phase in all_phases


def test_phase_handler_registry_error_handling() -> None:
    """
    Tests the registry's behavior when registering and retrieving an invalid handler class.
    
    Ensures that the registry either prevents registration of non-PhaseHandler classes or raises appropriate errors when such handlers are used, validating defensive programming and error reporting.
    """
    registry = PhaseHandlerRegistry()

    # Test registration with invalid handler class
    class NotAPhaseHandler:
        def some_other_method(self):
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
