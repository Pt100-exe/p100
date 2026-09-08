# Auditoría integral del PDF original PDFM1000v2.pdf

Fecha de revisión local: 7-8 de septiembre de 2026. Fuente: `P100_TRANSFER/00_ORIGINALES/PDFM1000v2.pdf`. Se leyó la extracción completa de las 35 páginas y se inspeccionaron visualmente las páginas 9, 11, 28 y 31 para comprobar código y fórmula. Texto íntegro por página preservado en `tmp/pdf_pages.json` (83.909 caracteres según pypdf). El archivo original no se modificó.

## 1. Identidad, alcance y nivel de evidencia

**Hechos documentales.** El título visible es “Guía de estudio e ingeniería para sistemas cuantitativos e IA financiera”; metadatos: “Documento Integrador: IA Financiera y Sistemas Cuantitativos”, autor “Microsoft 365 Copilot”, creador Writer, productor LibreOffice 26.2.0.3, fecha de creación 2026-09-04 18:09:51 UTC. Estos son metadatos del archivo, no prueba de autoría humana ni de verificación técnica. Portada: edición de estudio, 4 de septiembre de 2026. Declara basarse en PDFM1000.pdf y en un mensaje integrador del usuario (p. 1).

El PDF tiene dos capas claramente diferentes:

- **Síntesis editorial y correcciones:** partes I-VIII, pp. 1-13. Organiza alcance, currículo, arquitectura, datos, validación, riesgo, seguridad, Docker, pruebas y fuentes.
- **Registro histórico reproducido:** parte IX, pp. 13-35. Declara transcribir íntegramente el texto de PDFM1000.pdf y conservar sus errores y artefactos. Incluye una URL de conversación de Gemini, `https://gemini.google.com/app/596b7212a98b0e71`, preguntas y respuestas anteriores. Se recuperó después PDFM1000.pdf desde Downloads y se comparó con este anexo: ambos contienen 8 preguntas y 8 respuestas, 40.099 caracteres tras normalizar Unicode y espacios, y el mismo multiconjunto de caracteres. Las diferencias de secuencia corresponden a orden de extracción en tablas y fórmulas (véase sección 12). Esto apoya conservación del texto del PDF anterior; no demuestra que aquel PDF contuviera cada mensaje o adjunto de la conversación web original.

**Límite fundamental:** el PDF no documenta v0.1, v0.2, v0.3.1, v0.4, v0.5 ni roadmap v0.6 del simulador posterior. No proporciona datasets OHLCV completos, backtests ejecutados del proyecto ni tablas de rentabilidad de esas versiones. Sirve como contexto inicial y requisitos, no como evidencia de implementación o resultados del desarrollo posterior.

**Clasificación a mantener en el documento maestro:** una prescripción arquitectónica es una propuesta; un fragmento de código es un ejemplo; una cifra citada en la conversación es un ejemplo o estimación hasta encontrar su ejecución; una corrección calculada localmente sí puede etiquetarse como verificación local y debe especificar sus entradas.

## 2. Mapa completo de las 35 páginas

