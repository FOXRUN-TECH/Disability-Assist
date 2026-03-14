"""Shared constants for Claude Code hooks.

Single source of truth for file patterns, directory skip lists, and
documentation file sets used across all PostToolUse and pre-commit hooks.
"""

from __future__ import annotations

from typing import Final

# Documentation files that satisfy the doc-update requirement.
# Paths are relative to the repository root.
DOC_FILES: Final[frozenset[str]] = frozenset(
    {
        "CLAUDE.md",
        "README.md",
        "docs/roadmap.md",
    }
)

# Top-level source directories whose changes trigger doc-update checks.
SOURCE_PATTERNS: Final[tuple[str, ...]] = (
    "device/",
    "cloud/",
    "policy/",
    "mobile/",
    "infra/",
)

# Directories to skip when checking file paths (virtual envs, caches, etc.).
SKIP_DIRS: Final[frozenset[str]] = frozenset(
    {
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "build",
        ".git",
        ".claude",
    }
)

# Patterns that exclude files even if they match SOURCE_PATTERNS.
EXCLUDE_PATTERNS: Final[tuple[str, ...]] = (
    "__pycache__",
    "node_modules",
    ".pyc",
)

# Source file extensions that trigger the doc-update reminder.
SOURCE_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".css",
        ".html",
        ".json",
        ".yaml",
    }
)

# Maximum number of mypy error lines to display in lint output.
MYPY_OUTPUT_LIMIT: Final[int] = 10

# Maximum number of line-ending violations to display per file.
LINE_ENDING_DISPLAY_LIMIT: Final[int] = 5

# File extensions that must use CRLF line endings (Windows-specific files).
CRLF_EXTENSIONS: Final[frozenset[str]] = frozenset({".bat", ".cmd", ".ps1"})

# File extensions checked for line ending consistency.
# All text source files -- anything not in CRLF_EXTENSIONS should use LF.
LINE_ENDING_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".css",
        ".html",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".cfg",
        ".ini",
        ".md",
        ".txt",
        ".sh",
        ".bash",
        ".sql",
        ".xml",
        ".svg",
        ".env",
    }
)

# CI polling configuration for post-push verification.
CI_POLL_INITIAL_WAIT_SECONDS: Final[int] = 30
CI_POLL_RETRY_WAIT_SECONDS: Final[int] = 30
CI_POLL_MAX_RETRIES: Final[int] = 20  # 10 minutes maximum
