"""Phase-to-file-path mapping for commit scope enforcement.

Each phase maps to a set of path prefixes that belong to it.
Shared files (config, docs, .claude/) are allowed in any phase.
Update ACTIVE_PHASE when phases complete (or use /phase-complete).

Phases follow the roadmap in docs/roadmap.md:
  0 -- Repo foundation and governance
  1 -- Core cloud speech and device loop
  2 -- Smart-home and media control
  3 -- Personalization and assistive profile
  4 -- Caregiver app and role-based access
  5 -- Consent, retention, and deletion controls
  6 -- Pilot operations package
  7 -- v1 pilot launch
  8 -- v2 shared intelligence foundation
  9 -- Research workflow and governance

Used by: check-phase-scope.py (PostToolUse hook)
"""

from __future__ import annotations

from typing import Final

# Current active phase -- update this as phases complete.
ACTIVE_PHASE: Final[str] = "1"

# Files that are always allowed regardless of phase.
SHARED_PATHS: Final[frozenset[str]] = frozenset(
    {
        ".claude/",
        "config/",
        "docs/",
        "tests/",
        ".github/",
        ".pre-commit-config.yaml",
        "pyproject.toml",
        "CLAUDE.md",
        "README.md",
        ".env.example",
        ".gitignore",
        "scripts/",
    }
)

# Phase -> allowed file path prefixes (in addition to SHARED_PATHS).
PHASE_FILE_MAP: Final[dict[str, frozenset[str]]] = {
    "0": frozenset(
        {
            "docs/",
            ".claude/",
            "config/",
            "scripts/",
        }
    ),
    "1": frozenset(
        {
            "device/",
            "cloud/",
            "policy/",
            "tests/unit/",
        }
    ),
    "2": frozenset(
        {
            "device/smarthome/",
            "cloud/",
            "tests/",
        }
    ),
    "3": frozenset(
        {
            "device/profile/",
            "cloud/personalization/",
            "tests/",
        }
    ),
    "4": frozenset(
        {
            "mobile/",
            "cloud/api/caregiver/",
            "tests/",
        }
    ),
    "5": frozenset(
        {
            "cloud/consent/",
            "policy/",
            "device/consent/",
            "tests/",
        }
    ),
    "6": frozenset(
        {
            "infra/",
            "scripts/",
            "docs/",
        }
    ),
    "7": frozenset(
        {
            "infra/",
            "docs/",
            "scripts/",
        }
    ),
    "8": frozenset(
        {
            "cloud/rag/",
            "cloud/priors/",
            "tests/",
        }
    ),
    "9": frozenset(
        {
            "cloud/research/",
            "infra/research/",
            "tests/",
        }
    ),
}

# Phase -> required documentation files for phase-end commits.
PHASE_COMPLETION_DOCS: Final[dict[str, frozenset[str]]] = {
    "0": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "1": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "2": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "3": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "4": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "5": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "6": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "7": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "8": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
    "9": frozenset(
        {
            "CLAUDE.md",
            "README.md",
            "docs/roadmap.md",
        }
    ),
}
