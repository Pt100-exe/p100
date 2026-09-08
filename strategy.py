"""La estrategia propone exposición; la política de riesgo la limita aparte."""

from dataclasses import dataclass

from .regimes import Regime, Trend, Volatility
from .validation import finite_number


@dataclass(frozen=True)
class ExposureIntent:
    core: float
    tactical: float
    confidence: float = 1.0


@dataclass(frozen=True)
class StrategyConfig:
    core: float = 0.40
    tactical_up: float = 0.30
    tactical_down: float = -0.30
    tactical_flat: float = 0.0

    def __post_init__(self):
        if not 0 <= finite_number(self.core, "core") <= 1:
            raise ValueError("core debe estar entre 0 y 1")
        for name in ("tactical_up", "tactical_down", "tactical_flat"):
            if not -1 <= finite_number(getattr(self, name), name) <= 1:
                raise ValueError(f"{name} debe estar entre -1 y 1")


def propose_exposure(regime: Regime, confidence: float = 1.0, config: StrategyConfig = StrategyConfig()) -> ExposureIntent:
    confidence = finite_number(confidence, "confidence")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence debe estar entre 0 y 1")
    if not isinstance(regime.trend, Trend) or not isinstance(regime.volatility, Volatility):
        raise ValueError("régimen inválido")
    tactical = {
        Trend.UP: config.tactical_up,
        Trend.DOWN: config.tactical_down,
        Trend.FLAT: config.tactical_flat,
    }[regime.trend]
    return ExposureIntent(config.core, tactical, confidence)
