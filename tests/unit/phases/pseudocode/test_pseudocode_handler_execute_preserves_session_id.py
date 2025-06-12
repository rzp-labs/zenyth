"""Test that execute method preserves session ID in result metadata.

This test validates session tracking and metadata consistency.

SOLID Assessment:
- SRP: Test focused solely on session ID preservation
- OCP: Session handling extensible without handler modification
"""

import pytest

from zenyth.core.types import PhaseContext
from zenyth.phases.pseudocode import PseudocodeHandler


@pytest.mark.asyncio()
async def test_pseudocode_handler_execute_preserves_session_id() -> None:
    """Test that execute method preserves session ID in result metadata.

    Validates session tracking and metadata consistency.

    SOLID Assessment:
    - SRP: Test focused solely on session ID preservation
    - OCP: Session handling extensible without handler modification
    """
    handler = PseudocodeHandler()
    session_id = "preserve-session-789"
    context = PhaseContext(
        session_id=session_id,
        task_description="Build microservice architecture",
        previous_phases=[],
        global_artifacts={},
    )

    result = await handler.execute(context)

    # Should preserve session ID in metadata
    assert "session_id" in result.metadata
    assert result.metadata["session_id"] == session_id
