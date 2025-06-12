"""Test SessionContext with metadata.

This test validates that SessionContext properly stores metadata with multiple
fields and provides access to individual metadata values.
"""

from zenyth.core.types import SessionContext


def test_session_context_with_metadata() -> None:
    """Test SessionContext with metadata."""
    metadata = {"start_time": "2024-01-01", "user": "test_user"}
    context = SessionContext(session_id="test", task="test", metadata=metadata)
    assert context.metadata == metadata
    assert context.metadata["user"] == "test_user"
