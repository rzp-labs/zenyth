"""Test that execute returns proper PhaseResult.

This test validates that the ArchitectureHandler follows the PhaseHandler
contract and returns valid PhaseResult following SOLID principles.
"""

from unittest.mock import Mock

import pytest

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
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
async def test_architecture_handler_execute_returns_phase_result(
    architecture_handler: ArchitectureHandler,
    phase_context: PhaseContext,
) -> None:
    """Test that execute returns proper PhaseResult."""
    result = await architecture_handler.execute(phase_context)

    assert isinstance(result, PhaseResult)
    assert result.phase_name == SPARCPhase.ARCHITECTURE.value
    assert "architecture_document" in result.artifacts
    assert "error" not in result.metadata
