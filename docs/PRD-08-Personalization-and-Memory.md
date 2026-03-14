# PRD-08 · Personalization & User Memory

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Store the minimum user-specific information required to make future interactions easier, faster, and more predictable.

## 2. Memory Categories
- profile and accessibility settings;
- vocabulary mappings;
- device aliases;
- media preferences;
- routines;
- recent interaction history;
- caregiver-approved notes;
- privacy and consent preferences.

## 3. Storage Model
| Data Type | Default Location | Cloud Sync |
|---|---|---|
| accessibility settings | local + cloud if enabled | optional |
| vocabulary map | local | optional |
| routines | local | optional |
| recent history | local, bounded retention | optional metadata only |
| consent status | cloud canonical + local cache | required for cloud features |
| assistive priors imported from cloud | local cached | yes |

## 4. User Control
Where user capacity permits, the user can:
- inspect learned mappings;
- delete entries;
- disable learning categories;
- lock selected entries from caregiver editing.

Where a guardian or lawful representative controls settings, this must be recorded in role metadata.

## 5. Retention
- recent history default 30 days, configurable downward;
- profile and preferences retained until deletion;
- no routine raw-audio archive;
- export and wipe functions required.

## 6. Guardrails
The system must not build a theatrical “personality” profile. It may build:
- communication preferences;
- response-style preferences;
- routine patterns;
- accessibility patterns.

## 7. Cloud Statement
Disability-Assist does operate cloud services for v1 features. This PRD replaces any earlier assumption that all sync is user-owned-only storage.
