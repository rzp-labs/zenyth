"""Test execute method with realistic task context.

This test validates Single Responsibility Principle - focused on
specification phase logic only.
"""

import pytest

from zenyth.core.types import PhaseContext, SPARCPhase
from zenyth.phases.specification import SpecificationHandler


@pytest.mark.asyncio()
async def test_specification_handler_execute_with_task_context() -> None:
    """Test execute method with realistic task context.

    Validates Single Responsibility Principle - focused on
    specification phase logic only.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="spec-test-session",
        task_description="Build REST API for user management",
        previous_phases=[],
        global_artifacts={"project_type": "web_api"},
    )

    result = await handler.execute(context)

    # Should produce specification artifacts
    assert result.phase_name == SPARCPhase.SPECIFICATION.value
    assert isinstance(result.artifacts, dict)
    assert isinstance(result.metadata, dict)
