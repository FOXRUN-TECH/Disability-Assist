# .claude Configuration - Claude Code Context

## Mandatory Rules -- Claude MUST Follow These

1. **Do NOT run full test suites** (`pytest`, `pytest tests/`) unless the user explicitly asks. Targeted single-file tests are OK when debugging a specific change.
2. **Do NOT auto-update documentation** (`CLAUDE.md`, `README.md`, `docs/roadmap.md`) unless the user explicitly asks. The pre-commit hook will catch missing updates at commit time.
3. **No hardcoded values** -- all configuration must live in config modules. All code-level constants must use `typing.Final` in dedicated constants modules.
4. **CI must pass after every push.** After every `git push`, verify the GitHub Actions CI pipeline completes successfully:
   - Wait ~30s, then run `gh run list --limit 1` to check status
   - If `in_progress`, wait and re-check until complete
   - If `failure`, run `gh run view <run-id> --log-failed` to diagnose
   - Fix all failures, commit, and push again
   - The PostToolUse hook `check-ci-after-push.py` will remind you after every push

## Code Quality Standards (Mandatory)

5. **Google-style docstrings required** on all modules, classes, and public functions. Enforced by Ruff D rules. Format:
   ```python
   def func(arg: str) -> int:
       """Short summary line.

       Args:
           arg: Description of the argument.

       Returns:
           Description of the return value.

       Raises:
           ValueError: When arg is invalid.
       """
   ```
6. **No magic numbers or hardcoded strings** -- all constants must use `typing.Final` in dedicated constants modules. Enforced by `check-magic-numbers.py` hook.
7. **Custom exceptions required** -- all domain errors must subclass `AssistError`. Map to appropriate HTTP status codes in route handlers.
8. **Refactoring standards** -- no code duplication across files. Extract shared logic into utilities. Validate all external inputs at API boundaries.
9. **Conventional commits required** [CC] -- All commit messages must follow `type(scope): description`. Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `ci`.
10. **File-scoped commands first** [FC] -- ALWAYS use file-scoped lint/test/type-check commands during development. Only run project-wide commands when the user explicitly asks or as final pre-PR check.
11. **No mock drivers or stub implementations** in production code. The PostToolUse hook `check-no-mock.py` warns about mock patterns. Suppress with `# mock-ok`.
12. **Privacy-by-default** -- all new code paths must document consent lane, data classification, and retention policy. Enforced by `check-consent-lanes.py` and `check-privacy-patterns.py` hooks.

## Rule Hierarchy and Traceability Tags

Reference tags in commit messages and code comments: `[SecF] Added Pydantic validation` or `[PV] Consent lane annotation`.

### Critical Rules (Never Violate)

- **[SecF] Security First**: All inputs validated (Pydantic backend, Zod mobile). No secrets in code. Encryption for PII. No `eval()`, `exec()`, `subprocess.run(shell=True)` with user input.
- **[QG] Quality Gate**: Never commit without passing quality checks.
- **[PV] Privacy**: No PII in logs. No raw audio retained without consent. Minimum disclosure for caregivers. User data deletable on demand.
- **[DIG] Dignity**: No patronizing language. No clinical terminology as if diagnosing. Choice-based prompts. No "personality" -- use "assistive profile".
- **[CON] Consent**: Every data flow must identify which consent lane it belongs to. Optional lanes require explicit opt-in checks. Revocation must be immediate.
- **[LIC] License**: No GPL production dependencies. MIT/Apache/BSD preferred.

### Important Rules (Follow Unless Justified)

- **[RT] Risk Tier**: All actions must carry a documented risk tier (0-3). Tier 0-1 execute freely, Tier 2 requires confirmation, Tier 3 blocked.
- **[SF] Simplicity First**: Choose simplest solution. Complex patterns require justification.
- **[RP] Readability Priority**: Code understandable by humans AND future AI agents.
- **[DM] Dependency Minimalism**: No new libraries without explicit need and license check.
- **[TS] Type Safety**: mypy strict (Python) + TypeScript strict (React Native). Return types on all public functions.

### Preferences (Default Behavior)

- **[FC] File-Scoped Commands**: ALWAYS prefer file-scoped over project-wide checks during development.
- **[TF] Tests First**: When fixing bugs, write a failing test first, then fix.
- **[CC] Conventional Commits**: `type(scope): description` format on all commits.

## Security Checklist for AI-Generated Code [SecF]

Before accepting any code that handles user data, verify:

