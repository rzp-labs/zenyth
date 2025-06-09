# SPARC Orchestration Service Implementation Plan

## Executive Summary

This implementation plan details the construction of a SPARC methodology orchestration service using mcp-agent, with direct Claude Code SDK integration and Serena MCP for LSP-powered code operations. The service will demonstrate production-grade orchestration through implementation of the Specification phase, with comprehensive mock testing infrastructure.

## Project Scope Definition

### In Scope
- Core orchestration service using mcp-agent framework
- Direct Claude Code SDK integration (no AI SDK wrapper)
- Python-based SPARC configuration with full type safety
- Mock MCP server infrastructure for unit testing
- Complete implementation of SPARC Specification phase
- Integration with Serena MCP for semantic code operations
- Comprehensive test suite following TDD principles
- SOLID architectural patterns throughout

### Explicitly Out of Scope
- AI SDK provider wrappers or abstractions
- JavaScript/TypeScript implementations
- Full implementation of all SPARC phases (only Specification)
- Custom MCP server development
- Claude API key management (assumes Claude Code SDK handles auth)
- Production deployment configurations
- CI/CD pipeline setup
- Performance optimization beyond functional correctness

## Phase 1: Infrastructure Foundation (Week 1)

### Objectives
Establish the foundational architecture with proper abstractions and dependency injection patterns following SOLID principles.

### Implementation Tasks

#### 1.1 Project Structure Setup
```python
zenyth/
├── .serena/                  # Serena's domain (external)
│   └── memories/            # Created by Serena at runtime
├── sparc_config/            # SPARC methodology assets
│   ├── phases/              # Phase definitions
│   │   ├── specification.py # Typed, testable configs
│   │   ├── architecture.py
│   │   └── ...
│   ├── prompts/             # Prompt templates
│   │   ├── specification.py
│   │   └── ...
│   └── transitions.py       # State machine rules
├── src/
│   └── zenyth/  # Python package
│       ├── __init__.py
│       ├── core/           # SOLID interfaces
│       │   ├── interfaces.py
│       │   └── types.py
│       ├── orchestration/  # mcp-agent integration
│       │   ├── executor.py
│       │   └── factory.py
│       ├── integrations/   # External services
│       │   ├── claude_code.py
│       │   └── serena_mcp.py
│       └── phases/         # Phase implementations
│           ├── base.py
│           └── specification.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── mocks/
└── pyproject.toml
```

#### 1.2 Core Interfaces Definition (TDD: Write Tests First)
```python
# tests/unit/test_interfaces.py
def test_llm_interface_contract():
    """LLM interface must define generate method with proper signature"""
    from zenyth.core.interfaces import LLMInterface

    class TestLLM(LLMInterface):
        async def generate(self, prompt: str, **kwargs) -> str:
            return "test response"

    llm = TestLLM()
    assert hasattr(llm, 'generate')
    assert inspect.iscoroutinefunction(llm.generate)

# src/core/interfaces.py (Implementation after test)
from abc import ABC, abstractmethod
from typing import Protocol, Dict, Any, List

class LLMInterface(Protocol):
    """Interface Segregation: Minimal LLM contract for mcp-agent"""
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text completion from prompt"""
        ...

class PhaseExecutor(ABC):
    """Single Responsibility: Execute one SPARC phase"""
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> PhaseResult:
        """Execute phase with given context"""
        pass

    @abstractmethod
    def validate_preconditions(self, context: Dict[str, Any]) -> bool:
        """Liskov Substitution: All phases must validate preconditions"""
        pass
```

### Expected Outcomes
- Fully typed project structure with 100% mypy coverage
- Abstract interfaces defining contracts for all components
- Test infrastructure ready for TDD development
- Mock implementations for external dependencies

### Success Metrics
- [ ] All interfaces have corresponding test contracts
- [ ] mypy --strict passes with no errors
- [ ] Project structure follows Python packaging best practices
- [ ] Mock infrastructure can simulate MCP server responses

## Phase 2: SPARC Configuration System (Week 2)

