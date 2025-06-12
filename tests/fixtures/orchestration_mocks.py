"""Common fixtures and mock classes for integration orchestrator tests.

This module provides shared test infrastructure for integration testing
the SPARCOrchestrator with real phase execution.
"""

import pytest

from zenyth.core.interfaces import LLMInterface
from zenyth.core.types import PhaseContext, PhaseResult, SessionContext, SPARCPhase
from zenyth.orchestration.orchestrator import SPARCOrchestrator
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
        llm_provider=llm_provider,
        tool_registry=tool_registry,
        state_manager=state_manager,
    )
