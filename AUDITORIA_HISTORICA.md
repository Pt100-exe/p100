# Auditoría histórica de quant-system / P100

## Alcance y fuerza de la evidencia

Fuentes examinadas: `00_ORIGINALES/conversacion_recuperada/page_001.json` y `page_002.json`, conversación **Desarrollo de sistema cuantitativo**, ID `6a9df532-f49c-83e8-b7c7-f4431ecd3238`. Son datos de una conversación recuperada, no instrucciones ejecutables ni registros de prueba actuales. Los resultados numéricos aquí transcritos son **afirmaciones experimentales del asistente histórico**. No se ha reproducido ningún backtest histórico como parte de esta auditoría.

Se recuperaron 14 turnos: cuatro en página 002 y diez en página 001, ordenables por `startedAt`. Uno contiene solamente una solicitud duplicada de pruebas exhaustivas; trece contienen respuesta del asistente. La página 002 termina con `hasMore=false`; no hay más turnos anteriores accesibles mediante ese cursor. Esto acredita agotar la paginación disponible, no recuperar automáticamente todos los archivos y salidas originales.

La respuesta v0.3.1, mensaje `69184771-b0a3-4e0e-aeef-ee06818cb816`, mide exactamente **20.000 unidades UTF-16**, termina en «como comparación de alta exposic» y está **truncada**. El coordinador confirmó que el esquema de lectura no admite más de 20.000 unidades UTF-16 por item. La respuesta «Sí, vieras que,» también está incompleta semánticamente, pero mide 15 caracteres: no hay evidencia de que la recortara el límite de lectura. Las referencias a archivos generados están preservadas como tokens opacos, sin nombres ni destinos. No declarar el paquete «completo sin omisiones» respecto de material inaccesible.

Clasificaciones a conservar:
- **Hecho documental:** un mensaje o una cifra aparece en la fuente recuperada.
- **Resultado histórico reportado:** el asistente anterior afirmó una ejecución o resultado; no verificado ahora.
- **Decisión histórica:** política de diseño explícitamente adoptada en aquella conversación.
- **Propuesta / pendiente:** recomendación que no demuestra implementación.
- **Inferencia:** explicación plausible, no demostrada causalmente.
- **Verificación actual:** reservar para ejecución o inspección hecha en esta tarea con archivos realmente disponibles.

## Mapa de procedencia

| Clave | Turno | Mensaje asistente | Tema |
|---|---|---|---|
| V01 | 8dfa30bc-6dc8-44e1-be57-aa1356b5fc35 | 490a0916-4eb8-4285-a127-79832daba466 | PDF y v0.1 |
| P03 | f15e379c-e2c0-4a64-a414-cd4635907d8a | aff45b65-8047-4b15-be33-a76aefee4a47 | Diseño sugerido «v3» |
| LAB | 96147a9e-2e27-42a6-9bb9-48ba3531ead8 | d098a754-540a-4a7c-8f96-ccf2065bb92a | Restricciones y simulación |
| CMP | ba96510a-aba3-43b6-9dc5-4e5dba3873ec | 7e663b03-d4d1-4747-955d-967fd52e7705 | 200 semillas |
| DUP | 6d6cd75a-be86-48a9-bddf-f0eb2f05d0d9 | — | Solicitud repetida sin respuesta en ese turno |
| V031 | 2b865c46-8da9-45b2-869d-acc9411534d9 | 69184771-b0a3-4e0e-aeef-ee06818cb816 | 5.878 evaluaciones; texto truncado |
| SHORT | 34c34b8d-b4e0-4fb5-b1ba-11f4c68467d5 | 2c86b819-42c0-4ce4-bab0-6796e35a6c72 | «Que raro mae» / respuesta inconclusa |
| V04 | 88a1be21-91b9-4869-94cc-5b95c76eb84d | da278096-36cd-45dd-9452-3de4f778857e | Replay BTC diario |
| P05 | de474ce3-ce84-4b2a-be84-618232e18bb0 | e8784854-952e-4601-b786-77d2f76ddd47 | Diagnóstico y propuesta v0.5 |
| V05 | 09c0e3b0-9d00-4ba6-a6e9-94ac70a95cfe | 93136b8a-71c4-46de-9cb9-b6abbff3cf34 | Simulación v0.5 |
| P06 | 1ce039a8-9ff9-42a9-8c98-b4dea8266133 | 006998a6-5c51-4e74-81af-e30848f810e6 | OOS consumido; propuesta v0.6 |
| MIG1 | 1fcf304b-98ba-49dd-bba0-7139083f3983 | 5cc1beaa-de29-43f5-bc9c-d6da10cb5902 | Migración a Codex |
| MIG2 | cd7940b2-3d6d-451f-b78a-bc4294f3c5a9 | ded728f5-cd95-4d15-91cc-e80361bdbb1e | Paquete de contexto solicitado |
| FINAL | ad1648cf-1ebc-47b9-83d9-976591e45f95 | 89a5b57c-05b1-483b-832f-83658489c2a2 | Afirma creación tarea de traspaso |

