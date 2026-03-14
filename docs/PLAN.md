# PLAN.md -- Disability-Assist Implementation Plan

## Context

Disability-Assist is an open-source, cloud-first assistive communication system for people with speech, cognitive, sensory, and age-related communication barriers. The project has completed Phase 0 (documentation and governance) with 14 PRDs, a roadmap, and Claude Code tooling in place. No source code exists yet.

This plan breaks the 10-phase roadmap (Phases 0-9) into 41 subphases, each sized to complete within ~100k tokens of Claude Code context (well under the 70% limit). It maximizes parallel agent usage and reuse of production code from `D:\GitHub\Mira\voice-pipeline\voice_pipeline\`.

**Decision framework:** Dignity > Privacy > Accuracy > Simplicity

---

## Conventions

- **Complexity**: S = small (~30k tokens), M = medium (~60k tokens), L = large (~90k tokens)
- **Mira paths**: Relative to `D:\GitHub\Mira\`
- **Project paths**: Relative to `D:\GitHub\AI-Assist\`
- **Agents**: Where marked, tasks within a subphase can run as parallel Claude Code agents

---

## Mira Reuse Map

| Component | Mira Source | Adaptation |
|-----------|------------|------------|
| Cloud STT (Deepgram) | `voice_pipeline/cloud_stt.py` | Add consent lane tracking, privacy patterns |
| Cloud LLM (Claude) | `voice_pipeline/cloud_llm.py` | Repurpose as intent engine, add risk tiers |
| Cloud TTS (Azure) | `voice_pipeline/cloud_tts.py` | Add assistive voice params (pitch, rate, EQ) |
| TTS Facade + Engines | `voice_pipeline/tts.py` + `tts_engines/` | Reuse with sensory-safe mode additions |
| Local STT (Whisper) | `voice_pipeline/stt.py` | Degraded-mode fallback |
| Orchestrator | `voice_pipeline/orchestrator.py` | Refactor for intent->action->risk tier flow |
| Exceptions | `voice_pipeline/exceptions.py` | Extend with consent/privacy/policy exceptions |
| Constants | `voice_pipeline/constants.py` | Adapt naming, add assistive constants |
| Config loading | `mira_comm/config/loader.py` | Multi-source config merge |
| Config models | `mira_comm/config/models.py` | Pydantic schemas for device/cloud/policy |
| Encryption | `mirror-api/app/core/encryption.py` | Reuse for PII/consent data |
| Keyring store | `mirror-api/app/core/keyring_store.py` | Secret storage |
| HAL pattern | `mirror-api/app/core/hal.py` | Device hardware abstraction |
| WebSocket | `mirror-api/app/api/voice_ws.py` | Real-time caregiver feed |
| SSH client | `mira_comm/ssh/client.py` | Device provisioning |
| Network stack | `mira_comm/network/` | Connectivity testing |
| CLI framework | `mira_comm/cli/` | Device management |
| FastAPI patterns | `mirror-api/app/` | API structure, middleware |
| Docker patterns | `Dockerfile`, `docker-compose.yml` | Deployment |

**Shared dependency stack:** Python 3.11+, FastAPI, Pydantic 2.x, SQLAlchemy 2.0+, anthropic, deepgram-sdk, azure-cognitiveservices-speech, faster-whisper, pyaudio, sounddevice, paramiko, cryptography, ruff, mypy, pytest

---

## Phase 0: Repo Foundation and Governance (IN PROGRESS)

### Subphase 0a: Project Scaffolding and pyproject.toml [S]

**Goal**: Create the Python project skeleton so all future phases have a runnable project.

**Files to Create**:
- `pyproject.toml` -- dependencies, ruff/mypy/pytest config
- `.env.example` -- all environment variables documented
- `.pre-commit-config.yaml` -- hook configuration
- `.github/workflows/ci.yml` -- GitHub Actions CI
- `device/__init__.py`, `cloud/__init__.py`, `policy/__init__.py`, `infra/__init__.py`, `tests/__init__.py`
- `tests/conftest.py`

**Reuse**: `pyproject.toml` structure and ruff/mypy config from Mira

**Parallel Agents**:
- Agent A: pyproject.toml + .env.example
- Agent B: CI workflow + .pre-commit-config.yaml
- Agent C: directory stubs + tests/conftest.py

**Verification**: `ruff check .`, `mypy --version`, `pytest --collect-only`, `pre-commit run --all-files`

**Depends on**: Nothing

---

### Subphase 0b: Governance Documents [S]

**Goal**: Create formal governance documents required by the PRDs.

**Files to Create**:
- `docs/governance/threat-model.md`
- `docs/governance/data-classification-matrix.md`
- `docs/governance/consent-lane-matrix.md`
- `docs/governance/user-role-matrix.md`
- `docs/governance/adr-template.md`
- `docs/governance/adr/ADR-001-cloud-first-architecture.md`
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`

**Reuse**: `CONTRIBUTING.md` and `SECURITY.md` patterns from Mira

