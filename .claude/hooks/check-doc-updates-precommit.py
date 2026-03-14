#!/usr/bin/env python3
"""Pre-commit hook: block commits that modify source files without doc updates.

Checks ``git diff --cached`` for staged source files. If source files
are staged but none of the documentation files are also staged, the
commit is blocked with an explanatory message.

Exit codes:
    0 -- docs updated (or no source files changed).
    1 -- source changed without doc updates (blocks commit).

Bypass with ``git commit --no-verify`` for trivial changes.
"""

from __future__ import annotations

import subprocess
import sys

from _constants import DOC_FILES, SOURCE_PATTERNS


def main() -> int:
    """Check that source file changes include documentation updates."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0

    staged_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    if not staged_files:
        return 0

    # Check if any source files are staged.
    has_source = any(
        any(f.startswith(p) for p in SOURCE_PATTERNS)
        for f in staged_files
    )

    if not has_source:
        return 0

    # Check if any doc files are staged.
    has_docs = any(f in DOC_FILES or f.rstrip("/") in DOC_FILES for f in staged_files)

    if has_docs:
        return 0

    # Source files changed without doc updates.
    print(
        "\n"
        "=== DOCUMENTATION UPDATE REQUIRED ===\n"
        "\n"
        "Source files were modified but no documentation files are staged.\n"
        "\n"
        "Please update at least one of:\n"
    )
    for doc in sorted(DOC_FILES):
        print(f"  - {doc}")
    print(
        "\n"
        "For trivial changes (typos, comments), bypass with:\n"
        "  git commit --no-verify\n"
        "\n"
        "=== END ===\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
