# Roadmap de v0 6

Este plan parte de T11M2, el diagnóstico posterior a v0.5. Los criterios de aceptación y el orden de integración detallado son propuestas de ingeniería de esta transferencia. No se presentan como experimentos ya ejecutados. El estado del código nuevo se describe en CAMBIOS_ACTUALES.md.

## Recuperación y baseline

Recuperar los ZIP históricos, el dataset BTC exacto, configuraciones, curvas, operaciones, salidas de tests y el final de T06M2. Conservar originales con hashes y una copia de trabajo. Identificar el entorno de cada versión antes de instalar dependencias. Reproducir un caso congelado con sus costes y políticas; explicar toda diferencia en vez de cambiar el esperado por conveniencia. v0.5 permanece baseline histórica pendiente de recuperar.

El intervalo 2024-09-01 a 2024-11-08 queda registrado como desarrollo consumido. Se puede usar para verificar regresiones y estudiar mecanismos; sus resultados no pueden presentarse como evidencia independiente. El registro debe distinguir fecha de mercado, fecha de consulta y decisiones que esa consulta informó.

## Datos y reloj

Construir un catálogo con proveedor, endpoint, licencia, instrumento, mercado spot o derivados, frecuencia, zona horaria, inicio/fin, filas, hash y fecha de descarga. Guardar crudos inmutables; registrar huecos, duplicados, outliers, cambios de símbolo y revisiones. No interpolar saltos de precio o volumen de manera que borren eventos relevantes sin justificación.

Registrar por observación event_time, available_at y por decisión decision_time. El cierre de una vela no implica que todos sus campos fueran consumibles exactamente en ese instante. Las features y órdenes deben respetar la disponibilidad real y una convención explícita close t -> open t+1 cuando se use ese esquema.

La propuesta histórica amplía a BTC, ETH, SOL y quizá BNB; frecuencias 1h, 4h y 1d; varios años. Eso sigue pendiente. No son activos seleccionados por una evaluación actual. Diez mil velas horarias no son diez mil observaciones independientes. La alineación multi-activo debe respetar disponibilidad y evitar que una serie filtrada incorpore información posterior de otra.

## Regímenes independientes

Sustituir un enum excluyente high_vol/trend por ejes de tendencia UP/DOWN/FLAT, volatilidad LOW/NORMAL/HIGH y, cuando haya definición comprobable, estructura TRENDING/MEAN_REVERTING/UNCERTAIN. La base nueva implementa los dos primeros; no atribuirle inferencia de estructura no implementada.

Los umbrales aprendidos deben estimarse dentro del training de cada fold y congelarse antes de su validación. Un mercado UP + HIGH debe conservar ambos atributos. Comparar la versión multieje contra la anterior usando idénticos datos y políticas para separar cambio de clasificación de cambio de exposición.

## Core más Tactical

La propuesta histórica usa una exposición estructural más un ajuste táctico. Los ejemplos 30%-50% core, -30% a +50% overlay y 0%-100% final son ilustrativos, no parámetros optimizados ni recomendación de asignación. El componente de señal decide dirección/participación; el presupuesto de riesgo decide tamaño; el risk engine impone límites y vetos.

Evitar cuatro descuentos independientes de volatilidad, régimen y confianza que penalicen repetidamente una misma incertidumbre. Registrar cada paso de posición solicitada, presupuesto, posición final y razón del veto. Distinguir rebalanceo mínimo, histéresis y turnover de filtros de señal. El módulo nuevo prueba una formulación concreta y configurable; su mérito económico está pendiente.

## ML para aceptación y riesgo

Probar por separado un return model, un downside model y un meta-labeler. El meta-labeler recibe una señal candidata de una estrategia definida y estima si su resultado supera costes durante H períodos; la etiqueta debe fijar momento de entrada/salida, costes, tratamiento de solapamientos y vencimiento. El downside model necesita definir el evento de pérdida o cuantíl que intenta anticipar. Esas definiciones aún no se acordaron ni entrenaron aquí.

Comenzar con modelos simples: Ridge o Elastic Net, Random Forest y un boosting sencillo. Congelar temporalmente MLP mientras persista la muestra pequeña y revisar sus problemas de escala/objetivo antes de reintroducirlo. No confundir meta-confianza de v0.5 con un meta-labeler entrenado y calibrado: el código original debe demostrar qué implementó exactamente.

## Incertidumbre y selección

Estudiar intervalos de predicción, conformal o residuos walk-forward. Definir conjunto de calibración, objetivo de cobertura y tratamiento de dependencia temporal y cambios de régimen. La condición propuesta lower_confidence_bound > expected_cost + margin necesita validar unidades y calibración antes de habilitar decisiones; no hay garantía de cobertura universal en datos financieros cambiantes.

Construir predicciones out-of-fold walk-forward para elegir modelos y ensemble. La evaluación propuesta considera utilidad neta, costes, drawdown e inestabilidad entre folds, con posible penalización del peor fold. Coeficientes y métrica primaria deben registrarse antes de consultar el conjunto final. Evitar seleccionar el mejor fold o elegir pesos usando su propia evaluación final.

## Señales y fuentes complementarias

Mantener baselines Cash, Buy & Hold, SMA y reglas sencillas. Evaluar trend, reversión y breakout como hipótesis separadas. El filtro asimétrico de shorts exige más evidencia para abrir una posición corta que para reducir una larga; umbrales y costes específicos de derivados siguen pendientes. No trasladar una ventaja long observada en el rally conocido a una regla universal.

Explorar funding, open interest, basis, liquidaciones, spread, libro y relaciones entre activos cuando haya datos con historial y disponibilidad verificables. Más variantes RSI/SMA pueden añadir redundancia sin información nueva. Cada fuente debe demostrar valor incremental mediante ablación, costes de obtención y ausencia de fuga temporal.

## Protocolo de pruebas y examen final

Probar datos, todas las features, regímenes, fit de preprocesamiento, selección, pesos, modelos, señales y riesgo con prefijos truncados y futuros alterados. Añadir una implementación deliberadamente contaminada para comprobar que la prueba detecta el defecto. Purga debe basarse en el intervalo de la etiqueta, no solo en un número arbitrario de filas; embargo y separación entre instrumentos requieren justificación.

Ejecutar ablaciones con código y datos iguales, escenarios de costes y seeds apropiados, y registrar todos los intentos. Las pruebas nuevas de contratos no sustituyen esa integración. La próxima prueba final debe congelar datos, configuración, código, features, horizontes, criterios y modelos antes de mirar sus resultados; registrar cada acceso al conjunto. Un hash acredita identidad, no que nadie haya visto el contenido.

La validación por etapas termina en forward paper trading con nuevas velas y registro de decisiones. El tiempo de observación y sus criterios se fijan por evidencia, no por reutilizar literalmente los ejemplos de meses del PDF. No se inició un servicio de seguimiento ni operación persistente en esta transferencia.

## Registro mínimo por experimento

ID; hipótesis; fecha y responsable; fuente de la propuesta; versión de código; hashes de datos/config/modelo; activos/frecuencias; rango y disponibilidad; split y purga; features y targets; modelo/hiperparámetros/seeds; política de riesgo; reloj de señal/fill; costes; benchmarks; métricas e intervalos; fallos/advertencias; criterio de aceptación previo; resultado completo; conclusión; siguiente decisión; si consumió algún conjunto de evaluación.