| Página | Contenido relevante |
|---|---|
| 1 | Portada, propósito, origen PDFM1000.pdf, fecha de consolidación. |
| 2 | Instrucciones de lectura, responsabilidad humana y mapa de nueve partes. |
| 3 | Resumen ejecutivo, arquitectura y prohibiciones de modificar límites/retirar/ocultar logs; tabla de correcciones: Sharpe, umbral 1,5, paper 3-6 meses, diferencia 10%, autoencoder. |
| 4 | Correcciones RL, secretos Compose, lenguaje determinista; advertencia sobre cifras; currículo niveles 0-4. |
| 5 | Currículo niveles 4-8, plan semanal, arquitectura módulos 1-6. |
| 6 | Arquitectura módulos 7-12, RAG, contrato de datos, diseño experimental. |
| 7 | Registro de experimentos, métricas y límites, anti-fugas, primeros controles de riesgo. |
| 8 | Controles de órdenes/credenciales/kill switch/auditoría, amenazas, contexto legal, estructura propuesta. |
| 9 | Árbol de carpetas, Dockerfile didáctico, Compose y secretos. |
| 10 | Resto de Compose, advertencia secretos, pirámide de pruebas, prompts, inicio función Sharpe corregida. |
| 11 | Resto Sharpe, pruebas, checklist Go/No-Go. |
| 12 | Fuentes oficiales y jurídicas secundarias, primeras referencias de libros. |
| 13 | Últimos libros, fecha consulta, nota editorial, mensaje integrador resumido, inicio conversación original y primera pregunta. |
| 14 | Primera respuesta: IA/trading/riesgos; comienzo extensa solicitud de guía rigurosa del usuario. |
| 15 | Solicitud: fuentes clasificadas, fundamentos, matemáticas, mercados, IA, RAG, validación. |
| 16 | Solicitud: riesgo independiente, situaciones desconocidas, legalidad, roadmap, comparadores y formato. |
| 17 | Solicitud: límites de evidencia y no capital real por mero backtest; respuesta con ruta meses 1-6. |
| 18 | Ruta meses 7-12, árboles/RL, arquitectura híbrida de cuatro módulos. |
| 19 | Datos y anomalías, backtesting, fricciones, riesgo, posición, kill switch, API. |
| 20 | Autoencoder/OOD, normativa y fiscalidad general, umbrales Go/No-Go, comienzo bibliografía. |
| 21 | Tabla de libros y herramientas: López de Prado, Hull, Chan, CCXT, Taleb, LEAN. |
| 22 | Expectativas individuales 12-18 meses; prototipo 1-3 pares, 1h/4h, RF, infraestructura <20 USD/mes; pregunta sobre acelerar con IA. |
| 23 | Respuesta sobre tareas de IA, riesgos, estimación 4-6 meses, inicio pregunta sobre prompts. |
| 24 | Prompt genérico peligroso y función SMA 50/200 desplazada; pregunta sobre pruebas. |
| 25 | Pruebas deterministas/límites/temporales/invariantes; prompt detallado de QA y datos Sharpe. |
| 26 | Casos y herramientas pytest/numpy.testing/hypothesis; solicitud de documento completo; inicio documento integrado histórico. |
| 27 | Resumen repetido, diagrama textual de fases, fundamentos y mercados. |
| 28 | Fórmula Sharpe visualmente descompuesta, Sortino/MDD/VaR, validación, arquitectura. |
| 29 | RAG/OOD/riesgo, tabla de prompts, ejemplos repetidos. |
| 30 | SMA, código original de Sharpe y comienzo pruebas originales. |
| 31 | Prueba Sharpe incorrecta 18,2562, casos cero/NaN, Hypothesis, bibliografía. |
| 32 | Bibliografía, repetición de puertas 1,5 / 3-6 meses / 10%. |
| 33 | Continuación puertas; usuario pide PDF; respuesta menciona archivo generado y lista lo supuestamente incluido. |
| 34 | Resto lista, mención errónea de variables cifradas; usuario insiste en conversación completa; nueva propuesta de ruta. |
| 35 | Última propuesta de ruta, pregunta final del asistente histórico, cierre editorial. |

## 3. Idea inicial y requisitos expresos del usuario histórico

La primera pregunta plantea una IA que opere en cripto, trading, acciones y “virtual marketing” para producir ingresos pasivos seguros (pp. 13-14). La conversación reformula el alcance a aprendizaje, datos históricos y simulación; rechaza garantías de beneficio y el salto inmediato a dinero real. El desarrollo posterior debe preservar esta reformulación explícita, no convertir el deseo inicial en promesa.

La petición larga de pp. 14-17 exige:

