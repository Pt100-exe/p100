# Registro de experimentos históricos

20 grupos de resultados declarados, sin nueva reproducción de los backtests. Porcentajes expresados en puntos porcentuales; un campo percent=5.01 significa 5.01%. null se muestra como No reportado. Los nombres de métricas conservan sus unidades y la marca approx cuando existe. Los drawdowns se conservan con el signo de su fuente; no homogeneizar máximos negativos y magnitudes positivas sin explicarlo.

Los grupos reúnen tablas y pruebas comunicadas, no necesariamente ejecuciones independientes. Todos tienen currently_reproduced=false. La fuente primaria es la transcripción literal; los JSON estructurados facilitan consulta y no reemplazan archivos de mercado o resultados que faltan.

## H001 Demostración v0.1

Fuente T01M2 | Mensaje 490a0916-4eb8-4285-a127-79832daba466

### Protocolo

- data: OHLCV sintético determinista
- bars: 800
- initial_equity_usd: 10000
- execution: apertura siguiente, SMA desplazada una barra, long/cash

### Resultados

- final_equity_usd: 10221.76
- sharpe: 2.57
- max_drawdown_percent: 1.72

### Límites

- No demuestra alpha ni rentabilidad esperada.

## H002 Suite y stress v0.1

Fuente T01M2 | Mensaje 490a0916-4eb8-4285-a127-79832daba466

### Protocolo

- seeds: 100
- bars_per_seed: 600

### Resultados

- software_tests_passed: 22
- software_tests_total: 22
- stress_impossible_states: 0
- final_equity_approx_usd_range: 9515, 10748

### Límites

- No están presentes logs ni tests originales en las dos páginas JSON.

## H003 Conservador vs experimental relajado

Fuente T04M2 | Mensaje 7e663b03-d4d1-4747-955d-967fd52e7705

### Protocolo

- seeds: 200
- bars_per_seed: 600
- timeframe: 1h
- data: sintético común
- fee_bps: 5
- slippage_bps: 3
- signal: misma SMA desplazada
- initial_equity_usd: 10000
- policies.conservative: long/cash, máximo 25%, límites diarios/DD
- policies.relaxed: aprox. 95% long o short, sin límites diarios/DD

### Resultados

| Métrica | conservative | relaxed |
|---|---|---|
| return_mean_percent | 0.61 | -0.86 |
| return_median_percent | 0.28 | -2.72 |
| profitable_runs_percent | 55.5 | 41.5 |
| sharpe_mean | 0.64 | -0.25 |
| sharpe_median | 0.63 | -0.45 |
| dd_mean_percent | 2.77 | 16.09 |
| dd_median_percent | 2.59 | 15.52 |
| dd_worst_percent | 5.97 | 33.61 |
| trades_mean | 281 | 472 |
| final_equity_mean_usd | 10061 | 9914 |
- relaxed_outperforms_return_percent: 40.5
- relaxed_outperforms_sharpe_percent: 34.5
- relaxed_lower_dd_count: 0
- return_correlation_approx: 0.73
- conservative_return_p05_p95_percent_approx: -2.92, 5.48
- relaxed_return_p05_percent_approx: -20.58
- relaxed_upper_return_percent_approx: 23.86
- relaxed_trades_increase_percent_approx: 68

### Límites

- Comparación de exposición/riesgo, no de capacidad predictiva.
- El texto no identifica inequívocamente +23,86% como máximo o p95.

## H004 Tamaño de batería v0.3.1-review

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- data: 15 regímenes sintéticos

### Resultados

- reported_total: 5878
- categories.main_matrix: 1710
- categories.cost_sensitivity: 735
- categories.exposure: 1260
- categories.sample_length: 168
- categories.train_test_split: 392
- categories.probability_threshold: 336
- categories.oneshot_vs_walkforward: 96
- categories.model_seed_stability: 200
- categories.predictive_evaluations: 36
- categories.rule_parameter_combinations: 450
- categories.negative_oracle_controls: 90
- categories.fuzz: 300
- categories.reproducibility: 60
- categories.legacy_equivalence: 45
- software_tests_passed: 50
- software_tests_total: 50

