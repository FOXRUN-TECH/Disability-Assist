# Quality Gate Command

Run the full project quality gate. [QG]

## Usage

```text
/quality
```

## What It Does

Run each check in order. Report pass/fail for each step. Stop on first failure unless otherwise noted.

### Python Quality Gate

```bash
# 1. Lint (includes import sorting via I rule)
python -m ruff check device/ cloud/ policy/

# 2. Format check (CI mode, no modifications)
python -m ruff format --check device/ cloud/ policy/

# 3. Type checking
python -m mypy device/ cloud/ policy/ --ignore-missing-imports

# 4. Security scan (medium+ severity) [SecF]
python -m bandit -r device/ cloud/ policy/ -ll

# 5. Dependency CVE scan [SecF]
python -m pip_audit

# 6. Tests (fail fast)
python -m pytest tests/ -x --tb=short
```

### React Native Quality Gate (Phase 4+, when `mobile/` exists)

```bash
# 7. Lint
cd mobile && npx eslint src/

# 8. Tests
cd mobile && npx jest
```

### Documentation

```bash
# 9. Markdown lint (if markdownlint-cli2 installed)
npx markdownlint-cli2 "docs/**/*.md"
```

## Output Format

After running all checks, provide a summary table:

| Check | Status | Details |
|-------|--------|---------|
| Ruff lint | PASS/FAIL | Error count |
| Ruff format | PASS/FAIL | Files needing format |
| Mypy | PASS/FAIL | Error count |
| Bandit | PASS/FAIL | Issue count by severity |
| pip-audit | PASS/FAIL | CVE count |
| pytest | PASS/FAIL | Tests passed/failed |

## Auto-Fix Mode

If any lint/format checks fail, offer to auto-fix:

```bash
python -m ruff check device/ cloud/ policy/ --fix
python -m ruff format device/ cloud/ policy/
```

## Prerequisites

All tools are installed via `pip install -e ".[dev]"` and invoked with `python -m` to ensure the correct interpreter is used regardless of PATH configuration.

## Related Commands

- `/security-check` -- Security-focused scanning only
- `/privacy-audit` -- Privacy and consent verification
- `/commit` -- Commit workflow (runs file-scoped checks first)
- `/pr` -- Full PR workflow (runs this quality gate first)
