"""Test prerequisite validation fails without specification.

This test validates that ArchitectureHandler properly fails
validation when required artifacts are missing, following
defensive programming principles.
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
    return Mock(spec=SystemDesigner)


@pytest.fixture()
def mock_architecture_diagrammer() -> ArchitectureDiagrammer:
    """Create mock ArchitectureDiagrammer for testing."""
    return Mock(spec=ArchitectureDiagrammer)


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


def test_architecture_handler_validate_prerequisites_failure(
    architecture_handler: ArchitectureHandler,
) -> None:
    """Test prerequisite validation fails without specification."""
    empty_context = PhaseContext(
        session_id="test-session",
        task_description="Design system",
        previous_phases=[],
        global_artifacts={},
    )

    is_valid = architecture_handler.validate_prerequisites(empty_context)
    assert is_valid is False
