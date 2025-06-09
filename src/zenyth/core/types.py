"""Core data types for Zenyth SPARC orchestration system.

This module provides the fundamental immutable data structures used throughout
the Zenyth system for representing phase execution results and session state.
All types follow SOLID principles with clear separation of concerns and are
designed for thread-safety through immutability.

The types are optimized for homelab environments where memory efficiency and
clear error propagation are critical for debugging and monitoring.

Examples:
    Creating a successful phase result::

        result = PhaseResult(
            success=True,
            output="Phase completed successfully",
            metadata={"duration": 1.5, "tokens_used": 150}
        )

    Creating a session context::

        context = SessionContext(
            session_id="sparc-session-123",
            task="Implement user authentication",
            artifacts={"specification": "User auth spec..."},
            metadata={"start_time": "2024-01-01T10:00:00Z"}
        )
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SPARCPhase(Enum):
    """Enumeration of SPARC methodology phases.

    Defines the complete set of phases in the SPARC workflow following
    the established methodology with homelab-specific additions.
    """

    SPECIFICATION = "specification"
    PSEUDOCODE = "pseudocode"
    ARCHITECTURE = "architecture"
    REFINEMENT = "refinement"
    COMPLETION = "completion"
    VALIDATION = "validation"
    INTEGRATION = "integration"


@dataclass(frozen=True)
class PhaseContext:
    """Immutable context container for individual phase execution.

    Provides the necessary context and state for executing a single SPARC
    phase, including session information, task details, and accumulated
    artifacts from previous phases.

    Attributes:
        session_id: Unique identifier for the parent orchestration session
        task_description: The original task description or current focus
        previous_phases: List of PhaseResult objects from completed phases
        global_artifacts: Shared artifacts accessible to all phases
    """

    session_id: str
    task_description: str | None
    previous_phases: list["PhaseResult"] = field(default_factory=list)
    global_artifacts: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PhaseResult:
    """Immutable result container for SPARC phase execution outcomes.

    Represents the complete result of executing a single SPARC methodology phase,
    including success status, output content, error information, and execution
    metadata. Designed for reliable error propagation and comprehensive logging
    in homelab automation workflows.

    The frozen dataclass ensures thread-safety and prevents accidental mutation
    of results after creation, which is critical for audit trails and debugging.

    Attributes:
        phase_name: The name/identifier of the SPARC phase that was executed
        artifacts: Dictionary of artifacts produced by this phase execution
        next_phase: Optional identifier of the next phase to execute
        metadata: Additional execution context and metrics as key-value pairs.
                 Common keys include 'duration', 'tokens_used', 'tool_calls',
                 'timestamp', 'session_id'. Defaults to empty dict if not provided.

    Examples:
        Successful phase execution::

            result = PhaseResult(
                phase_name="architecture",
                artifacts={
                    "design_document": "Component architecture with 3 services...",
                    "component_diagram": "diagram_data"
                },
                metadata={
                    "duration": 2.3,
                    "tokens_used": 245,
                    "components_identified": 3
                }
            )

        Phase with next phase transition::

            result = PhaseResult(
                phase_name="specification",
                artifacts={"spec_document": "Requirements analysis..."},
                next_phase="architecture",
                metadata={"session_id": "sparc-123"}
            )

        Minimal phase result::

            result = PhaseResult(phase_name="completion")

    Note:
        PhaseResult instances are immutable after creation. Any attempt to modify
        attributes will raise AttributeError. This ensures data integrity and
        prevents accidental corruption in multi-threaded environments.
    """

    phase_name: str
    artifacts: dict[str, Any] = field(default_factory=dict)
    next_phase: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SessionContext:
    """Immutable context container for SPARC orchestration sessions.

    Maintains all state and accumulated artifacts for a complete SPARC workflow
    session, from initial specification through final integration. Provides the
    foundation for stateful orchestration while maintaining immutability for
    thread-safety and audit trails.

    The session context serves as the primary data structure passed between
    phases, containing both the original task definition and all artifacts
    produced during execution. This enables each phase to access previous
    work while maintaining clear data lineage.

    Attributes:
        session_id: Unique identifier for this orchestration session.
                   Used for logging, debugging, and correlating related operations
                   across distributed components. Should be URL-safe and human-readable.
        task: The original high-level task description provided by the user.
             Serves as the primary specification for what the session should accomplish.
             Remains constant throughout the session for reference and validation.
        artifacts: Dictionary of named artifacts produced during session execution.
                  Keys are typically phase names or artifact types (e.g., 'specification',
                  'architecture', 'code', 'tests'). Values can be any serializable data
                  including strings, dicts, lists, or complex nested structures.
                  Defaults to empty dict if not provided.
        metadata: Session-level metadata and execution context as key-value pairs.
                 Common keys include 'start_time', 'user_id', 'workflow_version',
                 'environment', 'resource_limits'. Used for monitoring, debugging,
                 and session management. Defaults to empty dict if not provided.

    Examples:
        Creating a new session context::

            context = SessionContext(
                session_id="sparc-auth-implementation-20240101",
                task="Implement JWT-based user authentication with role-based access control",
                metadata={
                    "start_time": "2024-01-01T10:00:00Z",
                    "user_id": "developer123",
                    "priority": "high"
                }
            )

        Session with accumulated artifacts::

            context = SessionContext(
                session_id="sparc-api-design-456",
                task="Design REST API for inventory management",
                artifacts={
                    "specification": "Detailed API specification with endpoints...",
                    "architecture": "Component diagram and data flow...",
                    "openapi_spec": {"openapi": "3.0.0", "info": {...}}
                },
                metadata={
                    "phases_completed": ["specification", "architecture"],
                    "total_duration": 145.7,
                    "last_updated": "2024-01-01T10:15:00Z"
                }
            )

        Minimal session context::

            context = SessionContext(
                session_id="test-session-001",
                task="Simple hello world implementation"
            )

    Note:
        SessionContext instances are immutable after creation. To add artifacts
        or update metadata during session progression, create new instances with
        the updated data. This immutability ensures data integrity and enables
        safe concurrent access in multi-threaded orchestration environments.

        The artifacts dict should contain serializable data only to support
        session persistence and recovery in homelab environments where reliability
        is critical for long-running automation tasks.
    """

    session_id: str
    task: str
    artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkflowResult:
    """Immutable result container for complete SPARC workflow execution.

    Represents the complete outcome of executing a full SPARC methodology workflow,
    from initial task specification through final integration. Contains comprehensive
    information about execution status, completed phases, generated artifacts,
    and detailed metadata for debugging and monitoring.

    Following SOLID principles with Single Responsibility for workflow result
    representation and immutability for thread-safety in concurrent orchestration
    environments.

    Attributes:
        success: Boolean indicating whether the entire workflow completed successfully.
               True if all phases executed without fatal errors, False if workflow
               failed or was aborted due to unrecoverable errors.
        task: The original high-level task description that initiated the workflow.
             Preserved for reference and correlation with workflow outcomes.
        phases_completed: List of PhaseResult objects for each successfully executed
                         phase in chronological order. Provides complete audit trail
                         of workflow progression and phase-specific outcomes.
        artifacts: Dictionary of final artifacts produced by the workflow execution.
                  Contains the accumulated and refined outputs from all phases,
                  typically including specification documents, architecture designs,
                  implementation code, test suites, and integration instructions.
        error: Optional error message if workflow failed. Contains human-readable
              description of the failure cause and context for debugging. None
              if workflow completed successfully.
        metadata: Workflow-level metadata and execution metrics as key-value pairs.
                 Common keys include 'total_duration', 'start_time', 'end_time',
                 'session_id', 'phases_attempted', 'resource_usage', 'quality_metrics'.
                 Defaults to empty dict if not provided.

    Examples:
        Successful workflow completion::

            result = WorkflowResult(
                success=True,
                task="Implement user authentication with JWT tokens",
                phases_completed=[
                    PhaseResult(phase_name="specification", artifacts={...}),
                    PhaseResult(phase_name="architecture", artifacts={...}),
                    PhaseResult(phase_name="completion", artifacts={...})
                ],
                artifacts={
                    "specification_document": "Detailed auth requirements...",
                    "architecture_design": "Component diagram and API design...",
                    "implementation_code": "Complete JWT authentication system...",
                    "test_suite": "Comprehensive authentication tests...",
                    "deployment_guide": "Instructions for homelab deployment..."
                },
                metadata={
                    "total_duration": 287.3,
                    "start_time": "2024-01-01T10:00:00Z",
                    "end_time": "2024-01-01T10:04:47Z",
                    "session_id": "sparc-auth-20240101",
                    "phases_attempted": 3,
                    "quality_score": 0.94
                }
            )

        Failed workflow with error information::

            result = WorkflowResult(
                success=False,
                task="Complex distributed system implementation",
                phases_completed=[
                    PhaseResult(phase_name="specification", artifacts={...}),
                    PhaseResult(phase_name="architecture", artifacts={...})
                ],
                artifacts={
                    "specification_document": "Requirements analysis...",
                    "architecture_design": "Partial system design..."
                },
                error="Architecture phase failed: insufficient system complexity analysis",
                metadata={
                    "total_duration": 156.8,
                    "failure_phase": "architecture",
                    "error_code": "ARCH_001",
                    "retry_possible": True
                }
            )

        Minimal workflow result::

            result = WorkflowResult(
                success=True,
                task="Simple hello world implementation",
                phases_completed=[
                    PhaseResult(phase_name="completion", artifacts={"code": "print('Hello')"})
                ]
            )

    Note:
        WorkflowResult instances are immutable after creation. Any attempt to modify
        attributes will raise AttributeError. This ensures data integrity and enables
        safe concurrent access in multi-threaded orchestration environments.

        The phases_completed list provides a complete audit trail of workflow execution,
        enabling detailed analysis of workflow performance, phase transition patterns,
        and artifact evolution throughout the SPARC methodology application.

        For homelab environments, the metadata should include resource usage information
        to support capacity planning and performance optimization of orchestration
        workflows under resource constraints.
    """

    success: bool
    task: str
    phases_completed: list["PhaseResult"] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
