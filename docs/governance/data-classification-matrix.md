# Data Classification Matrix -- Disability-Assist

**Version:** 0.1.0 | **Status:** Draft | **Last Updated:** 2026-03-13

## Purpose

This document defines the data classification levels for the Disability-Assist system and specifies handling requirements for each level. All contributors, operators, and integrators must follow these requirements when processing, storing, or transmitting data within the system.

**Decision Framework:** Dignity > Privacy > Accuracy > Simplicity

**Disclaimer:** This system is assistive, not clinical. It does not process diagnostic data, treatment records, or emergency communications. Data classifications here reflect assistive communication and environmental control use cases only.

---

## Classification Levels

| Level | Label | Color | Description |
|-------|-------|-------|-------------|
| 1 | **Public** | Green | Safe for public disclosure. No confidentiality requirements. |
| 2 | **Internal** | Yellow | For internal system use only. Not harmful if exposed, but not intended for public release. |
| 3 | **Sensitive** | Orange | Contains personal or behavioral data. Requires access controls and encryption. |
| 4 | **Restricted** | Red | Maximum protection. Contains raw biometric data, authentication secrets, or authority records. Minimum access principle strictly enforced. |

---

## Level 1: Public (Green)

### Examples

- Open-source project code and documentation
- Published PRDs, architecture documents, and contribution guides
- Public issue tracker content (scrubbed of user-specific details)
- System feature descriptions and release notes
- Hardware reference design specifications

### Handling Requirements

| Aspect | Requirement |
|--------|-------------|
| **Encryption in transit** | Not required (but HTTPS preferred for web-hosted docs) |
| **Encryption at rest** | Not required |
| **Access control** | None -- publicly accessible |
| **Logging** | Standard web server logs (no user-specific tracking) |
| **Retention** | Indefinite (version-controlled in git) |
| **Deletion** | Standard git history management; no special deletion process |
| **Consent lane** | None required |
| **Accessible by** | Anyone |
| **Storage location** | Public git repository, project website |

---

## Level 2: Internal (Yellow)

### Examples

- System logs stripped of PII (application events, errors, performance metrics)
- Device health metrics (CPU, memory, uptime, network status)
- Anonymized action audit records (action type, risk tier, timestamp -- no user identity)
- Aggregated usage statistics (command frequency, response latency distributions)
- Internal configuration values (non-secret)
- Anonymized error reports

### Handling Requirements

| Aspect | Requirement |
|--------|-------------|
| **Encryption in transit** | Required (TLS 1.2+) |
| **Encryption at rest** | Recommended but not mandatory |
| **Access control** | System operators and administrators only; no public exposure |
| **Logging** | Access logging for audit purposes |
| **Retention** | 90 days for operational logs; 1 year for aggregated metrics; bounded, never indefinite |
| **Deletion** | Automated expiry based on retention period; manual deletion on request within 30 days |
| **Consent lane** | `core-cloud` (implicit with system use) |
| **Accessible by** | Administrator |
| **Storage location** | Cloud infrastructure (log aggregation, metrics store); device local storage (temporary) |

### PII Safeguards

- All Internal-level data must be stripped of user identifiers before storage
- Log scrubbing applied at write time, not retroactively
- Device health metrics must not include location, network SSID, or MAC addresses of non-system devices
- `check-privacy-patterns.py` hook enforces no-PII-in-logs at development time

---

## Level 3: Sensitive (Orange)

### Examples

- User assistive profiles (vocabulary preferences, interaction patterns, communication style settings)
- Vocabulary mappings and personalized phrase banks
- Caregiver paraphrases (LLM-generated summaries of user intent, never raw transcripts)
- Consent records (what the user has opted into, when, by whom)
- Role assignments (user, caregiver, professional, guardian, administrator)
- User account information (name, contact details, relationship records)
- Session history (intent categories over time, not verbatim content)
- Home Assistant entity mappings (which devices, which rooms)
- De-identified community learning patterns (aggregated, not individual)

### Handling Requirements

