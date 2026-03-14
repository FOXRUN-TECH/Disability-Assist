# Consent Lane Matrix

**Project:** Disability-Assist
**Version:** 0.0.1
**Status:** Phase 0 Draft
**Authority:** PRD-11 Section 4, PRD-13 Sections 5-6

## Decision Framework

Dignity > Privacy > Accuracy > Simplicity

## Governing Principle

Refusing optional lanes must NOT break core local functionality beyond the requested
feature itself. Each lane is independently consentable and independently revocable.

---

## Summary Matrix

| Lane | Name | Required? | Default | Opt-In Method | Revocation Effect |
|------|------|-----------|---------|---------------|-------------------|
| 1 | Core Cloud Operation | Required | On | Accepted at setup | Service stops |
| 2 | Caregiver Remote Access | Optional | Off | Per-caregiver toggle | Feed stops, no history access |
| 3 | Cloud Sync of Personalization | Optional | Off | Settings toggle | Local-only, no cross-device sync |
| 4 | De-identified Community Learning | Optional | Off | Participation toggle | No new contributions; existing data stays de-identified |
| 5 | De-identified Research Participation | Optional | Off | Research consent form | Future data excluded; existing per DUA terms |
| 6 | Optional Audio Research | Optional | Off | Explicit separate consent | Audio deleted or excluded per protocol |

---

## Lane 1: Core Cloud Operation

### Data Flows

- Audio captured on device -> cloud STT transcription -> LLM intent engine -> TTS voice
  response returned to device.
- Device registration and account provisioning.
- Consent status stored in cloud (canonical) with local cache.
- Cloud-side audit logs for authentication, consent changes, and errors.

### Consent Collection

- Presented during initial device setup as a clear, plain-language agreement.
- Must be accepted before any cloud feature activates.
- Setup flow must explain what "core cloud operation" means in concrete terms:
  audio is sent to cloud servers for processing, results are returned, audio is not
  retained beyond processing unless another lane permits it.

### Versioning

- Consent version tracked in the consent record (e.g., `core-cloud-v1.0`).
- When the consent text changes materially, the version increments and re-consent
  is required at next interaction.
- Minor clarifications (no change in data handling) increment a patch version and
  do not require re-consent but are logged.

### Revocation Behavior

- **What changes:** All cloud processing stops. Device cannot perform STT, LLM
  inference, or TTS via cloud. The device falls back to offline-only mode (limited
  or no functionality in v1).
- **What remains:** Local data on the device is not deleted. Account record is
  retained for 30 days to allow re-activation, then purged per retention policy.
- **User experience:** Clear warning that revoking this lane disables the primary
  service. No guilt language; factual description only.

### Guardian / Substitute Decision-Maker Considerations

- For users who cannot independently consent, a guardian or substitute decision-maker
  (SDM) may accept Lane 1 on the user's behalf.
- The legal basis for the SDM's authority must be recorded in the system (e.g.,
  power of attorney, legal guardianship, parental authority for minors).
- If the user later gains or regains capacity, they may review and re-affirm or
  revoke consent independently.
- SDM consent decisions are audit-logged with the SDM's identity and stated authority.

### Compliance Mapping

| Jurisdiction | Basis | Notes |
|---|---|---|
| PIPEDA (Canada) | Meaningful consent, purpose limitation | Plain-language explanation required; consent must be specific to stated purposes |
| HIPAA-adjacent (US) | Not a covered entity in v1, but design for BAA readiness | Treat voice data as sensitive; encryption in transit and at rest |
| GDPR (EU/EEA) | Art. 6(1)(a) consent or Art. 6(1)(b) contract performance | Explicit consent preferred given disability-related data (Art. 9) |
| UK GDPR | Same as GDPR with ICO guidance | Age-appropriate design considerations for minors |

### Code Annotation

All code paths handling Lane 1 data must include:

```python
# consent-lane: core-cloud
```

---

## Lane 2: Caregiver Remote Access

### Data Flows

- LLM intent engine produces paraphrased intent summaries (never raw transcripts).
- Summaries pushed to caregiver feed, filtered by role and assignment.
- Escalation alerts (comfort request unresolved, repeated failed understanding,
  user requests caregiver, missed routine acknowledgement).
- Caregiver roster management (add, remove, role assignment).
- All caregiver access events logged to audit trail.

### Consent Collection

