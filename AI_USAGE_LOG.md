# Bitácora de Uso de IA (`AI_USAGE_LOG.md` — `ADA-08` Agent-Ready Repository)

Esta bitácora documenta las decisiones de ingeniería relevantes, lo detectado por el agente frente a lo validado por el estudiante, y las sugerencias aceptadas o rechazadas durante el desarrollo de **ADA-08**.

---

## Entrada 1 — Auditoría Inicial de Preparación del Repositorio (`BEFORE`)
- **Fecha**: 2026-10-26
- **Contexto**: Auditar el repositorio base (`ada08-baseline`, commit `a0f667c`) en las 8 dimensiones de *Agent-Ready Repository* antes de ejecutar la tarea controlada `CR-02`.
- **Qué detectó el agente**:
  - `AGENTS.md` ordenaba leer `REQUIREMENTS.md`, pero el archivo en disco estaba mal escrito como `REQUERIMENTS.md`.
  - `ARCHITECTURE.md` referenciaba un punto de entrada de CLI inexistente (`python search.py "termino"`) y describía límites de validación/errores que no coincidían con `src/cli.py` ni `src/storage.py`.
  - `.coverage` y 11 archivos binarios compilados (`src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc`) estaban rastreados en Git sin existir un archivo `.gitignore`.
  - No existían `docs/REPO_MAP.md`, `scripts/verify_repo.sh`, `scripts/check_repo_contract.py`, `requirements.txt` ni `.github/workflows/verify.yml`.
- **Qué validó y decidió el humano**:
  - Se validaron todos los hallazgos contra el árbol real del repositorio y se calificó el estado inicial con **39.0 / 100** en `REPOSITORY_READINESS_AUDIT.md`.
  - Se definió `TASK_UNDER_TEST.md` (`CR-02`: coincidencia exacta también en `last_name` + desempate determinista por `id` ascendente) y se preservó el tag `ada08-baseline` antes de correr el experimento `BEFORE`.

---

## Entrada 2 — Ejecución `BEFORE` y Descubrimiento de Conocimiento Implícito (`Discoverability / Implicit Knowledge`)
- **Fecha**: 2026-10-26
- **Contexto**: Ejecución del subagente en sesión limpia (`5b138d3d-6b95-4152-95d8-8db04fb55a83`) sobre la rama `before-experiment` usando exactamente el prompt oficial en inglés de la Sección 9 de ADA-08.
- **Qué información estaba oculta y cómo afectó al agente**:
  - El agente tuvo que ejecutar 2 escaneos de directorios (`Get-ChildItem`) y leer 15 archivos (incluyendo módulos irrelevantes como `src/cli.py`, `src/storage.py`, `tests/test_cli.py`, `tests/test_storage.py` y `data/customers.json`) para comprender la estructura y localizar `REQUERIMENTS.md`.
  - Su primera llamada a `edit_file` sobre `src/service.py` falló por los saltos de línea CRLF y espacios al final de línea, obligándolo a sobrescribir todo el archivo con `write_file`.
  - Al ejecutar `pytest -v --cov=src tests/`, se modificaron 3 archivos binarios rastreados (`.coverage` y 2 archivos `.pyc`) en `git status`.
  - El agente omitió actualizar `docs/traceability.md` con las 2 nuevas pruebas unitarias.
- **Decisión humana (`results/implicit-knowledge.md`)**:
  - Se calificó la corrida `BEFORE` como **PARTIAL** en `results/before-agent-run.md` y se documentaron 5 hallazgos de conocimiento implícito (`IK-01`..`IK-05`), decidiendo convertir las reglas de estructura, trazabilidad e higiene en verificaciones ejecutables (`check_repo_contract.py` + `.gitignore`) en lugar de depender solo de texto en Markdown.

---

## Entrada 3 — Diseño de `AGENTS.md` y Adaptador `GEMINI.md`
- **Fecha**: 2026-10-26
- **Contexto**: Diseño de la Mejora `I-01` (`AGENTS.md`) y la Mejora `I-02` (`GEMINI.md`).
- **Sugerencias aceptadas**:
  - Se incluyeron las 7 secciones operativas esenciales en `AGENTS.md` (redactado en inglés según la convención 6.1): `Read First`, `Sources of Truth`, `Repository Map`, `Standard Commands`, `Change Rules`, `Stop Conditions` y `Definition of Done`.
  - Se documentaron explícitamente tanto el comando en Git Bash (`D:\Git\bin\bash.exe scripts/verify_repo.sh` / `./scripts/verify_repo.sh`) como el wrapper equivalente en PowerShell (`pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify_repo.ps1`) tras validar que `bash` no estaba en el `PATH` por defecto de Windows.
