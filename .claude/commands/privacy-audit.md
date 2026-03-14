# Privacy Audit Command

Scan for PII exposure, verify consent lanes, and audit data classification. [PV][CON]

This is an AI-Assist-specific command -- assistive technology handling
sensitive user data requires dedicated privacy verification.

## Usage

```text
/privacy-audit
```

## What It Does

### Step 1: PII Scan

Grep source files for patterns suggesting PII handling:

- Email regex in log/print statements
- Phone number patterns in log/print
- User names in log/print (user.name, full_name, etc.)
- Raw transcript/utterance in log/print (should use paraphrase)
- Audio file paths being written to non-ephemeral storage
- Caregiver-facing code exposing raw transcript instead of paraphrase

Report any found outside of explicitly approved modules (suppress with `# pii-ok`).

### Step 2: Consent Lane Verification

For each module in `cloud/`, `device/`, `policy/` that handles user data:

- Check for consent lane annotation: `# consent-lane: <lane>`
- Valid lanes: `core-cloud`, `caregiver-access`, `cloud-sync`, `community-learning`, `research`, `audio-research`
- Report any data-handling functions without lane annotation

### Step 3: Data Classification Check

Verify that each data model/schema has a data classification:

- `public` -- non-sensitive, no restrictions
- `internal` -- not for external sharing
- `sensitive` -- PII, consent-gated
- `restricted` -- health-adjacent, multi-consent-gated

Look for Pydantic models handling user data without classification comments.

### Step 4: Retention Policy Check

Scan for data storage patterns without documented retention:

- Database writes without TTL or retention schedule reference
- File writes to persistent storage without cleanup mechanism
- Cache entries without expiration

### Step 5: Minimum Disclosure Check

Scan caregiver-facing code paths:

- Verify transcript is paraphrased, not passed as raw text
- Verify only intent is shared with caregiver feed (not verbatim transcript)
- Check that role-based filtering is applied before display

### Step 6: Role Boundary Check

Verify that caregiver access endpoints enforce role-based permissions:

- `user` -- self-directed access
- `family` -- family caregiver (consent-gated)
- `professional` -- support worker (role-limited)
- `guardian` -- substitute decision maker
- `administrator` -- system admin (no content access)

## Output Format

Privacy audit summary with findings categorized by severity:

| Severity | Category | Count |
|----------|----------|-------|
| **Critical** | PII leak in logs/output | count |
| **High** | Missing consent lane | count |
| **Medium** | Missing data classification | count |
| **Low** | Missing retention policy | count |

For each finding: file path, line number, description, and remediation.

## Related Commands

- `/security-check` -- Security-focused scanning
- `/review` -- Self-review including privacy dimension
- `/quality` -- Full quality gate
