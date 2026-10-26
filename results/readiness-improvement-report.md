# Readiness Improvement Report

## Resumen del análisis
En esta actividad evaluamos qué tan preparado estaba nuestro repositorio de búsqueda de clientes para ser modificado de forma segura por un agente de programación. En la primera ejecución partimos de un repositorio funcional pero con deuda documental y de configuración, donde el agente obtuvo una calificación inicial de 39 sobre 100 y un resultado parcial. Después de estructurar el contexto operativo, crear un mapa de navegación y programar validaciones automáticas, repetimos exactamente la misma tarea desde el código base original, logrando subir el puntaje a 98 sobre 100 y obteniendo una ejecución limpia y exitosa.

## Implicit Knowledge Found

### IK-01 Nombre incorrecto del archivo de requerimientos
Un desarrollador que ya trabajó en el proyecto sabía que el documento de requisitos se llamaba REQUERIMENTS.md por un error de dedo al crearlo, pero las instrucciones de AGENTS.md pedían leer REQUIREMENTS.md. El agente tuvo que listar los archivos de la carpeta raíz para descubrirlo. Esto no debía quedar implícito, por lo que se corrigió el nombre del archivo y se agregó al script de validación de contrato.

### IK-02 Archivos compilados y de cobertura subidos a Git
En el repositorio original se habían subido por error los archivos compilados de Python y la base de datos de cobertura. Al correr las pruebas durante la primera ejecución, estos archivos binarios se modificaron automáticamente, ensuciando el estado de Git con cambios fuera de alcance. Se resolvió eliminándolos del seguimiento de Git y bloqueando su presencia desde el script de verificación.

### IK-03 Punto de entrada y responsabilidades desactualizadas en la arquitectura
El documento de arquitectura mencionaba que el programa se ejecutaba con un archivo llamado search.py que nunca existió en el repositorio, además de describir límites entre capas que no coincidían del todo con la implementación real en src/cli.py y src/storage.py. Para evitar que el agente buscara archivos inexistentes, se corrigió ARCHITECTURE.md y se creó docs/REPO_MAP.md explicando exactamente qué hace cada archivo.

### IK-04 Comandos de validación no documentados en las instrucciones del agente
Aunque los requerimientos no funcionales exigían mantener la cobertura de pruebas y usar tipado estático en el código, AGENTS.md solo decía que se corriera pytest de manera general. Esta información se hizo explícita y ejecutable integrándola dentro de AGENTS.md y en el script scripts/verify_repo.sh.

### IK-05 Protección del archivo de datos de clientes
Quienes hicimos el proyecto en las actividades pasadas sabíamos que data/customers.json contiene los registros exactos con los que se prueban los casos de la terminal y que las pruebas unitarias del servicio deben simular esos datos con mocks en lugar de editar el archivo JSON. Como ese riesgo no estaba documentado, se declaró como ruta protegida en el mapa del repositorio y se programó una revisión en scripts/check_repo_contract.py que falla si el archivo sufre modificaciones.

## Changes Made

### Improvement I-01
Category: Context
Problem: El archivo AGENTS.md era demasiado breve, apuntaba a un nombre de archivo incorrecto y no especificaba los comandos de validación ni las condiciones en las que el agente debía detenerse.
Change: Se reescribió AGENTS.md definiendo el orden de lectura, las fuentes de verdad, el mapa resumido, los comandos estándar, las reglas de cambio y las condiciones de paro. También se renombró REQUIREMENTS.md y se unificó el idioma técnico en inglés.
Evidence: En la segunda ejecución el agente encontró todos los documentos normativos al primer intento y siguió el flujo de validación sin omitir pasos.

### Improvement I-02
Category: Navigation
Problem: No existía una guía rápida que indicara dónde estaba cada módulo ni qué archivos modificar según el tipo de tarea, lo que obligó al agente a leer todo el código fuente en la corrida inicial.
Change: Se creó docs/REPO_MAP.md detallando los puntos de entrada, la ubicación de las pruebas, una guía de cambios para la lógica de búsqueda y la lista de archivos que no deben editarse.
Evidence: En la ejecución posterior el agente leyó el mapa y fue directo a src/service.py y tests/test_search.py sin abrir los módulos de consola ni de almacenamiento.

### Improvement I-03
Category: Executable Knowledge
Problem: Las validaciones del proyecto estaban dispersas y dependían de que el usuario o el agente recordara qué banderas pasarle a pytest o cómo revisar la sintaxis del código.
Change: Se implementó scripts/verify_repo.sh como único comando encargado de correr las pruebas unitarias sin dejar archivos de caché, verificar la sintaxis de todos los scripts y ejecutar el validador de contrato.
Evidence: El agente ejecutó el script al finalizar su implementación y validó todo el repositorio en un solo paso.

### Improvement I-04
Category: Guardrail
Problem: Las reglas críticas del proyecto solo existían como texto en Markdown, permitiendo que se subieran archivos compilados, se omitieran anotaciones de tipos o se alteraran archivos de datos sin que nada fallara.
Change: Se programó scripts/check_repo_contract.py para verificar automáticamente la existencia de los documentos obligatorios, las secciones de AGENTS.md, las referencias de requisitos en SPEC.md, el tipado en las funciones principales, la ausencia de archivos binarios en Git y la integridad de data/customers.json.
Evidence: El script detecta de forma determinista cualquier incumplimiento y forma parte obligatoria del cierre de tareas.
