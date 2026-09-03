from datetime import datetime

import pandas as pd
from pandas import DataFrame


def check_missing_values(df: DataFrame):
    missing_stats = pd.DataFrame(
        {
            "total_missing": df.isnull().sum(),
            "percent_missing": (df.isnull().sum() / len(df) * 100).round(2),
        }
    ).sort_values("percent_missing", ascending=False)

    missing_stats["impact"] = missing_stats["percent_missing"].apply(
        lambda x: "High" if x > 15 else ("Medium" if x > 5 else "Low")
    )
    return missing_stats


def check_data_consistency(df, date_columns, numeric_columns):
    consistency_issues = []
    # Date validation
    for col in date_columns:
        future_dates = df[df[col] > datetime.now()][col].count()
        if future_dates > 0:
            consistency_issues.append(
                f"WARNING: {future_dates} future dates found in {col}"
            )
    return consistency_issues


def check_duplicates(df, subset_columns=None):
    duplicate_report = {
        "exact_duplicates": df.duplicated().sum(),
        "partial_duplicates": df.duplicated(subset=subset_columns).sum()
        if subset_columns
        else 0,
    }
    return duplicate_report


def check_time_series_completeness(
    df: DataFrame,
    start="31-12-2024 23:00",
    end="31-03-2026 23:00",
    datetime_column="DateUTC",
    frequency="h",
):
    """Check whether a time series contains every expected timestamp exactly once.

    ``start`` and ``end`` are inclusive. The timestamps can either be in
    ``datetime_column`` or in a DatetimeIndex with that name. Rows outside the
    requested interval are reported but do not make that interval incomplete.
    """
    if datetime_column in df.columns:
        raw_timestamps = df[datetime_column]
    elif df.index.name == datetime_column or isinstance(df.index, pd.DatetimeIndex):
        raw_timestamps = df.index
    else:
        raise KeyError(
            f"'{datetime_column}' was not found as a column or datetime index."
        )

    # UTC is used so timezone-aware and timezone-naive DateUTC values can be
    # compared. The timezone is then removed from both sides of the comparison.
    timestamps = pd.DatetimeIndex(
        pd.to_datetime(raw_timestamps, errors="coerce", dayfirst=True, utc=True)
    ).tz_localize(None)
    valid_timestamps = timestamps[~timestamps.isna()]

    start_timestamp = pd.to_datetime(start, dayfirst=True, utc=True).tz_localize(None)
    end_timestamp = pd.to_datetime(end, dayfirst=True, utc=True).tz_localize(None)
    if start_timestamp > end_timestamp:
        raise ValueError("start must be before or equal to end")

    expected_timestamps = pd.date_range(
        start=start_timestamp,
        end=end_timestamp,
        freq=frequency,
    )
    observed_in_range = valid_timestamps[
        (valid_timestamps >= start_timestamp) & (valid_timestamps <= end_timestamp)
    ]

    missing_timestamps = expected_timestamps.difference(observed_in_range)
    duplicate_timestamps = observed_in_range[
        observed_in_range.duplicated(keep=False)
    ].unique().sort_values()
    unexpected_timestamps = valid_timestamps[
        (valid_timestamps < start_timestamp) | (valid_timestamps > end_timestamp)
    ].unique().sort_values()
    invalid_timestamp_count = int(timestamps.isna().sum())

    return {
        "is_complete": (
            len(missing_timestamps) == 0
            and len(duplicate_timestamps) == 0
            and invalid_timestamp_count == 0
        ),
        "expected_timestamp_count": len(expected_timestamps),
        "observed_row_count": len(timestamps),
        "observed_in_range_count": len(observed_in_range),
        "missing_timestamps": missing_timestamps,
        "duplicate_timestamps": duplicate_timestamps,
        "unexpected_timestamps": unexpected_timestamps,
        "invalid_timestamp_count": invalid_timestamp_count,
    }
