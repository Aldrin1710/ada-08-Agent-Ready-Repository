# Readiness Improvement Report (`ADA-08`)

## 1. Executive Summary
This report documents the empirical evaluation and transformation of the **Customer Search CLI** repository (`ada-05` / `ada-07`) into an **Agent-Ready Repository** (`ada-08-agent-ready-repository`).
- **Baseline commit/tag**: `ada08-baseline` (`a0f667c`)
- **Task Under Test (`TASK_UNDER_TEST.md`)**: `CR-02` — Extend exact-match detection in `search_customers` (`src/service.py`) to include `last_name` (case-insensitive) alongside `name` and `email`, with deterministic ascending `id` tie-breaking across exact and partial matches, plus unit tests in `tests/test_search.py`.
- **Readiness Score Improvement**: **BEFORE: `39.0 / 100`** $\rightarrow$ **AFTER: `98.0 / 100`** (**Delta: `+59.0 points`**)
- **Agent Outcome Improvement**: **BEFORE: `PARTIAL`** (39 steps, 15 files read, 1 failed `edit_file` tool call, 3 out-of-scope binary files dirtied, `docs/traceability.md` missed) $\rightarrow$ **AFTER: `PASS`** (31 steps, targeted file reads via `REPO_MAP.md`, 0 failed commands/edits, 0 out-of-scope files dirtied, `docs/traceability.md` updated, `REPO_CONTRACT: PASS` and `VERIFY_REPO: PASS`).

---

## 2. Changes Made (Classified by Category — Section 10.1)

