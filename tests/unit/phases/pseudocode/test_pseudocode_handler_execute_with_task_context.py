"""Test execute method with specific task context processing.

This test validates that handler properly processes task description and
generates appropriate pseudocode artifacts.

SOLID Assessment:
- SRP: Handler coordinates but delegates analysis/generation to strategies
- DIP: Uses abstract interfaces for task processing
"""

import pytest

from zenyth.core.types import PhaseContext, SPARCPhase
from zenyth.phases.pseudocode import PseudocodeHandler


@pytest.mark.asyncio()
async def test_pseudocode_handler_execute_with_task_context() -> None:
    """Test execute method with specific task context processing.

    Validates that handler properly processes task description and
    generates appropriate pseudocode artifacts.

    SOLID Assessment:
    - SRP: Handler coordinates but delegates analysis/generation to strategies
    - DIP: Uses abstract interfaces for task processing
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="pseudocode-session-456",
        task_description="Create REST API for user management",
        previous_phases=[],
        global_artifacts={"specification": "User management API spec"},
        metadata={"priority": "high"},
    )

    result = await handler.execute(context)

    # Should process task context appropriately
    assert result.phase_name == SPARCPhase.PSEUDOCODE.value
    assert "pseudocode_document" in result.artifacts
    assert result.metadata["session_id"] == "pseudocode-session-456"

    # Should use task description in processing
    pseudocode_doc = result.artifacts["pseudocode_document"]
    assert "REST API" in pseudocode_doc or "user management" in pseudocode_doc.lower()