### Límites

- La suma de categorías es 5878.
- 60 comprobaciones de reproducibilidad son descritas después como 60 pares: número de ejecuciones distinto del de comparaciones.
- El mensaje llega recortado a 20 000 unidades UTF-16; el resto requiere una exportación del original.

## H005 Capacidad predictiva sintética

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- representative_regimes: 6

### Resultados

| model | roc_auc_mean_approx | brier_approx | balanced_accuracy_approx |
|---|---|---|---|
| MLP | 0.503 | 0.296 | 0.514 |
| Extra Trees | 0.5 | 0.252 | 0.498 |
| Logistic | 0.493 | 0.289 | 0.487 |
| Random Forest | 0.487 | 0.258 | 0.505 |
| HGB | 0.486 | 0.271 | No reportado |
| Ensemble | 0.483 | 0.266 | No reportado |

### Límites

- No se reportan intervalos de confianza ni filas predictivas.
- Ningún ML promovido; resultados cercanos a discriminación aleatoria.

## H006 Agregados 15 regímenes y patrones artificiales

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- all_regimes: random_walk, drift_up, drift_down, mean_revert, high_vol, low_vol, regime_switch, jump_crash, trend_reversal, vol_cluster, flat, alternating, gap_up, gap_down, ar_mean_revert

### Resultados

- mean_median_return_percent_approx.Logistic aggressive: 21.8, -3.75
- mean_median_return_percent_approx.Random Forest aggressive: 17.3, -4.15
- mean_median_return_percent_approx.Ensemble aggressive: 19.1, -4.51
- mean_median_return_percent_approx.Q-Learning aggressive: 14.3, -1.32
- q_learning_profitable_runs_percent_approx: 26.7
- alternating_return_percent_approx.Mean Reversion aggressive: 396
- alternating_return_percent_approx.Logistic aggressive: 348
- alternating_return_percent_approx.HGB aggressive: 322
- mean_reversion_in_mean_reverting_regime.return_percent_approx: 23
- mean_reversion_in_mean_reverting_regime.profitable_seeds_percent: 100

### Límites

- Los promedios dominados por patrones fáciles no demuestran generalización.

## H007 Subconjunto de 10 regímenes menos artificiales

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- excluded: flat, alternating, gap_up, gap_down, ar_mean_revert

### Resultados

| model | return_mean_percent | return_median_percent | profitable_percent | sharpe_mean | dd_mean_percent |
|---|---|---|---|---|---|
| SMA 20/50 aggressive | 3.35 | 2.9 | 56.7 | 0.23 | 18.8 |
| SMA 20/50 adaptive | 1.9 | 1.58 | 53.3 | 0.06 | 12.1 |
| v0.1 legacy | -1.02 | -1.11 | 40 | No reportado | 4.1 |
| Logistic aggressive | -4.39 | No reportado | 3.3 | No reportado | No reportado |
| Random Forest aggressive | -5.04 | No reportado | 0 | No reportado | No reportado |
| Ensemble aggressive | -5.38 | No reportado | 0 | No reportado | No reportado |
- dd_more_precise_percent.SMA aggressive: 18.84
- dd_more_precise_percent.SMA adaptive: 12.14

### Límites

- Resumen seleccionado después de observar heterogeneidad; conservar ambos resúmenes.

## H008 Controles random y oracle

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- oracle: oracle_future_LEAK_INVALID
- oracle_status: INVALID / TEST-ONLY / NEVER CANDIDATE

### Resultados

- return_mean_percent_approx.random.conservative: -4
- return_mean_percent_approx.random.adaptive: -15.6
- return_mean_percent_approx.random.aggressive: -29
- return_mean_percent_approx.oracle.conservative: 20.6
- return_mean_percent_approx.oracle.adaptive: 159.7
- return_mean_percent_approx.oracle.aggressive: 556.8

