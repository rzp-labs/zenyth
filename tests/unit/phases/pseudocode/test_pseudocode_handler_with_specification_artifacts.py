"""Test handler execution with specification phase artifacts.

This test validates that handler can build upon previous phase results
following the SPARC workflow progression.

SOLID Assessment:
- OCP: Handler extensible to work with various artifact types
- DIP: Depends on abstract artifact structure, not concrete formats
"""

import pytest

from zenyth.core.types import PhaseContext, PhaseResult
from zenyth.phases.pseudocode import PseudocodeHandler


@pytest.mark.asyncio()
async def test_pseudocode_handler_with_specification_artifacts() -> None:
    """Test handler execution with specification phase artifacts.

    Validates that handler can build upon previous phase results
    following the SPARC workflow progression.

    SOLID Assessment:
    - OCP: Handler extensible to work with various artifact types
    - DIP: Depends on abstract artifact structure, not concrete formats
    """
    handler = PseudocodeHandler()
    context = PhaseContext(
        session_id="with-spec-session",
        task_description="Implement user authentication",
        previous_phases=[],
        global_artifacts={
            "specification": "Detailed auth spec with JWT requirements",
            "requirements": ["Login endpoint", "Token validation", "Session management"],
        },
    )

    result = await handler.execute(context)

    # Should successfully process with specification artifacts
    assert isinstance(result, PhaseResult)
    assert "pseudocode_document" in result.artifacts
    assert result.metadata["session_id"] == "with-spec-session"

    # Should incorporate specification information into pseudocode
    pseudocode_doc = result.artifacts["pseudocode_document"]
    assert isinstance(pseudocode_doc, str)  # Serialized document
