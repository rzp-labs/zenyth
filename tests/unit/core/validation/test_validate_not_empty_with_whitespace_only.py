"""Test validate_not_empty with whitespace-only string.

This test validates that the Validator.validate_not_empty method correctly
treats strings containing only whitespace characters as empty.
"""

from zenyth.core.validation import ErrorCode, ValidationError, Validator


def test_validate_not_empty_with_whitespace_only() -> None:
    """Test validate_not_empty with whitespace-only string.

    Validates that whitespace-only strings are treated as empty.

    SOLID Assessment:
    - SRP: Test focused solely on whitespace handling
    - OCP: Whitespace logic extensible without modifying core validation
    """
    whitespace_strings = ["   ", "\t", "\n", "\r\n", "  \t  \n  "]

    for whitespace in whitespace_strings:
        result = Validator.validate_not_empty(whitespace, "test_field")
        assert isinstance(result, ValidationError)
        assert result.code == ErrorCode.EMPTY
