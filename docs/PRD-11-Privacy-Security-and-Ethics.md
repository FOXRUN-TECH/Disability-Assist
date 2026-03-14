# PRD-11 · Privacy, Security & Governance

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Scope

This project processes sensitive personal data and disability-related interaction data. Privacy, security, and governance are core product requirements, not paperwork.

## 2. Compliance Posture

The project must be designed for compliance readiness in defined launch jurisdictions, beginning with:
- Canada;
- United States;
- EU / EEA;
- United Kingdom.

The project must not claim universal worldwide compliance.

## 3. Product Claim Boundary

The system is positioned as:
- assistive communication;
- accessibility support;
- environmental control;
- caregiver coordination.

It is not positioned in v1/v2 as:
- diagnosis;
- treatment;
- disease monitoring;
- emergency medical response.

## 4. Consent Lanes

Consent must be collected separately for:
1. core cloud operation;
2. caregiver remote access;
3. optional cloud sync of personalization data;
4. de-identified community-learning contribution;
5. de-identified research participation;
6. optional future audio research contribution, if ever enabled.

Refusing optional lanes must not break core local functionality beyond the requested feature itself.

## 5. Role and Capacity Model
The system must support:
- self-directed adults;
- guardian-managed adults;
- minors;
- adults with fluctuating capacity;
- professional staff assignments.

Role assignments and legal authority basis must be auditable.

## 6. Data Minimization Rules
- default to paraphrase over verbatim display;
- no routine raw-audio retention;
- no location tracking unless explicitly added in a later governed feature;
- bounded retention on recent history;
- least-privilege role access.

## 7. Security Controls
- TLS for all cloud traffic;
- encrypted secrets handling;
- audit logs for caregiver access, consent changes, and policy overrides;
- signed updates or equivalent integrity verification;
- incident response process;
- key rotation plan for hosted services.

## 8. Research Governance
Research access must use de-identified data unless a stricter approved protocol exists.
Requirements:
- data use agreement;
- review workflow;
- purpose limitation;
- revocation handling where applicable;
- documented de-identification method;
- re-identification risk review.

## 9. Ethical Rules
The system must not be used for:
- covert surveillance;
- commercial behavioural exploitation;
- manipulative emotional design;
- presenting speculation as confirmed fact.

## 10. Accessibility and Dignity
Privacy controls must not create unusable experiences for the target users. Security must be strong, but the interface must remain understandable for caregivers and, where possible, users themselves.
