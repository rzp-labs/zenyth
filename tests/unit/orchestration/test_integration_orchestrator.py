"""Test suite for integrated SPARCOrchestrator with real phase execution.

Tests the complete integration between orchestrator and phase handlers,
validating end-to-end SPARC workflow execution and SOLID principles compliance.

SOLID Principles Alignment:
    - Single Responsibility: Orchestrator solely coordinates workflow execution
    - Open/Closed: Orchestrator closed for modification, extensible via dependency injection
    - Liskov Substitution: All injected dependencies are substitutable via protocols
    - Interface Segregation: Orchestrator depends on focused protocol interfaces
    - Dependency Inversion: Orchestrator depends on abstractions, not concrete implementations
"""

import inspect

import pytest

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import PhaseContext, PhaseResult, SessionContext, SPARCPhase, WorkflowResult
from zenyth.orchestration.orchestrator import SPARCOrchestrator
from zenyth.orchestration.registry import PhaseHandlerRegistry
from zenyth.phases.base import PhaseHandler


class MockLLMProvider(LLMInterface):
    """Mock LLM provider for testing orchestrator integration.

    Follows Liskov Substitution Principle by implementing LLMInterface contract.
    """

    def __init__(self, responses: list[str] | None = None):
        self.responses = responses or ["Mock LLM response"]
        self.call_count = 0
        self.prompts_received = []

    async def generate(self, prompt: str, **kwargs) -> str:
        self.prompts_received.append(prompt)
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response


class MockToolRegistry:
    """Mock tool registry for testing orchestrator integration.

    Follows Interface Segregation Principle with focused tool management.
    """

    def __init__(self):
        self.tools_by_phase = {
            SPARCPhase.SPECIFICATION: ["spec_tool1", "spec_tool2"],
            SPARCPhase.ARCHITECTURE: ["arch_tool1", "design_tool"],
            SPARCPhase.COMPLETION: ["code_tool", "build_tool"],
        }

    def get_for_phase(self, phase: SPARCPhase) -> list[str]:
        return self.tools_by_phase.get(phase, [])


class MockStateManager:
    """Mock state manager for testing orchestrator integration.

    Implements IStateManager protocol for session state persistence.
    """

    def __init__(self):
        self.sessions = {}
        self.save_calls = []
        self.load_calls = []

    async def save_session(self, session: SessionContext) -> None:
        self.save_calls.append(session.session_id)
        self.sessions[session.session_id] = session

    async def load_session(self, session_id: str) -> SessionContext:
        self.load_calls.append(session_id)
        return self.sessions.get(session_id)


