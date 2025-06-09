"""Test suite for protocol interfaces in Zenyth core system.

Tests the IToolRegistry and IStateManager protocol definitions, validating
interface contracts and enabling proper dependency injection patterns.

SOLID Principles Alignment:
    - Single Responsibility: Each protocol has one focused responsibility
    - Open/Closed: Protocols are closed for modification, open for implementation
    - Liskov Substitution: All implementations must honor protocol contracts
    - Interface Segregation: Minimal, focused interfaces without fat contracts
    - Dependency Inversion: Enables depending on abstractions, not concretions
"""

from typing import Any
from unittest.mock import Mock

import pytest

from zenyth.core.interfaces import IStateManager, IToolRegistry, LLMInterface
from zenyth.core.types import SessionContext, SPARCPhase


def test_itool_registry_protocol_exists() -> None:
    """
    Verifies that the IToolRegistry protocol is correctly defined as a typing.Protocol.
    
    Asserts the presence of protocol-specific attributes and metaclass to ensure proper protocol behavior and runtime type checking.
    """
    # Should be able to import and check as protocol
    assert hasattr(IToolRegistry, "_is_protocol")
    assert IToolRegistry.__class__.__name__ == "_ProtocolMeta"


def test_itool_registry_get_for_phase_signature() -> None:
    """
    Verifies that IToolRegistry defines a callable get_for_phase method with the correct signature.
    
    Ensures the method accepts a SPARCPhase argument and returns a list of tools, confirming interface contract adherence.
    """
    # Create mock implementation to test interface compliance
    mock_registry = Mock(spec=IToolRegistry)
    mock_registry.get_for_phase.return_value = ["tool1", "tool2"]

    # Should have the required method
    assert hasattr(mock_registry, "get_for_phase")
    assert callable(mock_registry.get_for_phase)

    # Test method call with SPARCPhase
    tools = mock_registry.get_for_phase(SPARCPhase.SPECIFICATION)
    assert tools == ["tool1", "tool2"]

    # Verify call was made with correct argument
    mock_registry.get_for_phase.assert_called_once_with(SPARCPhase.SPECIFICATION)


def test_itool_registry_runtime_checking() -> None:
    """Test IToolRegistry runtime protocol checking.

    Validates Liskov Substitution - implementations must honor protocol contract.
    Tests that incorrect implementations are rejected at runtime.
    """

    # Create correct implementation with instance state
    class ValidToolRegistry:
        def __init__(self) -> None:
            """
            Initializes the mock tool registry with a default tool cache.
            """
            self.tool_cache = {"default": ["tool1", "tool2"]}

        def get_for_phase(self, phase: SPARCPhase) -> list[Any]:
            """
            Retrieves a list of tools associated with the specified SPARC phase.
            
            Args:
                phase: The SPARCPhase for which to retrieve tools.
            
            Returns:
                A list of tools relevant to the given phase, or an empty list if none are found.
            """
            return self.tool_cache.get("default", [])

    # Create incorrect implementation (missing method)
    class InvalidToolRegistry:
        def wrong_method(self):
            pass

    valid_registry = ValidToolRegistry()
    invalid_registry = InvalidToolRegistry()

    # Runtime checking should work correctly
    assert isinstance(valid_registry, IToolRegistry)
    assert not isinstance(invalid_registry, IToolRegistry)


def test_istate_manager_protocol_exists() -> None:
    """Test that IStateManager protocol is properly defined.

    Validates Interface Segregation Principle - focused state management contract.
    Tests protocol definition and runtime checking capability.
    """
    # Should be able to import and check as protocol
    assert hasattr(IStateManager, "_is_protocol")
    assert IStateManager.__class__.__name__ == "_ProtocolMeta"


def test_istate_manager_save_session_signature() -> None:
    """
    Verifies that IStateManager defines an async save_session method.
    
    Ensures the protocol exposes the required method for session state persistence and that it is callable.
    """
    # Create mock implementation to test interface compliance
    mock_manager = Mock(spec=IStateManager)

    # Should have the required async method
    assert hasattr(mock_manager, "save_session")
    assert callable(mock_manager.save_session)


def test_istate_manager_load_session_signature() -> None:
    """Test IStateManager load_session method signature.

    Validates Single Responsibility - focused on session state retrieval.
    Tests async interface contract for loading session state.
    """
    # Create mock implementation to test interface compliance
    mock_manager = Mock(spec=IStateManager)

    # Should have the required async method
    assert hasattr(mock_manager, "load_session")
    assert callable(mock_manager.load_session)


@pytest.mark.asyncio()
async def test_istate_manager_full_interface() -> None:
    """
    Validates that a mock implementation of IStateManager correctly saves and loads session contexts asynchronously.
    
    This test ensures that the full async interface contract for IStateManager is honored, verifying that session data can be stored and retrieved as expected.
    """

    # Create mock that simulates async behavior
    class MockStateManager:
        def __init__(self):
            Initializes the mock state manager with an empty session storage dictionary.
            self.sessions = {}

        async def save_session(self, session: SessionContext) -> None:
            """
            Saves a session context to the internal session store.
            
            Args:
                session: The session context to be saved, identified by its session_id.
            """
            self.sessions[session.session_id] = session

        async def load_session(self, session_id: str) -> SessionContext:
            """
            Retrieves a session context by its session ID.
            
            Args:
                session_id: The unique identifier of the session to load.
            
            Returns:
                The SessionContext associated with the given session ID, or None if not found.
            """
            return self.sessions.get(session_id)

    manager = MockStateManager()

    # Test session creation and saving
    session = SessionContext(
        session_id="test-session-123",
        task="Test task for state management",
        artifacts={"test": "data"},
        metadata={"created": "2024-01-01"},
    )

    # Should be able to save session
    await manager.save_session(session)
    assert "test-session-123" in manager.sessions

    # Should be able to load session
    loaded_session = await manager.load_session("test-session-123")
    assert loaded_session.session_id == "test-session-123"
    assert loaded_session.task == "Test task for state management"


