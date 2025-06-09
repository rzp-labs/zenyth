"""Specification phase handler for SPARC methodology.

This module implements the first phase of the SPARC workflow - Specification.
Following SOLID principles with proper separation of concerns and dependency injection.

The implementation demonstrates:
- Single Responsibility: Each class/method has one clear purpose
- Open/Closed: Extensible through strategy pattern and dependency injection
- Liskov Substitution: Proper interface implementation with meaningful instance behavior
- Interface Segregation: Focused interfaces for each responsibility
- Dependency Inversion: Depends on abstractions, not concrete implementations

Examples:
    Basic usage with default strategies::

        handler = SpecificationHandler()
        context = PhaseContext(
            session_id="spec-session-123",
            task_description="Create user authentication system",
            previous_phases=[],
            global_artifacts={}
        )

        if handler.validate_prerequisites(context):
            result = await handler.execute(context)
            print(f"Specification completed: {result.artifacts}")

    Advanced usage with custom strategies::

        custom_analyzer = CustomRequirementsAnalyzer()
        custom_generator = CustomSpecificationGenerator()

        handler = SpecificationHandler(
            requirements_analyzer=custom_analyzer,
            specification_generator=custom_generator
        )
        result = await handler.execute(context)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.phases.base import PhaseHandler


@dataclass(frozen=True)
class RequirementsAnalysis:
    """Immutable container for requirements analysis results.

    Following Single Responsibility Principle - focused solely on
    containing analysis data with clear structure.
    """

    functional_requirements: list[str]
    non_functional_requirements: dict[str, str]
    constraints: list[str]
    assumptions: list[str]
    complexity_assessment: str


@dataclass(frozen=True)
class SpecificationDocument:
    """Immutable container for specification document content.

    Following Single Responsibility Principle - focused solely on
    containing specification data in structured format.
    """

    overview: str
    requirements_analysis: RequirementsAnalysis
    success_criteria: list[str]
    next_phase_recommendations: list[str]


class RequirementsAnalyzer(ABC):
    """Abstract interface for requirements analysis strategies.

    Following Interface Segregation Principle - focused solely on
    requirements analysis without coupling to other concerns.
    """

    @abstractmethod
    async def analyze(self, task_description: str, context: dict[str, Any]) -> RequirementsAnalysis:
        """Analyze task description to extract requirements.

        Args:
            task_description: The task to analyze
            context: Additional context that might inform analysis

        Returns:
            RequirementsAnalysis containing structured requirements
        """


class SpecificationGenerator(ABC):
    """Abstract interface for specification document generation.

    Following Interface Segregation Principle - focused solely on
    document generation without coupling to analysis logic.
    """

    @abstractmethod
    async def generate(
        self, task_description: str, analysis: RequirementsAnalysis, session_id: str
    ) -> SpecificationDocument:
        """Generate specification document from analysis.

        Args:
            task_description: Original task description
            analysis: Requirements analysis results
            session_id: Session identifier for context

        Returns:
            SpecificationDocument with structured content
        """


class BasicRequirementsAnalyzer(RequirementsAnalyzer):
    """Basic implementation of requirements analysis.

    Following Single Responsibility Principle - focused solely on
    basic requirements extraction without advanced logic.
    """

    def __init__(self, min_requirement_length: int = 10):
        """Initialize analyzer with configuration.

        Args:
            min_requirement_length: Minimum length for meaningful requirements
        """
        self._min_requirement_length = min_requirement_length
        # Configuration constants for complexity assessment
        self._simple_task_threshold = 20
        self._moderate_task_threshold = 100

    async def analyze(self, task_description: str, context: dict[str, Any]) -> RequirementsAnalysis:
        """Perform basic requirements analysis on task description."""
        # Use context information to enhance analysis
        context_keys = list(context.keys()) if context else []
        # Basic functional requirements extraction
        functional_requirements = [
            f"Implement core functionality: {task_description}",
            "Ensure proper error handling and validation",
            "Provide appropriate user feedback mechanisms",
            "Follow established coding patterns and standards",
        ]

        # Standard non-functional requirements
        non_functional_requirements = {
            "performance": "Standard response times and throughput",
            "security": "Appropriate security measures for task scope",
            "maintainability": "Clean, documented, testable code",
            "scalability": "Design should accommodate reasonable growth",
        }

        # Basic constraints identification - enhanced with context
        constraints = [
            "Must follow SOLID principles",
            "Code quality standards must be maintained",
            "Comprehensive testing required",
        ]

        # Add context-specific constraints if available
        if "existing_system" in context_keys:
            constraints.append("Must integrate with existing system architecture")
        if "performance_requirements" in context_keys:
            constraints.append("Must meet specified performance requirements")

        # Basic assumptions
        assumptions = [
            "Standard development environment available",
            "Access to necessary tools and libraries",
            "Reasonable time and resource constraints",
        ]

        # Use instance configuration for complexity assessment
        task_length = len(task_description.strip())
        if task_length < self._simple_task_threshold:
            complexity = "simple"
        elif task_length < self._moderate_task_threshold:
            complexity = "moderate"
        else:
            complexity = "complex"

        return RequirementsAnalysis(
            functional_requirements=functional_requirements,
            non_functional_requirements=non_functional_requirements,
            constraints=constraints,
            assumptions=assumptions,
            complexity_assessment=complexity,
        )


class BasicSpecificationGenerator(SpecificationGenerator):
    """Basic implementation of specification document generation.

    Following Single Responsibility Principle - focused solely on
    document generation with clear, structured output.
    """

    def __init__(self, include_detailed_analysis: bool = True):
        """Initialize generator with configuration.

        Args:
            include_detailed_analysis: Whether to include detailed analysis sections
        """
        self._include_detailed_analysis = include_detailed_analysis

    async def generate(
        self, task_description: str, analysis: RequirementsAnalysis, session_id: str
    ) -> SpecificationDocument:
        """Generate basic specification document."""
        # Create overview section with conditional detail based on instance config
        overview = f"""# Specification for: {task_description}

