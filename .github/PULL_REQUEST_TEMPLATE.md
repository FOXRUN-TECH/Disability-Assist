## Summary

<!-- 1-3 bullet points describing what this PR does -->

## Related Issues

<!-- Link issues: Closes #123, Fixes #456 -->

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] CI/CD or infrastructure change

## Phase

<!-- Which roadmap phase does this PR belong to? -->

- [ ] Phase 0 - Governance
- [ ] Phase 1 - Core Speech
- [ ] Phase 2 - Smart-Home
- [ ] Phase 3 - Personalization
- [ ] Phase 4 - Caregiver App
- [ ] Phase 5 - Consent Controls
- [ ] Phase 6 - Pilot Ops
- [ ] Phase 7 - Pilot Launch
- [ ] Phase 8 - Shared Intelligence
- [ ] Phase 9 - Research

## Quality Checklist

- [ ] `ruff check` passes on all modified files
- [ ] `ruff format --check` passes on all modified files
- [ ] `mypy` passes on all modified files
- [ ] Tests pass for modified modules
- [ ] No new magic numbers (use `typing.Final` constants)
- [ ] No mock/stub patterns in production code

## Privacy and Safety Checklist

<!-- Check all that apply -->

- [ ] No PII in logs or error messages
- [ ] Consent lane documented for new data flows (`# consent-lane: <lane>`)
- [ ] Risk tier assigned for new action paths
- [ ] No raw transcript exposure (paraphrase only for caregivers)
- [ ] No hard constraint violations (purchases, medication, emergency, clinical)
- [ ] N/A - This PR does not touch data flows or action paths

## Dignity Review

- [ ] No patronizing language in user-facing text, logs, or comments
- [ ] No clinical terminology used as if diagnosing
- [ ] Choice-based prompts (not leading questions)
- [ ] N/A - This PR does not include user-facing text

## Test Plan

<!-- How was this tested? What should reviewers verify? -->
