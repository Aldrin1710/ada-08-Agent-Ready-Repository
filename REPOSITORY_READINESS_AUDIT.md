# Repository Readiness Audit

## BEFORE

| Dimension | Score 0-5 | Weighted | Evidence | Main Gap |
|---|---:|---:|---|---|
| Entry Point & Navigation | 2 | 6.0 / 15 | El README indica cómo ejecutar la aplicación desde src/cli.py, pero el documento de arquitectura menciona un archivo search.py que no existe. Tampoco hay un mapa del repositorio. | Falta un mapa de navegación y la documentación contradice el punto de entrada real. |
| Agent Instructions | 2 | 6.0 / 15 | El archivo AGENTS.md solo tiene reglas generales y pide leer REQUIREMENTS.md, el cual tiene un error ortográfico en su nombre real (REQUERIMENTS.md). | Referencia rota al archivo de requerimientos, sin comandos exactos ni condiciones claras para detenerse. |
| Build / Run / Test | 2 | 6.0 / 15 | Se menciona el uso de pytest, pero no existe un script único de validación ni están documentados los comandos para verificar el tipado estático que exigen los requerimientos. | No hay un comando único reproducible que integre todas las validaciones del proyecto. |
| Architecture Boundaries | 2 | 4.0 / 10 | La arquitectura describe tres capas separadas, pero en el código la capa de almacenamiento imprime errores en consola y cierra el programa directamente. | Las responsabilidades reales del código no coinciden del todo con la arquitectura documentada y no se indican qué archivos no deben tocarse. |
| Requirements & Traceability | 2 | 4.0 / 10 | Los documentos usan identificadores para conectar requisitos y pruebas, pero el archivo principal tiene el nombre mal escrito y la especificación omite el apellido en las coincidencias exactas. | Error en el nombre del archivo fuente de verdad y ligera contradicción entre los requerimientos y la especificación. |
| Automation & Guardrails | 1 | 2.0 / 10 | No hay scripts que validen las reglas del repositorio ni archivo gitignore, por lo que los binarios compilados de Python y el reporte de cobertura están subidos al control de versiones. | Ausencia total de validaciones automáticas y presencia de archivos basura rastreados en el repositorio. |
| Testability & Evidence | 3 | 9.0 / 15 | El proyecto cuenta con 19 pruebas unitarias funcionales y buena cobertura, pero carece de una validación automática que compruebe el estado general del repositorio al terminar. | Existen buenas pruebas unitarias, pero falta automatizar la comprobación de los criterios de entrega. |
| Safety & Permissions | 1 | 2.0 / 10 | No existen reglas explícitas en las instrucciones generales para proteger la base de datos JSON de prueba ni mecanismos que detecten si fue alterada por accidente. | Falta definir rutas protegidas y agregar validaciones que impidan modificar datos semilla o subir archivos sensibles. |

TOTAL BEFORE: 39.0 / 100

Top 3 friction points:
1. Documentación con referencias rotas y falta de un mapa del proyecto, lo que obliga al agente a buscar archivo por archivo para entender la estructura y encontrar el documento de requerimientos mal escrito.
2. Archivos compilados de Python y reportes de cobertura rastreados en el control de versiones, provocando que cualquier ejecución de pruebas ensucie el repositorio con cambios fuera del alcance de la tarea.
3. Falta de un script único de verificación que valide pruebas, sintaxis y reglas del proyecto en un solo paso.

## AFTER

| Dimension | Score 0-5 | Weighted | Evidence | Improvement |
|---|---:|---:|---|---|
| Entry Point & Navigation | 5 | 15.0 / 15 | Se agregó el mapa del repositorio en docs/REPO_MAP.md y se corrigieron las rutas en la documentación. El agente localizó de inmediato los archivos a modificar sin revisar módulos ajenos. | Creación del mapa del repositorio con guía de cambios y corrección de referencias en la arquitectura. |
| Agent Instructions | 5 | 15.0 / 15 | El nuevo AGENTS.md establece el orden de lectura, las fuentes de verdad, los comandos oficiales, las restricciones de edición, cuándo pedir ayuda humana y la definición de terminado. | Reescritura completa de AGENTS.md como contrato operativo claro y directo. |
| Build / Run / Test | 5 | 15.0 / 15 | Se implementó el script scripts/verify_repo.sh que ejecuta las pruebas automatizadas, la revisión sintáctica y el contrato del repositorio en un solo comando. | Creación de un único script reproducible para validar todo el proyecto. |
| Architecture Boundaries | 5 | 10.0 / 10 | Se alineó la documentación de arquitectura con el comportamiento real de los módulos y se delimitó explícitamente qué carpetas y archivos de datos no deben modificarse. | Actualización de límites arquitectónicos y definición de archivos protegidos en el mapa del repositorio. |
| Requirements & Traceability | 5 | 10.0 / 10 | Se corrigió el nombre de REQUIREMENTS.md, se estandarizaron los documentos técnicos en inglés y se eliminó la contradicción sobre la búsqueda exacta por apellido. | Corrección del nombre del archivo de requisitos, alineación con la especificación y validación automática de identificadores. |
| Automation & Guardrails | 5 | 10.0 / 10 | Se creó scripts/check_repo_contract.py y se limpiaron los archivos binarios del historial activo, evitando que se generen cambios accidentales al correr las pruebas. | Implementación del validador de contrato del repositorio y limpieza de archivos generados. |
| Testability & Evidence | 5 | 15.0 / 15 | La batería subió a 21 pruebas pasando en su totalidad y el script de verificación comprueba tanto las pruebas como las anotaciones de tipos y las reglas del repositorio. | Integración de pruebas unitarias, análisis estático de tipos y verificación estructural en una sola salida. |
| Safety & Permissions | 4 | 8.0 / 10 | Se definieron condiciones claras de paro en AGENTS.md y el script de contrato verifica que la base de datos de clientes no sea alterada ni se suban archivos prohibidos. | Protección automática del archivo JSON de clientes y bloqueo de archivos temporales o sensibles. |

TOTAL AFTER: 98.0 / 100
DELTA: AFTER - BEFORE = +59.0 points
