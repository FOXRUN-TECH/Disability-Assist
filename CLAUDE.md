# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Disability-Assist** -- an open-source, cloud-first assistive communication and environmental-control system for people with speech, cognitive, sensory, developmental, and age-related communication barriers. The system interprets degraded or non-standard speech, infers intent via cloud AI, and provides voice output, smart-home control, and caregiver coordination.

**This is NOT** a diagnostic product, treatment device, clinical monitoring platform, emergency response system, or substitute for professional judgment.

**Version:** 0.0.1 | **Status:** Phase 0 (Documentation & Governance) | **License:** Open Source
**Full spec:** [docs/PRD-00-Index.md](docs/PRD-00-Index.md) | **Roadmap:** [docs/roadmap.md](docs/roadmap.md)
**Decision framework:** Dignity > Privacy > Accuracy > Simplicity

## Architecture (Planned)

Six-component system with cloud-first inference and local device runtime:

- **`device/`** -- Python RPi5 runtime (audio capture, wake word, action router, local SQLite cache)
- **`cloud/`** -- Cloud inference layer (STT, LLM intent engine, TTS, retrieval/RAG, consent service)
  - STT, LLM, TTS providers to be selected
  - PostgreSQL for accounts, consent, roles, audit
  - Qdrant for assistive priors / community patterns
- **`policy/`** -- Policy and safety layer (risk tiers 0-3, action validation, hard constraints)
- **`mobile/`** -- React Native caregiver app (Phase 4+: intent feed, consent mgmt, device health)
- **`infra/`** -- Deployment, provisioning, observability
- **`tests/`** -- Test suite (unit, integration, e2e)

### Key Data Flows

**Voice input:** RPi5 mic -> wake word (local) -> VAD + audio capture (local) -> cloud STT -> LLM intent engine -> risk tier check -> action router or voice response
**Caregiver feed:** LLM intent engine -> paraphrase (NOT raw transcript) -> role-filtered display -> mobile app
**Smart-home:** Action router -> Home Assistant API -> device command (risk tier 0-1 only)
**Consent:** User/guardian consent -> lane-specific opt-in -> scoped data flow -> revocable at any time

## Development Commands

```bash
# Python (backend/device) -- Phase 1+
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -e ".[dev]"
ruff check .                    # lint
ruff format .                   # format
mypy device/ cloud/ policy/ --ignore-missing-imports
pytest                          # all tests
pytest tests/unit/ -v           # unit only

# React Native (mobile app) -- Phase 4+
cd mobile && npm ci
npx eslint src/
npx jest

# Documentation
npx markdownlint-cli2 "docs/**/*.md"
```

## Code Style

- **Ruff** handles linting (E, W, F, I, B, C4, UP, D, TRY, SIM, PIE, RUF rules) and formatting
- **Google-style docstrings** enforced by Ruff D rules (`convention = "google"`)
- **Mypy** performs static type checking (`disallow_untyped_defs = true`)
- **No magic numbers** -- use `typing.Final` constants (enforced by `check-magic-numbers.py` hook)
- **Line endings** -- LF for all text files, CRLF only for `.bat`/`.cmd`/`.ps1`
- Line length: 100 characters
- Target: Python 3.11+
- Config lives in pyproject.toml
- ESLint + Prettier for React Native (Phase 4+)
- Claude Code PostToolUse hooks: auto-lint, magic numbers, line endings, phase scope, PII detection, consent lane verification

## Phase Status

| Phase | Name | Status |
|-------|------|--------|
| **Phase 0** | **Repo Foundation & Governance** | **In Progress** |
| Phase 1 | Core Cloud Speech & Device Loop | Planned |
| Phase 2 | Smart-Home & Media Control | Planned |
| Phase 3 | Personalization & Assistive Profile | Planned |
| Phase 4 | Caregiver App & Role-Based Access | Planned |
| Phase 5 | Consent, Retention & Deletion Controls | Planned |
| Phase 6 | Pilot Operations Package | Planned |
| Phase 7 | v1 Pilot Launch | Planned |
| Phase 8 | v2 Shared Intelligence Foundation | Planned |
| Phase 9 | Research Workflow & Governance | Planned |

Full roadmap with milestones: [docs/roadmap.md](docs/roadmap.md)

### Phase 0 Scope

- Repository structure and documentation baseline
- Architecture decision records template
- Threat model, data classification matrix, consent lane matrix
- User role matrix (user, family, professional, guardian, administrator)
- `.claude` configuration and governance tooling
- Issue and milestone taxonomy

## Claude-Specific Rules

1. **Do NOT run full test suites** unless the user explicitly asks. Targeted single-file tests are OK.
2. **Do NOT auto-update documentation** unless the user explicitly asks. Pre-commit hooks catch missing updates.
3. **No hardcoded config values** -- use config modules or constants with `typing.Final`.
4. **CI must pass after every push** -- verify with `gh run list --limit 1` after pushing.
5. **Privacy-first** -- no PII in logs, no audio retention without consent, minimum disclosure for caregivers.
6. **Dignity-first language** -- never patronizing, never clinical, never diagnostic. System is assistive.
7. **No API keys or secrets in code** -- secrets go in `.env` (gitignored).
8. **Consent lanes** -- every data flow must identify which consent lane it belongs to (6 lanes from PRD-11).
9. **Risk tier discipline** -- all actions must have a documented risk tier (0-3). Tier 0-1 free, Tier 2 confirm, Tier 3 blocked.
10. **Hard constraints** -- never generate code that executes purchases, medication advice, emergency calls, or clinical judgments.

## Documentation Update Policy

When source files (`device/`, `cloud/`, `policy/`, `mobile/`, `infra/`) are modified, keep these in sync:

- **`CLAUDE.md`** -- Phase status, architecture, module changes
- **`README.md`** -- Project status, features, structure
- **`docs/roadmap.md`** -- Phase completion status

Pre-commit hook enforces this (bypass with `--no-verify` for trivial changes).

## Key Constraints

- **Privacy**: PIPEDA (Canada), HIPAA-adjacent (US), GDPR (EU), UK GDPR compliance readiness
- **Assistive**: System must never simulate therapy, invent memories, fabricate caregiver communications
- **Action safety**: Risk tiers 0-3, hard constraints on purchases/medication/emergency/clinical
- **No medical claims**: System is assistive, not diagnostic or therapeutic
- **Deployment**: 10-20 unit pilot scope, scalable architecture
- **Cost**: Cloud operating target CAD 8-15 per user per month
- **Performance**: Median end-to-end response <= 3.5 seconds (cloud-connected)
- **Hardware**: Raspberry Pi 5 target, CAD 190-320 per unit

## Environment Configuration (Planned)

Copy `.env.example` to `.env`. Key variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `STT_PROVIDER` | Yes | Cloud STT provider (to be selected) |
| `LLM_PROVIDER` | Yes | Cloud LLM provider |
| `TTS_PROVIDER` | Yes | Cloud TTS provider |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `QDRANT_URL` | No | Vector store for assistive priors |
| `HOME_ASSISTANT_URL` | No | Home Assistant API endpoint |
| `HOME_ASSISTANT_TOKEN` | No | Home Assistant long-lived access token |
| `HOST_SUFFIX_ID` | For device | RPi5 IP suffix (e.g., `90` for `192.168.137.90`) |
| `SSH_USERNAME` | For device | SSH username for RPi5 |
| `DEBUG` | No | Debug mode (default: `false`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |
