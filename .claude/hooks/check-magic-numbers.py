"""PostToolUse hook: warn about magic numbers in Python code.

Fires after Write/Edit on .py files. Scans for numeric literals that
should be named constants per project rules (CLAUDE.md rule 6).

Exit codes:
    0 -- no magic numbers found (or non-Python file).
    2 -- magic numbers detected (non-blocking feedback to Claude).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _magic_numbers import MAGIC_NUMBER_DISPLAY_LIMIT, scan_file_for_magic_numbers


def main() -> int:
    """Check a Python file for magic numbers after Write/Edit."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        return 0

    file_path_str = payload.get("tool_input", {}).get("file_path", "")
    if not file_path_str:
        return 0

    file_path = Path(file_path_str)
    findings = scan_file_for_magic_numbers(file_path)

    if findings:
        print(f"\n[magic-numbers] {file_path}", file=sys.stderr)
        for line_no, number, context in findings[:MAGIC_NUMBER_DISPLAY_LIMIT]:
            print(f"  L{line_no}: {number} in: {context}", file=sys.stderr)
        if len(findings) > MAGIC_NUMBER_DISPLAY_LIMIT:
            print(
                f"  ... and {len(findings) - MAGIC_NUMBER_DISPLAY_LIMIT} more",
                file=sys.stderr,
            )
        print(
            "  Consider extracting to constants module with typing.Final\n",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
