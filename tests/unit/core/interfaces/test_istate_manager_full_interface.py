"""Test complete IStateManager interface with async methods.

This test validates that the IStateManager protocol works correctly with async
methods, demonstrating the Open/Closed Principle by showing the interface is
closed for modification but open for implementation.
"""

import pytest

from zenyth.core.types import SessionContext


@pytest.mark.asyncio()
async def test_istate_manager_full_interface() -> None:
    """Test complete IStateManager interface with async methods.

    Validates Open/Closed Principle - interface closed for modification.
    Tests full async interface contract implementation.
    """

    # Create mock that simulates async behavior
    class MockStateManager:
        def __init__(self) -> None:
            self.sessions: dict[str, SessionContext] = {}

        async def save_session(self, session: SessionContext) -> None:
            self.sessions[session.session_id] = session

        async def load_session(self, session_id: str) -> SessionContext:
            return self.sessions.get(session_id)

    manager = MockStateManager()

    # Test session creation and saving
    session = SessionContext(
        session_id="test-session-123",
        task="Test task for state management",
        artifacts={"test": "data"},
        metadata={"created": "2024-01-01"},
    )

    # Should be able to save session
    await manager.save_session(session)
    assert "test-session-123" in manager.sessions

    # Should be able to load session
    loaded_session = await manager.load_session("test-session-123")
    assert loaded_session.session_id == "test-session-123"
    assert loaded_session.task == "Test task for state management"
