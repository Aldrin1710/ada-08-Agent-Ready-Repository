# Reporte de Mejora de Preparación del Repositorio (`ADA-08`)

## 1. Resumen Ejecutivo
Este reporte documenta la evaluación empírica y la transformación del repositorio **Customer Search CLI** (`ada-05` / `ada-07`) en un **Agent-Ready Repository** (`ada-08-agent-ready-repository`).
- **Commit/tag de baseline**: `ada08-baseline` (`a0f667c`)
- **Tarea bajo prueba (`TASK_UNDER_TEST.md`)**: `CR-02` — Extender la detección de coincidencia exacta en `search_customers` (`src/service.py`) para incluir `last_name` (insensible a mayúsculas/minúsculas) junto con `name` y `email`, con desempate determinista por `id` ascendente tanto en coincidencias exactas como parciales, más pruebas unitarias en `tests/test_search.py`.
- **Mejora en el Score de Readiness**: **BEFORE: `39.0 / 100`** $\rightarrow$ **AFTER: `98.0 / 100`** (**Delta: `+59.0 puntos`**)
- **Mejora en el Resultado del Agente**: **BEFORE: `PARTIAL`** (39 pasos, 15 archivos leídos, 1 llamada fallida a `edit_file`, 3 archivos binarios fuera de alcance ensuciados, `docs/traceability.md` omitido) $\rightarrow$ **AFTER: `PASS`** (31 pasos, lecturas dirigidas vía `REPO_MAP.md`, 0 comandos/ediciones fallidas, 0 archivos fuera de alcance modificados, `docs/traceability.md` actualizado, `REPO_CONTRACT: PASS` y `VERIFY_REPO: PASS`).

---

## 2. Changes Made (Clasificación de Mejoras — Sección 10.1)

### Improvement I-01
- **Category**: `Context`
- **Problem**: `AGENTS.md` tenía solo 21 líneas, apuntaba a un archivo `REQUIREMENTS.md` inexistente (el archivo real se llamaba `REQUERIMENTS.md`), carecía de comandos estándar, no incluía un mapa del repositorio y tenía *stop conditions* y *Definition of Done* incompletos.
- **Change**: Se reescribió `AGENTS.md` como un contrato operativo conciso (`Read First`, `Sources of Truth`, `Repository Map`, `Standard Commands`, `Change Rules`, `Stop Conditions`, `Definition of Done`), se renombró `REQUERIMENTS.md` $\rightarrow$ `REQUIREMENTS.md` y se estandarizaron en inglés `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md` y `docs/traceability.md`.
- **Evidence**: En la ejecución AFTER, el agente leyó primero `AGENTS.md`, encontró `REQUIREMENTS.md` de inmediato sin errores y cumplió íntegramente las `Change Rules` y el `Definition of Done`.

### Improvement I-02
- **Category**: `Context` (Adaptador Tool-Specific y `Human Gate`)
- **Problem**: Los archivos específicos de herramienta (`GEMINI.md` y `.agents/skills/reviewing_pull_requests/SKILL.md`) o no existían o referenciaban el nombre mal escrito `REQUERIMENTS.md`.
- **Change**: Se creó `GEMINI.md` como adaptador ligero que apunta a `AGENTS.md` sin duplicar requisitos, y se actualizó `.agents/skills/reviewing_pull_requests/SKILL.md` (`v1.0.2`, `Human Gate` que impone revisiones en borrador de solo lectura y prohíbe `gh pr merge`).
- **Evidence**: `GEMINI.md` dirigió al agente en AFTER hacia `AGENTS.md`, `docs/REPO_MAP.md` y `scripts/verify_repo.ps1` sin duplicar requisitos del proyecto.

