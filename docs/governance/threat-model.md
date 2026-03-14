# Threat Model -- Disability-Assist

**Version:** 0.1.0 | **Status:** Draft | **Last Updated:** 2026-03-13

## Scope and Disclaimer

This threat model covers the Disability-Assist system: an open-source, cloud-first assistive communication and environmental-control platform for people with speech, cognitive, sensory, developmental, and age-related communication barriers.

**This system is NOT a clinical device, emergency response system, diagnostic tool, or substitute for professional judgment.** It does not process medication decisions, financial transactions, emergency calls, or clinical assessments. Threats related to those categories are out of scope because the system enforces hard constraints preventing such actions.

**Decision Framework:** Dignity > Privacy > Accuracy > Simplicity

All mitigations are evaluated against this hierarchy. When trade-offs arise, protecting the dignity and privacy of the person using the system takes precedence over accuracy or engineering simplicity.

## System Overview

| Component | Technology | Trust Boundary |
|-----------|-----------|----------------|
| Local device | Raspberry Pi 5, Python, local SQLite | Physical device perimeter |
| Cloud inference | STT, LLM intent engine, TTS providers | Cloud API boundary |
| Database | PostgreSQL (accounts, consent, audit) | Cloud infrastructure |
| Vector store | Qdrant (assistive priors, community patterns) | Cloud infrastructure |
| Smart-home | Home Assistant API integration | Local network / HA instance |
| Mobile app | React Native caregiver app | Mobile device perimeter |

## Trust Boundaries

1. **Device <-> Cloud**: TLS-encrypted API calls. Device authenticates with scoped tokens.
2. **Device <-> Home Assistant**: Local network. HA long-lived access tokens.
3. **Cloud <-> Mobile App**: TLS-encrypted API calls. JWT-based auth with role enforcement.
4. **Cloud <-> Database**: Encrypted connections. Service-level credentials.
5. **Cloud <-> Vector Store**: Internal network or encrypted connection.
6. **User <-> Device**: Physical proximity. Wake word activation. No biometric auth (Phase 0).

---

## 1. Audio/Voice Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| AV-01 | **Eavesdropping on ambient audio** -- always-on microphone captures private conversations beyond wake word activation | High | Medium | Wake word gating before any audio leaves device; VAD (voice activity detection) limits capture window; no raw audio retained by default; audio buffer purged after STT response received | Planned |
| AV-02 | **Replay attack** -- attacker records and replays a valid voice command to trigger actions | Medium | Low | Timestamp validation on commands; session-bound request IDs; risk tier enforcement limits impact of replayed commands to Tier 0-1 actions only | Planned |
| AV-03 | **Voice spoofing** -- attacker mimics the user's voice to issue commands | Medium | Low | System does not use voice as an authentication factor; all Tier 2 actions require explicit confirmation; Tier 3 actions are blocked entirely; caregiver/guardian role required for sensitive operations | Planned |
| AV-04 | **Raw audio exfiltration** -- cloud provider or network attacker captures raw audio stream | High | Low | Audio transmitted only during active utterance (post-wake-word, post-VAD); TLS 1.3 for transport; no audio persistence in cloud unless explicit consent (audio-research lane); audio deleted from memory after STT processing | Planned |
| AV-05 | **Microphone hijack via compromised device** -- malware on RPi5 activates microphone outside normal flow | High | Low | Minimal OS image; no general-purpose user accounts; hardware LED indicator tied to mic activation; application-level mic access control | Planned |