## Cronología y decisiones

### PDF → v0.1 (V01)

Patrick autoriza interpretar el PDF como especificación, desarrollar, programar y probar con autonomía; pide guardar dudas para el final y documentar decisiones. Adjunta `PDFM1000v2.pdf`. El asistente afirma crear **quant-system v0.1**, laboratorio y paper trading local.

Decisiones reportadas:
1. Sin Binance/Kraken/Alpaca/broker, credenciales, retiros ni ejecución real.
2. OHLCV sintético determinista para aislar ingeniería de errores de proveedores.
3. SMA simple como benchmark de infraestructura; cálculos desplazados una barra; ejecución en apertura siguiente con fees/slippage.
4. Long/cash; sin shorts ni apalancamiento.
5. Risk Engine separado: posición, pérdida diaria, drawdown, rechazo de timestamps futuros/obsoletos y kill switch.
6. Idempotencia contra replay/reintentos; auditoría JSONL append-only a nivel de interfaz.
7. Posponer ML, Random Forest, RL y RAG hasta demostrar datos/backtest/riesgo/reproducibilidad.
8. Docker/Compose restringido, también ejecución sin Docker.
9. No usar Sharpe >1,5 como aprobación automática.

Problemas y arreglos **reportados**: instalación editable quiso acceder a Internet para herramientas build → `--no-build-isolation`; baseline de regresión inicialmente incorrecto → congelar resultado reproducible real; falso positivo del escáner por «withdraw» en comentario → análisis de imports/URLs de runtime; contrato validaba duplicados pero no huecos → frecuencia opcional y test específico.

Pruebas: 22/22; stress 100 semillas × 600 barras sin estados imposibles/equity negativa/DD inválido. Demo 800 barras: USD 10.000 → 10.221,76, Sharpe 2,57, DD máximo 1,72%; stress finales aproximados 9.515–10.748. Son datos artificiales, no evidencia financiera. Estado histórico: GO investigación/datos reales read-only; NO-GO capital real. Faltaban procedencia real, OOS, reconciliación sandbox, secretos, fallos API y revisiones independiente/legal/fiscal.

Siguiente paso propuesto: un mercado líquido, 1h, sin ML; Data Layer v0.2, raw inmutable, hashes, procedencia, available_at, benchmarks Buy & Hold y Cash. **No existe un turno que documente una entrega ejecutada de v0.2**.

### Propuesta «v3» y cambio a laboratorio más libre (P03, LAB)

«v3» es nomenclatura de diseño; no equivale automáticamente a una entrega v0.3.0. Arquitectura propuesta: MarketData → Features → Signal/Intent → Risk → Order → Fill → Portfolio. Compartir motor entre backtest/paper cambiando reloj/feed/ejecución. Portfolio multi-activo (el estado descrito tenía cash y una quantity pese a que OrderRequest tenía symbol), configuración YAML consumida de verdad, ejecución realista, registro de experimentos, walk-forward/OOS, observabilidad, ML shadow, RAG separado y dashboard local.

