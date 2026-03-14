"""Pre-commit hook: block commits with mock/stub patterns in production code.

Scans staged .py, .ts, .tsx files for mock driver class names and stub
references. Blocks the commit if violations are found.

Exit codes:
    0 -- no mock patterns found (or no relevant files staged).
    1 -- mock patterns detected (blocks commit).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _no_mock import scan_file_for_mock_patterns, should_skip_file


def main() -> int:
    """Scan staged files for mock/stub patterns."""
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

    all_findings: list[tuple[str, int, str, str]] = []

    for rel_path in staged_files:
        file_path = Path(rel_path)
        if should_skip_file(file_path):
            continue

        findings = scan_file_for_mock_patterns(file_path)
        for line_no, description, context in findings:
            all_findings.append((rel_path, line_no, description, context))

    if all_findings:
        print("\n[no-mock] Mock/stub patterns found in staged files:\n", file=sys.stderr)
        for rel_path, line_no, description, context in all_findings:
            print(f"  {rel_path}:{line_no}: {description}: {context}", file=sys.stderr)
        print(
            "\nProduction code must use real implementations."
            " Suppress individual lines with # mock-ok"
            "\nBypass with: git commit --no-verify\n",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
