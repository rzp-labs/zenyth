"""Minimal LLM interface protocol for Zenyth SPARC orchestration system.

This module defines the core abstraction layer for Large Language Model providers
used throughout the Zenyth system. The interface follows the Interface Segregation
Principle (ISP) by providing only the minimal contract required for SPARC phase
execution, allowing for flexible provider implementations without unnecessary coupling.

The protocol-based design enables runtime type checking and supports dependency
injection patterns critical for testing and provider swapping in homelab environments
where different LLM services may be used based on availability and performance.

Key Design Principles:
    - Minimal interface surface area for maximum flexibility
    - Async-first design for non-blocking orchestration
    - Runtime protocol checking for type safety
    - Provider-agnostic abstraction

Examples:
    Implementing a concrete LLM provider::

        class ClaudeProvider:
            async def generate(self, prompt: str, **kwargs: Any) -> str:
                # Claude-specific implementation
                response = await self.claude_client.complete(prompt, **kwargs)
                return response.content

    Using with type checking::

        def create_orchestrator(llm: LLMInterface) -> SPARCOrchestrator:
            # Type checker ensures llm implements the protocol
            return SPARCOrchestrator(llm)

    Runtime protocol verification::

        provider = SomeProvider()
        if isinstance(provider, LLMInterface):
            # Safe to use as LLM provider
            result = await provider.generate("Hello")
"""

from collections.abc import AsyncGenerator
from typing import Any, Protocol, runtime_checkable

from zenyth.core.exceptions import (
    CorruptionError,
    SessionNotFoundError,
    StorageError,
    ValidationError,
)
from zenyth.core.types import LLMResponse, SessionContext, SPARCPhase


@runtime_checkable
class LLMInterface(Protocol):
    """Minimal protocol for Large Language Model provider integration.

    Defines the essential contract that all LLM providers must implement to
    participate in SPARC phase execution. Enhanced with session management
    capabilities for complex workflows and conversation continuity.

    This protocol follows the Dependency Inversion Principle (DIP) by allowing
    high-level orchestration logic to depend on this abstraction rather than
    concrete LLM implementations. This enables provider swapping, testing with
    mocks, and adaptation to different LLM services in homelab environments.

    The async design ensures non-blocking execution during long-running phase
    operations, which is critical for responsive orchestration and resource
    efficiency in constrained homelab environments.

    Methods:
        generate: Legacy method for simple text generation (deprecated)
        complete_chat: Generate response from a chat prompt
        create_session: Create new conversation session
        complete_chat_with_session: Generate response within existing session
        get_session_history: Retrieve session conversation history
        fork_session: Create branched session for parallel exploration
        revert_session: Remove messages from session history
        get_session_metadata: Get session metadata and statistics
        stream_chat: Stream chat completion responses in real-time
    """

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text response from the given prompt.

        Legacy method maintained for backward compatibility.
        New implementations should prefer complete_chat.
        """
        ...

    async def complete_chat(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Generate chat completion response from the given prompt.

        Primary interface for single-turn chat interactions without session state.
        Returns structured response with content and metadata.

        Args:
            prompt: The input text prompt to process
            **kwargs: Provider-specific parameters (model, temperature, etc.)

        Returns:
            LLMResponse containing generated content and metadata
        """
        ...

    async def create_session(self) -> str:
        """Create a new conversation session.

        Returns:
            Unique session identifier for use in session-based operations
        """
        ...

    async def complete_chat_with_session(
        self, session_id: str, prompt: str, **kwargs: Any
    ) -> LLMResponse:
        """Generate chat completion within an existing session.

        Maintains conversation context across multiple interactions.
        Critical for SPARC workflows where phases build on each other.

        Args:
            session_id: Existing session identifier
            prompt: The input text prompt to process
            **kwargs: Provider-specific parameters

        Returns:
            LLMResponse containing generated content and session metadata
        """
        ...

    async def get_session_history(self, session_id: str) -> dict[str, Any]:
        """Retrieve conversation history for a session.

        Returns:
            Dictionary containing messages, metadata, and session statistics
        """
        ...

    async def fork_session(self, session_id: str, name: str | None = None) -> str:
        """Create a branched session from an existing session.

        Enables parallel exploration of different approaches while maintaining
        the original conversation context. Perfect for SPARC architecture
        phase exploration.

        Args:
            session_id: Parent session to fork from
            name: Optional name for the forked session

        Returns:
            New session identifier for the forked session
        """
        ...

    async def revert_session(self, session_id: str, steps: int = 1) -> None:
        """Remove messages from session history.

        Enables "undoing" problematic interactions and trying alternative
        approaches. Critical for workflow debugging and refinement.

        Args:
            session_id: Session to modify
            steps: Number of messages to remove (default 1)
        """
        ...

    async def get_session_metadata(self, session_id: str) -> dict[str, Any]:
        """Get metadata and statistics for a session.

        Returns:
            Dictionary containing session metadata, usage stats, timing info
        """
        ...

    def stream_chat(self, prompt: str, **kwargs: Any) -> AsyncGenerator[LLMResponse, None]:
        """Stream chat completion responses in real-time.

        Yields incremental response chunks for real-time monitoring and
        early intervention. Critical for long-running tasks.

        Args:
            prompt: The input text prompt to process
            **kwargs: Provider-specific parameters

        Yields:
            LLMResponse objects containing incremental content chunks
        """
        ...


