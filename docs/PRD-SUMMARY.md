# PRD Summary

## Purpose of this document

This document summarizes the replacement PRD suite for Disability-Assist so contributors, reviewers, and pilot stakeholders can understand the project quickly before reading the full set.

## Executive summary

Disability-Assist is a cloud-first assistive communication and environmental-control system for people who are not well served by conventional voice assistants. It is designed for users whose speech may be incomplete, substituted, slowed, inconsistent, low-volume, sensory-sensitive, or shaped by developmental, cognitive, or age-related barriers.

The project is structured as a pilot-first system intended for small deployments in private homes and assisted-home settings. The first release includes cloud speech recognition, cloud language understanding, cloud speech synthesis, caregiver mobile support, smart-home control, personalization, role-based access, consent management, and optional de-identified contribution pathways.

The project is open source and public-benefit oriented, but it is not written around unrealistic assumptions such as universal free operation, zero-governance researcher access, or informal caregiver visibility without controls.

## What changed from the earlier draft direction

The replacement PRD set corrects several structural problems that typically weaken early assistive AI projects:
- it removes contradictory assumptions about whether cloud services exist;
- it places the caregiver app in v1 rather than treating it as optional later scope;
- it makes cloud speech and language services explicit because local-only quality is not sufficient for the intended users;
- it distinguishes personalization from “personality transfer” language;
- it treats assisted-home deployment as a first-class operating model;
- it separates consent lanes rather than pretending one initial opt-in solves everything;
- it treats research access as governed, de-identified, and conditional rather than casually open.

## Product scope at a glance

### Included in v1
- cloud STT, LLM, and TTS;
- device-side routing and safe execution of supported actions;
- smart-home and media control through constrained integration paths;
- caregiver mobile app;
- user memory and assistive profile handling;
- consent management by data lane;
- role-based access and auditability;
- private-home and assisted-home deployment modes;
- de-identified community-learning opt-in;
- research-program opt-in and governance hooks.

### Included in v2
- cross-user assistive pattern seeding;
- stronger retrieval and shared priors;
- advanced routines and templates;
- facility fleet tooling;
- structured researcher workflows;
- stronger analytics, governance, and update controls.

### Explicit non-goals
- diagnosis;
- treatment claims;
- clinical monitoring;
- emergency-response autonomy;
- unrestricted institutional surveillance;
- unsupported legal-compliance claims.

## User groups covered by the PRDs

The PRDs cover these user groups:
- elderly users with communication or hearing barriers;
- users with developmental disabilities;
- autistic users, including users with prior Asperger’s diagnoses;
- users with cognitive impairment or fluctuating communication ability;
- family caregivers;
- support workers and assisted-home staff;
- community operators and pilot administrators;
- researchers working with governed, de-identified data.

## Architecture summary

The architecture is deliberately split into cloud and local responsibilities.

### Cloud responsibilities
- speech-to-text;
- large-language intent inference;
- text-to-speech;
- retrieval augmentation and shared priors;
- caregiver app connectivity;
- consent and governance services;
- optional de-identified contribution workflows.

### Local responsibilities
- audio capture and buffering;
- wake, session, and local device control logic;
- constrained action routing;
- device cache and local profile support;
- degraded fallback behaviour when cloud is impaired.

The design is not local-first for speech and language quality. It is local-first only where local control, resilience, and privacy boundaries benefit from it.

## Privacy and governance summary

The PRDs assume that the project will handle sensitive personal data and therefore require stronger controls than a normal hobby voice assistant.

The replacement suite introduces a lane-based governance model:
- core operating data;
- personalization data;
- community-learning data;
- research data.

Each lane has separate consent expectations, separate access rules, and separate retention implications.

The PRDs also require:
- role-based access;
- minimum necessary disclosure;
- revocable participation;
- deletion workflows;
- audit logging;
- stricter assisted-home defaults;
- governed research participation.

## Cost posture

The PRDs assume a pilot reality rather than a mass-consumer fantasy. Cloud services, mobile connectivity, storage, logging, and governance functions all introduce real costs. The system is therefore written for public-benefit and cost-recovery operation, not for unsustainable free hosting promises.

## Why the PRD suite is structured this way

The main design choice is simple: real-world assistive usefulness matters more than ideological purity. If cloud speech and cloud language services are the only way to deliver acceptable understanding for the target users in v1, the PRDs must say so clearly. Everything else in the suite flows from that decision.

## Recommended reading order

1. `PRD-01-Overview-and-Vision.md`
2. `PRD-02-User-Personas-and-Journeys.md`
3. `PRD-03-System-Architecture.md`
4. `PRD-11-Privacy-Security-and-Ethics.md`
5. `PRD-14-Caregiver-Mobile-App.md`
6. `PRD-13-Cloud-RAG-and-Cross-User-Learning.md`
7. remaining PRDs in sequence

## Bottom line

This PRD set is written to support a serious assistive pilot, not a vague accessibility concept. It is more constrained, more honest, more governable, and more buildable than the earlier direction.
