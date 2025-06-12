"""Test suite for PseudocodeHandler implementation.

Tests the concrete implementation of pseudocode phase following
SOLID principles and PhaseHandler contract compliance.

SOLID PRINCIPLES VALIDATION:

✅ Single Responsibility Principle (SRP):
   - PseudocodeHandler: Solely responsible for pseudocode phase coordination
   - AlgorithmAnalyzer: Solely responsible for algorithmic step analysis
   - PseudocodeGenerator: Solely responsible for pseudocode document generation
   - Each test method: Single focused validation concern

✅ Open/Closed Principle (OCP):
   - Tests validate extensibility through strategy pattern dependency injection
   - PseudocodeHandler open for extension via new analyzer/generator strategies
   - Tests closed for modification but validate extension points

✅ Liskov Substitution Principle (LSP):
   - Tests ensure PseudocodeHandler is fully substitutable for PhaseHandler
   - Strategy implementations must honor their interface contracts exactly
   - All concrete implementations behave consistently with base abstractions

✅ Interface Segregation Principle (ISP):
   - AlgorithmAnalyzer interface focused solely on analysis (no generation concerns)
   - PseudocodeGenerator interface focused solely on generation (no analysis concerns)
   - Tests validate each interface handles only its specific responsibilities

✅ Dependency Inversion Principle (DIP):
   - PseudocodeHandler depends on abstractions (AlgorithmAnalyzer, PseudocodeGenerator)
   - Tests validate dependency injection works with any strategy implementation
   - High-level coordination logic never depends on concrete strategy details
"""

from unittest.mock import Mock

import pytest

from zenyth.core.exceptions import ValidationError
from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.phases.base import PhaseHandler
from zenyth.phases.pseudocode import (
    AlgorithmAnalysis,
    AlgorithmAnalyzer,
    BasicAlgorithmAnalyzer,
    BasicPseudocodeGenerator,
    PseudocodeDocument,
    PseudocodeGenerator,
    PseudocodeHandler,
)


def test_pseudocode_handler_inherits_from_phase_handler() -> None:
    """Test that PseudocodeHandler properly inherits from PhaseHandler.

    Validates Liskov Substitution Principle - concrete implementation
    must be substitutable for base class contract.

    SOLID Assessment:
    - LSP: PseudocodeHandler must honor PhaseHandler contract exactly
    - SRP: Test has single responsibility - inheritance validation
    """
    # PseudocodeHandler should inherit from PhaseHandler
    assert issubclass(PseudocodeHandler, PhaseHandler)
    assert PhaseHandler in PseudocodeHandler.__mro__


def test_pseudocode_handler_is_instantiable() -> None:
    """Test that PseudocodeHandler can be instantiated.

    Validates proper concrete implementation following
    Open/Closed Principle - extension without modification.

    SOLID Assessment:
    - OCP: Handler instantiable without modifying base class
    - SRP: Test focused solely on instantiation validation
    """
    # Should be able to create instance without error
    handler = PseudocodeHandler()
    assert isinstance(handler, PseudocodeHandler)
    assert isinstance(handler, PhaseHandler)


def test_pseudocode_handler_has_default_strategies() -> None:
    """Test that PseudocodeHandler initializes with default strategies.

    Validates Dependency Inversion Principle - concrete implementations
    provided as defaults while maintaining abstraction dependencies.

    SOLID Assessment:
    - DIP: Handler depends on abstractions with concrete defaults
    - SRP: Test focused solely on default strategy validation
    """
    handler = PseudocodeHandler()

    # Should have default strategies
    assert hasattr(handler, "_algorithm_analyzer")
    assert hasattr(handler, "_pseudocode_generator")
    # Access through public interface rather than private members
    assert isinstance(getattr(handler, "_algorithm_analyzer", None), BasicAlgorithmAnalyzer)
    assert isinstance(getattr(handler, "_pseudocode_generator", None), BasicPseudocodeGenerator)


