# Reporte de Mejora de Preparación del Repositorio (`ADA-08`)

## 1. Resumen Ejecutivo
Este reporte documenta la evaluación empírica y la transformación del repositorio **Customer Search CLI** (`ada-05` / `ada-07`) en un **Repositorio Preparado para Agentes (`Agent-Ready Repository`)** (`ada-08-agent-ready-repository`).
- **Commit/tag de línea base**: `ada08-baseline` (`a0f667c`)
- **Tarea bajo prueba (`TASK_UNDER_TEST.md`)**: `CR-02` — Extender la detección de coincidencia exacta en `search_customers` (`src/service.py`) para incluir `last_name` (insensible a mayúsculas/minúsculas) junto con `name` y `email`, con desempate determinista por `id` ascendente tanto en coincidencias exactas como parciales, más pruebas unitarias en `tests/test_search.py`.
- **Mejora en el Puntaje de Preparación**: **BEFORE: `39.0 / 100`** $\rightarrow$ **AFTER: `98.0 / 100`** (**Delta: `+59.0 puntos`**)
- **Mejora en el Resultado del Agente**: **BEFORE: `PARTIAL`** (39 pasos, 15 archivos leídos, 1 llamada fallida a `edit_file`, 3 archivos binarios fuera de alcance ensuciados) $\rightarrow$ **AFTER: `PASS`** (31 pasos, lecturas dirigidas vía `REPO_MAP.md`, 0 comandos/ediciones fallidas, 0 archivos fuera de alcance modificados, `REPO_CONTRACT: PASS` y `VERIFY_REPO: PASS`).

---

## 2. Conocimiento Implícito Detectado (`Implicit Knowledge Found` — Sección 9.1)

### IK-01
- **Qué era (`What`)**: El archivo fuente de verdad de requisitos se llamaba `REQUERIMENTS.md` (con error ortográfico) en lugar de `REQUIREMENTS.md` como lo referenciaban `AGENTS.md` y `TASK_UNDER_TEST.md`.
- **Cómo se descubrió (`How was it discovered`)**: Ejecutando `Get-ChildItem -Force` en la raíz del repositorio antes de intentar leer `REQUIREMENTS.md`.
- **¿Debería permanecer implícito?**: NO
- **Dónde se hizo explícito**: Se renombró a `REQUIREMENTS.md` y se validó su existencia de forma determinista mediante `scripts/check_repo_contract.py` y `AGENTS.md`.

### IK-02
- **Qué era (`What`)**: Los archivos de bytecode compilado (`src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc`) y `.coverage` estaban rastreados por error en Git, por lo que ejecutar `pytest --cov=src` contaminaba `git status` con cambios binarios fuera de alcance.
- **Cómo se descubrió (`How was it discovered`)**: Después de ejecutar `pytest -v --cov=src tests/; git status -s` al final de la corrida BEFORE.
- **Riesgo (`Risk`)**: El agente modificaba artefactos binarios no relacionados en cada ejecución de pruebas, violando el Definition of Done (*"No unrelated files are changed"*).
- **Remediación (`Remediation`)**: Se eliminaron `__pycache__/` y `.coverage` del índice de Git (`git rm --cached`), se configuró `PYTHONDONTWRITEBYTECODE=1` en `scripts/verify_repo.sh` y se agregó un guardrail determinista en `scripts/check_repo_contract.py`.

### IK-03
- **Qué era (`What`)**: El punto de entrada real de la CLI era `src/cli.py`, NO `search.py` como afirmaba `ARCHITECTURE.md` (`python search.py "termino"`), y las validaciones de entrada (`VR-01`, `VR-02`) vivían en `src/cli.py` mientras que el manejo de error de esquema JSON (`EH-02`) vivía en `src/storage.py`.
- **Cómo se descubrió (`How was it discovered`)**: Leyendo los 4 archivos dentro de `src/` (`cli.py`, `service.py`, `storage.py`, `model.py`) y comparándolos contra `ARCHITECTURE.md` y `README.md`.
- **Riesgo (`Risk`)**: Un agente que confiara en `ARCHITECTURE.md` buscaría un archivo `search.py` inexistente o colocaría la lógica en el módulo equivocado.
- **Remediación (`Remediation`)**: Se actualizó `ARCHITECTURE.md` y se creó `docs/REPO_MAP.md` con los puntos de entrada exactos, responsabilidades por capa y una Guía de Cambios paso a paso.

