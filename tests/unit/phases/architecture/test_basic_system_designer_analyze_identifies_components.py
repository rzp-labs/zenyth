"""Test that analyzer identifies system components from specification.

This test validates that BasicSystemDesigner properly analyzes
specifications and identifies components following Single Responsibility Principle.
"""

import pytest

from zenyth.core.types import PhaseContext
from zenyth.phases.architecture import BasicSystemDesigner


@pytest.fixture()
def basic_system_designer() -> BasicSystemDesigner:
    """Create BasicSystemDesigner with default configuration."""
    return BasicSystemDesigner(
        include_caching=True,
        prefer_microservices=False,
        min_component_threshold=2,
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
            },
        },
    )


@pytest.mark.asyncio()
async def test_basic_system_designer_analyze_identifies_components(
    basic_system_designer: BasicSystemDesigner,
    phase_context_with_api: PhaseContext,
) -> None:
    """Test that analyzer identifies system components from specification."""
    analysis = await basic_system_designer.analyze(
        phase_context_with_api.task_description,
        phase_context_with_api.global_artifacts,
    )

    assert "components" in analysis
    assert "relationships" in analysis
    assert "complexity_score" in analysis
    assert isinstance(analysis["components"], list)
    assert len(analysis["components"]) > 0
