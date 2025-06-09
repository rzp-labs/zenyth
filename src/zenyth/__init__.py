"""Zenyth: SPARC Orchestration System.

A sophisticated orchestration system that combines mcp-agent, Claude Code SDK,
and the SPARC methodology (Specification, Pseudocode, Architecture, Refinement,
Completion) with additional validation and integration phases for homelab automation.

Key Components:
- Intelligence Layer: Claude Code SDK for LLM reasoning
- Orchestration Layer: mcp-agent for workflow coordination
- Methodology Layer: SPARC configuration and phase management
- Tool Layer: Serena MCP and other tools with phase-based filtering

Architecture:
- Deterministic phase transitions with intelligent execution
- Session-based context management
- Tool isolation per SPARC phase
- Homelab-optimized for resource constraints and graceful degradation
"""

__version__ = "0.1.0"
__author__ = "rzp labs"
__email__ = "engineering@rzp-labs.com"

# Core imports for public API
from .models import (
    SPARCPhase,
    PhaseTransitionTrigger,
    ToolPermission,
    PhaseConfig,
    PhaseResult,
    SessionContext,
    WorkflowConfig,
    OrchestrationMetrics,
)

__all__ = [
    "SPARCPhase",
    "PhaseTransitionTrigger",
    "ToolPermission",
    "PhaseConfig",
    "PhaseResult",
    "SessionContext",
    "WorkflowConfig",
    "OrchestrationMetrics",
]
