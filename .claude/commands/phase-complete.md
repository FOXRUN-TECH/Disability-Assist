# Phase Complete Command

Validate and record completion of a phase in the implementation roadmap. [QG]

## Usage

```text
/phase-complete <phase-id>
```

Examples:
- `/phase-complete 0`
- `/phase-complete 1`
- `/phase-complete 4`

## What It Does

1. **Read** `docs/roadmap.md` and locate the phase by ID
2. **Look up** the exit criteria from the roadmap
3. **Run** the verification commands for that phase:
   - For device phases: `ruff check . && ruff format --check .` + `pytest` with coverage
   - For cloud phases: API tests + integration tests
   - For mobile phases (Phase 4+): `cd mobile && npm run build` + `npx jest`
   - For infrastructure phases: manual verification described in criteria
4. **Evaluate** results:
   - If **all checks pass** and exit criteria are met:
     - Update the Status column in `docs/roadmap.md`
     - Update `ACTIVE_PHASE` in `.claude/hooks/_phase_config.py`
     - Report success and suggest the **next phase**
   - If **any check fails**:
     - Report exactly what failed and why
     - Do **NOT** mark the phase as complete
     - Suggest fixes for the failures
5. **Show** a summary of overall progress (X/10 phases complete)

## Phase Dependency Order

```
Phase 0 (Repo foundation)
  -> Phase 1 (Core cloud speech)
    -> Phase 2 (Smart-home control)
    -> Phase 3 (Personalization)
    -> Phase 4 (Caregiver app)
      -> Phase 5 (Consent controls)
        -> Phase 6 (Pilot operations)
          -> Phase 7 (v1 pilot launch)
            -> Phase 8 (v2 shared intelligence)
              -> Phase 9 (Research governance)
```

Phases 2, 3, 4 can run in parallel after Phase 1.

## Important Rules

- NEVER mark a phase complete if tests fail or exit criteria are not met
- ALWAYS run file-scoped checks (not full project-wide) when possible
- If the phase involves manual verification, ask the user to confirm
- Follow the dependency graph -- do not skip ahead
- Update `_phase_config.py` ACTIVE_PHASE after marking complete

## Related Commands

- `/quality` -- Full quality gate (run before `/phase-complete`)
- `/commit --phase-end` -- Phase-end commit with doc enforcement
- `/review` -- Self-review before marking complete
