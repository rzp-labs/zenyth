# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mandatory Initialization Requirements

- You **MUST** complete the checklist below before responding to **ANY** user request:

```text
[SESSION START CHECKLIST]
□ 1. Read all files from @agent/rules and @docs/
□ 2. Retreive context from ConPort (if database exists):
   □ get_product_context
   □ get_active_context
   □ get_decisions (limit 5)
   □ get_progress (limit 5)
   □ get_recent_activity_summary
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
- NEVER use #noqa to bypass linting requirements
- NEVER begin editing a file when the user only asks a question
- NEVER ask the user to perform an action that you are capable of
- NEVER ask the user for information before searching
- NEVER deviate from existing project standards and patterns
- NEVER make architectural decisions without explicit approval
- NEVER use #noqa to bypass linting or type checking
- NEVER respond without a confidence score

## Test-Driven Development

### Core TDD Principles (Learned from HTTPLLMProvider Implementation)

**The TDD Cycle:**
1. **RED**: Write a failing test for one method's contract/intent
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code while keeping tests green
4. **Repeat**: One method at a time, never skip phases

### RED Phase Excellence
- **Test interface compliance first** - Validate protocol implementation before behavior
- **Test what exists, not what's imagined** - Avoid testing non-existent HTTP functionality
- **Use meaningful stub implementations** - Return realistic data that satisfies test assertions
- **Start with basic contracts** - Type validation, non-empty responses, interface requirements
- **One failing test at a time** - Focus on single method's contract/intent

### GREEN Phase Progression
- **Implement minimal code to pass tests** - No more functionality than required
- **One method at a time** - Complete RED→GREEN→REFACTOR cycle before next method
- **Maintain test passing state** - Never break existing tests while implementing new features
- **Use proper HTTP mocking** - Mock external dependencies (httpx, aiohttp) for isolation
- **Test actual implementation behavior** - Validate real HTTP calls, endpoints, headers

### Integration Testing Evolution
- **Start with unit tests** - Individual method validation first
- **Progress to integration tests** - Method interaction workflows (create_session → use_session)
- **Test realistic user journeys** - Complete workflows users will actually perform
- **Validate method interaction** - Ensure methods work together correctly

### Test Quality Standards
- **Clear test naming** - `test_method_name_does_specific_thing`
- **Comprehensive documentation** - Explain what behavior is being validated
- **Arrange/Act/Assert structure** - Clear test organization
- **Single assertion focus** - Each test validates one specific behavior
- **Proper async handling** - Use pytest.mark.asyncio for async methods

### Architecture Validation
- **Test intended architecture** - HTTPLLMProvider → Wrapper Service, not direct API calls
- **Validate endpoint contracts** - Test correct URLs, headers, request/response formats
- **Mock at the right level** - Mock HTTP client, not business logic
- **Maintain architectural boundaries** - Don't test implementation details across layers

### Common Anti-Patterns to Avoid
- **Testing mocks instead of behavior** - Mocking unimplemented functionality
- **Jumping to GREEN phase** - Writing tests for complex HTTP behavior before basic contracts
- **Testing implementation details** - Focus on interface contracts, not internal structure
- **Ignoring test failures** - All tests should pass; failing tests indicate missing implementation
- **Architectural confusion** - Testing wrong endpoints/APIs for the intended architecture

### Exemplary Progression (HTTPLLMProvider Example)

**Step 1: Interface Compliance (RED Phase Start)**
```python
def test_http_provider_implements_llm_interface():
    """Test HTTPLLMProvider implements LLMInterface protocol."""
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    assert isinstance(provider, LLMInterface)
```
*Implementation: Minimal class with `pass` methods, just enough to satisfy protocol*

**Step 2: Basic Method Behavior (Single Method Focus)**
```python
@pytest.mark.asyncio
async def test_http_provider_generate_returns_string():
    """Test generate method returns actual content rather than empty string."""
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    result = await provider.generate("Hello, world!")
    assert isinstance(result, str)
    assert len(result) > 0
```
*Implementation: `return "test response"` - minimal to pass test*

**Step 3: Constructor Contracts (Edge Cases)**
```python
def test_http_provider_init_requires_base_url():
    """Test HTTPLLMProvider requires base_url for initialization."""
    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        HTTPLLMProvider()  # Should fail without base_url