## 2. Cloud Transport Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| CT-01 | **Man-in-the-middle on device-to-cloud** -- attacker intercepts STT/LLM/TTS traffic | High | Low | TLS 1.3 enforced for all cloud API calls; certificate pinning on device; no fallback to unencrypted transport | Planned |
| CT-02 | **API key exposure** -- cloud provider API keys leaked in code, logs, or device storage | High | Medium | Keys stored in environment variables, never in code; `.env` files gitignored; device keys stored in encrypted config; key rotation policy; secrets detection in pre-commit hooks | Partial |
| CT-03 | **Cloud provider compromise** -- STT/LLM/TTS provider breached, exposing processed audio or text | High | Low | No PII sent to inference providers beyond utterance text; no user identifiers in STT/TTS requests; contractual data handling requirements with providers; provider selection criteria include data handling policies | Planned |
| CT-04 | **Token theft in transit** -- JWT or session tokens intercepted | High | Low | Short-lived JWTs; refresh token rotation; TLS-only transport; secure cookie flags on web endpoints | Planned |

## 3. Data at Rest Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| DR-01 | **Local SQLite exposure** -- device SQLite cache accessed by attacker with physical or remote access | Medium | Medium | SQLite stores only operational cache (no raw audio, no verbatim transcripts); filesystem permissions restrict access; planned: encrypted SQLite (SQLCipher); device full-disk encryption | Planned |
| DR-02 | **PostgreSQL breach** -- cloud database compromised, exposing accounts, consent records, audit logs | High | Low | Encrypted connections; field-level encryption for sensitive columns (consent records, role assignments); database access restricted to application service accounts; regular backups with encryption; audit logging on access | Planned |
| DR-03 | **Vector store data leakage** -- Qdrant vectors reverse-engineered to recover source utterances or user patterns | Medium | Low | Vectors derived from de-identified, aggregated patterns only; no verbatim text stored in vectors; community-learning lane requires explicit consent; vectors not linkable to individual users without additional data | Planned |
| DR-04 | **Backup exposure** -- database or device backups stored without encryption | High | Low | All backups encrypted at rest; backup access restricted to administrator role; backup retention policy enforced (bounded, not indefinite) | Planned |
| DR-05 | **Log file PII leakage** -- application logs contain personal data, transcripts, or identifiers | Medium | Medium | Structured logging with PII filter; no raw transcripts in logs; no user identifiers beyond opaque session IDs; `check-privacy-patterns.py` hook enforces at development time; log rotation with bounded retention | Partial |

## 4. Identity and Access Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| IA-01 | **Role escalation (caregiver to guardian)** -- caregiver account gains guardian privileges, accessing consent management or restricted data | High | Low | Role assignments stored in PostgreSQL with audit trail; role changes require administrator or existing guardian approval; role hierarchy enforced at API layer; no self-promotion of roles | Planned |
| IA-02 | **Unauthorized device pairing** -- attacker pairs a rogue device to a user's cloud account | Medium | Low | Device pairing requires physical confirmation on device plus cloud-side approval from authorized role; device identity bound to hardware identifier; pairing audit logged | Planned |
| IA-03 | **JWT theft or forgery** -- stolen or forged JWT used to access API as another user or role | High | Low | Short-lived access tokens (15 min); refresh token rotation with reuse detection; JWT signature verification on every request; role claims validated against database on sensitive operations | Planned |
| IA-04 | **Orphaned access** -- former caregiver retains access after relationship ends | Medium | Medium | Role revocation by guardian or administrator; access review reminders; session invalidation on role change; audit trail of all role modifications | Planned |
| IA-05 | **Substitute decision-maker conflict** -- multiple guardians issue conflicting consent or authority decisions | Medium | Low | Single primary guardian model with documented authority chain; conflict resolution requires administrator mediation; all authority changes audited | Planned |

