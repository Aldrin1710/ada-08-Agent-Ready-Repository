# Requirements — Customer Search

## User Story
As a user,
I want to search customers by name, last name, or email,
so that I can quickly find the customer record I need.

## Functional Requirements
- **FR-01**: The system must reject search requests and not process queries when the entered search term contains only whitespace or lacks alphanumeric characters.
- **FR-02**: The system must evaluate the search term exclusively against the customer's `name`, `last_name`, and `email` fields.
- **FR-03**: The system must identify a partial match when the entered search term is a prefix or substring of any of the allowed customer fields (`name`, `last_name`, `email`).
- **FR-04**: The system must return identical customer records regardless of whether the search term contains uppercase, lowercase, or mixed-case letters.
- **FR-05**: The system must order results by returning customers with an exact match on the search term first (across allowed fields `name`, `last_name`, or `email`, tie-broken deterministically by `id` ascending), followed by partial matches ordered alphabetically by `last_name` (and tie-broken by `id` ascending).
- **FR-06**: The system must return the standardized message `"No se encontraron clientes"` when a query produces no matches or is rejected by input validation.

## Non-Functional Requirements
- **NFR-01**: The system must execute search queries and return the result list in a maximum of 150 milliseconds for 95% of local requests over a structured JSON dataset of up to 50,000 customer records.
- **NFR-02**: The system must validate the structural integrity and field types of the JSON schema during initial load into memory, rejecting missing, corrupted, or malformed files within 500 milliseconds and reporting the failure with exit code `1` and the message `"Error: No se pudo cargar la base de datos de clientes"`.
- **NFR-03**: The source code in `src/` must achieve a minimum automated test coverage of 90% using `pytest` (`pytest-cov`) while passing static type-annotation and syntax checks without warnings.

## Open Questions
- **Q-01**: Should fuzzy search be supported in a future release to tolerate minor user typos?
- **Q-02**: Should the CLI store a local history of recent user searches?

## Constraints / Assumptions
- **C-01**: The system is developed in Python 3.11+ and executed locally via CLI.
- **C-02**: Data persistence is handled exclusively in memory from a local JSON file (`data/customers.json`), without external database engines.
- **A-01**: The source JSON file (`data/customers.json`) is assumed to be UTF-8 encoded.
