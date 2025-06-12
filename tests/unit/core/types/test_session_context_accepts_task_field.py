"""Test SessionContext accepts task field.

This test validates that SessionContext properly accepts and stores the
task field, which is a required field for session tracking.
"""

from zenyth.core.types import SessionContext


def test_session_context_accepts_task_field() -> None:
    """Test SessionContext accepts task field."""
    context = SessionContext(session_id="test", task="test task")
    assert context.task == "test task"