1. Guía progresiva para diseñar, programar, entrenar, evaluar y mantener un sistema financiero técnicamente sólido.
2. Gestión del riesgo, preservación del capital, ciberseguridad y validación científica como prioridades.
3. Fuentes oficiales, investigación académica, libros, cursos, conferencias, repositorios y comunidades, diferenciando opiniones y evidencia. Para cada fuente: contenido, prerrequisitos, fiabilidad, relación con proyecto, sesgos, coste y fase de estudio.
4. Python, estructuras, POO, tests, Git, Linux, Docker, bases de datos, APIs, nube, cifrado, credenciales, permisos y registros.
5. Álgebra, cálculo, probabilidad, estadística, series temporales, procesos estocásticos, optimización, métodos numéricos, causalidad, sesgos, incertidumbre e hipótesis.
6. Acciones y cripto, órdenes, liquidez, volatilidad, spread, costes, microestructura, cartera, concentración, apalancamiento y ruina.
7. Limpieza, ML supervisado/no supervisado, regímenes, incertidumbre, RL con límites, interpretabilidad, anomalías y comparación con reglas simples.
8. Evaluación de entrenar un gran modelo frente a combinar bases de datos, RAG, modelos especializados y controles; combatir datos falsos, antiguos, repetidos, manipulados y contradictorios.
9. Trazabilidad de cada decisión a datos, modelo y reglas. Más información no implica mejores decisiones.
10. Baseline, entrenamiento/validación/prueba separados, backtesting temporal, walk-forward, estrés, costes, spread, slippage, latencia, impuestos y fallos; prevención de overfitting, data snooping, survivorship y look-ahead.
11. Paper trading y criterios de abandono/revisión/parada sustentados en evidencia.
12. Capa de riesgo independiente que pueda vetar al modelo: exposición, pérdidas, tamaño, apalancamiento, diversificación, anomalías, API, variaciones extremas, parada manual, alertas, auditoría, prohibición de retiros y recuperación.
13. Reconocer incertidumbre, OOD y regímenes nuevos; reducir exposición, no operar o pedir revisión cuando falte confianza. No atribuir predicción de acontecimientos desconocidos.
14. Regulación/fiscalidad/privacidad/licencias/términos de uso, dependiendo de jurisdicción y fecha.
15. Roadmap con proyectos, tecnologías, tiempos bajo supuestos, costes, entregables, criterios, errores, ejercicios y checklist; distinguir evidencia/práctica/propuesta experimental.
16. Comparar con cartera pasiva, reglas simples y no operar; medir también riesgo, drawdown, estabilidad, costes, liquidez, capacidad y estrés.
17. Identificar capacidad individual, especialistas necesarios y expectativas personales realistas. No inventar datos, resultados o porcentajes; no avanzar a real solo por un backtest rentable.

## 4. Arquitectura de referencia: propuesta del PDF

La arquitectura inicial de cuatro módulos (pp. 18, 28-29) se amplía editorialmente a doce componentes (pp. 5-6):

1. **Ingesta:** conectores, frecuencia, rate limits, reintentos y reloj.
2. **Almacén/catálogo:** crudos inmutables, normalizados, metadatos, licencias, hashes y versiones.
3. **Calidad:** esquemas, tiempo monótono, duplicados, huecos, outliers y reconciliación.
4. **Investigación:** notebooks exploratorios separados de paquetes reproducibles.
5. **Features/etiquetas:** ajuste solo con pasado, linaje y ventanas explícitas.
6. **Modelos:** baselines, candidatos, calibración, drift y registro de artefactos.
7. **Backtester:** eventos, reloj simulado, cartera, órdenes, fills, fees, slippage y fallos.
8. **Risk engine:** determinista, independiente, bloquea por defecto.
9. **Paper execution:** adaptador separado, sandbox/testnet cuando proceda, sin permisos de retiro.
10. **Observabilidad:** métricas, logs, trazas, alertas y reconciliación.
11. **Auditoría:** versiones de datos, código, configuración, modelo y decisiones.
12. **Supervisión humana:** aprobaciones de operación, pausas, kill switch e incidentes.

