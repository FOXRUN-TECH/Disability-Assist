#!/usr/bin/env python3
"""PostToolUse hook: remind Claude to verify CI after git push.

Fires after any Bash tool call. If the command contains a ``git push``,
outputs a stderr reminder to check CI pipeline status.

Exit codes:
  0 -- always (non-blocking reminder)
"""

from __future__ import annotations

import json
import re
import sys

# Regex to detect git push commands with word boundaries.
_GIT_PUSH_PATTERN = re.compile(r"\bgit\s+push\b")


def main() -> int:
    """Read hook payload and emit a CI verification reminder after git push.

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

    # Detect git push commands in any part of a chained command
    if not _GIT_PUSH_PATTERN.search(command):
        return 0

    # Remind Claude to check CI
    print(
        "\n"
        "=== CI VERIFICATION REQUIRED ===\n"
        "\n"
        "You just pushed to the remote repository.\n"
        "Per project rules, you MUST verify CI passes:\n"
        "\n"
        "  1. Wait ~30s then run: gh run list --limit 1\n"
        "  2. If status is 'in_progress', wait and check again\n"
        "  3. If status is 'failure', run: gh run view <id> --log-failed\n"
        "  4. Fix failures, commit, and push again\n"
        "  5. Repeat until CI passes (status: 'completed' + 'success')\n"
        "\n"
        "=== END ===\n",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
