"""Test SessionContext supports equality comparison.

This test validates that SessionContext instances with the same field values
are considered equal using the == operator.
"""

from zenyth.core.types import SessionContext


def test_session_context_supports_equality_comparison() -> None:
    """Test SessionContext supports equality comparison."""
    context1 = SessionContext(session_id="test", task="task1")
    context2 = SessionContext(session_id="test", task="task1")
    assert context1 == context2

