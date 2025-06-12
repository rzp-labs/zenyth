"""Test SessionContext stores metadata field when provided.

This test validates that SessionContext properly accepts and stores metadata
information when provided during initialization.
"""

from zenyth.core.types import SessionContext


def test_session_context_stores_metadata_when_provided() -> None:
    """Test SessionContext stores metadata field when provided."""
    metadata = {"start_time": "2024-01-01"}
    context = SessionContext(session_id="test", task="test", metadata=metadata)
    assert context.metadata == metadata
