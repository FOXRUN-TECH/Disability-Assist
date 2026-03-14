#!/usr/bin/env python3
"""Update CONTRIBUTORS.md from git history.

Extracts unique contributors from git log and updates the auto-generated
section of CONTRIBUTORS.md. Intended to run in CI after merges to master.

Usage:
    python scripts/update-contributors.py [--check]

    --check   Dry-run mode: exits non-zero if CONTRIBUTORS.md is outdated.
              Used in CI to verify the file is up to date.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Markers in CONTRIBUTORS.md that bracket the auto-generated section.
START_MARKER = "<!-- CONTRIBUTORS-START -->"
END_MARKER = "<!-- CONTRIBUTORS-END -->"

# Bots and automated accounts to exclude from the contributor list.
EXCLUDED_NAMES: frozenset[str] = frozenset(
    {
        "dependabot[bot]",
        "github-actions[bot]",
        "renovate[bot]",
    }
)

# Co-author patterns (from commit trailers like Co-Authored-By).
CO_AUTHOR_RE = re.compile(r"Co-Authored-By:\s*(.+?)\s*<(.+?)>", re.IGNORECASE)


def get_git_contributors() -> list[tuple[str, str, int]]:
    """Extract contributors from git log.

    Returns:
        Sorted list of (name, email, commit_count) tuples.
    """
    # Get all commit authors.
    result = subprocess.run(
        ["git", "log", "--format=%aN\t%aE"],
        capture_output=True,
        text=True,
        check=True,
    )

    contributors: dict[str, tuple[str, int]] = {}

    for line in result.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", maxsplit=1)
        if len(parts) < 2:
            continue
        name, email = parts
        name = name.strip()
        email = email.strip()

        if name in EXCLUDED_NAMES:
            continue

        key = email.lower()
        if key in contributors:
            existing_name, count = contributors[key]
            # Prefer the longer name variant.
            display_name = name if len(name) > len(existing_name) else existing_name
            contributors[key] = (display_name, count + 1)
        else:
            contributors[key] = (name, 1)

    # Also extract co-authors from commit messages.
    co_result = subprocess.run(
        ["git", "log", "--format=%b"],
        capture_output=True,
        text=True,
        check=True,
    )

    for match in CO_AUTHOR_RE.finditer(co_result.stdout):
        name = match.group(1).strip()
        email = match.group(2).strip()

        if name in EXCLUDED_NAMES:
            continue

        key = email.lower()
        if key in contributors:
            existing_name, count = contributors[key]
            display_name = name if len(name) > len(existing_name) else existing_name
            contributors[key] = (display_name, count + 1)
        else:
            contributors[key] = (name, 1)

    # Sort by commit count (descending), then name (ascending).
    result_list = [(name, email, count) for email, (name, count) in contributors.items()]
    result_list.sort(key=lambda x: (-x[2], x[0].lower()))

    return result_list


def build_table(contributors: list[tuple[str, str, int]]) -> str:
    """Build the markdown contributor table.

    Args:
        contributors: List of (name, email, commit_count) tuples.

    Returns:
        Markdown table string.
    """
    lines = [
        START_MARKER,
        "<!-- This section is automatically maintained by CI. -->",
        "<!-- Do not edit manually between these markers. -->",
        "",
        "| Name | Contributions |",
        "|------|---------------|",
    ]

    for name, _email, count in contributors:
        label = "1 commit" if count == 1 else f"{count} commits"
        lines.append(f"| {name} | {label} |")

    if not contributors:
        lines.append("| *(no contributors yet)* | |")

    lines.append("")
    lines.append(END_MARKER)

    return "\n".join(lines)


def update_file(check_only: bool = False) -> bool:
    """Update CONTRIBUTORS.md with current git contributors.

    Args:
        check_only: If True, only check if the file is outdated.

    Returns:
        True if file was updated (or needs updating in check mode).
    """
    contributors_path = Path(__file__).resolve().parent.parent / "CONTRIBUTORS.md"

    if not contributors_path.exists():
        print(f"ERROR: {contributors_path} not found")
        return False

    content = contributors_path.read_text(encoding="utf-8")

    # Find the auto-generated section.
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find contributor markers in CONTRIBUTORS.md")
        return False

    # Build new table from git history.
    contributors = get_git_contributors()
    new_table = build_table(contributors)

    # Replace the section.
    new_content = content[:start_idx] + new_table + content[end_idx + len(END_MARKER) :]

    if new_content == content:
        print("CONTRIBUTORS.md is up to date.")
        return False

    if check_only:
        print("CONTRIBUTORS.md is outdated. Run: python scripts/update-contributors.py")
        return True

    contributors_path.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"Updated CONTRIBUTORS.md with {len(contributors)} contributor(s).")
    return True


if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    changed = update_file(check_only=check_mode)

    if check_mode and changed:
        sys.exit(1)
