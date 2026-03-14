"""Shared test fixtures for Disability-Assist test suite."""

from __future__ import annotations

import pytest


@pytest.fixture()
def sample_transcript() -> str:
    """Provide a sample transcript for testing."""
    return "turn on the living room light"


@pytest.fixture()
def sample_intent() -> dict[str, object]:
    """Provide a sample intent result for testing."""
    return {
        "action_class": "lighting",
        "arguments": {"entity": "living_room_light", "state": "on"},
        "risk_tier": 1,
        "confidence": 0.92,
        "caregiver_paraphrase": "Requested to turn on the living room light.",
        "clarification_request": None,
    }
