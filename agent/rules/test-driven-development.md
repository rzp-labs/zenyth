# Test-Driven Development

## Core TDD Principles (Learned from HTTPLLMProvider Implementation)

**The TDD Cycle:**
1. **RED**: Write a failing test for one method's contract/intent
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code while keeping tests green
4. **Repeat**: One method at a time, never skip phases

## RED Phase Excellence
- **Test interface compliance first** - Validate protocol implementation before behavior
- **Test what exists, not what's imagined** - Avoid testing non-existent HTTP functionality
- **Use meaningful stub implementations** - Return realistic data that satisfies test assertions
- **Start with basic contracts** - Type validation, non-empty responses, interface requirements
- **One failing test at a time** - Focus on single method's contract/intent

## GREEN Phase Progression
- **Implement minimal code to pass tests** - No more functionality than required
- **One method at a time** - Complete RED→GREEN→REFACTOR cycle before next method
- **Maintain test passing state** - Never break existing tests while implementing new features
- **Use proper HTTP mocking** - Mock external dependencies (httpx, aiohttp) for isolation
- **Test actual implementation behavior** - Validate real HTTP calls, endpoints, headers

## Integration Testing Evolution
- **Start with unit tests** - Individual method validation first
- **Progress to integration tests** - Method interaction workflows (create_session → use_session)
- **Test realistic user journeys** - Complete workflows users will actually perform
- **Validate method interaction** - Ensure methods work together correctly

## Test Quality Standards
- **Clear test naming** - `test_method_name_does_specific_thing`
- **Comprehensive documentation** - Explain what behavior is being validated
- **Arrange/Act/Assert structure** - Clear test organization
- **Single assertion focus** - Each test validates one specific behavior
- **Proper async handling** - Use pytest.mark.asyncio for async methods

## Architecture Validation
- **Test intended architecture** - HTTPLLMProvider → Wrapper Service, not direct API calls
- **Validate endpoint contracts** - Test correct URLs, headers, request/response formats
- **Mock at the right level** - Mock HTTP client, not business logic
- **Maintain architectural boundaries** - Don't test implementation details across layers

## Common Anti-Patterns to Avoid
- **Testing mocks instead of behavior** - Mocking unimplemented functionality
- **Jumping to GREEN phase** - Writing tests for complex HTTP behavior before basic contracts
- **Testing implementation details** - Focus on interface contracts, not internal structure
- **Ignoring test failures** - All tests should pass; failing tests indicate missing implementation
- **Architectural confusion** - Testing wrong endpoints/APIs for the intended architecture

## Exemplary Progression (HTTPLLMProvider Example)

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

## Test Coverage Evolution
- **Foundation first** - Interface compliance and basic behavior
- **Core functionality** - Primary methods (generate, complete_chat)
- **Advanced features** - Session management, streaming, forking
- **Edge cases** - URL normalization, error handling, empty inputs
- **Integration scenarios** - Multi-method workflows and realistic usage
