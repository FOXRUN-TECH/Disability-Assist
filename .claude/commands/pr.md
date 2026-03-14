# PR Creation Command

Run full quality gate, push to remote, and create a GitHub pull request with security and privacy checklists. [QG][CC]

## Usage

```text
/pr
```

## What It Does

1. **Run full quality gate** (`/quality`) -- all checks must pass
2. **Push to remote**: `git push -u origin <current-branch>`
3. **Create PR** via `gh pr create` with structured template

## PR Template

```bash
gh pr create --title "type(scope): short description" --body "$(cat <<'EOF'
## Summary

- Bullet point 1
- Bullet point 2

## Rule Tags Applied

[SecF] [QG] [PV] [DIG] [CON] [CC] (list tags relevant to this PR)

## Security Checklist

- [ ] All user inputs validated (Pydantic/Zod)
- [ ] No eval/exec/Function with user input
- [ ] No subprocess(shell=True) with user input
- [ ] No secrets or API keys in code
- [ ] PII encrypted before disk write
- [ ] Error messages don't leak internals
- [ ] No PII in logs
- [ ] Dependencies verified for CVEs

## Privacy Checklist

- [ ] Consent lane identified for all data flows
- [ ] Data classification documented (public/internal/sensitive/restricted)
- [ ] Retention policy documented (bounded, not indefinite)
- [ ] Minimum disclosure applied (paraphrase over verbatim for caregivers)
- [ ] No raw audio retained by default
- [ ] Role-based access enforced on caregiver endpoints

## Dignity Review

- [ ] No clinical terminology used as if diagnosing
- [ ] No patronizing language in user-facing text
- [ ] Choice-based prompts, not leading questions
- [ ] Clarification prompts short and respectful

## Test Plan

- [ ] File-scoped tests pass on all changed files
- [ ] Integration tests pass (if applicable)
- [ ] Privacy audit clean (`/privacy-audit`)

## Notes

Any additional context, trade-offs, or follow-up items.

---
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## PR Title Format [CC]

Follow conventional commit format: `type(scope): description`

- `feat(voice): add cloud STT integration`
- `fix(consent): correct revocation flow`
- `refactor(policy): extract risk tier validation`

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Current branch pushed to remote
- All quality gate checks passing

## After PR Creation

1. Share the PR URL with the user
2. Wait for CI checks to run on the PR
3. Check status: `gh pr checks`

## Related Commands

- `/quality` -- Full quality gate (run before PR)
- `/commit` -- Commit with conventional message
- `/review` -- Self-review before PR
- `/privacy-audit` -- Privacy verification
- `/security-check` -- Security scanning
