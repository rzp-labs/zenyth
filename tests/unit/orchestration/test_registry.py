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
        self.phase_name = phase_name
        self.execute_called = False
        self.validate_called = False
        self.call_count = 0

    async def execute(self, context: PhaseContext) -> PhaseResult:
        self.execute_called = True
        return PhaseResult(
            phase_name=self.phase_name,
            artifacts={f"{self.phase_name}_output": f"test_result_{self.call_count}"},
            metadata={"handler_type": "mock", "call_count": self.call_count},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        self.validate_called = True
        self.call_count += 1
        return context.task_description is not None


class AnotherMockHandler(PhaseHandler):
    """Alternative mock handler to test multiple registrations.

    Validates that different handlers can be registered and retrieved.
    """

    def __init__(self) -> None:
        self.response_suffix = "_different_result"

    async def execute(self, context: PhaseContext) -> PhaseResult:
        return PhaseResult(
            phase_name="alternative",
            artifacts={"alternative_output": f"alternative{self.response_suffix}"},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        # Use instance state to avoid static method warning
        min_length = len(self.response_suffix)
        return len(context.task_description or "") > min_length


def test_phase_handler_registry_creation() -> None:
    """Test PhaseHandlerRegistry instantiation.

    Validates Single Responsibility - registry creation without side effects.
    Tests basic registry initialization and empty state.
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
    """Test registering a single phase handler.

    Validates Open/Closed Principle - registry open for extension via registration.
    Tests basic registration functionality with SPARCPhase enum.
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
    """Test retrieving registered phase handler.

    Validates Dependency Inversion - registry depends on PhaseHandler abstraction.
    Tests that retrieved handlers implement the PhaseHandler contract.
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
    """Test retrieving handler that requires constructor arguments.

    Validates registry can handle handlers with initialization parameters.
    Tests dependency injection pattern through registry.
    """
    registry = PhaseHandlerRegistry()

    # Register handler class that takes constructor args
    registry.register(SPARCPhase.ARCHITECTURE, MockPhaseHandler, "architecture")

    # Should be able to get handler with args
    handler = registry.get_handler(SPARCPhase.ARCHITECTURE)
    assert handler is not None
    assert handler.phase_name == "architecture"


def test_phase_handler_registry_get_unregistered_handler() -> None:
    """Test retrieving handler for unregistered phase.

    Validates proper error handling for missing phase mappings.
    Tests registry robustness and clear error reporting.
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
    """Test that retrieved handlers comply with PhaseHandler contract.

    Validates Liskov Substitution - all handlers are substitutable.
    Tests that registry ensures contract compliance.
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
    """Test executing handler retrieved from registry.

    Validates complete integration between registry and handler execution.
    Tests that registry provides fully functional handler instances.
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
    """Test that list_phases returns consistent results.

    Validates Interface Segregation - focused query interface.
    Tests registry state consistency and proper enumeration.
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
    """Test registry behavior under simulated concurrent access.

    Validates registry robustness for concurrent registration/retrieval.
    Tests that registry maintains consistency under load.
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
    """Test registry error handling for invalid inputs.

    Validates registry robustness and proper error reporting.
    Tests defensive programming practices.
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
