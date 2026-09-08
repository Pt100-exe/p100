"""Sizing long/cash de un activo, sin broker ni efectos secundarios."""

from dataclasses import dataclass

from .strategy import ExposureIntent
from .validation import finite_number


@dataclass(frozen=True)
class RiskPolicy:
    target_annual_vol: float = 0.20
    max_exposure: float = 1.0
    min_tactical_confidence: float = 0.50

    def __post_init__(self):
        target = finite_number(self.target_annual_vol, "target_annual_vol")
        maximum = finite_number(self.max_exposure, "max_exposure")
        confidence = finite_number(self.min_tactical_confidence, "min_tactical_confidence")
        if target <= 0 or not 0 <= maximum <= 1 or not 0 <= confidence <= 1:
            raise ValueError("política de riesgo inválida")


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    target_exposure: float
    requested_exposure: float
    risk_cap: float
    reason: str


def size_exposure(intent: ExposureIntent, forecast_annual_vol: float, policy: RiskPolicy = RiskPolicy(), *, halted: bool = False) -> RiskDecision:
    """Un único límite por volatilidad; confianza filtra solo el overlay.

    Una salida de cero ante datos inválidos expresa un objetivo de investigación,
    NO una orden de liquidación ni una garantía de ejecución segura.
    """
    def reject(reason):
        return RiskDecision(False, 0.0, 0.0, 0.0, reason)

    if not isinstance(halted, bool):
        return reject("invalid_halt_state")
    if halted:
        return reject("halted")
    try:
        core = finite_number(intent.core, "core")
        tactical = finite_number(intent.tactical, "tactical")
        confidence = finite_number(intent.confidence, "confidence")
        vol = finite_number(forecast_annual_vol, "forecast_annual_vol")
    except (ValueError, AttributeError):
        return reject("invalid_input")
    if not 0 <= core <= 1 or not -1 <= tactical <= 1 or not 0 <= confidence <= 1 or vol <= 0:
        return reject("invalid_input")
    # Un overlay negativo reduce riesgo y no necesita superar la confianza.
    accept_tactical = tactical <= 0 or confidence >= policy.min_tactical_confidence
    requested = core + (tactical if accept_tactical else 0.0)
    maximum = policy.max_exposure
    # Evita overflow de target / vol en volatilidades positivas subnormales.
    cap = maximum if maximum == 0 or vol <= policy.target_annual_vol / maximum else policy.target_annual_vol / vol
    target = min(max(0.0, requested), cap)
    reason = "accepted" if accept_tactical else "core_only_low_confidence"
    if target < max(0.0, requested):
        reason += ";risk_capped"
    return RiskDecision(True, target, requested, cap, reason)
