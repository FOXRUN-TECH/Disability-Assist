"""PostToolUse hook: auto-sync version numbers across all project files.

Fires after Write/Edit on any version-carrying file.  Reads the canonical
version from ``pyproject.toml`` and propagates it to all other managed files.

Canonical source (single source of truth):
    pyproject.toml                              version = "X.Y.Z"

Managed files (auto-synced to match pyproject.toml):
    mobile/package.json                         "version": "X.Y.Z"
    device/__init__.py                          __version__ = "X.Y.Z"
    cloud/__init__.py                           __version__ = "X.Y.Z"

Workflow:
    - Edit pyproject.toml version  -> all other files auto-sync immediately.
    - Edit any other version file  -> it is corrected back to pyproject.toml's
      version (prevents accidental per-file version drift).

Exit codes:
    0 -- all versions already in sync (or trigger file is not a version file).
    2 -- one or more out-of-sync files were updated (non-blocking feedback).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Version file registry
# Each entry has:
#   path      -- relative path from repo root
#   pattern   -- compiled regex; group(1) captures the version string
#   canonical -- True for the single source of truth (pyproject.toml)
# ---------------------------------------------------------------------------
_ML = re.MULTILINE

VERSION_FILE_SPECS: list[dict[str, object]] = [
    {
        "path": "pyproject.toml",
        "pattern": re.compile(r'^version = "([^"]+)"', _ML),
        "canonical": True,
    },
    {
        "path": "mobile/package.json",
        "pattern": re.compile(r'"version":\s*"([^"]+)"', _ML),
        "canonical": False,
    },
    {
        "path": "device/__init__.py",
        "pattern": re.compile(r'^__version__ = "([^"]+)"', _ML),
        "canonical": False,
    },
    {
        "path": "cloud/__init__.py",
        "pattern": re.compile(r'^__version__ = "([^"]+)"', _ML),
        "canonical": False,
    },
]

# Quick lookup set for the trigger check.
VERSION_FILE_PATHS: frozenset[str] = frozenset(
    str(spec["path"]).replace("\\", "/") for spec in VERSION_FILE_SPECS
)


def find_repo_root(start: Path) -> Path:
    """Walk up from *start* until a directory containing pyproject.toml is found.

    Args:
        start: Directory to begin the search from.

    Returns:
        Absolute path to the repository root, or the current working directory
        if pyproject.toml is not found in any ancestor.
    """
    current = start.resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()


def read_version(file_path: Path, pattern: re.Pattern[str]) -> str | None:
    """Extract the version string from *file_path* using *pattern*.

    Args:
        file_path: Absolute path to the version-carrying file.
        pattern: Compiled regex where group(1) captures the version string.

    Returns:
        The version string, or ``None`` if the file is missing or the pattern
        does not match.
    """
    if not file_path.exists():
        return None
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = pattern.search(content)
    return m.group(1) if m else None


def write_version(file_path: Path, pattern: re.Pattern[str], new_version: str) -> bool:
    """Update the version string in *file_path* to *new_version* if it differs.

    Args:
        file_path: Absolute path to the version-carrying file.
        pattern: Compiled regex where group(1) captures the version string.
        new_version: Target version string.

    Returns:
        ``True`` if the file was rewritten, ``False`` if already correct or
        if the file is missing / unreadable / the pattern does not match.
    """
    if not file_path.exists():
        return False
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        return False

    m = pattern.search(content)
    if not m:
        return False
    if m.group(1) == new_version:
        return False

    # Replace only the captured version group, preserving surrounding text.
    new_content = content[: m.start(1)] + new_version + content[m.end(1) :]
    try:
        file_path.write_text(new_content, encoding="utf-8")
    except OSError:
        return False
    return True


def main() -> int:
    """Sync version numbers when a version-carrying file is written."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    if payload.get("tool_name", "") not in ("Write", "Edit"):
        return 0

    file_path_str = payload.get("tool_input", {}).get("file_path", "")
    if not file_path_str:
        return 0

    file_path = Path(file_path_str).resolve()
    repo_root = find_repo_root(file_path.parent)

    # Bail early if the edited file is not one of the version-carrying files.
    try:
        rel = str(file_path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return 0

    if rel not in VERSION_FILE_PATHS:
        return 0

    # Read the canonical version from pyproject.toml.
    canonical_spec = next(s for s in VERSION_FILE_SPECS if s["canonical"])
    canonical_path = repo_root / str(canonical_spec["path"])
    canonical_version = read_version(
        canonical_path,
        canonical_spec["pattern"],  # type: ignore[arg-type]
    )

    if not canonical_version:
        print(
            "[sync-versions] WARNING: could not read version from pyproject.toml",
            file=sys.stderr,
        )
        return 0

    # Sync every non-canonical file to the canonical version.
    synced: list[str] = []
    for spec in VERSION_FILE_SPECS:
        if spec["canonical"]:
            continue
        target = repo_root / str(spec["path"])
        if write_version(target, spec["pattern"], canonical_version):  # type: ignore[arg-type]
            synced.append(str(spec["path"]))

    if synced:
        print(
            f"[sync-versions] Version {canonical_version!r} synced to:\n"
            + "".join(f"  {p}\n" for p in synced),
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
