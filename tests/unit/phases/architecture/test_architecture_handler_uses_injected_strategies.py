"""Test that handler uses injected strategy dependencies.

This test validates the Strategy pattern implementation and
Dependency Inversion Principle in ArchitectureHandler.
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


@pytest.mark.asyncio()
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