### IK-04
- **Qué era (`What`)**: Verificar `NFR-03` (pruebas automatizadas + verificación estática de tipos/sintaxis) y el contrato del repositorio requería comandos que no aparecían en `AGENTS.md`.
- **Cómo se descubrió (`How was it discovered`)**: Cruzando manualmente la información de `README.md` y `REQUERIMENTS.md` (`NFR-03`).
- **¿Debería permanecer implícito?**: NO
- **Dónde se hizo explícito**: En `AGENTS.md` (sección `Standard Commands`) y en `scripts/verify_repo.sh`.

### IK-05
- **Qué era (`What`)**: `data/customers.json` es el dataset semilla utilizado por las pruebas de la CLI (`tests/test_cli.py`), y no debe modificarse al agregar pruebas unitarias (las pruebas en `tests/test_search.py` deben usar mocks sobre `src.service.load_customers`).
- **Cómo se descubrió (`How was it discovered`)**: Inspeccionando `tests/test_search.py`, `tests/test_cli.py` y `data/customers.json`.
- **Riesgo (`Risk`)**: Un agente podría editar `data/customers.json` para probar casos borde, rompiendo las pruebas existentes de la CLI.
- **Remediación (`Remediation`)**: Se documentó `data/customers.json` bajo `Do Not Edit Directly` en `docs/REPO_MAP.md` y `AGENTS.md`, y se implementó una verificación determinista con `git diff` sobre `data/customers.json` dentro de `scripts/check_repo_contract.py`.

---

## 3. Cambios Realizados (`Changes Made` — Clasificación de Mejoras Sección 10.1)

### Mejora I-01 (`Improvement I-01`)
- **Categoría (`Category`)**: `Context`
- **Problema (`Problem`)**: `AGENTS.md` tenía solo 21 líneas, apuntaba a un archivo `REQUIREMENTS.md` inexistente (el archivo real se llamaba `REQUERIMENTS.md`), carecía de comandos estándar, no incluía un mapa del repositorio y tenía condiciones de paro y *Definition of Done* incompletos.
- **Cambio (`Change`)**: Se reescribió `AGENTS.md` como un contrato operativo conciso (`Read First`, `Sources of Truth`, `Repository Map`, `Standard Commands`, `Change Rules`, `Stop Conditions`, `Definition of Done`), se renombró `REQUERIMENTS.md` $\rightarrow$ `REQUIREMENTS.md` y se estandarizaron en inglés `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md` y `TASKS.md`.
- **Evidencia (`Evidence`)**: En la ejecución AFTER, el agente leyó primero `AGENTS.md`, encontró `REQUIREMENTS.md` de inmediato sin errores y cumplió íntegramente las reglas de cambio y el *Definition of Done*.

### Mejora I-02 (`Improvement I-02`)
- **Categoría (`Category`)**: `Navigation`
- **Problema (`Problem`)**: No existía `docs/REPO_MAP.md` y `ARCHITECTURE.md` referenciaba un comando inexistente (`python search.py "termino"`). Durante BEFORE, el agente tuvo que ejecutar escaneos recursivos de directorios (`Get-ChildItem -Recurse`) y leer los 4 archivos de `src/*`, todos los de `tests/*` y `data/customers.json` (15 archivos en total).
- **Cambio (`Change`)**: Se creó `docs/REPO_MAP.md` con puntos de entrada (`Entry Points`), pruebas (`Tests`), una guía paso a paso (`Change Guide`) y reglas de archivos protegidos (`Do Not Edit Directly`), además de corregir `ARCHITECTURE.md`.
- **Evidencia (`Evidence`)**: Durante AFTER, el agente leyó `docs/REPO_MAP.md` y fue directamente a `src/service.py` y `tests/test_search.py`, omitiendo por completo los archivos irrelevantes (`src/cli.py`, `src/storage.py`, `src/model.py`, `tests/test_cli.py`, `tests/test_storage.py`, `data/customers.json`).

