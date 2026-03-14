"""Claude Code PostToolUse hook: remind about documentation updates.

Runs after Write/Edit on source files. Outputs a reminder to stderr
so Claude sees it in the tool feedback and remembers to update docs
**only when the user explicitly requests it**.

Only triggers for source files (device/, cloud/, policy/, mobile/, infra/).
Does NOT trigger for documentation files themselves to avoid infinite loops.

Exit codes:
  0 -- always (non-blocking reminder)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _constants import DOC_FILES, SKIP_DIRS, SOURCE_EXTENSIONS, SOURCE_PATTERNS

# Source directory names extracted from SOURCE_PATTERNS for part matching.
_SOURCE_DIRS: set[str] = {p.rstrip("/") for p in SOURCE_PATTERNS}


def main() -> int:
    """Read hook payload and emit a doc-update reminder for source files.

    Returns:
        Always 0 (non-blocking reminder, never fails the tool call).
    """
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    tool_input = payload.get("tool_input", {})
    file_path_str = tool_input.get("file_path", "")
    if not file_path_str:
        return 0

    file_path = Path(file_path_str)

    # Skip doc files themselves (check both name and relative path)
    if file_path.name in DOC_FILES or str(file_path).replace("\\", "/") in DOC_FILES:
        return 0

    # Skip non-source directories
    if any(part in SKIP_DIRS for part in file_path.parts):
        return 0

    # Check if this is a source file
    is_source = any(part in _SOURCE_DIRS for part in file_path.parts)
    if not is_source:
        return 0

    # Only remind for actual code files
    if file_path.suffix not in SOURCE_EXTENSIONS:
        return 0

    print(
        "[doc-reminder] Source file modified. Do NOT auto-update documentation or "
        "run full test suites. Only update docs or run tests when the user "
        "explicitly asks.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
