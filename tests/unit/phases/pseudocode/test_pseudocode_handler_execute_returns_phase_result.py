"""Test that execute method returns proper PhaseResult.

This test validates interface contract compliance and proper result structure.

SOLID Assessment:
- LSP: Must return PhaseResult as per PhaseHandler contract
- SRP: Test focused solely on return type validation
"""

import pytest

from zenyth.core.types import PhaseContext, PhaseResult, SPARCPhase
from zenyth.phases.pseudocode import PseudocodeHandler


@pytest.mark.asyncio()
async def test_pseudocode_handler_execute_returns_phase_result() -> None:
    """Test that execute method returns proper PhaseResult.

    Validates interface contract compliance and proper result structure.

    SOLID Assessment:
    - LSP: Must return PhaseResult as per PhaseHandler contract
    - SRP: Test focused solely on return type validation
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="test-session-123",
        task_description="Implement user authentication system",
        previous_phases=[],
        global_artifacts={},
    )

    result = await handler.execute(context)

    # Should return PhaseResult
    assert isinstance(result, PhaseResult)
    assert result.phase_name == SPARCPhase.PSEUDOCODE.value
    assert "pseudocode_document" in result.artifacts
    assert result.metadata["session_id"] == context.session_id
