# Estado de P100 y organización por componentes

## Decisión actual de Patrick

Centrarse en mercados conocidos y suficientemente funcionales. Desarrollar y perfeccionar componentes por separado antes de integrarlos. Expandir a otras clases de mercado después de comprobar lo existente. Otros compañeros están trabajando en partes del proyecto, pero aquí no se conocen ni se asignan sus tareas.

Esta entrega es un respaldo portátil. No añade estrategias, experimentos económicos, servicios recurrentes ni operaciones reales.

## Estado comprobado

- Historia: fuentes accesibles documentadas; faltan ZIP/CSV históricos y parte de un mensaje. v0.5 no está reproducida.
- Base v0.6 independiente: contratos temporales, regímenes y riesgo, con 38 tests.
- Avance 001: simulador con efectivo/unidades, comisiones y deslizamiento; 52 tests y 3240 simulaciones sintéticas.
- Avance 002: datos públicos diarios de BTCUSDT, ETHUSDT y SOLUSDT de 2025, 45 simulaciones y 67 tests. La banda de rebalanceo pasó el criterio previo de coste/degradación en esa muestra. La auditoría reconstruyó 16425 estados.
- Observación actual: seis intenciones registradas, dos políticas por activo, con velas cerradas. Se detectan duplicados. No se enviaron órdenes y todavía no hay fills virtuales prospectivos ni P&L forward. No hay seguimiento automático activo.

Los tests de las revisiones posteriores incluyen los anteriores: 38, 52 y 67 NO son tres conjuntos independientes para sumar como nuevas pruebas distintas. Los precios de 2025 ya son desarrollo consumido, no un examen final independiente.

## Componentes para integrar por etapas

| Componente | Base existente | Criterio antes de unirlo |
|---|---|---|
| Datos y calendario | Parser cripto diario, OHLCV, hashes y cobertura | Fuente y disponibilidad verificables; huecos y revisiones explícitos |
| Señal | Core y ajuste táctico, reglas fijas | Causalidad, comparación con baseline y costes; sin presentar hipótesis como alpha |
| Riesgo | Tope de exposición por volatilidad, long/cash | Límites verificables y razones de rechazo; especificar alcance por instrumento |
| Ejecución simulada | Cuenta y cola temporal; banda | Reconciliación, costes, lotes y rellenos realistas antes de paper avanzado |
| Registro en sombra | SQLite, observación puntual y duplicados | Convertir intenciones en fills virtuales solo después de observed_at |
| Evaluación | Manifiestos, tests, auditoría y resultados completos | Congelar hipótesis y muestras; conservar resultados negativos |

No se presupone que un compañero esté a cargo de una fila. Para incorporar su trabajo: traer código, contrato de entradas/salidas, pruebas y versión; comparar con el componente actual; integrar en una revisión nueva sin sobrescribir evidencia congelada.

## Próximo componente que tiene sentido perfeccionar aquí

El vínculo entre el registro en sombra y una cuenta paper persistente: consumir una intención una sola vez, esperar un precio posterior a su observación, registrar un fill virtual y conciliar efectivo/unidades. Se propone este foco para la continuación; no se presenta como implementado en esta copia.

Por ahora el soporte real demostrado es cripto spot diario de un proveedor. Acciones/ETF, FX y derivados requieren adaptadores propios; no se anuncian como soportados por tener campos de metadatos genéricos.
