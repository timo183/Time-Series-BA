from datetime import UTC, datetime, timedelta

import pandas as pd
import pytest

from config import DataSplit
from ingestion import LoadPanel, PanelConfig
from tests.ingestion.conftest import write_export

START = datetime(2023, 1, 1, tzinfo=UTC)
DAYS = 4
END = START + timedelta(days=DAYS, hours=-1)


@pytest.fixture
def config(tmp_path) -> PanelConfig:
    raw = tmp_path / "raw"
    raw.mkdir()
    # Two files with different layouts, split at day 2.
    write_export(raw / "a.csv", START, hours=48)
    write_export(
        raw / "b.csv",
        START + timedelta(days=2),
        hours=48,
        separator=";",
        date_sep="/",
        time_seconds=True,
    )
    return PanelConfig(
        raw_dir=raw,
        csv_files=("a.csv", "b.csv"),
        start=START,
        end=END,
        cache_path=tmp_path / "processed" / "panel.parquet",
    )


def test_clean_writes_cache_and_reuses_it(config):
    first = LoadPanel(config).clean()
    assert config.cache_path.exists()
    assert first.height == DAYS * 24
    assert set(first["Source"]) == {"a.csv", "b.csv"}

    for path in config.raw_dir.iterdir():
        path.unlink()

    cached = LoadPanel(config).clean()
    assert cached.equals(first)
    with pytest.raises(FileNotFoundError):
        LoadPanel(config).clean(refresh=True)


def test_cache_can_be_disabled(config, tmp_path):
    config = PanelConfig(**{**config.__dict__, "cache_path": None})

    LoadPanel(config).clean()

    assert not (tmp_path / "processed").exists()


def test_to_pandas_has_utc_index(config):
    df = LoadPanel(config).to_pandas()

    assert df.index.name == "DateUTC"
    assert str(df.index.tz) == "UTC"
    assert list(df.columns) == ["Value", "Source", "timestamp_corrected"]


def test_series_is_naive_hourly_and_half_open(config):
    panel = LoadPanel(config)

    y = panel.series(pd.Timestamp("2023-01-02"), datetime(2023, 1, 3, tzinfo=UTC))

    assert y.index.tz is None
    assert y.index.freqstr == "h"
    assert len(y) == 24
    assert y.index[0] == pd.Timestamp("2023-01-02 00:00")
    assert y.index[-1] == pd.Timestamp("2023-01-02 23:00")
    assert len(panel.series()) == DAYS * 24


def test_series_outside_panel_raises(config):
    with pytest.raises(ValueError, match="does not fully cover"):
        LoadPanel(config).series(end=pd.Timestamp("2023-01-10"))


def test_splits_return_named_series(config):
    split = DataSplit(
        START,
        START + timedelta(days=2),
        START + timedelta(days=3),
        START + timedelta(days=4),
    )

    splits = LoadPanel(config).splits(split)

    assert {name: len(y) for name, y in splits.items()} == {
        "train": 48,
        "validation": 24,
        "test": 24,
    }