### Mejora I-03 (`Improvement I-03`)
- **Categoría (`Category`)**: `Executable Knowledge`
- **Problema (`Problem`)**: La ejecución de pruebas, los chequeos estáticos de compilación/tipos (`NFR-03`) y la validación del contrato del repositorio no estaban integrados en un único comando reproducible.
- **Cambio (`Change`)**: Se creó `scripts/verify_repo.sh` para ejecutar en secuencia: (1) `python -B -m pytest -q -p no:cacheprovider tests/`, (2) verificación sintáctica AST sobre `src/`, `tests/` y `scripts/`, y (3) `python -B scripts/check_repo_contract.py`.
- **Evidencia (`Evidence`)**: En AFTER, el agente ejecutó la verificación unificada en un solo paso y obtuvo la salida determinista `REPO_CONTRACT: PASS` y `VERIFY_REPO: PASS`.

### Mejora I-04 (`Improvement I-04`)
- **Categoría (`Category`)**: `Guardrail`
- **Problema (`Problem`)**: En BEFORE, ningún chequeo determinista validaba los archivos esenciales del repositorio, protegía `data/customers.json`, verificaba las anotaciones de tipos de `NFR-03` ni bloqueaba archivos `.pyc`/`.coverage` rastreados en Git.
- **Cambio (`Change`)**: Se implementó `scripts/check_repo_contract.py` con verificaciones deterministas: (1) existencia de archivos/carpetas esenciales, (2) secciones obligatorias en `AGENTS.md`, (3) referencias a `FR-01`..`FR-06` y `AC-01`..`AC-05` en `SPEC.md`, (4) cero archivos `.pyc`, `__pycache__`, `.coverage` o `.env` rastreados en Git, (5) cero modificaciones en `data/customers.json` (`git diff`), y (6) verificación vía AST de anotaciones de tipos en funciones públicas de `src/service.py` y `src/storage.py`.
- **Evidencia (`Evidence`)**: En AFTER, `scripts/check_repo_contract.py` validó todo el contrato automáticamente y reportó `REPO_CONTRACT: PASS`.

### Mejora I-05 (`Improvement I-05`)
- **Categoría (`Category`)**: `Guardrail` / `Human Gate`
- **Problema (`Problem`)**: `.coverage` y `src/__pycache__/*.pyc` / `tests/__pycache__/*.pyc` estaban rastreados en Git, provocando que 3 archivos binarios fuera de alcance se ensuciaran durante BEFORE. Además, los saltos CRLF en `src/service.py` hicieron fallar a `edit_file` durante BEFORE.
- **Cambio (`Change`)**: Se eliminaron `__pycache__/` y `.coverage` del índice de Git (`git rm --cached`), se normalizaron los saltos de línea LF en `src/` y `tests/`, y se establecieron `Stop Conditions` explícitas en `AGENTS.md` para reservar decisiones de alto impacto a revisión humana.
- **Evidencia (`Evidence`)**: En AFTER hubo `0` fallos de `edit_file` (frente a 1 fallo en BEFORE) y `0` archivos binarios fuera de alcance en `git status -s` (frente a 3 en BEFORE).

---

## 4. Tabla Comparativa de Impacto (`BEFORE` vs `AFTER`)

| Indicador | BEFORE (`before-experiment` / `945f6ce`) | AFTER (`main` / `c301142`) |
|---|---|---|
| **Preguntas de aclaración (`Clarification questions`)** | `0` (procedió pese a la falta de `REQUIREMENTS.md` y la ambigüedad en `SPEC.md`) | `0` (`REQUIREMENTS.md` y `SPEC.md` alineados y explícitos) |
| **Comandos fallidos / desconocidos (`Failed / unknown commands`)** | `1` llamada fallida a `edit_file` en `src/service.py` (diferencia CRLF); sin comando único de verificación | `0` llamadas o comandos fallidos; ejecutó la verificación directamente |
| **Suposiciones incorrectas (`Incorrect assumptions`)** | `3` (omitió actualizar trazabilidad, asumió saltos LF, omitió chequeos estáticos/de contrato) | `0` (aplicó todos los cambios requeridos en el primer intento) |
| **Archivos fuera de alcance modificados (`Out-of-scope files modified`)** | `3` archivos binarios ensuciados (`.coverage` y 2 archivos `.pyc` rastreados en Git) | `0` (`git status -s` limpio salvo por los archivos objetivo) |
| **Validaciones ejecutadas correctamente (`Validations executed correctly`)** | Parcial (únicamente `pytest --cov=src`) | Completa (`scripts/verify_repo.sh`: 21 pruebas + chequeo AST + `check_repo_contract.py`) |
| **Pasos de trayectoria y exploración** | `39` pasos; `2` escaneos de directorios + `15` archivos leídos (incluyendo `cli.py`, `storage.py`, `customers.json`) | `31` pasos; lecturas dirigidas por `AGENTS.md` y `docs/REPO_MAP.md` |
| **Resultado final (`Final result`)** | **PARTIAL** | **PASS** |
| **Puntaje de Auditoría (`Readiness Audit Score`)** | **39.0 / 100** | **98.0 / 100** (**+59.0 pts**) |

