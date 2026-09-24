from datetime import datetime

import numpy as np
import pandas as pd

from common.loader import load_panel
from common.writer import save_panel
from config import END_DATETIME, FREQUENCY, START_DATETIME

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


def normalize_panel(panel: pd.DataFrame) -> pd.DataFrame:
    """Validate source fields and normalize DateUTC as a UTC column.

    Naive timestamps are assumed to represent UTC; aware timestamps are
    converted to UTC. The input panel is not modified.
    """
    frame = panel.copy()

    if "DateUTC" not in frame.columns:
        frame = frame.reset_index()
    required = {"DateUTC", "Value", "TimeFrom", "TimeTo"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(frame.columns))}")
    frame["DateUTC"] = pd.to_datetime(frame["DateUTC"], utc=True, errors="raise")
    if frame[list(required)].isna().any().any():
        raise ValueError("Missing timestamps, interval labels, or load values")
    frame["Value"] = pd.to_numeric(frame["Value"], errors="raise")
    if not np.isfinite(frame["Value"]).all():
        raise ValueError("Load values must be finite")
    if (frame["DateUTC"] != frame["DateUTC"].dt.floor("h")).any():
        raise ValueError("Timestamps must lie on hourly boundaries")

    return frame


def correct_known_timestamps(frame: pd.DataFrame) -> pd.DataFrame:
    """Repair the six known interval conflicts and retain an audit trail."""
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


def validate_gold(frame: pd.DataFrame, start: datetime, end: datetime) -> None:
    """Require valid measurements and a unique, complete hourly UTC index."""
    if frame.index.hasnans or frame.isna().any().any():
        raise ValueError("Missing timestamps, interval labels, or load values")
    if not np.isfinite(frame["Value"]).all():
        raise ValueError("Load values must be finite")
    if frame.index.has_duplicates:
        raise ValueError("Unresolved duplicate timestamps")
    expected = pd.date_range(start, end, freq=FREQUENCY, name="DateUTC")
    missing = expected.difference(frame.index)
    if not missing.empty:
        raise ValueError(
            f"Missing {len(missing)} hourly timestamps: {missing[:6].tolist()}"
        )
    if not frame.index.equals(expected):
        raise ValueError("Gold timestamps must match the ordered hourly UTC index")


def clean_panel(
    panel: pd.DataFrame,
    start: datetime = START_DATETIME,
    end: datetime = END_DATETIME,
) -> pd.DataFrame:
    """Normalize, deduplicate, repair, clip, and validate Silver for Gold."""
    frame = normalize_panel(panel)
    frame = frame.drop_duplicates().reset_index(drop=True)
    frame = correct_known_timestamps(frame)

    start, end = pd.Timestamp(start), pd.Timestamp(end)
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("Period bounds must be timezone-aware")
    start, end = start.tz_convert("UTC"), end.tz_convert("UTC")
    if start > end or start != start.floor("h") or end != end.floor("h"):
        raise ValueError("Period bounds must be ordered whole hours")
    frame = frame.loc[frame["DateUTC"].between(start, end)]
    frame = frame.set_index("DateUTC").sort_index()
    validate_gold(frame, start, end)
    return frame


def main() -> None:
    """Validate the complete cleaned panel before writing Gold."""
    silver = load_panel(type="silver")
    gold = clean_panel(silver)
    gold = gold.reset_index()[["DateUTC", "Value"]].rename(
        columns={"DateUTC": "timestamp", "Value": "load"}
    )
    save_panel(gold)


if __name__ == "__main__":
    main()
