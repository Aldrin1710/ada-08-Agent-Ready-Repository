# AI Usage Log

## Entry 01 - Auditoría inicial del repositorio
Stage: Audit BEFORE
Prompt/goal: Revisar el estado inicial del repositorio heredado de las actividades anteriores para calificar las ocho dimensiones de preparación antes de ejecutar al agente.
AI contribution: El asistente inspeccionó los archivos y el historial de Git, detectando que AGENTS.md apuntaba a un archivo REQUIREMENTS.md mal escrito en disco como REQUERIMENTS.md, que ARCHITECTURE.md mencionaba un archivo search.py inexistente y que había archivos compilados de Python y de cobertura subidos al repositorio.
Student decision: Validé cada uno de los hallazgos revisando los archivos del proyecto y asigné la calificación inicial de 39 sobre 100 en la tabla de auditoría, dejando documentados los tres puntos principales de fricción antes de tocar cualquier archivo.
Impact: Se estableció una línea base honesta y medible sobre el código original mediante el tag ada08-baseline.

## Entry 02 - Ejecución BEFORE e identificación de conocimiento implícito
Stage: BEFORE Execution & Implicit Knowledge
Prompt/goal: Ejecutar la tarea controlada CR-02 (incluir el apellido en las coincidencias exactas y desempatar por id ascendente) en una sesión limpia usando únicamente el prompt oficial.
AI contribution: El agente implementó correctamente la lógica en src/service.py y agregó dos pruebas en tests/test_search.py, pero durante el proceso tuvo que explorar quince archivos para ubicarse, falló en su primer intento de edición por los saltos de línea del archivo y al correr pytest ensució tres archivos binarios que estaban rastreados en Git.
Student decision: Evalué el resultado de la corrida como parcial porque, aunque las pruebas pasaron, el repositorio quedó con archivos fuera de alcance modificados. A partir de esta observación documenté las cinco piezas de conocimiento implícito que el agente tuvo que adivinar.
Impact: Se obtuvo evidencia clara de qué cosas sabíamos nosotros por haber hecho el proyecto antes pero que no estaban explícitas para un agente nuevo.

## Entry 03 - Rediseño de AGENTS.md y creación del mapa del repositorio
Stage: Context & Navigation Improvements
Prompt/goal: Mejorar AGENTS.md como contrato operativo y crear docs/REPO_MAP.md para evitar que el agente explore archivos innecesarios.
AI contribution: Propuso una estructura para AGENTS.md con orden de lectura, fuentes de verdad, comandos oficiales, reglas de cambio y condiciones de paro, además de un mapa de navegación con una guía específica para cambios en la lógica de búsqueda.
Student decision: Acepté la estructura propuesta asegurándome de que AGENTS.md y REPO_MAP.md no duplicaran las reglas de negocio que ya viven en REQUIREMENTS.md y SPEC.md. También decidí corregir el nombre de REQUIREMENTS.md y pasar los artefactos técnicos del agente a inglés para cumplir con la convención de la actividad.
Impact: La navegación del proyecto quedó centralizada y sin referencias rotas.

## Entry 04 - Creación del script de verificación y guardrails en código
Stage: Executable Knowledge & Guardrails
Prompt/goal: Convertir las reglas más importantes del repositorio en comprobaciones automáticas dentro de scripts/verify_repo.sh y scripts/check_repo_contract.py.
AI contribution: Desarrolló el script en Python para verificar la existencia de los archivos obligatorios, validar que SPEC.md referencie los identificadores de requisitos, comprobar mediante el árbol sintáctico que las funciones principales tengan anotaciones de tipos y asegurar con Git que no se modifique data/customers.json ni se rastreen archivos compilados.
Student decision: Aprobé la implementación y pedí que el script de verificación ejecutara pytest sin generar caché ni archivos bytecode para mantener siempre limpio el directorio de trabajo, eliminando además los archivos .pyc que venían arrastrándose de entregas pasadas.
Impact: Reglas que antes eran simples peticiones de texto en Markdown pasaron a ser validaciones automáticas que fallan si no se cumplen.

## Entry 05 - Ejecución AFTER y evaluación final
Stage: AFTER Execution & Impact Analysis
Prompt/goal: Restaurar el código funcional del baseline, aplicar únicamente las mejoras de preparación del repositorio y volver a ejecutar la tarea CR-02 en una sesión limpia con el mismo prompt.
AI contribution: En esta segunda sesión el agente leyó primero el contrato y el mapa del repositorio, fue directo a src/service.py y tests/test_search.py sin abrir archivos de otras capas, aplicó los cambios sin errores de edición y ejecutó el script de verificación obteniendo un resultado exitoso.
Student decision: Revisé que el árbol de trabajo de Git no tuviera archivos ajenos modificados y comparé las métricas de ambas sesiones, actualizando la auditoría final con un puntaje de 98 sobre 100. Reconocí que decisiones como cambiar la arquitectura, modificar los datos semilla de clientes o resolver ambigüedades del negocio siguen requiriendo juicio humano.
Impact: Se comprobó con evidencia que preparar el repositorio reduce la incertidumbre del agente, evita modificaciones accidentales y mejora la calidad de la entrega.