class TestPhaseHandler(PhaseHandler):
    """Test phase handler that records execution for verification.

    Follows PhaseHandler contract for testing orchestrator integration.
    """

    def __init__(self, phase_name: str, should_fail: bool = False):
        self.phase_name = phase_name
        self.should_fail = should_fail
        self.execute_called = False
        self.validate_called = False
        self.context_received = None

    async def execute(self, context: PhaseContext) -> PhaseResult:
        self.execute_called = True
        self.context_received = context

        if self.should_fail:
            raise RuntimeError(f"{self.phase_name} phase failed intentionally")

        return PhaseResult(
            phase_name=self.phase_name,
            artifacts={f"{self.phase_name}_artifact": f"Result from {self.phase_name}"},
            next_phase="next_phase" if self.phase_name != "completion" else None,
            metadata={"executed_by": "TestPhaseHandler", "session_id": context.session_id},
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        self.validate_called = True
        return context.task_description is not None and len(context.task_description.strip()) > 0


@pytest.fixture()
def mock_dependencies():
    """Create mock dependencies for orchestrator testing.

    Follows Dependency Inversion Principle by providing abstract dependencies.
    """
    llm_provider = MockLLMProvider(["Spec response", "Arch response", "Completion response"])
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()
    return llm_provider, tool_registry, state_manager


@pytest.fixture()
def orchestrator_with_mocks(mock_dependencies):
    """Create orchestrator with mock dependencies for testing.

    Validates dependency injection pattern in orchestrator construction.
    """
    llm_provider, tool_registry, state_manager = mock_dependencies
    return SPARCOrchestrator(
        llm_provider=llm_provider, tool_registry=tool_registry, state_manager=state_manager
    )


def test_sparc_orchestrator_dependency_injection(mock_dependencies):
    """Test orchestrator properly stores injected dependencies.

    Validates Dependency Inversion Principle - orchestrator depends on abstractions.
    Tests that constructor properly stores all required dependencies.
    """
    llm_provider, tool_registry, state_manager = mock_dependencies

    orchestrator = SPARCOrchestrator(
        llm_provider=llm_provider, tool_registry=tool_registry, state_manager=state_manager
    )

    # Should store all injected dependencies
    assert orchestrator.llm_provider == llm_provider
    assert orchestrator.tool_registry == tool_registry
    assert orchestrator.state_manager == state_manager


def test_sparc_orchestrator_validate_dependencies() -> None:
    """Test orchestrator validates required dependencies are provided.

    Validates defensive programming and clear error reporting.
    Tests that missing dependencies are detected early.
    """
    # Should reject None dependencies
    with pytest.raises(ValueError, match=r".*dependencies.*"):
        SPARCOrchestrator(None, None, None)


@pytest.mark.asyncio()
async def test_sparc_orchestrator_execute_returns_workflow_result(orchestrator_with_mocks):
    """Test that orchestrator.execute returns proper WorkflowResult.

    Validates Single Responsibility - orchestrator coordinates workflow execution.
    Tests return type compliance with WorkflowResult contract.
    """
    result = await orchestrator_with_mocks.execute("Test task execution")

    # Should return WorkflowResult instance
    assert isinstance(result, WorkflowResult)
    assert hasattr(result, "success")
    assert hasattr(result, "task")
    assert hasattr(result, "phases_completed")
    assert hasattr(result, "artifacts")
    assert hasattr(result, "error")
    assert hasattr(result, "metadata")


@pytest.mark.asyncio()
async def test_sparc_orchestrator_execute_with_phase_registry(orchestrator_with_mocks):
    """Test orchestrator execution with phase handler registry.

    Validates Open/Closed Principle - orchestrator extensible via registry.
    Tests integration between orchestrator and phase registry.
    """
    # Set up phase registry with test handlers
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, TestPhaseHandler, "specification")
    registry.register(SPARCPhase.ARCHITECTURE, TestPhaseHandler, "architecture")

    # Mock the orchestrator's registry (this would normally be injected)
    # Note: This is a test-only workaround - real code would use dependency injection
    orchestrator_with_mocks._phase_registry = registry  # noqa: SLF001

    result = await orchestrator_with_mocks.execute("Build authentication system")

    # Should have executed phases via registry
    assert isinstance(result, WorkflowResult)
    assert result.task == "Build authentication system"


@pytest.mark.asyncio()
async def test_sparc_orchestrator_sequential_phase_execution() -> None:
    """Test orchestrator executes phases sequentially with context passing.

    Validates workflow coordination and context preservation between phases.
    Tests that phase results are properly passed to subsequent phases.
    """
    # Create orchestrator with real phase registry
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with multiple phases
    registry = PhaseHandlerRegistry()
    spec_handler = TestPhaseHandler("specification")
    arch_handler = TestPhaseHandler("architecture")
    comp_handler = TestPhaseHandler("completion")

    registry.register(SPARCPhase.SPECIFICATION, lambda: spec_handler)
    registry.register(SPARCPhase.ARCHITECTURE, lambda: arch_handler)
    registry.register(SPARCPhase.COMPLETION, lambda: comp_handler)

    orchestrator._phase_registry = registry  # noqa: SLF001

    # Execute workflow
    result = await orchestrator.execute("Multi-phase workflow test")

    # Should return valid WorkflowResult
    assert isinstance(result, WorkflowResult)
    assert result.task == "Multi-phase workflow test"

    # All handlers should have been called
    assert spec_handler.execute_called
    assert arch_handler.execute_called
    assert comp_handler.execute_called

    # Context should have been passed between phases
    assert spec_handler.context_received is not None
    assert arch_handler.context_received is not None
    assert comp_handler.context_received is not None

    # Later phases should see artifacts from earlier phases
    assert len(arch_handler.context_received.global_artifacts) > 0
    assert len(comp_handler.context_received.global_artifacts) >= 2


@pytest.mark.asyncio()
async def test_sparc_orchestrator_artifact_accumulation() -> None:
    """Test orchestrator accumulates artifacts across phases.

    Validates artifact management and workflow state preservation.
    Tests that artifacts from each phase are preserved in final result.
    """
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with test handlers that produce different artifacts
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))
    registry.register(SPARCPhase.ARCHITECTURE, lambda: TestPhaseHandler("architecture"))

    orchestrator._phase_registry = registry  # noqa: SLF001

    result = await orchestrator.execute("Test artifact accumulation")

    # Final result should contain artifacts from all phases
    assert "specification_artifact" in result.artifacts
    assert "architecture_artifact" in result.artifacts
    assert result.artifacts["specification_artifact"] == "Result from specification"
    assert result.artifacts["architecture_artifact"] == "Result from architecture"


