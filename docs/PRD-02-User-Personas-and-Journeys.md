# PRD-02 · User Personas & Journey Maps

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Date:** 2026-03-13  
**Status:** Replacement Draft

## 1. Persona Design Rules

Personas in this project are operational tools, not marketing copy. They exist to drive:
- speech tolerance requirements;
- voice output configuration;
- response-style constraints;
- caregiver permissions;
- privacy defaults;
- memory and retrieval design.

## 2. Primary Personas

### Persona A — Margaret, 78 · Post-Stroke Aphasia
| Attribute | Detail |
|---|---|
| Speech profile | word substitution, halting phrases, mid-sentence loss |
| Hearing | mild high-frequency loss |
| Living situation | private home with spouse |
| Key need | infer likely intent despite incorrect word choice |
| Key risk | frustration when misunderstood repeatedly |

**Derived requirements**
- tolerate substitution phrases;
- use recent context and preference memory;
- default to short confirmation phrases;
- show inferred meaning to caregiver separately from raw text.

### Persona B — Walter, 84 · Dementia / Cognitive Decline
| Attribute | Detail |
|---|---|
| Speech profile | repetition, topic drift, incomplete sentences |
| Hearing | moderate bilateral loss |
| Living situation | assisted living |
| Key need | comfort requests, routine support, simple responses |
| Key risk | staff overexposure to sensitive content |

**Derived requirements**
- repeat-safe intent handling;
- routine-aware suggestions;
- professional-caregiver minimum-necessary view;
- stricter facility audit controls.

### Persona C — Diane, 67 · Parkinsonian Hypophonia
| Attribute | Detail |
|---|---|
| Speech profile | quiet, breathy, low-energy speech |
| Hearing | near normal |
| Living situation | private home |
| Key need | recognition without shouting |
| Key risk | false negatives from low-volume speech |

**Derived requirements**
- aggressive front-end gain control;
- low-volume speech acceptance;
- avoid repeated retry prompts;
- warm, non-robotic TTS.

### Persona D — Noah, 34 · Autistic Adult, Minimally Verbal
| Attribute | Detail |
|---|---|
| Speech profile | short phrases, echolalia, scripted speech |
| Sensory profile | sensitive to unpredictable audio |
| Living situation | family home / day program |
| Key need | predictable responses and phrase mapping |
| Key risk | distress from surprise output or noisy UI |

**Derived requirements**
- strong phrase-to-intent memory;
- strict response consistency;
- optional text-only mode;
- quiet mode and sensory-overload mode;
- no jokes or improvisational personality behaviour.

### Persona E — Claire, 19 · Autistic Adult, Former Asperger’s Diagnosis
| Attribute | Detail |
|---|---|
| Speech profile | verbal, precise when regulated; reduced coherence under overload |
| Sensory profile | sound, brightness, and pacing sensitivity |
| Living situation | family home / supported education |
| Key need | low-sensory, high-predictability interaction |
| Key risk | overwhelm caused by verbose or inconsistent responses |

**Derived requirements**
- concise responses;
- user-selectable text-first output;
- instant sensory overload routine;
- user control over caregiver visibility where capacity allows.

### Persona F — Samir, 41 · Acquired Speech Difficulty + Full Cognitive Capacity
| Attribute | Detail |
|---|---|
| Speech profile | dysarthric but intentional |
| Hearing | normal |
| Living situation | independent apartment with periodic caregiver visits |
| Key need | preserve autonomy and privacy |
| Key risk | caregiver overreach |

**Derived requirements**
- allow user-controlled locks on sensitive memory items;
- distinguish assistance from supervision;
- default raw transcript access off.

## 3. Secondary Personas

### Persona G — Family Caregiver
Needs fast understanding, simple controls, and confidence that the system is helping rather than spying.

### Persona H — Professional Support Worker
Needs short actionable summaries, shift-safe access controls, and logged access.

### Persona I — Pilot Administrator
Needs fleet health, consent status, update status, and incident workflows without blanket content access.

## 4. Journey Requirements

### Journey 1 — Basic Home Request
1. User speaks approximate request.
2. System sends utterance to cloud speech service.
3. Intent engine combines transcript, recent context, and memory.
4. Action executes or asks constrained clarification.
5. User receives intelligible confirmation.
6. Caregiver view receives concise paraphrase if enabled.

### Journey 2 — Communication Bridge in Assisted Home
1. User says unclear phrase.
2. System infers likely meaning with confidence band.
3. Care staff view shows “Likely request” and confidence.
4. Raw wording remains hidden by default.
5. Staff can acknowledge resolution.

### Journey 3 — Sensory Overload Support
1. User whispers or types trigger phrase.
2. System dims output, mutes TTS, simplifies UI.
3. Caregiver receives only an overload-safe status if permitted.
4. Recovery phrase exits mode.

### Journey 4 — New User Seeding
1. User or caregiver selects condition tags and preferences.
2. System optionally loads de-identified assistive priors for similar users.
3. All seeded mappings start low-confidence.
4. Confirmed local usage promotes them to user-specific memory.

## 5. Derived Accessibility Requirements

- voice-first operation with no touchscreen dependency;
- text-only response mode;
- configurable pitch, rate, accent, loudness, and EQ;
- deterministic phrasing mode for autistic users;
- no unexpected tones, chimes, or flourish audio;
- large-text caregiver and local display mode;
- multi-role privacy model;
- support for AAC-adjacent workflows rather than replacing AAC tools.
