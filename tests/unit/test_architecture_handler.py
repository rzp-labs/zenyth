"""Tests for ArchitectureHandler following TDD methodology and SOLID principles.

This test suite validates the SOLID-compliant ArchitectureHandler implementation
with Strategy pattern, dependency injection, and meaningful instance configuration.

Following the established pattern from SpecificationHandler tests.
"""

from typing import Any
from unittest.mock import Mock

import pytest

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.phases.architecture import (
    ArchitectureDiagrammer,
    ArchitectureHandler,
    BasicArchitectureDiagrammer,
    BasicSystemDesigner,
    SystemDesigner,
)


class TestArchitectureHandler:
    """Test suite for ArchitectureHandler SOLID compliance."""


@pytest.fixture()
def mock_system_designer() -> SystemDesigner:
    """Create mock SystemDesigner for testing."""
    designer = Mock(spec=SystemDesigner)
    designer.analyze.return_value = {
        "components": ["API Service", "Database", "Cache", "Auth Service", "Logger", "Monitor"],
        "relationships": [
            "API Service->Database",
            "API Service->Cache",
            "API Service->Auth Service",
        ],
        "complexity_score": 0.6,
    }
    return designer


@pytest.fixture()
def mock_architecture_diagrammer() -> ArchitectureDiagrammer:
    """Create mock ArchitectureDiagrammer for testing."""
    diagrammer = Mock(spec=ArchitectureDiagrammer)
    diagrammer.generate.return_value = {
        "diagram_type": "component",
        "diagram_content": (
            """```mermaid
graph TD
A[API] --> B[Database]
```"""
        ),
        "diagram_metadata": {"tool": "mermaid", "components": 3},
    }
    return diagrammer


@pytest.fixture()
def phase_context() -> PhaseContext:
    """Create test PhaseContext with specification artifacts."""
    return PhaseContext(
        session_id="test-session",
        task_description="Design user authentication system",
        previous_phases=[],
        global_artifacts={
            "specification": {
                "requirements": ["user login", "session management"],
                "api_contracts": ["POST /auth/login", "GET /auth/profile"],
                "data_models": ["User", "Session"],
            }
        },
    )


@pytest.fixture()
def architecture_handler(
    mock_system_designer: SystemDesigner,
    mock_architecture_diagrammer: ArchitectureDiagrammer,
) -> ArchitectureHandler:
    """Create ArchitectureHandler with injected dependencies."""
    return ArchitectureHandler(
        system_designer=mock_system_designer,
        architecture_diagrammer=mock_architecture_diagrammer,
        min_components=2,
        include_performance_analysis=True,
        track_design_patterns=True,
    )


async def test_architecture_handler_execute_returns_phase_result(
    architecture_handler: ArchitectureHandler, phase_context: PhaseContext
) -> None:
    """Test that execute returns proper PhaseResult."""
    result = await architecture_handler.execute(phase_context)

    assert isinstance(result, PhaseResult)
    assert result.phase_name == SPARCPhase.ARCHITECTURE.value
    assert "architecture_document" in result.artifacts
    assert "error" not in result.metadata


def test_architecture_handler_validate_prerequisites_success(
    architecture_handler: ArchitectureHandler, phase_context: PhaseContext
):
    """Test prerequisite validation with specification artifacts."""
    is_valid = architecture_handler.validate_prerequisites(phase_context)
    assert is_valid is True


def test_architecture_handler_validate_prerequisites_failure(
    architecture_handler: ArchitectureHandler,
):
    """Test prerequisite validation fails without specification."""
    empty_context = PhaseContext(
        session_id="test-session",
        task_description="Design system",
        previous_phases=[],
        global_artifacts={},
    )

    is_valid = architecture_handler.validate_prerequisites(empty_context)
    assert is_valid is False


async def test_architecture_handler_uses_injected_strategies(
    architecture_handler: ArchitectureHandler,
    phase_context: PhaseContext,
    mock_system_designer: SystemDesigner,
    mock_architecture_diagrammer: ArchitectureDiagrammer,
) -> None:
    """Test that handler uses injected strategy dependencies."""
    await architecture_handler.execute(phase_context)

    mock_system_designer.analyze.assert_called_once()
    mock_architecture_diagrammer.generate.assert_called_once()


