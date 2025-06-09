"""Check for atomicity violations in Python code."""

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


def find_atomic_violations(tree: ast.AST) -> list[str]:
    """Find atomicity violations in an AST."""
    violations: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        # Check if function is marked atomic
        is_atomic = any(isinstance(dec, ast.Name) and dec.id == "atomic" for dec in node.decorator_list)

        if not is_atomic:
            continue

        # Check for violations in atomic functions
        for child in ast.walk(node):
            if isinstance(child, ast.Yield | ast.YieldFrom):
                violations.append(f"{node.name}: Atomic function cannot be a generator")
            elif isinstance(child, ast.AsyncFunctionDef):
                violations.append(f"{node.name}: Atomic function cannot contain async operations")
            elif _is_subprocess_call(child):
                violations.append(f"{node.name}: Atomic function contains subprocess call")

    return violations


def _is_subprocess_call(node: ast.AST) -> bool:
    """Check if node is a subprocess call."""
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in {"subprocess", "os"}
        and node.func.attr in {"system", "popen", "run", "call"}
    )


def check_file(filepath: str | Path) -> list[str]:
    """Check a file for atomicity violations."""
    with Path(filepath).open(encoding="utf-8") as f:
        tree = ast.parse(f.read())

    return find_atomic_violations(tree)


def main(files: Sequence[str]) -> int:
    """Check multiple files for atomicity violations."""
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
