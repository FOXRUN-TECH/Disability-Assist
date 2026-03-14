# Claude Code Skills - Disability-Assist

This document lists all available skills (slash commands) for the AI-Assist project.

## Available Skills

| Skill | Description | Tag |
|-------|-------------|-----|
| `/quality` | Full quality gate (ruff, mypy, bandit, pip-audit, pytest, markdownlint) | [QG] |
| `/commit` | Quality gate, phase-scope check, conventional commit, push, CI verify. `--phase-end` for end-of-phase commits | [CC][FC][QG] |
| `/pr` | Full quality gate, push, create GitHub PR with security + privacy checklists | [QG][CC] |
| `/security-check` | Bandit + pip-audit + detect-secrets + npm audit | [SecF] |
| `/privacy-audit` | PII scan, consent lane verification, data classification audit | [PV][CON] |
| `/review` | Self-review against security, privacy, dignity, performance, compliance | [SecF][PV][DIG] |
| `/phase-complete <id>` | Validate phase exit criteria and update roadmap | [QG] |
| `/new-api <name>` | Scaffold Python API endpoint with Pydantic models, consent lane, tests | [TS][CON] |
| `/new-component <name>` | Scaffold React Native component with accessibility props (Phase 4+) | [TS][DIG] |
| `/device-setup` | RPi5 connectivity check, fix networking/dpkg, run provisioning | |

## Typical Workflows

**Rapid iteration:** Edit file -> lint/type-check file -> repeat

**Ready to commit:** `/review` -> `/commit`

**Ready for PR:** `/quality` -> `/privacy-audit` -> `/security-check` -> `/pr`

**New feature:** `/new-api <name>` or `/new-component <name>` -> implement -> `/commit`

**Phase completion:** Implement -> `/commit` -> `/phase-complete <id>`

**Device provisioning:** `/device-setup` -> verify

---

## Adding New Skills

1. Create a new `.md` file in `.claude/commands/`
2. Include: Usage, What It Does, Implementation steps, Related Commands
3. Add entry to this SKILLS.md file
4. Reference relevant rule tags ([SecF], [QG], [PV], [DIG], [CON], etc.)

### Skill File Template

```markdown
# Skill Name Command

Brief description. [Tags]

## Usage

\`\`\`text
/skill-name [options]
\`\`\`

## What It Does

1. Step one
2. Step two

## Related Commands

- `/other-skill` -- Description
```

---

## Related Documentation

- [CLAUDE.md](CLAUDE.md) -- Configuration, rules, and enforcement
- [AGENTS.md](AGENTS.md) -- Agent instructions
- [docs/roadmap.md](../docs/roadmap.md) -- Implementation roadmap