@runtime_checkable
class IToolRegistry(Protocol):
    """Protocol for tool registry abstraction in SPARC orchestration.

    Defines the contract for managing and providing tools based on SPARC phases.
    Following Interface Segregation Principle (ISP) with minimal, focused interface
    for tool management without coupling to other orchestration concerns.

    This protocol enables dependency inversion where high-level orchestration logic
    depends on this abstraction rather than concrete tool registry implementations.
    Critical for testing, provider swapping, and phase-based tool filtering in
    homelab environments with varying tool availability.

    SOLID Principles Alignment:
        - Single Responsibility: Focused solely on tool provision for phases
        - Open/Closed: Closed for modification, open for implementation
        - Liskov Substitution: All implementations must honor exact contract
        - Interface Segregation: Minimal tool-focused interface
        - Dependency Inversion: Enables abstraction-based dependencies

    Methods:
        get_for_phase: Retrieve tools appropriate for a specific SPARC phase.
                      Supports phase-based filtering for security and functionality.

    Examples:
        Implementing for MCP tool registry::

            class MCPToolRegistry:
                def __init__(self, mcp_client):
                    self.mcp_client = mcp_client
                    self.phase_tools = {
                        SPARCPhase.SPECIFICATION: ["read_file", "search"],
                        SPARCPhase.ARCHITECTURE: ["read_file", "create_diagram"],
                        SPARCPhase.COMPLETION: ["read_file", "write_file", "execute"]
                    }

                def get_for_phase(self, phase: SPARCPhase) -> list[Any]:
                    tool_names = self.phase_tools.get(phase, [])
                    return [self.mcp_client.get_tool(name) for name in tool_names]

        Implementing for testing::

            class MockToolRegistry:
                def get_for_phase(self, phase: SPARCPhase) -> list[Any]:
                    return [f"mock_tool_for_{phase.value}"]

        Using in orchestration::

            class SPARCOrchestrator:
                def __init__(self, tool_registry: IToolRegistry):
                    self.tools = tool_registry

                async def execute_phase(self, phase: SPARCPhase):
                    phase_tools = self.tools.get_for_phase(phase)
                    # Use phase-appropriate tools
    """

    def get_for_phase(self, phase: SPARCPhase) -> list[Any]:
        """Retrieve tools appropriate for the specified SPARC phase.

        Provides phase-specific tool filtering to ensure each phase has access
        only to appropriate tools based on security requirements and functionality
        needs. Critical for maintaining isolation and preventing unauthorized
        operations in orchestrated workflows.

        Args:
            phase: The SPARC phase for which to retrieve tools. Different phases
                  require different tool sets - specification might need read-only
                  tools, while completion might need write and execute permissions.

        Returns:
            List of tool objects or identifiers appropriate for the specified phase.
            Empty list if no tools are available for the phase. Tool objects can
            be any type depending on the implementation (MCP tools, function objects,
            service clients, etc.).

        Examples:
            Getting specification phase tools::

                tools = registry.get_for_phase(SPARCPhase.SPECIFICATION)
                # Returns: [read_file_tool, search_tool, analyze_tool]

            Getting completion phase tools::

                tools = registry.get_for_phase(SPARCPhase.COMPLETION)
                # Returns: [read_tool, write_tool, execute_tool, build_tool]

            Handling unknown phases::

                tools = registry.get_for_phase(SPARCPhase.CUSTOM_PHASE)
                # Returns: [] (empty list for unknown phases)

        Note:
            Implementations should return consistent tool sets for the same phase
            to ensure predictable workflow execution. Tool availability may vary
            based on environment configuration and security policies.

            For homelab environments, implementations should handle tool
            unavailability gracefully and provide appropriate fallbacks or
            clear error reporting when required tools are missing.
        """
        ...