- [ ] All user inputs validated with Pydantic (backend) or Zod (mobile)
- [ ] No `eval()`, `exec()`, `Function()` with user-influenced input (CWE-94)
- [ ] No `subprocess.run(..., shell=True)` with user input (CWE-78)
- [ ] No SQL string concatenation -- parameterized queries only (CWE-89)
- [ ] No secrets, API keys, or credentials in code (CWE-798)
- [ ] Sensitive data encrypted before disk write (CWE-312)
- [ ] Authentication checked on all protected endpoints (CWE-306)
- [ ] Error messages do not leak internal details (CWE-209)
- [ ] No personal data in log output
- [ ] Dependencies verified for known CVEs
- [ ] Voice transcripts: max length enforced, control characters stripped
- [ ] Caregiver paraphrases: never expose raw transcript
- [ ] Consent lane verified for all data flows
- [ ] Risk tier assigned for all action execution paths
- [ ] No medication, purchase, emergency, or clinical logic

## Privacy Checklist [PV][CON]

- [ ] Data classified (public, internal, sensitive, restricted)
- [ ] Consent lane identified (core-cloud, caregiver-access, cloud-sync, community-learning, research, audio-research)
- [ ] Retention policy documented (bounded, not indefinite)
- [ ] Minimum disclosure applied (paraphrase over verbatim)
- [ ] No raw audio retained by default
- [ ] No location tracking
- [ ] Least-privilege role access enforced
- [ ] Guardian/substitute-decision-maker flow supported where needed
- [ ] Revocation path exists (consent withdrawal changes future processing)
- [ ] Deletion request path exists (trackable, auditable)
- [ ] De-identification method documented for any research/community data

## Dignity Language Review [DIG]

Guidelines for code, comments, logs, user-facing text, and commit messages:

- Never use clinical terminology as if diagnosing
- Never patronizing phrasing ("good job", "well done" for adults)
- Choice-based prompts, not leading questions
- Clarification prompts must be short and not condescending
- Deterministic mode for autistic users in strict mode
- No "personality" language -- use "assistive profile" instead
- No simulation of therapy, invention of memories, fabrication of caregiver communications

## Input Validation Patterns [SecF][TS]

**Python (Pydantic):** All API request/response models MUST use Pydantic `BaseModel` with field validators:

- Strings: `constr(min_length=, max_length=)` with regex pattern for structured data
- Numbers: `conint(ge=, le=)` or `confloat()` with range validation
- URLs: HTTPS only in production, block private IP ranges (SSRF protection)
- File paths: reject path traversal (`..`), sanitize before use
- Voice transcripts: max 500 chars, strip control characters
- Consent tokens: strict format validation
- Risk tier values: enum validation (0-3 only)

**React Native (Zod):** All mobile inputs MUST use Zod schemas:

- `z.string().min().max()` with `.regex()` for structured data
- `z.number().int().min().max()` for numeric ranges
- Always `z.object().strict()` to reject unknown fields

## Coverage Targets

| Area | Target | Notes |
|------|--------|-------|
| Policy/safety layer | 95% | Risk tier enforcement, hard constraints |
| Consent flows | 90% | Lane validation, revocation |
| Cloud API integrations | 80% | STT, LLM, TTS clients |
| Device runtime | 80% | Audio capture, action router |
| React Native (mobile) | 70% | Caregiver app (Phase 4+) |
| Infrastructure | 60% | Deployment, provisioning |

## Test Naming Convention [TF]

Use behavior-driven names describing WHAT the code does:

- GOOD: `test_blocks_purchase_action_at_tier_3`
- GOOD: `test_paraphrases_transcript_for_caregiver_feed`
- GOOD: `test_revokes_consent_within_60_seconds`
- BAD: `test_action_router`
- BAD: `test_validator`

## Safety and Permissions

### Allowed Without Asking

- Read files, list directories, search codebase
- Lint, type check, format single files
- Run single unit test file
- View git history, diffs, logs, blame
- Create feature branches from `main`
- Commit to feature branches
- Create pull requests to `main`
- Install dev dependencies already listed in `pyproject.toml` / `package.json`

### Requires User Approval

- Installing NEW packages not in `pyproject.toml` / `package.json`
- Modifying config files (`pyproject.toml`, `tsconfig.json`)
- Running full project build or full test suite
- Force pushing (use `--force-with-lease` only)
- Pushing directly to `main`
- Deleting files or directories
- Modifying encryption, authentication, or authorization logic
- Changes to CI/CD pipeline (`.github/workflows/`)
- Adding dependencies with non-MIT/Apache/BSD licenses
- **Any changes to consent flows** [CON]
- **Any changes to risk tier definitions** [RT]
- **Any changes to hard constraints** (no purchases, no medication, no emergency, no clinical)

