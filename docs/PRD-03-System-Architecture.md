# PRD-03 · System Architecture

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Architecture Summary

v1 is explicitly cloud-first for:
- speech-to-text;
- large-language inference;
- text-to-speech.

The device remains local for:
- wake / trigger handling;
- utterance buffering;
- action routing;
- local cache and short-term memory;
- local control of supported devices;
- degraded-mode fallback for a narrow command subset.

## 2. High-Level Flow

```text
Mic Array
  -> Voice Activity Detection / Audio Front End
  -> Cloud STT
  -> Intent Engine (Cloud LLM + local policy layer + RAG context)
  -> Action Router
      -> Home Assistant / media / routine / caregiver channel
  -> Cloud TTS
  -> Local speaker / optional local display
  -> Caregiver mobile app / dashboard
```

## 3. Core Components

### 3.1 Device Runtime
- captures audio utterances;
- streams or uploads bounded clips to cloud STT;
- maintains local SQLite cache;
- executes local integrations;
- logs auditable device events.

### 3.2 Cloud Inference Layer
- STT endpoint;
- LLM endpoint;
- TTS endpoint;
- retrieval service;
- consent and account service;
- audit and policy service.

### 3.3 Policy & Safety Layer
Sits between model output and action execution.
It must:
- validate target device and action;
- enforce risk tier rules;
- block unsupported or high-risk actions;
- require confirmation where needed;
- produce caregiver-safe paraphrases.

### 3.4 Data Stores
| Store | Purpose |
|---|---|
| Local SQLite | user profile cache, routine cache, recent history, local mappings |
| PostgreSQL | accounts, consent records, role assignments, audit metadata |
| Vector store | de-identified retrieval corpus and assistive priors |
| Object storage | exports, model-eval artifacts, controlled research datasets |

## 4. Deployment Modes

### v1 Supported Modes
| Mode | Status | Notes |
|---|---|---|
| Cloud-first | Required | primary supported mode |
| Degraded local command fallback | Limited | only a narrow allow-list |
| Full local conversational parity | Not supported in v1 | explicitly out of scope |

## 5. Integration Model

Home Assistant is the primary abstraction layer for smart-home control.
Direct integrations are allowed only when:
- Home Assistant coverage is inadequate;
- the action is high-value;
- maintenance burden is justified.

## 6. Failure Handling

If cloud inference is unavailable:
- the system enters degraded mode;
- only allow-listed local actions are available;
- the user receives a plain-language explanation;
- caregiver app shows degraded-state status.

## 7. Observability

Required telemetry categories:
- device health;
- cloud round-trip timing;
- intent resolution outcomes;
- policy blocks;
- consent changes;
- caregiver access events.

Telemetry containing personal content must follow PRD-11.

## 8. Non-Functional Targets
- median cloud-connected response <= 3.5s;
- device boot to ready <= 90s;
- command execution success >= 95% on supported actions;
- local degraded-mode response <= 1.5s for allow-listed commands.