**Parallel Agents**:
- Agent A: threat-model + data-classification-matrix
- Agent B: consent-lane-matrix + user-role-matrix
- Agent C: ADR template + ADR-001 + CONTRIBUTING + SECURITY + CODE_OF_CONDUCT

**Verification**: `npx markdownlint-cli2 "docs/**/*.md"`

**Depends on**: 0a

---

### Subphase 0c: Phase 0 Completion [S]

**Goal**: Mark Phase 0 complete, update phase config to Phase 1.

**Files to Modify**:
- `CLAUDE.md` -- phase status table
- `README.md` -- project status
- `docs/roadmap.md` -- mark Phase 0 complete
- `.claude/hooks/_phase_config.py` -- set ACTIVE_PHASE = "1"

**Verification**: `/phase-complete`, all pre-commit hooks pass

**Depends on**: 0a, 0b

---

## Phase 1: Core Cloud Speech and Device Loop

The largest phase. Establishes the end-to-end voice interaction pipeline. Heavy Mira reuse.

### Subphase 1a: Exception Hierarchy and Constants [S]

**Goal**: Establish `AssistError` base exception hierarchy and central constants. Every subsequent subphase depends on these.

**Files to Create**:
- `cloud/exceptions.py` -- `AssistError` base, `STTError`, `LLMError`, `TTSError`, `PolicyError`, `ConsentError`, `ActionError`, `ConfigError`
- `cloud/constants.py` -- `typing.Final` constants for cloud services
- `device/exceptions.py` -- `DeviceError`, `AudioCaptureError`, `WakeWordError`
- `device/constants.py` -- device-specific constants
- `policy/exceptions.py` -- `PolicyViolationError`, `RiskTierBlockedError`, `HardConstraintError`
- `policy/constants.py` -- risk tier definitions, hard constraint lists
- `tests/unit/test_exceptions.py`

**Reuse**: `voice_pipeline/exceptions.py` (rename base), `voice_pipeline/constants.py` (extract and adapt)

**Parallel Agents**:
- Agent A: cloud/exceptions.py + cloud/constants.py
- Agent B: device/exceptions.py + device/constants.py
- Agent C: policy/exceptions.py + policy/constants.py + tests

**Verification**: `ruff check cloud/ device/ policy/`, `mypy cloud/ device/ policy/`, `pytest tests/unit/test_exceptions.py`

**Depends on**: 0c

---

### Subphase 1b: Configuration System [M]

**Goal**: Multi-source config loader (env > file > defaults) and Pydantic config models.

**Files to Create**:
- `cloud/config/loader.py` -- multi-source config loading
- `cloud/config/models.py` -- `CloudConfig`, `STTConfig`, `LLMConfig`, `TTSConfig`, `DatabaseConfig`
- `device/config/models.py` -- `DeviceConfig`, `AudioConfig`, `WakeWordConfig`
- `policy/config/models.py` -- `PolicyConfig`, `RiskTierConfig`
- `config/default-config.json` -- default values
- `tests/unit/test_config_loader.py`, `tests/unit/test_config_models.py`

**Reuse**: `mira_comm/config/loader.py` (merge pattern), `mira_comm/config/models.py` (Pydantic patterns), `mirror-api/app/core/config.py` (settings singleton)

**Parallel Agents**:
- Agent A: cloud/config/ (loader + models)
- Agent B: device/config/models.py + policy/config/models.py
- Agent C: tests + config/default-config.json

**Verification**: `pytest tests/unit/test_config_*.py -v`, `mypy cloud/config/ device/config/ policy/config/`

**Depends on**: 1a

---

### Subphase 1c: Cloud STT Client [M]

**Goal**: Adapt Mira Deepgram STT client with consent lane tracking, whisper acceptance, pause tolerance, transcript length limits.

