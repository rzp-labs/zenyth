#!/usr/bin/env python3
"""SPARC Specification Phase Configuration.

Defines the configuration for the specification phase of the SPARC methodology.
This phase focuses on requirements analysis and detailed specification creation.
"""

from zenyth.models import SPARCPhase, ToolPermission

# Phase identification
name = SPARCPhase.SPECIFICATION
description = "Analyze requirements and create detailed specifications"

# Phase instructions for the LLM agent
instructions = """
You are in the SPECIFICATION phase of the SPARC methodology.

Your objectives:
1. Analyze the user's requirements thoroughly
2. Create detailed technical specifications
3. Define acceptance criteria and success metrics
4. Identify system boundaries and constraints
5. Document API contracts and data models

Focus on understanding WHAT needs to be built, not HOW to build it.
Ask clarifying questions if requirements are ambiguous.
"""

# Tool access configuration
allowed_tools = [
    "find_symbol",
    "get_symbols_overview", 
    "read_file",
    "search_for_pattern",
    "list_dir",
    "write_memory",
    "get_decisions",
    "get_custom_data",
    "semantic_search_conport"
]

forbidden_tools = [
    "replace_symbol_body",
    "create_text_file",
    "insert_after_symbol",
    "insert_before_symbol",
    "execute_shell_command"
]

# Required artifacts this phase must produce
required_artifacts = [
    "specification.md",
    "api_contracts.json", 
    "acceptance_criteria.md",
    "system_boundaries.md"
]

# Completion criteria
completion_criteria = {
    "requirements_documented": True,
    "acceptance_criteria_defined": True,
    "system_boundaries_clear": True,
    "api_contracts_specified": True,
    "stakeholder_approval": False  # Optional for automated workflows
}

# Phase-specific configuration
timeout_seconds = 1800  # 30 minutes max for specification
max_retries = 2
cache_responses = True
allow_human_override = True

# Tool permission overrides
tool_permissions = {
    "read_file": ToolPermission.READ_ONLY,
    "find_symbol": ToolPermission.READ_ONLY,
    "search_for_pattern": ToolPermission.READ_ONLY,
    "write_memory": ToolPermission.WRITE,
    "log_decision": ToolPermission.WRITE,
    "log_progress": ToolPermission.WRITE
}

# Phase validation rules
validation_rules = {
    "min_artifacts": 3,
    "max_tokens": 50000,
    "require_approval": False
}

# Homelab-specific optimizations
homelab_config = {
    "memory_limit_mb": 512,
    "cpu_priority": "normal",
    "cache_ttl_hours": 24,
    "enable_checkpointing": True
}