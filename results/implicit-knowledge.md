# Implicit Knowledge Found

## IK-01
What:
The requirements source-of-truth file is actually named `REQUERIMENTS.md` (misspelled) instead of `REQUIREMENTS.md` as referenced in `AGENTS.md` and `TASK_UNDER_TEST.md`.

How was it discovered:
By running `Get-ChildItem -Force` on the repository root before attempting to read `REQUIREMENTS.md`.

Should this remain implicit?
NO

Where should it become explicit?
Rename the file to `REQUIREMENTS.md` and enforce its existence deterministically via `scripts/check_repo_contract.py` and `AGENTS.md`.

## IK-02
What:
Compiled bytecode files (`src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc`) and `.coverage` are erroneously tracked in Git, so running `pytest --cov=src` pollutes `git status` with out-of-scope binary diffs.

How was it discovered:
Only after executing `pytest -v --cov=src tests/; git status -s` at the end of the BEFORE run.

Risk:
The agent modifies unrelated binary artifacts on every test run, violating the Definition of Done ("No unrelated files are changed") and creating merge conflicts.

Remediation:
Untrack `__pycache__/` and `.coverage` from Git, add `.gitignore`, and add a deterministic guardrail in `scripts/check_repo_contract.py` that fails if any `.pyc`, `__pycache__`, or `.coverage` file is tracked or modified.

## IK-03
What:
The actual CLI entry point is `src/cli.py` (or `search.bat` on Windows), NOT `search.py` as claimed in `ARCHITECTURE.md` (`python search.py "termino"`), and input validations (`VR-01`, `VR-02`) live in `src/cli.py` while JSON schema exit handling (`EH-02`) lives in `src/storage.py`.

How was it discovered:
By reading all 4 files under `src/` (`cli.py`, `service.py`, `storage.py`, `model.py`) and comparing them against `ARCHITECTURE.md` and `README.md`.

Risk:
An agent relying on `ARCHITECTURE.md` looks for a non-existent `search.py` file or places validation/search logic in the wrong module.

Remediation:
Update `ARCHITECTURE.md` to reflect real module boundaries and create `docs/REPO_MAP.md` with accurate entry points, layer responsibilities, and a step-by-step Change Guide.

## IK-04
What:
Running coverage and verifying `NFR-03` (minimum 90% coverage + static type/quality verification) requires specific commands (`pytest --cov=src --cov-fail-under=90` and contract/syntax checks) that are absent from `AGENTS.md`.

How was it discovered:
By cross-referencing `README.md` (`pytest --cov=src tests/`), `REQUERIMENTS.md` (`NFR-03`), and `pytest.ini`.

Should this remain implicit?
NO

Where should it become explicit?
`AGENTS.md` (Standard Commands section), `scripts/verify_repo.sh`, and `.github/workflows/verify.yml`.

## IK-05
What:
`data/customers.json` is the production/seed dataset used by CLI integration tests (`test_cli_valid_term` in `tests/test_cli.py`), and must not be modified when adding unit tests (unit tests in `tests/test_search.py` must mock `src.service.load_customers`).

How was it discovered:
By inspecting `tests/test_search.py`, `tests/test_cli.py`, and `data/customers.json`.

Risk:
An agent might edit `data/customers.json` to test edge cases, breaking existing CLI integration tests or corrupting seed data.

Remediation:
Document `data/customers.json` under `Do Not Edit Directly` in `docs/REPO_MAP.md` and `AGENTS.md`, and enforce a deterministic checksum/clean-diff check on `data/customers.json` inside `scripts/check_repo_contract.py`.