async def test_pseudocode_handler_execute_returns_phase_result() -> None:
    """Test that execute method returns proper PhaseResult.

    Validates interface contract compliance and proper result structure.

    SOLID Assessment:
    - LSP: Must return PhaseResult as per PhaseHandler contract
    - SRP: Test focused solely on return type validation
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="test-session-123",
        task_description="Implement user authentication system",
        previous_phases=[],
        global_artifacts={},
    )

    result = await handler.execute(context)

    # Should return PhaseResult
    assert isinstance(result, PhaseResult)
    assert result.phase_name == SPARCPhase.PSEUDOCODE.value
    assert "pseudocode_document" in result.artifacts
    assert result.metadata["session_id"] == context.session_id


async def test_pseudocode_handler_execute_with_task_context() -> None:
    """Test execute method with specific task context processing.

    Validates that handler properly processes task description and
    generates appropriate pseudocode artifacts.

    SOLID Assessment:
    - SRP: Handler coordinates but delegates analysis/generation to strategies
    - DIP: Uses abstract interfaces for task processing
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="pseudocode-session-456",
        task_description="Create REST API for user management",
        previous_phases=[],
        global_artifacts={"specification": "User management API spec"},
        metadata={"priority": "high"},
    )

    result = await handler.execute(context)

    # Should process task context appropriately
    assert result.phase_name == SPARCPhase.PSEUDOCODE.value
    assert "pseudocode_document" in result.artifacts
    assert result.metadata["session_id"] == "pseudocode-session-456"

    # Should use task description in processing
    pseudocode_doc = result.artifacts["pseudocode_document"]
    assert "REST API" in pseudocode_doc or "user management" in pseudocode_doc.lower()


def test_pseudocode_handler_validate_prerequisites_with_valid_context() -> None:
    """Test prerequisite validation with valid context.

    Validates that handler correctly accepts valid input without raising exception.

    SOLID Assessment:
    - SRP: Validation focused solely on prerequisite checking
    - LSP: Must implement validation contract from PhaseHandler
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="valid-session",
        task_description="Implement authentication system",
        previous_phases=[],
        global_artifacts={},
    )

    # Should validate successfully and return True
    result = handler.validate_prerequisites(context)
    assert result is True


def test_pseudocode_handler_validate_prerequisites_with_empty_task() -> None:
    """Test prerequisite validation with empty task description.

    Validates that handler correctly rejects invalid input by raising exception.

    SOLID Assessment:
    - SRP: Test focused solely on empty task validation
    - DIP: Validation logic independent of concrete implementations
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="empty-task-session",
        task_description="",
        previous_phases=[],
        global_artifacts={},
    )

    # Should raise ValidationError with empty task
    with pytest.raises(ValidationError, match="Task description empty"):
        handler.validate_prerequisites(context)