### Improvement I-01
- **Category**: `Context`
- **Problem**: `AGENTS.md` had only 21 lines, pointed to a non-existent `REQUIREMENTS.md` (actual file was `REQUERIMENTS.md`), lacked standard commands, lacked a repository map, and had incomplete stop conditions and Definition of Done.
- **Change**: Rewrote `AGENTS.md` as a concise operational contract (`Read First`, `Sources of Truth`, `Repository Map`, `Standard Commands`, `Change Rules`, `Stop Conditions`, `Definition of Done`), renamed `REQUERIMENTS.md` $\rightarrow$ `REQUIREMENTS.md`, and standardized `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, and `docs/traceability.md` in English.
- **Evidence**: In AFTER, the agent read `AGENTS.md` first, found `REQUIREMENTS.md` immediately without errors, and followed the `Change Rules` and `Definition of Done` completely.

### Improvement I-02
- **Category**: `Context` (Tool-Specific Adapter & Human Gate)
- **Problem**: Tool-specific files (`GEMINI.md` and `.agents/skills/reviewing_pull_requests/SKILL.md`) either did not exist or referenced the misspelled `REQUERIMENTS.md`.
- **Change**: Created `GEMINI.md` as a lightweight adapter pointing to `AGENTS.md` without duplicating requirements, and updated `.agents/skills/reviewing_pull_requests/SKILL.md` (`v1.0.2`, `Human Gate` enforcing read-only draft reviews and blocking `gh pr merge`).
- **Evidence**: `GEMINI.md` directed the AFTER agent to `AGENTS.md`, `docs/REPO_MAP.md`, and `scripts/verify_repo.ps1` with zero requirement duplication.

### Improvement I-03
- **Category**: `Navigation`
- **Problem**: No `docs/REPO_MAP.md` existed, and `ARCHITECTURE.md` referenced a non-existent `python search.py "termino"`. During BEFORE, the agent had to run recursive directory scans (`Get-ChildItem -Recurse`) and read all 4 `src/*` files, all `tests/*` files, and `data/customers.json` (15 files total).
- **Change**: Created `docs/REPO_MAP.md` with explicit `Entry Points`, `Tests`, a task-by-task `Change Guide`, and `Do Not Edit Directly` rules, and corrected `ARCHITECTURE.md`.
- **Evidence**: During AFTER, the agent read `docs/REPO_MAP.md` and went directly to `src/service.py`, `tests/test_search.py`, and `docs/traceability.md`, completely skipping unrelated files (`src/cli.py`, `src/storage.py`, `src/model.py`, `tests/test_cli.py`, `tests/test_storage.py`, `data/customers.json`).

### Improvement I-04
- **Category**: `Executable Knowledge`
- **Problem**: Test coverage (`>= 90%` required by `NFR-03`), static compilation/type checks, and repository contract validation were not bundled into a single reproducible command.
- **Change**: Created `scripts/verify_repo.sh` (and Windows wrapper `scripts/verify_repo.ps1`) plus `requirements.txt` to execute in sequence: (1) `pytest -q --cov=src --cov-fail-under=90 tests/`, (2) `python -m compileall -q src tests scripts`, and (3) `python scripts/check_repo_contract.py`.
- **Evidence**: In AFTER, the agent executed `scripts/verify_repo.ps1` in a single step and obtained deterministic `REPO_CONTRACT: PASS` and `VERIFY_REPO: PASS` output.

### Improvement I-05
- **Category**: `Guardrail`
- **Problem**: In BEFORE, the agent forgot to update `docs/traceability.md` when adding 2 new unit tests to `tests/test_search.py`, and no deterministic check protected `data/customers.json`, verified `NFR-03` type annotations, or blocked tracked `.pyc`/`.coverage` files.
- **Change**: Implemented `scripts/check_repo_contract.py` with 7 deterministic checks: (1) required files/folders exist, (2) `AGENTS.md` required sections exist, (3) `SPEC.md` references `FR-01`..`FR-06` and `AC-01`..`AC-05`, (4) every `def test_*` in `tests/test_search.py` is registered in `docs/traceability.md`, (5) no `.pyc`, `__pycache__`, `.coverage`, or `.env` files are tracked in Git, (6) `data/customers.json` has zero modifications (`git diff`), and (7) AST verification of type annotations on public functions in `src/service.py` and `src/storage.py`.
- **Evidence**: In AFTER, the agent inspected `scripts/check_repo_contract.py`, updated `docs/traceability.md` proactively alongside `tests/test_search.py`, and passed `REPO_CONTRACT: PASS` on the first run.

### Improvement I-06
- **Category**: `Guardrail` (Git Hygiene & Line-Ending Normalization)
- **Problem**: `.coverage` and `src/__pycache__/*.pyc` / `tests/__pycache__/*.pyc` were tracked in Git, causing 3 out-of-scope binary files to be dirtied during BEFORE (`pytest --cov=src`). Additionally, CRLF and trailing whitespace in `src/service.py` caused `edit_file` to fail during BEFORE.
- **Change**: Untracked `__pycache__/` and `.coverage` from Git, added `.gitignore` and `.gitattributes` (`* text=auto eol=lf`), and normalized LF line endings across `src/` and `tests/`.
- **Evidence**: In AFTER, `0` `edit_file` calls failed (vs 1 failure in BEFORE) and `0` out-of-scope binary files appeared in `git status -s` (vs 3 in BEFORE).

### Improvement I-07
- **Category**: `CI Check`
- **Problem**: No CI workflow existed to enforce the same verification contract outside the agent's local session.
- **Change**: Created `.github/workflows/verify.yml` triggered on `push` and `pull_request`, installing `requirements.txt` and executing `bash ./scripts/verify_repo.sh`.
- **Evidence**: Human developers, the coding agent, and GitHub Actions CI now share the exact same single verification script (`scripts/verify_repo.sh`).

---

## 3. Comparative Analysis Table (BEFORE vs AFTER)

| Indicator | BEFORE (`before-experiment` / `945f6ce`) | AFTER (`main` / `c301142`) |
|---|---|---|
| **Clarification questions** | `0` (proceeded despite missing `REQUIREMENTS.md` and `SPEC.md` parenthetical ambiguity) | `0` (`REQUIREMENTS.md` and `SPEC.md` aligned and explicit) |
| **Failed / unknown commands** | `1` failed `edit_file` call on `src/service.py` (CRLF mismatch); no unified verify command | `0` failed tool calls or commands; ran `scripts/verify_repo.ps1` directly |
| **Incorrect assumptions** | `3` (skipped `docs/traceability.md` update, assumed LF line endings, skipped contract/type checks) | `0` (updated `src/service.py`, `tests/test_search.py`, and `docs/traceability.md` together) |
| **Out-of-scope files modified** | `3` binary files dirtied (`.coverage` and 2 `.pyc` files tracked in Git) | `0` (`git status -s` clean except for the 3 target files) |
| **Validations executed correctly** | Partial (`pytest --cov=src` only) | Complete (`scripts/verify_repo.ps1`: 21 tests + 96.55% coverage gate + `compileall` + `check_repo_contract.py`) |
| **Trajectory steps & exploration** | `39` steps; `2` directory scans + `15` files read (including unrelated `cli.py`, `storage.py`, `customers.json`) | `31` steps; `1` root listing + `13` targeted reads guided by `AGENTS.md` and `docs/REPO_MAP.md` |
| **Final result** | **PARTIAL** | **PASS** |
| **Readiness Audit Score** | **39.0 / 100** | **98.0 / 100** (**+59.0 pts**) |

---

## 4. Threats to Validity & Controlled Variables
- **Controlled Constants**: Both BEFORE (`5b138d3d-6b95-4152-95d8-8db04fb55a83`) and AFTER (`d0a93548-2bce-482a-978f-b5217f33da5c`) started from the exact same functional code (`src/` and `tests/` from `ada08-baseline`), used the exact same `TASK_UNDER_TEST.md` (`CR-02`), the exact same verbatim English prompt, the same `coding-agent` definition, the same model (`Gemini 4 Argon (Medium)`), and the same toolset and permissions in two isolated clean sessions.
- **Uncontrolled Variables / Threats to Validity**:
  1. LLM generation has inherent stochasticity across independent sessions even with the same model and prompt.
  2. Running on Windows PowerShell meant `bash` was located at `D:\Git\bin\bash.exe` rather than default `PATH`; providing both `scripts/verify_repo.sh` and `scripts/verify_repo.ps1` in `AGENTS.md` ensured cross-shell parity between Windows local runs and Ubuntu CI.

---

## 5. Reflexión Individual (13 Preguntas — Sección 26)

1. **¿Cuál fue el principal obstáculo para el agente en la ejecución BEFORE?**
   El principal obstáculo no fue escribir el código en `src/service.py`, sino la **deuda de contexto y de higiene del repositorio**: el archivo normativo estaba mal escrito (`REQUERIMENTS.md` en vez de `REQUIREMENTS.md`), no existía un mapa que le indicara qué archivos ignorar ni que debía actualizar `docs/traceability.md`, los saltos de línea CRLF hicieron fallar su primera llamada a `edit_file`, y la ausencia de `.gitignore` provocó que al correr `pytest --cov=src` se ensuciaran 3 archivos binarios rastreados (`.coverage` y dos `.pyc`), degradando el resultado a `PARTIAL`.

2. **¿Qué información tuvo que inferir el agente que un desarrollador experimentado ya conocía?**
   Tuvo que inferir cinco piezas de conocimiento implícito (`IK-01` a `IK-05`): (1) que `REQUIREMENTS.md` en realidad se llamaba `REQUERIMENTS.md`, (2) que el punto de entrada era `src/cli.py` y no `search.py` como decía `ARCHITECTURE.md`, (3) que `pytest --cov=src tests/` era el comando de validación esperado, (4) que `data/customers.json` no debía tocarse porque las pruebas de `tests/test_search.py` usan `@patch('src.service.load_customers')`, y (5) que los archivos `.pyc` y `.coverage` estaban versionados por error en Git.

3. **¿Qué mejora produjo el mayor impacto y por qué?**
   La combinación de **`docs/REPO_MAP.md` (`Change Guide`) + `scripts/check_repo_contract.py` (invocado desde `scripts/verify_repo.sh` / `.ps1`)**. Mientras que `REPO_MAP.md` guio al agente directamente a los 3 archivos exactos (`src/service.py`, `tests/test_search.py`, `docs/traceability.md`) sin explorar módulos irrelevantes, `check_repo_contract.py` convirtió la regla de actualizar `docs/traceability.md` y mantener limpio el árbol de trabajo en una verificación determinista imposible de omitir.

4. **¿Qué información pertenece en `AGENTS.md` y qué información NO debería vivir ahí?**
   En `AGENTS.md` pertenece el **contrato operativo**: orden de lectura (`Read First`), cuáles son las fuentes de verdad (`Sources of Truth`), mapa resumido de carpetas, comandos estándar ejecutables (`Install`, `Run`, `Test`, `Verify`), reglas de cambio, *stop conditions* y *Definition of Done*. **NO** deben vivir ahí los requisitos detallados del negocio, las reglas de dominio completas ni la arquitectura extensa, ya que duplicarían `REQUIREMENTS.md`, `SPEC.md` y `ARCHITECTURE.md`.

5. **¿Qué regla convertiste en software/hook/script en lugar de dejarla como instrucción?**
   Convertimos cuatro reglas críticas en comprobaciones deterministas dentro de `scripts/check_repo_contract.py` y `.gitignore`: (1) que toda función `def test_*` en `tests/test_search.py` esté registrada en `docs/traceability.md`, (2) que `data/customers.json` no sufra modificaciones (`git diff`), (3) que ningún archivo `.pyc`, `__pycache__`, `.coverage` o `.env` esté rastreado en Git (`git ls-files`), y (4) que las funciones públicas de `src/service.py` y `src/storage.py` tengan anotaciones de tipos (`ast` check para `NFR-03`).

6. **¿Qué diferencia observaste entre 'más contexto' y 'mejor contexto'?**
   En `BEFORE`, el agente leyó *más* archivos de código y datos (15 archivos incluyendo `cli.py`, `storage.py`, `model.py`, `test_cli.py`, `test_storage.py`, `customers.json`) porque tuvo que explorar a ciegas, y aun así olvidó actualizar `docs/traceability.md`. En `AFTER`, con *mejor contexto* estructurado (`AGENTS.md` + `docs/REPO_MAP.md`), leyó únicamente los archivos pertinentes a su tarea, no inspeccionó capas irrelevantes, redujo los pasos de 39 a 31 y cumplió el 100% del Definition of Done.

7. **¿Qué riesgo aparece cuando `CLAUDE.md`/`GEMINI.md`/copilot instructions duplican información del proyecto?**
   Aparece el riesgo de **deriva de configuración (split-brain / segunda fuente de verdad)**: cuando un requisito o comando cambia en `REQUIREMENTS.md`, `SPEC.md` o `AGENTS.md`, los archivos específicos de cada herramienta quedan desactualizados y contradicen la fuente normativa, haciendo que distintos agentes (o humanos) sigan reglas incompatibles. Por ello `GEMINI.md` se diseñó exclusivamente como un adaptador ligero hacia `AGENTS.md`.

8. **¿Qué checks comparten ahora el agente, el desarrollador humano y CI?**
   Los tres ejecutan exactamente el mismo contrato de verificación (`scripts/verify_repo.sh` / `scripts/verify_repo.ps1` invocado también por `.github/workflows/verify.yml`):
   1. `python -m pytest -q --cov=src --cov-fail-under=90 tests/` (pruebas unitarias + umbral de cobertura $\ge 90\%$).
   2. `python -m compileall -q src tests scripts` (verificación sintáctica y de compilación).
   3. `python scripts/check_repo_contract.py` (integridad de archivos, secciones de `AGENTS.md`, IDs en `SPEC.md`, sincronización de `docs/traceability.md`, protección de `data/customers.json`, bloqueo de `.pyc`/`.coverage`/`.env` y chequeo AST de tipado estático).

9. **¿Qué parte del proceso sigue requiriendo decisión humana?**
   Siguen requiriendo decisión humana (definidas en `Stop Conditions` y `Human Gate`): (1) resolver conflictos normativos entre `REQUIREMENTS.md` y `SPEC.md` o definir nuevos requisitos de negocio (como las preguntas abiertas `Q-01` sobre búsqueda difusa y `Q-02` sobre historial), (2) autorizar cambios en límites arquitectónicos o nuevas dependencias externas (`C-01`), (3) autorizar modificaciones al dataset semilla `data/customers.json`, y (4) aprobar y fusionar Pull Requests en GitHub (la skill `reviewing-pull-requests` es estrictamente *Draft-Only*).

10. **¿Qué evidencia demuestra que el AFTER es realmente mejor?**
    La evidencia comparativa entre `results/before-agent-run.md` (`945f6ce`) y `results/after-agent-run.md` (`c301142`):
    - Los archivos fuera de alcance modificados bajaron de **3 a 0**.
    - Los fallos de herramientas/edición bajaron de **1 a 0**.
    - Las omisiones de proceso (actualizar `docs/traceability.md` y ejecutar validaciones de contrato/tipado) bajaron de **3 a 0**.
    - El agente dejó de explorar archivos irrelevantes (`cli.py`, `storage.py`, `customers.json`) y redujo su trayectoria de **39 a 31 pasos**, pasando de un resultado **PARTIAL** a **PASS**.

11. **¿Qué mejora realizada para el agente también beneficia a un desarrollador que entra por primera vez al proyecto?**
    Todas, pero especialmente `docs/REPO_MAP.md` (que explica en 30 segundos dónde está cada capa y qué pasos seguir según el tipo de cambio), `requirements.txt` y `scripts/verify_repo.sh` (que eliminan la incertidumbre de "qué comando debo correr antes de abrir un PR"), y la limpieza de `.gitignore` (que evita ensuciar `git status` con binarios `.pyc` y `.coverage` al correr pruebas localmente).

12. **¿Qué variable no controlada podría afectar tu comparación BEFORE/AFTER?**
    La naturaleza no determinista (estocástica) de inferencia del modelo LLM entre ejecuciones independientes y las diferencias del entorno operativo local (Windows PowerShell donde `bash` no está en el `PATH` por defecto, sino en `D:\Git\bin\bash.exe`, lo cual mitigamos proveyendo tanto `scripts/verify_repo.sh` como `scripts/verify_repo.ps1` con los mismos pasos).

13. **¿Qué elementos de este ADA conservarás como base para tu proyecto final?**
    Conservaré cinco pilares como plantilla base: (1) el contrato operativo en `AGENTS.md` con `Stop Conditions` y `Definition of Done` explícitos, (2) el mapa de navegación y guía de cambios en `docs/REPO_MAP.md`, (3) el script único de verificación (`scripts/verify_repo.sh`) compartido idénticamente con GitHub Actions (`.github/workflows/verify.yml`), (4) el script determinista de guardrails (`scripts/check_repo_contract.py`) que valida trazabilidad y rutas protegidas, y (5) la skill de revisión de PRs con *Human Gate* de ADA-07.