### Límites

- Oracle usa futuro deliberadamente: nunca candidato financiero.

## H009 Sensibilidad a costes sintéticos

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- representative_regimes: 7
- reported_labels: zero, low, base, medium/high, extreme

### Resultados

- mean_reversion_aggressive.zero: 14.1
- mean_reversion_aggressive.base: -1.4
- mean_reversion_aggressive.medium: -13.6
- mean_reversion_aggressive.high: -45
- mean_reversion_aggressive.extreme: -73.5
- logistic_aggressive.zero: 2.5
- logistic_aggressive.base: -3.5
- logistic_aggressive.high: -24.3
- logistic_aggressive.extreme: -44.1
- ensemble.zero: 1.9
- ensemble.base: -4.6
- ensemble.high: -26.6
- ensemble.extreme: -47.2

### Límites

- Porcentajes aproximados.
- Etiquetas de niveles de coste no uniformes entre enumeración y ejemplos; importes bps no presentes.

## H010 Exposición y thresholds

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- exposure_percent_approx: 10, 25, 40, 60, 75, 95
- short_modes: No, Sí
- probability_thresholds: 0.5, 0.52, 0.55, 0.6

### Resultados

- logistic_95_long_short.mean_return_percent_approx: 22.6
- logistic_95_long_short.median_return_percent_approx: -2.5
- threshold_finding: Mayor threshold redujo actividad sin mejora sistemática.

### Límites

- No se preservan todas las filas de barrido en el texto.

## H011 One-shot vs walk-forward expansivo

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- policy: conservative
- models: Logistic, RF, HGB, Ensemble

### Resultados

- return_percent_approx.Logistic: -0.32, -0.31
- return_percent_approx.Random Forest: -0.4, -0.44
- return_percent_approx.HGB: -1.01, -0.95
- return_percent_approx.Ensemble: -0.62, -0.52
- column_order: one_shot, walk_forward

### Límites

- No apareció ventaja general reportada.

## H012 Seeds, fuzz, reproducibilidad, equivalencia

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- fuzz_runs: 300
- reproducibility_pairs: 60
- equivalence_datasets: 45
- equalized_costs.fee_bps: 5
- equalized_costs.slippage_bps: 3
- equalized_costs.half_spread_bps: 0

### Resultados

- model_seed_return_mean_std_percent_approx.Logistic conservative: -1.18, 0.34
- model_seed_return_mean_std_percent_approx.Ensemble: -1.11, 0.45
- model_seed_return_mean_std_percent_approx.HGB: -2.07, 0.61
- fuzz_failures: 0
- fuzz_worst_dd_percent_approx: 60.4
- reproducibility_discrepancies: 0
- equivalence_mean_return_difference_pp_approx: 0.0058
- equivalence_median_return_difference_pp_approx: 0.00024
- with_2bps_halfspread_mean_return_difference_pp_approx: -0.093
- gap_down_return_difference_pp_approx: 0.249

### Límites

- Atribuir mejora gap_down al reduce-only es hipótesis del asistente histórico, no causalidad probada.

## H013 Agregación políticas de riesgo

Fuente T06M2 | Mensaje 69184771-b0a3-4e0e-aeef-ee06818cb816

### Protocolo

- datasets: 45
- aggregation: todos los modelos

### Resultados

| policy | return_mean_percent | return_median_percent | dd_mean_percent | dd_p95_percent | fees_mean_usd_approx |
|---|---|---|---|---|---|
| Conservative | 0.16 | -0.52 | 2.02 | 7.24 | 68 |
| Adaptive | 6.69 | -3.04 | 7.69 | 19.43 | 471 |
| Aggressive | 10.96 | -4.14 | 11.19 | 34.94 | 712 |

### Límites

- Medianas negativas a pesar de promedios positivos; universos artificiales heterogéneos.

