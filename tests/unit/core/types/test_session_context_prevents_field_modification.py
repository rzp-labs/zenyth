"""Test SessionContext prevents modification of fields after creation.

This test validates that SessionContext is immutable (frozen dataclass) and
raises AttributeError when attempting to modify fields after initialization.
"""

import pytest

from zenyth.core.types import SessionContext


def test_session_context_prevents_field_modification() -> None:
    """Test SessionContext prevents modification of fields after creation."""
    context = SessionContext(session_id="test", task="test")

    with pytest.raises(AttributeError):
        context.session_id = "modified"

