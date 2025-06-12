"""Test SessionContext accepts session_id field.

This test validates that SessionContext properly accepts and stores the
session_id field, which is a required field for session tracking.
"""

from zenyth.core.types import SessionContext


def test_session_context_accepts_session_id_field() -> None:
    """Test SessionContext accepts session_id field."""
    context = SessionContext(session_id="test-session", task="test")
    assert context.session_id == "test-session"

