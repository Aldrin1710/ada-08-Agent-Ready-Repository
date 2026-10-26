# Repository Map

## Entry Points
- `src/cli.py` — CLI bootstrap and argument validation (`main()`). Run via `python src/cli.py "<term>"`.
- `src/service.py` — Domain search and sorting logic (`search_customers(term: str) -> list[Customer]`).
- `src/storage.py` — JSON file loading and schema/type validation (`load_customers(file_path: str) -> list[Customer]`).
- `src/model.py` — `Customer` dataclass (`id: int`, `name: str`, `last_name: str`, `email: str`).

## Tests
- `tests/test_search.py` — Unit tests for `src/service.py` (`search_customers`), mocking `src.service.load_customers`.
- `tests/test_cli.py` — End-to-end CLI argument and validation tests for `src/cli.py`.
- `tests/test_storage.py` — JSON persistence and schema error tests for `src/storage.py`.
- `tests/test_environment.py` — Test environment smoke check.

## Change Guide
If changing search, matching, or ordering behavior (`FR-02`..`FR-05`, `AC-02`..`AC-04`):
1. Check `REQUIREMENTS.md` / `SPEC.md`.
2. Update `src/service.py` (`search_customers`).
3. Add or modify unit tests in `tests/test_search.py`.
4. Run `./scripts/verify_repo.sh`.

## Do Not Edit Directly
- `data/customers.json` — Protected seed dataset verified by `scripts/check_repo_contract.py`.
- `.env` — Secrets and environment configuration.
- `__pycache__/` and `.coverage` — Generated cache artifacts.