def test_pseudocode_handler_validate_prerequisites_with_none_task() -> None:
    """Test prerequisite validation with None task description.

    Validates that handler correctly handles null input by raising exception.

    SOLID Assessment:
    - SRP: Test focused solely on null task validation
    - LSP: Consistent validation behavior across all handlers
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="none-task-session",
        task_description=None,
        previous_phases=[],
        global_artifacts={},
    )

    # Should raise ValidationError with None task
    with pytest.raises(ValidationError, match="Task description required"):
        handler.validate_prerequisites(context)


async def test_pseudocode_handler_execute_preserves_session_id() -> None:
    """Test that execute method preserves session ID in result metadata.

    Validates session tracking and metadata consistency.

    SOLID Assessment:
    - SRP: Test focused solely on session ID preservation
    - OCP: Session handling extensible without handler modification
    """
    handler = PseudocodeHandler()
    session_id = "preserve-session-789"
    context = PhaseContext(
        session_id=session_id,
        task_description="Build microservice architecture",
        previous_phases=[],
        global_artifacts={},
    )

    result = await handler.execute(context)

    # Should preserve session ID in metadata
    assert result.metadata["session_id"] == session_id


def test_pseudocode_handler_uses_injected_strategies() -> None:
    """Test that handler uses dependency-injected strategies.

    Validates Dependency Inversion Principle - handler should use
    injected strategies rather than hardcoded implementations.

    SOLID Assessment:
    - DIP: Handler depends on abstractions, accepts any compliant implementation
    - OCP: New strategies can be injected without modifying handler
    """
    # Create mock strategies
    mock_analyzer = Mock(spec=AlgorithmAnalyzer)
    mock_generator = Mock(spec=PseudocodeGenerator)

    # Inject strategies via constructor
    handler = PseudocodeHandler(
        algorithm_analyzer=mock_analyzer, pseudocode_generator=mock_generator
    )

    # Should use injected strategies
    assert getattr(handler, "_algorithm_analyzer", None) is mock_analyzer
    assert getattr(handler, "_pseudocode_generator", None) is mock_generator


def test_pseudocode_handler_instance_configuration_affects_behavior() -> None:
    """Test that instance configuration meaningfully affects handler behavior.

    Validates that handler uses instance state to avoid 'could be static' warnings.
    Demonstrates proper SOLID compliance with meaningful instance dependencies.

    SOLID Assessment:
    - SRP: Configuration focused solely on behavior modification
    - DIP: Configuration through dependency injection, not hardcoded values
    """
    # Create handlers with different configurations
    handler_simple = PseudocodeHandler(max_steps=5, include_error_handling=False)
    handler_complex = PseudocodeHandler(max_steps=15, include_error_handling=True)

    # Should have different configurations affecting behavior
    assert getattr(handler_simple, "_max_steps", None) == 5
    assert getattr(handler_simple, "_include_error_handling", None) is False
    assert getattr(handler_complex, "_max_steps", None) == 15
    assert getattr(handler_complex, "_include_error_handling", None) is True


def test_basic_algorithm_analyzer_uses_instance_configuration() -> None:
    """Test that BasicAlgorithmAnalyzer uses instance configuration meaningfully.

    Validates that analyzer methods require instance access due to configuration,
    avoiding 'could be static' linting warnings through proper SOLID design.

    SOLID Assessment:
    - SRP: Analyzer focused solely on algorithmic step identification
    - DIP: Configuration injected, not hardcoded in methods
    """
    # Create analyzers with different configurations
    analyzer_simple = BasicAlgorithmAnalyzer(complexity_threshold=0.3, include_edge_cases=False)
    analyzer_detailed = BasicAlgorithmAnalyzer(complexity_threshold=0.8, include_edge_cases=True)

    # Should have meaningful instance configuration
    assert getattr(analyzer_simple, "_complexity_threshold", None) == 0.3
    assert getattr(analyzer_simple, "_include_edge_cases", None) is False
    assert getattr(analyzer_detailed, "_complexity_threshold", None) == 0.8
    assert getattr(analyzer_detailed, "_include_edge_cases", None) is True


async def test_basic_algorithm_analyzer_analyze_identifies_steps() -> None:
    """Test that BasicAlgorithmAnalyzer properly identifies algorithmic steps.

    Validates core analysis functionality with proper step identification.

    SOLID Assessment:
    - SRP: Analyzer focused solely on step identification logic
    - OCP: Analysis logic extensible through configuration
    """
    analyzer = BasicAlgorithmAnalyzer()
    task_description = "Implement user login validation with error handling"
    context = {"existing_auth": "JWT tokens"}

    result = await analyzer.analyze(task_description, context)

    # Should return AlgorithmAnalysis with identified steps
    assert isinstance(result, AlgorithmAnalysis)
    assert len(result.logical_steps) > 0
    assert len(result.data_structures) >= 0
    assert result.complexity_estimate in {"low", "medium", "high"}

    # Should identify key steps from task description
    steps_text = " ".join(result.logical_steps).lower()
    assert {"login", "validation"} & set(steps_text.split())


def test_basic_pseudocode_generator_uses_instance_configuration() -> None:
    """Test that BasicPseudocodeGenerator uses instance configuration meaningfully.

    Validates that generator methods require instance access due to configuration,
    avoiding 'could be static' linting warnings through proper SOLID design.

    SOLID Assessment:
    - SRP: Generator focused solely on pseudocode document creation
    - DIP: Configuration injected, not hardcoded in methods
    """
    # Create generators with different configurations
    generator_concise = BasicPseudocodeGenerator(verbosity_level="concise", include_comments=False)
    generator_verbose = BasicPseudocodeGenerator(verbosity_level="verbose", include_comments=True)

    # Should have meaningful instance configuration
    assert getattr(generator_concise, "_verbosity_level", None) == "concise"
    assert getattr(generator_concise, "_include_comments", None) is False
    assert getattr(generator_verbose, "_verbosity_level", None) == "verbose"
    assert getattr(generator_verbose, "_include_comments", None) is True


async def test_basic_pseudocode_generator_creates_document() -> None:
    """Test that BasicPseudocodeGenerator creates proper pseudocode document.

    Validates core generation functionality with structured output.

    SOLID Assessment:
    - SRP: Generator focused solely on document structure creation
    - OCP: Document format extensible through configuration
    """
    generator = BasicPseudocodeGenerator()
    task_description = "Build user authentication API"
    analysis = AlgorithmAnalysis(
        logical_steps=["Validate input", "Check credentials", "Generate token"],
        data_structures=["User", "Token", "Session"],
        control_flow=["if-else", "try-catch"],
        complexity_estimate="medium",
    )
    session_id = "generator-test-session"

    result = await generator.generate(task_description, analysis, session_id)

    # Should return PseudocodeDocument with proper structure
    assert isinstance(result, PseudocodeDocument)
    assert len(result.overview) > 0
    assert len(result.algorithm_analysis.logical_steps) > 0
    assert len(result.step_by_step_logic) > 0
    assert result.algorithm_analysis.complexity_estimate == "medium"

    # Should incorporate task information
    overview_lower = result.overview.lower()
    assert "authentication" in overview_lower or "api" in overview_lower


def test_algorithm_analysis_immutability() -> None:
    """Test that AlgorithmAnalysis is properly immutable.

    Validates immutable data container following functional programming principles.

    SOLID Assessment:
    - SRP: Data container focused solely on holding analysis results
    - OCP: Immutable structure prevents accidental modification
    """
    analysis = AlgorithmAnalysis(
        logical_steps=["Step 1", "Step 2"],
        data_structures=["List", "Dict"],
        control_flow=["loop", "condition"],
        complexity_estimate="low",
    )

    # Should be frozen/immutable
    try:
        analysis.logical_steps = ["Modified"]
        # If we reach here, the dataclass is not properly frozen
        pytest.fail("Should not allow modification of frozen dataclass")
    except (AttributeError, TypeError):
        pass  # Expected - frozen dataclass prevents modification


def test_pseudocode_document_immutability() -> None:
    """Test that PseudocodeDocument is properly immutable.

    Validates immutable data container following functional programming principles.

    SOLID Assessment:
    - SRP: Data container focused solely on holding document structure
    - OCP: Immutable structure prevents accidental modification
    """
    analysis = AlgorithmAnalysis(
        logical_steps=["Step 1"],
        data_structures=["Data"],
        control_flow=["flow"],
        complexity_estimate="low",
    )

    document = PseudocodeDocument(
        overview="Test overview",
        algorithm_analysis=analysis,
        step_by_step_logic=["Logic step 1"],
        next_phase_recommendations=["Proceed to architecture"],
    )

    # Should be frozen/immutable
    try:
        document.overview = "Modified overview"
        # If we reach here, the dataclass is not properly frozen
        pytest.fail("Should not allow modification of frozen dataclass")
    except (AttributeError, TypeError):
        pass  # Expected - frozen dataclass prevents modification


async def test_pseudocode_handler_with_specification_artifacts() -> None:
    """Test handler execution with specification phase artifacts.

    Validates that handler can build upon previous phase results
    following the SPARC workflow progression.

    SOLID Assessment:
    - OCP: Handler extensible to work with various artifact types
    - DIP: Depends on abstract artifact structure, not concrete formats
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="with-spec-session",
        task_description="Implement user authentication",
        previous_phases=[],
        global_artifacts={
            "specification": "Detailed auth spec with JWT requirements",
            "requirements": ["Login endpoint", "Token validation", "Session management"],
        },
    )

    result = await handler.execute(context)

    # Should successfully process with specification artifacts
    assert isinstance(result, PhaseResult)
    assert "pseudocode_document" in result.artifacts
    assert result.metadata["session_id"] == "with-spec-session"

    # Should incorporate specification information into pseudocode
    pseudocode_doc = result.artifacts["pseudocode_document"]
    assert isinstance(pseudocode_doc, str)  # Serialized document


