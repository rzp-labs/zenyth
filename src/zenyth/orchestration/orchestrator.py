"""Core SPARC workflow orchestration implementation.

This module contains the main SPARCOrchestrator class that coordinates workflow
execution across SPARC methodology phases. The orchestrator is designed following
SOLID principles with dependency injection for LLM providers, tool registries,
and state management systems.

The implementation focuses on orchestration logic only, delegating specific
responsibilities to injected dependencies following the Single Responsibility
and Dependency Inversion principles.
"""

import time
import uuid
from typing import TYPE_CHECKING, Any

from zenyth.core.types import PhaseContext, SessionContext, WorkflowResult

if TYPE_CHECKING:
    from zenyth.orchestration.registry import PhaseHandlerRegistry


class SPARCOrchestrator:
    """Main workflow orchestrator for SPARC methodology execution.
    
    Coordinates the execution of SPARC phases (Specification, Pseudocode,
    Architecture, Refinement, Completion, Validation, Integration) while
    maintaining session state and managing tool access per phase.

    This class serves as the high-level orchestration coordinator and depends
    on abstractions rather than concrete implementations, following the
    Dependency Inversion Principle (DIP). It delegates specific responsibilities
    to injected dependencies following the Single Responsibility Principle (SRP).

    Design Principles Applied:
        - Single Responsibility: Only handles workflow orchestration coordination
        - Open/Closed: Extensible through dependency injection, closed for modification
        - Liskov Substitution: All dependencies are interchangeable via interfaces
        - Interface Segregation: Depends on focused abstractions, not fat interfaces
        - Dependency Inversion: Depends on abstractions, not concrete implementations

    Attributes:
        llm_provider: LLM service abstraction for intelligent phase execution
        tool_registry: Tool management abstraction for phase-specific tool access
        state_manager: Session state persistence abstraction for workflow continuity

    Examples:
        Basic orchestrator usage::

            orchestrator = SPARCOrchestrator(
                llm_provider=claude_provider,
                tool_registry=mcp_registry,
                state_manager=session_manager
            )

            result = await orchestrator.execute("Create user authentication system")
            print(f"Workflow completed: {result.success}")

        Orchestrator with different implementations::

            # Production orchestrator
            prod_orchestrator = SPARCOrchestrator(
                llm_provider=ClaudeCodeProvider(),
                tool_registry=MCPToolRegistry(),
                state_manager=DatabaseStateManager()
            )

            # Test orchestrator with mocks
            test_orchestrator = SPARCOrchestrator(
                llm_provider=MockLLMProvider(responses=["test"]),
                tool_registry=MockToolRegistry(),
                state_manager=InMemoryStateManager()
            )

        Error handling workflow::

            try:
                result = await orchestrator.execute("Complex task")
                if not result.success:
                    logger.error(f"Workflow failed: {result.error}")
            except OrchestrationError as e:
                logger.error(f"Orchestration error: {e}")

    Note:
        The orchestrator follows the Hollywood Principle ("Don't call us, we'll
        call you") by controlling the workflow execution flow while delegating
        specific implementation details to injected dependencies.

        All dependencies must be provided during initialization to ensure proper
        operation. The orchestrator does not create or manage the lifecycle of
        its dependencies, maintaining clear separation of concerns.
    """
    
    _phase_registry: "PhaseHandlerRegistry | None"

    def __init__(self, llm_provider: Any, tool_registry: Any, state_manager: Any) -> None:
        """
        Initializes the SPARCOrchestrator with required workflow dependencies.
        
        Validates and stores the provided LLM provider, tool registry, and state manager abstractions for later use in workflow orchestration. Raises a ValueError if any dependency is missing to ensure fail-fast behavior.
        """
        # Validate dependencies following fail-fast principle
        if llm_provider is None or tool_registry is None or state_manager is None:
            msg = "All dependencies (llm_provider, tool_registry, state_manager) must be provided"
            raise ValueError(msg)

        # Store dependencies for later use (Dependency Inversion Principle)
        self.llm_provider = llm_provider
        self.tool_registry = tool_registry
        self.state_manager = state_manager
        self._phase_registry = None

        # Initialize phase registry for connecting to phase handlers
        # This will be injected or created based on configuration in future iterations
        self._phase_registry = None

    async def execute(self, task: str) -> Any:
        """
        Executes the full SPARC workflow for a given task, coordinating all phases and managing session state.
        
        Validates the input task, initializes a session, and sequentially executes each registered SPARC phase using injected dependencies for LLM, tool management, and state persistence. Accumulates artifacts and tracks completed phases. Returns a detailed `WorkflowResult` indicating success or failure, including artifacts, completed phases, timing, and error metadata. If the task is empty or a phase fails, returns a failure result with diagnostic information.
        """
        # Validate input following fail-fast principle (Single Responsibility)
        if not task or not task.strip():
            # Return failed result for empty task instead of raising exception
            return WorkflowResult(
                success=False,
                task="",
                phases_completed=[],
                artifacts={},
                error="Task description cannot be empty - prerequisite validation failed",
                metadata={
                    "total_duration": 0.0,
                    "session_id": "invalid",
                    "error_type": "ValidationError",
                    "failure_stage": "prerequisite_validation",
                },
            )

        # Generate unique session ID for tracking and state management
        session_id = f"sparc-{int(time.time())}-{str(uuid.uuid4())[:8]}"
        start_time = time.time()
        phases_completed: list[Any] = []
        accumulated_artifacts: dict[str, Any] = {}
        phases_attempted = 0

        try:
            # Create session context for state management (Dependency Inversion)
            session_context = SessionContext(
                session_id=session_id,
                task=task.strip(),
                artifacts={},
                metadata={
                    "start_time": time.time(),
                    "orchestrator_version": "1.0.0",
                    "sparc_methodology": True,
                },
            )

            # Save initial session state (Single Responsibility - delegate to state manager)
            await self.state_manager.save_session(session_context)

            # Execute phases if registry is available
            if self._phase_registry is not None:
                # Get available phases from registry
                available_phases = self._phase_registry.list_phases()

                # Execute each available phase in sequence
                for phase in available_phases:
                    phases_attempted += 1

                    try:
                        # Get phase handler from registry (Open/Closed Principle)
                        handler = self._phase_registry.get_handler(phase)

                        # Create phase context with accumulated artifacts
                        phase_context = PhaseContext(
                            session_id=session_id,
                            task_description=task.strip(),
                            previous_phases=[p.phase_name for p in phases_completed],
                            global_artifacts=accumulated_artifacts.copy(),
                        )

                        # Validate prerequisites before execution
                        if not handler.validate_prerequisites(phase_context):
                            # Skip phase if prerequisites not met, but don't fail entire workflow
                            continue

                        # Execute phase (Liskov Substitution - all handlers substitutable)
                        phase_result = await handler.execute(phase_context)

                        # Accumulate artifacts from phase result
                        if hasattr(phase_result, "artifacts") and phase_result.artifacts:
                            accumulated_artifacts.update(phase_result.artifacts)

                        # Track completed phases
                        phases_completed.append(phase_result)

                    except Exception as phase_error:
                        # Handle phase execution errors gracefully
                        end_time = time.time()
                        error_message = f"{phase.value} phase failed: {phase_error!s}"

                        return WorkflowResult(
                            success=False,
                            task=task.strip(),
                            phases_completed=phases_completed,
                            artifacts=accumulated_artifacts,
                            error=error_message,
                            metadata={
                                "total_duration": end_time - start_time,
                                "session_id": session_id,
                                "start_time": start_time,
                                "end_time": end_time,
                                "phases_attempted": phases_attempted,
                                "failed_phase": phase.value,
                                "error_type": type(phase_error).__name__,
                            },
                        )



            # Create successful workflow result (Open/Closed - extensible through configuration)
            end_time = time.time()
            return WorkflowResult(
                success=True,
                task=task.strip(),
                phases_completed=phases_completed,
                artifacts={
                    **accumulated_artifacts,  # Include phase artifacts
                    "session_info": {
                        "session_id": session_id,
                        "orchestrator": "SPARCOrchestrator",
                        "methodology": "SPARC",
                    },
                },
                error=None,
                metadata={
                    "total_duration": end_time - start_time,
                    "session_id": session_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "phases_attempted": phases_attempted,
                    "dependencies_validated": True,
                    "state_management": "enabled",
                },
            )

        except Exception as e:
            # Error handling with comprehensive context (Single Responsibility)
            end_time = time.time()
            error_message = f"Workflow execution failed: {e!s}"

            # Create failed workflow result with error information
            return WorkflowResult(
                success=False,
                task=task.strip(),
                phases_completed=phases_completed,
                artifacts=accumulated_artifacts,
                error=error_message,
                metadata={
                    "total_duration": end_time - start_time,
                    "session_id": session_id,
                    "error_type": type(e).__name__,
                    "failure_stage": "orchestration_setup",
                    "phases_attempted": phases_attempted,
                },
            )
