# User Role Matrix

**Project:** Disability-Assist
**Version:** 0.0.1
**Status:** Phase 0 Draft
**Authority:** PRD-09, PRD-11 Section 5

## Decision Framework

Dignity > Privacy > Accuracy > Simplicity

## Governing Principle

The caregiver communication bridge exists to clarify communication, not to monitor
private behaviour. All role definitions serve assistive goals, never surveillance.

---

## Role Summary

| Role | Description | Home Mode | Assisted-Home Mode |
|------|-------------|-----------|-------------------|
| User | The person being assisted | Full self-access | Full self-access where capacity allows |
| Family Caregiver | Family member providing care | Broad config + alerts + summaries | Same, but for assigned user(s) only |
| Professional Caregiver | Paid care staff | N/A | Task-oriented, assigned residents only, shift-scoped |
| Guardian / SDM | Substitute decision-maker | Elevated consent + access admin | Same |
| Administrator | Facility or system admin | Device management | Operational metadata, NOT blanket content |

---

## Role 1: User

The person being assisted by the system. The system exists to serve this person.

### Permissions

| Capability | Access |
|---|---|
| Use voice input and receive voice output | Full |
| View own intent history and action log | Full |
| Manage own vocabulary, routines, preferences | Full |
| Control consent lanes (grant/revoke) | Full (where capacity allows) |
| Manage own caregiver roster | Full (where capacity allows) |
| Lock entries from caregiver editing | Full |
| Request data export | Full |
| Request data deletion | Full |
| View own raw transcripts | Full |
| Access smart-home controls | Per risk tier (0-1 free, 2 confirm, 3 blocked) |

### Hidden by Default

- Nothing is hidden from the user about their own data.
- System internals (confidence scores, model metadata) are not displayed in the
  primary interface but are accessible on request.

### Audit Requirements

- User's own actions are logged for system integrity but are not exposed to
  caregivers unless the user opts into caregiver access (Lane 2).
- User access to their own data is not treated as a reviewable event.

### Capacity Considerations

- **Self-directed adults:** Full autonomy over all settings and consent.
- **Adults with fluctuating capacity:** The system supports a capacity flag managed
  by the guardian (not by the system itself). When the flag indicates reduced
  capacity, the guardian's settings take precedence. When the flag indicates
  capacity, the user's own choices take precedence. The system never determines
  capacity -- it only respects the externally set flag.
- **Minors:** Guardian consent required for all lanes. The minor's own preferences
  are respected where developmentally appropriate (e.g., vocabulary choices,
  routine preferences) but consent decisions are the guardian's.
- **Regaining capacity:** If a user regains capacity (flag changed by guardian or
  legal process), they may review and modify all settings, including overriding
  previous guardian decisions on optional lanes.

### Anti-Surveillance Safeguards

- The user's raw audio is never retained without Lane 6 consent.
- The user's raw transcripts are never shared with caregivers by default.
- The system does not track location.
- The system does not report on private behaviour unrelated to assistance goals.

---

## Role 2: Family Caregiver

A family member or close person providing care. Added by the user or guardian.

### Permissions

| Capability | Home Mode | Assisted-Home Mode |
|---|---|---|
| View intent summaries (paraphrased) | Yes, for their user | Yes, for assigned user(s) only |
| Receive escalation alerts | Yes | Yes |
| Configure device settings | Yes (broad) | Yes, for assigned user(s) |
| Manage vocabulary and routines | Yes (unless user-locked) | Yes, for assigned user(s) |
| View action results and status | Yes | Yes |
| Add/remove other caregivers | No (user/guardian only) | No |
| Modify consent lanes | No (user/guardian only) | No |
| View raw transcripts | No (see below) | No |
| Access audit logs | Own access log only | Own access log only |
| Export user data | No (user/guardian only) | No |

### Hidden by Default

- **Raw transcripts:** Always hidden. Access requires separate elevated permission
  granted by the user or guardian, and every access is individually audit-logged
  with justification.
- **Confidence scores and model internals:** Hidden.
- **Other caregivers' access logs:** Hidden (each caregiver sees only their own).
- **Consent lane details:** Caregiver can see which lanes are active (to understand
  what features are available) but cannot modify them.
- **Other users' data:** In assisted-home mode, a family caregiver sees only their
  assigned user(s), never other residents.

### Audit Requirements

- Every caregiver access event is logged: what was viewed, when, by whom.
- Escalation alert deliveries are logged.
- Configuration changes made by the caregiver are logged with before/after values.
- Audit logs are available to the user (if they have capacity) and the guardian.

