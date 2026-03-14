#!/usr/bin/env python3
"""Pre-commit hook: block commits with PII violations in staged files.

Scans all staged .py, .ts, .tsx files for patterns that suggest
personally identifiable information (PII) exposure in logs, print
statements, and data handling code.

Exit codes:
    0 -- no PII patterns found (or no relevant files staged).
    1 -- PII patterns detected (blocks the commit).

Suppress individual lines with ``# pii-ok`` or bypass with
``git commit --no-verify``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _constants import SKIP_DIRS
from _privacy_patterns import PII_EXEMPT_PATTERNS, PII_PATTERNS, PII_SUPPRESS_COMMENT

# File extensions to scan.
_SCAN_EXTENSIONS: frozenset[str] = frozenset({".py", ".ts", ".tsx"})

# Maximum findings to display per file.
_DISPLAY_LIMIT: int = 5


def main() -> int:
    """Scan staged files for PII exposure patterns and block if found."""
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

    all_findings: dict[str, list[tuple[int, str, str]]] = {}

    for rel_path in staged_files:
        file_path = Path(rel_path)

        if file_path.suffix not in _SCAN_EXTENSIONS:
            continue

        if any(part in SKIP_DIRS for part in file_path.parts):
            continue

        path_str = str(file_path).replace("\\", "/")
        if any(pat in path_str for pat in PII_EXEMPT_PATTERNS):
            continue

        if not file_path.exists():
            continue

        try:
            lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        findings: list[tuple[int, str, str]] = []
        for line_no, line in enumerate(lines, start=1):
            if PII_SUPPRESS_COMMENT in line:
                continue
            for pattern, description in PII_PATTERNS:
                if pattern.search(line):
                    findings.append((line_no, description, line.strip()[:80]))

        if findings:
            all_findings[rel_path] = findings

    if not all_findings:
        return 0

    print(
        "\n"
        "=== PII EXPOSURE DETECTED ===\n"
        "\n"
        "The following files contain patterns that may expose personally\n"
        "identifiable information (PII) in logs, output, or caregiver feeds:\n",
        file=sys.stderr,
    )

    for rel_path, findings in all_findings.items():
        print(f"\n  {rel_path}:", file=sys.stderr)
        for line_no, description, context in findings[:_DISPLAY_LIMIT]:
            print(f"    L{line_no}: {description}", file=sys.stderr)
            print(f"           {context}", file=sys.stderr)
        if len(findings) > _DISPLAY_LIMIT:
            print(
                f"    ... and {len(findings) - _DISPLAY_LIMIT} more",
                file=sys.stderr,
            )

    print(
        "\n"
        "PII must not appear in logs or be exposed as raw text.\n"
        "Use paraphrases for caregiver feeds.\n"
        "Suppress individual lines with: # pii-ok\n"
        "Bypass this hook with: git commit --no-verify\n"
        "\n"
        "=== END ===\n",
        file=sys.stderr,
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())