**Files to Create**:
- `cloud/stt/client.py` -- `CloudSTT` class
- `cloud/stt/models.py` -- `TranscriptionResult` (extends Mira's with confidence, consent metadata)
- `cloud/stt/protocols.py` -- `STTProvider` Protocol
- `tests/unit/cloud/test_stt_client.py`, `tests/unit/cloud/test_stt_models.py`

**Reuse**: `voice_pipeline/cloud_stt.py` (direct adaptation), `voice_pipeline/transcription_result.py` (base model)

**Parallel Agents**:
- Agent A: client.py + protocols.py
- Agent B: models.py + tests

**Verification**: `pytest tests/unit/cloud/test_stt_*.py -v`, `mypy cloud/stt/`

**Depends on**: 1a, 1b

---

### Subphase 1d: Cloud LLM Intent Engine [L]

**Goal**: Build the intent engine wrapping Claude LLM for structured intent output with risk tiers, action params, caregiver paraphrases, and confidence bands. This is the most critical Mira adaptation -- Mira's `CloudLLM` is conversational, but DA needs structured intent inference.

**Files to Create**:
- `cloud/llm/client.py` -- `IntentEngine` class
- `cloud/llm/prompts.py` -- system prompts for assistive intent inference
- `cloud/llm/models.py` -- `IntentResult` (action_class, arguments, risk_tier, confidence, caregiver_paraphrase, clarification_request)
- `cloud/llm/protocols.py` -- `LLMProvider` Protocol
- `policy/risk_tiers.py` -- `RiskTier` enum (0-3), validation, hard constraint list
- `policy/validators.py` -- `validate_action()`, `enforce_hard_constraints()`
- `tests/unit/cloud/test_intent_engine.py`, `tests/unit/policy/test_risk_tiers.py`, `tests/unit/policy/test_validators.py`

**Reuse**: `voice_pipeline/cloud_llm.py` (class structure, streaming, history), `voice_pipeline/intent_parser.py` (action tag extraction)

**Parallel Agents**:
- Agent A: cloud/llm/client.py + protocols.py
- Agent B: cloud/llm/prompts.py + models.py
- Agent C: policy/risk_tiers.py + policy/validators.py + all tests

**Verification**: `pytest tests/unit/cloud/test_intent_engine.py tests/unit/policy/ -v`, `mypy cloud/llm/ policy/`

**Depends on**: 1a, 1b, 1c

---

### Subphase 1e: Cloud TTS Client [M]

**Goal**: Adapt Mira Azure TTS with assistive voice parameters (pitch, rate, EQ, sensory-safe mode, intelligibility mode, text-only mode).

**Files to Create**:
- `cloud/tts/client.py` -- `CloudTTS` class
- `cloud/tts/models.py` -- `VoiceProfile` (pitch, rate, loudness, pause_spacing, eq_profile, mode)
- `cloud/tts/protocols.py` -- `TTSProvider` Protocol
- `cloud/tts/modes.py` -- `AccessibilityMode` enum
- `tests/unit/cloud/test_tts_client.py`

**Reuse**: `voice_pipeline/cloud_tts.py` (Azure streaming), `voice_pipeline/tts.py` (facade pattern), `voice_pipeline/tts_engines/base.py` (Protocol)

**Parallel Agents**:
- Agent A: client.py + protocols.py
- Agent B: models.py + modes.py + tests

**Verification**: `pytest tests/unit/cloud/test_tts_*.py -v`, `mypy cloud/tts/`

**Depends on**: 1a, 1b

---

### Subphase 1f: Device Audio Capture and Wake Word [M]

**Goal**: Port Mira audio capture and wake word for RPi5 with accessibility adaptations (whisper mode, longer silence tolerance, configurable gain).

**Files to Create**:
- `device/audio/capture.py` -- `AudioCapture` class
- `device/audio/wake_word.py` -- `WakeWordDetector` class
- `device/audio/vad.py` -- VAD wrapper with configurable sensitivity
- `tests/unit/device/test_audio_capture.py`, `tests/unit/device/test_wake_word.py`

**Reuse**: `voice_pipeline/audio_capture.py` (PyAudio + silero-vad), `voice_pipeline/wake_word.py` (openWakeWord)

**Parallel Agents**:
- Agent A: capture.py + vad.py
- Agent B: wake_word.py + tests

**Verification**: `pytest tests/unit/device/test_audio_*.py tests/unit/device/test_wake_word.py -v`

**Depends on**: 1a, 1b

---

### Subphase 1g: Device Action Router [M]

**Goal**: Build action router that receives intent results and dispatches to handlers (voice response, smart-home stub, caregiver bridge stub) with risk-tier enforcement.

**Files to Create**:
- `device/router/action_router.py` -- `ActionRouter` class
- `device/router/models.py` -- `ActionRequest`, `ActionResult`
- `device/router/handlers/base.py` -- `ActionHandler` Protocol
- `device/router/handlers/voice_response.py`
- `device/router/handlers/clarification.py`
- `tests/unit/device/test_action_router.py`, `tests/unit/device/test_handlers.py`

**Reuse**: `voice_pipeline/command_executor.py` (dispatch and result patterns)

**Parallel Agents**:
- Agent A: action_router.py + models.py
- Agent B: handlers/ + tests

**Verification**: `pytest tests/unit/device/test_action_router.py tests/unit/device/test_handlers.py -v`

**Depends on**: 1a, 1b, 1d (IntentResult), 1e (TTS)

---

### Subphase 1h: Device Orchestrator [L]

**Goal**: Core state machine tying together: wake word -> audio capture -> cloud STT -> intent engine -> policy check -> action router -> TTS response. Adapted from Mira's orchestrator for the intent-action-risk-tier flow.

**Files to Create**:
- `device/orchestrator/pipeline.py` -- `Pipeline` (idle -> listening -> processing -> responding)
- `device/orchestrator/session.py` -- `Session` (turn history, context)
- `device/orchestrator/degraded.py` -- degraded-mode handler (local-only allow-list)
- `device/main.py` -- entry point
- `tests/unit/device/test_pipeline.py`, `tests/unit/device/test_session.py`
- `tests/integration/test_pipeline_e2e.py`

**Reuse**: `voice_pipeline/orchestrator.py` (state machine, signal handling)

**Parallel Agents**:
- Agent A: pipeline.py (core state machine)
- Agent B: session.py + degraded.py
- Agent C: main.py + all tests

**Verification**: `pytest tests/unit/device/ tests/integration/test_pipeline_e2e.py -v`, `mypy device/`

**Depends on**: 1c, 1d, 1e, 1f, 1g (all pipeline components)

---

### Subphase 1i: Cloud API Server Foundation [M]

**Goal**: FastAPI cloud server with health check, voice endpoint, and middleware.

**Files to Create**:
- `cloud/api/app.py` -- FastAPI application factory
- `cloud/api/routes/health.py` -- health check
- `cloud/api/routes/voice.py` -- voice processing endpoint (STT -> LLM -> TTS)
- `cloud/api/middleware/logging.py` -- request/response logging (no PII)
- `cloud/api/middleware/errors.py` -- exception-to-HTTP mapping
- `cloud/main.py` -- uvicorn entry point
- `tests/unit/cloud/test_api_health.py`, `tests/unit/cloud/test_api_voice.py`

**Reuse**: `mirror-api/app/main.py` (app factory), `mirror-api/app/api/voice.py` (endpoint structure)

**Parallel Agents**:
- Agent A: app.py + main.py + routes/health.py
- Agent B: routes/voice.py + middleware/
- Agent C: tests

**Verification**: `pytest tests/unit/cloud/test_api_*.py -v`, `mypy cloud/api/`

**Depends on**: 1a, 1b, 1c, 1d, 1e

---

### Subphase 1j: Encryption and Secrets Management [S]

**Goal**: Port Mira encryption for PII, consent data, and secrets at rest.

**Files to Create**:
- `cloud/security/encryption.py` -- Fernet encryption (PBKDF2, machine ID)
- `cloud/security/secrets.py` -- secret storage (keyring + fallback)
- `tests/unit/cloud/test_encryption.py`, `tests/unit/cloud/test_secrets.py`

**Reuse**: `mirror-api/app/core/encryption.py` (direct port), `mirror-api/app/core/keyring_store.py`

**Parallel Agents**:
- Agent A: encryption.py + tests
- Agent B: secrets.py + tests

**Verification**: `pytest tests/unit/cloud/test_encryption.py tests/unit/cloud/test_secrets.py -v`

**Depends on**: 1a

---

### Subphase 1k: Instrumentation and Latency Tracking [S]

**Goal**: Latency and failure instrumentation for all pipeline stages. Target: median <= 3.5s.

**Files to Create**:
- `cloud/observability/metrics.py` -- timing decorators, latency tracking
- `cloud/observability/logging.py` -- structured JSON logging (no PII)
- `device/observability/health.py` -- device health reporting
- `tests/unit/test_metrics.py`

**Reuse**: `mirror-api/app/api/analytics.py` (timing patterns)

**Parallel Agents**:
- Agent A: cloud/observability/
- Agent B: device/observability/ + tests

**Verification**: `pytest tests/unit/test_metrics.py -v`

**Depends on**: 1a

---

## Phase 2: Smart-Home and Media Control

### Subphase 2a: Home Assistant Client [M]

**Goal**: HA REST API client for device control (lights, switches, scenes, media, thermostat).

**Files to Create**:
- `device/smarthome/ha_client.py` -- Home Assistant API client (httpx async)
- `device/smarthome/models.py` -- `HAEntity`, `HAState`, `HAServiceCall`
- `device/smarthome/constants.py`
- `tests/unit/device/test_ha_client.py`

**Reuse**: `mirror-api/app/api/lighting.py` (HA integration), `mirror-api/app/core/hal.py` (Protocol pattern)

**Parallel Agents**:
- Agent A: ha_client.py + constants.py
- Agent B: models.py + tests

**Depends on**: 1a, 1b

---

### Subphase 2b: Smart-Home Action Handlers [M]

**Goal**: Implement handlers for v1 action classes: lights, media, TV, comfort routines, reminders, caregiver alerts. Wire into action router.

**Files to Create**:
- `device/router/handlers/lighting.py`
- `device/router/handlers/media.py`
- `device/router/handlers/routine.py`
- `device/router/handlers/reminder.py`
- `device/router/handlers/caregiver_alert.py`
- `device/smarthome/aliases.py` -- user-specific device name aliases
- `tests/unit/device/test_lighting_handler.py`, `tests/unit/device/test_media_handler.py`

**Reuse**: `voice_pipeline/command_executor.py` (dispatch patterns)

**Parallel Agents**:
- Agent A: lighting.py + media.py
- Agent B: routine.py + reminder.py + caregiver_alert.py
- Agent C: aliases.py + tests

**Depends on**: 1g, 2a

---

### Subphase 2c: Confirmation Policy and Action Audit [M]

**Goal**: Confirmation flow for risk tier 2, hard constraint blocking for tier 3, duplicate suppression, idempotent execution, and action audit log.

**Files to Create**:
- `policy/confirmation.py` -- confirmation flow
- `policy/audit.py` -- action audit log (local SQLite + cloud sync)
- `policy/dedup.py` -- duplicate action suppression
- `device/router/confirmation_handler.py`
- `tests/unit/policy/test_confirmation.py`, `tests/unit/policy/test_audit.py`, `tests/unit/policy/test_dedup.py`

**Parallel Agents**:
- Agent A: confirmation.py + dedup.py
- Agent B: audit.py + confirmation_handler.py
- Agent C: tests (coverage target: 95% on policy/)

**Depends on**: 1d, 1g, 2b

---

### Subphase 2d: Compatibility Matrix and Integration Tests [S]

**Goal**: Document supported devices and write e2e integration tests for voice-to-action path.

**Files to Create**:
- `docs/compatibility-matrix.md`
- `tests/integration/test_smarthome_e2e.py`
- `tests/integration/conftest.py`

**Depends on**: 2a, 2b, 2c

---

## Phase 3: Personalization and Assistive Profile

### Subphase 3a: Local Profile Store [M]

**Goal**: SQLite-based assistive profile store for vocabulary, aliases, settings, routines, and history.

**Files to Create**:
- `device/profile/store.py` -- SQLite CRUD
- `device/profile/models.py` -- `AssistiveProfile`, `VocabularyMapping`, `DeviceAlias`, `Routine`, `AccessibilitySettings`
- `device/profile/constants.py` -- retention defaults (30 days)
- `device/profile/migrations.py`
- `tests/unit/device/test_profile_store.py`

**Reuse**: `mirror-api/app/core/state_store.py` (SQLite patterns)

**Parallel Agents**:
- Agent A: store.py + migrations.py
- Agent B: models.py + constants.py + tests

**Depends on**: 1a, 1b, 1j

---

### Subphase 3b: Vocabulary and Phrase Normalization [M]

**Goal**: Vocabulary mapping engine for non-standard speech (aphasic substitutions, echolalia, scripted phrases) -> recognized intents. Integrates with LLM as context.

**Files to Create**:
- `cloud/personalization/vocabulary.py` -- mapper (lookup, fuzzy match, learning)
- `cloud/personalization/normalizer.py` -- phrase normalization
- `cloud/personalization/context_builder.py` -- build LLM context from profile + vocabulary + routine
- `tests/unit/cloud/test_vocabulary.py`, `tests/unit/cloud/test_normalizer.py`, `tests/unit/cloud/test_context_builder.py`

**Parallel Agents**:
- Agent A: vocabulary.py + normalizer.py
- Agent B: context_builder.py + tests

**Depends on**: 3a, 1d

---

### Subphase 3c: Voice Output Tuning and Profile Admin [M]

**Goal**: Per-user voice output tuning and caregiver-visible profile administration API.

**Files to Create**:
- `cloud/tts/voice_profile.py` -- load/save from assistive profile
- `cloud/api/routes/profile.py` -- profile CRUD API (role-gated)
- `device/profile/export.py` -- profile export and wipe
- `tests/unit/cloud/test_voice_profile.py`, `tests/unit/cloud/test_profile_api.py`

**Parallel Agents**:
- Agent A: voice_profile.py + export.py
- Agent B: API routes + tests

**Depends on**: 3a, 3b, 1e

---

## Phase 4: Caregiver App and Role-Based Access

### Subphase 4a: Authentication and Role Model [M]

**Goal**: JWT auth system and RBAC (user, family caregiver, professional caregiver, guardian, administrator).

**Files to Create**:
- `cloud/auth/models.py` -- `User`, `Role`, `RoleAssignment`, `DevicePairing`
- `cloud/auth/jwt.py` -- JWT creation/validation
- `cloud/auth/rbac.py` -- role-based access control
- `cloud/auth/constants.py` -- role definitions, permission matrix
- `cloud/api/routes/auth.py` -- login, register, device pairing
- `cloud/api/middleware/auth.py` -- JWT middleware
- `tests/unit/cloud/test_auth.py`, `tests/unit/cloud/test_rbac.py`

**Parallel Agents**:
- Agent A: models.py + jwt.py + constants.py
- Agent B: rbac.py + middleware/auth.py
- Agent C: routes/auth.py + tests

**Depends on**: 1i, 1j

---

### Subphase 4b: Database Models and Migrations [M]

**Goal**: PostgreSQL schema with SQLAlchemy 2.0 for accounts, consent, roles, audit, devices.

**Files to Create**:
- `cloud/db/engine.py` -- async SQLAlchemy engine + session factory
- `cloud/db/models/user.py`, `cloud/db/models/device.py`, `cloud/db/models/consent.py`, `cloud/db/models/audit.py`
- `cloud/db/migrations/` -- Alembic setup
- `tests/unit/cloud/test_db_models.py`

**Parallel Agents**:
- Agent A: engine.py + models/user.py + models/device.py
- Agent B: models/consent.py + models/audit.py
- Agent C: migrations + tests

**Depends on**: 1b, 4a

---

### Subphase 4c: Caregiver Event Feed API [M]

**Goal**: Real-time WebSocket caregiver feed. Events: likely intent, confidence, action result, clarifications, escalations. Raw transcript NOT exposed by default.

**Files to Create**:
- `cloud/api/routes/caregiver/feed.py` -- WebSocket endpoint
- `cloud/api/routes/caregiver/models.py` -- `CaregiverEvent`, `IntentSummary`, `EscalationAlert`
- `cloud/api/routes/caregiver/feed_service.py` -- event filtering by role, paraphrase generation
- `cloud/api/routes/caregiver/transcript_access.py` -- elevated access (audited)
- `tests/unit/cloud/test_caregiver_feed.py`

**Reuse**: `mirror-api/app/api/voice_ws.py` (WebSocket pattern)

**Parallel Agents**:
- Agent A: feed.py + feed_service.py
- Agent B: models.py + transcript_access.py + tests

**Depends on**: 4a, 4b, 1d

---

### Subphase 4d: React Native Caregiver App Foundation [L]

**Goal**: Initialize React Native project with TypeScript, navigation, auth, and basic feed screen.

**Files to Create**:
- `mobile/package.json`, `mobile/tsconfig.json`, `mobile/.eslintrc.js`
- `mobile/src/App.tsx`, `mobile/src/navigation/`
- `mobile/src/screens/LoginScreen.tsx`, `mobile/src/screens/FeedScreen.tsx`, `mobile/src/screens/DeviceHealthScreen.tsx`
- `mobile/src/services/auth.ts`, `mobile/src/services/websocket.ts`
- `mobile/src/schemas/` -- Zod validation
- `mobile/src/__tests__/`

**Parallel Agents**:
- Agent A: project setup (package.json, tsconfig, eslint, App.tsx, navigation)
- Agent B: screens (Login, Feed, DeviceHealth)
- Agent C: services + schemas + tests

**Depends on**: 4c

---

### Subphase 4e: Assisted-Home Mode and Audit View [M]

**Goal**: Staff restricted to assigned residents, shift-safe summaries, handover notes, per-access audit logging.

**Files to Create**:
- `cloud/api/routes/caregiver/assisted_home.py`
- `cloud/api/routes/audit.py`
- `mobile/src/screens/AuditScreen.tsx`, `mobile/src/screens/RosterScreen.tsx`
- `tests/unit/cloud/test_assisted_home.py`, `tests/unit/cloud/test_audit_api.py`

**Parallel Agents**:
- Agent A: cloud API routes + tests
- Agent B: mobile screens

**Depends on**: 4a, 4b, 4c, 4d

---

## Phase 5: Consent, Retention, and Deletion Controls

### Subphase 5a: Consent Lane Service [M]

**Goal**: Lane-based consent covering all 6 lanes from PRD-11. Separate opt-in/out, versioning, timestamps.

**Files to Create**:
- `cloud/consent/service.py` -- `ConsentService` (grant, revoke, query, version)
- `cloud/consent/models.py` -- `ConsentLane` enum, `ConsentGrant`, `ConsentRevocation`
- `cloud/consent/constants.py`
- `cloud/api/routes/consent.py`
- `device/consent/cache.py` -- local consent cache
- `tests/unit/cloud/test_consent_service.py`, `tests/unit/device/test_consent_cache.py`

**Parallel Agents**:
- Agent A: service.py + models.py + constants.py
- Agent B: API routes + device/consent/cache.py
- Agent C: tests (coverage target: 90%)

**Depends on**: 4b

---

### Subphase 5b: Guardian and Substitute Decision-Maker Flows [M]

**Goal**: Capacity model: self-directed adults, guardian-managed, minors, fluctuating capacity.

**Files to Create**:
- `cloud/consent/guardian.py`, `cloud/consent/capacity.py`
- `cloud/api/routes/guardian.py`
- `mobile/src/screens/ConsentScreen.tsx`, `mobile/src/screens/GuardianScreen.tsx`
- `tests/unit/cloud/test_guardian.py`, `tests/unit/cloud/test_capacity.py`

**Parallel Agents**:
- Agent A: guardian.py + capacity.py + tests
- Agent B: API routes + mobile screens

**Depends on**: 5a, 4a

---

### Subphase 5c: Retention Scheduler and Deletion Workflow [M]

**Goal**: Bounded retention (30-day default), cleanup scheduler, trackable deletion requests.

**Files to Create**:
- `cloud/retention/scheduler.py`, `cloud/retention/models.py`, `cloud/retention/deletion.py`
- `cloud/api/routes/retention.py`
- `tests/unit/cloud/test_retention.py`, `tests/unit/cloud/test_deletion.py`

**Parallel Agents**:
- Agent A: scheduler.py + models.py
- Agent B: deletion.py + API routes + tests

**Depends on**: 5a, 4b

---

### Subphase 5d: Consent Integration Tests and Mobile UI [S]

**Goal**: Full consent lifecycle integration tests. Participation toggles in mobile app.

**Files to Create**:
- `tests/integration/test_consent_lifecycle.py`
- `mobile/src/screens/PrivacySettingsScreen.tsx`
- `mobile/src/components/ConsentToggle.tsx`

**Parallel Agents**:
- Agent A: integration tests
- Agent B: mobile screens + components

**Depends on**: 5a, 5b, 5c

---

## Phase 6: Pilot Operations Package

### Subphase 6a: Device Provisioning and Registration [M]

**Goal**: Provision RPi5: image, register with cloud, establish credentials, verify connectivity.

**Files to Create**:
- `infra/provisioning/imager.py`, `infra/provisioning/register.py`, `infra/provisioning/credentials.py`, `infra/provisioning/verify.py`
- `scripts/provision-device.sh`
- `cloud/api/routes/device.py`
- `tests/unit/infra/test_provisioning.py`

**Reuse**: `mira_comm/ssh/client.py`, `mira_comm/network/connectivity.py`, `mira_comm/network/discovery.py`, `mira_comm/provisioning/`, `mira_comm/cli/`

**Parallel Agents**:
- Agent A: provisioning scripts
- Agent B: cloud API device endpoint + tests

**Depends on**: 1b, 1j, 4a

---

### Subphase 6b: Fleet Configuration and Observability [M]

**Goal**: Fleet config push, health aggregation, observability dashboard data API.

**Files to Create**:
- `infra/fleet/config_push.py`, `infra/fleet/health_aggregator.py`
- `cloud/api/routes/fleet.py`, `cloud/api/routes/dashboard.py`
- `infra/observability/dashboard.py`
- `tests/unit/infra/test_fleet.py`

**Reuse**: `mira_comm/ssh/client.py`, `mirror-api/app/api/analytics.py`

**Parallel Agents**:
- Agent A: fleet/ (config_push, health_aggregator)
- Agent B: observability + API routes + tests

**Depends on**: 6a, 1k

---

### Subphase 6c: Support Runbook and Onboarding [S]

**Goal**: Operational documentation for pilot support.

**Files to Create**:
- `docs/operations/support-runbook.md`
- `docs/operations/pilot-onboarding-checklist.md`
- `docs/operations/incident-response.md`
- `docs/operations/deployment-guide.md`
- `docs/operations/troubleshooting.md`

**Parallel Agents**:
- Agent A: support-runbook + troubleshooting
- Agent B: onboarding + incident-response + deployment-guide

**Depends on**: 6a, 6b

---

## Phase 7: v1 Pilot Launch

### Subphase 7a: Pilot Participant Framework [S]

**Goal**: Participant criteria, measurement plan, data collection protocol, consent form templates.

**Files to Create**:
- `docs/pilot/participant-criteria.md`, `docs/pilot/measurement-plan.md`
- `docs/pilot/data-collection-protocol.md`, `docs/pilot/consent-forms/`

**Depends on**: 5a

---

### Subphase 7b: Training Materials and Bug Triage [S]

**Goal**: Caregiver/operator training, bug triage workflow, issue templates.

**Files to Create**:
- `docs/pilot/caregiver-training.md`, `docs/pilot/operator-training.md`
- `docs/pilot/bug-triage-workflow.md`, `docs/pilot/issue-categories.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/safety_concern.md`, `.github/ISSUE_TEMPLATE/privacy_issue.md`

**Parallel Agents**:
- Agent A: training materials
- Agent B: triage workflow + issue templates

**Depends on**: 6c

---

### Subphase 7c: Deployment Hardening and Smoke Tests [M]

**Goal**: Docker containers, secure defaults, e2e smoke tests, pilot review cadence.

**Files to Create**:
- `Dockerfile` -- cloud API container
- `docker-compose.yml` -- cloud services (API, PostgreSQL, Qdrant)
- `tests/smoke/test_pilot_smoke.py`
- `scripts/deploy-cloud.sh`
- `docs/pilot/review-cadence.md`

**Reuse**: `Dockerfile` (multi-stage build), `docker-compose.yml` (service composition) from Mira

**Parallel Agents**:
- Agent A: Docker files + deploy script
- Agent B: smoke tests + review cadence

**Depends on**: All Phase 1-6 components

---

## Phase 8: v2 Shared Intelligence Foundation

### Subphase 8a: De-identification Pipeline [M]

**Goal**: Remove direct identifiers, generalize device labels, coarsen timestamps, validate for residual identifiers. 7-step pipeline from PRD-13.

**Files to Create**:
- `cloud/rag/deidentify.py`, `cloud/rag/models.py`, `cloud/rag/validators.py`
- `tests/unit/cloud/test_deidentify.py`

**Parallel Agents**:
- Agent A: deidentify.py + validators.py
- Agent B: models.py + tests

**Depends on**: 5a

---

### Subphase 8b: Vector Store and Assistive Priors [M]

**Goal**: Qdrant vector store for de-identified assistive priors with condition-scoped retrieval.

**Files to Create**:
- `cloud/rag/vector_store.py` -- Qdrant client wrapper
- `cloud/rag/retrieval.py` -- condition-scoped, locale-filtered retrieval
- `cloud/rag/ingestion.py` -- contribution ingestion
- `cloud/rag/constants.py`
- `cloud/priors/seeding.py` -- new-user seeding with low-confidence priors
- `tests/unit/cloud/test_vector_store.py`, `tests/unit/cloud/test_retrieval.py`, `tests/unit/cloud/test_seeding.py`

**Parallel Agents**:
- Agent A: vector_store.py + retrieval.py + constants.py
- Agent B: ingestion.py + seeding.py
- Agent C: tests

**Depends on**: 8a

---

### Subphase 8c: Evaluation Harness and Rollback [M]

**Goal**: Evaluate shared priors impact on intent resolution. Rollback mechanism for bad updates.

**Files to Create**:
- `cloud/rag/evaluation.py`, `cloud/rag/rollback.py`
- `cloud/api/routes/community.py` -- opt-in category management
- `tests/unit/cloud/test_evaluation.py`, `tests/unit/cloud/test_rollback.py`
- `tests/integration/test_rag_pipeline.py`

**Parallel Agents**:
- Agent A: evaluation.py + rollback.py
- Agent B: API routes + tests

**Depends on**: 8b

---

## Phase 9: Research Workflow and Governance

### Subphase 9a: Research Participation and Data Access [M]

**Goal**: Researcher request/approval flow, data use agreements, purpose limitation, access controls.

**Files to Create**:
- `cloud/research/participation.py`, `cloud/research/access.py`, `cloud/research/models.py`
- `cloud/api/routes/research.py`
- `tests/unit/cloud/test_research_participation.py`, `tests/unit/cloud/test_research_access.py`

**Parallel Agents**:
- Agent A: participation.py + access.py + models.py
- Agent B: API routes + tests

**Depends on**: 5a, 8a

---

### Subphase 9b: Dataset Governance and Publication Safeguards [M]

**Goal**: Dataset lineage, provenance, release review, re-identification risk assessment, governed export.

**Files to Create**:
- `cloud/research/lineage.py`, `cloud/research/review.py`, `cloud/research/reidentification.py`
- `infra/research/export.py`
- `docs/research/release-review-checklist.md`, `docs/research/data-governance-policy.md`
- `tests/unit/cloud/test_lineage.py`, `tests/unit/cloud/test_review.py`

**Parallel Agents**:
- Agent A: lineage.py + review.py + reidentification.py
- Agent B: export.py + docs + tests

**Depends on**: 9a, 8a

---

## Cross-Cutting: Phase Transition Checklist

At the end of each phase:
1. Update `CLAUDE.md` phase status table
2. Update `README.md` project status
3. Update `docs/roadmap.md` phase completion
4. Update `.claude/hooks/_phase_config.py` ACTIVE_PHASE
5. Run `/phase-complete`
6. Run `/quality`
7. All CI checks pass

---

## Summary

| Phase | Subphases | Complexity |
|-------|-----------|------------|
| 0 | 0a, 0b, 0c | S + S + S |
| 1 | 1a-1k (11) | S + M + M + L + M + M + M + L + M + S + S |
| 2 | 2a-2d (4) | M + M + M + S |
| 3 | 3a-3c (3) | M + M + M |
| 4 | 4a-4e (5) | M + M + M + L + M |
| 5 | 5a-5d (4) | M + M + M + S |
| 6 | 6a-6c (3) | M + M + S |
| 7 | 7a-7c (3) | S + S + M |
| 8 | 8a-8c (3) | M + M + M |
| 9 | 9a-9b (2) | M + M |
| **Total** | **41 subphases** | |

## Critical File References

| Purpose | Path |
|---------|------|
| Phase scope enforcement | `.claude/hooks/_phase_config.py` |
| STT reuse source | `D:\GitHub\Mira\voice-pipeline\voice_pipeline\cloud_stt.py` |
| LLM reuse source | `D:\GitHub\Mira\voice-pipeline\voice_pipeline\cloud_llm.py` |
| TTS reuse source | `D:\GitHub\Mira\voice-pipeline\voice_pipeline\cloud_tts.py` |
| Orchestrator reuse | `D:\GitHub\Mira\voice-pipeline\voice_pipeline\orchestrator.py` |
| Encryption reuse | `D:\GitHub\Mira\mirror-api\app\core\encryption.py` |
| Config loader reuse | `D:\GitHub\Mira\mira_comm\config\loader.py` |
| SSH/provisioning reuse | `D:\GitHub\Mira\mira_comm\ssh\client.py` |
| Docker reuse | `D:\GitHub\Mira\Dockerfile` |
