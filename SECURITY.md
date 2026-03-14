# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.0.x   | Yes       |

Only the latest release in each supported version line receives security updates.

## Reporting a Vulnerability

**Do NOT report security vulnerabilities as public GitHub issues.**

To report a vulnerability, email **<security@disability-assist.org>** with:

- A description of the vulnerability
- Steps to reproduce
- The potential impact
- Any suggested remediation (optional)

### What to Expect

| Step | Timeline |
| ---- | -------- |
| Acknowledgment of your report | Within 48 hours |
| Initial assessment and severity classification | Within 5 business days |
| Status update with remediation plan | Within 10 business days |
| Fix released (critical/high severity) | Within 30 days |
| Fix released (medium/low severity) | Within 90 days |

We will keep you informed throughout the process. If you do not receive an acknowledgment within 48 hours, please follow up.

## Scope

The following are considered security issues and should be reported through this process:

- **Authentication or authorization bypass** -- accessing resources or actions without proper credentials or permissions
- **PII exposure** -- personal data leaked in logs, error messages, API responses, or storage
- **Consent bypass** -- data processed outside its authorized consent lane, or consent revocation not honored
- **Risk tier bypass** -- actions executed at a higher risk tier than authorized (e.g., tier 2-3 actions without confirmation or despite being blocked)
- **Injection vulnerabilities** -- SQL injection, command injection, prompt injection leading to unauthorized actions
- **Credential exposure** -- API keys, tokens, or passwords in code, logs, or client-side storage
- **Transport security** -- unencrypted transmission of audio, transcripts, or personal data
- **Privilege escalation** -- a user gaining access to another user's data or a higher role's capabilities
- **Hard constraint violations** -- any path that allows the system to execute purchases, provide medication advice, make emergency calls, or render clinical judgments
- **Audio data retention** -- raw audio stored without explicit consent or beyond documented retention periods

## Out of Scope

The following are NOT considered security vulnerabilities for this project:

- Social engineering attacks against contributors or maintainers
- Physical access to a device by someone with valid device credentials
- Denial of service against cloud providers (report to the cloud provider)
- Vulnerabilities in dependencies that do not affect this project's usage of them (though we appreciate the heads-up)
- Bugs that do not have a security impact

## Recognition

We believe in recognizing the contributions of security researchers who help keep this project and its users safe. With your permission, we will:

- Credit you by name (or handle) in the security advisory
- List you in a SECURITY-ACKNOWLEDGMENTS file in the repository

We do not currently offer a paid bug bounty program.

## Security Practices

This project follows these security practices:

- **No secrets in code** -- all credentials stored in `.env` (gitignored)
- **Input validation** -- Pydantic (Python) and Zod (React Native) for all external inputs
- **Encrypted transport** -- TLS 1.3+ for all cloud communication
- **Dependency scanning** -- pip-audit for known CVEs in Python dependencies
- **Static analysis** -- Bandit for Python security anti-patterns
- **Secrets detection** -- detect-secrets in pre-commit hooks
- **Consent enforcement** -- all data flows annotated with consent lanes
- **Risk tier enforcement** -- all actions carry documented risk tiers with appropriate gates