## H014 Replay real v0.4

Fuente T08M2 | Mensaje da278096-36cd-45dd-9452-3de4f778857e

### Protocolo

- symbol: BTC/USDT
- timeframe: 1d
- provider_as_reported: repositorio público identifica Binance Spot, actualizado desde API Binance; URL no preservada
- data_start: 2024-05-04
- data_end: 2024-11-08
- rows_reported: 189
- ml_training_until: 2024-08-29
- oos_start: 2024-09-01
- oos_end: 2024-11-08
- oos_decisions: 69
- execution: cierre t para señal, open t+1 para orden
- cost_bps_per_turnover: 10
- policy: adaptive

### Resultados

| strategy | return_net_percent | sharpe | max_dd_signed_percent |
|---|---|---|---|
| Buy & Hold | 28.45 | 3.26 | -8.73 |
| SMA 20/50 | 8.16 | 1.45 | -14.09 |
| Random Forest | 6.42 | 1.18 | -12.21 |
| MLP | 5.3 | 1 | -14.95 |
| Mean Reversion | 2.58 | 0.81 | -4.8 |
| HistGB | 1.58 | 0.42 | -11.97 |
| Cash | 0 | 0 | 0 |
| Logistic | -3.92 | -0.5 | -16.54 |
| Momentum 20 | -7.26 | -1.07 | -14.61 |
| Ensemble | -17.03 | -2.93 | -22.85 |
| Extra Trees | -17.99 | -3.12 | -23.27 |
- btc_market_return_percent_approx: 28.7

### Límites

- Solo 69 decisiones, un activo y ventana alcista; no evidencia robusta de alpha.
- Q-Learning excluido por escasez de visitas de estado.
- Replay histórico, no forward paper trading.

## H015 Predicción, stress costes y conservadores

Fuente T08M2 | Mensaje da278096-36cd-45dd-9452-3de4f778857e

### Protocolo

- oos_decisions: 69
- cost_stress_bps: 25

### Resultados

- auc_oos.MLP: 0.58
- auc_oos.Logistic: 0.554
- auc_oos.Extra Trees: 0.546
- auc_oos.Ensemble: 0.531
- auc_oos.Random Forest: 0.53
- auc_oos.HistGB: 0.48
- returns_10_25bps_percent.SMA: 8.16, 7.62
- returns_10_25bps_percent.Random Forest: 6.42, 3.23
- returns_10_25bps_percent.MLP: 5.3, 2.75
- returns_10_25bps_percent.Mean Reversion: 2.58, 0.38
- returns_10_25bps_percent.HistGB: 1.58, -1.78
- returns_10_25bps_percent.Logistic: -3.92, -7.39
- sma_conservative.return_percent: 4.89
- sma_conservative.sharpe: 2.9
- sma_conservative.max_dd_signed_percent: -2.16
- mlp_conservative.return_percent_approx: 4.75
- mlp_conservative.mean_exposure_percent_approx: 5.5

### Límites

- AUC 0,58 no basta para concluir alpha.
- Exposición media baja puede distorsionar lectura de Sharpe aislado.

## H016 Comparativa v0.5 sobre período ya observado

Fuente T10M2 | Mensaje 93136b8a-71c4-46de-9cb9-b6abbff3cf34

### Protocolo

- symbol: BTC/USDT
- timeframe: 1d
- oos_start: 2024-09-01
- oos_end: 2024-11-08
- oos_decisions: 69
- cost_bps: 10
- usable_training_observations_reported: 64
- validation_observations_reported: 37
- target_horizons_days: 1, 3
- feature_warmup_days: 50
- test_classification_current: DEVELOPMENT / VALIDATION BURNED SET

### Resultados

