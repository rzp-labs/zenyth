"""Test that instance configuration meaningfully affects behavior.

This test validates that ArchitectureHandler respects instance-level
configuration following the Open/Closed Principle.
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


@pytest.mark.asyncio()
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
