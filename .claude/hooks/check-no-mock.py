"""PostToolUse hook: warn about mock/stub patterns in production code.

Fires after Write/Edit on .py, .ts, .tsx files. Scans for mock driver
class names and stub references that indicate the code is not using
real implementations.

Exit codes:
    0 -- no mock patterns found (or file is excluded).
    2 -- mock patterns detected (non-blocking feedback to Claude).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from _no_mock import NO_MOCK_DISPLAY_LIMIT, scan_file_for_mock_patterns, should_skip_file


def main() -> int:
    """Check a source file for mock/stub patterns after Write/Edit."""
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
    if should_skip_file(file_path):
        return 0

    findings = scan_file_for_mock_patterns(file_path)

    if findings:
        print(f"\n[no-mock] {file_path}", file=sys.stderr)
        for line_no, description, context in findings[:NO_MOCK_DISPLAY_LIMIT]:
            print(f"  L{line_no}: {description}: {context}", file=sys.stderr)
        if len(findings) > NO_MOCK_DISPLAY_LIMIT:
            print(
                f"  ... and {len(findings) - NO_MOCK_DISPLAY_LIMIT} more",
                file=sys.stderr,
            )
        print(
            "  Production code should use real implementations. Suppress with # mock-ok\n",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
