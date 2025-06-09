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
        """
        Asynchronously generates a text response from the given prompt using an LLM provider.
        
        This method serves as the primary interface for text generation during SPARC phase execution. It accepts a prompt and optional provider-specific parameters, returning the generated text as a string. The response may be empty depending on the prompt and provider behavior.
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
        """
        Returns a list of tools appropriate for the given SPARC phase.
        
        Filters and provides only those tools permitted for the specified phase, supporting security and functional isolation in orchestrated workflows. Returns an empty list if no tools are available for the phase.
        
        Args:
            phase: The SPARC phase for which to retrieve tools.
        
        Returns:
            A list of tool objects or identifiers suitable for the specified phase. The list is empty if no tools are available.
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
        """
        Persists the complete session context for workflow recovery and auditability.
        
        Stores all relevant session data, including task details, artifacts, and metadata, to support workflow resumption and debugging in orchestration systems. Implementations should ensure data consistency and handle concurrent saves appropriately.
        """
        ...

    async def load_session(self, session_id: str) -> SessionContext:
        """
        Loads a previously saved session context by its unique identifier.
        
        Retrieves the complete session state, including task, artifacts, and metadata, to enable workflow resumption, analysis, or debugging. Implementations should ensure data integrity and provide clear error messages if loading fails.
        
        Args:
            session_id: The unique identifier of the session to load.
        
        Returns:
            The restored SessionContext as it was when saved.
        """
        ...
