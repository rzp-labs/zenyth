"""Check for common non-idempotent patterns in Python code."""

from __future__ import annotations

import ast
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def check_for_io_operations(node: ast.FunctionDef) -> list[str]:
    """Check for I/O operations in a function."""
    violations = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == "open":
            violations.append(f"{node.name}: Idempotent function contains I/O operation")
    return violations


def check_for_randomness(node: ast.FunctionDef) -> list[str]:
    """Check for random operations in a function."""
    violations = []
    for child in ast.walk(node):
        if isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name) and child.value.id == "random":
            violations.append(f"{node.name}: Idempotent function uses random")
    return violations


def check_for_time_operations(node: ast.FunctionDef) -> list[str]:
    """Check for time-dependent operations in a function."""
    violations = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Attribute) and isinstance(child.func.value, ast.Name):
                if child.func.value.id in {"time", "datetime"}:
                    violations.append(f"{node.name}: Idempotent function uses time-dependent operations")
            elif isinstance(child.func, ast.Name) and child.func.id in {"time", "datetime"}:
                violations.append(f"{node.name}: Idempotent function uses time-dependent operations")
    return violations


def find_idempotency_violations(tree: ast.AST) -> list[str]:
    """Find idempotency violations in an AST."""
    violations: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        # Check if function is marked idempotent
        is_idempotent = any(isinstance(dec, ast.Name) and dec.id == "idempotent" for dec in node.decorator_list)

        if not is_idempotent:
            continue

        # Check for various violations
        violations.extend(check_for_io_operations(node))
        violations.extend(check_for_randomness(node))
        violations.extend(check_for_time_operations(node))

    return violations


def check_file(filepath: str | Path) -> list[str]:
    """Check a file for idempotency violations."""
    with Path(filepath).open(encoding="utf-8") as f:
        tree = ast.parse(f.read())

    return find_idempotency_violations(tree)


def main(files: Sequence[str]) -> int:
    """Check multiple files for idempotency violations."""
    violations: list[str] = []

    for file in files:
        try:
            violations.extend(check_file(file))
        except (OSError, SyntaxError) as e:
            logger.error("Failed to check %s: %s", file, e)
            return 1

    if violations:
        for violation in violations:
            logger.error(violation)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