El módulo semántico RAG se propone para documentos/noticias y extracción estructurada, no para generar órdenes. Debe conservar fuente, publicación, consulta, jurisdicción, licencia, fragmentos recuperados, versión y confianza; deduplicar y marcar documentos sustituidos; mostrar discrepancias. El gestor de incertidumbre agrupa contradicciones y variabilidad de modelos. Autoencoder OOD, Random Forest, XGBoost, LSTM, Transformers y RL son opciones/propuestas, sin prueba en este PDF de modelos entrenados o desplegados.

**Estructura propuesta (pp. 8-9):** `pyproject.toml`, `README.md`, `.gitignore`, `compose.yaml`, `Dockerfile`, `config/{research,paper}.yaml`, `data/` fuera de Git, `src/quant_system/{data,features,models,backtest,risk,execution,observability}`, `tests/{unit,integration,property,temporal}`, `notebooks/`, `docs/{decisions,runbooks}`. No se debe afirmar que esta estructura existe solo porque está impresa.

## 5. Contrato de datos, diseño experimental e integridad temporal

**Contrato mínimo (p. 6):** UTC interno conservando zona original; reloj y latencia; OHLCV con tipos/unidades/precisión/moneda/agregación; proveedor/endpoint/símbolo/licencia/fecha descarga; hash/filas/rango/huecos/duplicados; correcciones versionadas con motivo y responsable; timestamp de disponibilidad efectiva en producción. El anexo añade splits/dividendos, caídas de exchanges y cautela al filtrar flash crashes (p. 19).

**Diseño (pp. 6-7):** hipótesis falsable y métrica primaria antes de observar resultados; conjunto final fuera de muestra con acceso restringido; transformaciones dentro del fold; benchmark pasivo/regla simple/no operar; fees/spread/slippage/latencia/rechazos en escenarios; distribuciones/intervalos/sensibilidad; todos los experimentos registrados para medir selección retrospectiva.

**Anti-fugas (p. 7):** no barajar sin justificación; separar evento/disponibilidad/decisión; fit de escaladores/imputación/selección solo en entrenamiento; purgar etiquetas solapadas y gap/embargo acorde a dependencia; probar que el futuro no altera salidas históricas; congelar conjunto final y registrar sus consultas.

**Límite a remarcar:** `.shift(1)` es una convención coherente si se decide antes de disponer de la barra actual, pero por sí solo no acredita ausencia total de fugas. Deben declararse reloj de decisión, disponibilidad, etiquetado, entrenamiento y ejecución. Una simulación por eventos tampoco garantiza por sí sola realismo exacto de latencia o fills.

## 6. Métricas y fórmulas

El PDF explica retorno total/anualizado, volatilidad, Sharpe, Sortino, máximo drawdown, VaR, CVaR/ES, turnover/costes y calibración (p. 7). Límites asociados: trayectoria ausente en retorno; simetría de volatilidad; no normalidad/autocorrelación/frecuencia para Sharpe; umbral y downside para Sortino; muestra observada para MDD; cola más allá del cuantil para VaR; escasez de extremos para ES; ejecución para costes; regímenes/drift para calibración.

La fórmula tipográfica de Sharpe de p. 28 está descompuesta visualmente: numerador y denominador quedan muy separados. Su lectura es `SR = E[Rp - Rf] / sigma_p`. No debe trasladarse como imagen ilegible al nuevo documento. Para la función concreta de pp. 10-11:

`exceso_i = retorno_i - rf_anual / periodos_ano`

`sigma = desviacion_muestral(exceso, ddof=1)`

`Sharpe_anualizado = media(exceso) / sigma * sqrt(periodos_ano)`

Esta convención usa reparto lineal de una tasa anual y factor de anualización fijo, no conversión compuesta de tasa ni ajuste por autocorrelación. La frecuencia `252` debe entenderse como parámetro del ejemplo, no reutilizarse automáticamente para barras cripto de 1h o 4h.

