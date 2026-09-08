# P100 — ensayo 002, fijado antes de consultar precios

## Objetivo

Pasar del laboratorio sintético a una primera prueba histórica con datos públicos reales. Aislar el efecto de una banda de rebalanceo y comprobar un reloj conservador de disponibilidad. No es una prueba con dinero, no reproduce v0.5 y no acredita rentabilidad futura.

## Diseño previo

- Universo fijo por continuidad del roadmap: BTCUSDT, ETHUSDT, SOLUSDT spot. Son tres activos de una sola clase y un solo proveedor, no tres mercados independientes.
- Fuente propuesta: API pública de Binance, endpoint GET /api/v3/klines, frecuencia 1d UTC, año civil 2025 completo (365 filas por símbolo). Se conservan respuesta cruda, URL, fecha de consulta, hash y CSV normalizado. Los datos descargados se consideran desarrollo histórico consumido, no holdout desconocido.
- Si la fuente no está disponible o no supera las validaciones, no sustituir precios ni fuente silenciosamente; registrar fallo y continuar ingeniería con fixtures.
- OHLC completo, volumen no negativo, fechas únicas ordenadas, sin huecos de días en cripto 24/7; rechazar barras incompletas o rangos inválidos. No interpolación ni corrección silenciosa.
- Disponibilidad histórica REAL desconocida: modelar close_time + 1 segundo. Señal calculada con el prefijo a esa disponibilidad. Fill en la primera apertura posterior, por tanto normalmente t+2 en velas diarias contiguas. Es conservadurismo temporal, no reconstrucción del feed real.
- Primeros 30 retornos de cada serie para calentamiento. Sin entrenamiento ni selección de hiperparámetros. Mantener el intervalo quemado de 2024 fuera de esta ejecución no vuelve independiente a 2025.
- Cuatro políticas: cash, buy_hold, core_risk, core_tactical_risk; una quinta, core_tactical_band, usa la misma señal/riesgo y una banda fija de 5 puntos porcentuales al ejecutar. Si la diferencia entre peso actual y objetivo es menor que 0.05, conservar posición solo si no excede el límite de riesgo; objetivo cero siempre liquida en el fill simulado. La igualdad a 0.05 rebalancea.
- Core=0.40, overlay=±0.30, umbral tendencia ±0.02 a 30 retornos, volatilidad muestral anualizada sqrt(365), mínimo 0.01, presupuesto 0.20, confianza constante 1. No ML, cortos ni apalancamiento.
- Comisiones por lado 0/10/30 pb; deslizamiento 0/5/5 pb respectivamente. 45 ejecuciones totales. Un capital separado de 10000 USDT por activo y política; no sumar estas cuentas como una cartera.
- Publicar retorno, drawdown, exposición, turnover, costes, órdenes pendientes, días y trades para las 45 ejecuciones. Publicar bloques trimestrales derivados de la curva continua; no llamarlos folds walk-forward ni muestras independientes.

## Hipótesis y puerta siguiente

H1 (costes): a comisión 10 pb, la banda reduce o iguala turnover y coste frente a core_tactical_risk en cada uno de los tres activos. H2 (degradación): en cada activo, retorno no empeora más de 1 punto porcentual y drawdown no empeora más de 1 punto porcentual. Para promover la banda deben cumplirse H1 y H2 en TODOS. No cambiar tolerancias al ver resultados. El resultado de este ensayo sirve para desarrollo; no basta para desplegar una estrategia rentable.

Puerta de ingeniería para una prueba en sombra: pruebas causales y contables pasan; parser rechaza datos corruptos; entradas y configuración están congeladas; no existe conexión para enviar órdenes; registro de decisiones persistente detecta duplicados. Si falta alguna, completar antes de proponer seguimiento. Una prueba en sombra observa datos reales y registra intenciones sin dinero. No se inicia un servicio recurrente sin indicar claramente su alcance.

## Ampliación de mercados

Separar proveedor, instrumento, calendario, anualización y ejecución. Admitir un contrato OHLC normalizado para spot; verificar evidencia por clase. Acciones/ETF necesitan ajustes corporativos y calendarios de sesión; FX conversiones y calendario; futuros vencimientos, multiplicadores, margen y funding. Esos adaptadores económicos no están implementados por aceptar una etiqueta. Mercados no financieros requieren definir valor, liquidez, acciones y objetivos con Patrick.

## Referencias revisadas

- https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market — esquema oficial de klines (12 campos, timestamps, paginación y UTC).
- https://github.com/binance/binance-public-data — referencia del proveedor para archivos públicos; no es fuente descargada en este ensayo.
- TikTok aportado por Patrick: https://vt.tiktok.com/ZSqrXtKt6/ . El navegador de investigación rechazó la apertura del enlace; no se vio el video ni se extrajeron requisitos de su contenido.
