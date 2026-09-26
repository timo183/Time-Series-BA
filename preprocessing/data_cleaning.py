from datetime import datetime

import numpy as np
import pandas as pd

from common.loader import load_panel
from common.writer import save_panel
from config import END_DATETIME, START_DATETIME

CORRECTION_TIMESTAMPS = pd.to_datetime(
    [
        "2019-03-31 03:00",
        "2020-03-29 03:00",
        "2021-03-28 03:00",
        "2022-03-27 03:00",
        "2023-03-26 03:00",
        "2024-03-31 03:00",
    ],
    utc=True,
)


def normalize_dates(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.reset_index()
    panel["DateUTC"] = pd.to_datetime(panel["DateUTC"], utc=True, errors="raise")
    return panel


def validate_source_fields(panel: pd.DataFrame) -> pd.DataFrame:
    frame = panel.copy()

    if "DateUTC" not in frame.columns:
        frame = frame.reset_index()
    required = {"DateUTC", "Value", "TimeFrom", "TimeTo"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(frame.columns))}")
    frame["DateUTC"] = pd.to_datetime(frame["DateUTC"], utc=True, errors="raise")
    if frame[list(required)].isna().any().any():
        raise ValueError("Missing timestamps, interval labels, or load values")
    if not np.isfinite(frame["Value"]).all():
        raise ValueError("Load values must be finite")
    if (frame["DateUTC"] != frame["DateUTC"].dt.floor("h")).any():
        raise ValueError("Timestamps must lie on hourly boundaries")

    return frame


def correct_known_timestamps(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    time_from = pd.to_timedelta(frame["TimeFrom"], errors="raise")
    time_to = pd.to_timedelta(frame["TimeTo"], errors="raise")
    hour, day = pd.Timedelta(hours=1), pd.Timedelta(days=1)
    for labels in (time_from, time_to):
        if (
            labels.isna()
            | (labels < pd.Timedelta(0))
            | (labels >= day)
            | (labels % hour != pd.Timedelta(0))
        ).any():
            raise ValueError("Interval labels must be whole hours from 00:00 to 23:00")
    if ((time_to - time_from) % day != hour).any():
        raise ValueError("Intervals must span exactly one hour")

    candidate = frame["DateUTC"].dt.normalize() + time_from
    mismatch = candidate != frame["DateUTC"]
    confirmed = (
        frame["DateUTC"].isin(CORRECTION_TIMESTAMPS)
        & (time_from == 2 * hour)
        & (time_to == 3 * hour)
    )
    if (mismatch & ~confirmed).any():
        raise ValueError("Unknown conflict between DateUTC and TimeFrom")
    frame["DateUTC_original"] = frame["DateUTC"]
    frame["timestamp_corrected"] = mismatch
    frame.loc[mismatch, "DateUTC"] = candidate[mismatch]
    return frame


def filter_time_window(
    panel: pd.DataFrame,
    start: datetime = START_DATETIME,
    end: datetime = END_DATETIME,
) -> pd.DataFrame:

    start, end = pd.Timestamp(start), pd.Timestamp(end)
    frame = panel.loc[panel["DateUTC"].between(start, end)]
    frame = frame.set_index("DateUTC").sort_index()
    return frame


def main() -> None:
    """Validate the complete cleaned panel before writing Gold."""
    silver = load_panel(type="silver")
    silver = normalize_dates(panel=silver)
    silver = validate_source_fields(panel=silver)
    silver = correct_known_timestamps(frame=silver)
    gold = filter_time_window(panel=silver)
    gold = gold.reset_index()[["DateUTC", "Value"]]
    save_panel(gold)


if __name__ == "__main__":
    main()
