# PRD-12 · Open Source Contribution Guide

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Define how external contributors can improve the project without weakening safety, privacy, accessibility, or maintainability.

## 2. Contribution Priorities
High-value contributions include:
- accessibility eval sets;
- hardware refinements;
- prompt and policy improvements;
- privacy/security hardening;
- documentation based on lived experience;
- multilingual planning groundwork;
- integration adapters through approved abstractions.

## 3. Required Standards
All contributions must:
- align with the PRD set;
- preserve dignity-focused language;
- avoid introducing medical or legal claims without approval;
- include tests where behaviour changes;
- avoid hardcoding secrets or unsafe defaults.

## 4. Restricted Change Areas
Maintainer review is mandatory for:
- consent flows;
- researcher export logic;
- caregiver permissions;
- cryptography / secrets;
- any feature that could imply medical use;
- any feature involving minors or institutional deployment.

## 5. Community Data Contributions
Speech, vocabulary, and interaction data contributions must:
- be explicitly consented;
- be documented by dataset card;
- include provenance and removal workflow;
- avoid publishing identifiable personal content.

## 6. Governance
The repository should maintain:
- code of conduct;
- misuse policy;
- security disclosure path;
- decision log for major governance changes.