### Improvement I-03
- **Category**: `Navigation`
- **Problem**: No existía `docs/REPO_MAP.md` y `ARCHITECTURE.md` referenciaba un comando inexistente (`python search.py "termino"`). Durante BEFORE, el agente tuvo que ejecutar escaneos recursivos de directorios (`Get-ChildItem -Recurse`) y leer los 4 archivos de `src/*`, todos los de `tests/*` y `data/customers.json` (15 archivos en total).
- **Change**: Se creó `docs/REPO_MAP.md` con `Entry Points`, `Tests`, una guía paso a paso (`Change Guide`) y reglas `Do Not Edit Directly`, además de corregir `ARCHITECTURE.md`.
- **Evidence**: Durante AFTER, el agente leyó `docs/REPO_MAP.md` y fue directamente a `src/service.py`, `tests/test_search.py` y `docs/traceability.md`, omitiendo por completo los archivos irrelevantes (`src/cli.py`, `src/storage.py`, `src/model.py`, `tests/test_cli.py`, `tests/test_storage.py`, `data/customers.json`).

### Improvement I-04
- **Category**: `Executable Knowledge`
- **Problem**: La cobertura de pruebas ($\ge 90\%$ exigida por `NFR-03`), los chequeos estáticos de compilación/tipos y la validación del contrato del repositorio no estaban integrados en un único comando reproducible.
- **Change**: Se crearon `scripts/verify_repo.sh` (y su equivalente para Windows PowerShell `scripts/verify_repo.ps1`) junto con `requirements.txt` para ejecutar en secuencia: (1) `pytest -q --cov=src --cov-fail-under=90 tests/`, (2) `python -m compileall -q src tests scripts` y (3) `python scripts/check_repo_contract.py`.
- **Evidence**: En AFTER, el agente ejecutó `scripts/verify_repo.ps1` en un solo paso y obtuvo la salida determinista `REPO_CONTRACT: PASS` y `VERIFY_REPO: PASS`.

### Improvement I-05
- **Category**: `Guardrail`
- **Problem**: En BEFORE, el agente olvidó actualizar `docs/traceability.md` al agregar 2 pruebas unitarias en `tests/test_search.py`, y ningún chequeo determinista protegía `data/customers.json`, verificaba las anotaciones de tipos de `NFR-03` ni bloqueaba archivos `.pyc`/`.coverage` rastreados.
- **Change**: Se implementó `scripts/check_repo_contract.py` con 7 verificaciones deterministas: (1) existencia de archivos/carpetas esenciales, (2) secciones obligatorias en `AGENTS.md`, (3) referencias a `FR-01`..`FR-06` y `AC-01`..`AC-05` en `SPEC.md`, (4) registro en `docs/traceability.md` de toda función `def test_*` definida en `tests/test_search.py`, (5) cero archivos `.pyc`, `__pycache__`, `.coverage` o `.env` rastreados en Git, (6) cero modificaciones en `data/customers.json` (`git diff`), y (7) verificación vía AST de anotaciones de tipos en funciones públicas de `src/service.py` y `src/storage.py`.
- **Evidence**: En AFTER, el agente inspeccionó `scripts/check_repo_contract.py`, actualizó proactivamente `docs/traceability.md` junto con `tests/test_search.py` y aprobó `REPO_CONTRACT: PASS` en la primera ejecución.

### Improvement I-06
- **Category**: `Guardrail` (Higiene de Git y Normalización de Saltos de Línea)
- **Problem**: `.coverage` y `src/__pycache__/*.pyc` / `tests/__pycache__/*.pyc` estaban rastreados en Git, provocando que 3 archivos binarios fuera de alcance se ensuciaran durante BEFORE (`pytest --cov=src`). Además, los saltos CRLF y espacios al final de línea en `src/service.py` hicieron fallar a `edit_file` durante BEFORE.
- **Change**: Se eliminaron `__pycache__/` y `.coverage` del índice de Git (`git rm --cached`), se agregaron `.gitignore` y `.gitattributes` (`* text=auto eol=lf`), y se normalizaron los saltos de línea LF en `src/` y `tests/`.
- **Evidence**: En AFTER hubo `0` fallos de `edit_file` (frente a 1 fallo en BEFORE) y `0` archivos binarios fuera de alcance en `git status -s` (frente a 3 en BEFORE).