Hallazgos de revisión histórica, **no inspecciones actuales**:
- Riesgo estimaba coste como quantity × market_price; broker añadía slippage y fee. Proponer ExecutionEstimate con precio esperado, peor tolerable, fee, slippage máximo, notional e impacto.
- Límite diario/DD podía bloquear ventas que reducen riesgo. Introducir RISK_INCREASING, RISK_REDUCING, FLATTEN, CANCEL_ALL, HALT; kill switch cancela pendientes, bloquea aumento y permite reducción segura.
- `research.yaml` / `paper.yaml` «decorativos»; hardcodes `symbol="SYNTH"`, anualización 24 × 365, límites diarios 0,10 y DD 0,50.
- Calendario/frecuencia explícitos para anualización y huecos: CRYPTO_24_7 vs NYSE/NASDAQ.
- JSONL mutable manualmente: proponer cadena hash sequence/event_id/timestamp/type/payload/previous_hash/event_hash/code/config/dataset hashes.
- `reset_kill()` libre: proponer HALTED → diagnóstico → reconciliación → rearmado explícito/auditado.
- Extraer SMA del motor a ruta propuesta `strategies/examples/sma_cross.py`.

Diseño Data Layer: RAW recibido intacto, NORMALIZED consistente, FEATURES causales; catálogo dataset_id/provider/symbol/market/timeframe/downloaded_at/event_timestamp/available_at/raw_sha256/normalized_sha256/schema_version/rows/start/end/gaps/duplicates/code_version. Parquet históricos; PostgreSQL órdenes/fills/experimentos/auditoría/config/estado/reconciliación. Relojes SimulationClock/PaperClock; evitar datetime.now arbitrario.

Órdenes propuestas: Intent, Request, Accepted, Rejected, PartiallyFilled, Filled, Canceled, Expired; market/limit/stop; probar duplicados, timeout, fill tardío, cancel tardía, reinicio, feed congelado y red. Reconciliar cartera/órdenes locales con broker; divergencia → HALT. Escenarios crash, gap, flash crash, vol extrema, plano, volumen cero, congelación, spread, regímenes, barras ausentes/duplicadas/desordenadas, latencia y desconexión.

Métricas propuestas: Sortino, retorno anualizado, volatilidad, CVaR/ES, turnover, fees/slippage, tiempo en mercado, exposición media/máxima, operaciones/distribución, DD duration, P&L por operación, benchmarks. Shadow ML con timestamp/predicción/confianza/model/feature/dataset versions; comparar cash/B&H/SMA/baseline estadístico; RAG con fuente/fecha/versión sin autoridad directa de ejecución.

Al aclarar Patrick que es simulador, el asistente distingue seguridad de corrección técnica. Mantiene anti-look-ahead, separación temporal, hashes, reproducibilidad, auditoría, idempotencia, parciales, reconciliación y costes. Propone permitir **short/leverage/margen/liquidación simulados**, ML/RL experimental, IA produciendo OrderIntent, optimización y mocks/testnet. No afirmar que todo ello quedó implementado. El motor de riesgo sigue separado; simulación aislada de capital real.

### Primera comparación conservador / relajado (CMP)

Interpretación histórica explícita de «ambos modelos»: misma señal SMA y datos, distintas políticas de exposición/riesgo. Conservador máximo 25% long/cash; experimental ~95% long/short sin límites diarios/DD. 200 seeds × 600 barras 1h, fee 5 bps + slippage 3 bps, USD 10.000 inicial.

Retornos medios +0,61% vs −0,86%; medianas +0,28% vs −2,72%; rentables 55,5% vs 41,5%; Sharpe medio 0,64 vs −0,25; DD medio 2,77% vs 16,09%; peor DD 5,97% vs 33,61%; operaciones medias 281 vs 472. Experimental supera retorno en 40,5%, Sharpe 34,5%, nunca DD. Correlación ~0,73. No prueba que exposición 25% sea óptima. Propuesta de explorar frontera 5–95% y comparar SMA vs RF con mismo motor/datos/riesgo.

