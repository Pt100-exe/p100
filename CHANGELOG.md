# Cambios de esta contribución

Primera base independiente creada durante la transferencia de septiembre de 2026. Origen: propuestas posteriores a v0.5, mensaje T11M2. No se dispone de una baseline binaria v0.5 para producir un diff histórico.

- Separación explícita de tendencia y volatilidad en vez de categorías mutuamente excluyentes.
- Propuesta Core + Tactical separada del límite por presupuesto de volatilidad.
- Confianza como filtro del overlay positivo; reducción de exposición permitida con baja confianza.
- Validación de tiempo y valores numéricos, retorno causal disponible en as_of y riesgo que rechaza entradas inválidas.
- Purga temporal por final de etiqueta con fronteras estrictas.
- Registro del intervalo consumido y estados que no certifican un holdout desconocido.
- Congelación por hashes, escritura exclusiva y verificaciones de rutas y cambios.
- 38 pruebas ejecutables con escenarios deterministas y de perturbación.

Decisiones nuevas ilustrativas: parámetros de config/example.json; long/cash para este módulo; tope de riesgo en vez de múltiples descuentos; tercera dimensión de régimen pospuesta; ausencia explícita de datos y holdout. No son resultados de optimización.
