"""Registro explícito de evaluación consumida, sin certificar OOS desconocido."""

from dataclasses import dataclass
from datetime import datetime, timezone

from .validation import aware_time


@dataclass(frozen=True)
class EvaluationWindow:
    start: datetime
    end: datetime

    def __post_init__(self):
        if aware_time(self.start, "start") >= aware_time(self.end, "end"):
            raise ValueError("intervalo vacío o invertido")


BURNED_WINDOW = EvaluationWindow(
    datetime(2024, 9, 1, tzinfo=timezone.utc),
    datetime(2024, 11, 9, tzinfo=timezone.utc),
)
BURNED_RECORD = {
    "status": "DEVELOPMENT_VALIDATION_BURNED_SET",
    "start_inclusive": BURNED_WINDOW.start.isoformat(),
    "end_exclusive": BURNED_WINDOW.end.isoformat(),
    "reported_dates": "2024-09-01 a 2024-11-08, inclusivas",
    "reported_decisions": 69,
    "evidence_type": "historical_conversation_claim_not_reproduced",
    "conversation_id": "6a9df532-f49c-83e8-b7c7-f4431ecd3238",
    "v04_turn_id": "88a1be21-91b9-4869-94cc-5b95c76eb84d",
    "v04_item_id": "da278096-36cd-45dd-9452-3de4f778857e",
    "normalization": "Fechas civiles convertidas conservadoramente a días UTC completos; no proceden de CSV recuperado.",
}


def candidate_holdout_status(window: EvaluationWindow | None) -> str:
    if window is None:
        return "NOT_SELECTED"
    if window.start < BURNED_WINDOW.end and BURNED_WINDOW.start < window.end:
        raise ValueError("la ventana candidata se solapa con evaluación consumida")
    # Evitar una falsa certificación: no solaparse no demuestra no haberla visto.
    return "CANDIDATE_NOT_VERIFIED_UNSEEN"
