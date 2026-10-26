# AI Usage Log (`ADA-08` — Agent-Ready Repository)

This log documents the key engineering decisions, agent observations, accepted/rejected suggestions, and verification steps executed during **ADA-08** (building upon the ADA-05 and ADA-07 history).

---

## Entry 1 — Initial Repository Readiness Audit (`BEFORE`)
- **Date**: 2026-10-26
- **Context**: Auditing the baseline repository (`ada08-baseline`, commit `a0f667c`) across the 8 dimensions of Agent-Ready Repository prior to executing the controlled task `CR-02`.
- **What the Agent Detected**:
  - `AGENTS.md` referenced `REQUIREMENTS.md`, whereas the file on disk was misspelled `REQUERIMENTS.md`.
  - `ARCHITECTURE.md` referenced a non-existent CLI entry point (`python search.py "termino"`) and described validation/error boundaries that differed from `src/cli.py` and `src/storage.py`.
  - `.coverage` and 11 compiled bytecode files (`src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc`) were tracked in Git with no `.gitignore`.
  - No `docs/REPO_MAP.md`, `scripts/verify_repo.sh`, `scripts/check_repo_contract.py`, `requirements.txt`, or `.github/workflows/verify.yml` existed.
- **Human Validation & Decision**:
  - Validated all findings against the repository tree and scored the baseline at **39.0 / 100** in `REPOSITORY_READINESS_AUDIT.md`.
  - Defined `TASK_UNDER_TEST.md` (`CR-02`: exact match on `last_name` + deterministic tie-breaking by `id` ascending) and preserved the `ada08-baseline` tag before running the BEFORE experiment.

---

## Entry 2 — Execution of `BEFORE` & Discovery of Implicit Knowledge
- **Date**: 2026-10-26
- **Context**: Running the clean-session coding agent (`5b138d3d-6b95-4152-95d8-8db04fb55a83`) on branch `before-experiment` using the verbatim English prompt from ADA-08 Section 9.
- **Observed Agent Friction**:
  - The agent had to run 2 directory scans (`Get-ChildItem`) and read 15 files (including unrelated modules `src/cli.py`, `src/storage.py`, `tests/test_cli.py`, `tests/test_storage.py`, `data/customers.json`) to understand the repository structure and locate `REQUERIMENTS.md`.
  - Its first `edit_file` call on `src/service.py` failed due to CRLF line endings and trailing whitespace, forcing a full-file overwrite.
  - Running `pytest -v --cov=src tests/` modified 3 tracked binary files (`.coverage` and 2 `.pyc` files) in `git status`.
  - The agent failed to update `docs/traceability.md` with the 2 new unit tests.
- **Human Decision (`results/implicit-knowledge.md`)**:
  - Classified the BEFORE run as **PARTIAL** in `results/before-agent-run.md` and cataloged 5 implicit knowledge items (`IK-01`..`IK-05`), deciding to remediate structural/traceability/hygiene rules via deterministic scripts (`check_repo_contract.py` + `.gitignore`) rather than relying on prose alone.

---

## Entry 3 — Design of `AGENTS.md` & `GEMINI.md` Adapter
- **Date**: 2026-10-26
- **Context**: Designing Improvement `I-01` (`AGENTS.md`) and Improvement `I-02` (`GEMINI.md`).
- **Suggestions Accepted**:
  - Included the 7 essential operational sections in `AGENTS.md`: `Read First`, `Sources of Truth`, `Repository Map`, `Standard Commands`, `Change Rules`, `Stop Conditions`, and `Definition of Done`.
  - Explicitly documented both the Git Bash command (`D:\Git\bin\bash.exe scripts/verify_repo.sh` / `./scripts/verify_repo.sh`) and the PowerShell equivalent (`pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify_repo.ps1`) after discovering that `bash` was not on the default Windows `PATH`.
