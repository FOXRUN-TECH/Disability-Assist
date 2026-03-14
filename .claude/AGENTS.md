# AGENTS.md - Disability-Assist

Disability-Assist is an open-source assistive communication and environmental-control system for people with speech, cognitive, sensory, developmental, and age-related communication barriers. It is NOT diagnostic, therapeutic, or clinical.

**Version:** 0.0.1 | **Phase:** 0 (Documentation & Governance) | **Decision framework:** Dignity > Privacy > Accuracy > Simplicity

Full spec: [docs/PRD-00-Index.md](../docs/PRD-00-Index.md) | Roadmap: [docs/roadmap.md](../docs/roadmap.md) | Rules: [.claude/CLAUDE.md](CLAUDE.md)

## Tech Stack

Python 3.11, FastAPI, Pydantic v2, React Native (mobile, Phase 4+), PostgreSQL, Qdrant, Home Assistant

**DO NOT USE:** Black (use `ruff format`), Flask, Django, React for device, `eval()`, `exec()`, raw dicts for API data

## File-Scoped Commands [FC]

**ALWAYS use file-scoped during development.** Project-wide only when user asks or pre-PR.

| Operation | File-Scoped | Project-Wide | Time Saved |
|-----------|-------------|--------------|------------|
| Type check | `mypy cloud/api/voice.py` (3s) | `mypy cloud/` (60s) | 95% |
| Lint | `ruff check device/audio.py` (1s) | `ruff check device/` (10s) | 90% |
| Test | `pytest tests/unit/test_voice.py -x` (2s) | `pytest tests/` (3min) | 98% |

## Project Structure (Planned)

| Directory | Purpose | Key Areas |
|-----------|---------|-----------|
| `device/` | RPi5 runtime | Audio capture, action router, local cache |
| `cloud/` | Cloud inference | STT, LLM, TTS, retrieval, consent service |
| `policy/` | Policy & safety | Risk tiers, action validation, hard constraints |
| `mobile/` | React Native caregiver app | Intent feed, consent mgmt, device health |
| `infra/` | Deployment & ops | Provisioning, observability |
| `tests/` | Test suite | unit/, integration/ |
| `docs/` | PRDs & roadmap | 14 PRD documents |

## Code Style

- **Python**: snake_case, Google docstrings, `typing.Final` constants, Pydantic models
- **TypeScript**: camelCase functions, PascalCase components, strict mode, Zod validation
- **DO**: Use `constr`/`conint` validators, `BaseModel`, custom exceptions (subclass `AssistError`)
- **DON'T**: Use `eval`/`exec`, hardcoded config, raw dicts for API data

## Testing [TF]

- Behavior-driven names: `test_blocks_purchase_action_at_tier_3` (not `test_router`)
- Coverage: 95% policy/safety, 90% consent, 80% core, 70% mobile
- File-scoped first: `pytest tests/unit/test_consent.py -x`
- Deterministic: no randomness, no network calls in unit tests

## Security [SecF]

- All inputs validated (Pydantic backend, Zod mobile)
- No `eval()`, `exec()`, `Function()` with user input
- No `subprocess.run(shell=True)` with user input
- No secrets in code -- `.env` only (gitignored)
- Encrypt PII before disk write
- No PII in logs

## Privacy [PV]

- Minimum disclosure: paraphrase over verbatim for caregivers
- 6 consent lanes: core-cloud, caregiver-access, cloud-sync, community-learning, research, audio-research
- No raw audio retention without explicit consent
- Data deletable on demand
- Role-based access: user, family, professional, guardian, administrator

## Dignity [DIG]

- No patronizing language or clinical terminology
- Choice-based prompts, not leading questions
- System is assistive, not therapeutic or diagnostic
- No "personality" -- use "assistive profile"

## Git Workflow [CC]

- Branch: `feature/<name>` from `main`
- Commit: `type(scope): description` -- types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `ci`
- PR: run `/quality` -> push -> `gh pr create` with security + privacy checklists
- CI verification mandatory after every push

## Safety and Permissions

**Allowed without asking:** Read files, search code, lint/format/type-check single files, run single test file, git history, create feature branches, commit to feature branches, create PRs, install listed dev deps

**Requires approval:** New packages, config changes, full test suite, force push, push to `main`, delete files, modify auth/encryption/consent logic, CI/CD changes, non-MIT/Apache/BSD deps, changes to consent flows or risk tiers

## Trust Spectrum

| Code Area | Trust | Review Required |
|-----------|-------|-----------------|
| Consent/privacy/encryption | Very Low | Human + privacy audit + security audit |
| Risk tier enforcement | Low | Human review + full coverage |
| Voice/audio | Medium-low | Privacy review + tests |
| Cloud API | Medium | Integration tests + review |
| Mobile UI | Medium | Accessibility review + tests |
| Docs/config | High | Quick review |

## Rule Hierarchy

Tags: **[SecF]** Security First, **[QG]** Quality Gate, **[PV]** Privacy, **[DIG]** Dignity, **[CON]** Consent, **[RT]** Risk Tier, **[LIC]** License, **[SF]** Simplicity, **[RP]** Readability, **[DM]** Dependency Minimalism, **[TS]** Type Safety, **[FC]** File-Scoped, **[TF]** Tests First, **[CC]** Conventional Commits

Full rules and enforcement details: [.claude/CLAUDE.md](CLAUDE.md)