**Resultado experimental local verificado de manera independiente, sin pandas:** usando `statistics` y `math` del runtime Python, entradas `[0.01,0.02,-0.01,0.03,0.01]`, `rf_anual=0.001`, `periodos_ano=252`: media `0.012`; varianza muestral `0.00021999999999999998`; desviación muestral `0.014832396974191326`; media exceso `0.011996031746031746`; Sharpe `12.838862164299517`. Confirma la corrección editorial de pp. 3 y 11. El esperado `18.2562` de p. 31 es incompatible con esa función y esas entradas.

**Otros umbrales y números:** 1,5 de Sharpe; 3-6 meses paper; diferencia de P&L 10%; pérdida diaria 2% con pausa 24h; latencia 50-100 ms; 1-3 pares; 1h/4h; 12-18 meses individual; 4-6 meses con ayuda IA; coste <20 USD/mes. Todos son ejemplos, heurísticas o estimaciones históricas. No son resultados medidos del proyecto ni puertas universales. El PDF no aporta fórmulas desarrolladas de Kelly, Sortino, VaR/ES ni cálculo verificable de esos costes.

## 7. Riesgo, seguridad y operación: requisitos

**Risk engine (pp. 7-8):** límites por activo/clase/contraparte/global; límites diarios/acumulados ex ante; tope duro de apalancamiento; veto por precios/timestamps/feed inválidos; circuit breaker API/timeout/rate limits; idempotencia y límites de tamaño/precio; reconciliación; credenciales mínimas y retiros desactivados; allowlist IP si disponible; parada manual/automática periódicamente probada; logs append-only de señal/veto/orden/fill/versión/usuario.

La frase del PDF “apalancamiento ... cero como valor inicial” es ambigua si se interpreta como razón exposición/equity: debe concretarse como **sin endeudamiento ni posiciones apalancadas**, distinguiéndolo de exposición nula. La propuesta histórica de liquidar todo y revocar claves “instantáneamente” (p. 19) requiere especificación por plataforma y condiciones, no garantiza fills ni revocación instantánea.

**Amenazas (p. 8):** claves en Git/logs/notebooks/imágenes/soporte; supply chain; prompt injection/documento manipulado RAG; cambio API/símbolo; replay/órdenes duplicadas; cuenta/SIM swap/2FA; manipulación de datos/proveedor/reloj.

**Docker (pp. 9-10):** Python 3.12-slim, usuario no privilegiado, variables que impiden bytecode y buffer; app read-only, tmpfs, drop ALL capabilities, no-new-privileges; secretos por archivo/servicio; modo paper; PostgreSQL 17 con volumen. Madurez propuesta: fijar versiones/hashes, SBOM, escaneo, multistage, exclusión de secretos. Corrección explícita: Compose no proporciona automáticamente cifrado del host ni reemplaza permisos/rotación/gestor de secretos.

**Contexto normativo (pp. 8,12,20):** el PDF contiene referencias secundarias a normativa costarricense fechadas en 2026 y pide comprobar texto oficial y aplicabilidad. Para el traspaso son afirmaciones históricas no revalidadas aquí. No deben presentarse como asesoramiento ni conclusión vigente de obligaciones de Patrick. El requerimiento trasladable es gestionar jurisdicción/fecha/licencias/términos/privacidad y revisión profesional cuando corresponda.

## 8. Pruebas, criterios de avance y defectos del material didáctico

**Pirámide de pruebas (p. 10):** unitarias (retornos/fees/redondeo/tamaño/límites); temporales (futuro/disponibilidad); propiedades (capital/pesos/límites); integración (proveedor/DB/schema/retries/idempotencia); simulación (fills parciales/latencia/gaps/caída/rate limits); regresión (artefacto/datos congelados); operación/caos (reinicio/red/reloj/clave revocada).

**Dimensiones históricas (pp. 25-26):** casos deterministas con cálculo independiente; límites como varianza nula/división/NaN; invariancia temporal; invariantes de cartera. `pytest`, `numpy.testing`, `hypothesis` son propuestas de herramientas. “Los pesos siempre suman 1” necesita especificar si se incluye efectivo y si existe apalancamiento.

