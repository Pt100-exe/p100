# Índice maestro de P100

Paquete de transferencia y documento de lectura para Patrick y el equipo. Edición creada el 7 de septiembre de 2026 en Costa Rica, con registros UTC del 8 de septiembre. Asistente de esta tarea: Atlas.

**Estado:** fuentes recuperadas organizadas y base nueva de v0.6 probada. La transferencia histórica tiene faltantes explícitos: proyectos ZIP, CSV y un mensaje recortado. No se ha reproducido v0.5.

## Ruta de lectura

1. `02_EVIDENCIA/COBERTURA_Y_FALTANTES.md` para conocer qué llegó y qué falta.
2. `01_CONTEXTO/PROJECT_CONTEXT.md` para propósito, evolución y clases de evidencia.
3. `01_CONTEXTO/EQUIPO_Y_ATLAS.md` para la presentación y acuerdos de colaboración.
4. `02_EVIDENCIA/AUDITORIA_PDF.md` para requisitos del documento inicial y sus correcciones.
5. `01_CONTEXTO/DECISIONS.md` y `EXPERIMENT_LOG.md` para decisiones, pruebas y cifras desde v0.1.
6. `01_CONTEXTO/KNOWN_ISSUES.md`, `ROADMAP.md` y `CAMBIOS_ACTUALES.md` para problemas, siguientes pasos y contribución nueva.
7. `03_ARRANQUE/START_HERE.md` para continuar en Codex y comprobar el paquete.
8. `00_ORIGINALES/conversacion_recuperada/TRANSCRIPCION_LITERAL.md` para consultar todo el texto recuperado, incluidos 100 bloques de código y 14 tablas.
9. `05_CODIGO/v06_foundations/README.md` y `TEST_REPORT.md` para ejecutar y revisar los módulos nuevos.

## Documento consolidado

`04_DOCUMENTO/P100_Documento_integral.pdf` reúne la lectura estructurada, conversación recuperada, código nuevo, pruebas y ambos PDF originales anexados. Tiene índice y marcadores para navegar. `P100_Documento_integral.md` conserva una versión de texto editable; los PDF originales se entregan en sus archivos binarios y sus extracciones por página.

## Evidencia organizada

- `00_ORIGINALES`: los dos PDF, solicitudes de esta tarea y páginas JSON del chat. Conservar inmutables.
- `01_CONTEXTO`: contexto, equipo, decisiones, experimentos, problemas, roadmap y cambios actuales.
- `02_EVIDENCIA`: auditorías completas; cobertura; índice de mensajes; 20 registros experimentales; bloques de código; tablas; referencias y nombres de archivos.
- `03_ARRANQUE`: instrucciones concretas para retomar el trabajo.
- `04_DOCUMENTO`: documento de lectura y versión editable.
- `05_CODIGO/v06_foundations`: componentes nuevos de v0.6, configuración, tests, logs y manifiesto de congelación.
- `06_VERIFICACION`: verificador del paquete, scripts/resultados de auditoría de PDF y reporte de control documental.

`INVENTARIO_ARCHIVOS.csv` lista los archivos efectivamente entregados. `MANIFEST_SHA256.json` registra sus tamaños y hashes. Las referencias a archivos ausentes se conservan en `02_EVIDENCIA/MENCIONES_ARCHIVOS.json` y `REFERENCIAS_ARCHIVOS_OPACAS.json`, separadas del inventario real.

## Convención de referencias

TxxMy resuelve a un mensaje del chat en `00_ORIGINALES/conversacion_recuperada/INDICE_MENSAJES.json`. H001 a H020 resuelven a grupos del registro experimental. Las páginas de la auditoría PDF son páginas originales de PDFM1000v2.pdf. Los resultados de tests actuales se encuentran en logs con comando, fecha y entorno. Una cita histórica sin archivo recuperado se considera referencia pendiente de contrastar.