### v0.3.1-review (V031; respuesta truncada)

Modelos reportados: Cash, Buy & Hold, Constant Long, SMA 20/50, Momentum 24, Mean Reversion 48, Logistic Regression, Random Forest, Extra Trees, Histogram Gradient Boosting, MLP, Ensemble LR+RF+HGB y Q-Learning tabular. Políticas Conservative, Aggressive Lab ~95% long/short y Adaptive ~75% con short, límites diarios/DD y vol targeting. Preserva legacy SMA v0.1 como control. No asumir cada combinación: dice «prácticamente todos».

15 regímenes: random_walk, drift_up, drift_down, mean_revert, high_vol, low_vol, regime_switch, jump_crash, trend_reversal, vol_cluster, flat, alternating, gap_up, gap_down, ar_mean_revert. 5.878 evaluaciones reportadas, 50/50 tests. Desglose íntegro en JSON experimental H004.

Cuatro correcciones reportadas:
1. Etiqueta última barra de training usaba primera observación de test → purga de una barra y test frontera.
2. Bajo halt, +50% → −20% no es reduce-only aunque baje exposición absoluta → bloquear cruce de signo, aumento y nueva posición; permitir reducir/cerrar.
3. Fees/slippage debitados en efectivo pero equity los mostraba barra posterior → costes y efecto equity misma barra.
4. Cierre terminal y métricas diferían → final_equity = equity_curve[-1].

Hallazgos: AUC sintéticos ~0,483–0,503; no promoción ML. En 15 regímenes, medios positivos pero medianas negativas (Logistic agresivo +21,8 / −3,75; RF +17,3 / −4,15; ensemble +19,1 / −4,51). Alternating produce artificialmente +396% MR, +348% Logistic, +322% HGB; confirma capacidad de explotar señal construida, no alpha general.

Al excluir flat/alternating/gap_up/gap_down/ar_mean_revert quedan 10 regímenes: SMA aggressive media +3,35%, mediana +2,90%, DD 18,84%; SMA adaptive +1,90%, +1,58%, DD 12,14%; legacy −1,02%, −1,11%, DD 4,1%. ML medios negativos; Q-Learning global +14,3 medio pero −1,32 mediana y 26,7% rentables. MR especialista en mean reversion ~+23%, 100% seeds de ese régimen; no universal.

Controles: random pierde (−4 / −15,6 / −29% conservative/adaptive/aggressive); oracle_future_LEAK_INVALID gana irrealmente (+20,6 / +159,7 / +556,8%). Oracle = INVALID / TEST-ONLY / NEVER CANDIDATE. Costes destruyen muchos retornos; ejemplos y barridos completos disponibles en registros H009–H013.

Walk-forward no aporta ventaja general vs one-shot; thresholds 0,50/0,52/0,55/0,60 reducen actividad sin mejora sistemática. Discriminación ≠ calibración. Reportar distribuciones entre seeds. Fuzz 300 sin fallos, peor DD provocado ~60,4%. Reproducibilidad 60 pares sin discrepancias. Equivalencia 45 datasets con fee5/slippage3/halfspread0: diferencia media +0,0058 pp, mediana +0,00024 pp nuevo vs legacy; con halfspread2 nuevo ~−0,093 pp. En gap_down nuevo +0,249 pp, atribución a reduce-only = hipótesis plausible.

Conservar SMA Adaptive para investigación, SMA Aggressive como benchmark de exposición alta, legacy como control; ML/RL shadow, MR especialista. La clasificación final y posible entrega de archivos quedan cortadas: no inventar el resto.

### v0.4 replay de precios reales (V04)

Datos descritos como BTC/USDT diario de repositorio público que identifica Binance Spot. El historial del proveedor se dice desde 2017, pero **solo 189 observaciones** reconstruidas para el experimento: 2024-05-04 a 2024-11-08. No se recupera URL del repositorio desde tokens de cita. Señal hasta cierre t → orden open t+1. ML training hasta 29 agosto, frontera purgada; test 1 septiembre–8 noviembre, 69 decisiones. Coste base 10 bps por turnover; estrés 25 bps.