**Go/No-Go editorial (p. 11):** hipótesis/métricas previas, procedencia/licencias, cero fugas conocidas, costes y ejecución, benchmarks fuera de muestra, sensibilidad/estrés, riesgo independiente, no retiros, kill switch/recuperación, logs/reconciliación, revisión jurídica/fiscal actual, revisión independiente y aceptación escrita de riesgos residuales. La decisión por defecto si falta control crítico es No-Go; no operar es válido.

### Hallazgos de revisión local, distintos de las correcciones que ya trae el PDF

1. **Prueba temporal insuficiente, comprobado experimentalmente.** El ejemplo de p. 11 calcula una serie de 300 observaciones y otra de 301, pero compara solo primeras 250. Se ejecutó un contraejemplo con `base=pd.Series(range(300),dtype=float)` y `rolling(50).mean().shift(-1)`: usa información de la barra siguiente y aun pasa exactamente ese esquema de comparación de primeras 250. El buffer sin comprobar oculta la fuga. Debe validarse contra prefijos que terminan justo en cada decisión y contra alteraciones del futuro, además de disponibilidad, no solo añadir una fila lejana.
2. **Fragmentos incompletos.** La función `sma_desplazada` llamada en p. 11 no se define en el PDF; el bloque de pruebas corregidas requiere importar `pytest`. Por ello no se puede etiquetar todo como suite directamente ejecutable.
3. **Invariancia de Sharpe global mal enunciada en el anexo (p. 26).** Cambiar el tamaño de la muestra cambia legítimamente el Sharpe agregado. La propiedad debe comparar una salida histórica calculada con el mismo prefijo, no exigir que el Sharpe de N observaciones sea igual al de N+100.
4. **Ejemplo Docker no validado.** P. 9 instala el paquete tras copiar solo `pyproject.toml`, antes de copiar `src`. En un layout habitual `src/`, puede no instalar el paquete correcto o fallar si el build requiere fuentes/README. No hay pyproject completo en el PDF ni evidencia de build. PostgreSQL tampoco tiene configuración completa de inicialización/conectividad/healthchecks. Debe tratarse como plantilla parcial, no despliegue probado.
5. **Política Sharpe cero discutible.** La versión corregida devuelve `0.0` para menos de dos valores, periodos no positivos, sigma casi cero/no finita o resultado no finito. Esto mezcla insuficiencia de datos/error/infinito con un Sharpe económico nulo. Debe explicitarse la política y contemplar estado de validez separado. La elección no prueba rentabilidad ni ausencia de errores.
6. **Hypothesis histórico pendiente de compatibilidad.** P. 31 combina floats acotados `[-0.5,0.5]` con `allow_nan=True`; es un punto a revisar frente a la versión concreta, no prueba ejecutada aquí (Hypothesis no está instalado en el runtime revisado). Independientemente, comprobar solo tipo finito no garantiza exactitud numérica ni integridad temporal.
7. **Afirmaciones demasiado absolutas en registro histórico.** “Comisiones insignificantes” por usar 1h/4h, “latencia cero” institucional, “imitar exactamente” producción, indicadores sin alfa desde hace décadas, posibilidad de detectar con autoencoder un régimen nunca visto, todos los errores financieros indetectables por IA, velocidad/calendario/coste prometidos, retiro/revocación instantánea: requieren matices o evidencia. Se preservan en transcripción, pero no se promueven a hechos del documento maestro.
8. **Riesgo de usar umbrales como garantías.** Superar Sharpe 1,5 o seis meses no acredita seguridad; la propia capa editorial corrige esto. La discrepancia relativa de P&L de 10% además requiere definir denominador y manejo de valores pequeños/negativos, y no identifica por sí sola una causa.
9. **Trazabilidad de adjuntos limitada.** El anexo menciona `guia_ia_financiera_completa.pdf` y un marcador `[file-tag: code-generated-file-39a83229-a319-4de5-b9f3-ef7065c08b0c]` (p. 33). Eso documenta que se mencionó un archivo, no recupera su contenido binario ni confirma que esté disponible. El PDF preserva descripción, no ese adjunto.