### Assignment and Revocation

- **Assignment:** User or guardian adds the family caregiver by identity, assigning
  the "family caregiver" role and specifying which user(s) they support.
- **Revocation:** User or guardian removes the caregiver at any time. Effect is
  immediate: feed stops, server-side history access removed.
- **Self-removal:** A caregiver may remove themselves from the roster.
- **No auto-assignment:** The system never automatically adds caregivers.

### Anti-Surveillance Safeguards

- Caregivers see paraphrased intent, never raw transcript.
- Caregivers do not see interactions unrelated to assistance (e.g., if the user
  asks the system a private question, the paraphrase must not expose the content
  unless it triggers an escalation).
- The caregiver feed is not a real-time audio monitor. It shows intent summaries
  with inherent latency.
- Caregivers cannot enable audio retention (Lane 6) or research participation
  (Lane 5) on the user's behalf.

---

## Role 3: Professional Caregiver

Paid care staff in a facility or home-care setting. Operates under assisted-home
mode constraints.

### Permissions

| Capability | Assisted-Home Mode |
|---|---|
| View intent summaries for assigned residents | Yes, shift-scoped |
| Receive escalation alerts for assigned residents | Yes, shift-scoped |
| View action results and status | Yes, for assigned residents |
| Contribute handover notes | Yes |
| Configure device settings | Limited (facility-approved settings only) |
| Manage vocabulary and routines | Limited (facility-approved scope) |
| View raw transcripts | No |
| Modify consent lanes | No |
| Add/remove caregivers | No |
| Access audit logs | Own access log only |
| View other residents' data | No (assigned residents only) |
| Access data outside shift window | No |

### Hidden by Default

- **Raw transcripts:** Always hidden. No elevated access path for professional
  caregivers (only guardians and users can grant raw transcript access, and only
  to specific individuals with justification).
- **Data from other residents:** Strictly invisible. The system enforces assignment
  boundaries at the data layer, not just the UI layer.
- **Historical data outside shift:** Professional caregivers see only current-shift
  and recent-handover data. Historical interaction logs beyond the handover window
  are not accessible.
