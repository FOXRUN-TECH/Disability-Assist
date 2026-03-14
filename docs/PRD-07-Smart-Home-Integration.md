# PRD-07 · Smart Home & Device Integration

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Allow the user to control key comfort, media, and communication functions without needing precise conventional commands.

## 2. Primary Integration Strategy

Home Assistant is the default integration hub for:
- lights;
- switches;
- scenes;
- media playback;
- TV / streaming;
- thermostat where available;
- notifications and helper entities.

## 3. Direct Integrations
Direct integrations are allowed for:
- media services where hub support is insufficient;
- caregiver messaging services;
- selected device types important to pilot sites.

## 4. Supported v1 Action Classes
- light on/off/dim;
- media play/pause/volume/source;
- TV power/input/basic navigation;
- comfort routines;
- reminder create/cancel;
- caregiver message / attention request.

## 5. Unsupported v1/v2 Actions Without Separate Governance
- door unlock;
- security alarm disarm;
- purchases;
- medical equipment control unless separately approved.

## 6. Names and Mappings
The system must support user-specific aliases, for example:
- “bright box” -> living room lamp;
- “my show” -> predefined media routine;
- scripted quote -> preferred playlist.

## 7. Reliability
- idempotent execution where possible;
- duplicate suppression;
- fallback acknowledgement if integration unavailable;
- action audit trail.