### Objectives
Implement a type-safe, testable configuration system for SPARC methodology phases.

### Implementation Tasks

#### 2.1 SPARC Phase Configuration (TDD First)
```python
# tests/unit/test_sparc_config.py
def test_phase_configuration_validation():
    """Phase configs must have required fields with correct types"""
    from zenyth.config import PhaseConfig

    config = PhaseConfig(
        name="specification",
        role="Specification Writer",
        instructions="Break down requirements into modular components",
        required_tools=["get_symbols_overview", "find_symbol"],
        completion_criteria=["requirements.md exists", "all endpoints documented"],
        next_phases=["pseudocode", "architecture"]
    )

    assert config.validate()
    assert config.get_prompt_template() is not None

# src/config/sparc_methodology.py (Implementation)
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum

class SPARCPhase(Enum):
    """Open/Closed: Extend phases without modifying enum"""
    SPECIFICATION = "specification"
    PSEUDOCODE = "pseudocode"
    ARCHITECTURE = "architecture"
    REFINEMENT = "refinement"
    COMPLETION = "completion"

@dataclass
class PhaseConfig:
    """Immutable phase configuration with validation"""
    name: SPARCPhase
    role: str
    instructions: str
    required_tools: List[str]
    completion_criteria: List[str]
    next_phases: List[SPARCPhase]
    optional_tools: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate configuration on instantiation"""
        if not self.instructions:
            raise ValueError(f"Phase {self.name} must have instructions")
        if not self.required_tools:
            raise ValueError(f"Phase {self.name} must have required tools")
```

#### 2.2 Configuration Validation System
```python
# src/config/validators.py
from typing import Type, TypeVar, Generic
from pydantic import BaseModel, validator

T = TypeVar('T', bound=BaseModel)

class ConfigValidator(Generic[T]):
    """Dependency Inversion: Validator depends on abstraction"""
    def __init__(self, schema: Type[T]):
        self.schema = schema

    def validate(self, data: Dict[str, Any]) -> T:
        """Validate and return typed configuration"""
        return self.schema(**data)

class PromptTemplate(BaseModel):
    """Validates SPARC prompt templates"""
    template: str
    required_variables: Set[str]

    @validator('template')
    def template_has_variables(cls, v, values):
        """Ensure template contains all required variables"""
        required = values.get('required_variables', set())
        for var in required:
            if f"{{{var}}}" not in v:
                raise ValueError(f"Template missing required variable: {var}")
        return v
```

### Expected Outcomes
- Type-safe SPARC configuration system with runtime validation
- Extensible phase definition system following Open/Closed principle
- Comprehensive validation for all configuration aspects
- Clear separation between configuration and implementation

### Success Metrics
- [ ] 100% test coverage for configuration validation
- [ ] All SPARC phases have validated configurations
- [ ] Configuration changes don't require code changes
- [ ] Pydantic validation catches all malformed configs

## Phase 3: Orchestration Core Implementation (Week 3)

### Objectives
Build the core orchestration engine integrating mcp-agent with Claude Code SDK.

### Implementation Tasks

#### 3.1 Claude Code Integration (TDD First)
```python
# tests/unit/test_claude_integration.py
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_claude_code_llm_adapter():
    """Claude Code adapter implements LLMInterface correctly"""
    from zenyth.integrations import ClaudeCodeLLM

    mock_client = Mock()
    mock_client.complete = AsyncMock(return_value=Mock(content="test response"))

    llm = ClaudeCodeLLM(client=mock_client)
    response = await llm.generate("test prompt", temperature=0.7)

    assert response == "test response"
    mock_client.complete.assert_called_once()

# src/integrations/claude_code.py
from zenyth.core.interfaces import LLMInterface
from claude_code import ClaudeClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ClaudeCodeLLM:
    """Adapter pattern: Adapts Claude Code SDK to LLMInterface"""
    def __init__(self, client: Optional[ClaudeClient] = None):
        self.client = client or ClaudeClient()
        self._call_count = 0  # Metrics tracking

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion using Claude Code SDK"""
        try:
            self._call_count += 1
            logger.debug(f"Claude Code call #{self._call_count}: {len(prompt)} chars")

            response = await self.client.complete(
                prompt=prompt,
                max_tokens=kwargs.get('max_tokens', 4096),
                temperature=kwargs.get('temperature', 0.7)
            )

            return response.content
        except Exception as e:
            logger.error(f"Claude Code generation failed: {e}")
            raise
```

