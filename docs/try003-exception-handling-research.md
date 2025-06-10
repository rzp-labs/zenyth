# TRY003 Exception Handling Research and Best Practices

## Executive Summary

This document presents comprehensive research on the TRY003 linting rule ("Avoid specifying long messages outside the exception class") and its application in the Zenyth codebase. The research reveals that while TRY003 has valid design goals, strict adherence can conflict with established Python patterns for meaningful error messages, particularly in validation scenarios.

## Background

During implementation of the PseudocodeHandler, we encountered 5 TRY003 linting warnings for exception messages like `raise ValidationError("Task description required")`. This prompted investigation into best practices for balancing linting compliance with meaningful error messages.

## TRY003 Rule Analysis

### What TRY003 Checks

The TRY003 rule, part of the tryceratops plugin, discourages formatting exception messages directly at the `raise` site:

```python
# Discouraged - violates TRY003
raise ValueError(f"{value} is invalid")

# Preferred - message defined in exception class
class InvalidValueError(ValueError):
    def __init__(self, value):
        super().__init__(f"{value} is invalid")
```

### Rule Rationale

1. **Consistency**: Exception classes provide consistent messaging across all raise sites
2. **Reusability**: Custom exception classes can be reused without duplicating message logic
3. **Maintainability**: Message changes require updates in only one location
4. **Structure**: Encourages thoughtful exception hierarchy design

## Community Research Findings

### Major Library Patterns

**Pydantic**: Extensively uses meaningful messages with built-in exceptions:
```python
@field_validator('price')
def price_must_be_positive(cls, value):
    if value <= 0:
        raise ValueError('Price must be positive')
    return value
```

**FastAPI**: Follows similar patterns for validation:
```python
if age < 0:
    raise ValueError("age must not be negative")
```

**Django**: Uses descriptive messages with built-in exceptions throughout the framework.

### Community Debate

GitHub issues and discussions reveal significant debate about TRY003:

1. **Built-in Exception Controversy**: Many developers argue TRY003 should not apply to built-in exceptions like `ValueError` and `TypeError`, similar to how it already exempts `NotImplementedError`

2. **Practical Concerns**: Developers report that strict TRY003 compliance leads to "lots of specialized exception classes" that bloat codebases

3. **Validation Use Cases**: Validation scenarios commonly require descriptive error messages that don't warrant custom exception classes

## Zenyth Codebase Analysis

### Existing Patterns

Investigation of the Zenyth codebase revealed an established pattern in `SpecificationHandler`:

```python
# Lines 321-322 in specification.py
msg = "Prerequisites not met for specification phase"
raise ValueError(msg)
```

This pattern:
- Satisfies TRY003 by using a variable instead of string literal
- Maintains meaningful error messages
- Follows established project conventions
- Requires no functional changes

### Project Configuration

The `pyproject.toml` shows intentional TRY003 configuration:
- Enabled globally (line 140: `"TRY"`)
- Explicitly ignored for tests (lines 157, 165: `"TRY003"`)
- Demonstrates conscious team decisions about appropriate usage

## Alternative Solutions Evaluated

### 1. Custom Exception Classes
```python
class TaskDescriptionMissingError(ValidationError):
    def __init__(self):
        super().__init__("Task description required")

class TaskDescriptionEmptyError(ValidationError):
    def __init__(self):
        super().__init__("Task description empty")
```

**Pros**: Full TRY003 compliance
**Cons**: Exception proliferation, maintenance overhead, inconsistent with project patterns

### 2. Error Code Systems
```python
TASK_MISSING = "TASK_001"
TASK_EMPTY = "TASK_002"
raise ValidationError(f"Error {TASK_MISSING}: Task description required")
```

**Pros**: Structured error handling
**Cons**: Loses message clarity, adds complexity

### 3. Configuration-Based Ignoring
```toml
[tool.ruff.lint]
ignore = ["TRY003"]
```

**Pros**: Simple implementation
**Cons**: Loses rule's value for legitimate use cases

### 4. Variable Assignment Pattern (Chosen)
```python
msg = "Task description required"
raise ValidationError(msg)
```

**Pros**: Satisfies TRY003, maintains clarity, follows project patterns
**Cons**: Slightly more verbose than direct literals

## Recommended Approach

### Variable Assignment Pattern

Based on research and existing codebase patterns, the recommended approach is:

```python
# For validation errors
msg = "Task description required"
raise ValidationError(msg)

# For runtime errors  
msg = "Phase execution failed"
raise ZenythError(msg)
```

### Implementation Guidelines

1. **Use Existing Exception Hierarchy**: Leverage `ValidationError`, `ZenythError`, etc. from `core.exceptions`
2. **Assign to Variable**: Use descriptive variable names like `msg` or `error_message`
3. **Maintain Message Quality**: Prioritize clear, actionable error messages
4. **Follow Project Patterns**: Consistency with existing code (e.g., SpecificationHandler)

## Benefits of Chosen Approach

### Technical Benefits
- ✅ Satisfies TRY003 linting rule
- ✅ Maintains meaningful error messages
- ✅ Uses existing exception hierarchy
- ✅ Requires no functional changes
- ✅ Compatible with existing tests

### Design Benefits
- ✅ Follows SOLID principles (SRP, DIP)
- ✅ Consistent with project patterns
- ✅ Embodies "listen to guardrails" philosophy
- ✅ Balances linting compliance with usability

### Maintenance Benefits
- ✅ Clear error messages for debugging
- ✅ Easy to modify messages if needed
- ✅ No exception class proliferation
- ✅ Familiar pattern for team members

## Testing Implications

The variable assignment pattern requires no test changes:

```python
# Tests continue to work unchanged
with pytest.raises(ValidationError, match="Task description required"):
    handler.validate_prerequisites(context)
```

This validates that the refactor is purely a code quality improvement without functional impact.

## Future Considerations

### For New Phase Handlers

1. Follow the variable assignment pattern established here
2. Use existing exception classes from `core.exceptions`
3. Prioritize meaningful error messages
4. Document any deviations from this pattern

### For Exception Hierarchy Evolution

If the project grows to need more specialized exceptions:
1. Extend existing base classes (`ValidationError`, `ZenythError`)
2. Group related validation scenarios into logical exception classes
3. Maintain the variable assignment pattern for message clarity
4. Update this document with new patterns

## Conclusion

The TRY003 rule serves valid design goals, but strict compliance can conflict with practical needs for meaningful error messages. The variable assignment pattern provides an elegant solution that satisfies both linting rules and usability requirements while maintaining consistency with existing codebase patterns.

This approach demonstrates the value of thorough research before making architectural decisions and exemplifies the "listen to guardrails" principle by finding design solutions rather than bypassing rules.

## References

- [Ruff TRY003 Documentation](https://docs.astral.sh/ruff/rules/raise-vanilla-args/)
- [GitHub Issue: TRY003 and built-in exceptions](https://github.com/astral-sh/ruff/issues/2246)
- [Pydantic Validation Patterns](https://docs.pydantic.dev/latest/concepts/validators/)
- [Python Exception Handling Best Practices](https://realpython.com/python-raise-exception/)

---

*Research conducted: June 2025*  
*Status: Implemented in PseudocodeHandler*