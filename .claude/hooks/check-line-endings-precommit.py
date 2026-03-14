#!/usr/bin/env python3
"""Pre-commit hook: fix line endings in all staged files.

Automatically converts line endings to the correct format before commit:
  - LF for all text source files
  - CRLF for Windows-specific files (.bat, .cmd, .ps1)

Fixed files are re-staged automatically. The hook exits non-zero when
fixes were applied so the user can review and re-commit.

Exit codes:
    0 -- all line endings correct (or no relevant files staged).
    1 -- line endings were fixed (blocks commit so user can review).

Bypass with ``git commit --no-verify``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _constants import (
    CRLF_EXTENSIONS,
    LINE_ENDING_EXTENSIONS,
)


def get_staged_files() -> list[Path]:
    """Return list of staged file paths."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(line.strip()) for line in result.stdout.splitlines() if line.strip()]


def fix_file_line_endings(file_path: Path) -> int:
    """Fix line endings in a single file.

    Args:
        file_path: Path to the file to fix.

    Returns:
        Number of lines that were fixed, or 0 if no changes needed.
    """
    suffix = file_path.suffix.lower()
    all_checked = LINE_ENDING_EXTENSIONS | CRLF_EXTENSIONS
    if suffix not in all_checked:
        return 0

    if not file_path.exists() or not file_path.is_file():
        return 0

    try:
        raw = file_path.read_bytes()
    except OSError:
        return 0

    if not raw:
        return 0

    expect_crlf = suffix in CRLF_EXTENSIONS

    if expect_crlf:
        normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        fixed = normalized.replace(b"\n", b"\r\n")
    else:
        fixed = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    if fixed == raw:
        return 0

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
    """Fix line endings in all staged files and re-stage them."""
    staged_files = get_staged_files()
    if not staged_files:
        return 0

    fixed_files: dict[Path, int] = {}

    for file_path in staged_files:
        fixes = fix_file_line_endings(file_path)
        if fixes:
            fixed_files[file_path] = fixes

    if not fixed_files:
        return 0

    # Re-stage the fixed files
    re_stage = [str(p) for p in fixed_files]
    subprocess.run(["git", "add", *re_stage], check=True)

    print(
        "\n"
        "=== LINE ENDINGS FIXED ===\n"
        "\n"
        "The following files had incorrect line endings and were auto-fixed:\n",
    )

    for file_path, count in fixed_files.items():
        suffix = file_path.suffix.lower()
        target = "CRLF" if suffix in CRLF_EXTENSIONS else "LF"
        print(f"  {file_path}: {count} line(s) -> {target}")

    print(
        "\n"
        "Files have been fixed and re-staged.\n"
        "Please review the changes and commit again.\n"
        "\n"
        "=== END ===\n",
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())
