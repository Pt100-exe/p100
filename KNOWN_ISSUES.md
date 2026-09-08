# Problemas conocidos y límites de la evidencia

## Material no recuperado

F01. Faltan los proyectos originales de v0.1, v0.3-experimental, v0.3.1, v0.4 y v0.5, incluidos configuraciones, dependencias, tests, logs y CSV. Hay 22 apariciones de referencias de archivos opacas; sus índices son locales al mensaje y no deben deduplicarse globalmente. No se conocen todos sus nombres reales.

F02. T06M2 fue devuelto con 20 000 unidades UTF-16 y acaba a mitad de «alta exposic». Su texto restante y posibles archivos del final no están incluidos. T05M1 repite la solicitud de pruebas y no tiene respuesta recuperada; T07M2 contiene solamente «Sí, vieras que,». Se preservan ambas entradas sin inventar contenido.

F03. El proveedor del dataset BTC se describe como repositorio con Binance Spot, pero los enlaces se convirtieron en marcadores internos de cita. No se dispone de URL exacta, hash del CSV, zona horaria verificable, filas OHLCV, ajustes ni licencia del dataset específico. No sustituirlo por otro CSV y llamarlo reproducción exacta.

## Problemas metodológicos

M01. La ventana 2024-09-01 a 2024-11-08 está consumida para diseño. Su reutilización en v0.5 impide considerarla prueba final independiente. No es equivalente a una fuga de filas futuras dentro del backtester.

M02. La prueba histórica anti-futuro de v0.5 se describe después como una comprobación de ret20. No acredita invariancia de entrenamiento, selección, regímenes, pesos, señales o ejecución. El contraejemplo de la auditoría del PDF demuestra además que comprobar un prefijo alejado de la frontera puede dejar escapar una función anticipatoria.

M03. v0.5 declara 64 filas de entrenamiento y 37 de validación frente a muchos modelos y transformaciones. Faltan conteos de features, hiperparámetros, partición exacta de las 37 filas y definición del score para una auditoría independiente. MLP quedó con peso cero; la congelación propuesta no significa prohibición permanente de redes.

M04. Predicción de dirección, retorno bruto y utilidad neta son objetivos distintos. Los resultados positivos de un sistema durante un rally no prueban valor predictivo. AUC de 0.58 con 69 observaciones tampoco acredita alpha sin incertidumbre y repetición independiente.

M05. Los factores de régimen, confianza, volatilidad y límites pueden reducir repetidamente la misma exposición. La relación con el bajo 12.9% es una hipótesis plausible, no una atribución causal demostrada por una ablación.

M06. Un régimen mutuamente excluyente high_vol/trend pierde información: tendencia alcista y volatilidad alta pueden coexistir. La corrección multieje es conceptual; su mejora financiera requiere evaluación posterior.

M07. La suma de las categorías de v0.3.1 da 5 878, pero «60 pares» y «60 comprobaciones» no fijan una misma unidad. La cifra total no significa 5 878 tests unitarios independientes. Unidades, dependencias entre escenarios y criterios de pase necesitan los logs originales.

M08. La frase histórica «no existe una fuga temporal» es más fuerte que las pruebas disponibles. Debe leerse como afirmación del asistente anterior, no como certificación de esta transferencia. La exactitud de las métricas de equity, Sharpe, drawdown y turnover tampoco puede revalidarse sin curvas y operaciones.

## Problemas detectados en el PDF

P01. El anexo conserva un Sharpe didáctico de 18.2562. La guía correctiva del propio PDF lo rectifica a aproximadamente 12.84 para los supuestos indicados. La auditoría actual vuelve a obtener 12.838862164299517. El cálculo didáctico no es rendimiento de P100.

P02. La prueba anti-futuro de p. 11 puede aceptar una media desplazada hacia el futuro. El contrato debe comparar todo el prefijo disponible hasta la frontera y demostrar que una implementación deliberadamente contaminada falla.

P03. Los fragmentos del PDF incluyen piezas incompletas, como sma_desplazada sin definición en su ejemplo, y un orden de instalación Docker que debe revisarse antes de copiarlo literalmente. El PDF es una guía y una transcripción de antecedentes, no un repositorio ejecutable ya validado.

## Límites de la contribución actual

El código nuevo es una base independiente para contratos de v0.6. Sus pruebas no evalúan el motor histórico ni una estrategia completa. No se han ejecutado nuevos backtests de rentabilidad, entrenado meta-labelers, validado intervalos conformales, incorporado datos multi-activo o conectado brokers. La cobertura exacta y los casos ejecutados se indican en su README y TEST_REPORT.
