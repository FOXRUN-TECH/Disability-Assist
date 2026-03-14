"""PostToolUse hook: fix line endings after Write/Edit.

Fires after Write/Edit on text source files. Automatically converts
line endings to the correct format:
  - LF for all text source files
  - CRLF for Windows-specific files (.bat, .cmd, .ps1)

Exit codes:
    0 -- no fixes needed (or non-text file).
    2 -- line endings were fixed (non-blocking feedback to Claude).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _constants import (
    CRLF_EXTENSIONS,
    LINE_ENDING_EXTENSIONS,
    SKIP_DIRS,
)


def fix_line_endings(file_path: Path) -> int:
    """Fix line endings in a file to match the expected format.

    Args:
        file_path: Path to the file to fix.

    Returns:
        Number of lines that were fixed, or 0 if no changes needed.
    """
    if not file_path.exists() or not file_path.is_file():
        return 0

    suffix = file_path.suffix.lower()
    all_checked = LINE_ENDING_EXTENSIONS | CRLF_EXTENSIONS
    if suffix not in all_checked:
        return 0

    try:
        raw = file_path.read_bytes()
    except OSError:
        return 0

    if not raw:
        return 0

    expect_crlf = suffix in CRLF_EXTENSIONS

    if expect_crlf:
        # Normalize everything to LF first, then convert to CRLF
        normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        fixed = normalized.replace(b"\n", b"\r\n")
    else:
        # Convert CRLF and bare CR to LF
        fixed = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    if fixed == raw:
        return 0

    # Count how many lines changed
    old_crlf = raw.count(b"\r\n")
    old_cr = raw.count(b"\r") - old_crlf
    old_lf = raw.count(b"\n") - old_crlf

    fixes = old_lf + old_cr if expect_crlf else old_crlf + old_cr

    try:
        file_path.write_bytes(fixed)
    except OSError:
        return 0

    return fixes


def main() -> int:
    """Fix line endings in a file after Write/Edit."""
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

    if any(part in SKIP_DIRS for part in file_path.parts):
        return 0

    fixes = fix_line_endings(file_path)

    if fixes:
        suffix = file_path.suffix.lower()
        target = "CRLF" if suffix in CRLF_EXTENSIONS else "LF"
        print(
            f"[line-endings] Fixed {fixes} line(s) -> {target}: {file_path}",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