- **Sugerencias rechazadas**:
  - Se rechazó copiar las reglas detalladas de búsqueda (`SR-01`..`SR-03`) o la matriz de trazabilidad dentro de `AGENTS.md` o `GEMINI.md`, evitando crear una segunda fuente de verdad que pudiera contradecir a `REQUIREMENTS.md`, `SPEC.md` o `docs/traceability.md`.

---

## Entrada 4 — Guardrail: Qué Regla se Convirtió a Software y Por Qué (`check_repo_contract.py`)
- **Fecha**: 2026-10-26
- **Contexto**: Diseño de la Mejora `I-05` (`scripts/check_repo_contract.py`) y la Mejora `I-06` (`.gitignore` / `.gitattributes`).
- **Por qué convertirla a software en lugar de instrucción natural**:
  - En `BEFORE`, `AGENTS.md` ya decía en lenguaje natural *"Documentation reflects final behavior"* y *"No unrelated files are changed"*, pero el agente aun así olvidó actualizar `docs/traceability.md` y ensució `.coverage` y `*.pyc`.
- **Reglas convertidas en chequeos deterministas en `scripts/check_repo_contract.py`**:
  1. Verificación con expresiones regulares de que toda función `def test_*` en `tests/test_search.py` aparezca registrada en `docs/traceability.md`.
  2. Chequeo con `git ls-files` que falla si cualquier archivo `.pyc`, `__pycache__`, `.coverage` o `.env` está rastreado en Git.
  3. Chequeo de ruta protegida con `git diff` que asegura que `data/customers.json` no haya sido modificado.
  4. Chequeo de análisis sintáctico (AST) que verifica que las funciones públicas en `src/service.py` y `src/storage.py` tengan anotaciones de tipo en sus parámetros y retorno (`NFR-03`).

---

## Entrada 5 — CI: Verificaciones Compartidas entre Humano, Agente y Pipeline (`verify_repo.sh` y `.github/workflows/verify.yml`)
- **Fecha**: 2026-10-26
- **Contexto**: Diseño de la Mejora `I-04` (`scripts/verify_repo.sh`) y la Mejora `I-07` (`.github/workflows/verify.yml`).
- **Qué verificaciones se decidió compartir y por qué**:
  - Se decidió que humano, agente y CI compartan exactamente los mismos 3 pasos a través de `scripts/verify_repo.sh`: (1) `pytest -q --cov=src --cov-fail-under=90 tests/`, (2) `python -m compileall -q src tests scripts` y (3) `python scripts/check_repo_contract.py`.
  - `.github/workflows/verify.yml` instala `requirements.txt` e invoca directamente `bash ./scripts/verify_repo.sh` sin duplicar lógica dentro del YAML, garantizando un único contrato ejecutable compartido.

---

## Entrada 6 — Ejecución `AFTER`: Qué Cambió en el Comportamiento del Agente
- **Fecha**: 2026-10-26
- **Contexto**: Restauración del código funcional base (`src/` y `tests/` de `ada08-baseline`), aplicación exclusiva de las mejoras de *Repository Readiness* (`21cc88a`) y ejecución de una nueva sesión limpia de `coding-agent` (`d0a93548-2bce-482a-978f-b5217f33da5c`) con el mismo prompt y `TASK_UNDER_TEST.md`.
- **Cambios observados en el comportamiento del agente**:
  - El agente siguió `AGENTS.md` $\rightarrow$ `docs/REPO_MAP.md`, omitió todos los módulos irrelevantes (`cli.py`, `storage.py`, `model.py`, `customers.json`), editó `src/service.py`, `tests/test_search.py` y `docs/traceability.md` en un solo turno con `0` llamadas fallidas, ejecutó `scripts/verify_repo.ps1` (`REPO_CONTRACT: PASS`, `VERIFY_REPO: PASS`) y finalizó en 31 pasos (vs. 39 en BEFORE) con `0` archivos fuera de alcance modificados (**Resultado Final: `PASS`**).

---

## Entrada 7 — Evaluación Final: Qué Limitación Sigue Requiriendo Intervención Humana
- **Fecha**: 2026-10-26
- **Contexto**: Cierre de `REPOSITORY_READINESS_AUDIT.md` (`AFTER: 98.0 / 100`, `Delta: +59.0`) y `results/readiness-improvement-report.md`.
- **Límites que siguen requiriendo decisión humana (`Human Gate`)**:
  - Resolver ambigüedades de negocio (`Q-01` sobre búsqueda difusa, `Q-02` sobre historial de búsquedas) o posibles contradicciones futuras entre `REQUIREMENTS.md` y `SPEC.md`.
  - Aprobar cambios en los límites de arquitectura (`ARCHITECTURE.md`), la introducción de dependencias externas de ejecución (`C-01`) o cambios al dataset semilla protegido (`data/customers.json`).
  - Aprobar y hacer merge de Pull Requests en GitHub (restringido explícitamente como *Human Gate* por `.agents/skills/reviewing_pull_requests/SKILL.md`).