- Per-caregiver toggle in user (or guardian) settings.
- Each caregiver added by name/identifier with a specific role assignment.
- The user (or guardian) controls who receives the feed and can revoke individually.
- Adding a professional caregiver in assisted-home mode may be initiated by a
  facility administrator but must be ratified by the user or guardian.

### Versioning

- Consent version: `caregiver-access-v1.0`.
- Changes to what data flows to caregivers require version increment and re-consent.
- Adding a new caregiver does not require re-consent to the lane itself, only
  confirmation of the specific caregiver assignment.

### Revocation Behavior

- **What changes:** The revoked caregiver's feed stops immediately. No new summaries
  or alerts are delivered.
- **What remains:** Historical summaries already delivered to the caregiver are not
  retroactively deleted from their device (technically infeasible), but the caregiver
  loses access to any server-side history. Audit logs of past access are retained.
- **Revoking the entire lane:** All caregiver feeds stop. The user continues to use
  the system normally; only the sharing dimension is removed.
- **Core functionality impact:** None. Lane 2 refusal does not affect Lane 1.

### Guardian / Substitute Decision-Maker Considerations

- A guardian may configure caregivers on the user's behalf.
- Professional caregiver assignments in facility settings require both administrative
  assignment and guardian/user ratification.
- If a user has fluctuating capacity, the system must support a model where the user
  can manage their own caregiver list during periods of capacity, and the guardian
  manages it otherwise. The capacity model flag is set by the guardian, not the system.
- The system must never auto-add caregivers without explicit consent action.

### Compliance Mapping

| Jurisdiction | Basis | Notes |
|---|---|---|
| PIPEDA (Canada) | Separate consent for disclosure to third parties | Each caregiver is a separate disclosure recipient |
| HIPAA-adjacent (US) | Minimum necessary standard | Paraphrase only; never raw transcript |
| GDPR (EU/EEA) | Art. 6(1)(a) explicit consent; Art. 9 special category | Per-recipient consent; data minimization |
| UK GDPR | Same as GDPR | ICO guidance on sharing health-adjacent data |

### Code Annotation

```python
# consent-lane: caregiver-access
```

---

## Lane 3: Cloud Sync of Personalization

### Data Flows

- Vocabulary mappings, device aliases, routines, accessibility settings,
  media preferences -> encrypted cloud backup.
- Cloud -> device restore on new/replacement device (if lane active).
- Consent preferences themselves are always cloud-synced under Lane 1 (canonical
  consent record); Lane 3 covers everything else.

### Consent Collection

- Settings toggle, off by default.
- Plain-language explanation: "Your personalization data (vocabulary, routines,
  preferences) will be backed up to the cloud so it can be restored if your device
  is replaced."

### Versioning

- Consent version: `cloud-sync-v1.0`.
- Material changes to what is synced require version increment and re-consent.

### Revocation Behavior

- **What changes:** Cloud sync stops. Existing cloud backup is marked for deletion
  within 30 days (or immediately on explicit deletion request).
- **What remains:** All local personalization data remains on the device and
  continues to function. The user simply loses cloud backup and cross-device sync.
- **Core functionality impact:** None. The device works identically with local-only
  personalization.

### Guardian / Substitute Decision-Maker Considerations

- Guardian may enable or disable cloud sync on behalf of the user.
- If the user has capacity, they may override the guardian's choice for this
  optional lane (unless legal authority specifies otherwise).

### Compliance Mapping

| Jurisdiction | Basis | Notes |
|---|---|---|
| PIPEDA (Canada) | Consent for secondary use (backup) | Must explain cloud storage location |
| HIPAA-adjacent (US) | Design for encryption at rest | Personalization data may contain health-adjacent patterns |
| GDPR (EU/EEA) | Art. 6(1)(a) consent; storage limitation | Deletion within 30 days of revocation |
| UK GDPR | Same as GDPR | Data residency considerations |

### Code Annotation

```python
# consent-lane: cloud-sync
```

---

## Lane 4: De-identified Community Learning

### Data Flows

- De-identified interaction patterns extracted from local usage.
- Direct identifiers removed, device-specific labels generalized, timestamps
  coarsened (per PRD-13 contribution pipeline).
- Payload validated for residual identifiers before transmission.
- Encrypted in transit to shared assistive priors corpus (Qdrant or equivalent).
- Consent status checked before ingestion.
- Contributed patterns used to seed low-confidence priors for new users
  (condition-scoped, overridable).