## 5. Smart-Home Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| SH-01 | **Unauthorized device control** -- attacker triggers smart-home actions (lights, locks, appliances) | High | Low | Risk tier enforcement: only Tier 0-1 actions execute freely; Tier 2 requires confirmation; Tier 3 blocked; HA API access scoped to specific entities; no lock/security system control without guardian approval | Planned |
| SH-02 | **Home Assistant API abuse** -- compromised HA token used to control devices beyond intended scope | Medium | Low | HA long-lived tokens scoped to minimum required entities; token stored encrypted on device; separate tokens per device instance; token rotation policy | Planned |
| SH-03 | **Risk tier bypass** -- attacker or bug causes a Tier 2/3 action to execute without confirmation | High | Low | Risk tier enforcement in policy layer (separate from action router); defense in depth with HA entity allowlists; all action executions audit-logged with tier and confirmation status | Planned |
| SH-04 | **Command injection via intent** -- crafted utterance causes LLM to generate unintended HA service calls | Medium | Low | Action router validates all commands against allowlist of HA services and entities; no arbitrary service call passthrough; parameterized command templates only | Planned |

## 6. Privacy and Consent Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| PC-01 | **Consent bypass** -- data flows proceed without required consent lane opt-in | High | Medium | Consent lane enforcement in code (`check-consent-lanes.py` hook); runtime consent verification before data leaves core processing; six defined consent lanes with explicit opt-in for optional lanes | Partial |
| PC-02 | **Raw transcript exposure to caregivers** -- verbatim speech shown to caregivers instead of paraphrased intent | High | Medium | Caregiver feed receives only LLM-generated paraphrases, never raw STT output; paraphrase function enforced at API boundary; `check-privacy-patterns.py` detects raw transcript exposure patterns | Partial |
| PC-03 | **PII in application logs** -- names, health information, or identifiers written to log files | Medium | Medium | Structured logging with PII scrubber; pre-commit and PostToolUse hooks detect PII patterns; log review in security audits | Partial |
| PC-04 | **Data retention violations** -- data kept beyond stated retention period | Medium | Medium | Retention policies defined per data classification; automated retention enforcement (planned); deletion audit trail; no indefinite retention for sensitive or restricted data | Planned |
| PC-05 | **Consent revocation not honored** -- user withdraws consent but data continues to flow or persist | High | Low | Revocation triggers immediate cessation of future processing in affected lane; revocation audit-logged; existing data handled per deletion policy; revocation propagated to all system components | Planned |
| PC-06 | **Re-identification of anonymized data** -- community learning or research data linked back to individuals | Medium | Low | De-identification before community/research lanes; k-anonymity or differential privacy for aggregated patterns; no demographic data in vector store; research lane requires explicit consent and ethics review | Planned |

## 7. Device Physical Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| DP-01 | **Device theft** -- RPi5 unit physically stolen | Medium | Medium | No raw audio or verbatim transcripts stored on device; local SQLite contains only operational cache; device can be remotely deregistered; full-disk encryption (planned) | Planned |
| DP-02 | **SD card extraction** -- attacker removes SD card to read device storage offline | Medium | Medium | Full-disk encryption (planned); API keys and tokens encrypted at rest; no sensitive user data cached locally beyond current session | Planned |
| DP-03 | **Physical tampering** -- hardware modification to intercept audio or inject commands | High | Low | Tamper indicators (planned for pilot hardware); device health monitoring; anomaly detection on command patterns | Planned |
| DP-04 | **USB attack** -- malicious USB device plugged into RPi5 | Medium | Low | USB ports disabled in production config (except required peripherals); USB device allowlisting; minimal OS with no auto-mount | Planned |
| DP-05 | **Unattended device in shared space** -- device left active in environment where unauthorized people can issue commands | Medium | Medium | Wake word required for activation; Tier 2+ actions require confirmation; session timeout; device can be placed in locked mode requiring caregiver unlock | Planned |

