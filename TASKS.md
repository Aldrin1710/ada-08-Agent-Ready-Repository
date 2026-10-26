# Tasks

## T-01 Project Setup
- **Goal**: Establish base directory structure (`src/`, `tests/`, `docs/`) and configure `pytest`.
- **Files**: `pytest.ini`, `tests/test_environment.py`
- **Acceptance**: `pytest` runs cleanly from the repository root.
- **Verification**: `pytest -v`

## T-02 Domain Model & Storage
- **Goal**: Implement `Customer` domain model and `load_customers` JSON storage loader with structural and type validation (`NFR-02`, `EH-02`).
- **Files**: `src/model.py`, `src/storage.py`, `data/customers.json`
- **Acceptance**: Valid JSON parses into `list[Customer]`; missing/malformed files exit with code `1`.
- **Verification**: `pytest tests/test_storage.py`

## T-03 Search & Ordering Logic
- **Goal**: Implement `search_customers(term: str) -> list[Customer]` with case-insensitive matching (`FR-02`, `FR-03`, `FR-04`) and exact-before-partial deterministic ordering (`FR-05`, `AC-03`, `AC-04`).
- **Files**: `src/service.py`, `tests/test_search.py`
- **Acceptance**: `AC-02`, `AC-03`, and `AC-04` are verified by unit tests in `tests/test_search.py`.
- **Verification**: `pytest tests/test_search.py`

## T-04 CLI Validation & Error Handling
- **Goal**: Implement CLI entry point, input validations (`VR-01`, `VR-02`), and standardized error messages (`EH-01`, `EH-02`).
- **Files**: `src/cli.py`, `tests/test_cli.py`
- **Acceptance**: `AC-01` and `AC-05` pass without exposing stack traces.
- **Verification**: `pytest tests/test_cli.py`

## T-05 Automated Tests & Quality Gate
- **Goal**: Maintain >= 90% test coverage on `src/` (`NFR-03`) and pass all test scenarios (`TS-01` through `TS-07`).
- **Files**: `tests/test_search.py`, `tests/test_cli.py`, `tests/test_storage.py`
- **Acceptance**: Coverage on `src/` >= 90% and all tests pass.
- **Verification**: `pytest --cov=src --cov-fail-under=90 tests/`

## T-06 Traceability & Repository Verification
- **Goal**: Keep `docs/traceability.md` synchronized with all requirements, acceptance criteria, source files, and unit test functions, and pass repository contract checks.
- **Files**: `docs/traceability.md`, `scripts/check_repo_contract.py`, `scripts/verify_repo.sh`
- **Acceptance**: Every test in `tests/test_search.py` is mapped in `docs/traceability.md` and `scripts/check_repo_contract.py` reports `REPO_CONTRACT: PASS`.
- **Verification**: `python scripts/check_repo_contract.py`
