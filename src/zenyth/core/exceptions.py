"""Custom exception classes for Zenyth SPARC orchestration system.

This module defines the exception hierarchy used throughout the Zenyth system,
providing clear contracts for error handling and enabling consistent exception
management across different components and implementations.

The exception hierarchy follows Python best practices with a base exception
class and specialized exceptions for different error categories. This enables
fine-grained error handling while maintaining clear inheritance relationships.

Examples:
    Handling storage-related exceptions::

        try:
            await state_manager.save_session(session)
        except StorageError as e:
            logger.error(f"Storage operation failed: {e}")
            # Implement fallback strategy
        except ValidationError as e:
            logger.error(f"Invalid session data: {e}")
            # Fix data and retry

    Handling session retrieval exceptions::

        try:
            session = await state_manager.load_session(session_id)
        except SessionNotFoundError:
            # Create new session
            session = create_new_session(session_id)
        except CorruptionError as e:
            logger.error(f"Session data corrupted: {e}")
            # Implement recovery strategy
"""


class ZenythError(Exception):
    """Base exception class for all Zenyth-specific errors.

    Provides a common base for all custom exceptions in the Zenyth system,
    enabling broad exception handling when needed while allowing for
    specific exception types for fine-grained error management.

    All custom exceptions in the Zenyth system should inherit from this
    base class to maintain consistency and enable hierarchical exception
    handling patterns.

    Attributes:
        message: Human-readable error message describing the issue
        details: Optional additional context or diagnostic information
    """

    def __init__(self, message: str, details: str | None = None):
        """Initialize base Zenyth exception.

        Args:
            message: Human-readable error message describing the issue
            details: Optional additional context or diagnostic information
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class StorageError(ZenythError):
    """Exception raised when storage operations fail.

    Indicates issues with persisting or retrieving data from storage backends
    such as databases, file systems, or cloud storage services. This includes
    network connectivity issues, permission problems, or storage service
    unavailability.

    Common scenarios:
        - Database connection failures
        - File system permission errors
        - Cloud storage service unavailability
        - Disk space exhaustion
        - Network connectivity issues

    Examples:
        Database storage failure::

            raise StorageError(
                "Failed to save session to database",
                details="Connection timeout after 30 seconds"
            )

        File system storage failure::

            raise StorageError(
                "Cannot write session file",
                details="Permission denied: /var/lib/zenyth/sessions/"
            )
    """


class ValidationError(ZenythError):
    """Exception raised when data validation fails.

    Indicates that provided data does not meet the expected format, constraints,
    or business rules. This includes schema validation failures, missing required
    fields, invalid data types, or constraint violations.

    Common scenarios:
        - Missing required session fields
        - Invalid data types in session context
        - Constraint violations (e.g., session_id format)
        - Schema validation failures
        - Business rule violations

    Examples:
        Missing required field::

            raise ValidationError(
                "Session validation failed",
                details="Required field 'session_id' is missing"
            )

        Invalid data format::

            raise ValidationError(
                "Invalid session data format",
                details="Field 'artifacts' must be a dictionary, got list"
            )
    """


class SessionNotFoundError(ZenythError):
    """Exception raised when a requested session cannot be found.

    Indicates that a session with the specified identifier does not exist
    in the storage backend. This is typically raised during session retrieval
    operations when the session_id is not found.

    Common scenarios:
        - Session ID does not exist in storage
        - Session was deleted or expired
        - Incorrect session ID provided
        - Storage backend corrupted

    Examples:
        Session not found in storage::

            raise SessionNotFoundError(
                f"Session '{session_id}' not found",
                details="No session file exists in storage directory"
            )

        Session expired or deleted::

            raise SessionNotFoundError(
                f"Session '{session_id}' no longer available",
                details="Session may have been expired or manually deleted"
            )
    """


class CorruptionError(ZenythError):
    """Exception raised when stored data is corrupted or invalid.

    Indicates that data retrieved from storage is malformed, corrupted, or
    cannot be properly deserialized. This suggests storage integrity issues
    or incompatible data formats from different system versions.

    Common scenarios:
        - Corrupted session files
        - Incompatible data format versions
        - Partial write operations
        - Storage medium failures
        - Manual data modification

    Examples:
        Corrupted session file::

            raise CorruptionError(
                "Session data is corrupted",
                details="JSON decode error: Unexpected end of file"
            )

        Incompatible data version::

            raise CorruptionError(
                "Session data format is incompatible",
                details="Data version 2.0 not supported by current system"
            )
    """


class PhaseExecutionFailedError(ZenythError):
    """Exception raised when phase execution encounters an unrecoverable error."""

    def __init__(self) -> None:
        super().__init__("Phase execution failed")
