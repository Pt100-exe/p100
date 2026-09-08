from math import sqrt
from statistics import stdev
from p100_foundations.regimes import classify_regime
from p100_foundations.strategy import ExposureIntent, propose_exposure
from p100_foundations.risk import size_exposure
from .execution import Target

POLICIES = ("cash", "buy_hold", "core_risk", "core_tactical_risk", "core_tactical_band")


def make_signal(policy, instrument):
    if policy not in POLICIES:
        raise ValueError("política desconocida")
    def signal(history):
        if len(history)<31:
            return None
        if policy=="cash":
            return Target(0.)
        if policy=="buy_hold":
            return Target(1.)
        prices = [b.close for b in history[-31:]]
        returns = [b/a-1 for a,b in zip(prices,prices[1:])]
        vol = max(.01, stdev(returns)*sqrt(instrument.periods_per_year))
        regime = classify_regime(prices[-1]/prices[0]-1, vol)
        intent = ExposureIntent(.4, 0., 1.) if policy=="core_risk" else propose_exposure(regime)
        risk = size_exposure(intent, vol)
        if not risk.allowed:
            raise ValueError("riesgo rechazó señal")
        return Target(risk.target_exposure, risk.risk_cap, .05 if policy=="core_tactical_band" else 0.)
    return signal