#### 3.2 MCP Agent Factory (Dependency Injection)
```python
# src/orchestration/agent_factory.py
from mcp_agent import MCPAgent
from typing import Dict, List
from zenyth.core.interfaces import LLMInterface
from zenyth.config import PhaseConfig

class AgentFactory:
    """Factory pattern: Creates configured mcp-agents per phase"""

    def __init__(self, llm: LLMInterface, tool_registry: 'ToolRegistry'):
        self.llm = llm
        self.tool_registry = tool_registry

    def create_phase_agent(self,
                          phase_config: PhaseConfig,
                          context: Dict[str, Any]) -> MCPAgent:
        """Create agent configured for specific SPARC phase"""

        # Build contextualized instructions
        instructions = self._build_instructions(phase_config, context)

        # Filter tools for this phase
        tools = self.tool_registry.get_tools_for_phase(phase_config.name)

        return MCPAgent(
            name=f"SPARC_{phase_config.name.value}",
            llm=self.llm,
            instructions=instructions,
            tools=tools,
            max_iterations=10,  # Prevent runaway execution
            context_window=8192
        )

    def _build_instructions(self,
                           config: PhaseConfig,
                           context: Dict[str, Any]) -> str:
        """Build phase-specific instructions with context"""
        template = f"""
You are a {config.role} following SPARC methodology.

{config.instructions}

Available tools: {', '.join(config.required_tools)}

Previous context:
{context.get('previous_results', 'No previous context')}

Completion criteria:
{chr(10).join(f"- {c}" for c in config.completion_criteria)}
"""
        return template
```

### Expected Outcomes
- Fully integrated mcp-agent orchestration system
- Clean adapter pattern for Claude Code SDK
- Factory pattern for phase-specific agent creation
- Comprehensive error handling and logging

### Success Metrics
- [ ] All integration points have mock test coverage
- [ ] Claude Code adapter passes LLMInterface contract tests
- [ ] Agent factory creates properly configured agents
- [ ] Error scenarios are handled gracefully

## Phase 4: Mock MCP Server Infrastructure (Week 4)

### Objectives
Build comprehensive mock infrastructure for testing orchestration without external dependencies.

### Implementation Tasks

#### 4.1 Mock MCP Server Implementation
```python
# tests/mocks/mock_mcp_server.py
from typing import Dict, Any, List, Optional
import asyncio
from dataclasses import dataclass
import json

@dataclass
class MockResponse:
    """Structured mock response for MCP operations"""
    success: bool
    data: Any
    error: Optional[str] = None

class MockMCPServer:
    """Mock MCP server for testing orchestration logic"""

    def __init__(self, server_name: str):
        self.server_name = server_name
        self.responses: Dict[str, MockResponse] = {}
        self.call_history: List[Dict[str, Any]] = []
        self._setup_default_responses()

    def _setup_default_responses(self):
        """Configure default responses for common operations"""
        self.responses['get_symbols_overview'] = MockResponse(
            success=True,
            data={
                "src/main.py": [
                    {"name": "Application", "kind": "class", "line": 10},
                    {"name": "main", "kind": "function", "line": 50}
                ]
            }
        )

        self.responses['find_symbol'] = MockResponse(
            success=True,
            data=[{
                "name": "UserService",
                "path": "src/services/user.py",
                "line": 15,
                "kind": "class"
            }]
        )

    async def execute_tool(self, tool_name: str, **params) -> Any:
        """Execute mock tool and return configured response"""
        self.call_history.append({
            "tool": tool_name,
            "params": params,
            "timestamp": asyncio.get_event_loop().time()
        })

        response = self.responses.get(tool_name)
        if not response:
            raise ValueError(f"No mock configured for tool: {tool_name}")

        # Simulate network delay
        await asyncio.sleep(0.1)

        if not response.success:
            raise Exception(response.error)

        return response.data

    def configure_response(self, tool_name: str, response: MockResponse):
        """Configure specific response for testing scenarios"""
        self.responses[tool_name] = response

    def assert_tool_called(self, tool_name: str, times: int = 1):
        """Assertion helper for test verification"""
        calls = [c for c in self.call_history if c["tool"] == tool_name]
        assert len(calls) == times, \
            f"Expected {tool_name} called {times} times, got {len(calls)}"
```

