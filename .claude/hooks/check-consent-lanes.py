"""PostToolUse hook: verify consent lane annotations on data-handling code.

Fires after Write/Edit on .py files under cloud/, device/, or policy/.
Scans for functions that handle user data (heuristic: parameter names
like user_id, transcript, profile, consent, audio) and verifies each
has a consent lane annotation comment (# consent-lane: <lane>).

This is an AI-Assist-specific hook -- the consent model requires every
data flow to identify which of the six consent lanes it belongs to.

Exit codes:
    0 -- all data-handling functions annotated (or file is excluded).
    2 -- missing consent lane annotations (non-blocking warning).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from _constants import SKIP_DIRS
from _privacy_patterns import CONSENT_LANES, DATA_HANDLING_PARAMS, PII_EXEMPT_PATTERNS

# Maximum findings to display.
_DISPLAY_LIMIT: int = 5

# Regex to match function definitions.
_FUNC_PATTERN: re.Pattern[str] = re.compile(r"^\s*(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)")

# Regex to match consent lane annotation.
_CONSENT_LANE_PATTERN: re.Pattern[str] = re.compile(
    r"#\s*consent-lane:\s*(" + "|".join(re.escape(lane) for lane in CONSENT_LANES) + r")"
)

# Source directories where consent lane checking applies.
_CONSENT_CHECK_DIRS: frozenset[str] = frozenset({"cloud", "device", "policy"})


def scan_file_for_consent_lanes(file_path: Path) -> list[tuple[int, str]]:
    """Scan a Python file for data-handling functions missing consent lane annotations.

    Args:
        file_path: Path to the Python file to scan.

    Returns:
        List of (line_number, function_name) tuples for functions that
        handle user data but lack a consent lane annotation.
    """
    if file_path.suffix != ".py":
        return []

    if any(part in SKIP_DIRS for part in file_path.parts):
        return []

    # Only check files in consent-relevant directories.
    path_parts = file_path.parts
    if not any(d in path_parts for d in _CONSENT_CHECK_DIRS):
        return []

    # Skip exempt file patterns (tests, fixtures, etc.)
    path_str = str(file_path).replace("\\", "/")
    if any(pat in path_str for pat in PII_EXEMPT_PATTERNS):
        return []

    if not file_path.exists():
        return []

    findings: list[tuple[int, str]] = []

    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings

    for line_no, line in enumerate(lines, start=1):
        match = _FUNC_PATTERN.match(line)
        if not match:
            continue

        func_name = match.group(1)
        params = match.group(2).lower()

        # Check if this function handles user data.
        has_data_param = any(param in params for param in DATA_HANDLING_PARAMS)
        if not has_data_param:
            continue

        # Check for consent lane annotation in the surrounding lines.
        # Look at the 5 lines before and 10 lines after the function def.
        context_start = max(0, line_no - 6)
        context_end = min(len(lines), line_no + 10)
        context_block = "\n".join(lines[context_start:context_end])

        if not _CONSENT_LANE_PATTERN.search(context_block):
            findings.append((line_no, func_name))

    return findings


def main() -> int:
    """Check a Python file for consent lane annotations after Write/Edit."""
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
    findings = scan_file_for_consent_lanes(file_path)

    if findings:
        print(f"\n[consent-lanes] Missing annotations in {file_path}", file=sys.stderr)
        for line_no, func_name in findings[:_DISPLAY_LIMIT]:
            print(
                f"  L{line_no}: {func_name}() handles user data but has no consent lane annotation",
                file=sys.stderr,
            )
        if len(findings) > _DISPLAY_LIMIT:
            print(
                f"  ... and {len(findings) - _DISPLAY_LIMIT} more",
                file=sys.stderr,
            )
        print(
            "\n  Add a comment near the function: # consent-lane: <lane>\n"
            f"  Valid lanes: {', '.join(CONSENT_LANES)}\n",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
