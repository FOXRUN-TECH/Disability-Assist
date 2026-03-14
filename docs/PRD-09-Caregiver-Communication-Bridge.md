# PRD-09 · Caregiver Communication Bridge

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Help another person understand what the user is likely trying to communicate without turning the product into a surveillance tool.

## 2. Default Display Model
The caregiver view should show:
- likely intent;
- confidence band;
- suggested follow-up if unresolved;
- action result status.

It should **not** show raw audio or verbatim transcript by default.

## 3. Roles

| Role | Typical Access |
|---|---|
| User | full self-access where capable |
| Family caregiver | broad access, still logged |
| Professional caregiver | task-oriented access only |
| Guardian / substitute decision-maker | elevated access as lawfully configured |
| Facility administrator | operational metadata, not blanket content access |

## 4. Raw Transcript Policy
Raw transcript access:
- off by default;
- separately permissioned;
- audited every time;
- justified by role and setting.

## 5. Escalations
Supported v1 escalations:
- comfort request unresolved;
- repeated failed understanding;
- user requests caregiver;
- routine reminder acknowledgement missing.

Unsupported v1:
- emergency triage automation;
- clinical escalation scoring.

## 6. Assisted-Home Mode
Assisted-home mode must:
- restrict staff visibility to assigned residents;
- expose shift-safe summaries;
- support handover notes without disclosing unnecessary raw content;
- maintain per-access logs.

## 7. Anti-Surveillance Rule
This bridge exists to clarify communication, not to monitor private behaviour unrelated to assistance goals.
