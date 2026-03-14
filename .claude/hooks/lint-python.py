"""Claude Code PostToolUse hook: lint Python files after Write/Edit.

Reads JSON from stdin, extracts the file path, and runs quality checks
on .py files. Outputs diagnostics to stderr for Claude to see.

Exit codes:
  0 -- success (or skipped non-Python file)
  2 -- linter reported issues (non-blocking feedback to Claude)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from _constants import MYPY_OUTPUT_LIMIT, SKIP_DIRS


def _run_tool(cmd: list[str], label: str, path: str) -> tuple[bool, str]:
    """Run an external tool and capture its output.

    Args:
        cmd: Command and arguments to execute.
        label: Display label for stderr output (e.g. ``"ruff"``).
        path: File path being checked (for display purposes).

    Returns:
        Tuple of (had_issues, output_text). ``had_issues`` is True if the
        tool returned a non-zero exit code with meaningful output.
    """
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip() or result.stderr.strip()
    if result.returncode != 0 and output:
        print(f"[{label}] {path}", file=sys.stderr)
        print(output, file=sys.stderr)
        return True, output
    return False, ""


def main() -> int:
    """Read hook payload from stdin and run linters on the target file.

    Returns:
        0 if no issues found or file was skipped, 2 if linters reported issues.
    """
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    # Extract file path from tool input
    tool_input = payload.get("tool_input", {})
    file_path_str = tool_input.get("file_path", "")
    if not file_path_str:
        return 0

    file_path = Path(file_path_str)

    # Only lint Python files
    if file_path.suffix != ".py":
        return 0

    # Skip virtual environments, caches, and build artifacts
    if any(part in SKIP_DIRS for part in file_path.parts):
        return 0

    # Skip if the file doesn't exist (deleted files)
    if not file_path.exists():
        return 0

    had_issues = False
    str_path = str(file_path)

    # 1. Ruff check (lint with auto-fix, includes import sorting via I rule)
    issues, _ = _run_tool(
        [sys.executable, "-m", "ruff", "check", "--fix", str_path],
        "ruff",
        str_path,
    )
    had_issues = had_issues or issues

    # 2. Ruff format
    issues, _ = _run_tool(
        [sys.executable, "-m", "ruff", "format", str_path],
        "ruff format",
        str_path,
    )
    had_issues = had_issues or issues

    # 3. Mypy (type check -- non-blocking, informational)
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", str_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and result.stdout.strip():
        lines = [ln for ln in result.stdout.strip().splitlines() if "error:" in ln]
        if lines:
            print(f"[mypy] {str_path}", file=sys.stderr)
            for ln in lines[:MYPY_OUTPUT_LIMIT]:
                print(f"  {ln}", file=sys.stderr)
            had_issues = True

    return 2 if had_issues else 0


if __name__ == "__main__":
    sys.exit(main())
