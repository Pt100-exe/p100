# Cambios y verificaciones de esta transferencia

Patrick autorizó aplicar propuestas pendientes y probarlas antes de terminar el documento. La falta del código histórico impidió modificarlas sobre v0.5 o repetir sus experimentos. Se creó una base independiente y acotada de v0.6, preservando el PDF y las transcripciones. Su estado no se describe como v0.6 completa.

## Implementaciones nuevas

Regímenes con tendencia y volatilidad independientes; estrategia Core + Tactical; riesgo separado con un tope por volatilidad y máximos de exposición; validación de entradas; feature mínima por disponibilidad; partición temporal con purga estricta; registro del período consumido; manifiestos de código/configuración/datos. Los parámetros son ejemplos de ingeniería, no optimizaciones de mercado.

Se revisaron los módulos y ejecutaron 38 tests con éxito. Incluyen nueve combinaciones de regímenes y 720 combinaciones de parámetros dentro de los tests, además de perturbaciones del futuro, disponibilidad retrasada, fronteras y hashes. La salida y el entorno exactos están en 05_CODIGO/v06_foundations/test_run.log. La verificación del manifiesto de esa base produjo PASS.

El sizing conserva la tendencia incluso con volatilidad alta. Por ejemplo, UP + HIGH solicita 0.70 y queda limitado a 0.25 cuando el presupuesto es 0.20 y la volatilidad 0.80. Este comportamiento prueba un contrato aritmético; no demuestra mejora financiera.

## Auditoría del PDF y de la conversación

Se conservaron los dos PDF originales y se extrajo su texto por página. La comparación del primer PDF con el anexo de v2 encontró igual longitud normalizada y multiconjunto de caracteres, con diferencias de orden de extracción de tablas y fórmulas; no se detectó omisión de prosa en los bloques inspeccionados. Se mantienen ambos archivos para revisar cualquier discrepancia.

Se recalculó el Sharpe didáctico de las entradas indicadas en la guía: 12.838862164299517. Se ejecutó un contraejemplo que demuestra que la prueba de prefijo de p. 11 puede aceptar una función con shift(-1). Los scripts, entradas, logs y resultados se incluyen en 06_VERIFICACION/pdf_checks. No son experimentos de mercado.

Se agotó la paginación del chat accesible y se preservaron 14 turnos, 27 mensajes, 100 bloques de código, 14 tablas y 22 apariciones de referencias de archivos. T06M2 está recortado. Los archivos mencionados que no llegaron se registraron como faltantes, sin regenerarlos con nombres de originales.

## Pendiente para integrar v0 6

Recuperar y reproducir v0.5, ampliar datos, entrenar meta-labeling/downside, calibrar incertidumbre, validar selección out-of-fold, implementar costes y ejecución realistas, y ejecutar ablaciones con un protocolo congelado. El código nuevo no incluye estimador de volatilidad, tercer eje de estructura, modelos, datos multi-activo, motor de fills, broker o paper trading persistente. La causalidad del pipeline completo sigue pendiente de prueba.
