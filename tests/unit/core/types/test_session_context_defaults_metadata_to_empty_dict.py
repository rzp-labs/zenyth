"""Test SessionContext defaults metadata to empty dict when not provided.

This test validates that SessionContext properly defaults the optional metadata
field to an empty dictionary when not explicitly provided during initialization.
"""

from zenyth.core.types import SessionContext


def test_session_context_defaults_metadata_to_empty_dict() -> None:
    """Test SessionContext defaults metadata to empty dict when not provided."""
    context = SessionContext(session_id="test", task="test")
    assert context.metadata == {}

