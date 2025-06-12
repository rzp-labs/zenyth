"""Test that SessionContext is immutable after creation.

This test validates that SessionContext enforces immutability by raising
AttributeError when attempting to modify any field after initialization.
"""

import pytest

from zenyth.core.types import SessionContext


def test_session_context_immutable() -> None:
    """Test that SessionContext is immutable after creation."""
    context = SessionContext(session_id="test", task="test")

    # Should raise AttributeError when trying to modify
    with pytest.raises(AttributeError):
        context.session_id = "modified"