| strategy | return_percent | sharpe | max_dd_signed_percent | turnover | mean_exposure_percent |
|---|---|---|---|---|---|
| Buy & Hold | 28.45 | 3.26 | -8.73 | 2 | 100 |
| v0.4 SMA adaptive | 8.16 | 1.45 | -14.09 | 3.4 | 72.9 |
| Trend Capture | 5.01 | 2.21 | -3.84 | 3.01 | 12.9 |
| Hybrid long/cash | 0.57 | 0.47 | -1.75 | 3.15 | 7.1 |
| Cash | 0 | 0 | 0 | 0 | 0 |
| Gated Rules | -0.06 | 0.03 | -4.95 | 7.22 | 25.7 |
| Hybrid ML | -5.43 | -1.98 | -7.31 | 11 | 32.6 |
| ML Economic Edge | -8.52 | -2.47 | -12.62 | 9.78 | 35.5 |
- ensemble_weights_percent.Ridge: 71.5
- ensemble_weights_percent.Random Forest: 28.5
- ensemble_weights_percent.Extra Trees: 0
- ensemble_weights_percent.HistGB: 0
- ensemble_weights_percent.MLP: 0

### Límites

- No es OOS independiente: desarrollo informado por resultados v0.4.
- 64 training y 37 validation no pueden asumirse conjuntos disjuntos sin código.
- La fuente mezcla exposición media con tiempo en mercado; no son equivalentes.
- Multi-activo no implementado/testado en esta ronda por datos disponibles.

## H017 Stress costes v0.5

Fuente T10M2 | Mensaje 93136b8a-71c4-46de-9cb9-b6abbff3cf34

### Protocolo

- cost_bps: 10, 25, 50

### Resultados

- return_percent.Buy & Hold: 28.45, 28.06, 27.41
- return_percent.SMA: 8.16, 7.62, 6.72
- return_percent.Trend Capture: 5.01, 4.53, 3.75
- return_percent.Hybrid Long/Cash: 0.57, 0.09, -0.69
- return_percent.Gated Rules: -0.06, -1.14, -2.92
- return_percent.Hybrid ML: -5.43, -6.98, -9.43
- return_percent.ML Economic Edge: -8.52, -9.86, -12.04

### Límites

- Barrido sobre período consumido; útil descriptivamente y para desarrollo.

## H018 Thresholds y seeds v0.5

Fuente T10M2 | Mensaje 93136b8a-71c4-46de-9cb9-b6abbff3cf34

### Protocolo

- edge_threshold_bps_approx_range: 5, 50
- hybrid_model_seeds: 5

### Resultados

- ml_pure_return_percent_approx_range: -8.97, -8.03
- hybrid_return_percent_approx_range: -5.43, -4.93
- hybrid_seeds.best_percent_approx: -4.35
- hybrid_seeds.worst_percent_approx: -5.43
- hybrid_seeds.median_percent_approx: -4.77
- hybrid_seeds.mean_percent_approx: -4.91

### Límites

- No se conservan seeds exactas ni tabla completa.
- Cinco seeds negativas no prueban imposibilidad estructural; sí describen esta muestra.

## H019 Integridad v0.5 reportada

Fuente T10M2 | Mensaje 93136b8a-71c4-46de-9cb9-b6abbff3cf34

### Protocolo

- checks: OOS posterior a training, purga target 3 días, cero features faltantes OOS, equity finita, drawdowns válidos, límites posición, mutación precios futuros no cambia features históricas, compilación script

### Resultados

- reported_status: PASS
- numeric_test_count: No reportado

### Límites

- La revisión posterior especifica que la prueba anti-futuro cubría ret20, no todo el pipeline.
- No equivale a auditoría actual ni prueba completa de ausencia de fugas.

## H020 Datos de validación citados en diagnóstico v0.6

Fuente T11M2 | Mensaje 006998a6-5c51-4e74-81af-e30848f810e6

### Protocolo

- model: MLP

### Resultados

- validation_mae_approx: 0.48, 0.8
- ensemble_weight_percent: 0

### Límites

- No especifica en este mensaje correspondencia MAE-horizonte ni unidades.
- Diagnóstico histórico sin tabla original recuperada.