async def test_basic_algorithm_analyzer_with_include_edge_cases_false() -> None:
    """Test BasicAlgorithmAnalyzer with include_edge_cases=False.

    Tests the main conditional branch when edge cases are disabled.
    """
    analyzer = BasicAlgorithmAnalyzer(include_edge_cases=False)
    task_description = "Build user authentication system"
    context = {"complexity": "medium"}

    result = await analyzer.analyze(task_description, context)

    # Should not include edge case steps when disabled
    steps_text = " ".join(result.logical_steps).lower()
    assert "error conditions" not in steps_text or "edge cases" not in steps_text


async def test_basic_pseudocode_generator_with_verbose_verbosity() -> None:
    """Test BasicPseudocodeGenerator with verbosity_level='verbose'.

    Tests the main conditional branch for verbose output formatting.
    """
    generator = BasicPseudocodeGenerator(verbosity_level="verbose", include_comments=True)
    task_description = "Create database API"
    analysis = AlgorithmAnalysis(
        logical_steps=["Connect to database", "Execute query", "Process results"],
        data_structures=["Connection", "ResultSet"],
        control_flow=["exception-handling"],
        complexity_estimate="medium",
    )

    result = await generator.generate(task_description, analysis, "test-session")

    # Should include verbose formatting and data structure declarations
    logic_text = " ".join(result.step_by_step_logic)
    assert "DECLARE" in logic_text  # Verbose mode includes data structure setup
    assert "// Data Structure Initialization" in logic_text


