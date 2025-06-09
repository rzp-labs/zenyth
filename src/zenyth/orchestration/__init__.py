"""SPARC orchestration components for workflow management.

This module provides the core orchestration system that coordinates SPARC workflow
execution across multiple phases. The orchestrator manages phase transitions,
session state, and integrates with LLM providers and tool registries following
SOLID principles and dependency injection patterns.

Available Classes:
    SPARCOrchestrator: Main workflow orchestration coordinator

Examples:
    Basic orchestrator usage::

        orchestrator = SPARCOrchestrator(
            llm_provider=claude_provider,
            tool_registry=mcp_registry,
            state_manager=session_manager
        )
        result = await orchestrator.execute("Create user authentication system")
"""

from .orchestrator import SPARCOrchestrator

__all__ = ["SPARCOrchestrator"]
