# P100 — Avance 002: primera evaluación histórica real y primera captura en sombra

Patrick, podemos empezar una prueba en sombra con datos reales. Ya se registró la primera captura de señales actuales. El avance aprobado es de ingeniería e investigación: todavía no acredita una estrategia lista para operar dinero.

Atlas — asistente de IA de OpenAI, colaborador técnico de Patrick. Revisión del 8 de septiembre de 2026 UTC (7 de septiembre en Costa Rica durante la captura).

## Qué está comprobado

- Se descargaron respuestas originales del endpoint público de Binance y se validaron 1095 velas: 365 días de 2025 para BTCUSDT, ETHUSDT y SOLUSDT. Se guardaron bytes originales, normalizados, URLs, hora de descarga y hashes.
- Se ejecutaron las 45 combinaciones del protocolo previo: tres instrumentos, cinco políticas y tres escenarios de costes, con curva y eventos completos. No se descartaron resultados desfavorables.
- Auditoría independiente del motor: 16425 estados y 14985 eventos reconciliados; hashes de 23 archivos previos y seis archivos de datos (tres crudos y tres normalizados) verificados.
- Pasaron 67 métodos de prueba: 52 anteriores, 11 de mercado/reloj/banda y cuatro de observación/persistencia. Se verificaron invariancia ante futuro alterado, espera por disponibilidad, límite de riesgo por encima de banda, datos incompletos y duplicados.
- Se registraron seis intenciones actuales: dos políticas en tres símbolos. La reproducción sin red confirmó las seis y detectó sus seis duplicados sin insertarlos otra vez. Órdenes enviadas: 0.

## El cambio temporal necesario

Las velas diarias del proveedor cierran un milisegundo antes de la siguiente apertura. La disponibilidad histórica exacta no está registrada en esos datos. Fijé antes del ensayo el supuesto close_time + 1 segundo; bajo ese supuesto la primera apertura elegible suele ser t+2. La nueva cola utiliza el tiempo disponible, no un desplazamiento ciego de una fila. Es una convención conservadora de investigación, no una medición de la latencia real del proveedor.

La primera señal usa 30 retornos; el primer fill es en índice 32 (2 de febrero de 2025). Buy & Hold comparte ese comienzo, por lo que su retorno NO es el retorno del año natural completo. Se termina valorando posiciones abiertas a mercado; no se cobra una liquidación final inexistente. Dos decisiones al final quedan pendientes.

## Resultados con comisión 10 pb y deslizamiento 5 pb por lado

Cada fila usa una cuenta simulada independiente de 10000 USDT. Retorno y drawdown son de la curva completa con el calentamiento común en efectivo. No son una cartera combinada ni rentabilidades esperadas.

| Activo | Política | Retorno neto | Drawdown | Rebalanceos con cantidad no nula | Omitidos por banda | Coste total USDT |
|---|---|---:|---:|---:|---:|---:|
| BTCUSDT | cash | 0.00% | 0.00% | 0 | 0 | 0.00 |
| BTCUSDT | buy_hold | -13.04% | -32.02% | 1 | 0 | 14.98 |
| BTCUSDT | core_risk | -4.33% | -14.04% | 333 | 0 | 29.20 |
| BTCUSDT | core_tactical_risk | 0.26% | -12.90% | 333 | 0 | 271.95 |
| BTCUSDT | core_tactical_band | 0.18% | -12.89% | 94 | 239 | 258.71 |
| ETHUSDT | cash | 0.00% | 0.00% | 0 | 0 | 0.00 |
| ETHUSDT | buy_hold | -4.82% | -52.81% | 1 | 0 | 14.98 |
| ETHUSDT | core_risk | 2.12% | -18.09% | 333 | 0 | 51.99 |
| ETHUSDT | core_tactical_risk | 8.71% | -12.04% | 333 | 0 | 100.62 |
| ETHUSDT | core_tactical_band | 8.21% | -11.95% | 58 | 275 | 80.16 |
| SOLUSDT | cash | 0.00% | 0.00% | 0 | 0 | 0.00 |
| SOLUSDT | buy_hold | -41.57% | -51.68% | 1 | 0 | 14.98 |
| SOLUSDT | core_risk | -7.43% | -15.88% | 333 | 0 | 48.95 |
| SOLUSDT | core_tactical_risk | -0.50% | -11.58% | 333 | 0 | 90.00 |
| SOLUSDT | core_tactical_band | 0.74% | -10.61% | 63 | 270 | 72.99 |

## Resultado de la hipótesis fijada antes de descargar

La banda fija de 5 puntos de exposición solo conserva una posición cuando la diferencia es menor que la banda, no supera el límite de riesgo y el objetivo no es cero. H1 exigía coste y turnover no mayores en cada activo. H2 exigía no perder más de 1 punto porcentual de retorno ni empeorar el drawdown más de 1 punto en cada activo.

| Activo | Ahorro de coste USDT | Delta retorno (pp) | Delta drawdown (pp) | H1 | H2 |
|---|---:|---:|---:|---|---|
| BTCUSDT | 13.24 | -0.079 | 0.006 | True | True |
| ETHUSDT | 20.47 | -0.492 | 0.083 | True | True |
| SOLUSDT | 17.01 | 1.237 | 0.974 | True | True |

Criterio conjunto aprobado: **True**. La promoción significa conservar esta variante para la siguiente prueba en sombra, no aprobación para operar dinero. BTC y ETH tuvieron un retorno algo menor con la banda; se conserva ese resultado porque estaba dentro de la tolerancia previa. El ahorro en número de rebalanceos es mucho mayor que el ahorro monetario: muchos de los rebalanceos eliminados eran pequeños.

