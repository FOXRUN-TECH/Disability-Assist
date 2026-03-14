# Contributing to Disability-Assist

Thank you for your interest in contributing to Disability-Assist. This project builds assistive communication technology for people with speech, cognitive, sensory, developmental, and age-related communication barriers. Every contribution matters.

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md). In particular, this project requires dignity-first communication. Never use patronizing language toward or about people with disabilities.

## Reporting Issues

Use [GitHub Issues](https://github.com/AI-Assist/issues) to report bugs, request features, or ask questions. When reporting a bug, include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, hardware)

**Security vulnerabilities** must NOT be reported as public issues. See [SECURITY.md](SECURITY.md) for responsible disclosure instructions.

## Development Setup

### Prerequisites

- Python 3.11 or later
- Git

### Getting Started

```bash
# Clone the repository
git clone https://github.com/your-fork/AI-Assist.git
cd AI-Assist

# Create a virtual environment
python -m venv .venv

# Activate (Windows)
.venv/Scripts/activate

# Activate (Linux/macOS)
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Environment Configuration

Copy `.env.example` to `.env` and fill in required variables. Never commit `.env` files or API keys.

## Code Style

### Python

- **Ruff** handles linting and formatting. Rules: E, W, F, I, B, C4, UP, D, TRY, SIM, PIE, RUF.
- **Mypy** for static type checking (`disallow_untyped_defs = true`).
- **Google-style docstrings** on all modules, classes, and public functions.
- **No magic numbers** -- use `typing.Final` constants in dedicated constants modules. Suppress with `# magic-ok` only when justified.
- **Line length:** 100 characters.
- **Line endings:** LF for all text files. CRLF only for `.bat`, `.cmd`, `.ps1`.

```bash
# Lint a single file
ruff check path/to/file.py

# Format a single file
ruff format path/to/file.py

# Type check a single file
mypy path/to/file.py --ignore-missing-imports
```

### React Native (Phase 4+)

- ESLint + Prettier
- TypeScript strict mode
- Zod for input validation

## Commit Messages

This project uses **conventional commits**. Every commit message must follow this format:

```text
type(scope): description
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `ci`

**Examples:**

- `feat(cloud): add STT provider abstraction layer`
- `fix(device): correct wake word sensitivity threshold`
- `docs(governance): add ADR for cloud-first architecture`
- `test(policy): add risk tier enforcement tests`

## Pull Request Process

1. **Create a feature branch** from `master`. Use descriptive branch names (e.g., `feat/stt-provider-abstraction`).
2. **Make focused changes.** Each PR should address one concern.
3. **Run quality checks** before submitting:

   ```bash
   ruff check .
   ruff format --check .
   mypy device/ cloud/ policy/ --ignore-missing-imports
   pytest tests/unit/ -v
   ```

4. **CI must pass.** The GitHub Actions pipeline runs linting, type checking, and tests. PRs with failing CI will not be merged.
5. **Request review.** All PRs require at least one review before merge.

### Quality Gate

PRs touching code in `device/`, `cloud/`, `policy/`, or `mobile/` must pass:

- Ruff lint and format checks
- Mypy type checking
- All relevant unit tests
- No magic numbers (or justified `# magic-ok` suppressions)
- No mock patterns in production code (or justified `# mock-ok` suppressions)
- No PII in log statements (or justified `# pii-ok` suppressions)

## Testing

### Naming Convention

Use behavior-driven test names that describe what the code does:

```python
# Good
def test_blocks_purchase_action_at_tier_3(): ...
def test_paraphrases_transcript_for_caregiver_feed(): ...
def test_revokes_consent_within_60_seconds(): ...

# Bad
def test_action_router(): ...
def test_validator(): ...
```

### Running Tests

```bash
# Run a single test file
pytest tests/unit/test_specific_file.py -v

# Run all unit tests (only when explicitly needed)
pytest tests/unit/ -v
```

### Coverage Targets

| Area | Target |
| ---- | ------ |
| Policy/safety layer | 95% |
| Consent flows | 90% |
| Cloud API integrations | 80% |
| Device runtime | 80% |
| React Native (mobile) | 70% |
| Infrastructure | 60% |

## Phase-Aware Development

This project follows a phased roadmap. Before contributing, check which phase is active by reviewing `docs/roadmap.md` and `.claude/hooks/_phase_config.py`. Contributions outside the active phase scope will be flagged during review.

## Privacy and Consent

All code that handles user data must:

- Document the **consent lane** it belongs to (annotate with `# consent-lane: <lane>`)
- Classify data sensitivity (public, internal, sensitive, restricted)
- Document retention policy
- Never log PII (suppress with `# pii-ok` only when justified)
- Never expose raw transcripts to caregivers (use paraphrases)
- Support consent revocation

The six consent lanes are: core-cloud, caregiver-access, cloud-sync, community-learning, research, audio-research.

## Dignity Language Guidelines

All code, comments, documentation, and user-facing text must follow dignity-first principles:

- Never use clinical terminology as if diagnosing
- Never use patronizing language ("good job", "well done" for adults)
- Use choice-based prompts, not leading questions
- Use "assistive profile" not "personality"
- Never simulate therapy, invent memories, or fabricate caregiver communications
- Clarification prompts must be short and respectful

## License Requirements

- Production dependencies must use MIT, Apache 2.0, or BSD licenses
- **No GPL dependencies** in production code
- If you want to add a new dependency, check its license first and note it in your PR

## Questions?

If you are unsure about anything, open a GitHub Issue or Discussion. We are happy to help.
