# Informe de pruebas de la base nueva

VERIFICADO EN ESTA TAREA. Ejecución conservada: 8 de septiembre de 2026 a las 01:10:40 UTC, equivalente al 7 de septiembre a las 19:10:40 en Costa Rica. Python 3.12.14; Windows 11. Biblioteca estándar; ninguna llamada a broker o proveedor de datos.

Comando: `python -B -m unittest discover -s tests -v`.

Resultado: **38 pruebas ejecutadas, 38 aprobadas, cero fallos y cero errores**, 0.033 segundos informados por unittest. Salida completa en test_run.log. Dentro de los métodos hay 9 combinaciones de regímenes y una rejilla de 720 combinaciones de parámetros, además de subcasos de entradas inválidas y fronteras temporales. No son 720 backtests.

Se verificó también `python -B -m p100_foundations verify`: PASS, lista de errores vacía. El manifiesto declara NO_MARKET_DATA_PROVIDED y holdout NOT_SELECTED. Su hash de contenido es 70bd9ce5cdead51d1002dd1bd2a67744b1e3a3d9aa451b6b47b189e6ab6f029f.

La revisión comprobó fórmulas de tamaño y convenciones temporales en el código. No se ejecutaron las suites históricas 22/22 o 50/50 y no se reprodujeron los 5 878 escenarios declarados en v0.3.1. Las pruebas de causalidad cubren solo la cadena determinista implementada, con volatilidad fijada en los fixtures; no cubren modelos entrenados, selección de features o pesos de ensemble.
