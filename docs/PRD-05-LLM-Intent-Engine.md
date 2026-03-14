# PRD-05 · Intent Engine & Action Safety

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Transform transcript, context, and assistive memory into:
- likely intent;
- action parameters;
- user-facing response;
- caregiver-safe paraphrase;
- confidence and policy flags.

## 2. Inputs
- transcript;
- speech confidence;
- recent interaction turns;
- user profile memory;
- routine state;
- assistive priors from retrieval where allowed;
- device capability inventory.

## 3. Outputs
- action class;
- structured arguments;
- confirmation phrasing;
- caregiver paraphrase;
- clarification request where needed;
- confidence / safety band.

## 4. Risk Tiers

| Tier | Example | Behaviour |
|---|---|---|
| 0 | conversational reply, repeat phrase | execute freely |
| 1 | lights, music, TV volume | execute if high confidence |
| 2 | routine changes, outbound caregiver message | require confirmation or trusted rule |
| 3 | purchases, door locks, financial tasks, medication instructions | blocked in v1 and v2 unless separately governed |

## 5. Hard Constraints
The model output must never directly execute:
- purchases;
- unlocking external doors;
- medication dosing advice;
- legal or financial commitments;
- emergency-service contact;
- clinical judgments.

## 6. Clarification Rules
Clarification prompts must be:
- short;
- not patronizing;
- choice-based when possible;
- deterministic for autistic users in strict mode.

## 7. Personalization Rules
The engine may personalize:
- phrasing style;
- confirmation brevity;
- preferred device names;
- routine suggestions.

It may not:
- simulate therapy;
- invent memories;
- fabricate caregiver communications;
- present inferred facts as confirmed facts.

## 8. Evaluation
Key eval sets must include:
- aphasia substitutions;
- autistic scripted phrases;
- sensory-overload triggers;
- dementia repetition cases;
- caregiver message routing;
- harmful or disallowed intent attempts.
