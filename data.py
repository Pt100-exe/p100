from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import math
from p100_lab.engine import Bar
from p100_foundations.validation import finite_number


@dataclass(frozen=True)
class Instrument:
    symbol: str
    asset_class: str
    quote: str
    periods_per_year: int
    calendar: str

    def __post_init__(self):
        if not self.symbol or not self.quote:
            raise ValueError("instrumento sin identificar")
        if self.asset_class not in ("crypto_spot", "equity_spot"):
            raise ValueError("clase sin modelo de ejecución implementado")
        if isinstance(self.periods_per_year, bool) or not isinstance(self.periods_per_year, int) or self.periods_per_year<=0:
            raise ValueError("anualización inválida")
        if self.calendar not in ("daily_24x7", "explicit_sessions"):
            raise ValueError("calendario desconocido")


def parse_klines(raw, instrument, start, end, *, latency_seconds=1):
    """Adapter Binance 1d; expected interval [start,end), known completed historical bars."""
    if instrument.asset_class != "crypto_spot" or instrument.calendar != "daily_24x7" or instrument.periods_per_year != 365:
        raise ValueError("este adaptador solo admite spot cripto diario UTC")
    if not 0 <= finite_number(latency_seconds, "latency") < 86400:
        raise ValueError("latencia diaria inválida")
    if start.tzinfo is None or end.tzinfo is None or start >= end:
        raise ValueError("rango inválido")
    if not isinstance(raw, list) or len(raw) != (end-start).days:
        raise ValueError("cobertura incompleta")
    bars, normalized = [], []
    for i, row in enumerate(raw):
        if not isinstance(row, list) or len(row) != 12:
            raise ValueError("fila klines inválida")
        if type(row[0]) is not int or type(row[6]) is not int:
            raise ValueError("timestamps deben ser enteros en milisegundos")
        expected = start + timedelta(days=i)
        expected_close = expected+timedelta(days=1, milliseconds=-1)
        if row[0] != int(expected.timestamp()*1000) or row[6] != int(expected_close.timestamp()*1000):
            raise ValueError("hueco, duplicado, unidad temporal o duración incorrecta")
        opening, closing = expected, expected_close
        o, h, l, c, v = [float(row[j]) for j in (1, 2, 3, 4, 5)]
        if not all(math.isfinite(x) for x in (o,h,l,c,v)) or min(o,h,l,c)<=0 or v<0:
            raise ValueError("OHLCV no finito o fuera de rango")
        if not l <= min(o,c) <= max(o,c) <= h:
            raise ValueError("OHLC inconsistente")
        available = closing + timedelta(seconds=latency_seconds)
        bars.append(Bar(opening, closing, available, o, c))
        normalized.append(dict(symbol=instrument.symbol, open_time=opening.isoformat(), close_time=closing.isoformat(),
                               available_at_assumed=available.isoformat(), open=o, high=h, low=l, close=c, volume=v))
    return bars, normalized
