# Self-Review Command

Review all modified code against security, privacy, dignity, performance, correctness, and compliance criteria. [SecF][PV][DIG]

## Usage

```text
/review
```

## What It Does

1. **Identify modified files** since last commit: `git diff --name-only` and `git diff --staged --name-only`
2. **Read each modified file** and review against the six criteria below
3. **Output a structured report** with findings per file

## Review Criteria

### Security [SecF]

- Are all user inputs validated (Pydantic backend, Zod mobile)?
- Any injection risks (`eval`, `exec`, `subprocess(shell=True)`, SQL concat)?
- Are secrets hardcoded anywhere?
- Is PII encrypted before disk write?
- Do error messages leak internal details?
- Is authentication checked on protected endpoints?

### Privacy [PV]

- Is PII exposed in log/print statements?
- Is the correct consent lane identified and enforced?
- Is minimum disclosure applied (paraphrase over verbatim)?
- Is data retention bounded (not indefinite)?
- Are role-based permissions enforced on caregiver endpoints?
- Is raw audio being retained without explicit consent?

### Dignity [DIG]

- Is language respectful and non-patronizing?
- No clinical terminology used as if diagnosing?
- Are prompts choice-based, not leading?
- Are clarification prompts short and not condescending?
- Is the system presenting as assistive, not therapeutic?

### Performance

- Any O(n^2) loops without justification?
- End-to-end response within 3.5s cloud budget (from PRD-03)?
- Memory leaks (audio buffers not dereferenced)?

### Correctness

- Edge cases handled (empty inputs, null values, boundary conditions)?
- Error handling present and appropriate (custom exceptions, not bare raises)?
- Type safety maintained (no untyped `Any` without comment)?
- Return types on all public functions?

### Compliance

- Follows CLAUDE.md rules and existing project patterns?
- Google-style docstrings on public functions?
- Constants extracted (not hardcoded)?
- Tests included for new functionality?
- Conventional commit message format [CC]?
- No PII in logs [PV]?

## Output Format

For each file, report:

```
### <file_path>
- **Security**: [PASS | findings...]
- **Privacy**: [PASS | findings...]
- **Dignity**: [PASS | findings...]
- **Performance**: [PASS | findings...]
- **Correctness**: [PASS | findings...]
- **Compliance**: [PASS | findings...]
```

## Trust Spectrum

Apply review intensity based on code area:

| Code Area | Required Depth |
|-----------|---------------|
| Consent/privacy/encryption | Deep manual review + privacy audit |
| Risk tier enforcement | Full test coverage + review |
| Voice/audio processing | Privacy focus + tests |
| Cloud API integrations | Integration tests + review |
| Caregiver app UI | Accessibility review + tests |
| Documentation/config | Quick review |

## Related Commands

- `/security-check` -- Automated security scanning
- `/privacy-audit` -- Privacy and consent verification
- `/quality` -- Full quality gate
