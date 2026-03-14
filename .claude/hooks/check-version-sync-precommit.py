#!/usr/bin/env python3
"""Pre-commit hook: enforce version consistency across all project files.

Reads the canonical version from ``pyproject.toml`` and blocks the commit if
any other version-carrying file contains a different version string.

Exit codes:
    0 -- all versions in sync.
    1 -- version mismatch detected (blocks commit).

Bypass with ``git commit --no-verify``.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Version file registry (must be kept identical to sync-versions.py)
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


def find_repo_root() -> Path:
    """Return the repository root as reported by git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def read_version(file_path: Path, pattern: re.Pattern[str]) -> str | None:
    """Extract the version string from *file_path* using *pattern*."""
    if not file_path.exists():
        return None
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = pattern.search(content)
    return m.group(1) if m else None


def main() -> int:
    """Check that all managed version files agree with pyproject.toml."""
    repo_root = find_repo_root()

    # Read canonical version.
    canonical_spec = next(s for s in VERSION_FILE_SPECS if s["canonical"])
    canonical_path = repo_root / str(canonical_spec["path"])
    canonical_version = read_version(
        canonical_path,
        canonical_spec["pattern"],  # type: ignore[arg-type]
    )

    if not canonical_version:
        print(
            "check-version-sync: ERROR: could not read version from pyproject.toml\n"
            '  Ensure pyproject.toml exists and contains:  version = "X.Y.Z"\n'
        )
        return 1

    # Check all non-canonical files.
    mismatches: list[tuple[str, str]] = []
    for spec in VERSION_FILE_SPECS:
        if spec["canonical"]:
            continue
        file_path = repo_root / str(spec["path"])
        version = read_version(file_path, spec["pattern"])  # type: ignore[arg-type]
        if version is None:
            continue
        if version != canonical_version:
            mismatches.append((str(spec["path"]), version))

    if not mismatches:
        return 0

    # Report and block.
    print(
        "\n"
        "=== VERSION MISMATCH ===\n"
        "\n"
        f"  Canonical (pyproject.toml): {canonical_version}\n"
        "\n"
        "  Out-of-sync files:\n"
    )
    for path, version in mismatches:
        print(f"    {path}  ({version!r}  !=  {canonical_version!r})")
    print(
        "\n"
        "  Fix: update pyproject.toml to the desired version, then save it.\n"
        "  The sync-versions PostToolUse hook will auto-update all other files.\n"
        "\n"
        "  Bypass: git commit --no-verify\n"
        "=== END ===\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