### What Is Shared

Per PRD-13 Section 2:

- Vocabulary mappings (de-identified).
- Action-success patterns.
- Routine templates.
- Sensory-safe preference archetypes.
- Accessibility-related phrasing priors.
- Condition-scoped assistive strategies.

NOT shared: raw transcripts, audio, personal identifiers, caregiver names,
location data, or anything framed as "personality."

### Consent Collection

- Participation toggle in settings, off by default.
- Plain-language explanation of what de-identification means and what is contributed.
- Separate from Lane 5 (research) -- a user may contribute to community learning
  without participating in research, or vice versa.

### Versioning

- Consent version: `community-learning-v1.0`.
- Changes to the de-identification pipeline or what is contributed require version
  increment and re-consent.

### Revocation Behavior

- **What changes:** No new contributions are sent from this user's device.
- **What remains:** Previously contributed de-identified data remains in the corpus.
  Because it has been de-identified, it cannot be practically traced back to the
  user. This is explained at consent time.
- **Core functionality impact:** None. The user still benefits from community priors
  (receiving is part of Lane 1, not Lane 4). Only contributing is affected.

### Guardian / Substitute Decision-Maker Considerations

- Guardian may enable or disable on behalf of the user.
- For minors, guardian consent is required and the minor's assent should be sought
  where developmentally appropriate.
- This lane is never auto-enabled, even by guardians or administrators.

### Compliance Mapping

| Jurisdiction | Basis | Notes |
|---|---|---|
| PIPEDA (Canada) | De-identified data has reduced obligations but consent still collected | Document de-identification method |
| HIPAA-adjacent (US) | Safe Harbor or Expert Determination for de-identification | Document method and residual risk |
| GDPR (EU/EEA) | If truly anonymous, GDPR does not apply; if pseudonymous, Art. 6(1)(a) | Conservative: treat as pseudonymous, collect consent |
| UK GDPR | Same as GDPR | ICO anonymization guidance |

### Code Annotation

```python
# consent-lane: community-learning
```

---

## Lane 5: De-identified Research Participation

### Data Flows

- De-identified datasets extracted per approved research protocol.
- Data use agreement (DUA) governs each research engagement.
- Review workflow validates purpose limitation before data release.
- Datasets may include interaction patterns, vocabulary distributions,
  action-success rates, and other non-identifying usage data.
- Re-identification risk review conducted before each release.

### Consent Collection

- Research consent form, separate from all other lanes.
- Must explain: who may access the data, for what purpose classes, under what
  governance, and how long.
- Consent is purpose-scoped: the user consents to "research into assistive
  communication" (or similar defined purpose), not to unlimited research use.

### Versioning

- Consent version: `research-v1.0`.
- Material changes to research governance, purpose scope, or data handling
  require version increment and re-consent.
- Each DUA is independently versioned and tracked.

### Revocation Behavior

- **What changes:** No new data from this user is included in future research
  datasets.
- **What remains:** Data already released under an executed DUA remains governed
  by that DUA's terms. This is explained at consent time. Researchers cannot
  receive new data from the revoked user, but existing de-identified datasets
  already in use are not recalled (practically infeasible and governed by DUA).
- **Core functionality impact:** None.

### Guardian / Substitute Decision-Maker Considerations

- Guardian consent required for users who lack capacity and for all minors.
- Research involving minors may require additional institutional review (IRB/REB)
  approval beyond the system's own governance.
- The system records whether consent was given by the user directly or by a
  guardian, and on what authority basis.

### Compliance Mapping

| Jurisdiction | Basis | Notes |
|---|---|---|
| PIPEDA (Canada) | Research exception with safeguards (PIPEDA s.7(2)(c)) or consent | Prefer consent; document safeguards either way |
| HIPAA-adjacent (US) | De-identified per Safe Harbor / Expert Determination | IRB/Privacy Board review for any identifiable data |
| GDPR (EU/EEA) | Art. 89 research exemptions with safeguards; or Art. 6(1)(a) consent | DPIA required; pseudonymization minimum |
| UK GDPR | Same as GDPR + UK research provisions | ICO research guidance |

### Code Annotation

```python
# consent-lane: research
```

---

## Lane 6: Optional Audio Research

### Data Flows

