"""Test that diagrammer creates diagram from analysis.

This test validates that BasicArchitectureDiagrammer properly
generates diagrams from system analysis following Single Responsibility Principle.
"""

from typing import Any

import pytest

from zenyth.phases.architecture import BasicArchitectureDiagrammer


@pytest.fixture()
def basic_architecture_diagrammer() -> BasicArchitectureDiagrammer:
    """Create BasicArchitectureDiagrammer with configuration."""
    return BasicArchitectureDiagrammer(
        diagram_format="mermaid",
        include_metadata=True,
        max_components_per_diagram=10,
    )


@pytest.fixture()
def system_analysis() -> dict[str, Any]:
    """Create sample system analysis."""
    return {
        "components": ["API Gateway", "Auth Service", "Database"],
        "relationships": ["API Gateway->Auth Service", "Auth Service->Database"],
        "complexity_score": 0.6,
    }


@pytest.mark.asyncio()
async def test_basic_architecture_diagrammer_creates_diagram(
    basic_architecture_diagrammer: BasicArchitectureDiagrammer,
    system_analysis: dict[str, Any],
) -> None:
    """Test that diagrammer creates diagram from analysis."""
    diagram = await basic_architecture_diagrammer.generate(
        "Test task",
        system_analysis,
        "session-123",
    )

    assert "diagram_type" in diagram
    assert "diagram_content" in diagram
    assert "diagram_metadata" in diagram
    assert isinstance(diagram["diagram_content"], str)
    assert len(diagram["diagram_content"]) > 0
