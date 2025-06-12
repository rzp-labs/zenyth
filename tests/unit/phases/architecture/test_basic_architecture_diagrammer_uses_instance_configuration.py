"""Test that diagrammer uses instance configuration meaningfully.

This test validates that BasicArchitectureDiagrammer respects
instance-level configuration following the Strategy pattern.
"""

from typing import Any

import pytest

from zenyth.phases.architecture import BasicArchitectureDiagrammer


@pytest.fixture()
def system_analysis() -> dict[str, Any]:
    """Create sample system analysis."""
    return {
        "components": ["API Gateway", "Auth Service", "Database"],
        "relationships": ["API Gateway->Auth Service", "Auth Service->Database"],
        "complexity_score": 0.6,
    }


@pytest.mark.asyncio()
async def test_basic_architecture_diagrammer_uses_instance_configuration(
    system_analysis: dict[str, Any],
) -> None:
    """Test that diagrammer uses instance configuration meaningfully."""
    # Diagrammer with metadata enabled
    diagrammer_with_metadata = BasicArchitectureDiagrammer(
        diagram_format="mermaid",
        include_metadata=True,
        max_components_per_diagram=5,
    )

    # Diagrammer with metadata disabled
    diagrammer_without_metadata = BasicArchitectureDiagrammer(
        diagram_format="plantuml",
        include_metadata=False,
        max_components_per_diagram=3,
    )

    diagram_with_metadata = await diagrammer_with_metadata.generate(
        "Test task",
        system_analysis,
        "session-123",
    )
    diagram_without_metadata = await diagrammer_without_metadata.generate(
        "Test task",
        system_analysis,
        "session-123",
    )

    # Results should differ based on configuration
    assert diagram_with_metadata != diagram_without_metadata
