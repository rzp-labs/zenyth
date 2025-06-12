"""Test SessionContext with artifacts storage.

This test validates that SessionContext properly stores and provides access to
complex artifacts including nested dictionaries.
"""

from zenyth.core.types import SessionContext


def test_session_context_with_artifacts() -> None:
    """Test SessionContext with artifacts storage."""
    artifacts = {"spec": "requirement doc", "code": "implementation"}
    context = SessionContext(session_id="test", task="test", artifacts=artifacts)
    assert context.artifacts == artifacts
    assert context.artifacts["spec"] == "requirement doc"

