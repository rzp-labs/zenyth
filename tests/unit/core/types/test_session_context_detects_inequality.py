"""Test SessionContext detects inequality correctly.

This test validates that SessionContext instances with different field values
are correctly identified as not equal using the != operator.
"""

from zenyth.core.types import SessionContext


def test_session_context_detects_inequality() -> None:
    """Test SessionContext detects inequality correctly."""
    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task2")
    assert context1 != context2