## Overview
Task: {task_description}
Session: {session_id}
Complexity: {analysis.complexity_assessment}

This specification provides a comprehensive analysis of requirements and
establishes the foundation for subsequent SPARC phases.
"""

        # Add detailed analysis section if configured
        if self._include_detailed_analysis:
            overview += f"""

## Detailed Analysis
Functional Requirements: {len(analysis.functional_requirements)} identified
Non-Functional Requirements: {len(analysis.non_functional_requirements)} categories
Constraints: {len(analysis.constraints)} identified
Assumptions: {len(analysis.assumptions)} documented
"""

        # Define success criteria based on analysis
        success_criteria = [
            "All functional requirements implemented and tested",
            "Non-functional requirements met according to specifications",
            "Code quality standards achieved with comprehensive documentation",
            "All constraints and assumptions validated",
            f"Task completion verified: {task_description}",
        ]

        # Recommend next phases based on complexity
        if analysis.complexity_assessment == "complex":
            next_phase_recommendations = [
                "Proceed to pseudocode phase for algorithm design",
                "Consider architecture phase for system design",
                "Plan for iterative refinement approach",
            ]
        else:
            next_phase_recommendations = [
                "Proceed directly to architecture phase",
                "Consider simplified implementation approach",
                "Plan for standard refinement and completion phases",
            ]

        return SpecificationDocument(
            overview=overview,
            requirements_analysis=analysis,
            success_criteria=success_criteria,
            next_phase_recommendations=next_phase_recommendations,
        )


class SpecificationHandler(PhaseHandler):
    """SOLID-compliant implementation of the SPARC specification phase.

    This class demonstrates all five SOLID principles:

    1. Single Responsibility: Coordinates specification creation process only
    2. Open/Closed: Extensible via dependency injection of strategies
    3. Liskov Substitution: Fully substitutable PhaseHandler implementation
    4. Interface Segregation: Uses focused, specific interfaces
    5. Dependency Inversion: Depends on abstractions (RequirementsAnalyzer, SpecificationGenerator)

    The handler acts as a coordinator, delegating actual work to injected
    strategy implementations following the Strategy pattern.
    """

    def __init__(
        self,
        requirements_analyzer: RequirementsAnalyzer | None = None,
        specification_generator: SpecificationGenerator | None = None,
        min_task_length: int = 3,
    ):
        """Initialize handler with strategy dependencies.

        Following Dependency Inversion Principle - depends on abstractions
        rather than concrete implementations.

        Args:
            requirements_analyzer: Strategy for analyzing requirements
            specification_generator: Strategy for generating specifications
            min_task_length: Minimum task description length for validation
        """
        # Use default implementations if none provided (following Open/Closed)
        self._requirements_analyzer = requirements_analyzer or BasicRequirementsAnalyzer()
        self._specification_generator = specification_generator or BasicSpecificationGenerator()
        self._min_task_length = min_task_length
        # Configuration for artifact creation
        self._include_context_analysis = True
        self._track_strategy_usage = True
        # Configuration for phase transition logic
        self._prefer_pseudocode_for_complex = True

    async def execute(self, context: PhaseContext) -> PhaseResult:
        """Execute specification phase using injected strategies.

        Following Single Responsibility Principle - coordinates the process
        but delegates actual work to strategy implementations.

        This method demonstrates Dependency Inversion by using injected
        abstractions rather than creating concrete implementations.
        """
        # Validate prerequisites using instance state
        if not self.validate_prerequisites(context):
            msg = "Prerequisites not met for specification phase"
            raise ValueError(msg)

        # After validation, we know task_description is not None
        if context.task_description is None:
            msg = "Task description unexpectedly None after validation"
            raise RuntimeError(msg)
        task_description = context.task_description

        # Use injected analyzer strategy (Dependency Inversion)
        analysis = await self._requirements_analyzer.analyze(
            task_description, context.global_artifacts
        )

        # Use injected generator strategy (Dependency Inversion)
        specification = await self._specification_generator.generate(
            task_description, analysis, context.session_id
        )

        # Structure artifacts for next phase
        artifacts = self._create_artifacts(specification, analysis, context)

        # Create execution metadata
        metadata = self._create_metadata(context, analysis)

        return PhaseResult(
            phase_name=SPARCPhase.SPECIFICATION.value,
            artifacts=artifacts,
            next_phase=self._determine_next_phase(analysis),
            metadata=metadata,
        )

    def validate_prerequisites(self, context: PhaseContext) -> bool:
        """Validate prerequisites using instance configuration.

        Following Liskov Substitution Principle - this method meaningfully
        uses instance state (self._min_task_length) making it a proper
        instance method that couldn't be static.
        """
        if context.task_description is None:
            return False

        # Use instance configuration for validation (meaningful use of self)
        return len(context.task_description.strip()) >= self._min_task_length

    def _create_artifacts(
        self,
        specification: SpecificationDocument,
        analysis: RequirementsAnalysis,
        context: PhaseContext,
    ) -> dict[str, Any]:
        """Create structured artifacts dictionary using instance configuration.

        Following Single Responsibility Principle - focused solely on
        artifact creation and structuring.
        """
        artifacts = {
            "specification_document": specification.overview,
            "functional_requirements": analysis.functional_requirements,
            "non_functional_requirements": analysis.non_functional_requirements,
            "constraints": analysis.constraints,
            "assumptions": analysis.assumptions,
            "success_criteria": specification.success_criteria,
            "next_phase_recommendations": specification.next_phase_recommendations,
            "task_analysis": {
                "original_task": context.task_description,
                "complexity_assessment": analysis.complexity_assessment,
                "context_considered": bool(context.global_artifacts),
            },
        }

        # Add optional context analysis if configured
        if self._include_context_analysis and context.global_artifacts:
            artifacts["context_analysis"] = {
                "global_artifacts_count": len(context.global_artifacts),
                "previous_phases_count": len(context.previous_phases),
            }

        return artifacts

    def _create_metadata(
        self, context: PhaseContext, analysis: RequirementsAnalysis
    ) -> dict[str, Any]:
        """Create execution metadata using instance configuration.

        Following Single Responsibility Principle - focused solely on
        metadata creation.
        """
        metadata = {
            "session_id": context.session_id,
            "phase_duration": "coordination_completed",
            "requirements_count": len(analysis.functional_requirements),
            "complexity": analysis.complexity_assessment,
        }

        # Add strategy information if configured to track usage
        if self._track_strategy_usage:
            metadata["strategies_used"] = {
                "analyzer": type(self._requirements_analyzer).__name__,
                "generator": type(self._specification_generator).__name__,
            }

        return metadata

    def _determine_next_phase(self, analysis: RequirementsAnalysis) -> str:
        """Determine next phase based on analysis results and instance configuration.

        Following Single Responsibility Principle - focused solely on
        phase transition logic using instance configuration.
        """
        # Use instance configuration for complex task handling
        if analysis.complexity_assessment == "complex" and self._prefer_pseudocode_for_complex:
            return SPARCPhase.PSEUDOCODE.value

        # Most tasks proceed directly to architecture
        return SPARCPhase.ARCHITECTURE.value
