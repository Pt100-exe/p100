"""Partición cronológica de un único fold con purga de horizontes."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Sequence

from .validation import aware_time


@dataclass(frozen=True)
class LabeledWindow:
    feature_time: datetime
    label_end: datetime


@dataclass(frozen=True)
class TemporalSplit:
    train: tuple[int, ...]
    validation: tuple[int, ...]
    excluded: tuple[int, ...]


def purged_split(rows: Sequence[LabeledWindow], validation_start: datetime, validation_end: datetime, *, pre_validation_gap: timedelta = timedelta(0)) -> TemporalSplit:
    """Training label_end < validation_start - gap, desigualdad estricta.

    La validación exige feature_time en [start,end) y label_end < end.
    No añade training posterior: no es CPCV ni embargo de datos posteriores.
    """
    start = aware_time(validation_start, "validation_start")
    end = aware_time(validation_end, "validation_end")
    if start >= end:
        raise ValueError("ventana de validación vacía o invertida")
    if not isinstance(pre_validation_gap, timedelta) or pre_validation_gap < timedelta(0):
        raise ValueError("pre_validation_gap debe ser timedelta no negativo")
    try:
        train_cutoff = start - pre_validation_gap
    except OverflowError as exc:
        raise ValueError("gap fuera del rango datetime") from exc
    train, validation, excluded = [], [], []
    previous = None
    for index, row in enumerate(rows):
        feature_time = aware_time(row.feature_time, "feature_time")
        label_end = aware_time(row.label_end, "label_end")
        if label_end < feature_time or (previous is not None and feature_time <= previous):
            raise ValueError("filas desordenadas, duplicadas o con label_end anterior")
        previous = feature_time
        if feature_time < start and label_end < train_cutoff:
            train.append(index)
        elif start <= feature_time < end and label_end < end:
            validation.append(index)
        else:
            excluded.append(index)
    return TemporalSplit(tuple(train), tuple(validation), tuple(excluded))
