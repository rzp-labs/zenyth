"""Core data types for Zenyth."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PhaseResult:
    """Result of a SPARC phase execution."""

    success: bool
    output: str
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SessionContext:
    """Context for a SPARC session."""

    session_id: str
    task: str
    artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
