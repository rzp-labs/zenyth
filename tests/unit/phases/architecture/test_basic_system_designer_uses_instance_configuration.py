"""Test that designer uses instance configuration meaningfully.

This test validates that BasicSystemDesigner respects instance-level
configuration following the Strategy pattern.
"""

import pytest

from zenyth.core.types import PhaseContext
from zenyth.phases.architecture import BasicSystemDesigner


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
async def test_basic_system_designer_uses_instance_configuration(
    phase_context_with_api: PhaseContext,
) -> None:
    """Test that designer uses instance configuration meaningfully."""
    # Designer with caching enabled
    designer_with_caching = BasicSystemDesigner(
        include_caching=True,
        prefer_microservices=False,
        min_component_threshold=1,
    )

    # Designer with caching disabled
    designer_without_caching = BasicSystemDesigner(
        include_caching=False,
        prefer_microservices=True,
        min_component_threshold=5,
    )

    analysis_with_caching = await designer_with_caching.analyze(
        phase_context_with_api.task_description,
        phase_context_with_api.global_artifacts,
    )
    analysis_without_caching = await designer_without_caching.analyze(
        phase_context_with_api.task_description,
        phase_context_with_api.global_artifacts,
    )

    # Results should differ based on configuration
    assert analysis_with_caching != analysis_without_caching