| Aspect | Requirement |
|--------|-------------|
| **Encryption in transit** | Required (TLS 1.3) |
| **Encryption at rest** | Required (AES-256 or equivalent) |
| **Access control** | Role-based access control (RBAC) enforced at API layer; principle of least privilege |
| **Logging** | All access logged with actor identity, timestamp, and operation; access logs are themselves Sensitive |
| **Retention** | User profiles: active account lifetime + 30-day deletion grace period. Consent records: retained for audit for 3 years after revocation. Session history: 90 days rolling. |
| **Deletion** | On user/guardian request: delete within 30 days; provide deletion confirmation; audit trail of deletion retained (metadata only, no content) |
| **Consent lane** | Varies by data type (see consent lane mapping below) |
| **Accessible by** | See role access matrix below |
| **Storage location** | PostgreSQL (encrypted columns for PII fields); device local cache (encrypted, session-scoped only) |

### Role Access Matrix (Sensitive Data)

| Data Type | User | Caregiver | Professional | Guardian | Administrator |
|-----------|------|-----------|-------------|----------|---------------|
| User profile | Read/Write (own) | Read (assigned) | Read (assigned) | Read/Write (ward) | Read (all) |
| Vocabulary mappings | Read/Write (own) | Read (assigned) | Read/Write (assigned) | Read/Write (ward) | Read (all) |
| Caregiver paraphrases | N/A | Read (assigned, filtered by role) | Read (assigned) | Read (ward) | Read (all, audit only) |
| Consent records | Read (own) | None | None | Read/Write (ward) | Read (all) |
| Role assignments | Read (own) | Read (own) | Read (own) | Read/Write (ward) | Read/Write (all) |
| Account information | Read/Write (own) | Read (assigned, limited) | Read (assigned, limited) | Read/Write (ward) | Read/Write (all) |
| Session history | Read (own) | Read (assigned, summarized) | Read (assigned) | Read (ward) | Read (all, audit only) |
| HA entity mappings | Read/Write (own) | Read (assigned) | None | Read/Write (ward) | Read/Write (all) |
| Community patterns | None | None | Read (de-identified) | None | Read (de-identified) |

### Consent Lane Mapping (Sensitive Data)

| Data Type | Consent Lane | Opt-in Required |
|-----------|-------------|-----------------|
| User profile | `core-cloud` | Implicit (required for system function) |
| Vocabulary mappings | `core-cloud` | Implicit |
| Caregiver paraphrases | `caregiver-access` | Explicit opt-in |
| Consent records | `core-cloud` | Implicit |
| Role assignments | `core-cloud` | Implicit |
| Session history | `cloud-sync` | Explicit opt-in |
| HA entity mappings | `core-cloud` | Implicit |
| Community patterns | `community-learning` | Explicit opt-in |

---

## Level 4: Restricted (Red)

### Examples

- Raw audio recordings (if retained under explicit audio-research consent)
- Verbatim STT transcripts (transient in processing pipeline; never stored by default)
- Authentication credentials (password hashes, API keys, encryption keys)
- JWT signing keys and refresh tokens
- Guardian authority records (legal authority documentation, substitute decision-maker designations)
- Encryption keys (data-at-rest keys, TLS certificates, device identity keys)
- Cloud provider API keys and service account credentials
- Database connection strings with credentials
- Device provisioning secrets

### Handling Requirements

| Aspect | Requirement |
|--------|-------------|
| **Encryption in transit** | Required (TLS 1.3, no fallback) |
| **Encryption at rest** | Required (AES-256); key management via dedicated secrets manager; keys rotated on schedule |
| **Access control** | Maximum restriction; named individuals only; no group access; multi-factor authentication required for human access |
| **Logging** | All access logged with full context (who, what, when, why); access logs for Restricted data are themselves Restricted; tamper-evident logging |
| **Retention** | Raw audio: maximum 30 days, then permanent deletion (no archive). Credentials: rotated per policy, old credentials purged. Guardian records: active relationship lifetime + legal retention requirement. Transcripts: not retained (transient processing only). |
| **Deletion** | Immediate on consent revocation (raw audio); cryptographic deletion where supported; deletion verification required; audit trail retained |
| **Consent lane** | See consent lane mapping below |
| **Accessible by** | See role access matrix below |
| **Storage location** | Secrets manager (credentials, keys); encrypted PostgreSQL columns (guardian records); encrypted ephemeral storage (raw audio, if retained); never in application logs, never in version control, never in client-side storage |

