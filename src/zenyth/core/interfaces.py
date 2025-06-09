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

from typing import Any, Protocol, runtime_checkable

from zenyth.core.exceptions import (  # noqa: F401
    CorruptionError,
    SessionNotFoundError,
    StorageError,
    ValidationError,
)
from zenyth.core.types import SessionContext, SPARCPhase


@runtime_checkable
class LLMInterface(Protocol):
    """Minimal protocol for Large Language Model provider integration.

    Defines the essential contract that all LLM providers must implement to
    participate in SPARC phase execution. The interface is deliberately minimal
    to maximize compatibility across different LLM services while providing the
    core functionality required for text generation.

    This protocol follows the Dependency Inversion Principle (DIP) by allowing
    high-level orchestration logic to depend on this abstraction rather than
    concrete LLM implementations. This enables provider swapping, testing with
    mocks, and adaptation to different LLM services in homelab environments.

    The async design ensures non-blocking execution during long-running phase
    operations, which is critical for responsive orchestration and resource
    efficiency in constrained homelab environments.

    Methods:
        generate: Asynchronously generate text response from a given prompt.
                 Accepts arbitrary keyword arguments to support provider-specific
                 parameters like temperature, max_tokens, model selection, etc.

    Examples:
        Implementing for OpenAI GPT::

            class OpenAIProvider:
                def __init__(self, api_key: str, model: str = "gpt-4"):
                    self.client = openai.AsyncOpenAI(api_key=api_key)
                    self.model = model

                async def generate(self, prompt: str, **kwargs: Any) -> str:
                    response = await self.client.chat.completions.create(
                        model=kwargs.get("model", self.model),
                        messages=[{"role": "user", "content": prompt}],
                        temperature=kwargs.get("temperature", 0.7),
                        max_tokens=kwargs.get("max_tokens", 1000)
                    )
                    return response.choices[0].message.content

        Implementing for local Ollama::

            class OllamaProvider:
                def __init__(self, base_url: str, model: str):
                    self.base_url = base_url
                    self.model = model

                async def generate(self, prompt: str, **kwargs: Any) -> str:
                    async with aiohttp.ClientSession() as session:
                        payload = {
                            "model": kwargs.get("model", self.model),
                            "prompt": prompt,
                            "stream": False
                        }
                        async with session.post(f"{self.base_url}/api/generate",
                                               json=payload) as response:
                            result = await response.json()
                            return result["response"]

        Testing with mock implementation::

            class MockLLMProvider:
                def __init__(self, responses: list[str]):
                    self.responses = responses
                    self.call_count = 0

                async def generate(self, prompt: str, **kwargs: Any) -> str:
                    response = self.responses[self.call_count % len(self.responses)]
                    self.call_count += 1
                    return f"Mock response to '{prompt}': {response}"

    Note:
        Implementations should handle errors appropriately and may raise exceptions
        for network failures, API errors, or invalid parameters. The protocol does
        not specify error handling to allow providers flexibility in error management
        strategies appropriate for their service characteristics.

        The **kwargs parameter allows providers to accept arbitrary configuration
        parameters without requiring interface changes, supporting extensibility
        while maintaining backward compatibility.
    """

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text response from the given prompt.

        Asynchronously processes the input prompt using the underlying LLM service
        and returns the generated text response. This method serves as the primary
        interface for all text generation operations in SPARC phase execution.

        Args:
            prompt: The input text prompt to process. Should be well-formatted
                   and contain clear instructions or questions for the LLM.
                   Maximum length depends on the provider's context window.
            **kwargs: Additional provider-specific parameters that may include:
                     - temperature: Randomness control (0.0-2.0 typical range)
                     - max_tokens: Maximum tokens to generate
                     - model: Specific model variant to use
                     - top_p: Nucleus sampling parameter
                     - frequency_penalty: Repetition penalty
                     - presence_penalty: Topic penalty
                     - stop: Stop sequences for generation termination
                     - timeout: Request timeout in seconds

        Returns:
            The generated text response as a string. The content and length
            depend on the prompt, provider capabilities, and configuration
            parameters. Empty strings are valid responses for certain prompts.

        Raises:
            The protocol does not specify exact exceptions to allow provider
            flexibility, but implementations typically raise:
            - ConnectionError: For network connectivity issues
            - TimeoutError: For request timeouts
            - ValueError: For invalid parameters or prompt format
            - AuthenticationError: For API key or credential issues
            - RateLimitError: For API rate limit exceeded
            - ProviderError: For service-specific errors

        Examples:
            Basic text generation::

                llm = SomeLLMProvider()
                response = await llm.generate("Explain quantum computing")
                print(response)

            With provider-specific parameters::

                response = await llm.generate(
                    "Write a Python function to sort a list",
                    temperature=0.2,
                    max_tokens=500,
                    model="gpt-4-turbo"
                )

            Error handling::

                try:
                    response = await llm.generate(prompt, timeout=30)
                except TimeoutError:
                    response = "Generation timed out, please try again"
                except Exception as e:
                    logger.error(f"LLM generation failed: {e}")
                    response = "Error occurred during generation"

        Note:
            Implementations should be thread-safe and support concurrent calls
            where the underlying service allows. Response times can vary significantly
            based on prompt complexity, model size, and service load.

            For homelab deployments, implementations should include appropriate
            retry logic and fallback strategies to handle temporary service
            unavailability or network issues.
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
