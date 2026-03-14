"""Shared magic-number scanning logic for Claude Code hooks.

Provides the core detection engine used by both the PostToolUse hook
(``check-magic-numbers.py``) and the pre-commit hook
(``check-magic-numbers-precommit.py``).

Rules:
    - Numeric literals of 2+ digits that aren't in ``ALLOWED_NUMBERS``
      are flagged as potential magic numbers.
    - Lines containing exempt patterns (constant definitions, test code,
      etc.) are skipped.
    - Files in exempt directories (constants/, tests/) are skipped entirely.
    - Suppress individual lines with ``# magic-ok`` or ``# noqa``.
"""

from __future__ import annotations

import re
from pathlib import Path

from _constants import SKIP_DIRS

# Numeric literals that are always acceptable (common indices, flags, defaults).
ALLOWED_NUMBERS: frozenset[str] = frozenset(
    {"0", "1", "2", "-1", "0.0", "1.0", "0.5", "100", "1000"}
)

# Maximum number of findings to display per file.
MAGIC_NUMBER_DISPLAY_LIMIT: int = 5

# Pattern: standalone integer or float literals (2+ digits, not part of names).
NUMBER_PATTERN: re.Pattern[str] = re.compile(
    r"(?<![a-zA-Z_\"\'\.])\b(\d{2,}\.?\d*)\b(?![a-zA-Z_\"\'])"
)

# Lines containing any of these substrings are exempt from checking.
EXEMPT_LINE_PATTERNS: tuple[str, ...] = (
    "# noqa",
    "# magic-ok",
    "typing.Final",
    "Final[",
    "range(",
    "sleep(",
    "version",
    "__version__",
    "def test_",
    "assert ",
    "pytest.mark",
    "@pytest",
    "# type:",
    "rev:",
)

# File path substrings that are exempt from checking.
EXEMPT_FILE_PATTERNS: tuple[str, ...] = (
    "constants/",
    "constants.py",
    "/tests/",
    "test_",
    "conftest.py",
    "migrations/",
    "_phase_config.py",
)


def scan_file_for_magic_numbers(
    file_path: Path,
) -> list[tuple[int, str, str]]:
    """Scan a Python file for magic number violations.

    Args:
        file_path: Path to the Python file to scan.

    Returns:
        List of ``(line_number, number_literal, context_snippet)`` tuples
        for each magic number found.  Empty list if the file is clean,
        exempt, or does not exist.
    """
    if file_path.suffix != ".py":
        return []

    # Skip files in excluded directories.
    if any(part in SKIP_DIRS for part in file_path.parts):
        return []

    # Skip exempt file patterns.
    path_str = str(file_path).replace("\\", "/")
    if any(pat in path_str for pat in EXEMPT_FILE_PATTERNS):
        return []

    if not file_path.exists():
        return []

    findings: list[tuple[int, str, str]] = []
    in_docstring = False
    lines = file_path.read_text(encoding="utf-8").splitlines()

    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track triple-quoted docstrings / multi-line strings.
        triple_count = stripped.count('"""') + stripped.count("'''")
        if triple_count:
            if not in_docstring:
                # Entering a docstring.  If it opens and closes on same line, skip.
                if triple_count >= 2:
                    continue
                in_docstring = True
                continue
            else:
                # Closing a docstring.
                in_docstring = False
                continue
        if in_docstring:
            continue

        # Skip comments, empty lines, imports, and exempt patterns.
        if not stripped or stripped.startswith(("#", "import ")):
            continue
        if stripped.startswith("from "):
            continue
        # Skip string-only lines (inline docstrings, log messages with examples).
        if stripped.startswith(('"', "'")):
            continue
        if any(pat in stripped for pat in EXEMPT_LINE_PATTERNS):
            continue

        for match in NUMBER_PATTERN.finditer(line):
            number = match.group(1)
            if number not in ALLOWED_NUMBERS:
                findings.append((line_no, number, stripped[:80]))

    return findings
