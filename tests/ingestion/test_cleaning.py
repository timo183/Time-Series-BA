from datetime import UTC, datetime, time, timedelta

import polars as pl
import pytest

from ingestion.cleaning import PanelCleaner
from tests.ingestion.conftest import hourly_frame

START = datetime(2023, 3, 26, tzinfo=UTC)  # a listed spring DST day
HOURS = 24
END = START + timedelta(hours=HOURS - 1)


def cleaner(**kwargs) -> PanelCleaner:
    return PanelCleaner(start=kwargs.pop("start", START), end=kwargs.pop("end", END), **kwargs)


def with_dst_label_conflict(df: pl.DataFrame) -> pl.DataFrame:
    """Reproduce the export bug: interval 02:00-03:00 is labelled DateUTC 03:00.

    The genuine 03:00 row is dropped so the corrected grid is complete again.
    """
    two, three = START + timedelta(hours=2), START + timedelta(hours=3)
    df = df.filter(pl.col("DateUTC") != three)
    return df.with_columns(
        pl.when(pl.col("DateUTC") == two)
        .then(pl.lit(three, dtype=pl.Datetime("ms", "UTC")))
        .otherwise(pl.col("DateUTC"))
        .alias("DateUTC")
    ).vstack(hourly_frame(three, 1))


def test_clean_panel_passes_and_adds_flags():
    out = cleaner().clean(hourly_frame(START, HOURS))

    assert out.height == HOURS
    assert not out["timestamp_corrected"].any()
    assert out["DateUTC"].equals(out["DateUTC_original"])


@pytest.mark.parametrize(
    ("df", "message"),
    [
        (hourly_frame(START, HOURS).drop("TimeTo"), "Missing columns"),
        (
            hourly_frame(START, HOURS).with_columns(
                pl.when(pl.int_range(pl.len()) == 3).then(None).otherwise(pl.col("Value")).alias("Value")
            ),
            "Missing timestamps",
        ),
        (
            hourly_frame(START, HOURS).with_columns(
                pl.when(pl.int_range(pl.len()) == 3)
                .then(float("inf"))
                .otherwise(pl.col("Value"))
                .alias("Value")
            ),
            "finite",
        ),
        (
            hourly_frame(START, HOURS).with_columns(
                pl.col("DateUTC") + pl.duration(minutes=15)
            ),
            "hourly boundaries",
        ),
        (hourly_frame(START, HOURS, Cov_ratio=pl.lit(98.0)), "Cov_ratio"),
        (
            hourly_frame(START, HOURS, TimeTo=pl.col("TimeFrom")),
            "exactly one hour",
        ),
        (
            hourly_frame(START, HOURS, TimeFrom=pl.lit(time(0, 30))),
            "whole hours",
        ),
    ],
)
def test_invalid_input_raises(df, message):
    with pytest.raises(ValueError, match=message):
        cleaner().clean(df)


def test_known_dst_timestamp_is_corrected():
    out = cleaner().clean(with_dst_label_conflict(hourly_frame(START, HOURS)))

    corrected = out.filter(pl.col("timestamp_corrected"))
    assert corrected["DateUTC"].to_list() == [START + timedelta(hours=2)]
    assert corrected["DateUTC_original"].to_list() == [START + timedelta(hours=3)]
    assert out.height == HOURS


def test_unknown_timestamp_conflict_raises():
    df = with_dst_label_conflict(hourly_frame(START, HOURS))

    with pytest.raises(ValueError, match="Unknown conflict"):
        cleaner(correction_timestamps=()).clean(df)


def test_midnight_interval_is_valid():
    out = cleaner().clean(hourly_frame(START, HOURS))

    last = out.row(-1, named=True)
    assert (last["TimeFrom"], last["TimeTo"]) == (time(23), time(0))


def test_window_bounds_are_inclusive_and_sorted():
    df = hourly_frame(START - timedelta(hours=2), HOURS + 4).reverse()

    out = cleaner().clean(df)

    assert out["DateUTC"].to_list()[0] == START
    assert out["DateUTC"].to_list()[-1] == END
    assert out["DateUTC"].is_sorted()


def test_duplicate_timestamp_raises():
    df = hourly_frame(START, HOURS)

    with pytest.raises(ValueError, match="Duplicate"):
        cleaner().clean(df.vstack(df.head(1)))


def test_gap_raises():
    df = hourly_frame(START, HOURS).filter(pl.col("DateUTC") != START + timedelta(hours=5))

    with pytest.raises(ValueError, match="Incomplete hourly grid"):
        cleaner().clean(df)
