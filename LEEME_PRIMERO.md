# P100 — copia completa portátil

Patrick, este paquete reúne todo el material del proyecto disponible en esta tarea al preparar la copia del 8 de septiembre de 2026: recuperación histórica, documentos, código, datos originales y sintéticos, pruebas, resultados, capturas, archivos de trabajo y las tres entregas ZIP anteriores.

## Abrir en otro equipo

1. Descomprime el ZIP completo en una carpeta tuya, por ejemplo `Documentos/P100`. No ejecutes scripts desde dentro del ZIP.
2. Para leer, abre los documentos Markdown o `P100_TRANSFER/04_DOCUMENTO/P100_Documento_integral.pdf`. No necesitas Python para consultar el PDF.
3. Para ejecutar código, instala Python 3.12 y abre una terminal en esta carpeta. No se incluyen instalaciones de Python ni entornos del PC de origen. El código de investigación usa la biblioteca estándar.
4. Ejecuta `python verificar.py` (en algunos equipos `python3 verificar.py`). Comprueba los hashes de todos los archivos de esta copia.
5. Ejecuta `python verificar.py --pruebas` para comprobar además los manifiestos de las tres entregas, la auditoría histórica nueva y los 67 tests de la revisión actual. No necesita internet ni credenciales; no envía operaciones.
6. Abre esta carpeta como proyecto local en tu entorno de desarrollo. Empieza leyendo `ESTADO_Y_TRABAJO_POR_COMPONENTES.md` y las instrucciones `AGENTS.md`.

El código y los datos se han probado en Windows con Python 3.12.14. Las rutas de los motores y verificadores usan la ubicación del archivo, para poder mover la carpeta. No se ejecutaron pruebas físicas en macOS/Linux. Los scripts antiguos de creación de PDF y algunos logs conservan rutas del PC original y requieren adaptar rutas, fuentes y dependencias si se quieren regenerar documentos; los PDF ya generados están incluidos.

## Índice

| Carpeta/archivo | Contenido |
|---|---|
| ESTADO_Y_TRABAJO_POR_COMPONENTES.md | Estado actual, límites y decisión de trabajar por partes en mercados conocidos |
| P100_TRANSFER/ | Paquete histórico, conversación recuperada, ambos PDF originales, informe integral y primera base v0.6 |
| P100_LAB/ | Avance 001: motor sintético, 3240 simulaciones, 64800 barras y registros completos |
| P100_RESEARCH/ | Avance 002: 1095 velas reales, 45 simulaciones, seis intenciones actuales, código y pruebas |
| ENTREGAS_ORIGINALES/ | Los tres ZIP previamente entregados y sus sumas, preservados byte por byte |
| tmp/ | Archivos de trabajo conservados: extracción, auditorías, scripts de documentos y comprobaciones visuales; no son la versión recomendada para operar |
| sources/ | Carpeta de referencias sincronizadas; estaba vacía al crear esta copia |
| PORTABILIDAD/ | Conversación de Codex accesible, transcripción derivada, contexto de esta petición y scripts de empaquetado |
| CONTENIDO_SHA256.json | Lista completa con tamaños y hashes; se excluye a sí misma para evitar autorreferencia |

## Lo que esta copia no puede recuperar

Los ZIP/CSV originales de las versiones históricas que nunca pudimos descargar siguen faltando, junto al final de un mensaje histórico. No se inventaron ni se sustituyeron por código nuevo. La conversación original recuperada y su cobertura están documentadas en `P100_TRANSFER/02_EVIDENCIA/COBERTURA_Y_FALTANTES.md`.

Se conserva también la representación accesible de esta tarea de Codex: nueve entradas devueltas por la app, con mensajes y metadatos de acciones cuando estaban disponibles. No equivale a una exportación completa de la cuenta, no incluye razonamiento interno ni garantiza todas las salidas de herramientas; las entradas vacías o incompletas se identifican. Los mensajes más recientes de Patrick se añaden expresamente en `PORTABILIDAD/CONTEXTO_DE_ESTA_COPIA.md`.

Este paquete no incluye el trabajo de otros compañeros o tareas que no estuviera en esta carpeta y que no se haya incorporado aquí. No necesita contraseñas o API keys; no se copiaron perfiles de navegador, credenciales ni configuración personal de Codex.

## Mantener una copia verificable

Conserva este ZIP como respaldo. Para desarrollar, trabaja en otra copia o crea una revisión nueva: cambios en código, datos o SQLite harán fallar correctamente los hashes antiguos. El ZIP incluye resultados voluminosos y copias de las entregas originales; esa duplicación es intencional para conservar tanto material extraído como entregables originales.
