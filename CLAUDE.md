# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mandatory Initialization Requirements

**[CRITICAL]**

- You **MUST** use `serena` for all file system operations

- You **MUST** import all files from `@agent/rules` into your context
- You **MUST** complete the checklist below before responding to **ANY** user request:

```text
[SESSION START CHECKLIST]
□ 1. Import all content from @agent/rules and @docs/
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

### [ALWAYS]

- ALWAYS follow [SOLID principles](/Users/stephen/Projects/rzp-labs/zenyth/agent/rules/SOLID_PRINCIPLES.md)
- ALWAYS consider the impact on other components before making changes
- ALWAYS check for existing utilities/helpers before creating new ones
- ALWAYS read all lines when viewing or editing files
- ALWAYS form your tool use using the XML format specified for each tool
- ALWAYS use <thinking> tags for every tool call or response
- ALWAYS remove temporary files when no longer needed
- ALWAYS include Actions/Expected/Actual in EVERY `ConPort` log entry

### [NEVER]

- NEVER sacrifice accuracy
- NEVER begin editing a file when the user only asks a question
- NEVER ask the user to perform an action that you are capable of
- NEVER ask the user for information before searching
- NEVER deviate from existing project standards and patterns
- NEVER make architectural decisions without explicit approval
- NEVER use #noqa to bypass linting or type checking
- NEVER respond without a confidence score

## Important Constraints

- Follow SOLID principles rigorously (see [@agent/rules/SOLID_PRINCIPLES.md](@agent/rules/SOLID_PRINCIPLES.md))
- Maintain interface contracts for all abstractions
- Use dependency injection for all components
- Implement new phases as plugins, not modifications
- Security scanning with Trivy after dependency changes

### Listen to the Guardrails

**Key Principle**: SOLID principles and type checking are guides us toward better design, not hindrances to bypass.

**Required Reading:**

- [docs/balancing-semantic-clarity.md](docs/balancing-semantic-clarity.md)
- [docs/challenging-rules-reference-guide.md](docs/challenging-rules-reference-guide.md)
- [docs/structured-validation.md](docs/structured-validation.md)

**What This Means:**
- When linting rules warn "method could be static" → Consider if the method truly needs instance state
- When type checker complains about `None` values → Fix the types at the source, don't mask with workarounds
- When exceptions feel awkward → Use Python's natural exception handling, don't create artificial `NoReturn` helpers
- When code feels complex → Simplify the design rather than adding annotations to work around complexity

**Anti-patterns to Avoid:**
- Adding artificial instance variables just to avoid "could be static" warnings
- Using `NoReturn` annotations to bypass proper exception handling
- Creating helper methods that only exist to satisfy linting rules
- Fighting the type system instead of listening to what it's telling us

**Successful Pattern:**
- Listen to what tools are telling us about our design
- Fix root causes rather than symptoms
- Work with the language and tools, not against them
- Let SOLID principles emerge naturally from good design choices

### ConPort Integration

**Workspace ID:** `/Users/stephen/Projects/rzp-labs/zenyth`

**ConPort Logging Requirements** - Every ConPort log entry MUST include:

1. **Actions Performed**: Detailed description of what was done
2. **Expected Result**: What outcome was anticipated
3. **Actual Result**: What actually happened

**Tool Usage Protocol:**
- Explain intent before calling file operations
- Place ALL MCP tool calls at the very END of response messages
- Wait for results before proceeding with dependent actions

## Project Overview

Zenyth is a SPARC orchestration system that combines mcp-agent, Claude Code, and Serena for homelab automation. It implements a multi-agent architecture where AI systems coordinate through the SPARC methodology (Specification, Pseudocode, Architecture, Refinement, Completion) with additional validation and integration phases.

## Development Commands

### Environment Setup
```bash
# Install dependencies
source .venv/bin/activate && pip install -e ".[dev]"

# Install pre-commit hooks
source .venv/bin/activate && pre-commit install
```

### Code Quality
```bash
# Format code
source .venv/bin/activate && black src/ tests/

# Lint with ruff
source .venv/bin/activate && ruff check src/ tests/

# Type checking
source .venv/bin/activate && mypy src/

# Security scanning
source .venv/bin/activate && bandit -r src/

# Run all quality checks
source .venv/bin/activate && black src/ tests/ && ruff check src/ tests/ && mypy src/ && bandit -r src/
```
### Testing
```bash
# Run all tests
source .venv/bin/activate && pytest

# Run with coverage
source .venv/bin/activate && pytest --cov=zenyth --cov-report=html

# Run specific test types
source .venv/bin/activate && pytest -m "not integration"  # Unit tests only
source .venv/bin/activate && pytest -m integration        # Integration tests only
source .venv/bin/activate && pytest -m mcp               # MCP-related tests
source .venv/bin/activate && pytest -m slow              # Slow tests
```

### CLI Usage
```bash
# Main entry point
source .venv/bin/activate && zenyth --help

# Run workflow
source .venv/bin/activate && zenyth workflow run --config workflow.yaml
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

- `pyproject.toml`: Main project configuration with strict typing and quality tools - uses UV
- Python 3.11+ required
- Line length: 100 characters (Black and Ruff)
- Strict mypy configuration enabled