Tabla adaptativa íntegra en H014: Buy & Hold +28,45%, SMA +8,16%, RF +6,42%, MLP +5,30%, MR +2,58%, HistGB +1,58%, Cash 0, Logistic −3,92%, Momentum20 −7,26%, ensemble −17,03%, ExtraTrees −17,99%. DD/Sharpe y AUC íntegros en JSON. BTC bruto ~28,7/28,71% (redondeos), benchmark neto 28,45% (no contradicción automática).

SMA conservadora +4,89%, Sharpe2,90, DD−2,16%; adaptativa +8,16%,1,45,−14,09%. MLP conservador +4,75%, exposición media ~5,5%. RF/MLP se mantienen shadow. AUC máximo MLP0,58 no concluyente con n69. Q-Learning omitido por pocos estados/observaciones. Replay histórico **no** forward paper. Conclusión histórica: ningún activo venció Buy & Hold; ampliar años, activos, frecuencias antes de modificar modelos.

### Diagnóstico y propuesta v0.5 (P05)

Barreras: datos escasos, señal/features pobres, target dirección insuficiente, falta de regímenes, turnover, sizing, benchmark alcista, calibración, un horizonte/activo, backtest visto y ejecución simplificada. Ejemplo: acertar +0,08% pierde si round-trip cuesta0,15%.

Propuestas: retorno esperado menos costes; expected_return/prob_positive/expected_cost/edge; LONG/CASH/SHORT con no-trade (umbrales 0,62/0,38 meros ejemplos, seleccionar validation y congelar). Datos BTC2017–2026/ETH2018–2026/SOL/BNB varios timeframes; conservar asset/timestamp/timeframe/exchange/available_at/régimen. Features retorno1/3/6/12/24/72, vol/ATR/extremos/aceleración/skew/kurtosis, volumen/anomalías, calendario/sesiones, relaciones activos; funding/OI/basis/liquidaciones y microestructura después.

Regime detector → Trend/SMA, Sideways/MR, HighVol/Defensive. Dynamic sizing por confidence × volatility_scaler × risk_budget con límites. Multiobjetivos retorno, dirección, vol, régimen y cola. Gated ensemble aprendido training/validation. Medir retorno/DD, retorno/exposición, alpha/beta/capture, excess risk-adjusted, underwater y cola. Meta-model confianza/contexto/OOD; drift features/predicción/calibración/performance/régimen → NORMAL/CAUTION/REDUCE/HALT. Forward paper con código/features/hiperparámetros/riesgo/estrategias/umbrales congelados. Todo ello era **propuesta**, no evidencia de haber sido implementado.

### v0.5 (V05)

Afirma implementar target económico, features amplias, horizontes1/3 días, regímenes, no-trade, ensemble temporal, meta-confianza, sizing dinámico, especialistas, turnover y DD. **Multi-activo no probado**: solo BTC verificable. Mismo test visto de v0.4; 10 bps. Warmup features50 días y purga3 días; 64 observaciones training reportadas,37 validation,69 OOS. La relación entre 64 y37 no se documenta claramente en conversación: no sumarlas como particiones disjuntas.

Resultados íntegros H016–H019. Trend Capture +5,01%, Sharpe2,21, DD−3,84%, turnover3,01, exposición12,9%; Hybrid long/cash +0,57%; Gated Rules −0,06%; Hybrid ML −5,43%; ML Economic Edge −8,52%. Buy & Hold28,45 y SMA8,16 siguen superiores retorno absoluto. Ensemble Ridge71,5%, RF28,5%, ET/HGB/MLP0%. Costes10/25/50 bps: Trend5,01/4,53/3,75; ML y Hybrid negativos. Barrido edge5–50 bps no rescata ML (−8,97..−8,03) ni Hybrid (−5,43..−4,93). Cinco seeds híbrido: mejor−4,35, peor−5,43, mediana−4,77, media−4,91.

