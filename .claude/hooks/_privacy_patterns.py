"""Shared PII and consent scanning logic for Claude Code hooks.

Provides detection patterns for personally identifiable information (PII)
leaks, consent lane verification, and data classification checks.

Used by: check-privacy-patterns.py (PostToolUse and pre-commit hooks)
         check-consent-lanes.py (PostToolUse hook)
"""

from __future__ import annotations

import re
from typing import Final

# -- PII detection patterns --------------------------------------------------
# These detect PII exposure in log/print statements and data handling code.

PII_PATTERNS: Final[list[tuple[re.Pattern[str], str]]] = [
    # Email addresses in log/print statements
    (
        re.compile(
            r"(?:log(?:ger)?|print|logging)\s*[\.(].*"
            r"(?:email|e_mail|mail_addr)",
            re.IGNORECASE,
        ),
        "PII: email address in log/print output",
    ),
    # Phone numbers in log/print statements
    (
        re.compile(
            r"(?:log(?:ger)?|print|logging)\s*[\.(].*"
            r"(?:phone|tel(?:ephone)?|mobile)",
            re.IGNORECASE,
        ),
        "PII: phone number in log/print output",
    ),
    # User names in log/print statements
    (
        re.compile(
            r"(?:log(?:ger)?|print|logging)\s*[\.(].*"
            r"(?:user\.name|user_name|full_name|first_name|last_name)",
            re.IGNORECASE,
        ),
        "PII: user name in log/print output",
    ),
    # Raw transcript in log/print (should use paraphrase instead)
    (
        re.compile(
            r"(?:log(?:ger)?|print|logging)\s*[\.(].*"
            r"(?:transcript|utterance|raw_text|spoken_text)",
            re.IGNORECASE,
        ),
        "PII: raw transcript in log/print (use paraphrase instead)",
    ),
    # Audio file paths being stored (should be ephemeral)
    (
        re.compile(
            r"(?:save|write|store|persist|open\s*\().*"
            r"(?:audio_path|recording_path|wav_file|audio_file)",
            re.IGNORECASE,
        ),
        "PII: audio file being persisted (should be ephemeral)",
    ),
    # Raw transcript exposed to caregiver (should use paraphrase)
    (
        re.compile(
            r"(?:caregiver|carer|staff).*(?:transcript|utterance|raw_text)",
            re.IGNORECASE,
        ),
        "Privacy: raw transcript exposed to caregiver (use paraphrase)",
    ),
]

# -- Consent lane definitions ------------------------------------------------
# From PRD-11 Section 5: six separate consent lanes.
CONSENT_LANES: Final[tuple[str, ...]] = (
    "core-cloud",
    "caregiver-access",
    "cloud-sync",
    "community-learning",
    "research",
    "audio-research",
)

# Optional consent lanes that require an explicit opt-in check in code.
OPTIONAL_CONSENT_LANES: Final[frozenset[str]] = frozenset(
    {
        "community-learning",
        "research",
        "audio-research",
    }
)

# -- Exempt patterns ---------------------------------------------------------
# Files and patterns that are excluded from PII scanning.

PII_EXEMPT_PATTERNS: Final[tuple[str, ...]] = (
    "tests/",
    "test_",
    "conftest.py",
    "fixtures/",
    "_privacy_patterns.py",
)

# Suppression comment: add to any line to skip PII scanning for that line.
PII_SUPPRESS_COMMENT: Final[str] = "# pii-ok"

# -- Data handling function parameter names ----------------------------------
# Functions with these parameter names are considered data-handling and
# should have a consent lane annotation comment.
DATA_HANDLING_PARAMS: Final[frozenset[str]] = frozenset(
    {
        "user_id",
        "transcript",
        "profile",
        "consent",
        "audio",
        "utterance",
        "recording",
        "user_data",
        "personal_data",
    }
)