## Trust Spectrum

Apply appropriate scrutiny based on code criticality:

| Code Area | Trust Level | Review Required |
|-----------|------------|-----------------|
| Consent/privacy/encryption | Very Low | Human review + privacy audit + security audit |
| Risk tier enforcement | Low | Human review + full test coverage |
| Voice/audio processing | Medium-low | Privacy review + unit tests |
| Cloud API integrations | Medium | Integration tests + review |
| Caregiver app UI | Medium | Accessibility review + tests |
| Documentation/config | High | Quick review |

## Claude Code Hooks

### PostToolUse: lint-python.py
Runs after Write/Edit on `.py` files. Auto-lints with Ruff and type-checks with mypy. Exit 0 = clean, exit 2 = issues. Timeout: 30s.

### PostToolUse: check-magic-numbers.py
Runs after Write/Edit on `.py` files. Detects numeric literals needing extraction. Suppress with `# magic-ok`. Timeout: 10s.

### PostToolUse: check-line-endings.py
Runs after Write/Edit on text files. Auto-fixes to LF (or CRLF for `.bat`/`.cmd`/`.ps1`). Timeout: 10s.

### PostToolUse: check-no-mock.py
Runs after Write/Edit on `.py`/`.ts`/`.tsx` files. Warns about mock/stub patterns. Suppress with `# mock-ok`. Timeout: 10s.

### PostToolUse: check-phase-scope.py
Runs after Bash calls containing `git add`. Warns about files outside active phase scope. Timeout: 10s.

### PostToolUse: remind-doc-update.py
Runs after Write/Edit on source files. Non-blocking reminder about docs. Timeout: 5s.

### PostToolUse: check-privacy-patterns.py
Runs after Write/Edit on `.py`/`.ts`/`.tsx` files. Scans for PII in logs, raw transcript exposure, audio retention. Suppress with `# pii-ok`. Timeout: 10s.

### PostToolUse: check-consent-lanes.py
Runs after Write/Edit on `.py` files in `cloud/`, `device/`, `policy/`. Warns about data-handling functions without consent lane annotation (`# consent-lane: <lane>`). Timeout: 10s.

### PostToolUse: sync-versions.py
Runs after Write/Edit on version files. Syncs from `pyproject.toml` to all managed files. Timeout: 10s.

### PostToolUse: check-ci-after-push.py
Runs after Bash calls containing `git push`. Reminds to verify CI. Timeout: 5s.

### PostToolUse: remind-plan-update.py
Runs after Bash calls containing `git commit`. Reminds to run `/phase-complete`. Timeout: 5s.

### PostToolUse: remind-device-route.py
Runs after Bash calls with network errors. Reminds to fix RPi5 default route. Timeout: 5s.

### Pre-commit Hooks

| Hook | Behavior | Bypass |
|------|----------|--------|
| `check-line-endings-precommit.py` | Auto-fix + re-stage, block for review | `--no-verify` |
| `check-magic-numbers-precommit.py` | Block commits with magic numbers | `# magic-ok` or `--no-verify` |
| `check-no-mock-precommit.py` | Block mock patterns in production code | `# mock-ok` or `--no-verify` |
| `check-doc-updates-precommit.py` | Block if source changed without docs | `--no-verify` |
| `check-version-sync-precommit.py` | Block version mismatches | `--no-verify` |
| `check-privacy-patterns-precommit.py` | Block PII violations | `# pii-ok` or `--no-verify` |

## Testing Hooks Manually

```bash
echo '{"tool_input":{"file_path":"device/main.py"},"tool_name":"Write"}' | python .claude/hooks/lint-python.py
echo $?

echo '{"tool_input":{"file_path":"cloud/api/routes/voice.py"},"tool_name":"Edit"}' | python .claude/hooks/check-privacy-patterns.py
echo $?

echo '{"tool_input":{"command":"git push origin main"},"tool_name":"Bash"}' | python .claude/hooks/check-ci-after-push.py
echo $?
```

## Quality Toolchain

| Tool | Purpose | When It Runs |
|------|---------|--------------|
| **Ruff (check)** | Linting (E/W/F/I/B/C4/UP/D/TRY/SIM/PIE/RUF) | Hook, pre-commit, CI |
| **Ruff (format)** | Code formatting | Hook, pre-commit, CI |
| **Mypy** | Static type checking | Hook, pre-commit, CI |
| **Bandit** | Python SAST (security vulnerabilities) | `/security-check`, `/quality`, CI |
| **pip-audit** | Python dependency CVE scanner | `/security-check`, `/quality`, CI |
| **detect-secrets** | Secrets detection in code | Pre-commit, `/security-check` |
| **Pre-commit** | Git hook runner | On `git commit` |

