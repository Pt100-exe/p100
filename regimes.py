"""Tendencia y volatilidad son ejes independientes, sin prioridad excluyente."""

from dataclasses import dataclass
from enum import Enum

from .validation import finite_number


class Trend(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    FLAT = "FLAT"


class Volatility(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


@dataclass(frozen=True)
class Regime:
    trend: Trend
    volatility: Volatility


@dataclass(frozen=True)
class RegimeConfig:
    trend_threshold: float = 0.02
    low_vol: float = 0.20
    high_vol: float = 0.60

    def __post_init__(self):
        trend = finite_number(self.trend_threshold, "trend_threshold")
        low = finite_number(self.low_vol, "low_vol")
        high = finite_number(self.high_vol, "high_vol")
        if trend < 0 or not 0 <= low < high:
            raise ValueError("umbrales inválidos")


def classify_regime(trend_score: float, annual_vol: float, config: RegimeConfig = RegimeConfig()) -> Regime:
    trend_score = finite_number(trend_score, "trend_score")
    annual_vol = finite_number(annual_vol, "annual_vol")
    if annual_vol < 0:
        raise ValueError("annual_vol no puede ser negativa")
    trend = Trend.UP if trend_score > config.trend_threshold else (
        Trend.DOWN if trend_score < -config.trend_threshold else Trend.FLAT
    )
    volatility = Volatility.LOW if annual_vol < config.low_vol else (
        Volatility.HIGH if annual_vol > config.high_vol else Volatility.NORMAL
    )
    return Regime(trend, volatility)
