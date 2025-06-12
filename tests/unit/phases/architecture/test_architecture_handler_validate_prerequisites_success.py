"""Test prerequisite validation with specification artifacts.

This test validates that ArchitectureHandler properly validates
prerequisites following the Single Responsibility Principle.
"""

from unittest.mock import Mock

import pytest

from zenyth.core.types import PhaseContext
from zenyth.phases.architecture import (
    ArchitectureDiagrammer,
    ArchitectureHandler,
    SystemDesigner,
)


@pytest.fixture()
def mock_system_designer() -> SystemDesigner:
    """Create mock SystemDesigner for testing."""
    designer = Mock(spec=SystemDesigner)
    designer.analyze.return_value = {
        "components": ["API Service", "Database"],
        "relationships": ["API Service->Database"],
        "complexity_score": 0.3,
    }
    return designer


@pytest.fixture()
def mock_architecture_diagrammer() -> ArchitectureDiagrammer:
    """Create mock ArchitectureDiagrammer for testing."""
    diagrammer = Mock(spec=ArchitectureDiagrammer)
    diagrammer.generate.return_value = {
        "diagram_type": "component",
        "diagram_content": "```mermaid\ngraph TD\n```",
        "diagram_metadata": {"tool": "mermaid"},
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
            },
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


def test_architecture_handler_validate_prerequisites_success(
    architecture_handler: ArchitectureHandler,
    phase_context: PhaseContext,
) -> None:
    """Test prerequisite validation with specification artifacts."""
    is_valid = architecture_handler.validate_prerequisites(phase_context)
    assert is_valid is True