@runtime_checkable
class IStateManager(Protocol):
    """Protocol for session state management in SPARC orchestration.

    Defines the contract for persisting and retrieving workflow session state
    across phase transitions and system restarts. Following Interface Segregation
    Principle (ISP) with focused responsibility for state operations only.

    This protocol enables dependency inversion where orchestration logic depends
    on this abstraction rather than concrete state storage implementations.
    Critical for workflow resumption, debugging, and audit trails in homelab
    environments where reliability and transparency are essential.

    SOLID Principles Alignment:
        - Single Responsibility: Focused solely on session state persistence
        - Open/Closed: Closed for modification, open for implementation
        - Liskov Substitution: All implementations must honor async contracts
        - Interface Segregation: Minimal state-focused interface
        - Dependency Inversion: Enables abstraction-based dependencies

    Methods:
        save_session: Persist session state for later retrieval and recovery.
        load_session: Retrieve previously saved session state by identifier.

    Examples:
        Implementing for file-based storage::

            class FileStateManager:
                def __init__(self, storage_dir: Path):
                    self.storage_dir = storage_dir

                async def save_session(self, session: SessionContext) -> None:
                    session_file = self.storage_dir / f"{session.session_id}.json"
                    with open(session_file, 'w') as f:
                        json.dump(asdict(session), f, indent=2)

                async def load_session(self, session_id: str) -> SessionContext:
                    session_file = self.storage_dir / f"{session_id}.json"
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                    return SessionContext(**data)

        Implementing for database storage::

            class DatabaseStateManager:
                async def save_session(self, session: SessionContext) -> None:
                    await self.db.sessions.upsert({
                        "session_id": session.session_id,
                        "task": session.task,
                        "artifacts": json.dumps(session.artifacts),
                        "metadata": json.dumps(session.metadata)
                    })

        Using in orchestration::

            class SPARCOrchestrator:
                def __init__(self, state_manager: IStateManager):
                    self.state = state_manager

                async def execute(self, task: str):
                    session = SessionContext(...)
                    await self.state.save_session(session)
                    # Continue workflow...
    """

    async def save_session(self, session: SessionContext) -> None:
        """Persist session state for later retrieval and recovery.

        Stores complete session context including task description, artifacts,
        and metadata to enable workflow resumption, debugging, and audit trails.
        Critical for reliability in long-running orchestration workflows.

        Args:
            session: Complete session context to persist. Should contain all
                    information needed to resume or analyze the workflow state
                    including task description, accumulated artifacts, and
                    execution metadata.

        Raises:
            StorageError: If session cannot be saved due to storage issues
            ValidationError: If session data is invalid or incomplete
            PermissionError: If insufficient permissions for storage operation

        Examples:
            Saving workflow session::

                session = SessionContext(
                    session_id="sparc-auth-20240101",
                    task="Implement authentication system",
                    artifacts={"specification": "..."},
                    metadata={"start_time": "2024-01-01T10:00:00Z"}
                )
                await state_manager.save_session(session)

            Error handling::

                try:
                    await state_manager.save_session(session)
                except StorageError as e:
                    logger.error(f"Failed to save session: {e}")
                    # Implement fallback strategy

        Note:
            Implementations should handle concurrent save operations gracefully
            and ensure data consistency. Session data should be serializable
            for storage in various backends (files, databases, cloud storage).

            For homelab environments, implementations should include appropriate
            backup strategies and recovery mechanisms to prevent data loss.
        """
        ...

    async def load_session(self, session_id: str) -> SessionContext:
        """Retrieve previously saved session state by identifier.

        Loads complete session context to enable workflow resumption, analysis,
        or debugging. Critical for recovering from interruptions and providing
        comprehensive audit trails for orchestrated workflows.

        Args:
            session_id: Unique identifier for the session to retrieve. Should
                       correspond to a previously saved session identifier.

        Returns:
            Complete SessionContext with task, artifacts, and metadata as they
            were when the session was saved. All data should be restored exactly
            to enable proper workflow resumption.

        Raises:
            SessionNotFoundError: If session_id does not exist in storage
            StorageError: If session cannot be loaded due to storage issues
            CorruptionError: If stored session data is corrupted or invalid
            PermissionError: If insufficient permissions for read operation

        Examples:
            Loading existing session::

                session = await state_manager.load_session("sparc-auth-20240101")
                print(f"Task: {session.task}")
                print(f"Artifacts: {session.artifacts}")

            Error handling::

                try:
                    session = await state_manager.load_session(session_id)
                except SessionNotFoundError:
                    # Handle missing session
                    session = create_new_session()
                except CorruptionError as e:
                    logger.error(f"Session data corrupted: {e}")
                    # Implement recovery strategy

        Note:
            Implementations should validate loaded data integrity and provide
            clear error messages for debugging. Session loading should be
            fast enough for interactive use in orchestration workflows.

            For homelab environments, implementations should include appropriate
            caching strategies and handle storage backend unavailability gracefully.
        """
        ...