### Role Access Matrix (Restricted Data)

| Data Type | User | Caregiver | Professional | Guardian | Administrator |
|-----------|------|-----------|-------------|----------|---------------|
| Raw audio | None | None | None | None | None (system-only, if retained) |
| Verbatim transcripts | None | None | None | None | None (transient, never stored) |
| Auth credentials | Own only | Own only | Own only | Own only | System management only |
| JWT signing keys | None | None | None | None | System management only |
| Guardian authority records | None | None | None | Read (own authority) | Read/Write (all) |
| Encryption keys | None | None | None | None | Key management only |
| API keys | None | None | None | None | System management only |
| Device provisioning secrets | None | None | None | None | System management only |

### Consent Lane Mapping (Restricted Data)

| Data Type | Consent Lane | Opt-in Required |
|-----------|-------------|-----------------|
| Raw audio | `audio-research` | Explicit opt-in; guardian approval if applicable |
| Verbatim transcripts | N/A (transient, not retained) | N/A |
| Auth credentials | `core-cloud` | Implicit (required for authentication) |
| Guardian authority records | `core-cloud` | Implicit (required for guardian role) |
| Encryption/API keys | N/A (system infrastructure) | N/A |

---

## Consent Lanes Reference

The six consent lanes governing data flow in Disability-Assist:

| Lane | Type | Description |
|------|------|-------------|
| `core-cloud` | Required | Basic cloud processing (STT, LLM, TTS). Implicit with system use. Minimum data for assistive function. |
| `caregiver-access` | Optional | Paraphrased intent shared with assigned caregivers. Never raw transcripts. Role-filtered. |
| `cloud-sync` | Optional | Session history and preferences synchronized across devices via cloud. |
| `community-learning` | Optional | De-identified patterns contributed to shared assistive vocabulary. |
| `research` | Optional | Anonymized, aggregated data shared with approved researchers. Ethics review required. |
| `audio-research` | Optional | Raw audio retained for speech model improvement. Maximum consent requirements. Guardian approval mandatory if applicable. |

---

## Cross-Cutting Requirements

### Regulatory Alignment

All data handling must be consistent with:

- **PIPEDA** (Canada) -- consent, purpose limitation, retention limits, access rights
- **HIPAA-adjacent practices** (US) -- minimum necessary, access controls, audit trails (system is not a covered entity but follows best practices)
- **GDPR** (EU) -- data minimization, purpose limitation, right to erasure, data portability
- **UK GDPR** -- same as GDPR with UK-specific provisions

### Development Enforcement

| Tool | What It Enforces |
|------|-----------------|
| `check-privacy-patterns.py` | No PII in logs, no raw transcript exposure, no audio retention without consent annotation |
| `check-consent-lanes.py` | Data-handling functions annotated with consent lane |
| `check-privacy-patterns-precommit.py` | Blocks commits containing PII violation patterns |
| Ruff D rules | Documentation requirements (including data handling docs) |

### Incident Response

If data is exposed at a level inconsistent with its classification:

1. Immediately contain the exposure (revoke access, rotate credentials)
2. Assess the scope (what data, what classification, who was exposed)
3. Notify affected users/guardians per applicable regulation
4. Document the incident and update threat model
5. Implement corrective controls

---

## Review Schedule

This matrix should be reviewed:

- Before each phase transition
- When new data types are introduced
- When new integrations or providers are added
- After any data-related incident
- At minimum every 6 months during active development

---

*This document is part of the Disability-Assist governance framework. For the complete project specification, see [PRD-00-Index.md](../PRD-00-Index.md). For privacy and consent details, see [PRD-11-Privacy-Security-and-Ethics.md](../PRD-11-Privacy-Security-and-Ethics.md). For the threat model, see [threat-model.md](threat-model.md).*