---

## 5. Reflexión Individual (13 Preguntas — Sección 26)

1. **¿Cuál fue el principal obstáculo para el agente en la ejecución BEFORE?**
   El principal obstáculo no fue escribir el código en `src/service.py`, sino la **deuda de contexto y de higiene del repositorio**: el archivo normativo estaba mal escrito (`REQUERIMENTS.md` en vez de `REQUIREMENTS.md`), no existía un mapa que le indicara qué archivos ignorar, los saltos de línea CRLF hicieron fallar su primera llamada a `edit_file`, y los archivos `.coverage` y `.pyc` rastreados en Git hicieron que al correr `pytest` se ensuciaran 3 archivos binarios fuera de alcance, degradando el resultado a `PARTIAL`.

2. **¿Qué información tuvo que inferir el agente que un desarrollador experimentado ya conocía?**
   Tuvo que inferir cinco piezas de conocimiento implícito (`IK-01` a `IK-05`): (1) que `REQUIREMENTS.md` en realidad se llamaba `REQUERIMENTS.md`, (2) que el punto de entrada era `src/cli.py` y no `search.py` como decía `ARCHITECTURE.md`, (3) qué comando de pruebas ejecutar, (4) que `data/customers.json` no debía tocarse porque las pruebas de `tests/test_search.py` usan `@patch('src.service.load_customers')`, y (5) que los archivos `.pyc` y `.coverage` estaban versionados por error en Git.

3. **¿Qué mejora produjo el mayor impacto y por qué?**
   La combinación de **`docs/REPO_MAP.md` (`Change Guide`) + `scripts/check_repo_contract.py` (invocado desde `scripts/verify_repo.sh`)**. Mientras que `REPO_MAP.md` guio al agente directamente a los archivos exactos (`src/service.py` y `tests/test_search.py`) sin explorar módulos irrelevantes, `check_repo_contract.py` convirtió la validación del contrato y la limpieza del árbol de trabajo en una verificación determinista.

4. **¿Qué información pertenece en `AGENTS.md` y qué información NO debería vivir ahí?**
   En `AGENTS.md` pertenece el **contrato operativo**: orden de lectura (`Read First`), cuáles son las fuentes de verdad (`Sources of Truth`), mapa resumido de carpetas, comandos estándar ejecutables (`Install`, `Run`, `Test`, `Verify`), reglas de cambio, *stop conditions* y *Definition of Done*. **NO** deben vivir ahí los requisitos detallados del negocio, las reglas de dominio completas ni la arquitectura extensa, ya que duplicarían `REQUIREMENTS.md`, `SPEC.md` y `ARCHITECTURE.md`.

5. **¿Qué regla convertiste en software/hook/script en lugar de dejarla como instrucción?**
   Convertimos reglas críticas en comprobaciones deterministas dentro de `scripts/check_repo_contract.py` y `scripts/verify_repo.sh`: (1) que todos los archivos esenciales e IDs de `SPEC.md` existan, (2) que `data/customers.json` no sufra modificaciones (`git diff`), (3) que ningún archivo `.pyc`, `__pycache__`, `.coverage` o `.env` esté rastreado en Git (`git ls-files`), y (4) que las funciones públicas de `src/service.py` y `src/storage.py` tengan anotaciones de tipos (`ast` check para `NFR-03`).