async def test_architecture_handler_instance_configuration_affects_behavior(
    mock_system_designer: SystemDesigner,
    mock_architecture_diagrammer: ArchitectureDiagrammer,
    phase_context: PhaseContext,
) -> None:
    """Test that instance configuration meaningfully affects behavior."""
    handler_with_different_config = ArchitectureHandler(
        system_designer=mock_system_designer,
        architecture_diagrammer=mock_architecture_diagrammer,
        min_components=5,
        include_performance_analysis=False,
        track_design_patterns=False,
    )

    result = await handler_with_different_config.execute(phase_context)

    # Configuration should affect result metadata
    assert "min_components" in result.metadata
    assert result.metadata["min_components"] == 5
    assert result.metadata["include_performance_analysis"] is False


@pytest.fixture()
def basic_system_designer() -> BasicSystemDesigner:
    """Create BasicSystemDesigner with default configuration."""
    return BasicSystemDesigner(
        include_caching=True, prefer_microservices=False, min_component_threshold=2
    )


@pytest.fixture()
def phase_context_with_api() -> PhaseContext:
    """Create PhaseContext with API specification."""
    return PhaseContext(
        session_id="test-session",
        task_description="Design REST API",
        previous_phases=[],
        global_artifacts={
            "specification": {
                "api_contracts": ["POST /users", "GET /users/{id}"],
                "data_models": ["User", "Profile"],
                "requirements": ["user management", "data persistence"],
            }
        },
    )


async def test_basic_system_designer_uses_instance_configuration(
    phase_context_with_api: PhaseContext,
) -> None:
    """Test that designer uses instance configuration meaningfully."""
    # Designer with caching enabled
    designer_with_caching = BasicSystemDesigner(
        include_caching=True, prefer_microservices=False, min_component_threshold=1
    )

    # Designer with caching disabled
    designer_without_caching = BasicSystemDesigner(
        include_caching=False, prefer_microservices=True, min_component_threshold=5
    )

    analysis_with_caching = await designer_with_caching.analyze(
        phase_context_with_api.task_description, phase_context_with_api.global_artifacts
    )
    analysis_without_caching = await designer_without_caching.analyze(
        phase_context_with_api.task_description, phase_context_with_api.global_artifacts
    )

    # Results should differ based on configuration
    assert analysis_with_caching != analysis_without_caching


async def test_basic_system_designer_analyze_identifies_components(
    basic_system_designer: BasicSystemDesigner, phase_context_with_api: PhaseContext
) -> None:
    """Test that analyzer identifies system components from specification."""
    analysis = await basic_system_designer.analyze(
        phase_context_with_api.task_description, phase_context_with_api.global_artifacts
    )

    assert "components" in analysis
    assert "relationships" in analysis
    assert "complexity_score" in analysis
    assert isinstance(analysis["components"], list)
    assert len(analysis["components"]) > 0


@pytest.fixture()
def basic_architecture_diagrammer() -> BasicArchitectureDiagrammer:
    """Create BasicArchitectureDiagrammer with configuration."""
    return BasicArchitectureDiagrammer(
        diagram_format="mermaid", include_metadata=True, max_components_per_diagram=10
    )


@pytest.fixture()
def system_analysis() -> dict[str, Any]:
    """Create sample system analysis."""
    return {
        "components": ["API Gateway", "Auth Service", "Database"],
        "relationships": ["API Gateway->Auth Service", "Auth Service->Database"],
        "complexity_score": 0.6,
    }


async def test_basic_architecture_diagrammer_uses_instance_configuration(
    system_analysis: dict[str, Any],
) -> None:
    """Test that diagrammer uses instance configuration meaningfully."""
    # Diagrammer with metadata enabled
    diagrammer_with_metadata = BasicArchitectureDiagrammer(
        diagram_format="mermaid", include_metadata=True, max_components_per_diagram=5
    )

    # Diagrammer with metadata disabled
    diagrammer_without_metadata = BasicArchitectureDiagrammer(
        diagram_format="plantuml", include_metadata=False, max_components_per_diagram=3
    )

    diagram_with_metadata = await diagrammer_with_metadata.generate(
        "Test task", system_analysis, "session-123"
    )
    diagram_without_metadata = await diagrammer_without_metadata.generate(
        "Test task", system_analysis, "session-123"
    )

    # Results should differ based on configuration
    assert diagram_with_metadata != diagram_without_metadata


async def test_basic_architecture_diagrammer_creates_diagram(
    basic_architecture_diagrammer: BasicArchitectureDiagrammer,
    system_analysis: dict[str, Any],
) -> None:
    """Test that diagrammer creates diagram from analysis."""
    diagram = await basic_architecture_diagrammer.generate(
        "Test task", system_analysis, "session-123"
    )

    assert "diagram_type" in diagram
    assert "diagram_content" in diagram
    assert "diagram_metadata" in diagram
    assert isinstance(diagram["diagram_content"], str)
    assert len(diagram["diagram_content"]) > 0
