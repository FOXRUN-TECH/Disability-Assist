# Roadmap

## Purpose

This roadmap translates the PRD suite into an implementation sequence suitable for a 10–20 unit pilot deployment in private homes and assisted-home settings.

The goal is not to build every possible feature at once. The goal is to build a pilot that works, can be governed, and can be expanded without rewriting the foundations.

## Delivery philosophy

The implementation order is driven by four constraints:
- cloud-first accuracy is required in v1;
- privacy and consent controls must exist before scale;
- caregiver visibility is core product scope, not a later add-on;
- assisted-home deployment introduces role, audit, and dignity requirements from day one.

## Phase 0 — Repo foundation and governance baseline ✅ COMPLETE

### Objectives
- establish the repo structure and documentation baseline;
- convert the PRD suite into implementation workstreams;
- define naming, data classification, and decision records;
- create initial threat model, consent model, and role model.

### Deliverables
- project README aligned with PRDs;
- architecture decision records template;
- threat model document;
- data classification matrix;
- consent lane matrix;
- user role matrix for home and assisted-home modes;
- issue and milestone taxonomy.

### Exit criteria
- every major feature in the PRDs maps to a tracked workstream;
- governance assumptions are documented before code starts spreading.

## Phase 1 — Core cloud speech and device loop

### Objectives
- establish the end-to-end interaction loop from microphone input to cloud processing to local action routing;
- prove that real target-user speech can be captured, transcribed, interpreted, and responded to reliably enough for pilot use.

### Deliverables
- audio capture pipeline;
- session handling and buffering;
- cloud STT integration;
- cloud LLM integration for intent inference;
- cloud TTS integration;
- local action router;
- structured response object for action, clarification, and caregiver bridge flows;
- latency and failure instrumentation.

### Exit criteria
- target-user interactions succeed at a baseline acceptable rate in scripted tests;
- the system fails safely when cloud services are slow or unavailable;
- supported smart actions are executed only through constrained paths.

## Phase 2 — Smart-home and media control

### Objectives
- make the device actually useful in daily life by supporting clear, bounded actions.

### Deliverables
- Home Assistant integration as primary control layer;
- music, TV, lighting, and simple routine triggers;
- confirmation policy for medium-risk actions;
- action audit log;
- supported-device compatibility matrix.

### Exit criteria
- supported commands execute reliably;
- unsupported commands degrade gracefully;
- high-risk or ambiguous commands do not execute without policy checks.

## Phase 3 — Personalization and assistive profile

### Objectives
- let the system improve per user without turning into an opaque black box.

### Deliverables
- local assistive profile store;
- vocabulary mapping and phrase normalization;
- routine and preference memory;
- hearing and voice-output tuning controls;
- caregiver-visible but role-limited profile administration;
- profile reset and export mechanisms.

### Exit criteria
- personalization improves command resolution measurably;
- user or authorized caregiver can review and change profile settings;
- profile data is separated from research and community-learning data.

## Phase 4 — Caregiver app and role-based access

### Objectives
- provide useful caregiver visibility without defaulting to invasive surveillance.

### Deliverables
- caregiver mobile app foundation;
- authentication and device pairing;
- home mode and assisted-home mode role sets;
- minimum-necessary event feed;
- clarification support UI;
- audit view for remote access events;
- transcript exposure controls with strict defaults.

### Exit criteria
- caregiver access is usable and logged;
- staff visibility differs correctly from family visibility where required;
- raw content exposure is restricted, not casual.

## Phase 5 — Consent, retention, and deletion controls

### Objectives
- make governance real inside the product rather than only in documentation.

### Deliverables
- lane-based consent flows;
- guardian and substitute-decision-maker flows;
- consent versioning and timestamps;
- retention scheduler;
- deletion request workflow;
- participation toggles for personalization sync, community learning, and research.

### Exit criteria
- every major data use has a product-level control path;
- consent revocation changes future processing behaviour correctly;
- deletion requests are trackable and auditable.

## Phase 6 — Pilot operations package

### Objectives
- make the system deployable across 10–20 real units.

### Deliverables
- deployment scripts and provisioning flow;
- device registration;
- fleet configuration basics;
- observability dashboard;
- support runbook;
- pilot onboarding checklist for home and assisted-home settings;
- incident response and escalation process.

### Exit criteria
- new units can be provisioned consistently;
- operators can diagnose common failures;
- pilot support does not depend on tribal knowledge.

## Phase 7 — v1 pilot launch

### Objectives
- run the first real deployment with defined measurement and governance.

### Deliverables
- pilot participant criteria;
- baseline measurement plan;
- caregiver and operator training materials;
- bug triage workflow;
- issue categorization by safety, privacy, and usability severity;
- pilot review cadence.

### Exit criteria
- 10–20 units deployed;
- data is collected according to documented consent lanes;
- major safety, privacy, and usability issues are visible to the team quickly.

## Phase 8 — v2 shared intelligence foundation

### Objectives
- introduce shared assistive priors without crossing privacy or dignity boundaries.

### Deliverables
- de-identified community-learning ingestion pipeline;
- assistive pattern library;
- condition-scoped retrieval layers;
- cross-user seeding controls;
- evaluation harness for shared priors;
- rollback path for bad model or retrieval updates.

### Exit criteria
- v2 features improve intent resolution without copying personal identity or exposing sensitive user detail;
- contribution and non-contribution populations are both supported cleanly.

## Phase 9 — Research workflow and governance

### Objectives
- enable ethically governed research support without turning the production system into an uncontrolled data dump.

### Deliverables
- research participation workflow;
- de-identification pipeline;
- release review checklist;
- researcher request and approval flow;
- dataset lineage and provenance documentation;
- publication and misuse safeguards where appropriate.

### Exit criteria
- research outputs are governed;
- access is deliberate;
- the production system remains separated from ad hoc research demands.

## Cross-cutting requirements

These requirements apply to every phase:
- accessibility review;
- threat modeling updates;
- role and permission review;
- logging and observability;
- cost tracking;
- failure-mode testing;
- documentation updates.

## Suggested milestone structure

### Milestone A
Repo foundation, governance baseline, architecture skeleton.

### Milestone B
Cloud speech loop, device control loop, smart-home execution.

### Milestone C
Personalization, caregiver app, role-based access.

### Milestone D
Consent system, retention and deletion controls, pilot operations.

### Milestone E
v1 pilot deployment and measured review.

### Milestone F
v2 shared priors, researcher workflows, fleet improvements.

## What not to do early

Do not spend early cycles on:
- broad consumer-market polish;
- speculative multilingual expansion before pilot evidence;
- facility analytics dashboards before role boundaries are stable;
- research exports before de-identification and approval workflows exist;
- advanced autonomy beyond the documented action safety model.

## Final implementation rule

If a feature increases surveillance risk, ambiguity, or governance burden faster than it improves user dignity and communication success, it should be delayed or cut.
