"""PostToolUse hook: scan for PII leaks and privacy violations.

Fires after Write/Edit on .py, .ts, .tsx files. Scans for patterns
that suggest personally identifiable information (PII) exposure in
logs, print statements, and data handling code.

This is an AI-Assist-specific hook -- assistive technology handling
sensitive user data requires strict PII discipline.

Exit codes:
    0 -- no PII patterns found (or file is excluded).
    2 -- PII patterns detected (non-blocking feedback to Claude).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _constants import SKIP_DIRS
from _privacy_patterns import PII_EXEMPT_PATTERNS, PII_PATTERNS, PII_SUPPRESS_COMMENT

# Maximum findings to display.
_DISPLAY_LIMIT: int = 5

# File extensions to scan.
_SCAN_EXTENSIONS: frozenset[str] = frozenset({".py", ".ts", ".tsx"})


def scan_file_for_pii(file_path: Path) -> list[tuple[int, str, str]]:
    """Scan a source file for PII exposure patterns.

    Args:
        file_path: Path to the file to scan.

    Returns:
        List of (line_number, description, line_content) tuples.
    """
    if file_path.suffix not in _SCAN_EXTENSIONS:
        return []

    if any(part in SKIP_DIRS for part in file_path.parts):
        return []

    # Skip exempt file patterns (tests, fixtures, etc.)
    path_str = str(file_path).replace("\\", "/")
    if any(pat in path_str for pat in PII_EXEMPT_PATTERNS):
        return []

    if not file_path.exists():
        return []

    findings: list[tuple[int, str, str]] = []

    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings

    for line_no, line in enumerate(lines, start=1):
        # Skip suppressed lines
        if PII_SUPPRESS_COMMENT in line:
            continue

        for pattern, description in PII_PATTERNS:
            if pattern.search(line):
                findings.append((line_no, description, line.strip()[:80]))

    return findings


def main() -> int:
    """Check a source file for PII patterns after Write/Edit."""
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
    findings = scan_file_for_pii(file_path)

    if findings:
        print(f"\n[privacy] PII exposure detected in {file_path}", file=sys.stderr)
        for line_no, description, context in findings[:_DISPLAY_LIMIT]:
            print(f"  L{line_no}: {description}", file=sys.stderr)
            print(f"         {context}", file=sys.stderr)
        if len(findings) > _DISPLAY_LIMIT:
            print(
                f"  ... and {len(findings) - _DISPLAY_LIMIT} more",
                file=sys.stderr,
            )
        print(
            "\n  PII must not appear in logs or be exposed to caregivers as raw text.\n"
            "  Use paraphrases for caregiver feeds. Suppress with # pii-ok\n",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