#### 4.2 Mock Claude Code Implementation
```python
# tests/mocks/mock_claude_code.py
class MockClaudeClient:
    """Mock Claude Code client for deterministic testing"""

    def __init__(self):
        self.responses = {}
        self.call_count = 0
        self._setup_default_responses()

    def _setup_default_responses(self):
        """Configure phase-specific responses"""
        self.responses['specification'] = """
Based on my analysis of the codebase:

## Requirements Specification

1. **User Authentication System**
   - RESTful API endpoints for login/logout
   - JWT token-based authentication
   - Role-based access control (RBAC)

2. **Technical Constraints**
   - Must integrate with existing UserService
   - PostgreSQL database backend
   - Redis for session management

3. **Completion Artifacts**
   - Created: requirements.md
   - Created: api_specification.yaml
   - All endpoints documented: ✓
"""

    async def complete(self, prompt: str, **kwargs):
        """Return deterministic response based on prompt content"""
        self.call_count += 1

        # Detect phase from prompt
        if "Specification Writer" in prompt:
            return MockResponse(content=self.responses['specification'])

        return MockResponse(content="Generic mock response")
```

### Expected Outcomes
- Complete mock infrastructure for isolated testing
- Deterministic responses for all SPARC phase operations
- Assertion helpers for behavior verification
- Network delay simulation for realistic testing

### Success Metrics
- [ ] Mock servers support all required MCP operations
- [ ] Tests can configure custom responses for edge cases
- [ ] Call history tracking enables behavior verification
- [ ] Mock infrastructure has its own test coverage

## Phase 5: Specification Phase Implementation (Week 5)

### Objectives
Implement the complete SPARC Specification phase as proof of orchestration functionality.

### Implementation Tasks

#### 5.1 Specification Phase Executor
```python
# tests/integration/test_specification_phase.py
@pytest.mark.asyncio
async def test_specification_phase_execution():
    """Specification phase produces required artifacts"""
    from zenyth.phases import SpecificationPhase

    # Setup mocks
    mock_claude = MockClaudeClient()
    mock_serena = MockMCPServer("serena")

    phase = SpecificationPhase(
        llm=ClaudeCodeLLM(mock_claude),
        mcp_server=mock_serena
    )

    context = {"project_root": "/test/project"}
    result = await phase.execute(context)

    assert result.success
    assert "requirements.md" in result.artifacts
    assert result.next_phase in ["pseudocode", "architecture"]
    mock_serena.assert_tool_called("get_symbols_overview")

# src/phases/specification.py
from zenyth.core.interfaces import PhaseExecutor
from zenyth.core.types import PhaseResult
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SpecificationPhase(PhaseExecutor):
    """SPARC Specification phase implementation"""

    def __init__(self, llm: LLMInterface, mcp_server: MCPServer):
        self.llm = llm
        self.mcp_server = mcp_server
        self.config = self._load_phase_config()

    async def execute(self, context: Dict[str, Any]) -> PhaseResult:
        """Execute specification phase"""
        try:
            # Validate preconditions
            if not self.validate_preconditions(context):
                return PhaseResult(
                    success=False,
                    error="Preconditions not met"
                )

            # Analyze codebase structure
            symbols = await self.mcp_server.execute_tool(
                "get_symbols_overview",
                path=context["project_root"]
            )

            # Generate specification using Claude
            prompt = self._build_specification_prompt(symbols, context)
            specification = await self.llm.generate(prompt)

            # Extract artifacts from response
            artifacts = self._extract_artifacts(specification)

            # Validate completion criteria
            if self._check_completion_criteria(artifacts):
                return PhaseResult(
                    success=True,
                    artifacts=artifacts,
                    next_phase=self._determine_next_phase(artifacts),
                    summary=specification
                )
            else:
                return PhaseResult(
                    success=False,
                    error="Completion criteria not met",
                    artifacts=artifacts
                )

        except Exception as e:
            logger.error(f"Specification phase failed: {e}")
            return PhaseResult(
                success=False,
                error=str(e)
            )

    def validate_preconditions(self, context: Dict[str, Any]) -> bool:
        """Ensure project context is available"""
        return "project_root" in context and context["project_root"]

    def _check_completion_criteria(self, artifacts: Dict[str, Any]) -> bool:
        """Verify all specification requirements are met"""
        required = {"requirements.md", "api_specification.yaml"}
        return required.issubset(artifacts.keys())
```

