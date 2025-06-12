"""Test that execute method returns proper PhaseResult.

This test validates interface contract compliance and return type
following Liskov Substitution Principle.
"""

import pytest

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.phases.specification import SpecificationHandler


@pytest.mark.asyncio()
async def test_specification_handler_execute_returns_phase_result() -> None:
    """Test that execute method returns proper PhaseResult.

    Validates interface contract compliance and return type
    following Liskov Substitution Principle.
    """
    handler = SpecificationHandler()
    context = PhaseContext(
        session_id="test-session",
        task_description="Create user authentication system",
        previous_phases=[],
        global_artifacts={},
    )

    # Execute should return PhaseResult
    result = await handler.execute(context)
    assert isinstance(result, PhaseResult)
    assert result.phase_name == SPARCPhase.SPECIFICATION.value
