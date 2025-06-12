"""Test SessionContext with optional fields.

This test validates that SessionContext properly defaults all optional fields
when only the required session_id and task are provided.
"""

from zenyth.core.types import SessionContext


def test_session_context_optional_fields() -> None:
    """Test SessionContext with optional fields."""
    context = SessionContext(session_id="test", task="test")
    assert context.artifacts == {}
    assert context.metadata == {}

