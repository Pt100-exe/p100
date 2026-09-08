# Cobertura de recuperación y material faltante

Esta entrega reúne todo el material recuperable mediante los accesos disponibles y distingue los vacíos. **La transferencia histórica aún no puede certificarse como completa**: faltan adjuntos ejecutables y el final de una respuesta. La documentación y el código nuevo sí se entregan como artefactos concretos revisables.

## Fuentes presentes

| Fuente | Recuperación | Qué acredita |
|---|---|---|
| PDFM1000v2.pdf | 35 páginas completas y texto por página | Guía, requisitos y transcripción de antecedentes |
| PDFM1000.pdf | 14 páginas completas, hallado en Downloads | Antecedente de la guía y conversación incluida |
| Chat Desarrollo de sistema cuantitativo | 14 turnos, 27 mensajes, 108 281 caracteres Unicode | Texto de las decisiones y resultados declarados |
| Código en mensajes | 100 bloques con fuente | Fragmentos históricos, incluidos pseudocódigo y ejemplos |
| Tablas en mensajes | 14 tablas con fuente | Resultados y comparaciones comunicados |
| Registro estructurado | 20 grupos experimentales | Organización de cifras históricas, sin reejecución |
| Solicitudes actuales | Transferencia, documento, autorización y acuerdos | Instrucciones de Patrick para esta tarea |
| Base v0 6 nueva | Código, configuración, 38 tests, logs y hashes | Comportamiento determinista verificado en esta entrega |

El recuento de conversación corresponde a la salida visible de la herramienta de lectura, con paginación agotada. No incluye razonamiento interno, llamadas de herramientas del chat histórico, exportación de toda la cuenta ni otras ramas que no se expusieron. El PDF antecedente contiene ocho preguntas y ocho respuestas de una conversación previa; se preserva sin atribuirle los desarrollos v0.1 a v0.5.

## Fuentes parciales y ausentes

T06M2, el informe de v0.3.1, llega hasta 20 000 unidades UTF-16 (19 993 caracteres Unicode) y termina en «alta exposic». No se conoce cuánto falta. T05M1 tiene una solicitud repetida sin respuesta en esa entrada; T07M2 es una respuesta de 15 caracteres inconclusa. No se reconstruyeron esos textos.

Hay 22 apariciones de referencias opacas de archivos generados, agrupadas por mensaje. No significan 22 archivos únicos. Se conservaron los índices y sus IDs de mensaje; no se pudieron recuperar los destinos ni contenidos. La asociación exacta de cada índice con ZIP, informe o CSV no está disponible.

Faltan los proyectos ejecutables v0.1, v0.3-experimental, v0.3.1, real_sim v0.4 y real_sim_v05, con sus dependencias, configuraciones, tests, logs, curvas y resultados crudos. No hay prueba de una entrega separada v0.2 o v0.3.0. Falta el dataset BTC exacto, su URL verificable y su manifiesto de procedencia. Los nombres de archivos sugeridos en mensajes de migración no prueban que esos archivos se generaran.

El PDF menciona además un archivo histórico llamado guia_ia_financiera_completa.pdf mediante un marcador; ese adjunto no está recuperado. La copia PDFM1000.pdf sí está presente y se conserva bajo su propio nombre.

## Búsqueda realizada

Se leyó el chat mediante la herramienta de tareas de la app en dos páginas, hasta hasMore=false. Su adjunto expuesto fue PDFM1000v2.pdf. La carpeta sources del proyecto estaba vacía. Se buscaron nombres relacionados con quant, P100, prototipos, real_sim, v0 y M1000 en Downloads, Documents y Desktop; aparecieron los dos PDF. No se encontraron allí los paquetes del simulador. El navegador disponible no tenía sesión autenticada de ChatGPT. No se alteraron los archivos sincronizados del proyecto.

## Cómo cerrar los vacíos

Incorporar los ZIP y CSV originales, y una exportación completa del chat o el tramo restante de T06M2. Calcular hashes antes de descomprimir a una copia de trabajo, mapear cada archivo a su mensaje/versión y conservar su origen. Después inspeccionar e instalar el entorno correspondiente, ejecutar sus suites, reproducir una baseline y documentar diferencias. Hasta entonces toda rentabilidad histórica de este paquete conserva la etiqueta de resultado declarado.

## Preservación y versión de lectura

Los JSON de conversación y la transcripción literal mantienen las referencias internas y el texto original. El PDF de lectura convierte Markdown en formato legible, representa referencias inaccesibles con etiquetas explicativas y conserva el contenido técnico. Cuando un carácter decorativo no tenga glifo disponible se muestra su código Unicode. Los originales binarios PDF se anexan íntegros con su paginación propia y también se entregan separados. El índice de archivos y el manifiesto permiten verificar qué está efectivamente dentro del paquete.
