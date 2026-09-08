# Arranque de Codex con P100

## Abrir y leer

Descomprime el paquete en una carpeta de trabajo y abre esa carpeta como proyecto local en la app. La documentación oficial permite elegir una carpeta y trabajar con sus archivos y contexto. El procedimiento no depende de que un historial anterior aparezca automáticamente. Fuente consultada durante esta transferencia: [Aplicación de escritorio](https://learn.chatgpt.com/docs/app).

Lee INDICE_MAESTRO.md, 02_EVIDENCIA/COBERTURA_Y_FALTANTES.md y 01_CONTEXTO/PROJECT_CONTEXT.md. Después lee DECISIONS.md, EXPERIMENT_LOG.md, KNOWN_ISSUES.md, ROADMAP.md y CAMBIOS_ACTUALES.md. Consulta la auditoría del PDF, los originales y la transcripción literal para cualquier detalle. La numeración TxxMy conduce al ID original del mensaje.

El AGENTS.md incluido resume los acuerdos operativos del paquete. Codex lee este tipo de archivo como instrucciones de proyecto; mantenerlo breve evita confundir el archivo de arranque con la documentación completa. Fuente: [Instrucciones de proyecto con AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Comprobar integridad y ejecutar lo disponible

Desde la carpeta P100_TRANSFER, ejecuta `python 06_VERIFICACION/verify_package.py` para comprobar el manifiesto de archivos. Necesita Python 3.12 o posterior para mantener el entorno sugerido; el verificador usa biblioteca estándar. El manifiesto verifica identidad de archivos, no valida conclusiones científicas.

Las pruebas ejecutables disponibles pertenecen a `05_CODIGO/v06_foundations`. Consulta su README para el comando y contratos exactos. Son código nuevo de esta tarea; no incluyen los tests históricos de v0.1 a v0.5. Las comprobaciones didácticas del PDF están en `06_VERIFICACION/pdf_checks`.

## Primer encargo sugerido

Lee el índice maestro y el registro de cobertura de P100 antes de modificar nada. Identifica qué proviene del PDF, qué son declaraciones históricas, qué se verificó en esta entrega y qué sigue faltando. Comprueba el manifiesto y ejecuta las pruebas del código nuevo. Conserva los originales. Si se incorporaron ZIP históricos, inventaría y verifica sus hashes, inspecciona código y dependencias y reproduce una baseline con el dataset exacto. Continúa el roadmap v0.6 sin utilizar 2024-09-01 a 2024-11-08 como examen desconocido. Registra cada cambio y cada experimento, incluidos los resultados negativos. No presentes la base nueva como si fuera v0.5 recuperada o v0.6 completa.

## Material necesario para cerrar la transferencia histórica

Se necesita una exportación completa del chat o el texto restante de la respuesta v0.3.1; los ZIP/proyectos v0.1, v0.3-experimental, v0.3.1, v0.4 y v0.5; los CSV originales de BTC y resultados; y sus configuraciones, tests y logs. No hace falta compartir credenciales de brokers. Recibir esos archivos es una necesidad de evidencia, no una nueva aprobación para investigar y programar.

En esta sesión se pudo leer el chat mediante la herramienta de tareas de la app, pero el navegador no estaba autenticado. La lectura tuvo un límite por mensaje. Por eso no se adoptan como instrucciones actuales las antiguas afirmaciones categóricas sobre qué chats puede ver Codex: el estado observado en esta tarea y los archivos entregados son la referencia práctica.
