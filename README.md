# Disability-Assist

Disability-Assist is an open-source, cloud-first assistive communication and environmental-control system intended to help people with speech, cognitive, sensory, developmental, and age-related communication barriers communicate more effectively and control parts of their environment with less frustration.

This repository is structured around a pilot-first approach for small deployments in private homes and assisted-home settings. The initial target is a 10–20 unit pilot that prioritizes real-world usability, dignity, caregiver coordination, and strong privacy boundaries over unnecessary feature sprawl.

## What the project does

Disability-Assist is intended to:
- interpret incomplete, degraded, non-standard, or substituted speech;
- infer likely intent using cloud speech, language, and retrieval systems;
- provide intelligible voice output tuned to user hearing and sensory preferences;
- help caregivers understand likely meaning when direct speech is difficult to interpret;
- control supported smart-home and media devices through a constrained action layer;
- learn user-specific routines, vocabulary, and preferences over time;
- optionally support de-identified community learning and research participation.

## What the project is not

This project is not positioned as:
- a diagnostic product;
- a treatment device;
- a clinical monitoring platform;
- an emergency response system;
- a substitute for trained medical or professional judgment.

Those boundaries are intentional. The system is designed as an assistive communication and accessibility platform, not as a clinical product.

## Delivery model

The project is:
- open source at the code and documentation level;
- intended for public-benefit, community, research, and pilot use;
- capable of cost-recovery hosted services where needed for cloud processing, caregiver connectivity, and governance functions.

The project is not written around a universal free-service assumption. Cloud speech, language, storage, and mobile access introduce real operating costs. The PRDs are written to support a sustainable pilot and a realistic long-term operating model.

## Version model

### v1 Pilot
v1 is the first fully scoped pilot release and includes:
- cloud-first STT, LLM, and TTS;
- local device action routing and fail-safe behaviour;
- caregiver mobile app;
- consent management;
- smart-home and media control;
- local personalization with optional cloud-linked services;
- role-based access controls;
- private-home and assisted-home deployment modes;
- de-identified community-learning and research opt-in pathways.

### v2 Shared Intelligence
v2 expands the pilot foundation with:
- cross-user assistive pattern seeding;
- stronger retrieval and condition-scoped priors;
- facility and fleet management capabilities;
- advanced routines and automation templates;
- researcher workflow tooling;
- stronger governance, analytics, and update controls.

## Guiding principles

- dignity first;
- cloud-first accuracy in v1;
- minimum necessary disclosure;
- predictable behaviour for sensory-sensitive users;
- separate consent lanes for separate uses;
- strong caregiver and facility role boundaries;
- no false claims;
- public documentation and open governance where practical.

## Repo reading order

Start here:
1. `docs/PRD-00-Index.md`
2. `docs/PRD-SUMMARY.md`
3. `docs/PRD-01-Overview-and-Vision.md`
4. `roadmap.md`

Then read the supporting PRDs in numerical order.

## Core documents

- `docs/PRD-00-Index.md` — package entry point
- `docs/PRD-SUMMARY.md` — executive summary of the full PRD suite
- `docs/PRD-01-Overview-and-Vision.md` — product framing, scope, and non-goals
- `docs/PRD-02-User-Personas-and-Journeys.md` — user groups and accessibility scenarios
- `docs/PRD-03-System-Architecture.md` — system design and deployment topology
- `docs/PRD-04-Voice-Input-and-STT.md` — cloud speech input path and controls
- `docs/PRD-05-LLM-Intent-Engine.md` — intent inference and action safety
- `docs/PRD-06-Adaptive-Voice-Output.md` — voice output tuning
- `docs/PRD-07-Smart-Home-Integration.md` — device and service integration
- `docs/PRD-08-Personalization-and-Memory.md` — user memory and assistive profile handling
- `docs/PRD-09-Caregiver-Communication-Bridge.md` — caregiver-facing interpretation support
- `docs/PRD-10-Hardware-Reference-Design.md` — pilot hardware guidance
- `docs/PRD-11-Privacy-Security-and-Ethics.md` — governance and privacy boundaries
- `docs/PRD-12-Open-Source-Contribution-Guide.md` — contribution posture and operating rules
- `docs/PRD-13-Cloud-RAG-and-Cross-User-Learning.md` — shared retrieval and assistive priors
- `docs/PRD-14-Caregiver-Mobile-App.md` — mobile app requirements
- `roadmap.md` — implementation roadmap by phase

## Recommended implementation posture

Build the project in this order:
- establish governance and consent flows first;
- stand up the cloud speech and intent path;
- build local action routing and smart-home control;
- add caregiver app and role-based access;
- add personalization and retrieval;
- add de-identified contribution workflows only after the core pilot is stable.

## Pilot success criteria

The pilot should prove five things:
- the system improves real-world understanding for target users;
- caregivers receive useful help without unacceptable surveillance;
- the cloud architecture is accurate enough to justify cost;
- deployment in home and assisted-home settings is operationally manageable;
- the project can scale governance before it scales user count.

## Contribution expectations

This project should not become a generic AI assistant repo. Contributions must support the documented assistive goals, privacy model, consent boundaries, safety rules, and deployment reality defined in the PRDs.