def test_http_provider_normalizes_base_url():
    """Test HTTPLLMProvider removes trailing slashes from base URL."""
    provider = HTTPLLMProvider(base_url="http://localhost:3001/")
    assert provider.base_url == "http://localhost:3001"
```
*Implementation: `def __init__(self, base_url: str): self.base_url = base_url.rstrip("/")`*

**Step 4: Structured Responses (LLMResponse Contract)**
```python
@pytest.mark.asyncio
async def test_http_provider_complete_chat_returns_llm_response():
    """Test complete_chat returns proper LLMResponse with content and metadata."""
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    response = await provider.complete_chat("What is 2+2?")

    assert isinstance(response, LLMResponse)
    assert isinstance(response.content, str)
    assert len(response.content) > 0
    assert isinstance(response.metadata, dict)
```
*Implementation: `return LLMResponse(content="4", metadata={"model": "test"})`*

**Step 5: Session Management (Integration Testing)**
```python
@pytest.mark.asyncio
async def test_http_provider_complete_chat_with_session():
    """Test session workflow: create session then use it for chat."""
    provider = HTTPLLMProvider(base_url="http://localhost:3001")
    session_id = await provider.create_session()  # Integration step 1
    response = await provider.complete_chat_with_session(session_id, "What is 2+2?")  # Integration step 2

    assert isinstance(response, LLMResponse)
    assert isinstance(response.content, str)
    assert len(response.content) > 0
```
*Implementation: Session methods with meaningful stubs that maintain session context*

**Step 6: Complete Interface Coverage (Methodical Expansion)**
```python
# Added systematically, one test per method:
async def test_http_provider_get_session_history()
async def test_http_provider_fork_session()
async def test_http_provider_revert_session()
async def test_http_provider_get_session_metadata()
async def test_http_provider_stream_chat()
```
*Implementation: Each method implemented with minimal but realistic stub responses*

**Step 7: HTTP Implementation (GREEN Phase Transition)**
```python
# New file: test_http_llm_provider_http.py
@pytest.mark.asyncio
async def test_generate_makes_http_post_request():
    """Test generate method makes HTTP POST request to correct endpoint."""
    provider = HTTPLLMProvider(base_url="http://localhost:3001")

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = Mock(status_code=200, json=Mock(return_value={"content": "response"}))
        mock_client.post.return_value = mock_response

        result = await provider.generate("Test prompt")

        # Validate exact HTTP behavior
        mock_client.post.assert_called_once_with(
            "http://localhost:3001/v1/completions",
            json={"prompt": "Test prompt", "temperature": 0.7},
            headers={"Content-Type": "application/json"}
        )
```
*Implementation: Replace stubs with actual httpx HTTP calls*

**Key Progression Insights:**
- **Test evolution**: `isinstance` → return types → content validation → HTTP calls
- **Implementation evolution**: `pass` → hardcoded returns → parameter handling → HTTP client
- **Incremental complexity**: Interface → method → constructor → integration → HTTP
- **Architectural clarity**: Tests drove the base_url → wrapper service design decision
- **Foundation first**: 12 tests providing complete interface coverage before HTTP implementation

### Test Coverage Evolution
- **Foundation first** - Interface compliance and basic behavior
- **Core functionality** - Primary methods (generate, complete_chat)
- **Advanced features** - Session management, streaming, forking
- **Edge cases** - URL normalization, error handling, empty inputs
- **Integration scenarios** - Multi-method workflows and realistic usage

## Important Constraints

- Maintain interface contracts for all abstractions
- Use dependency injection for all components
- Implement new phases as plugins, not modifications
- Security scanning with Trivy after dependency changes

### Listen to the Guardrails

**Key Principle**: SOLID principles and type checking are guides us toward better design, not hindrances to bypass.

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
- Coverage target with HTML reports

## Configuration

- `pyproject.toml`: Main project configuration with strict typing and quality tools - uses UV
- Python 3.11+ required
- Line length: 100 characters (Black and Ruff)
- Strict mypy configuration enabled
