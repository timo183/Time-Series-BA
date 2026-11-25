from datetime import UTC, datetime, timedelta

import pytest

from config import DATA_SPLIT, END_DATETIME, START_DATETIME, DataSplit, parse_date

HORIZON = timedelta(hours=168)


def test_parse_date_is_day_first_utc_midnight():
    assert parse_date("01-01-2019") == datetime(2019, 1, 1, tzinfo=UTC)
    assert parse_date("02-04-2025") == datetime(2025, 4, 2, tzinfo=UTC)


def test_out_of_order_split_raises():
    with pytest.raises(ValueError, match="must satisfy"):
        DataSplit.from_strings("01-01-2019", "02-04-2025", "01-01-2025", "01-04-2026")


def test_evaluation_periods_are_whole_horizons():
    for start, end in (DATA_SPLIT.validation, DATA_SPLIT.test):
        assert (end - start) % HORIZON == timedelta(0)
    assert (DATA_SPLIT.validation[1] - DATA_SPLIT.validation[0]) == 13 * HORIZON
    assert (DATA_SPLIT.test[1] - DATA_SPLIT.test[0]) == 52 * HORIZON


def test_panel_window_matches_split():
    assert START_DATETIME == DATA_SPLIT.train_start
    assert END_DATETIME == DATA_SPLIT.test_end - timedelta(hours=1)
