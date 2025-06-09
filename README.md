# Zenyth

> *A sophisticated orchestration system combining mcp-agent, Claude Code, and Serena for structured AI-assisted development*

Zenyth implements a **decoupled orchestration architecture** that separates intelligent work execution from workflow management, enabling transparent, debuggable AI-assisted development workflows through the SPARC methodology.

## 🏗️ Architecture

Based on extensive homelab practitioner research, Zenyth implements four distinct layers:

### 1. Intelligence Layer (Claude Code SDK)
- Provides LLM reasoning for complex decisions within phases
- Direct SDK integration without abstraction overhead
- Intelligence focused on creative work, not orchestration logic

### 2. Orchestration Layer (mcp-agent)
- Manages workflow execution and agent coordination
- Hub-and-spoke pattern with phase-specific agents
- **Key Innovation**: Deterministic routing with intelligent execution

### 3. Methodology Layer (SPARC Configuration)
- Defines phases, transitions, and validation rules
- YAML-based configuration enables methodology experimentation
- Supports standard SPARC phases plus validation and integration

### 4. Tool Layer (Serena MCP + Others)
- Semantic code operations through MCP protocol
- Phase-based tool filtering for security and focus
- Standardized tool access across different providers

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Basic Usage

```bash
# Start a SPARC workflow
zenyth workflow run --task "Create user authentication system"

# Execute specific phase
zenyth execute-phase specification "Define API endpoints"

# Monitor workflow progress
zenyth status --session-id <session-id>
```

## 🧠 SPARC Methodology

Zenyth implements the complete SPARC methodology with intelligent phase transitions:

1. **Specification**: Analyze requirements and create detailed specifications
2. **Pseudocode**: Develop algorithmic approaches (for complex logic)
3. **Architecture**: Design system structure and component relationships
4. **Refinement**: Optimize and refine the implementation
5. **Completion**: Final implementation and validation
6. **Validation**: Comprehensive testing and quality assurance
7. **Integration**: System integration and deployment preparation

### Phase-Specific Tool Access

- **Specification**: Read-only tools (`find_symbol`, `get_overview`, `read_file`)
- **Architecture**: Design tools (diagram creation, dependency analysis)
- **Completion**: Write tools (`replace_symbol`, `create_file`, `execute_shell`)

## 🛠️ Development

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
```

### Project Structure

```
zenyth/
├── .serena/                 # Serena project configuration
├── sparc/                   # SPARC methodology configuration
│   ├── methodology.yaml     # Phase definitions
│   ├── prompts/            # Phase-specific prompts
│   └── transitions.yaml    # Transition rules
├── src/
│   ├── agents/             # Phase-specific agents
│   ├── llm/                # LLM integrations
│   ├── mcp/                # MCP tool integrations
│   ├── models/             # Pydantic data models
│   └── utils/              # Utilities
├── tests/                  # Test suite
├── examples/               # Example workflows
└── docs/                   # Documentation
```

## 🏠 Homelab Deployment

Zenyth is designed for resource-constrained homelab environments:

### Resource Optimizations
- **Lazy Loading**: Phase agents loaded only when needed
- **Response Caching**: Cache deterministic LLM operations
- **Memory Efficiency**: Stream large outputs, avoid buffering
- **Graceful Degradation**: Fallback strategies for service failures

### Production Configuration
```bash
# Systemd service for resilience
sudo systemctl enable zenyth-orchestrator

# PostgreSQL for session storage
export ZENYTH_DB_URL="postgresql://user:pass@localhost/zenyth"

# Prometheus metrics
export ZENYTH_METRICS_ENABLED=true
```

## 🔧 Configuration

### SPARC Methodology Configuration

```yaml
# sparc/methodology.yaml
phases:
  specification:
    description: "Analyze requirements and create detailed specifications"
    allowed_tools:
      - find_symbol
      - get_symbols_overview
      - read_file
    required_artifacts:
      - specification.md
      - api_contracts.json
    completion_criteria:
      - all_requirements_documented
      - acceptance_criteria_defined
```

### Phase Transitions

```yaml
# sparc/transitions.yaml
transitions:
  specification:
    to_architecture:
      conditions:
        - specification_complete: true
        - system_boundaries_defined: true
    to_pseudocode:
      conditions:
        - specification_complete: true
        - algorithmic_complexity_high: true
```

## 📊 Monitoring and Debugging

### Logging
```bash
# Debug logging
export ZENYTH_LOG_LEVEL=DEBUG

# Structured logging for analysis
tail -f ~/.zenyth/logs/orchestrator.json
```

### Performance Metrics
- Phase execution times
- LLM/tool call counts
- Memory and CPU usage
- Cache hit/miss ratios

### Session Management
- Automatic session persistence
- Recovery from phase failures
- Context preservation across restarts

## 🧪 Testing Strategy

### Unit Tests
- Phase transition logic (deterministic, fast)
- Tool filtering rules
- Context preservation

### Integration Tests
- Full workflow execution
- MCP server communication
- Session management

### Homelab-Specific Tests
- Resource constraint simulation
- Service failure scenarios
- Recovery mechanisms

## 🤝 Contributing

1. Follow SOLID principles rigorously (see `docs/SOLID_PRINCIPLES.md`)
2. Maintain interface contracts for all abstractions
3. Use dependency injection for all components
4. Implement new phases as plugins, not modifications
5. Run quality checks before committing

### Code Style
- **Line Length**: 100 characters (Black formatting)
- **Type Hints**: Complete type annotations required
- **Docstrings**: Google-style for all public methods
- **Async First**: Prefer async/await for I/O operations

## 🤖 AI Agent Integration

Zenyth includes comprehensive AI agent configuration for consistent, high-quality assistance:

### Agent Configuration
- **Mandatory Initialization**: Session start checklist and ConPort integration
- **Communication Rules**: Direct, technical communication standards
- **Task Planning**: Dual-tool approach with planning and tracking
- **Research Methodology**: Structured approach to knowledge gaps

### Key Features
- **ConPort Integration**: Persistent project memory and context management
- **Session Management**: Proper initialization and context refresh protocols
- **Quality Standards**: Comprehensive logging and validation requirements
- **Tool Orchestration**: Phase-specific tool access aligned with SPARC methodology

See [`docs/AGENT_GUIDE.md`](docs/AGENT_GUIDE.md) for complete agent integration documentation.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built on insights from 147 homelab orchestration deployments and extensive practitioner research. Special thanks to the homelab community for sharing deployment patterns and optimization strategies.

---

*Zenyth: Transparent, debuggable AI orchestration for the homelab era*