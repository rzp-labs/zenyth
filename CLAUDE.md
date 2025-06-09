# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mandatory Initialization Requirements

**[CRITICAL]**

- You **MUST** use `serena` for all file system operations
- You **MUST** read all lines when viewing or editing files
- You **MUST** import all files from `@agent/rules` into your context
- You **MUST** complete the checklist below before responding to **ANY** user request:

```text
[SESSION START CHECKLIST]
□ 1. Import all content from /Users/stephen/Projects/rzp-labs/zenyth/agent/rules
□ 2. Determine and declare active mode
□ 3. Initialize ConPort (if database exists):
   □ get_product_context
   □ get_active_context
   □ get_decisions (limit 5)
   □ get_progress (limit 5)
   □ get_recent_activity_summary
□ 4. Display initialization status
□ 5. State current mode and applicable rules
```

**First message format:**

```text
[SESSION INITIALIZED]
Status: [CONPORT_ACTIVE/INACTIVE]
Mode: [<MODE>]

Context loaded: [Summary of loaded context]

Ready to assist with your request.
```

## Agent Rules and Communication

> **THE USER WILL BE VERY SAD AND FRUSTRATED IF YOU DO NOT FOLLOW THESE RULES**

### [ALWAYS]

- ALWAYS follow [SOLID principles](/Users/stephen/Projects/rzp-labs/zenyth/agent/rules/SOLID_PRINCIPLES.md)
- ALWAYS consider the impact on other components before making changes
- ALWAYS check for existing utilities/helpers before creating new ones
- ALWAYS form your tool use using the XML format specified for each tool
- ALWAYS use <thinking> tags for every tool call or response
- ALWAYS remove temporary files when no longer needed
- ALWAYS include Actions/Expected/Actual in EVERY `ConPort` log entry

### [NEVER]

- NEVER ignore the user
- NEVER sacrifice accuracy
- NEVER responde without a confidence score
- NEVER begin editing a file before answering the user's question
- NEVER ask the user to perform an action that you are capable of
- NEVER ask the user for information before searching
- NEVER deviate from existing project standards and patterns
- NEVER make architectural decisions without explicit approval

### ConPort Integration

**Workspace ID:** `/Users/stephen/Projects/rzp-labs/zenyth`

**ConPort Logging Requirements** - Every ConPort log entry MUST include:

1. **Actions Performed**: Detailed description of what was done
2. **Expected Result**: What outcome was anticipated
3. **Actual Result**: What actually happened

**Tool Usage Protocol:**
- Explain intent before calling ConPort operations
- Never mention specific ConPort operation names to user
- Place ALL ConPort MCP tool calls at the very END of response messages
- Wait for results before proceeding with dependent actions

## Project Overview

Zenyth is a SPARC orchestration system that combines mcp-agent, Claude Code, and Serena for homelab automation. It implements a multi-agent architecture where AI systems coordinate through the SPARC methodology (Specification, Pseudocode, Architecture, Refinement, Completion) with additional validation and integration phases.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint with ruff
ruff check src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/

# Run all quality checks
black src/ tests/ && ruff check src/ tests/ && mypy src/ && bandit -r src/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=zenyth --cov-report=html

# Run specific test types
pytest -m "not integration"  # Unit tests only
pytest -m integration        # Integration tests only
pytest -m mcp               # MCP-related tests
pytest -m slow              # Slow tests
```

### CLI Usage
```bash
# Main entry point
zenyth --help

# Run workflow
zenyth workflow run --config workflow.yaml
```

## Architecture

### Core Components

- **SPARC Phases**: Defined in `src/models/__init__.py` with strict enum types for phases (specification, pseudocode, architecture, refinement, completion, validation, integration)
- **Plugin Architecture**: Phases implemented as handlers following the PhaseHandler interface, allowing extension without modification
- **Dependency Injection**: High-level orchestration depends on abstractions (ILLMProvider, IToolRegistry, IStateManager)
- **Session Management**: Context preserved across phase transitions with selective context loading per phase

### Key Patterns

- **SOLID Principles**: Extensively documented in `agent/rules/SOLID_PRINCIPLES.md` - critical for maintainability
- **Interface Segregation**: Separate interfaces for phase execution, state management, and tool registry
- **Strategy Pattern**: Tool selection strategies for different environments (restrictive vs permissive)
- **Observer Pattern**: Workflow event handling for metrics and monitoring

### Phase Context Management

Phases receive only relevant context to optimize memory usage:
- Architecture phase gets specification artifacts
- Refinement phase gets architecture and completion artifacts
- Global artifacts available to all phases

### Tool Integration

- MCP (Model Context Protocol) tools with permission levels (read_only, write, execute, none)
- Tool selection strategies based on phase and environment
- Codacy integration for automatic code analysis after edits

## Testing Strategy

- Interface-based testing for all PhaseHandler implementations
- Dependency injection for test isolation
- Separate markers for integration, slow, and MCP tests
- Coverage target with HTML reports

## Configuration

- `pyproject.toml`: Main project configuration with strict typing and quality tools
- Line length: 100 characters (Black and Ruff)
- Python 3.10+ required
- Strict mypy configuration enabled

## Important Constraints

- Follow SOLID principles rigorously (see [@agent/rules/SOLID_PRINCIPLES.md](@agent/rules/SOLID_PRINCIPLES.md))
- Maintain interface contracts for all abstractions
- Use dependency injection for all components
- Implement new phases as plugins, not modifications
- Security scanning with Trivy after dependency changes
