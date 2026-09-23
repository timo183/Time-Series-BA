import pandas as pd
import pytest
from pandas import DataFrame, DatetimeIndex

from common.loader import load_panel
from config import (
    DATETIME_COLUMN,
    END_DATETIME,
    FREQUENCY,
    START_DATETIME,
)


@pytest.fixture(scope="module")
def panel() -> DataFrame:
    """Load the processed electricity-load panel once for this test module."""
    return load_panel()


@pytest.fixture(scope="module")
def timestamps(panel: DataFrame) -> DatetimeIndex:
    """Provide normalized timestamps for the time-series tests."""
    if DATETIME_COLUMN in panel.columns:
        values = panel[DATETIME_COLUMN]
    else:
        values = panel.index

    return DatetimeIndex(data=pd.to_datetime(values, errors="coerce", utc=True))


@pytest.fixture(scope="module")
def valid_timestamps(timestamps: DatetimeIndex) -> DatetimeIndex:
    return timestamps.dropna()


@pytest.fixture(scope="module")
def expected_timestamps() -> DatetimeIndex:
    return pd.date_range(
        start=START_DATETIME,
        end=END_DATETIME,
        freq=FREQUENCY,
    )


def test_datetime_field_exists(panel: DataFrame) -> None:
    has_datetime_column = DATETIME_COLUMN in panel.columns
    has_datetime_index = panel.index.name == DATETIME_COLUMN

    assert has_datetime_column or has_datetime_index


def test_all_timestamps_are_valid(timestamps: DatetimeIndex) -> None:
    invalid_count = int(timestamps.isna().sum())

    assert invalid_count == 0, f"{invalid_count} ungültige Zeitstempel gefunden"


def test_no_duplicate_timestamps(valid_timestamps: DatetimeIndex) -> None:
    duplicates = valid_timestamps[valid_timestamps.duplicated(keep=False)].unique()

    assert duplicates.empty, (
        f"Doppelte Zeitstempel gefunden (Summe: {duplicates.shape[0]}): {duplicates.tolist()}"
    )


def test_no_timestamps_before_start(
    valid_timestamps: DatetimeIndex,
) -> None:
    start = START_DATETIME
    timestamps_before_start = valid_timestamps[valid_timestamps < start]

    assert timestamps_before_start.empty, (
        f"Zeitstempel vor dem erwarteten Start gefunden (Summe: {timestamps_before_start.shape[0]}): "
        f"{timestamps_before_start.tolist()}"
    )


def test_no_timestamps_after_end(
    valid_timestamps: DatetimeIndex,
) -> None:
    end = END_DATETIME
    timestamps_after_end = valid_timestamps[valid_timestamps > end]

    assert timestamps_after_end.empty, (
        f"Zeitstempel nach dem erwarteten Ende gefunden (Summe: {timestamps_after_end.shape[0]}): "
        f"{timestamps_after_end.tolist()}"
    )


def test_no_hourly_timestamps_are_missing(
    valid_timestamps: DatetimeIndex,
    expected_timestamps: DatetimeIndex,
) -> None:
    missing_timestamps = expected_timestamps.difference(valid_timestamps)

    assert missing_timestamps.empty, (
        f"Fehlende Zeitstempel gefunden (Summe: {missing_timestamps.shape[0]}): {missing_timestamps.tolist()}"
    )


def test_no_exact_duplicate_rows(panel: DataFrame) -> None:
    duplicate_count = int(panel.duplicated().sum())

    assert duplicate_count == 0, (
        f"{duplicate_count} vollständig identische Zeilen gefunden"
    )


def test_no_missing_values(panel: DataFrame) -> None:
    missing_values = panel.isna().sum()
    affected_columns = missing_values[missing_values > 0].to_dict()

    assert not affected_columns, (
        f"Fehlende Werte gefunden (Summe: {sum(affected_columns.values())}): {affected_columns}"
    )