- Audio samples (voice recordings) contributed to a governed research corpus.
- This is the only lane that involves retention of raw audio beyond immediate
  processing.
- Audio is stored encrypted, access-controlled, and governed by DUA.
- Audio is never used for community learning (Lane 4) -- only for approved
  research protocols.

### Consent Collection

- Explicit separate consent, independent of all other lanes.
- Off by default. Must be actively sought; never bundled with other consents.
- The consent form must clearly state:
  - Audio recordings of your voice will be stored.
  - They will be used for research into assistive communication.
  - They will be stored securely and access-controlled.
  - You can request deletion at any time.
- This lane should only be offered when a governed research program exists to
  receive the data. Do not collect audio speculatively.

### Versioning

- Consent version: `audio-research-v1.0`.
- Any change to audio handling, storage location, access controls, or research
  scope requires version increment and re-consent.

### Revocation Behavior

- **What changes:** No new audio is collected or retained.
- **What remains:** On revocation, stored audio is either:
  - Deleted within 30 days (default), or
  - Excluded from future research use but retained in anonymized form if already
    incorporated into a published dataset (per DUA terms).
- The user may request immediate deletion, which is honored within 30 days for
  audio not yet released under a DUA.
- **Core functionality impact:** None. Audio processing for Lane 1 (STT) continues
  normally; the audio is simply not retained.

### Guardian / Substitute Decision-Maker Considerations

- Guardian consent required. This lane involves the most sensitive data type
  (biometric voice data).
- For minors, additional institutional review may be required.
- The system must record the specific authority under which consent was given.
- Revocation by either the user (if they have capacity) or the guardian is
  honored -- either party can revoke.

### Compliance Mapping

| Jurisdiction | Basis | Notes |
|---|---|---|
| PIPEDA (Canada) | Explicit consent required for biometric data | Retention schedule must be defined and communicated |
| HIPAA-adjacent (US) | Voice is biometric identifier; treat as PHI-adjacent | Encryption at rest mandatory; access audit mandatory |
| GDPR (EU/EEA) | Art. 9 special category (biometric for identification) | Explicit consent (Art. 9(2)(a)); DPIA required |
| UK GDPR | Same as GDPR | ICO biometric data guidance applies |

### Code Annotation

```python
# consent-lane: audio-research
```

---

## Cross-Cutting Requirements

### Consent Record Schema

Every consent record must include:

| Field | Description |
|---|---|
| `user_id` | The user whose data is governed |
| `lane` | Lane identifier (1-6) |
| `version` | Consent text version accepted |
| `granted_by` | User ID of the person who granted consent (may differ from `user_id` if guardian) |
| `authority_basis` | Self, parental, guardianship, power of attorney, or other legal basis |
| `granted_at` | Timestamp of consent grant |
| `revoked_at` | Timestamp of revocation (null if active) |
| `revoked_by` | User ID of the person who revoked (null if active) |
| `ip_or_device` | Device or session identifier at time of consent action |

### Consent Versioning Protocol

1. Each lane has an independent version string (e.g., `core-cloud-v1.0`).
2. Material changes (new data flows, new recipients, new purposes) increment the
   major version and require re-consent.
3. Clarification-only changes increment the minor version and are logged but do
   not require re-consent.
4. The system must not process data under a lane if the user's accepted version
   is below the current required version.

### Interaction Between Lanes

- Lane 1 is prerequisite for all other lanes (no cloud features without core
  cloud consent).
- Lanes 2-6 are independent of each other.
- Revoking Lane 1 implicitly suspends Lanes 2-6 (no cloud processing available),
  but does not delete the consent records for Lanes 2-6. If Lane 1 is re-granted,
  previously active optional lanes resume without re-consent (same version).
- Lane 6 data is never used for Lane 4 purposes (community learning).

### Audit Trail

- All consent grants, revocations, and version changes are audit-logged.
- All caregiver access events (Lane 2) are audit-logged.
- All research data releases (Lanes 5-6) are audit-logged.
- Audit logs are retained for the longer of: 7 years or the applicable regulatory
  minimum.
- Audit logs are append-only and tamper-evident.

### User-Facing Consent Dashboard

The system must provide a consent dashboard (accessible to user or guardian) showing:

- Current status of each lane (active/inactive).
- Version accepted vs. current version.
- Date of last consent action.
- List of caregivers with access (Lane 2).
- Option to revoke any optional lane.
- Option to request data export or deletion.
