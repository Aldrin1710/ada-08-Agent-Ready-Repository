# Architecture

## Overview
Local Python CLI application that searches customer records stored in `data/customers.json`. It uses a three-layer architecture separating CLI input/output, domain search logic, and JSON persistence.

## Components & Responsibilities
1. **CLI Layer (`src/cli.py`)**:
   - Entry point (`main()`).
   - Reads command-line arguments (`sys.argv`), enforces input validation rules (`VR-01`, `VR-02`), invokes `search_customers(term)` from `src/service.py`, formats matching records as `[{id}] {name} {last_name} - {email}`, and handles top-level exceptions without exposing stack traces.
2. **Service / Domain Layer (`src/service.py` & `src/model.py`)**:
   - `src/model.py` defines the `Customer` dataclass (`id: int`, `name: str`, `last_name: str`, `email: str`).
   - `src/service.py` defines `search_customers(term: str) -> list[Customer]`, implementing case-insensitive exact and partial matching and deterministic ordering (`FR-02`, `FR-03`, `FR-04`, `FR-05`, `AC-03`, `AC-04`).
   - Must remain independent of `sys.argv` and CLI stdout formatting so it can be unit-tested in isolation with mocked storage.
3. **Storage Layer (`src/storage.py`)**:
   - Defines `load_customers(file_path: str) -> list[Customer]`.
   - Reads `data/customers.json` (UTF-8), validates JSON list/dict structure, required keys (`id`, `name`, `last_name`, `email`), and field data types (`NFR-02`), exiting with code `1` and printing the standardized error message (`EH-02`) on failure.

## Data Flow
1. User runs `python src/cli.py "<term>"` (or `search.bat "<term>"` on Windows).
2. `src/cli.py` validates `<term>` against `VR-01` and `VR-02` and calls `search_customers(term)`.
3. `src/service.py` calls `load_customers('data/customers.json')` from `src/storage.py`.
4. `src/service.py` classifies and orders exact and partial matches according to `SPEC.md`.
5. `src/cli.py` prints the ordered matches or `"No se encontraron clientes"` (`EH-01`).

## Architecture Boundaries & Protected Paths
- **Do not couple `src/service.py` to CLI I/O**: `src/service.py` must return `list[Customer]` and must never call `print()` or `sys.exit()`.
- **Do not modify `data/customers.json`**: It is the canonical seed dataset used by CLI tests (`tests/test_cli.py`). Unit tests for `src/service.py` in `tests/test_search.py` must mock `src.service.load_customers`.
- **Do not add external runtime dependencies**: Runtime code under `src/` must use only the Python standard library (`C-01`).

## Testing Strategy
- `tests/test_search.py`: Unit tests for `src/service.py` (`search_customers`) using `@patch('src.service.load_customers')`.
- `tests/test_storage.py`: Persistence and schema validation tests for `src/storage.py` (`load_customers`) using temporary JSON files.
- `tests/test_cli.py`: End-to-end CLI argument, validation, and error-handling tests for `src/cli.py` (`main`).
- `tests/test_environment.py`: Smoke test verifying test runner configuration.