## 9. Roadmap educativo original, sin atribuirlo a v0.6

El currículo editorial (pp. 4-5) cambia un calendario rígido por entregables:

| Nivel | Orientación temporal histórica | Entregable y puerta |
|---|---|---|
| 0 Riesgo/método | 1-2 semanas sugeridas | Objetivos, registro riesgos, política sin capital real; explicar límites del backtest. |
| 1 Python/Git/Linux/testing | 6-10 semanas | Paquete, README, pruebas, instalación reproducible, sin secretos. |
| 2 Datos/estadística | 8-12 semanas | Pipeline OHLCV/catálogo/calidad; tiempo/zonas/duplicados/faltantes documentados. |
| 3 Mercados/microestructura | 6-10 semanas | Simulador limitado/costes; distinguir señal/orden/fill/posición/P&L realizado y no realizado. |
| 4 Backtesting | 8-12 semanas | Eventos/walk-forward/purga/benchmarks/costes/anti-fugas; fuera de muestra, seeds y versiones. |
| 5 ML financiero | 10-16 semanas | Baseline frente a ML, incertidumbre; mejora tras costes y periodos múltiples. |
| 6 Híbrido/RAG | 6-10 semanas | Citas y salida insuficiente evidencia; fuente/fecha/versión/confianza. |
| 7 Paper/operación | Evidencia, no calendario | Risk engine, auditoría, recuperación, divergencias explicadas y cero bypass. |
| 8 Revisión independiente | Antes de capital real | Informe Go/No-Go y riesgos residuales; No-Go si faltan pruebas. |

Plan semanal: estudio con notas/fuentes; pequeña implementación con commit/docstring/ejemplo; tests deterministas/límites/propiedades; revisión de fugas/supuestos/fallos; reflexión sobre cambios/incertidumbre/próximo paso.

El prototipo histórico sugerido (p. 22) usa 1-3 pares líquidos, BTC/USDT y ETH/USDT como ejemplos, frecuencia 1h/4h, Random Forest de reversión tras volatilidad, SQLite/PostgreSQL y datos públicos de klines. No debe imponerse al proyecto posterior si decisiones y experimentos posteriores lo sustituyeron. El roadmap v0.6 debe recuperarse de la conversación posterior y confrontarse con estos principios, no inventarse a partir de esta lista.

## 10. Fuentes que deben preservarse como referencias del PDF

Fecha de consulta declarada: 4 de septiembre de 2026. No fueron reconsultadas durante esta extracción.

- Python Tutorial: `https://docs.python.org/3/tutorial/index.html`.
- pandas User Guide: `https://pandas.pydata.org/docs/user_guide/index.html`.
- scikit-learn TimeSeriesSplit: `https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html` (el PDF advierte que no implementa toda purga de etiquetas).
- scikit-learn Cross-validation: `https://scikit-learn.org/stable/modules/cross_validation.html`.
- Docker Compose secrets: `https://docs.docker.com/compose/how-tos/use-secrets/`.
- CCXT Manual: `https://github.com/ccxt/ccxt/wiki/Manual`.
- LEAN: `https://www.quantconnect.com/docs/v2/lean-engine/getting-started`.
- Referencias legales secundarias históricas: `https://aglegal.com/es/regulacion-cripto-costa-rica/`; `https://consortiumlegal.com/en/2026/06/24/vasp-regulation-costa-rica/`.
- Libros: *Advances in Financial Machine Learning* (Marcos López de Prado); *Options, Futures, and Other Derivatives* (John C. Hull); *Algorithmic Trading* (Ernest P. Chan); *Statistical Consequences of Fat Tails* (Nassim Nicholas Taleb); *The Elements of Statistical Learning*; *Forecasting: Principles and Practice*.