## Quick Reference

| Task | Location |
|------|----------|
| Project context | `/CLAUDE.md` |
| Product requirements index | `docs/PRD-00-Index.md` |
| System architecture | `docs/PRD-03-System-Architecture.md` |
| Privacy and ethics | `docs/PRD-11-Privacy-Security-and-Ethics.md` |
| Consent model | `docs/PRD-11-Privacy-Security-and-Ethics.md` Section 5 |
| Risk tiers | `docs/PRD-05-LLM-Intent-Engine.md` Section 4 |
| Caregiver model | `docs/PRD-09-Caregiver-Communication-Bridge.md` |
| Hardware reference | `docs/PRD-10-Hardware-Reference-Design.md` |
| Roadmap | `docs/roadmap.md` |
| Add slash command | `.claude/commands/*.md` + `SKILLS.md` |
| Add tool permission | `.claude/settings.json` |
| Modify hooks | `.claude/hooks/` + `settings.json` |

## Directory Structure

```text
.claude/
├── CLAUDE.md              # This file (configuration guidance + rules)
├── AGENTS.md              # Agent instructions (abbreviated rules)
├── SKILLS.md              # Slash command reference
├── settings.json          # Shared permissions + hooks
├── commands/
│   ├── quality.md            # /quality -- full quality gate
│   ├── commit.md             # /commit -- conventional commit + push
│   ├── pr.md                 # /pr -- quality gate + GitHub PR
│   ├── security-check.md     # /security-check -- Bandit, pip-audit, detect-secrets
│   ├── privacy-audit.md      # /privacy-audit -- PII scan, consent verification
│   ├── review.md             # /review -- self-review checklist
│   ├── phase-complete.md     # /phase-complete -- validate phase completion
│   ├── new-api.md            # /new-api -- scaffold Python API endpoint
│   ├── new-component.md      # /new-component -- scaffold React Native component
│   └── device-setup.md       # /device-setup -- RPi5 connectivity + provisioning
└── hooks/
    ├── _constants.py         # Shared constants for all hooks
    ├── _magic_numbers.py     # Shared magic-number scanning logic
    ├── _no_mock.py           # Shared mock-pattern scanning logic
    ├── _phase_config.py      # Phase-to-file mapping for scope enforcement
    ├── _privacy_patterns.py  # Shared PII/consent scanning logic
    ├── lint-python.py        # PostToolUse: auto-lint Python on Write/Edit
    ├── check-magic-numbers.py # PostToolUse: magic number detection
    ├── check-line-endings.py # PostToolUse: line ending enforcement
    ├── check-no-mock.py      # PostToolUse: mock/stub pattern warning
    ├── check-phase-scope.py  # PostToolUse: phase scope warning on git add
    ├── remind-doc-update.py  # PostToolUse: doc update reminder
    ├── check-privacy-patterns.py  # PostToolUse: PII exposure detection
    ├── check-consent-lanes.py     # PostToolUse: consent lane annotation check
    ├── sync-versions.py      # PostToolUse: version sync across files
    ├── check-ci-after-push.py     # PostToolUse: CI verification reminder
    ├── remind-plan-update.py      # PostToolUse: roadmap update reminder
    ├── remind-device-route.py     # PostToolUse: RPi5 networking reminder
    ├── check-line-endings-precommit.py    # Pre-commit: line ending enforcement
    ├── check-magic-numbers-precommit.py   # Pre-commit: magic number blocking
    ├── check-no-mock-precommit.py         # Pre-commit: mock pattern blocking
    ├── check-doc-updates-precommit.py     # Pre-commit: doc update enforcement
    ├── check-version-sync-precommit.py    # Pre-commit: version mismatch blocking
    └── check-privacy-patterns-precommit.py # Pre-commit: PII violation blocking
```

## File Loading Order

Claude Code automatically loads configuration in this order:

1. **`/CLAUDE.md`** (project root) - Main project context
2. **`.claude/settings.json`** - Shared tool permissions (version controlled)
3. **`.claude/settings.local.json`** - Local overrides (gitignored)

---

This file provides guidance for maintaining Claude Code configuration in this directory.
For project context see [CLAUDE.md](../CLAUDE.md) (root). For detailed docs see [docs/](../docs/).
