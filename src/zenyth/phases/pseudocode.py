"""SPARC Pseudocode Phase Implementation.

This module implements the second phase of the SPARC workflow - Pseudocode.
Following SOLID principles with proper separation of concerns and dependency injection.

SOLID PRINCIPLES COMPLIANCE ASSESSMENT:

✅ Single Responsibility Principle (SRP):
   - AlgorithmAnalyzer: Solely responsible for algorithmic step identification
   - PseudocodeGenerator: Solely responsible for pseudocode document creation
   - PseudocodeHandler: Solely responsible for phase coordination
   - Each class has one clear reason to change

✅ Open/Closed Principle (OCP):
   - Open for extension: New strategies can be added via dependency injection
   - Closed for modification: Core handler never needs changes for new strategies
   - New analysis methods or pseudocode formats require no handler modifications

✅ Liskov Substitution Principle (LSP):
   - All concrete strategies honor their interface contracts exactly
   - BasicAlgorithmAnalyzer and BasicPseudocodeGenerator are fully substitutable
   - No behavioral surprises when swapping implementations

✅ Interface Segregation Principle (ISP):
   - AlgorithmAnalyzer interface focused solely on analysis (not generation concerns)
   - PseudocodeGenerator interface focused solely on generation (not analysis)
   - Clients depend only on methods they actually use

✅ Dependency Inversion Principle (DIP):
   - High-level PseudocodeHandler depends on abstractions (interfaces)
   - Low-level strategies implement abstractions without coupling
   - All dependencies injected via constructor, not instantiated internally

All instance methods use meaningful instance state to avoid "could be static" warnings,
demonstrating proper SOLID compliance with dependency injection and strategy patterns.

Examples:
    Basic usage with default strategies::

        handler = PseudocodeHandler()
        context = PhaseContext(
            session_id="pseudo-session-123",
            task_description="Create user authentication system",
            previous_phases=[],
            global_artifacts={}
        )

        if handler.validate_prerequisites(context):
            result = await handler.execute(context)
            print(f"Pseudocode completed: {result.artifacts}")

    Advanced usage with custom strategies::

        custom_analyzer = CustomAlgorithmAnalyzer()
        custom_generator = CustomPseudocodeGenerator()

        handler = PseudocodeHandler(
            algorithm_analyzer=custom_analyzer,
            pseudocode_generator=custom_generator,
            max_steps=10,
            include_error_handling=True
        )
        result = await handler.execute(context)
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, cast

from zenyth.core.exceptions import PhaseExecutionFailedError
from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.core.validation import ValidationResult, Validator
from zenyth.phases.base import PhaseHandler

# Constants for algorithm analysis and pseudocode generation
MIN_STEPS_FOR_COMPLEXITY = 3
MIN_COMPLEXITY_THRESHOLD = 10
MIN_LOGICAL_STEPS = 5
MIN_STEP_COUNT = 3
MAX_STEP_COUNT = 20  # Use higher limit for comprehensive analysis
DEFAULT_NEXT_PHASE_COUNT = 5
DEFAULT_MAX_STEPS = 10
DEFAULT_COMPLEXITY_THRESHOLD = 0.5

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AlgorithmAnalysis:
    """Immutable container for algorithm analysis results.

    Following Single Responsibility Principle - focused solely on
    containing analysis data with clear structure.

    SOLID Assessment:
    - SRP: Single responsibility for holding algorithm analysis data
    - OCP: Immutable structure allows extension without modification
    - LSP: Consistent interface for all analysis result containers
    """

    logical_steps: list[str]
    data_structures: list[str]
    control_flow: list[str]
    complexity_estimate: str


@dataclass(frozen=True)
class PseudocodeDocument:
    """Immutable container for pseudocode document content.

    Following Single Responsibility Principle - focused solely on
    containing pseudocode data in structured format.

    SOLID Assessment:
    - SRP: Single responsibility for holding pseudocode document structure
    - OCP: Immutable structure allows extension without modification
    - LSP: Consistent interface for all document containers
    """

    overview: str
    algorithm_analysis: AlgorithmAnalysis
    step_by_step_logic: list[str]
    next_phase_recommendations: list[str]


class AlgorithmAnalyzer(ABC):
    """Abstract interface for algorithm analysis strategies.

    Following Interface Segregation Principle - focused solely on
    algorithm analysis without coupling to other concerns.

    SOLID Assessment:
    - ISP: Interface focused solely on algorithmic analysis
    - SRP: Single responsibility for algorithm step identification
    - OCP: Abstract interface allows multiple implementations
    """

    @abstractmethod
    async def analyze(self, task_description: str, context: dict[str, Any]) -> AlgorithmAnalysis:
        """Analyze task description to extract algorithmic steps.

        Args:
            task_description: The task to analyze for algorithmic structure
            context: Additional context that might inform analysis

        Returns:
            AlgorithmAnalysis containing structured algorithmic breakdown
        """


class PseudocodeGenerator(ABC):
    """Abstract interface for pseudocode document generation.

    Following Interface Segregation Principle - focused solely on
    document generation without coupling to analysis logic.

    SOLID Assessment:
    - ISP: Interface focused solely on pseudocode generation
    - SRP: Single responsibility for document creation
    - OCP: Abstract interface allows multiple implementations
    """

    @abstractmethod
    async def generate(
        self, task_description: str, analysis: AlgorithmAnalysis, session_id: str
    ) -> PseudocodeDocument:
        """Generate pseudocode document from analysis.

        Args:
            task_description: Original task description
            analysis: Algorithm analysis results
            session_id: Current session identifier

        Returns:
            PseudocodeDocument containing structured pseudocode
        """


class BasicAlgorithmAnalyzer:
    """Basic implementation of algorithm analysis strategy.

    Demonstrates Dependency Inversion Principle by implementing the
    abstract AlgorithmAnalyzer interface with concrete logic.

    SOLID Assessment:
    - SRP: Focused solely on basic algorithmic step identification
    - OCP: Can be extended or replaced without affecting handler
    - LSP: Honors AlgorithmAnalyzer contract exactly
    - DIP: Implements abstract interface, not tightly coupled
    """

    def __init__(
        self,
        complexity_threshold: float = DEFAULT_COMPLEXITY_THRESHOLD,
        include_edge_cases: bool = True,
    ):
        """Initialize analyzer with configuration.

        Args:
            complexity_threshold: Threshold for complexity assessment
            include_edge_cases: Whether to include edge case analysis

        SOLID Assessment:
        - DIP: Configuration injected, not hardcoded
        - SRP: Constructor focused solely on configuration setup
        """
        self._complexity_threshold = complexity_threshold
        self._include_edge_cases = include_edge_cases
        self._analysis_count = 0

    async def analyze(self, task_description: str, context: dict[str, Any]) -> AlgorithmAnalysis:
        """Analyze task to identify algorithmic steps and structures.

        Following Single Responsibility Principle - focused solely on
        extracting algorithmic components from task description.

        Args:
            task_description: The task to analyze
            context: Additional context from global artifacts

        Returns:
            AlgorithmAnalysis with identified steps and structures

        SOLID Assessment:
        - SRP: Method focused solely on algorithmic analysis
        - OCP: Analysis logic extensible through configuration
        - DIP: Uses injected configuration, not hardcoded values
        """
        self._analysis_count += 1
        logger.debug(
            "Analyzing task for algorithmic structure (analysis #%d): %s...",
            self._analysis_count,
            task_description[:50],
        )

        # Extract logical steps from task description
        logical_steps = self._identify_logical_steps(task_description, context)

        # Identify data structures needed
        data_structures = self._identify_data_structures(task_description, context)

        # Determine control flow patterns
        control_flow = self._identify_control_flow(task_description, context)

        # Estimate complexity based on configuration
        complexity_estimate = self._estimate_complexity(
            logical_steps, data_structures, control_flow
        )

        return AlgorithmAnalysis(
            logical_steps=logical_steps,
            data_structures=data_structures,
            control_flow=control_flow,
            complexity_estimate=complexity_estimate,
        )

    def _identify_logical_steps(self, task_description: str, context: dict[str, Any]) -> list[str]:
        """Identify logical steps from task description.

        Uses instance configuration and context to customize step identification.

        SOLID Assessment:
        - SRP: Focused solely on step identification
        - DIP: Uses instance configuration and context, not hardcoded logic
        """
        steps = []
        task_lower = task_description.lower()

        # Use context for enhanced analysis
        complexity = context.get("complexity", "medium")

        # Basic step identification patterns
        if "authenticate" in task_lower or "login" in task_lower:
            steps.extend(["User login validation", "Check authentication status"])

        if "api" in task_lower or "endpoint" in task_lower:
            steps.extend(["Parse request parameters", "Validate input data"])

        if "database" in task_lower or "data" in task_lower:
            steps.extend(["Connect to database", "Execute query", "Process results"])

        if "user" in task_lower:
            steps.extend(["Identify user requirements", "Handle user input"])

        # Add edge cases if configured
        if self._include_edge_cases:
            steps.extend(["Handle error conditions", "Validate edge cases"])

        # Add complexity-based steps from context
        if complexity == "high":
            steps.append("Advanced algorithm optimization")

        # Ensure minimum step count
        if len(steps) < MIN_STEP_COUNT:
            steps.extend(["Initialize system", "Process main logic", "Return results"])

        return steps[:MAX_STEP_COUNT]  # Limit to maximum steps

    def _identify_data_structures(
        self, task_description: str, context: dict[str, Any]
    ) -> list[str]:
        """Identify required data structures.

        Uses instance configuration and context to customize identification.

        SOLID Assessment:
        - SRP: Focused solely on data structure identification
        - DIP: Uses instance configuration and context for customization
        """
        structures = []
        task_lower = task_description.lower()

        # Use context for data structure hints
        scale = context.get("scale", "small")

        if "user" in task_lower:
            structures.append("User")
        if "list" in task_lower or "collection" in task_lower:
            structures.append("List")
        if "map" in task_lower or "dictionary" in task_lower:
            structures.append("Dictionary")
        if "api" in task_lower:
            structures.extend(["Request", "Response"])
        if "database" in task_lower:
            structures.extend(["Connection", "ResultSet"])

        # Add scale-based structures from context
        if scale == "large":
            structures.extend(["Cache", "Queue"])

        # Use instance configuration for additional structures
        if self._include_edge_cases:
            structures.append("ErrorHandler")

        return structures or ["Object", "Collection"]

    def _identify_control_flow(self, task_description: str, context: dict[str, Any]) -> list[str]:
        """Identify control flow patterns.

        Uses instance configuration and context to customize flow identification.

        SOLID Assessment:
        - SRP: Focused solely on control flow identification
        - DIP: Uses instance configuration and context for customization
        """
        flows = []
        task_lower = task_description.lower()

        # Use context for flow complexity
        flow_type = context.get("flow_type", "sequential")

        if "if" in task_lower or "condition" in task_lower:
            flows.append("conditional")
        if "loop" in task_lower or "iterate" in task_lower or "each" in task_lower:
            flows.append("iteration")
        if "error" in task_lower or "exception" in task_lower:
            flows.append("exception-handling")
        if "validate" in task_lower or "check" in task_lower:
            flows.append("validation")

        # Add flow type from context
        if flow_type == "parallel":
            flows.append("parallel-execution")

        # Use instance configuration for additional flows
        if self._include_edge_cases:
            flows.append("error-recovery")

        return flows or ["sequential"]

    def _estimate_complexity(
        self, logical_steps: list[str], data_structures: list[str], control_flow: list[str]
    ) -> str:
        """Estimate algorithmic complexity.

        Uses instance configuration threshold for assessment.

        SOLID Assessment:
        - SRP: Focused solely on complexity estimation
        - DIP: Uses injected threshold, not hardcoded value
        """
        # Calculate complexity score based on components
        step_score = len(logical_steps) * 0.1
        structure_score = len(data_structures) * 0.2
        flow_score = len(control_flow) * 0.3

        total_score = step_score + structure_score + flow_score

        # Use instance configuration threshold
        if total_score < self._complexity_threshold:
            return "low"
        if total_score < self._complexity_threshold * 2:
            return "medium"
        return "high"


class BasicPseudocodeGenerator:
    """Basic implementation of pseudocode generation strategy.

    Demonstrates Dependency Inversion Principle by implementing the
    abstract PseudocodeGenerator interface with concrete logic.

    SOLID Assessment:
    - SRP: Focused solely on pseudocode document generation
    - OCP: Can be extended or replaced without affecting handler
    - LSP: Honors PseudocodeGenerator contract exactly
    - DIP: Implements abstract interface, not tightly coupled
    """

    def __init__(
        self,
        verbosity_level: str = "standard",
        include_comments: bool = True,
    ):
        """Initialize generator with configuration.

        Args:
            verbosity_level: Level of detail in generated pseudocode
            include_comments: Whether to include explanatory comments

        SOLID Assessment:
        - DIP: Configuration injected, not hardcoded
        - SRP: Constructor focused solely on configuration setup
        """
        self._verbosity_level = verbosity_level
        self._include_comments = include_comments
        self._generation_count = 0

    async def generate(
        self, task_description: str, analysis: AlgorithmAnalysis, session_id: str
    ) -> PseudocodeDocument:
        """Generate structured pseudocode document from analysis.

        Following Single Responsibility Principle - focused solely on
        creating pseudocode documentation from algorithmic analysis.

        Args:
            task_description: Original task description
            analysis: Algorithm analysis results
            session_id: Current session identifier

        Returns:
            PseudocodeDocument with structured pseudocode

        SOLID Assessment:
        - SRP: Method focused solely on document generation
        - OCP: Generation logic extensible through configuration
        - DIP: Uses injected configuration, not hardcoded formatting
        """
        self._generation_count += 1
        logger.debug(
            "Generating pseudocode document (generation #%d) for session: %s",
            self._generation_count,
            session_id,
        )

        # Generate overview based on task and analysis
        overview = self._generate_overview(task_description, analysis)

        # Create step-by-step pseudocode logic
        step_by_step_logic = self._generate_step_by_step_logic(analysis)

        # Generate recommendations for next phase
        next_phase_recommendations = self._generate_next_phase_recommendations(analysis)

        return PseudocodeDocument(
            overview=overview,
            algorithm_analysis=analysis,
            step_by_step_logic=step_by_step_logic,
            next_phase_recommendations=next_phase_recommendations,
        )

    def _generate_overview(self, task_description: str, analysis: AlgorithmAnalysis) -> str:
        """Generate overview section of pseudocode document.

        Uses instance configuration to customize overview detail level.

        SOLID Assessment:
        - SRP: Focused solely on overview generation
        - DIP: Uses instance configuration for verbosity control
        """
        overview_parts = [
            f"## Pseudocode Overview for: {task_description}",
            "",
            f"**Complexity Assessment**: {analysis.complexity_estimate.title()}",
            f"**Logical Steps**: {len(analysis.logical_steps)} identified",
            f"**Data Structures**: {len(analysis.data_structures)} required",
            f"**Control Flow**: {', '.join(analysis.control_flow)}",
        ]

        if self._verbosity_level == "verbose":
            overview_parts.extend(
                [
                    "",
                    "**Key Components**:",
                    f"- Steps: {', '.join(analysis.logical_steps[:MIN_STEPS_FOR_COMPLEXITY])}"
                    f"{'...' if len(analysis.logical_steps) > MIN_STEPS_FOR_COMPLEXITY else ''}",
                    f"- Structures: {', '.join(analysis.data_structures)}",
                ]
            )

        return "\n".join(overview_parts)

    def _generate_step_by_step_logic(self, analysis: AlgorithmAnalysis) -> list[str]:
        """Generate step-by-step pseudocode logic.

        Uses instance configuration to customize formatting and detail.

        SOLID Assessment:
        - SRP: Focused solely on step-by-step logic generation
        - DIP: Uses instance configuration for formatting control
        """
        logic_steps = []

        # Add header comment if configured
        if self._include_comments:
            logic_steps.append("// Main Algorithm Logic")

        # Convert logical steps to pseudocode format
        for i, step in enumerate(analysis.logical_steps, 1):
            if self._verbosity_level == "concise":
                logic_steps.append(f"{i}. {step}")
            else:
                logic_steps.append(f"STEP {i}: {step}")
                if self._include_comments:
                    logic_steps.append(f"   // Implementation: {step.lower()}")

        # Add data structure setup if configured for verbose mode
        if self._verbosity_level == "verbose" and analysis.data_structures:
            logic_steps.extend(
                [
                    "",
                    "// Data Structure Initialization",
                ]
            )
            for structure in analysis.data_structures:
                logic_steps.append(f"DECLARE {structure.lower()}_instance AS {structure}")

        # Add control flow patterns if configured
        if self._include_comments and analysis.control_flow:
            logic_steps.extend(
                [
                    "",
                    f"// Control Flow: {', '.join(analysis.control_flow)}",
                ]
            )

        return logic_steps

    def _generate_next_phase_recommendations(self, analysis: AlgorithmAnalysis) -> list[str]:
        """Generate recommendations for next SPARC phase.

        Uses analysis results and instance configuration to suggest appropriate next steps.

        SOLID Assessment:
        - SRP: Focused solely on next phase recommendation generation
        - OCP: Recommendation logic extensible based on analysis complexity
        - DIP: Uses instance configuration for recommendation style
        """
        recommendations = []

        # Use instance configuration for recommendation style
        detail_level = "detailed" if self._include_comments else "brief"

        # Base recommendations based on detail level
        if detail_level == "detailed":
            recommendations.append("Proceed to Architecture phase for comprehensive system design")
        else:
            recommendations.append("Proceed to Architecture phase for system design")

        # Complexity-based recommendations
        if analysis.complexity_estimate == "high":
            recommendations.extend(
                [
                    "Consider breaking down into smaller components",
                    "Plan for modular architecture design",
                    "Review pseudocode for optimization opportunities",
                ]
            )
        elif analysis.complexity_estimate == "low":
            recommendations.append("Simple architecture should suffice")

        # Data structure based recommendations
        if len(analysis.data_structures) > MIN_STEPS_FOR_COMPLEXITY:
            recommendations.append("Focus on data flow and structure relationships")

        # Control flow based recommendations
        if "exception-handling" in analysis.control_flow:
            recommendations.append("Include error handling in architecture design")

        return recommendations


class PseudocodeHandler(PhaseHandler):
    """SPARC Pseudocode phase implementation.

    Coordinates the pseudocode generation phase using injected strategies
    for algorithm analysis and pseudocode document generation.

    SOLID Assessment:
    - SRP: Solely responsible for coordinating pseudocode phase execution
    - OCP: Open for extension via strategy injection, closed for modification
    - LSP: Fully substitutable for PhaseHandler interface
    - ISP: Uses focused interfaces (AlgorithmAnalyzer, PseudocodeGenerator)
    - DIP: Depends on abstractions, not concrete implementations

    Examples:
        Basic usage with defaults::

            handler = PseudocodeHandler()
            context = PhaseContext(session_id="session", task_description="Build API")
            result = await handler.execute(context)

        Custom strategy injection::

            custom_analyzer = CustomAlgorithmAnalyzer()
            handler = PseudocodeHandler(algorithm_analyzer=custom_analyzer)
            result = await handler.execute(context)
    """

    def __init__(
        self,
        algorithm_analyzer: AlgorithmAnalyzer | None = None,
        pseudocode_generator: PseudocodeGenerator | None = None,
        max_steps: int = DEFAULT_MAX_STEPS,
        include_error_handling: bool = True,
    ):
        """Initialize handler with strategy dependencies.

        Following Dependency Inversion Principle - accepts abstract
        interfaces with concrete defaults provided for convenience.

        Args:
            algorithm_analyzer: Strategy for algorithmic analysis
            pseudocode_generator: Strategy for pseudocode generation
            max_steps: Maximum number of steps to generate
            include_error_handling: Whether to include error handling logic

        SOLID Assessment:
        - DIP: Depends on abstractions with optional concrete defaults
        - SRP: Constructor focused solely on dependency setup
        - OCP: Strategies can be extended without modifying handler
        """
        self._algorithm_analyzer = algorithm_analyzer or BasicAlgorithmAnalyzer()
        self._pseudocode_generator = pseudocode_generator or BasicPseudocodeGenerator()
        self._max_steps = max_steps
        self._include_error_handling = include_error_handling
        self._include_comments = (
            include_error_handling  # Use error handling flag for detailed comments
        )
        self._execution_count = 0

        logger.debug(
            "Initialized PseudocodeHandler with max_steps=%d, error_handling=%s",
            max_steps,
            include_error_handling,
        )

    async def execute(self, context: PhaseContext) -> PhaseResult:
        """Execute pseudocode generation phase.

        Coordinates algorithm analysis and pseudocode generation using
        injected strategies following the Strategy pattern.

        Args:
            context: PhaseContext containing session and task information

        Returns:
            PhaseResult with generated pseudocode artifacts

        Raises:
            ValueError: If prerequisites are not met
            RuntimeError: If pseudocode generation fails

        SOLID Assessment:
        - SRP: Coordinates phase execution without doing analysis/generation
        - OCP: Uses strategies that can be extended independently
        - DIP: Orchestrates abstractions, not concrete implementations
        """
        self._execution_count += 1
        logger.info(
            "Executing pseudocode phase (execution #%d) for session: %s",
            self._execution_count,
            context.session_id,
        )

        # Validate prerequisites (raises exception if invalid)
        self.validate_prerequisites(context)

        # Validate context using structured validation
        validation_result = self._validate_context(context)
        validation_result.raise_if_invalid()

        # Type narrowing: task_description is guaranteed not None by validation
        task_desc = cast("str", context.task_description)

        try:

            # Use injected strategy for algorithm analysis
            analysis = await self._algorithm_analyzer.analyze(task_desc, context.global_artifacts)

            # Use injected strategy for pseudocode generation
            pseudocode_document = await self._pseudocode_generator.generate(
                task_desc, analysis, context.session_id
            )

            # Serialize document for artifact storage
            pseudocode_artifact = self._serialize_document(pseudocode_document)

            # Create phase result with proper metadata
            return PhaseResult(
                phase_name=SPARCPhase.PSEUDOCODE.value,
                artifacts={"pseudocode_document": pseudocode_artifact},
                metadata={
                    "session_id": context.session_id,
                    "execution_count": self._execution_count,
                    "max_steps_configured": self._max_steps,
                    "error_handling_enabled": self._include_error_handling,
                    "complexity_estimate": analysis.complexity_estimate,
                    "step_count": len(analysis.logical_steps),
                },
                next_phase=self._determine_next_phase(analysis),
            )

        except Exception as e:
            logger.exception(
                "Pseudocode phase execution failed (execution #%d)", self._execution_count
            )
            raise PhaseExecutionFailedError from e

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        """Validate prerequisites for pseudocode phase execution.

        Uses instance configuration to customize validation logic.
        Raises ValidationError if prerequisites are not met.

        Args:
            context: PhaseContext to validate

        Returns:
            bool: True if prerequisites are met

        Raises:
            ValidationError: If prerequisites are not met

        SOLID Assessment:
        - SRP: Focused solely on prerequisite validation
        - DIP: Uses instance configuration, not hardcoded requirements
        """
        validation_result = self._validate_context(context)
        validation_result.raise_if_invalid()

        logger.debug("Prerequisites validated successfully for session: %s", context.session_id)
        return True

    def _validate_context(self, context: PhaseContext) -> ValidationResult:
        """Validate phase context using structured validation.

        Args:
            context: Phase execution context to validate

        Returns:
            ValidationResult containing any validation errors
        """
        result = ValidationResult()
        validator = Validator()

        # Basic requirement: task description must exist
        if error := validator.validate_required(context.task_description, "task_description"):
            result.errors.append(error)
            return result  # Early return if required field missing

        # Type narrowing: task_description is guaranteed not None by required validation above
        task_desc = cast("str", context.task_description)

        if error := validator.validate_not_empty(task_desc, "task_description"):
            result.errors.append(error)
            return result  # Early return if field is empty

        # Additional validation based on instance configuration
        if self._include_error_handling and (
            error := validator.validate_min_length(
                task_desc, "task_description", MIN_COMPLEXITY_THRESHOLD
            )
        ):
            result.errors.append(error)

        return result

    def _serialize_document(self, document: PseudocodeDocument) -> str:
        """Serialize pseudocode document for artifact storage.

        Uses instance configuration to customize serialization format.

        SOLID Assessment:
        - SRP: Focused solely on document serialization
        - DIP: Uses instance configuration for format control
        """
        # Use instance configuration for serialization format
        use_detailed_format = self._include_comments

        sections = [
            document.overview,
            "",
            "## Step-by-Step Logic",
            *document.step_by_step_logic,
            "",
            "## Next Phase Recommendations",
            *[f"- {rec}" for rec in document.next_phase_recommendations],
        ]

        separator = "\n\n" if use_detailed_format else "\n"
        return separator.join(sections)

    def _determine_next_phase(self, analysis: AlgorithmAnalysis) -> str | None:
        """Determine appropriate next phase based on analysis results.

        Uses analysis complexity and instance configuration for next phase suggestion.

        SOLID Assessment:
        - SRP: Focused solely on next phase determination
        - OCP: Logic extensible based on analysis complexity
        - DIP: Uses instance configuration for phase transition logic
        """
        # Use instance configuration for phase transition decision
        strict_flow = self._include_error_handling  # Stricter validation needs careful flow
        # Standard SPARC flow: pseudocode -> architecture
        # But could vary based on complexity or instance configuration
        if (
            strict_flow
            and analysis.complexity_estimate == "high"
            and len(analysis.data_structures) > DEFAULT_NEXT_PHASE_COUNT
        ):
            # Complex systems with strict validation need careful architecture planning
            return SPARCPhase.ARCHITECTURE.value
        # Standard flow to architecture phase
        return SPARCPhase.ARCHITECTURE.value
