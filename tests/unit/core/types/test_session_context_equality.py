"""Test SessionContext equality comparison.

This test validates that SessionContext equality comparison works correctly
for instances with the same and different field values.
"""

from zenyth.core.types import SessionContext


def test_session_context_equality() -> None:
    """Test SessionContext equality comparison."""
    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task1")
    context3 = SessionContext(session_id="test", task="task2")

    assert context1 == context2
    assert context1 != context3