- **Consent configuration:** Visible as feature availability only (e.g., "cloud
  sync is enabled") but not modifiable.
- **Guardian contact details:** Not visible unless the facility administrator has
  configured it for escalation purposes.

### Audit Requirements

- Every access event is logged with the professional's identity, shift identifier,
  and assigned resident.
- Access outside assigned residents triggers an alert (should not be possible, but
  defense in depth).
- Handover note creation is logged.
- All audit logs are available to the facility administrator and the guardian.

### Assignment and Revocation

- **Assignment:** Facility administrator assigns professional caregivers to
  residents, specifying shift schedule and access scope. Assignment must be
  ratified by the user's guardian or the user (if they have capacity).
- **Shift scoping:** Access is bounded by shift start/end times. Outside shift
  hours, the professional caregiver's access is suspended automatically.
- **Revocation:** Facility administrator or guardian can revoke at any time.
  Effect is immediate.
- **Offboarding:** When a professional caregiver leaves the facility, all
  assignments must be revoked as part of the offboarding process.

### Handover Support

- Professional caregivers can create structured handover notes for the next shift.
- Handover notes contain: unresolved requests, pending actions, relevant context.
- Handover notes must not contain raw transcripts or unnecessary detail about
  private interactions.
- Handover notes are visible to the incoming shift's assigned caregiver(s) and
  to the guardian.

### Anti-Surveillance Safeguards

- Task-oriented access only: the professional sees what they need to assist,
  nothing more.
- No access to interaction content unrelated to care tasks.
- No ability to install monitoring, enable audio retention, or change consent.
- Shift-scoped access prevents accumulation of longitudinal behavioural data
  by individual staff members.
- The system does not provide "staff performance" metrics based on resident
  interaction data.

---

## Role 4: Guardian / Substitute Decision-Maker (SDM)

A person with legal authority to make decisions on behalf of the user. This
includes legal guardians, holders of power of attorney, parents of minors, and
other lawfully designated representatives.

### Permissions

| Capability | Home Mode | Assisted-Home Mode |
|---|---|---|
| All Family Caregiver permissions | Yes | Yes |
| Grant/revoke consent for all lanes | Yes | Yes |
| Add/remove caregivers (family and professional) | Yes | Yes (with facility admin for professionals) |
| Set capacity flag | Yes | Yes |
| View elevated data (raw transcripts) | Yes, audit-logged | Yes, audit-logged |
| Request data export | Yes | Yes |
| Request data deletion | Yes | Yes |
| Override user-locked entries | Yes, with justification logged | Yes, with justification logged |
| View all audit logs for their user | Yes | Yes |
| Ratify professional caregiver assignments | N/A | Yes |

### Hidden by Default

- **Raw transcripts:** Available but not displayed by default. Guardian must
  explicitly navigate to raw transcript view; each access is audit-logged.
- **Other users' data:** Guardian sees only their assigned user(s).
- **System internals:** Model confidence scores, infrastructure metrics, etc.
  are hidden unless specifically requested.
- **Facility operational data:** In assisted-home mode, the guardian sees their
  user's data only, not facility-wide operational information.

### Audit Requirements

- All guardian actions are logged: consent changes, caregiver roster changes,
  capacity flag changes, raw transcript access, data export/deletion requests.
- Audit logs include the guardian's identity and the legal authority basis.
- Audit logs for guardian actions are retained for the longer of: 7 years or the
  applicable regulatory minimum.
- A secondary audit trail (accessible to the facility administrator or a
  designated oversight body) records guardian actions for accountability.

### Assignment and Revocation

- **Assignment:** Guardian role is configured during setup with documentation of
  legal authority (type of authority, jurisdiction, date granted).
- **Multiple guardians:** The system supports multiple guardians for a single user
  (e.g., co-guardians, separated parents). Conflict resolution policy must be
  configured at setup (e.g., either guardian can revoke, both must agree to
  enable).
- **Authority changes:** Guardian assignment can be updated when legal authority
  changes (e.g., guardianship revoked by court, child reaches age of majority).
  The previous guardian's access is immediately revoked.
- **No self-assignment:** A person cannot assign themselves as guardian through
  the system. Assignment requires an administrator or existing guardian action
  plus documentation of legal basis.

### Capacity Considerations

- The guardian manages the capacity flag, which determines whether the user or
  the guardian has precedence for consent and configuration decisions.
- **Fluctuating capacity model:** The capacity flag can be changed over time.
  When set to "full capacity," the user's own decisions take precedence. When
  set to "reduced capacity," the guardian's decisions take precedence.
- The system does not assess capacity. It only enforces the externally set flag.
- Changes to the capacity flag are audit-logged with justification.

### Anti-Surveillance Safeguards

- Guardian access exists to support decision-making, not to monitor behaviour.
- Raw transcript access requires deliberate action and is audit-logged.
- The system does not provide guardian-facing dashboards that aggregate
  behavioural patterns over time (e.g., "activity levels," "social engagement
  scores"). The data shown is interaction-specific.
- Guardians cannot enable covert monitoring. All data flows visible to the
  guardian are also visible to the user (if they have capacity to view them).

---

## Role 5: Administrator

Facility or system administrator responsible for device management and
operational oversight.

### Permissions

| Capability | Home Mode | Assisted-Home Mode |
|---|---|---|
| Device provisioning and management | Yes | Yes |
| System configuration (network, updates, etc.) | Yes | Yes |
| Assign professional caregivers to residents | N/A | Yes (subject to guardian ratification) |
| View operational metadata (uptime, errors, versions) | Yes | Yes |
| View aggregated usage statistics (non-identifying) | N/A | Yes |
| View user interaction content | No | No |
| View raw transcripts | No | No |
| Modify consent lanes | No | No |
| View caregiver feed content | No | No |
| Manage guardian assignments | Yes (with legal documentation) | Yes (with legal documentation) |
| Access audit logs | System-level only | System-level + staff access logs |

### Hidden by Default

- **All user interaction content:** Administrators do not see intent summaries,
  transcripts, vocabulary, routines, or any content produced by the user's
  interaction with the system.
- **Caregiver feed content:** The administrator knows that caregiver access is
  configured but cannot see what flows through it.
- **Consent lane details beyond status:** The administrator can see which lanes
  are active for operational purposes but cannot see consent form contents or
  modify consent.
- **Individual user behavioural data:** The administrator may see aggregate
  statistics (e.g., "15 of 20 devices active") but not individual interaction
  patterns.

### What Administrators CAN See

- Device status: online/offline, software version, last update, error counts.
- Network status and connectivity.
- Professional caregiver assignment roster (who is assigned to whom, shift
  schedules).
- Staff access audit logs (which staff accessed which resident's data, when).
- System error logs (no user content in error logs -- see privacy requirements).
- Consent lane status per user (active/inactive, not details).
- Aggregate usage metrics for capacity planning.

### Audit Requirements

- Administrator actions are logged: device provisioning, staff assignments,
  system configuration changes.
- Administrator audit logs are available to a designated oversight body or
  facility governance.
- Attempts by administrators to access user content (if technically possible
  through system administration) are logged and flagged.

### Assignment and Revocation

- **Home mode:** The device owner or guardian designates an administrator
  (may be themselves for self-managed setups).
- **Assisted-home mode:** The facility designates administrators through a
  documented process. Multiple administrators may be assigned with defined
  scope (e.g., one for device management, another for staff assignments).
- **Revocation:** Administrator access is revoked through the same process
  that granted it. In assisted-home mode, facility governance controls this.
- **Separation of duties:** In assisted-home mode, the administrator role
  should be held by someone who is NOT also a caregiver for the same residents,
  where operationally feasible. This prevents combining operational access
  with content access.

### Anti-Surveillance Safeguards

- The administrator role explicitly does NOT include content access.
  This is a hard boundary, not a default that can be overridden.
- Administrators cannot install monitoring features, enable audio retention,
  or access caregiver feeds.
- The system does not provide administrators with individual behavioural
  analytics.
- Staff access audit logs show access events (who, when, which resident)
  but not the content that was accessed.

---

## Cross-Cutting Requirements

### Raw Transcript Access Policy

Raw transcripts are the most sensitive data type in the system (aside from
raw audio, which is governed by consent Lane 6). Access rules:

| Role | Raw Transcript Access | Conditions |
|---|---|---|
| User | Yes | Own transcripts, always available |
| Family Caregiver | Possible | Only if elevated permission granted by user/guardian; each access audit-logged |
| Professional Caregiver | No | Never available to professional caregivers |
| Guardian / SDM | Yes | Available but not default; each access audit-logged |
| Administrator | No | Never available to administrators |

### Audit Log Architecture

All caregiver and guardian access events are logged in an append-only,
tamper-evident audit trail:

| Field | Description |
|---|---|
| `event_id` | Unique event identifier |
| `timestamp` | UTC timestamp of the event |
| `actor_id` | User ID of the person performing the action |
| `actor_role` | Role at time of action |
| `target_user_id` | User whose data was accessed/modified |
| `action` | What was done (view_summary, view_transcript, change_setting, etc.) |
| `resource` | Specific resource accessed |
| `shift_id` | Shift identifier (professional caregivers only) |
| `justification` | Required for elevated access (raw transcripts, guardian overrides) |

### Role Assignment Lifecycle

```
1. Request    -> Who is requesting, what role, for which user, legal basis
2. Validate   -> Legal documentation check (guardian/SDM), facility approval (professional)
3. Ratify     -> User or guardian confirms (except administrator assigned by facility)
4. Activate   -> Role becomes active, permissions enforced
5. Monitor    -> Ongoing audit logging
6. Revoke     -> Immediate effect, access removed, audit log retained
```

### Capacity Model

The system supports three capacity states, set externally (never by the system):

| State | Who Decides | Effect |
|---|---|---|
| Full capacity | User | User controls all settings and consent |
| Reduced capacity | Guardian | Guardian controls consent and configuration; user retains interaction access |
| Minor | Guardian (parent) | Guardian controls consent; user preferences respected where appropriate |

Transitions between capacity states are audit-logged with the identity of the
person making the change and the stated basis.

### Anti-Surveillance Principles

These principles apply across all roles:

1. **No covert monitoring.** All data collection is disclosed to the user
   (where they have capacity to understand it) and to the guardian.
2. **No behavioural scoring.** The system does not aggregate interaction
   data into behavioural scores, engagement metrics, or compliance ratings.
3. **Assistance-scoped access.** Every access permission is justified by an
   assistance need, not by a monitoring interest.
4. **Minimum disclosure.** Caregivers see the minimum information needed to
   provide effective assistance. Paraphrase over verbatim. Summary over detail.
5. **No reverse inference.** The system does not infer or report on the user's
   emotional state, cognitive state, or health status from interaction patterns.
   It processes communication intent only.
6. **User visibility.** The user (where capacity allows) can see who has
   accessed their data and what they saw.
7. **Time-bounded access.** Professional caregiver access is shift-scoped.
   No role accumulates permanent access without ongoing authorization.