### Improvement I-07
- **Category**: `CI Check`
- **Problem**: No existía un pipeline de CI que ejecutara el mismo contrato de verificación fuera de la sesión local del agente.
- **Change**: Se creó `.github/workflows/verify.yml` activado en `push` y `pull_request`, que instala `requirements.txt` y ejecuta `bash ./scripts/verify_repo.sh`.
- **Evidence**: Desarrolladores humanos, el coding agent y GitHub Actions CI comparten ahora exactamente el mismo script único de verificación (`scripts/verify_repo.sh`).

---

## 3. Tabla Comparativa de Impacto (BEFORE vs AFTER)

| Indicador | BEFORE (`before-experiment` / `945f6ce`) | AFTER (`main` / `c301142`) |
|---|---|---|
| **Clarification questions** | `0` (procedió pese a la falta de `REQUIREMENTS.md` y la ambigüedad en `SPEC.md`) | `0` (`REQUIREMENTS.md` y `SPEC.md` alineados y explícitos) |
| **Failed / unknown commands** | `1` llamada fallida a `edit_file` en `src/service.py` (diferencia CRLF); sin comando único de verificación | `0` llamadas o comandos fallidos; ejecutó `scripts/verify_repo.ps1` directamente |
| **Incorrect assumptions** | `3` (omitió actualizar `docs/traceability.md`, asumió saltos LF, omitió chequeos estáticos/de contrato) | `0` (actualizó `src/service.py`, `tests/test_search.py` y `docs/traceability.md` simultáneamente) |
| **Out-of-scope files modified** | `3` archivos binarios ensuciados (`.coverage` y 2 archivos `.pyc` rastreados en Git) | `0` (`git status -s` limpio salvo por los 3 archivos objetivo) |
| **Validations executed correctly** | Parcial (únicamente `pytest --cov=src`) | Completa (`scripts/verify_repo.ps1`: 21 pruebas + gate de cobertura 96.55% + `compileall` + `check_repo_contract.py`) |
| **Pasos de trayectoria y exploración** | `39` pasos; `2` escaneos de directorios + `15` archivos leídos (incluyendo `cli.py`, `storage.py`, `customers.json`) | `31` pasos; `1` listado raíz + `13` lecturas dirigidas por `AGENTS.md` y `docs/REPO_MAP.md` |
| **Final result** | **PARTIAL** | **PASS** |
| **Readiness Audit Score** | **39.0 / 100** | **98.0 / 100** (**+59.0 pts**) |

---

## 4. Amenazas a la Validez y Variables Controladas
- **Variables mantenidas constantes**: Tanto BEFORE (`5b138d3d-6b95-4152-95d8-8db04fb55a83`) como AFTER (`d0a93548-2bce-482a-978f-b5217f33da5c`) partieron exactamente del mismo código funcional (`src/` y `tests/` de `ada08-baseline`), utilizaron la misma `TASK_UNDER_TEST.md` (`CR-02`), el mismo prompt oficial en inglés sin pistas adicionales, la misma definición de subagente (`coding-agent`), el mismo modelo (`Gemini 4 Argon (Medium)`) y las mismas herramientas y permisos en dos sesiones limpias independientes.
- **Variables no controladas / Amenazas a la validez**:
  1. La generación de los modelos LLM posee estocasticidad inherente entre sesiones independientes aun con el mismo modelo y prompt.
  2. La ejecución local en Windows PowerShell implicó que `bash` estuviera en `D:\Git\bin\bash.exe` y no en el `PATH` por defecto; proveer tanto `scripts/verify_repo.sh` como `scripts/verify_repo.ps1` en `AGENTS.md` garantizó paridad exacta entre ejecuciones locales en Windows y ejecuciones en Ubuntu CI.

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
