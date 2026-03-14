#!/usr/bin/env python3
"""Check that Python source files include the Apache 2.0 license header.

Scans staged or all Python files in device/, cloud/, policy/, and infra/
for the required license header. Files in tests/ and __init__.py are exempt.

Usage:
    python scripts/check-license-headers.py [--all]

    --all    Check all files, not just staged ones.

Exit codes:
    0 -- All files have headers (or no files to check).
    1 -- One or more files are missing the header.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Final

REQUIRED_SNIPPET: Final[str] = "Licensed under the Apache License, Version 2.0"

# Maximum bytes to read from file top when checking for header.
HEADER_READ_LIMIT: Final[int] = 1024

# Copyright year for the license header.
COPYRIGHT_YEAR: Final[str] = "2026"

# Directories to check for license headers.
SOURCE_DIRS: Final[tuple[str, ...]] = ("device", "cloud", "policy", "infra")

# Files exempt from header requirement.
EXEMPT_PATTERNS: Final[tuple[str, ...]] = (
    "__init__.py",
    "conftest.py",
)


def get_files(check_all: bool = False) -> list[Path]:
    """Get Python files to check.

    Args:
        check_all: If True, check all files. Otherwise, only staged files.

    Returns:
        List of Path objects to check.
    """
    if check_all:
        files: list[Path] = []
        for src_dir in SOURCE_DIRS:
            src_path = Path(src_dir)
            if src_path.exists():
                files.extend(src_path.rglob("*.py"))
        return files

    # Only check staged files.
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )

    files = []
    for line in result.stdout.strip().splitlines():
        path = Path(line.strip())
        if path.suffix == ".py" and any(line.startswith(d) for d in SOURCE_DIRS):
            files.append(path)

    return files


def check_header(filepath: Path) -> bool:
    """Check if a file contains the required license header.

    Args:
        filepath: Path to the file to check.

    Returns:
        True if the header is present or the file is exempt.
    """
    if filepath.name in EXEMPT_PATTERNS:
        return True

    try:
        # Read the first portion -- header should be at the top.
        content = filepath.read_text(encoding="utf-8")[:HEADER_READ_LIMIT]
        return REQUIRED_SNIPPET in content
    except (OSError, UnicodeDecodeError):
        return True  # Skip unreadable files.


def main() -> int:
    """Run the license header check.

    Returns:
        Exit code (0 = pass, 1 = failures found).
    """
    check_all = "--all" in sys.argv
    files = get_files(check_all=check_all)

    missing = [f for f in files if not check_header(f)]

    if not missing:
        if files:
            print(f"License header check passed ({len(files)} file(s) checked).")
        return 0

    print(f"Missing Apache 2.0 license header in {len(missing)} file(s):")
    for f in sorted(missing):
        print(f"  {f}")
    print()
    print("Add this header to the top of each file (after the shebang if present):")
    print()
    print(f"  # Copyright {COPYRIGHT_YEAR} Disability-Assist Contributors")
    print("  # Licensed under the Apache License, Version 2.0.")
    print("  # See LICENSE for details.")
    print()

    return 1


if __name__ == "__main__":
    sys.exit(main())