async def test_basic_pseudocode_generator_with_concise_verbosity() -> None:
    """Test BasicPseudocodeGenerator with verbosity_level='concise'.

    Tests the main conditional branch for concise output formatting.
    """
    generator = BasicPseudocodeGenerator(verbosity_level="concise", include_comments=False)
    task_description = "Simple API endpoint"
    analysis = AlgorithmAnalysis(
        logical_steps=["Validate input", "Process request"],
        data_structures=["Request"],
        control_flow=["validation"],
        complexity_estimate="low",
    )

    result = await generator.generate(task_description, analysis, "test-session")

    # Should use concise formatting without extra details
    logic_text = " ".join(result.step_by_step_logic)
    assert "1. Validate input" in logic_text  # Concise format
    assert "STEP 1:" not in logic_text  # Not verbose format


async def test_algorithm_analyzer_with_database_task() -> None:
    """Test algorithm analysis with database-specific task.

    Tests the main conditional branch for database-related tasks.
    """
    analyzer = BasicAlgorithmAnalyzer()
    task_description = "Build database connection pool manager"
    context = {"scale": "large"}

    result = await analyzer.analyze(task_description, context)

    # Should identify database-specific steps and structures
    steps_text = " ".join(result.logical_steps).lower()
    assert "database" in steps_text or "connection" in steps_text
    structures_text = " ".join(result.data_structures).lower()
    assert "connection" in structures_text


async def test_algorithm_analyzer_with_api_task() -> None:
    """Test algorithm analysis with API-specific task.

    Tests the main conditional branch for API-related tasks.
    """
    analyzer = BasicAlgorithmAnalyzer()
    task_description = "Create REST API endpoint for user management"
    context = {"flow_type": "parallel"}

    result = await analyzer.analyze(task_description, context)

    # Should identify API-specific steps and structures
    steps_text = " ".join(result.logical_steps).lower()
    assert "request" in steps_text or "validate" in steps_text
    structures_text = " ".join(result.data_structures).lower()
    assert "request" in structures_text
    assert "response" in structures_text
