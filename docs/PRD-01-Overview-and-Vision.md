# PRD-01 · Project Overview & Vision

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Date:** 2026-03-13  
**Status:** Replacement Draft

## 1. Purpose

Disability-Assist is an open-source assistive communication and environmental-control system for people with speech, cognitive, sensory, developmental, and age-related communication barriers.

The system is intended for:
- private homes;
- assisted-living and supportive-housing environments;
- small pilot deployments of approximately 10–20 units in community settings.

The product goal is straightforward: help the user communicate intent more clearly, help caregivers understand the user more reliably, and help the user control their environment with less frustration and more dignity.

## 2. Product Positioning

Disability-Assist is:
- a public-benefit, open-source project;
- intended for non-commercial community use, pilot programs, cost-recovery hosting, and research collaboration;
- cloud-first in v1 for speech recognition, language understanding, and speech output;
- local-first for device control, user profile cache, and fail-safe behaviour.

Disability-Assist is **not** positioned in v1 or v2 as:
- a diagnostic device;
- a treatment device;
- a clinical monitoring platform;
- an emergency response system;
- a substitute for professional medical judgment.

## 3. Problem Statement

Many existing voice assistants fail users who:
- speak quietly, slowly, inconsistently, or with non-standard phrasing;
- substitute words, pause mid-sentence, or lose words during speech;
- rely on routines, scripted phrases, or AAC-adjacent communication styles;
- need predictable responses and minimal sensory load;
- need a caregiver, family member, or support worker to understand inferred intent.

These failures are not edge cases for this project. They are the core use case.

## 4. Vision

> A system that understands intent under real-world disability conditions and helps other people understand that intent too.

The system shall:
1. accept incomplete, approximate, degraded, or non-standard speech;
2. infer likely intent using cloud speech, language, and retrieval services;
3. produce intelligible output tuned to the user’s hearing and sensory needs;
4. control smart-home and media systems through a constrained action layer;
5. provide caregiver visibility without defaulting to invasive surveillance;
6. learn user-specific preferences, routines, and vocabulary over time;
7. optionally contribute de-identified pattern data to improve future performance for similar users.

## 5. Deployment Scope

### 5.1 v1 Pilot Scope
Included in v1:
- cloud STT, LLM, and TTS;
- local device action routing;
- caregiver mobile app;
- consent management;
- smart-home and media control;
- user profile memory;
- de-identified community-learning opt-ins;
- researcher opt-in pathway;
- private-home and assisted-home deployment modes;
- audit logging and role-based access controls.

### 5.2 v2 Scope
Included in v2:
- cross-user assistive pattern seeding;
- condition-scoped retrieval improvements;
- facility fleet tools;
- researcher portal workflows;
- advanced routines and automation templates;
- multilingual expansion planning;
- stronger analytics and governance tooling.

## 6. Core Principles

- **Dignity first** — the system must not infantilize, patronize, or dehumanize the user.
- **Cloud-first accuracy** — v1 prioritizes actual performance over ideological local-only purity.
- **Consent by lane** — core operation, caregiver access, cloud sync, community learning, and research access are distinct decisions.
- **Minimum necessary disclosure** — caregivers and staff should see what they need, not everything available.
- **Predictable behaviour** — especially for autistic and sensory-sensitive users.
- **Open implementation** — source code, prompts, and governance documents are public unless doing so would create security exposure.
- **No false claims** — the project must not claim universal legal compliance or medical status it does not have.

## 7. Target Users

| User Group | Description |
|---|---|
| Primary users | People with speech, cognitive, sensory, developmental, or age-related communication barriers |
| Secondary users | Family caregivers, support workers, assisted-home staff |
| Tertiary users | Researchers, open-source contributors, accessibility advocates |
| Operators | Small pilot administrators and community organizations |

## 8. Explicit Non-Goals

The system will not in v1 or v2:
- diagnose disease or disability;
- provide clinical cognitive scoring;
- claim treatment efficacy;
- autonomously call emergency services;
- expose full raw interaction content by default to staff or institutions;
- claim to be compliant with all national and international laws.

## 9. Success Metrics

| Metric | v1 Target |
|---|---|
| Successful intent resolution for target users | >= 85% in pilot scenarios |
| Caregiver-reported comprehension improvement | >= 30% over unaided baseline |
| Smart-home action success rate | >= 95% for supported integrations |
| Median end-to-end response time | <= 3.5 seconds cloud-connected |
| Setup time for private home | <= 45 minutes |
| Setup time for assisted-home resident | <= 60 minutes |
| Consent revocation action completion | <= 60 seconds to queue; deletion SLA documented separately |

## 10. PRD Map

This document is the entry point to the replacement PRD set:
- PRD-02 Personas
- PRD-03 System Architecture
- PRD-04 Voice Input & Cloud STT
- PRD-05 Intent Engine & Action Safety
- PRD-06 Adaptive Voice Output
- PRD-07 Smart-Home Integration
- PRD-08 Personalization & Memory
- PRD-09 Caregiver Communication Bridge
- PRD-10 Hardware Reference Design
- PRD-11 Privacy, Security & Governance
- PRD-12 Open Source Contribution Guide
- PRD-13 Cloud RAG & Cross-User Learning
- PRD-14 Caregiver Mobile App