6. **¿Qué diferencia observaste entre 'más contexto' y 'mejor contexto'?**
   En `BEFORE`, el agente leyó *más* archivos de código y datos (15 archivos incluyendo `cli.py`, `storage.py`, `model.py`, `test_cli.py`, `test_storage.py`, `customers.json`) porque tuvo que explorar a ciegas. En `AFTER`, con *mejor contexto* estructurado (`AGENTS.md` + `docs/REPO_MAP.md`), leyó únicamente los archivos pertinentes a su tarea, no inspeccionó capas irrelevantes, redujo los pasos de 39 a 31 y cumplió el 100% del Definition of Done.

7. **¿Qué riesgo aparece cuando `CLAUDE.md`/`GEMINI.md`/copilot instructions duplican información del proyecto?**
   Aparece el riesgo de **deriva de configuración (segunda fuente de verdad)**: cuando un requisito o comando cambia en `REQUIREMENTS.md`, `SPEC.md` o `AGENTS.md`, los archivos específicos de cada herramienta quedan desactualizados y contradicen la fuente normativa, haciendo que distintos agentes (o humanos) sigan reglas incompatibles.

8. **¿Qué checks comparten ahora el agente, el desarrollador humano y CI?**
   Comparten exactamente el mismo contrato de verificación (`scripts/verify_repo.sh`):
   1. `python -B -m pytest -q -p no:cacheprovider tests/` (ejecución completa de la suite de 21 pruebas unitarias y de integración).
   2. Verificación sintáctica AST sobre `src/`, `tests/` y `scripts/`.
   3. `python -B scripts/check_repo_contract.py` (integridad de archivos, secciones de `AGENTS.md`, IDs en `SPEC.md`, protección de `data/customers.json`, bloqueo de `.pyc`/`.coverage`/`.env` y chequeo AST de tipado estático).

9. **¿Qué parte del proceso sigue requiriendo decisión humana?**
   Siguen requiriendo decisión humana (definidas en `Stop Conditions` y `Human Gate`): (1) resolver conflictos normativos entre `REQUIREMENTS.md` y `SPEC.md` o definir nuevos requisitos de negocio (como las preguntas abiertas `Q-01` sobre búsqueda difusa y `Q-02` sobre historial), (2) autorizar cambios en límites arquitectónicos o nuevas dependencias externas (`C-01`), y (3) autorizar modificaciones al dataset semilla `data/customers.json`.

10. **¿Qué evidencia demuestra que el AFTER es realmente mejor?**
    La evidencia comparativa entre `results/before-agent-run.md` (`945f6ce`) y `results/after-agent-run.md` (`c301142`):
    - Los archivos fuera de alcance modificados bajaron de **3 a 0**.
    - Los fallos de herramientas/edición bajaron de **1 a 0**.
    - El agente dejó de explorar archivos irrelevantes (`cli.py`, `storage.py`, `customers.json`) y redujo su trayectoria de **39 a 31 pasos**, pasando de un resultado **PARTIAL** a **PASS**.

11. **¿Qué mejora realizada para el agente también beneficia a un desarrollador que entra por primera vez al proyecto?**
    Especialmente `docs/REPO_MAP.md` (que explica en 30 segundos dónde está cada capa y qué pasos seguir según el tipo de cambio), `scripts/verify_repo.sh` (que elimina la incertidumbre de qué comando correr antes de entregar un cambio) y la eliminación de binarios `.pyc` y `.coverage` del control de versiones.

12. **¿Qué variable no controlada podría afectar tu comparación BEFORE/AFTER?**
    La naturaleza no determinista (estocástica) de inferencia del modelo LLM entre ejecuciones independientes y las diferencias del entorno operativo local en Windows.

13. **¿Qué elementos de este ADA conservarás como base para tu proyecto final?**
    Conservaré cuatro pilares como plantilla base: (1) el contrato operativo en `AGENTS.md` con `Stop Conditions` y `Definition of Done` explícitos, (2) el mapa de navegación y guía de cambios en `docs/REPO_MAP.md`, (3) el script único de verificación (`scripts/verify_repo.sh`), y (4) el script determinista de guardrails (`scripts/check_repo_contract.py`) que valida fuentes de verdad y rutas protegidas.
