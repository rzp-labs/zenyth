"""Test SessionContext initialization with required fields.

This test validates that SessionContext properly initializes with both
required fields (session_id and task).
"""

from zenyth.core.types import SessionContext


def test_session_context_initialization() -> None:
    """Test SessionContext initialization with required fields."""
    context = SessionContext(session_id="test-session", task="test task")
    assert context.session_id == "test-session"
    assert context.task == "test task"

