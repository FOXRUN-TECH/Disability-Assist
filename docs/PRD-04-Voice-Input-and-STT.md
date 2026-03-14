# PRD-04 · Voice Input & Cloud STT

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Speech recognition shall prioritize real-world usability for degraded, quiet, approximate, and non-standard speech. v1 uses a managed cloud speech provider as the primary recognition path.

## 2. Requirements

### 2.1 Supported Conditions
The speech pipeline must tolerate:
- aphasic substitution;
- dysarthric slurring;
- hypophonia / very low volume speech;
- long pauses;
- incomplete phrases;
- echolalia and scripted phrases;
- repeated phrases;
- caregiver background speech contamination.

### 2.2 Input Controls
- max utterance duration configurable, default 30s;
- silence timeout adaptive by user profile;
- gain control and denoise enabled by default;
- speaker suppression / echo management required where feasible.

## 3. Cloud-First Recognition

The system shall:
- send bounded utterances over encrypted transport to cloud STT;
- receive transcript + confidence + metadata where available;
- pass low-confidence results to the intent layer rather than hard-failing too early.

## 4. Low-Confidence Strategy
If transcript confidence is low but non-trivial:
- include recent turns;
- include user preference memory;
- include routine context;
- set a low-confidence flag for the intent engine.

Hard failure should be reserved for near-garbage audio.

## 5. Audio Retention Policy

Default policy:
- audio is processed for current inference only;
- no routine long-term audio storage;
- no always-on archival recording.

Optional future research audio contribution, if ever implemented, must be:
- separate from core consent;
- off by default;
- explicitly versioned;
- separately governed under PRD-11 and PRD-13.

## 6. Accessibility-Specific Behaviours
- whisper acceptance for sensory or low-volume users;
- longer pause tolerance for word-finding difficulty;
- repeated-request de-duplication;
- phrase-level custom vocabulary boosts where provider supports them.

## 7. Testing
| Test | Pass Criterion |
|---|---|
| low-volume recognition | >= 80% task success in controlled pilot set |
| aphasic substitution recovery | >= 75% intent success with memory help |
| pause tolerance | user can pause mid-request without immediate timeout |
| repeated request handling | duplicate execution prevented |
| background speech interference | protected from obvious caregiver takeover in single-user mode |
