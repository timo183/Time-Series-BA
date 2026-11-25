"""Validation and cleaning of the combined raw load panel."""

from collections.abc import Iterable
from datetime import UTC, datetime, timedelta

import polars as pl

from config import END_DATETIME, START_DATETIME

# Spring DST days on which the export labels the 02:00-03:00 interval with
# DateUTC 03:00. These timestamps are moved back to 02:00 (see DEC in docs).
CORRECTION_TIMESTAMPS: tuple[datetime, ...] = tuple(
    datetime(year, month, day, 3, tzinfo=UTC)
    for year, month, day in [
        (2019, 3, 31),
        (2020, 3, 29),
        (2021, 3, 28),
        (2022, 3, 27),
        (2023, 3, 26),
        (2024, 3, 31),
    ]
)

REQUIRED_COLUMNS = ("DateUTC", "Value", "Cov_ratio", "TimeFrom", "TimeTo")


class PanelCleaner:
    """Validate and clean a raw panel as produced by ``EntsoeCsvSource``.

    Steps: validate source fields, check coverage, correct known DST
    timestamps, restrict to the inclusive window ``[start, end]`` and verify a
    complete, duplicate-free hourly grid. ``DateUTC`` must be UTC-aware.
    """

    def __init__(
        self,
        start: datetime = START_DATETIME,
        end: datetime = END_DATETIME,
        correction_timestamps: Iterable[datetime] = CORRECTION_TIMESTAMPS,
    ) -> None:
        self.start = start
        self.end = end
        self.correction_timestamps = tuple(correction_timestamps)

    def clean(self, df: pl.DataFrame) -> pl.DataFrame:
        df = self._validate_source_fields(df)
        df = self._check_coverage(df)
        df = self._correct_known_timestamps(df)
        df = self._filter_window(df)
        self._validate_grid(df)
        return df

    @staticmethod
    def _validate_source_fields(df: pl.DataFrame) -> pl.DataFrame:
        missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        if df.select(pl.any_horizontal(pl.col(REQUIRED_COLUMNS).is_null())).to_series().any():
            raise ValueError("Missing timestamps, interval labels, or load values")
        if not df["Value"].is_finite().all():
            raise ValueError("Load values must be finite")
        if (df["DateUTC"] != df["DateUTC"].dt.truncate("1h")).any():
            raise ValueError("Timestamps must lie on hourly boundaries")
        return df

    @staticmethod
    def _check_coverage(df: pl.DataFrame) -> pl.DataFrame:
        """All 2019+ exports report Germany with full coverage (DEC-002)."""
        if (df["Cov_ratio"] != 100).any():
            raise ValueError("Cov_ratio must be 100; coverage harmonization is not implemented")
        return df

    def _correct_known_timestamps(self, df: pl.DataFrame) -> pl.DataFrame:
        for column in ("TimeFrom", "TimeTo"):
            labels = df[column]
            if ((labels.dt.minute() != 0) | (labels.dt.second() != 0)).any():
                raise ValueError("Interval labels must be whole hours from 00:00 to 23:00")

        hour_from = pl.col("TimeFrom").dt.hour().cast(pl.Int32)
        hour_to = pl.col("TimeTo").dt.hour().cast(pl.Int32)
        if not df.select(((hour_to - hour_from) % 24 == 1).all()).item():
            raise ValueError("Intervals must span exactly one hour")

        candidate = pl.col("DateUTC").dt.truncate("1d") + pl.duration(hours=hour_from)
        mismatch = candidate != pl.col("DateUTC")
        confirmed = (
            pl.col("DateUTC").is_in(
                pl.Series(self.correction_timestamps, dtype=pl.Datetime("us", "UTC"))
                .cast(df["DateUTC"].dtype)
                .implode()
            )
            & (hour_from == 2)
            & (hour_to == 3)
        )
        if df.select((mismatch & ~confirmed).any()).item():
            raise ValueError("Unknown conflict between DateUTC and TimeFrom")

        return df.with_columns(
            pl.col("DateUTC").alias("DateUTC_original"),
            mismatch.alias("timestamp_corrected"),
            candidate.alias("DateUTC"),
        )

    def _filter_window(self, df: pl.DataFrame) -> pl.DataFrame:
        return df.filter(pl.col("DateUTC").is_between(self.start, self.end)).sort("DateUTC")

    def _validate_grid(self, df: pl.DataFrame) -> None:
        if df["DateUTC"].is_duplicated().any():
            raise ValueError("Duplicate timestamps found")
        expected = int((self.end - self.start) / timedelta(hours=1)) + 1
        if df.height != expected:
            raise ValueError(
                f"Incomplete hourly grid: {df.height} of {expected} hours "
                f"between {self.start} and {self.end}"
            )