## 8. Supply Chain Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| SC-01 | **Dependency vulnerabilities** -- known CVEs in Python, Node.js, or system packages | High | Medium | `pip-audit` for Python dependencies; `npm audit` for Node.js; Dependabot or equivalent for automated alerts; license and CVE check in CI pipeline | Partial |
| SC-02 | **Malicious package injection** -- typosquatting or compromised package in dependency tree | High | Low | Pinned dependency versions; hash verification; minimal dependency policy (`[DM]` rule); review of new dependency additions | Partial |
| SC-03 | **Compromised OS image** -- malicious RPi5 OS image distributed to pilot participants | High | Low | Official Raspberry Pi OS base; documented image build process; image checksums published; signed update mechanism (planned) | Planned |
| SC-04 | **Malicious OTA update** -- attacker pushes compromised firmware or application update | High | Low | Signed updates only; update verification on device before application; rollback capability; update audit logging | Planned |

## 9. Availability Threats

| ID | Threat | Impact | Likelihood | Mitigations | Status |
|----|--------|--------|------------|-------------|--------|
| AV-01 | **Cloud outage** -- STT/LLM/TTS providers unavailable | High | Medium | Degraded mode on device: pre-cached responses for common intents; local phrase bank; clear user indication of degraded state; automatic recovery when cloud returns | Planned |
| AV-02 | **Device failure** -- RPi5 hardware failure, power loss, or OS crash | Medium | Medium | Watchdog process for automatic restart; device health reporting to cloud; spare device provisioning guide for pilot; local state recovery from SQLite cache | Planned |
| AV-03 | **Denial of service** -- attacker floods cloud API or device network interface | Medium | Low | API rate limiting per device and per user; cloud infrastructure autoscaling (within cost constraints); device-side request throttling | Planned |
| AV-04 | **Network connectivity loss** -- Wi-Fi or internet outage at user location | High | Medium | Same degraded mode as cloud outage (AV-01); local action execution for Tier 0 smart-home commands via cached HA state; network status indicator to user | Planned |
| AV-05 | **Database unavailability** -- PostgreSQL or Qdrant outage | Medium | Low | Device continues to operate with cached context; cloud services degrade gracefully (no new consent changes, no community learning); automatic reconnection and sync | Planned |

---

## Risk Summary Matrix

| Category | Critical Threats | Highest Impact | Primary Mitigation Strategy |
|----------|-----------------|----------------|----------------------------|
| Audio/Voice | AV-01, AV-04 | Privacy violation | Wake word gating, no audio retention, TLS |
| Cloud Transport | CT-01, CT-02 | Data breach | TLS 1.3, secrets management, key rotation |
| Data at Rest | DR-02, DR-05 | Data breach, PII exposure | Encryption, PII filtering, bounded retention |
| Identity & Access | IA-01, IA-03 | Unauthorized access | Role enforcement, short-lived tokens, audit |
| Smart-Home | SH-01, SH-03 | Physical safety | Risk tier enforcement, entity allowlists |
| Privacy & Consent | PC-01, PC-02 | Dignity violation | Consent lane enforcement, paraphrase-only |
| Device Physical | DP-01, DP-02 | Data exposure | Disk encryption, minimal local storage |
| Supply Chain | SC-01, SC-04 | System compromise | Dependency auditing, signed updates |
| Availability | AV-01, AV-04 | Loss of assistive function | Degraded mode, local fallbacks |

## Assumptions

1. The user's home network is assumed to be semi-trusted (WPA2/WPA3 Wi-Fi).
2. Cloud providers are assumed to honor their data processing agreements.
3. Caregivers and guardians are assumed to act in the user's interest (but the system still enforces role boundaries).
4. The device operates in a domestic environment, not a clinical or institutional setting.
5. Pilot scale is 10-20 units; threat model will be revisited before broader deployment.

## Review Schedule

This threat model should be reviewed:

- Before each phase transition (Phase 0 -> 1, etc.)
- After any security incident
- When new components or integrations are added
- At minimum every 6 months during active development

---

*This document is part of the Disability-Assist governance framework. For the complete project specification, see [PRD-00-Index.md](../PRD-00-Index.md). For privacy and consent details, see [PRD-11-Privacy-Security-and-Ethics.md](../PRD-11-Privacy-Security-and-Ethics.md).*
