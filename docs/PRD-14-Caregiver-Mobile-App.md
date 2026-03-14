# PRD-14 · Caregiver Mobile App

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Provide caregivers and approved staff with timely visibility, configuration controls, and consent management without making the app a blanket surveillance portal.

## 2. v1 In-Scope Features
- live interaction feed;
- likely-intent display;
- routine management;
- vocabulary and alias review;
- consent management;
- alert notifications;
- device health status;
- multi-user switching for approved caregivers;
- assisted-home resident assignment view.

## 3. Access Model

| Role | Key Capabilities |
|---|---|
| Family caregiver | broad configuration, alerts, summaries |
| Professional caregiver | assigned-user live feed, limited edits |
| Guardian | consent and access administration where lawful |
| Administrator | deployment and health metadata, limited content access |

## 4. Privacy Rules
- raw transcripts hidden by default;
- transcript reveal requires elevated permission and audit log;
- no raw audio playback in standard v1 app;
- user-lockable items supported where capacity allows.

## 5. Technical Architecture
- React Native client;
- cloud API backend;
- push notifications;
- secure auth;
- offline cache of limited recent state.

## 6. Assisted-Home Requirements
- roster view for assigned residents;
- shift handover notes;
- strong separation between staff and admin roles;
- rapid revocation when staffing changes.

## 7. Performance Targets
- live feed update <= 1s nominal;
- critical alert delivery <= 10s nominal;
- offline cache of recent summaries available.

## 8. App Governance
App releases affecting:
- consent,
- caregiver permissions,
- transcript exposure,
- researcher opt-ins

must undergo heightened review.
