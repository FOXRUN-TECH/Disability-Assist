"""Shared mock/stub pattern scanning logic for Claude Code hooks.

Used by both the PostToolUse hook (check-no-mock.py) and the
pre-commit hook (check-no-mock-precommit.py).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

# Maximum number of findings to display per file.
NO_MOCK_DISPLAY_LIMIT: Final[int] = 5

# File extensions to scan.
SCAN_EXTENSIONS: Final[frozenset[str]] = frozenset({".py", ".ts", ".tsx"})

# Directories/path segments to skip entirely.
_SKIP_SEGMENTS: Final[frozenset[str]] = frozenset(
    {
        "tests",
        "test-utils",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        ".claude",
    }
)

# File name patterns to skip (test files, conftest).
_SKIP_FILE_PATTERNS: Final[tuple[str, ...]] = (
    ".test.ts",
    ".test.tsx",
    ".test.js",
    "test_",
    "conftest",
)

# Patterns that indicate mock/stub usage in production code.
# Each tuple: (compiled regex, description, line-level exemption patterns)
_MOCK_PATTERNS: list[tuple[re.Pattern[str], str, tuple[str, ...]]] = [
    (
        re.compile(r"\bMock[A-Z]\w+"),
        "Mock class name",
        ("unittest.mock", "from unittest", "# mock-ok"),
    ),
    (
        re.compile(r"\bstub\b", re.IGNORECASE),
        "Stub reference",
        ("# mock-ok", "beta", "501"),
    ),
]


def should_skip_file(file_path: Path) -> bool:
    """Check if the file should be skipped from scanning.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file should be skipped.
    """
    if file_path.suffix not in SCAN_EXTENSIONS:
        return True

    parts = file_path.parts
    for segment in _SKIP_SEGMENTS:
        if segment in parts:
            return True

    name_lower = file_path.name.lower()
    return any(pattern in name_lower for pattern in _SKIP_FILE_PATTERNS)


def scan_file_for_mock_patterns(file_path: Path) -> list[tuple[int, str, str]]:
    """Scan a file for mock/stub patterns.

    Args:
        file_path: Path to the file to scan.

    Returns:
        List of (line_number, pattern_description, line_content) tuples.
    """
    findings: list[tuple[int, str, str]] = []

    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings

    for line_no, line in enumerate(lines, start=1):
        for pattern, description, exemptions in _MOCK_PATTERNS:
            if pattern.search(line):
                if any(ex in line for ex in exemptions):
                    continue
                findings.append((line_no, description, line.strip()))

    return findings
