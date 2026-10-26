# AGENTS.md

## Read First
1. `REQUIREMENTS.md`
2. `SPEC.md`
3. `ARCHITECTURE.md`
4. `TASKS.md`
5. `docs/REPO_MAP.md`

## Sources of Truth
- Requirements live only in `REQUIREMENTS.md`.
- Verifiable behavior lives in `SPEC.md`.
- Do not change `REQUIREMENTS.md` or `SPEC.md` merely to make tests pass.

## Repository Map
- `src/` — CLI (`cli.py`), domain search (`service.py`), model (`model.py`), JSON storage (`storage.py`)
- `tests/` — Automated `pytest` suite (`test_search.py`, `test_cli.py`, `test_storage.py`, `test_environment.py`)
- `docs/` — Operational navigation and change guide (`docs/REPO_MAP.md`)
- `scripts/` — Deterministic verification (`scripts/verify_repo.sh`, `scripts/check_repo_contract.py`)
- `results/` — Generated readiness and agent execution evidence

## Standard Commands
- **Install**: `pip install pytest pytest-cov`
- **Run**: `python src/cli.py "ale"`
- **Test**: `python -B -m pytest -q -p no:cacheprovider tests/`
- **Lint / Check**: `python -B scripts/check_repo_contract.py`
- **Verify**: `./scripts/verify_repo.sh` (or `D:\Git\bin\bash.exe scripts/verify_repo.sh` on Windows)

## Change Rules
- Keep changes scoped to the requested task (`TASK_UNDER_TEST.md`).
- Do not weaken existing tests.
- Do not introduce new dependencies without justification.
- Do not modify `data/customers.json`, secrets, or generated files.

## Stop Conditions
Stop and ask for human input when:
- requirements conflict,
- a destructive action is required,
- an architecture boundary must change,
- a required external system is unavailable.

## Definition of Done
1. Requested code changes and unit tests in `tests/` are implemented within scope.
2. `./scripts/verify_repo.sh` completes with `REPO_CONTRACT: PASS` and `VERIFY_REPO: PASS`.
3. `git status -s` shows no unrelated or untracked files modified.
