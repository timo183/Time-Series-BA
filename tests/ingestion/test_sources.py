from datetime import UTC, datetime, time

import polars as pl
import pytest

from ingestion.sources import PANEL_COLUMNS, EntsoeCsvSource
from tests.ingestion.conftest import write_export


def test_tab_separated_export_keeps_country_and_schema(tmp_path, start):
    path = write_export(tmp_path / "2023.csv", start, hours=3)

    df = EntsoeCsvSource(path).load()

    assert tuple(df.columns) == PANEL_COLUMNS
    assert df.height == 3
    assert df["DateUTC"].dtype == pl.Datetime("ms", "UTC")
    assert df["DateUTC"][0] == start
    assert df["Value"].to_list() == [1000.0, 1001.0, 1002.0]
    assert df["TimeFrom"][1] == time(1)
    assert df["Source"].unique().to_list() == ["2023.csv"]


def test_semicolon_export_with_slashes_and_seconds_is_day_first(tmp_path):
    start = datetime(2021, 8, 10, tzinfo=UTC)
    path = write_export(
        tmp_path / "2021.csv",
        start,
        hours=2,
        separator=";",
        date_sep="/",
        time_seconds=True,
    )

    df = EntsoeCsvSource(path).load()

    # "10/08/2021" must be 10 August, not 8 October.
    assert df["DateUTC"].to_list() == [start, datetime(2021, 8, 10, 1, tzinfo=UTC)]
    assert df["TimeTo"].to_list() == [time(1), time(2)]


def test_other_country_can_be_selected(tmp_path, start):
    path = write_export(tmp_path / "2023.csv", start, hours=2)

    df = EntsoeCsvSource(path, country="AT").load()

    assert df["Value"].to_list() == [1.0, 1.0]


def test_unparseable_timestamp_raises(tmp_path, start):
    path = write_export(tmp_path / "2023.csv", start, hours=1, countries=("DE",))
    path.write_text(path.read_text().replace("01-01-2023 00:00", "2023/01/01 0h"))

    with pytest.raises(ValueError, match="unparseable"):
        EntsoeCsvSource(path).load()


def test_unknown_layout_raises(tmp_path):
    path = tmp_path / "broken.csv"
    path.write_text("a,b\n1,2\n")

    with pytest.raises(ValueError, match="unknown CSV layout"):
        EntsoeCsvSource(path).load()