No se han convertido URLs en evidencia vigente de precios, legislación o capacidades. La función de esta lista es conservar la trazabilidad del material recibido.

## 11. Qué confrontar con el desarrollo v0.1-v0.5

Para cada versión real, pedir evidencia disponible de: contrato de datos y fecha de disponibilidad; procedimiento de fold/preprocesamiento/labels; reloj señal-orden-fill; costes y benchmark; activos/frecuencia/rango/filas; seed/config/versión/hash; risk engine y estado de paradas; pruebas ejecutadas y salidas; resultado fuera de muestra frente a ejemplo sintético; divergencias encontradas; límites y estado de implementación.

Las mejoras posteriores pueden satisfacer, modificar o posponer requisitos del PDF. El documento maestro debe conservar la cadena “requisito original -> decisión posterior -> artefacto/experimento -> limitación -> próximo paso”. Si falta un archivo, el vacío se declara en el inventario. No se reconstruyen resultados ni código ausentes con apariencia de original.

## 12. Recuperación del primer PDF y comparación reproducible

Se encontró `C:/Users/Patrick/Downloads/PDFM1000.pdf` y se copió sin modificarlo a `P100_TRANSFER/00_ORIGINALES/PDFM1000.pdf`. Tiene 14 páginas, 1.360.706 bytes y 46.617 caracteres extraídos por pypdf; SHA256 `9b1b96a98260b127e8cc024db88b0949bd157921c1e35d0110017b9fa840333f`. El PDFM1000v2.pdf de Downloads tiene el mismo SHA256 que la copia del paquete: `1ac4796614ba80f122a456531bad08cbc99b94b5354ca9d144d1cc2b2587c9db`.

**Método:** extracción de ambas fuentes con pypdf; retirada de cabeceras/pies del v2; aislamiento del texto de sección 27 antes del cierre editorial; normalización Unicode NFKC y retirada de espacios; comparación de secuencia de caracteres con SequenceMatcher sin autojunk; conteos de marcadores y caracteres. Resultado:

- Primer PDF: 8 marcadores `User prompt:` y 8 `Response:`. Anexo de v2: 8 y 8.
- Longitud normalizada: exactamente 40.099 caracteres cada uno.
- El multiconjunto de caracteres normalizados es idéntico: no sobran caracteres en un lado frente al otro.
- Similitud de secuencia: 96,89518442%; 127 bloques de diferencia inspeccionados.
- Los bloques reflejan orden de lectura de columnas/celdas de bibliografías, tabla de pruebas y tabla de prompts; además, subíndices y variables de fórmulas aparecen al final de páginas del primer PDF y en línea en el v2. No se detectó omisión de prosa en estos bloques.
- Esta métrica de secuencia **no representa un 3,1% de contenido faltante**: las tablas están ordenadas de forma distinta por extracción. El mismo conteo de caracteres tampoco es por sí solo prueba absoluta de identidad semántica. Se preservan ambos binarios para comprobación visual y posibles discrepancias.

El primer PDF contiene la conversación de Gemini que comienza con la pregunta sobre ingresos pasivos seguros y termina con la propuesta de ruta diaria. No aporta los binarios de los adjuntos mencionados ni las versiones v0.1-v0.5. El marcador histórico del archivo generado sigue sin ser un adjunto recuperado.

**Artefactos entregados para reproducir la auditoría:** `P100_TRANSFER/06_VERIFICACION/pdf_checks/verify_pdf_sources.py`; extracciones por página `PDFM1000_pages.json` y `PDFM1000v2_pages.json`; `verification_results.json` con hashes, diferencias completas y resultados numéricos; `verification.log` con ejecución, entorno y resumen. El script reproduce tanto la comparación como el cálculo independiente de Sharpe y el contraejemplo temporal. Estas comprobaciones son pruebas sintéticas de matemática e integridad documental, no experimentos de rentabilidad.
