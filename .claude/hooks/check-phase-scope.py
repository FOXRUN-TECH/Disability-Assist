"""PostToolUse hook: warn about files outside current phase scope.

Fires after Bash tool calls containing ``git add``. Checks staged files
against the active phase's allowed path prefixes defined in
``_phase_config.py``.

Exit codes:
    0 -- always (non-blocking warning only).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

from _phase_config import ACTIVE_PHASE, PHASE_FILE_MAP, SHARED_PATHS

_GIT_ADD_PATTERN: re.Pattern[str] = re.compile(r"\bgit\s+add\b")


def _get_staged_files() -> list[str]:
    """Return list of staged file paths from git."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _is_allowed(file_path: str, phase: str) -> bool:
    """Check if a file path is allowed for the given phase.

    Args:
        file_path: Relative path from repository root.
        phase: Active phase identifier (e.g. ``"0"``).

    Returns:
        True if the file is within scope for the phase or is a shared file.
    """
    # Shared paths are always allowed.
    for shared in SHARED_PATHS:
        if file_path.startswith(shared) or file_path == shared.rstrip("/"):
            return True

    # Phase-specific paths.
    phase_paths = PHASE_FILE_MAP.get(phase, frozenset())
    return any(file_path.startswith(p) for p in phase_paths)


def main() -> int:
    """Check staged files against active phase scope after git add."""
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return 0

    if data.get("tool_name") != "Bash":
        return 0

    command = data.get("tool_input", {}).get("command", "")
    if not _GIT_ADD_PATTERN.search(command):
        return 0

    staged = _get_staged_files()
    if not staged:
        return 0

    out_of_scope = [f for f in staged if not _is_allowed(f, ACTIVE_PHASE)]

    if out_of_scope:
        display_limit = 10
        file_list = "\n".join(f"  - {f}" for f in out_of_scope[:display_limit])
        extra = ""
        if len(out_of_scope) > display_limit:
            extra = f"\n  ... and {len(out_of_scope) - display_limit} more"
        print(
            f"\n=== PHASE SCOPE WARNING ===\n\n"
            f"Active phase: {ACTIVE_PHASE}\n"
            f"The following staged files are outside this phase's scope:\n\n"
            f"{file_list}{extra}\n\n"
            f"If this is intentional (e.g., fixing a bug in another module),\n"
            f"proceed. Otherwise, unstage files outside the current phase.\n\n"
            f"=== END ===\n",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
