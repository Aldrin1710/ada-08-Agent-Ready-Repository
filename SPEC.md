# Customer Search Feature Specification

## Goal
Provide a local Python CLI tool to search customer records by `name`, `last_name`, or `email` against a local JSON dataset (`data/customers.json`).

## Requirements Covered
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- NFR-01
- NFR-02
- NFR-03
- C-01
- C-02
- A-01

## Scope
Exact and partial customer search, JSON dataset loading and schema validation, deterministic result ordering, and CLI output formatting.

## Out of Scope
Creating, updating, or deleting customer records (`data/customers.json` is read-only seed data).

## Domain Model
`Customer` (`src/model.py`):
- `id`: `int`
- `name`: `str`
- `last_name`: `str`
- `email`: `str`

## Search Rules
- **SR-01 [FR-02, FR-03, FR-04]**: Case-insensitive matching is evaluated exclusively against `name`, `last_name`, and `email`. A partial match occurs when the lowercased search term is a substring of `name`, `last_name`, or `email`.
- **SR-02 [FR-02, FR-05]**: A customer is classified as an **exact match** when the lowercased search term equals `name`, `last_name`, or `email`. Exact matches are returned before partial matches and ordered deterministically by `id` ascending.
- **SR-03 [FR-05]**: Partial matches (customers that match partially but are not exact matches) are ordered alphabetically by `last_name` (case-insensitive) and tie-broken deterministically by `id` ascending.

## Validation Rules
- **VR-01 [FR-01]**: The search term must not be empty, whitespace-only, or devoid of alphanumeric characters.
- **VR-02 [FR-01]**: The search term must be at least 3 characters long (`len(term) >= 3`).

## Error Handling
- **EH-01 [FR-06]**: An invalid search term (`VR-01`, `VR-02`) or a valid search term with zero matches prints `"No se encontraron clientes"` to stdout and exits with code `0`.
- **EH-02 [NFR-02]**: If the source JSON file does not exist, is malformed, or contains invalid field types, the system prints `"Error: No se pudo cargar la base de datos de clientes"` and exits with code `1`.

## Acceptance Criteria
- **AC-01 [FR-01]**: An empty search term, a term shorter than 3 characters, or a term without alphanumeric characters is rejected and outputs `"No se encontraron clientes"`.
- **AC-02 [FR-02]**: A search term that does not match `name`, `last_name`, or `email` returns zero customer records.
- **AC-03 [FR-03, FR-04]**: A lowercase partial search term (`"ale"`) matches a customer stored with uppercase/mixed-case characters (`"Alejandro"`).
- **AC-04 [FR-05]**: Search results always list exact matches (on `name`, `last_name`, or `email`, ordered by `id` ascending) before partial matches (ordered by `last_name` ascending, then `id` ascending).
- **AC-05 [FR-06]**: Searching for a non-existent customer prints `"No se encontraron clientes"` and returns no customer records.

## Test Scenarios
- `TS-01` -> `AC-01` (`VR-01`: non-alphanumeric search term rejected)
- `TS-02` -> `AC-02` (unallowed fields / unmatched term returns empty list)
- `TS-03` -> `AC-03` (case-insensitive matching)
- `TS-04` -> `VR-01`, `AC-04` (empty search term rejected; exact and partial ordering verified)
- `TS-05` -> `VR-02` (short search term `< 3` chars rejected)
- `TS-06` -> `EH-01`, `AC-05` (no matches prints standardized message)
- `TS-07` -> `EH-02`, `NFR-02` (missing or corrupted JSON exits with code `1`)

## Constraints
- **C-01**: Python 3.11+ CLI application using the Python standard library for runtime and `pytest` / `pytest-cov` for testing.
- **C-02**: Persistence is read-only from `data/customers.json`.