@pytest.mark.asyncio()
async def test_sparc_orchestrator_error_handling() -> None:
    """Test orchestrator handles phase execution errors gracefully.

    Validates error handling and graceful degradation.
    Tests that workflow failures are properly reported.
    """
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with failing handler
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))
    registry.register(
        SPARCPhase.ARCHITECTURE, lambda: TestPhaseHandler("architecture", should_fail=True)
    )

    orchestrator._phase_registry = registry  # noqa: SLF001

    result = await orchestrator.execute("Test error handling")

    # Should return failed WorkflowResult
    assert isinstance(result, WorkflowResult)
    assert result.success is False
    assert result.error is not None
    assert "architecture phase failed" in result.error.lower()

    # Should contain phases that completed before failure
    assert len(result.phases_completed) == 1
    assert result.phases_completed[0].phase_name == "specification"


@pytest.mark.asyncio()
async def test_sparc_orchestrator_prerequisite_validation() -> None:
    """Test orchestrator validates phase prerequisites before execution.

    Validates fail-fast approach and prerequisite checking.
    Tests that invalid contexts are rejected before expensive operations.
    """
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up registry with handler that validates prerequisites
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))

    orchestrator._phase_registry = registry  # noqa: SLF001

    # Test with invalid task (empty string)
    result = await orchestrator.execute("")

    # Should fail due to prerequisite validation
    assert result.success is False
    assert result.error is not None
    assert "prerequisite" in result.error.lower() or "validation" in result.error.lower()


@pytest.mark.asyncio()
async def test_sparc_orchestrator_state_management_integration() -> None:
    """Test orchestrator integrates with state manager for session persistence.

    Validates state management integration and session handling.
    Tests that workflow state is properly saved and retrievable.
    """
    llm_provider = MockLLMProvider()
    tool_registry = MockToolRegistry()
    state_manager = MockStateManager()

    orchestrator = SPARCOrchestrator(llm_provider, tool_registry, state_manager)

    # Set up minimal registry
    registry = PhaseHandlerRegistry()
    registry.register(SPARCPhase.SPECIFICATION, lambda: TestPhaseHandler("specification"))

    orchestrator._phase_registry = registry  # noqa: SLF001

    result = await orchestrator.execute("Test state management")

    # Should return valid WorkflowResult
    assert isinstance(result, WorkflowResult)
    assert result.task == "Test state management"

    # State manager should have been called to save session
    assert len(state_manager.save_calls) > 0

    # Should be able to retrieve saved session
    session_id = state_manager.save_calls[0]
    saved_session = await state_manager.load_session(session_id)
    assert saved_session is not None
    assert saved_session.task == "Test state management"


def test_sparc_orchestrator_solid_principles_compliance() -> None:
    """Test that orchestrator implementation follows SOLID principles.

    Validates comprehensive SOLID compliance in orchestrator design.
    Tests architectural patterns and dependency relationships.
    """
    # Single Responsibility: Orchestrator should only coordinate workflow execution
    orchestrator_methods = [
        method
        for method in dir(SPARCOrchestrator)
        if not method.startswith("_") and callable(getattr(SPARCOrchestrator, method))
    ]

    # Should have focused interface - primarily execute method
    assert "execute" in orchestrator_methods

    # Should not have methods for specific phase logic, tool management, or LLM communication
    phase_methods = [
        m
        for m in orchestrator_methods
        if "specification" in m.lower() or "architecture" in m.lower()
    ]
    tool_methods = [m for m in orchestrator_methods if "tool" in m.lower() and m != "tool_registry"]
    llm_methods = [m for m in orchestrator_methods if "llm" in m.lower() and m != "llm_provider"]

    assert len(phase_methods) == 0, "Orchestrator should not contain phase-specific methods"
    assert len(tool_methods) == 0, "Orchestrator should not contain tool management methods"
    assert len(llm_methods) == 0, "Orchestrator should not contain LLM communication methods"

    # Dependency Inversion: Should accept abstract dependencies in constructor

    init_signature = inspect.signature(SPARCOrchestrator.__init__)
    init_params = list(init_signature.parameters.keys())

    assert "llm_provider" in init_params
    assert "tool_registry" in init_params
    assert "state_manager" in init_params
