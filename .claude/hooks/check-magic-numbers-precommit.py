#!/usr/bin/env python3
"""Pre-commit hook: block commits containing magic numbers in Python code.

Scans all staged ``.py`` files for numeric literals that should be
named constants per project rules (CLAUDE.md rule 6).

Exit codes:
    0 -- no magic numbers found (or no Python files staged).
    1 -- magic numbers detected (blocks the commit).

Suppress individual lines with ``# magic-ok`` or bypass the entire
hook with ``git commit --no-verify``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _magic_numbers import MAGIC_NUMBER_DISPLAY_LIMIT, scan_file_for_magic_numbers


def get_staged_python_files() -> list[Path]:
    """Return list of staged Python file paths."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        Path(line.strip()) for line in result.stdout.splitlines() if line.strip().endswith(".py")
    ]


def main() -> int:
    """Scan staged Python files for magic numbers and block commit if found."""
    staged_files = get_staged_python_files()
    if not staged_files:
        return 0

    total_findings: dict[Path, list[tuple[int, str, str]]] = {}

    for file_path in staged_files:
        findings = scan_file_for_magic_numbers(file_path)
        if findings:
            total_findings[file_path] = findings

    if not total_findings:
        return 0

    print(
        "\n"
        "=== MAGIC NUMBERS DETECTED ===\n"
        "\n"
        "The following files contain numeric literals that should be\n"
        "named constants (typing.Final) in the constants module:\n",
    )

    for file_path, findings in total_findings.items():
        print(f"  {file_path}:")
        for line_no, number, context in findings[:MAGIC_NUMBER_DISPLAY_LIMIT]:
            print(f"    L{line_no}: {number} in: {context}")
        if len(findings) > MAGIC_NUMBER_DISPLAY_LIMIT:
            print(f"    ... and {len(findings) - MAGIC_NUMBER_DISPLAY_LIMIT} more")
        print()

    print(
        "Extract magic numbers to constants module with typing.Final.\n"
        "Suppress individual lines with: # magic-ok\n"
        "Bypass this hook with: git commit --no-verify\n"
        "\n"
        "=== END ===\n",
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())
