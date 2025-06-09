"""Abstract base class for SPARC phase handlers.

This module defines the PhaseHandler abstract base class that all concrete
phase implementations must inherit from. Following the Open/Closed Principle,
this base class is closed for modification but open for extension.

The design follows Interface Segregation Principle with focused responsibilities:
- Phase execution contract
- Prerequisite validation contract
- Clear separation of concerns

Examples:
    Creating a custom phase handler::

        class CustomPhaseHandler(PhaseHandler):
            async def execute(self, context: PhaseContext) -> PhaseResult:
                # Custom phase logic here
                return PhaseResult(
                    phase_name="custom_phase",
                    artifacts={"result": "Custom phase completed"},
                    metadata={"duration": 1.5}
                )

            def validate_prerequisites(self, context: PhaseContext) -> bool:
                # Custom validation logic
                return context.task_description is not None
"""

from abc import ABC, abstractmethod

from zenyth.core.types import PhaseContext, PhaseResult


class PhaseHandler(ABC):
    """Abstract base class for all SPARC phase implementations.

    This class defines the contract that all phase handlers must implement,
    following the Template Method pattern and Interface Segregation Principle.
    Each phase handler is responsible for executing a single SPARC methodology
    phase with clear input/output contracts.

    The class is designed following SOLID principles:
    - Single Responsibility: Focused solely on phase execution contract
    - Open/Closed: Closed for modification, open for extension via inheritance
    - Liskov Substitution: All subclasses must honor the exact same contract
    - Interface Segregation: Minimal, focused interface with no fat contracts
    - Dependency Inversion: Depends on abstract PhaseContext, not concrete types

    All concrete implementations must provide:
    1. Async execute method for phase logic
    2. Synchronous validate_prerequisites for input validation

    Examples:
        Implementing a specification phase::

            class SpecificationHandler(PhaseHandler):
                async def execute(self, context: PhaseContext) -> PhaseResult:
                    # Analyze requirements and create specification
                    specification = await self._analyze_requirements(context.task_description)

                    return PhaseResult(
                        phase_name="specification",
                        artifacts={"specification_document": specification},
                        next_phase="architecture",
                        metadata={"session_id": context.session_id}
                    )

                def validate_prerequisites(self, context: PhaseContext) -> bool:
                    # Specification requires a task description
                    return (context.task_description is not None and
                            len(context.task_description.strip()) > 0)

        Testing phase handler contract compliance::

            def test_phase_handler_contract():
                handler = MyPhaseHandler()
                assert isinstance(handler, PhaseHandler)
                assert hasattr(handler, 'execute')
                assert hasattr(handler, 'validate_prerequisites')

    Note:
        This class cannot be instantiated directly and will raise TypeError
        if instantiation is attempted. All methods marked with @abstractmethod
        must be implemented by concrete subclasses.

        Phase handlers should be stateless and thread-safe to support
        concurrent execution in homelab environments where resource efficiency
        is critical.
    """

    @abstractmethod
    async def execute(self, context: PhaseContext) -> PhaseResult:
        """Execute the phase logic with the provided context.

        This method contains the core logic for the specific SPARC phase,
        processing the input context and producing artifacts and results.
        Must be implemented by all concrete phase handlers.

        Following the Command pattern, this method encapsulates all the logic
        needed to execute a complete phase of the SPARC methodology, from
        input validation through artifact generation.

        Args:
            context: PhaseContext containing session information, task details,
                    previous phase results, and global artifacts. Provides all
                    the input data needed for phase execution.

        Returns:
            PhaseResult containing the phase name, generated artifacts,
            optional next phase identifier, and execution metadata. The result
            should be immutable and contain all output from the phase execution.

        Raises:
            NotImplementedError: If called on the abstract base class directly.
            ValueError: If context validation fails during execution.
            RuntimeError: If phase execution encounters unrecoverable errors.

        Examples:
            Basic phase execution::

                async def execute(self, context: PhaseContext) -> PhaseResult:
                    # Validate context first
                    if not self.validate_prerequisites(context):
                        raise ValueError("Prerequisites not met")

                    # Execute phase-specific logic
                    result = await self._process_phase(context)

                    # Return structured result
                    return PhaseResult(
                        phase_name=self.phase_name,
                        artifacts={"output": result},
                        metadata={"session_id": context.session_id}
                    )

            Phase with artifact dependencies::

                async def execute(self, context: PhaseContext) -> PhaseResult:
                    # Access previous phase artifacts
                    spec = context.global_artifacts.get("specification")

                    # Build on previous work
                    architecture = await self._design_architecture(spec)

                    return PhaseResult(
                        phase_name="architecture",
                        artifacts={"architecture_design": architecture},
                        next_phase="refinement"
                    )

        Note:
            Implementations should be async to support I/O operations like
            LLM calls, file operations, or network requests common in SPARC
            phases. The method should handle its own error recovery and
            provide meaningful error messages for debugging.

            Context should be treated as immutable - create new PhaseResult
            instances rather than modifying input context.
        """

    @abstractmethod
    def validate_prerequisites(self, context: PhaseContext) -> bool:
        """Validate that all prerequisites are met for phase execution.

        This method checks whether the provided context contains all necessary
        information and artifacts required for successful phase execution.
        Should be called before execute() to ensure graceful failure handling.

        Following the Fail Fast principle, this method enables early detection
        of invalid states before expensive phase execution begins. Helps with
        debugging and provides clear feedback on missing requirements.

        Args:
            context: PhaseContext to validate against phase requirements.
                    Contains session info, task description, previous results,
                    and global artifacts that may be needed for validation.

        Returns:
            bool: True if all prerequisites are satisfied and phase execution
                 can proceed safely. False if any required conditions are not
                 met and execution should be skipped or deferred.

        Examples:
            Basic task description validation::

                def validate_prerequisites(self, context: PhaseContext) -> bool:
                    return (context.task_description is not None and
                            len(context.task_description.strip()) > 0)

            Validation with artifact dependencies::

                def validate_prerequisites(self, context: PhaseContext) -> bool:
                    # Architecture phase needs specification
                    has_specification = "specification" in context.global_artifacts
                    has_task = context.task_description is not None
                    return has_specification and has_task

            Complex validation with multiple checks::

                def validate_prerequisites(self, context: PhaseContext) -> bool:
                    # Check session validity
                    if not context.session_id:
                        return False

                    # Check required artifacts from previous phases
                    required_artifacts = ["specification", "architecture"]
                    for artifact in required_artifacts:
                        if artifact not in context.global_artifacts:
                            return False

                    return True

        Note:
            This method should be fast and side-effect free since it may be
            called multiple times during workflow planning and validation.

            Should not raise exceptions - return False instead to indicate
            validation failure. The execute() method can provide more detailed
            error information if needed.

            Validation logic should be conservative - when in doubt, return
            False to prevent partial or incorrect phase execution.
        """