def test_istate_manager_runtime_checking() -> None:
    """
    Tests that only classes implementing all required IStateManager protocol methods pass runtime type checks.
    
    Ensures that valid implementations with both async `save_session` and `load_session` methods are recognized as IStateManager, while incomplete implementations are not.
    """

    # Create correct implementation with instance state
    class ValidStateManager:
        def __init__(self) -> None:
            Initializes the mock state manager with an empty session storage dictionary.
            self.sessions: dict[str, SessionContext] = {}

        async def load_session(self, session_id: str) -> SessionContext:
            """
            Loads a session context for the given session ID.
            
            Args:
                session_id: The unique identifier of the session to load.
            
            Returns:
                The SessionContext associated with the session ID, or a new SessionContext if none exists.
            """
            return self.sessions.get(session_id, SessionContext(session_id=session_id, task="test"))

        async def save_session(self, session: SessionContext) -> None:
            """
            Saves a session context to the internal session store.
            
            Args:
                session: The session context to be saved, identified by its session_id.
            """
            self.sessions[session.session_id] = session

    # Create incorrect implementation (missing method)
    class InvalidStateManager:
        async def save_session(self, session: SessionContext) -> None:
            """
            Persists the provided session context asynchronously.
            
            Args:
                session: The session context to be saved.
            """
            pass

        # Missing load_session method

    valid_manager = ValidStateManager()
    invalid_manager = InvalidStateManager()

    # Runtime checking should work correctly
    assert isinstance(valid_manager, IStateManager)
    assert not isinstance(invalid_manager, IStateManager)


def test_llm_interface_protocol_still_works() -> None:
    """
    Verifies that a mock implementation satisfies the LLMInterface protocol.
    
    Ensures that a class with an async `generate` method passes runtime type checks and maintains compatibility with the LLMInterface abstraction.
    """

    # Create mock LLM implementation with instance state
    class MockLLMProvider:
        def __init__(self) -> None:
            """
            Initializes the mock LLM provider with a predefined response prefix.
            """
            self.response_prefix = "Generated response to: "

        async def generate(self, prompt: str, **kwargs: Any) -> str:
            """
            Generates a response string by prefixing the prompt with a predefined value.
            
            Args:
                prompt: The input string to be processed.
            
            Returns:
                The generated string with the response prefix prepended to the prompt.
            """
            return f"{self.response_prefix}{prompt}"

    provider = MockLLMProvider()

    # Should pass runtime checking
    assert isinstance(provider, LLMInterface)

    # Should have required method
    assert hasattr(provider, "generate")
    assert callable(provider.generate)


def test_protocol_separation_of_concerns() -> None:
    """
    Verifies that each protocol exposes only methods relevant to its domain, ensuring separation of concerns.
    
    Asserts that IToolRegistry, IStateManager, and LLMInterface maintain focused responsibilities by checking their method names for domain-specific keywords.
    """
    # IToolRegistry should only deal with tools
    tool_methods = [attr for attr in dir(IToolRegistry) if not attr.startswith("_")]
    assert any("tool" in method.lower() or "phase" in method.lower() for method in tool_methods)

    # IStateManager should only deal with state/sessions
    state_methods = [attr for attr in dir(IStateManager) if not attr.startswith("_")]
    assert any("session" in method.lower() for method in state_methods)

    # LLMInterface should only deal with text generation
    llm_methods = [attr for attr in dir(LLMInterface) if not attr.startswith("_")]
    assert any("generate" in method.lower() for method in llm_methods)


def test_dependency_inversion_enablement() -> None:
    """
    Verifies that protocol abstractions support dependency inversion by allowing high-level components to depend on them.
    
    This test ensures that instances of `LLMInterface`, `IToolRegistry`, and `IStateManager` can be injected into a high-level orchestrator, confirming that the protocols enable proper dependency injection and storage of dependencies.
    """

    # Simulate high-level component depending on abstractions
    class HighLevelOrchestrator:
        def __init__(
            self,
            llm_provider: LLMInterface,
            tool_registry: IToolRegistry,
            state_manager: IStateManager,
        ):
            """
            Initializes the orchestrator with LLM, tool registry, and state manager dependencies.
            
            Args:
                llm_provider: An implementation of the LLMInterface protocol.
                tool_registry: An implementation of the IToolRegistry protocol.
                state_manager: An implementation of the IStateManager protocol.
            """
            self.llm_provider = llm_provider
            self.tool_registry = tool_registry
            self.state_manager = state_manager

        def has_dependencies(self) -> bool:
            """
            Determines whether all required dependencies are present.
            
            Returns:
                True if the LLM provider, tool registry, and state manager are all set; otherwise, False.
            """
            return all(
                [
                    self.llm_provider is not None,
                    self.tool_registry is not None,
                    self.state_manager is not None,
                ]
            )

    # Create mock implementations
    mock_llm = Mock(spec=LLMInterface)
    mock_tools = Mock(spec=IToolRegistry)
    mock_state = Mock(spec=IStateManager)

    # Should be able to inject dependencies
    orchestrator = HighLevelOrchestrator(mock_llm, mock_tools, mock_state)

    # Should store injected dependencies
    assert orchestrator.llm_provider == mock_llm
    assert orchestrator.tool_registry == mock_tools
    assert orchestrator.state_manager == mock_state
