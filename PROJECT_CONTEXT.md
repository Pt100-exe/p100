# Contexto maestro de P100

## Propósito y estado

P100, también denominado quant-system, es un laboratorio de investigación cuantitativa inspirado en PDFM1000v2.pdf. Su objetivo documentado es construir un sistema modular con datos, señales, modelos, validación temporal, riesgo separado, ejecución simulada y trazabilidad. El objetivo no queda reducido a obtener una rentabilidad favorable en un único backtest.

La conversación declara implementaciones desde v0.1 hasta v0.5 y resultados sintéticos e históricos. En esta transferencia se recuperaron 14 turnos, 27 mensajes y el PDF original completo. No llegaron los ZIP del código ni los CSV de mercado y resultados que el asistente histórico dijo generar. Por tanto, esta entrega preserva el expediente disponible y añade código nuevo acotado; no certifica la reproducción de v0.1 a v0.5 ni constituye v0.6 completa.

La referencia TxxMy identifica un mensaje en INDICE_MENSAJES.json y en la transcripción literal. Las páginas PDF citadas siempre son las del PDF original de 35 páginas, no las páginas globales del documento consolidado.

## Clases de evidencia

HECHO DOCUMENTAL significa que el texto o requisito puede verse directamente en el PDF o en un mensaje. Que un mensaje diga «ejecuté 22 pruebas» prueba que se afirmó, pero no que esas pruebas se hayan vuelto a ejecutar aquí.

RESULTADO HISTÓRICO DECLARADO significa una cifra o prueba que el asistente anterior comunicó. Se conserva con el conjunto de datos, política y período cuando se conocen. No se eleva a resultado reproducido sin código, datos, entorno y logs.

VERIFICADO EN ESTA TAREA significa una inspección o ejecución realizada durante esta transferencia con su evidencia guardada. Incluye la integridad de archivos, cálculos didácticos contrastados y las pruebas del código nuevo.

INFERENCIA significa una interpretación razonada que los datos disponibles no demuestran por sí solos. PROPUESTA significa una idea pendiente; IMPLEMENTACIÓN NUEVA significa código escrito en esta tarea con alcance propio. FALTANTE significa material que no pudo recuperarse, aunque la conversación lo mencione.

## Evolución del proyecto

v0.1 fue descrita como una base de ingeniería con OHLCV sintético determinista, estrategia SMA, long/cash, sin apalancamiento ni conexión a broker. El asistente declaró riesgo separado, idempotencia, auditoría JSONL, Docker y 22 pruebas. Sus cifras de rendimiento proceden de datos artificiales y no demuestran capacidad predictiva. Fuente T01M2.

La propuesta llamada v3 planteó separar research, paper, shadow y live, ampliar contratos de datos, validación walk-forward, estrategias y modelos, y hacer riesgo configurable. «v3» es el nombre usado en la conversación para la propuesta; no permite inferir la existencia de una versión publicada v3.0. Tampoco se recuperó un artefacto ejecutado de v0.2. Fuentes T02M2 y T03M2.

La comparación v0.1 frente a v0.3-experimental usó caminos sintéticos. La política agresiva ganó más retorno bruto pero deterioró drawdown, costes y estabilidad. La ronda v0.3.1 incorporó varias políticas, estrategias clásicas, modelos supervisados y Q-Learning, y expuso fallos de arquitectura. La respuesta de esa ronda está recortada; las cifras visibles se preservan sin completar su final. Fuentes T04M2 y T06M2.

v0.4 fue el primer replay histórico declarado: BTC/USDT diario, 189 filas, del 4 de mayo al 8 de noviembre de 2024. Entrenamiento ML hasta el 29 de agosto, purga y 69 decisiones del 1 de septiembre al 8 de noviembre. Señales con información hasta el cierre t y ejecución al open t+1; costes base de 10 bp por unidad de turnover. Buy & Hold obtuvo +28.45%; SMA adaptativa +8.16%; ningún candidato activo lo superó. No se recuperó la URL del repositorio original ni sus filas. Fuente T08M2.

v0.5 cambió a objetivos de retorno y amplió features, horizontes, regímenes, ensemble, selectividad y sizing. Después del warm-up y purga, la conversación declara 64 observaciones de entrenamiento, 37 de validación y 69 OOS. Trend Capture obtuvo +5.01%, Sharpe 2.21, drawdown -3.84% y exposición media 12.9%; el ML económico perdió -8.52%. Estas cifras reutilizan el período de v0.4. Fuentes T10M2 y T11M2.

El diagnóstico posterior reconoció que el conocimiento del rally OOS influyó en long/cash y Trend Capture. Desde ese momento la ventana se considera DEVELOPMENT / VALIDATION BURNED SET. La purga puede impedir que un target atraviese una frontera temporal, pero no elimina la contaminación por decisiones humanas informadas por el test. Fuente T11M2.

## Arquitectura que se pretende preservar

La estructura conceptual es datos crudos con procedencia y disponibilidad, features causales, estrategias/modelos, validación y selección temporal, construcción de posición, risk engine independiente, ejecución, reconciliación y auditoría. El PDF la propone y la conversación afirma implementaciones parciales. No se asume que todos los módulos existan en los archivos que faltan.

En v0.6 se propone separar tendencia y volatilidad, incorporar Core + Tactical, usar ML para aceptar señales o estimar downside, introducir incertidumbre y ampliar datos. El filtro de confianza y el presupuesto de riesgo deben tener responsabilidades explícitas; multiplicar varios descuentos sobre la misma exposición puede producir una participación muy reducida. La base nueva incluida aborda solo algunos contratos deterministas de esta propuesta.

## Interpretación de los resultados

El expediente disponible no demuestra alpha. Buy & Hold dominó el retorno del corto rally de BTC estudiado; una menor exposición explica parte de la menor ganancia y del menor drawdown de otros sistemas. Exposición media no equivale necesariamente a porcentaje de tiempo en mercado. Sharpe en 69 decisiones no basta para afirmar robustez y sus convenciones de anualización no pueden verificarse sin los scripts.

El peso mayoritario de Ridge y los pesos cero de varios modelos justifican explorar una arquitectura más simple, pero no prueban que Ridge domine fuera de esa validación. El fracaso de cinco seeds o varios hurdles limita esas explicaciones concretas; no demuestra por sí solo la causa de la pérdida. La escasez de datos es una limitación observada, no una garantía de que más datos resolverán el problema.

## Prioridad para continuar

Primero recuperar los artefactos históricos y consolidar contratos temporales. Luego reproducir una baseline en el conjunto ya consumido, ampliar datos trazables, congelar el protocolo y evaluar cambios por ablaciones en validaciones walk-forward. El examen final requiere un período no usado para decidir el diseño; una fecha posterior por sí sola no demuestra que sea desconocido. Los módulos de broker y la operación con capital no forman parte del código nuevo de esta entrega.