### Expected Outcomes
- Complete implementation of SPARC Specification phase
- Integration with mcp-agent orchestration
- Artifact generation and validation
- Proper error handling and logging

### Success Metrics
- [ ] Specification phase passes all integration tests
- [ ] Artifacts are correctly generated and validated
- [ ] Phase transitions follow SPARC methodology
- [ ] Error scenarios are handled gracefully

## Phase 6: Integration and End-to-End Testing (Week 6)

### Objectives
Validate the complete orchestration system with comprehensive integration tests.

### Implementation Tasks

#### 6.1 End-to-End Orchestration Test
```python
# tests/integration/test_e2e_orchestration.py
@pytest.mark.asyncio
async def test_full_specification_orchestration():
    """Complete orchestration from initialization to phase completion"""
    from zenyth import SPARCOrchestrator

    # Initialize orchestrator with mocks
    orchestrator = SPARCOrchestrator(
        llm=MockClaudeClient(),
        mcp_servers={"serena": MockMCPServer("serena")}
    )

    # Execute specification phase
    result = await orchestrator.execute_phase(
        phase="specification",
        context={"project_root": "/test/project"}
    )

    # Verify complete orchestration
    assert result.success
    assert result.phase_executed == "specification"
    assert result.next_phase in ["pseudocode", "architecture"]
    assert len(result.artifacts) > 0

    # Verify orchestration metrics
    metrics = orchestrator.get_metrics()
    assert metrics.llm_calls > 0
    assert metrics.mcp_tool_calls > 0
    assert metrics.execution_time > 0
```

### Expected Outcomes
- Full end-to-end validation of orchestration system
- Performance metrics collection
- Integration test suite covering all components
- Documentation of orchestration flow

### Success Metrics
- [ ] All integration tests pass consistently
- [ ] Orchestration metrics are collected accurately
- [ ] System handles both success and failure paths
- [ ] Performance meets acceptable thresholds

## Project Success Criteria

### Technical Metrics
1. **Code Quality**
   - 100% type coverage with mypy strict mode
   - >90% test coverage with meaningful tests
   - All SOLID principles demonstrably followed
   - Zero high-severity linting issues

2. **Orchestration Functionality**
   - Successfully orchestrates Specification phase
   - Proper integration between Claude Code and mcp-agent
   - Mock infrastructure enables isolated testing
   - Clear phase transition logic

3. **Maintainability**
   - Configuration changes don't require code changes
   - New phases can be added without modifying core
   - Clear separation of concerns throughout
   - Comprehensive documentation

### Homelab Research Validation
Based on my analysis of homelab practitioner patterns, this implementation addresses the key challenges:
- No API key management complexity
- Direct integration without unnecessary abstractions
- Testable without external dependencies
- Clear extension points for additional phases

This implementation plan provides a production-grade foundation for SPARC orchestration that can evolve with your homelab needs while maintaining architectural integrity.
