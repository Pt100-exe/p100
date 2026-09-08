# P100 — avance 002: datos reales y observación en sombra

Leer AVANCE_002.md y ARQUITECTURA_MERCADOS.md. El protocolo previo está en PROTOCOL_002.md. Este directorio es una revisión independiente; no modifica P100_LAB ni los archivos históricos.

## Ejecutar sin red

Python 3.12, biblioteca estándar. Desde esta carpeta:

```text
python -B -m unittest discover -s tests -v
python -B audit_study.py
python -B audit_shadow.py
python -B verify_delivery.py
```

El auditor histórico vuelve a comprobar los 45 resultados guardados y los hashes congelados. El auditor en sombra reproduce la primera captura y prueba que repetirla no duplica las seis intenciones; está diseñado para la entrega inicial con seis registros. Tras acumular nuevas sesiones deberá adaptarse a la cantidad de registros, conservando esta entrega como evidencia inicial.

## Captura nueva de observación

```text
python -B -m market_lab.shadow
```

Hace tres solicitudes HTTPS públicas y termina. Solo registra intenciones calculadas con velas cerradas, junto a la hora real de observación. No mantiene un servicio ni envía órdenes. La red puede requerir autorización del entorno. La repetición de una vela/política con idéntico contenido es idempotente; si cambian datos o código para esa misma clave, se rechaza el conflicto y se requiere una nueva revisión deliberada.

La última señal no debe ejecutarse retrospectivamente en una apertura anterior a su hora real de observación. El registro todavía no es una cuenta paper con fills futuros; esa integración es una siguiente etapa.

## Estudio histórico y reproducción

results/study_002 contiene el intento inicial bloqueado por permisos de red. results/study_002_retry contiene la ejecución completa autorizada, congelada antes de obtener precios, con 45 curvas. Los originales se guardan en data/. Todos los precios de 2025 son desarrollo consumido.

Para reproducir con nuevas descargas, usa una copia de trabajo limpia del código, tests, config y protocolo, con data/ vacío, y un identificador nuevo:

```text
python -B -m market_lab.study --run reproduction_001
```

El runner rechaza datos existentes para evitar sobrescribir los originales. Para verificar la entrega actual sin descargar de nuevo, usa audit_study.py. El servidor puede revisar históricos; comparar siempre hashes de datos, código y métricas.

## Contenido

- market_lab/data.py: contrato de instrumento y parser Binance diario con validaciones OHLCV/UTC/cobertura.
- market_lab/execution.py: cola de disponibilidad y banda con prioridad del límite de riesgo.
- market_lab/signals.py: políticas fijas con anualización por instrumento.
- market_lab/study.py: descarga pública, congelados, ensayo, trimestres y evaluación de hipótesis.
- market_lab/shadow.py: observación puntual de datos actuales y registro SQLite de intenciones.
- p100_foundations/ y p100_lab/: copias de la base anterior. El estudio nuevo usa market_lab.execution; p100_lab.engine aporta la aritmética de rebalanceo ya probada. El runner sintético anterior conserva su propio reloj y no debe confundirse con el nuevo.
- tests/: 52 métodos anteriores y 15 nuevos (11 mercado/ejecución, cuatro observador).
- results/tests_pre_data.log, tests_shadow_initial_failure.log, tests_final.log: evidencia de pruebas y del fallo SQLite corregido.
- data/: respuestas originales y CSV normalizados de los tres instrumentos.
- results/study_002_retry/: catálogo, congelados, métricas, curvas, trimestres, hipótesis y auditoría.
- results/shadow/: primera captura, respuestas originales, seis intenciones y auditoría.
- CUADERNO_TECNICO_002.md: informe y código para lectura continua.
- MANIFEST.json: hashes de la entrega. Nuevas capturas pueden cambiar la base SQLite; conserva el ZIP como revisión inicial verificable.

Sin instalación de broker, credenciales, apalancamiento ni automatización recurrente.