- **Suggestions Rejected**:
  - Rejected embedding domain search rules (`SR-01`..`SR-03`) or the full traceability table inside `AGENTS.md` or `GEMINI.md` to prevent duplicating `REQUIREMENTS.md`, `SPEC.md`, and `docs/traceability.md`.

---

## Entry 4 — Converting Tribal Rules into Deterministic Guardrails (`check_repo_contract.py`)
- **Date**: 2026-10-26
- **Context**: Designing Improvement `I-05` (`scripts/check_repo_contract.py`) and Improvement `I-06` (`.gitignore` / `.gitattributes`).
- **Why Software Instead of Natural Language**:
  - In BEFORE, `AGENTS.md` already said *"Documentation reflects final behavior"* and *"No unrelated files are changed"*, yet the agent still forgot to update `docs/traceability.md` and dirtied `.coverage` / `*.pyc`.
- **Implemented Guardrails**:
  1. Regex/AST check ensuring every `def test_*` in `tests/test_search.py` appears in `docs/traceability.md`.
  2. `git ls-files` check blocking any tracked `.pyc`, `__pycache__`, `.coverage`, or `.env` file.
  3. `git diff` protected-path check ensuring `data/customers.json` is never modified.
  4. AST check verifying public functions in `src/service.py` and `src/storage.py` include parameter and return type annotations (`NFR-03`).

---

## Entry 5 — Shared Verification Contract Between Human, Agent, and CI (`verify_repo.sh` & `.github/workflows/verify.yml`)
- **Date**: 2026-10-26
- **Context**: Designing Improvement `I-04` (`scripts/verify_repo.sh`) and Improvement `I-07` (`.github/workflows/verify.yml`).
- **Decision & Rationale**:
  - Configured `.github/workflows/verify.yml` to install `requirements.txt` and invoke `bash ./scripts/verify_repo.sh` directly rather than duplicating `pytest`, `compileall`, and `check_repo_contract.py` steps inside the YAML workflow.
  - This guarantees a single verification contract (`Human developer -> verify_repo.sh <- Coding agent <- CI`).

---

## Entry 6 — Execution of `AFTER` in a Clean Agent Session
- **Date**: 2026-10-26
- **Context**: Restoring the baseline functional code (`src/` and `tests/` from `ada08-baseline`), applying only the repository readiness improvements (`21cc88a`), and running a new clean session of `coding-agent` (`d0a93548-2bce-482a-978f-b5217f33da5c`) with the exact same prompt and `TASK_UNDER_TEST.md`.
- **Observed Behavioral Change**:
  - The agent followed `AGENTS.md` $\rightarrow$ `docs/REPO_MAP.md`, skipped all unrelated modules (`cli.py`, `storage.py`, `model.py`, `customers.json`), edited `src/service.py`, `tests/test_search.py`, and `docs/traceability.md` in one parallel turn with `0` failed tool calls, executed `scripts/verify_repo.ps1` (`REPO_CONTRACT: PASS`, `VERIFY_REPO: PASS`), and finished in 31 steps with `0` out-of-scope files modified (**Final Result: `PASS`**).

---

## Entry 7 — Final Evaluation & Remaining Human-in-the-Loop Boundaries
- **Date**: 2026-10-26
- **Context**: Completing `REPOSITORY_READINESS_AUDIT.md` (`AFTER: 98.0 / 100`, `Delta: +59.0`) and `results/readiness-improvement-report.md`.
- **Remaining Limitations Requiring Human Intervention**:
  - Resolving product ambiguities (`Q-01` fuzzy search, `Q-02` search history) or conflicting business requirements between `REQUIREMENTS.md` and `SPEC.md`.
  - Approving changes to architectural boundaries (`ARCHITECTURE.md`), external runtime dependencies (`C-01`), or protected seed datasets (`data/customers.json`).
  - Final human review and merge approval of Pull Requests on GitHub (enforced as a `Human Gate` by `.agents/skills/reviewing_pull_requests/SKILL.md`).
