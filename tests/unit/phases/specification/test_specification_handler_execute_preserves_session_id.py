"""Test that execute preserves session context.

This test validates context preservation following state management
best practices and Interface Segregation Principle.
"""

import pytest

from zenyth.core.types import PhaseContext
from zenyth.phases.specification import SpecificationHandler


@pytest.mark.asyncio()
async def test_specification_handler_execute_preserves_session_id() -> None:
    """Test that execute preserves session context.

    Validates context preservation following state management
    best practices and Interface Segregation Principle.
    """
    handler = SpecificationHandler()
    session_id = "preserve-session-test"
    context = PhaseContext(
        session_id=session_id,
        task_description="Test session preservation",
        previous_phases=[],
        global_artifacts={},
    )

    result = await handler.execute(context)

    # Should preserve session context in metadata
    assert "session_id" in result.metadata
    assert result.metadata["session_id"] == session_id