PASS histórico: temporalidad, purga3 días, features completas OOS, equity/DD/límites, prueba mutación futuro, compilación. No reporta número total de tests. Posteriormente se aclara que anti-futuro cubría **ret20**, no todo pipeline.

Decisión: conservar target económico/no-trade/regímenes/sizing/ensemble con exclusión/meta-confianza/multihorizonte como hipótesis de investigación; congelar MLP con muestra pequeña, no seguir ajustando umbrales a ese test. Explicaciones «cuello de botella ya no arquitectura», «problema estructural» y «eficiencia por exposición» son interpretaciones del asistente, no pruebas causales.

### Diagnóstico y roadmap v0.6 (P06)

Corrección metodológica central: diseño v0.5 usó resultados v0.4 para añadir long/cash y Trend Capture. Aunque las features/modelos no hubieran visto futuro dentro del backtest, investigadores sí orientaron diseño con conocimiento del test. Etiquetar 2024-09-01..11-08 **DEVELOPMENT / VALIDATION BURNED SET**. Nuevo holdout, ajeno al desarrollo, abierto una sola vez tras congelar especificación. No seguir llamando v0.5 validación independiente.

Cambios propuestos (no implementaciones históricas verificadas):
1. ML meta-labeler de señales sencillas (¿supera costes en H períodos?), no principal predictor diario.
2. Core + Tactical; ejemplos base30–50%, overlay−30..+50%, resultado0–100%; parámetros no validados.
3. Régimen multieje: tendencia UP/DOWN/FLAT, volatilidad LOW/NORMAL/HIGH, estructura TRENDING/MEAN-REVERTING/UNCERTAIN. Corrige prioridad high_vol que ocultaba tendencia.
4. Evitar descuentos duplicados: 0,95 × vol_scale × regime_factor × confidence puede hundir posición; ejemplo0,95×0,7×0,55×0,5=18,2875%. Separar señal/confianza/presupuesto/sizing. Vol targeting≈riesgo objetivo/vol esperada × ajuste confianza, limitado.
5. Modelos retorno, downside/cola y meta-labeling.
6. Incertidumbre: intervalos/conformal/residuos walk-forward; filtro lower_confidence_bound > expected_cost + margin. No garantía distribucional demostrada.
7. Datos multi-año BTC/ETH/SOL/posible BNB y1h/4h/1d; observaciones no independientes por ser numerosas; purga/embargo.
8. Nuevas fuentes además de transformaciones OHLCV: funding/OI/basis/liquidaciones/spread/order imbalance/relaciones activos.
9. Simplificar a Ridge/ElasticNet, RF, boosting simple; MLP congelado. MAE MLP0,48/0,80 citado sin especificar aquí unidades/horizonte.
10. Ensemble por out-of-fold walk-forward; utilidad neta−costes−DD−inestabilidad, robustez/peor fold, no mejor fold aislado.
11. Evidencia short mayor que long: reducir/cash antes de short; hipótesis a verificar sin perpetuar sesgo de período alcista.
12. Anti-leak todo pipeline: mutar/añadir futuro no cambia pasado en features/regímenes/modelo/señales; scaler/train, thresholds según protocolo temporal, feature selection/train, ensemble/validation, target no cruza frontera.

Secuencia histórica: jubilar OOS → varios años/activos → multi-axis → Core+Tactical → meta-label/risk filter → incertidumbre → modelos simples → multi-fold → fuentes nuevas → holdout congelado. Arquitectura: datos → features → regímenes → core+tactical → meta-label → downside → incertidumbre → sizing → risk → execution.

## Problemas de consistencia y cautelas concretas