## Sensibilidad a fricciones: variante con banda

En 0 pb también se elimina el deslizamiento; en 10/30 pb se mantienen 5 pb de deslizamiento por lado.

| Activo | Retorno a 0 pb | Retorno a 10 pb | Retorno a 30 pb |
|---|---:|---:|---:|
| BTCUSDT | 2.67% | 0.18% | -3.04% |
| ETHUSDT | 9.03% | 8.21% | 7.13% |
| SOLUSDT | 1.47% | 0.74% | -0.22% |

## Qué empezó realmente en sombra

Primera observación: 2026-09-08T05:05:08.463376+00:00. Última vela cerrada utilizada: 2026-09-07T23:59:59.999000+00:00. Se usaron las políticas core_risk y core_tactical_band como comparación. Se excluyó la vela diaria todavía en formación.

Se conservan intenciones y hora de observación real en SQLite. No hay broker, órdenes, fills virtuales posteriores ni P&L forward todavía. Cualquier próxima simulación de fills tendrá que usar precios posteriores a observed_at; no puede adjudicarse una apertura que ya pasó al observar la señal. Esta captura fue puntual y el proceso terminó: no hay un monitor recurrente activo.

## Interpretación y límites

Hecho experimental: en esta muestra y con estos supuestos, la banda superó el criterio de costes/degradación y el control temporal/contable pasó. Inferencia de trabajo: merece avanzar a observación prospectiva frente al mismo baseline de riesgo. No se infiere que los retornos vayan a repetirse.

Un año, tres criptoactivos correlacionados y un proveedor no representan la mayoría de mercados digitales. Los precios 2025 ya están consumidos para desarrollo y no son un holdout independiente. Los bloques trimestrales son resúmenes de la misma curva, sin reentrenamiento; no son validación walk-forward. No hubo ML ni ajuste de parámetros tras ver los resultados.

Los costes son supuestos por lado, sin spread variable, impacto por volumen, mínimos de orden, tamaño de lote, intereses sobre efectivo, funding ni tasas de conversión de USDT. Unidades fraccionarias y saldo sin apalancamiento. El límite de exposición actúa al rebalancear, no garantiza que el precio no haga derivar el peso intrabar. Los datos públicos descargados ahora pueden contener revisiones no disponibles históricamente.

## Problemas detectados y corregidos

1. Una prueba con timestamp en microsegundos provocó OSError en Windows al intentar convertirlo como milisegundos. Se cambió el parser para verificar primero el timestamp entero exacto contra el esperado, y luego construir las fechas. El test conserva la entrada incorrecta y ahora obtiene el rechazo explícito.
2. El primer intento de descarga falló por permisos de socket del entorno. Se conserva results/study_002/FETCH_FAILURE.json. Tras autorización automática de red se ejecutó study_002_retry con nuevo congelado previo. No hubo sustitución silenciosa de fuente o datos.
3. El administrador de contexto de SQLite confirma transacciones, pero no cierra automáticamente la conexión. Dos tests fallaron al limpiar archivos bloqueados en Windows. Se añadió cierre explícito de conexión y los 67 métodos pasaron. La salida fallida se conserva junto a la final.
4. El enlace TikTok no pudo abrirse. No se vio el video ni se atribuyeron requisitos a su contenido.

## Próximo paso significativo

Podemos pasar a una prueba en sombra con nuevas sesiones. El siguiente componente debe transformar las intenciones ya persistidas en fills virtuales posteriores a su observación, manteniendo cuenta de efectivo y comparación core_risk frente a core_tactical_band. Primero exigir continuidad de registros, ausencia de duplicados y reconciliación; la evaluación económica necesita un período prospectivo y criterios fijados antes de observarlo.

Para ampliar clases de mercado, el próximo adaptador financiero debe resolver calendario, ajustes corporativos y divisa de acciones/ETF antes de reutilizar señales. ARQUITECTURA_MERCADOS.md distingue lo implementado de lo pendiente. El alcance de mercados no financieros queda pendiente de la precisión de Patrick; no impidió completar esta etapa.

No se usó el restablecimiento de uso de Patrick. La entrega incluye código, pruebas, datos crudos, resultados completos y registros actuales; los paquetes anteriores permanecen separados.

## Fuentes y trazabilidad

La API oficial describe las velas, su esquema y el endpoint público de datos: [documentación de mercado](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market), [documentación del endpoint de datos públicos](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md). El acceso al endpoint de este ensayo fue de lectura, sin claves. Las URLs exactas y hashes de las respuestas están en DATA_CATALOG.json.

- BTCUSDT: [solicitud original](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime=1735689600000&endTime=1767225599999&limit=1000), SHA-256 `3bc3222ceea83a7d4cbd7ddc22f20c412089beac10ddb17f3dea5e3d92c76ab7`, descarga 2026-09-08T05:03:24.367353+00:00.
- ETHUSDT: [solicitud original](https://data-api.binance.vision/api/v3/klines?symbol=ETHUSDT&interval=1d&startTime=1735689600000&endTime=1767225599999&limit=1000), SHA-256 `bde55cdfd3e747d3246bab1a23c1117ae7ea1c336342367b015de982636378dd`, descarga 2026-09-08T05:03:25.989826+00:00.
- SOLUSDT: [solicitud original](https://data-api.binance.vision/api/v3/klines?symbol=SOLUSDT&interval=1d&startTime=1735689600000&endTime=1767225599999&limit=1000), SHA-256 `51e27e96587eb220071ae497c98fc0aa4bd1c90382b0bf88f5c0c3c837f226e1`, descarga 2026-09-08T05:03:27.412071+00:00.
