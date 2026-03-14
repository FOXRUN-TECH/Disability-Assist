# PRD-13 · Cloud RAG & Cross-User Assistive Learning

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Use cloud retrieval and de-identified cross-user learning to improve intent resolution for future users while protecting privacy and preserving user control.

## 2. What This System Should Share

The project may share, when opted in and properly de-identified:
- vocabulary mappings;
- action-success patterns;
- routine templates;
- sensory-safe preference archetypes;
- accessibility-related phrasing priors;
- condition-scoped assistive strategies.

The project should not frame this as sharing “personalities.”

## 3. Retrieval Model
RAG should combine:
- user-local memory;
- cloud assistive priors;
- condition-scoped namespaces;
- device and environment metadata stripped of personal identifiers.

## 4. Vector / Search Stack
Preferred stack:
- Qdrant or equivalent open, scalable vector store;
- PostgreSQL for control metadata;
- object storage for governed datasets.

Selection criteria:
- predictable cost;
- no hard vendor lock-in;
- scalability to high volume;
- support for filtered retrieval by condition, locale, and modality.

## 5. Contribution Pipeline
1. local interaction record created;
2. direct identifiers removed;
3. device-specific labels generalized;
4. timestamps coarsened where possible;
5. payload validated for obvious residual identifiers;
6. payload encrypted in transit;
7. consent status checked before ingestion.

## 6. Opt-In Categories
- interaction pattern contribution;
- routine template contribution;
- researcher program contribution.

These must be separately selectable and revocable.

## 7. Cross-User Seeding Rules
v2 may seed new users with low-confidence assistive priors based on:
- condition tags;
- communication profile;
- sensory profile;
- selected environment type.

Seeded priors must:
- start low confidence;
- be local-user overridable;
- never override confirmed user-specific mappings.

## 8. Scale Targets
The architecture should be viable from:
- pilot: 10–20 units;
- early community: 1,000 users;
- growth: 100,000 users;
- large-scale public service: 1,000,000+ users.

## 9. Cost Model
Early cloud estimate for a cloud-first active user:
- approximately CAD 8–15 per user per month depending on usage and provider pricing.

Pilot estimate:
- 10 units: roughly CAD 80–300 per month;
- 20 units: roughly CAD 160–600 per month.

These are planning estimates, not promises.

## 10. Research Program Constraints
Research data access must be:
- de-identified by default;
- governed by agreement and review;
- free or cost-recovery aligned with the project mission.
