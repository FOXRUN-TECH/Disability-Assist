#!/usr/bin/env python3
"""PostToolUse hook: remind Claude to update the roadmap after commits.

Fires after any Bash tool call. If the command contains a ``git commit``,
outputs a stderr reminder to consider running ``/phase-complete``.

Exit codes:
  0 -- always (non-blocking reminder)
"""

from __future__ import annotations

import json
import re
import sys

# Regex to detect git commit commands with word boundaries.
_GIT_COMMIT_PATTERN = re.compile(r"\bgit\s+commit\b")


def main() -> int:
    """Read hook payload and emit a plan update reminder after git commit.

    Returns:
        Always 0 (non-blocking reminder, never fails the tool call).
    """
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return 0

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        return 0

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Detect git commit commands in any part of a chained command
    if not _GIT_COMMIT_PATTERN.search(command):
        return 0

    # Remind Claude to update the roadmap
    print(
        "\n"
        "=== ROADMAP REMINDER ===\n"
        "\n"
        "You just committed changes.\n"
        "If a phase milestone is complete, run /phase-complete <phase-id>\n"
        "to validate exit criteria and update docs/roadmap.md.\n"
        "\n"
        "Current roadmap: docs/roadmap.md\n"
        "\n"
        "=== END ===\n",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
