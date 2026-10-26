# Task Under Test

Change ID: CR-02

## Goal
Extend exact-match detection in customer search so that an exact match on `last_name` (case-insensitive) is also prioritized as an exact match alongside `name` and `email`, and ensure deterministic tie-breaking by `id` (ascending) within exact matches and within partial matches that share the same `last_name`.

## Requirements Covered
- FR-02
- FR-04
- FR-05
- AC-03
- AC-04

## Verification
Automated unit tests in `tests/test_search.py` proving that:
1. Searching a term that exactly matches a customer's `last_name` (regardless of case) classifies that customer in the exact-match group ahead of partial matches.
2. Multiple exact matches are ordered deterministically by `id` ascending, and partial matches with identical `last_name` are tie-broken by `id` ascending.
3. All existing repository tests continue to pass without regressions.

## Constraints
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.
