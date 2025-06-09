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
from typing import Any


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
        success: Whether the phase execution completed successfully without errors.
                Used for workflow control and error handling decisions.
        output: The primary textual output produced by the phase execution.
               Contains generated content, analysis results, or completion messages.
               Never None - empty string indicates no output produced.
        error: Optional error message if phase execution failed or encountered issues.
              None indicates successful execution. When present, contains detailed
              error information for debugging and user feedback.
        metadata: Additional execution context and metrics as key-value pairs.
                 Common keys include 'duration', 'tokens_used', 'tool_calls',
                 'timestamp', 'phase_name'. Defaults to empty dict if not provided.

    Examples:
        Successful phase execution::

            result = PhaseResult(
                success=True,
                output="Architecture design completed with 3 components",
                metadata={
                    "duration": 2.3,
                    "tokens_used": 245,
                    "components_identified": 3
                }
            )

        Failed phase execution::

            result = PhaseResult(
                success=False,
                output="",
                error="Invalid specification format: missing required sections",
                metadata={"attempted_at": "2024-01-01T10:30:00Z"}
            )

        Minimal successful result::

            result = PhaseResult(success=True, output="Task completed")

    Note:
        PhaseResult instances are immutable after creation. Any attempt to modify
        attributes will raise AttributeError. This ensures data integrity and
        prevents accidental corruption in multi-threaded environments.
    """

    success: bool
    output: str
    error: str | None = None
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
