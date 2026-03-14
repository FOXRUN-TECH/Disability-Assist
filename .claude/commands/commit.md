# Commit Command

Run quality gate, enforce phase scope, create a conventional commit, push, and verify CI. [CC][QG][FC]

## Usage

```text
/commit
/commit --phase-end          # End-of-phase commit (enforces doc updates + phase scope)
/commit --skip-quality       # Skip quality gate (emergency only, requires justification)
```

## What It Does

### Step 1: Identify Changes

- `git status` to find modified/untracked files
- `git diff` and `git diff --staged` to review changes
- Read `.claude/hooks/_phase_config.py` to identify `ACTIVE_PHASE`

### Step 2: Phase Scope Check

- Compare staged/modified files against the active phase's allowed paths
  (defined in `.claude/hooks/_phase_config.py` `PHASE_FILE_MAP`)
- If files outside the phase scope are found, warn and ask user to confirm
- If `--phase-end` flag is used, verify ALL phase-specific docs are also staged
  (from `PHASE_COMPLETION_DOCS` in `_phase_config.py`)

### Step 3: Quality Gate (file-scoped) [FC]

Run file-scoped quality checks on EACH modified Python file:

```bash
# For each modified .py file:
python -m ruff check <file>
python -m ruff format --check <file>
python -m mypy <file> --ignore-missing-imports
python -m bandit <file> -ll
```

For each modified React Native file (.ts, .tsx) (Phase 4+):

```bash
cd mobile && npx eslint <file>
```

Run targeted tests for modified modules:

```bash
# If tests/unit/test_<module>.py exists, run it:
python -m pytest tests/unit/test_<module>.py -x --tb=short
```

If ANY check fails:

1. Offer to auto-fix (`ruff check --fix`, `ruff format`)
2. Report remaining issues
3. Do NOT proceed to commit until all checks pass

### Step 4: Stage Files

- Stage specific files by name -- NEVER use `git add -A` or `git add .`
- Never stage files matching: `.env*`, `*credentials*`, `*secret*`, `*consent_key*`, `*.key`, `*.pem`
- If `--phase-end`, also stage the required documentation files for the phase

### Step 5: Generate Conventional Commit [CC]

- Format: `type(scope): description`
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `ci`
- Scope: optional but encouraged (e.g., `feat(voice):`, `fix(consent):`)
- If `--phase-end`, include `Completes phase X` in the commit body

### Step 6: Create Commit

- Create commit with message and Co-Authored-By trailer
- Pre-commit hooks will run (ruff, line endings, magic numbers, PII check)
- If pre-commit fails, fix and retry (do NOT use `--no-verify`)

### Step 7: Push

- Push to `origin` on the current branch (not hardcoded to `main`)

### Step 8: Verify CI [QG]

After pushing, actively verify CI passes:

1. Wait 30 seconds
2. Run `gh run list --limit 1` to get the run ID and status
3. If status is `in_progress`: wait 30s and re-check (max 20 retries / 10 min)
4. If `completed` + `success`: Report success
5. If `completed` + `failure`: Run `gh run view <run-id> --log-failed`, report, offer to fix

## Conventional Commit Examples

```
feat(voice): add cloud STT integration
fix(consent): correct revocation flow for guardian role
refactor(policy): extract risk tier validation
docs: update PRD-11 consent lane definitions
chore: bump dependency versions
test(privacy): add PII detection edge cases
ci: add privacy pattern scan to pipeline
```

## Safety Rules

- Never use `git add -A` or `git add .` (prevents accidental staging)
- Never commit `.env`, credentials, or secrets
- Never stage files matching: `.env*`, `*credentials*`, `*secret*`, `*consent_key*`, `*.key`, `*.pem`
- Push to current branch, not hardcoded `main`

## Related Commands

- `/quality` -- Full quality gate (pre-PR)
- `/pr` -- Full PR creation workflow
- `/phase-complete <id>` -- Validate and record phase completion
- `/review` -- Self-review before committing
