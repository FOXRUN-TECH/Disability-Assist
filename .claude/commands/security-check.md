# Security Check Command

Run the full security scanning pipeline. [SecF]

## Usage

```text
/security-check
```

## What It Does

Run each security scanner and report findings by severity.

### Scanning Pipeline

```bash
# 1. Python SAST -- static analysis for security vulnerabilities
python -m bandit -r device/ cloud/ policy/ -ll

# 2. Python dependency CVEs
python -m pip_audit

# 3. Secrets detection -- scan for API keys, passwords, tokens
detect-secrets scan

# 4. Node dependency CVEs (Phase 4+, when mobile/ exists)
cd mobile && npm audit --audit-level=high
```

### What Each Tool Catches

| Tool | Detects |
|------|---------|
| **Bandit** | Code injection (CWE-94), OS command injection (CWE-78), hardcoded passwords (CWE-259), insecure functions (`eval`, `exec`, `pickle`) |
| **pip-audit** | Known CVEs in Python dependencies |
| **detect-secrets** | API keys, passwords, tokens, private keys in source code |
| **npm audit** | Known CVEs in Node.js dependencies |

## Output Format

Provide a summary with severity levels:

| Scanner | Status | High | Medium | Low |
|---------|--------|------|--------|-----|
| Bandit | PASS/FAIL | count | count | count |
| pip-audit | PASS/FAIL | count | - | - |
| detect-secrets | PASS/FAIL | count | - | - |
| npm audit | PASS/FAIL | count | count | count |

For each finding, include: file path, line number, description, and remediation guidance.

## Security Checklist Review

After scanning, also verify the AI-generated code checklist from `.claude/CLAUDE.md`:

- [ ] All user inputs validated (Pydantic/Zod)
- [ ] No `eval()`/`exec()`/`Function()` with user input
- [ ] No `subprocess.run(shell=True)` with user input
- [ ] No SQL string concatenation
- [ ] No secrets in code
- [ ] PII encrypted before disk write
- [ ] Auth on protected endpoints
- [ ] Error messages don't leak internals
- [ ] No PII in logs
- [ ] Dependencies verified for CVEs
- [ ] Voice transcripts: max length enforced, control characters stripped
- [ ] Consent lane verified for all data flows
- [ ] Risk tier assigned for all action execution paths

## Prerequisites

All tools are installed via `pip install -e ".[dev]"` and invoked with `python -m`.

## Related Commands

- `/quality` -- Full quality gate (includes security checks)
- `/review` -- Self-review against security/privacy/compliance
- `/privacy-audit` -- Privacy-focused verification