1. **Total5878:** suma aritmética exacta de categorías. «Simulaciones individuales» y «60 pares» mezclan unidades; no decir5878 backtests únicos verificados.
2. **Sin v0.2 ejecutada / v0.3.0:** aparecen planes v2/v3; siguiente entrega explícita es v0.3.1-review. No inventar versiones intermedias.
3. **OOS consumido:** v0.4 fue holdout respecto del entrenamiento según afirmación; v0.5 ya es desarrollo retrospectivo. Por extensión v0.6 no puede validarse allí.
4. **Proveniencia datos:** «repositorio desde2017» no significa haber utilizado todo2017+. Se usó archivo189 filas; URLs y SHA originales ausentes.
5. **64+37+69:** no interpretar como170 filas independientes; podría validation estar contenida en64 disponibles antes de test. Requiere script/cortes originales.
6. **DD signos:** v0.1/v0.3.1 reportan magnitud positiva; v0.4/v0.5 lo escriben negativo. Conservar convención explícita o normalizar mostrando magnitud.
7. **Exposición media ≠ tiempo en mercado:** frase v0.5 «12,9% del tiempo/capital medio» mezcla métricas. Usar exposición media12,9%; no inferir porcentaje de días invertidos.
8. **Costes v0.3.1:** enumeración zero/low/base/medium-high/extreme no coincide exactamente con rótulos ejemplos zero/base/medium/high/extreme. Bps concretos no presentes para toda la curva.
9. **AUC/Sharpe sin incertidumbre:** n pequeño, regímenes heterogéneos, promedios sesgados; no concluir superioridad estadística ni alpha.
10. **Cobertura temporal:** «todas las pruebas de integridad pasaron» no implica todo pipeline causal, especialmente test ret20 único aclarado después.
11. **Diagnósticos categóricos históricos:** «arquitectura ya no cuello de botella», «ML falló por64 ejemplos», «risk engine explica gap_down» son inferencias. No certificación actual.
12. **Umbrales train vs validation:** P05 propone selection validation; P06 dice thresholds solo training. Resolver en protocolo nuevo: selección temporal anidada train/validation, test sellado. No copiar reglas contradictorias literalmente.
13. **28,7 /28,71 bruto y28,45 neto:** compatibles con redondeo/fricción, no cifra inconsistente por sí sola.
14. **22→50 tests y luego PASS sin conteo:** suites diferentes; no sumar como pruebas únicas ni afirmar tests originales disponibles.
15. **Mensaje truncated / contenido opaco:** límite real de exhaustividad; preservar huecos y manifest faltantes en entrega.

## Inventario recuperable y faltantes

Archivo con nombre y ruta de adjunto: PDFM1000v2.pdf. Menciones concretas: quant-system v0.1, quant-system v0.3.1-review, real_sim_v05/, research.yaml, paper.yaml, Dockerfile y Compose sin nombre exacto. strategies/examples/sma_cross.py era ruta propuesta. PROJECT_CONTEXT.md, DECISIONS.md, EXPERIMENT_LOG.md, KNOWN_ISSUES.md y ROADMAP.md se propusieron para el traspaso; su mención histórica no acredita creación.

Referencias generadas opacas: V01 índices1–3; CMP índice2; V04 índices3–9; V05 índices1–10; MIG1 índice5. **22 apariciones** de referencias, no22 archivos únicos demostrados. Cada índice es local al mensaje. V031 puede haber incluido entregables después del recorte; imposible inventariarlos con certeza.

Faltan para reproducción histórica: ZIPs/prototipos fuente, configuraciones exactas, datasets189 filas y raw originales, CSV de matriz/costes/exposure/seeds/predicciones/equity, logs pytest, scripts de experimentos, hyperparameters/cortes/seed exactas, hashes, registro de dependencias y mapping de citas. No reconstruir bytes originales desde narrativa y llamarlos recuperados.

Los números pormenorizados están en `02_EVIDENCIA/EXPERIMENTOS_HISTORICOS.json`; menciones y referencias por mensaje, en `02_EVIDENCIA/MENCIONES_ARCHIVOS.json`. Una nueva implementación basada en esta historia debe etiquetarse claramente como reconstrucción nueva y llevar pruebas actuales separadas.

