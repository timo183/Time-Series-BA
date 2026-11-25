"""Object-oriented entry point to the cleaned German load panel.

Usage (notebook or pipeline)::

    from ingestion import LoadPanel

    panel = LoadPanel()
    df = panel.to_pandas()        # DataFrame, UTC-aware DatetimeIndex
    y = panel.series()            # hourly pd.Series, naive UTC
    splits = panel.splits()       # {"train": ..., "validation": ..., "test": ...}
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd
import polars as pl

from config import (
    COUNTRY_CODE,
    CSV_FILES,
    DATA_SPLIT,
    END_DATETIME,
    FREQUENCY,
    PANEL_CACHE_PATH,
    RAW_DATA_DIR,
    START_DATETIME,
    DataSplit,
)
from ingestion.cleaning import CORRECTION_TIMESTAMPS, PanelCleaner
from ingestion.sources import EntsoeCsvSource

PANDAS_COLUMNS = ["Value", "Source", "timestamp_corrected"]


@dataclass(frozen=True)
class PanelConfig:
    """Where the raw exports live and which window the cleaned panel covers."""

    raw_dir: Path = RAW_DATA_DIR
    csv_files: tuple[str, ...] = CSV_FILES
    country: str = COUNTRY_CODE
    start: datetime = START_DATETIME
    end: datetime = END_DATETIME
    cache_path: Path | None = PANEL_CACHE_PATH
    correction_timestamps: tuple[datetime, ...] = field(
        default=CORRECTION_TIMESTAMPS
    )


class LoadPanel:
    """Build, cache and serve the cleaned hourly load panel.

    The panel is built from the raw CSVs on first use and written to
    ``config.cache_path`` as parquet; later instances read the cache. Pass
    ``refresh=True`` to :meth:`clean` to rebuild, or ``cache_path=None`` in the
    config to disable caching.
    """

    def __init__(self, config: PanelConfig | None = None) -> None:
        self.config = config or PanelConfig()
        self._raw: pl.DataFrame | None = None
        self._clean: pl.DataFrame | None = None

    @property
    def sources(self) -> list[EntsoeCsvSource]:
        return [
            EntsoeCsvSource(self.config.raw_dir / name, country=self.config.country)
            for name in self.config.csv_files
        ]

    @property
    def cleaner(self) -> PanelCleaner:
        return PanelCleaner(
            start=self.config.start,
            end=self.config.end,
            correction_timestamps=self.config.correction_timestamps,
        )

    def raw(self) -> pl.DataFrame:
        """All raw exports for the country stacked vertically, uncleaned."""
        if self._raw is None:
            self._raw = pl.concat(
                [source.load() for source in self.sources], how="vertical"
            )
        return self._raw

    def clean(self, refresh: bool = False) -> pl.DataFrame:
        """Validated, timestamp-corrected panel restricted to the window."""
        cache = self.config.cache_path
        if self._clean is not None and not refresh:
            return self._clean
        if cache is not None and cache.exists() and not refresh:
            self._clean = pl.read_parquet(cache)
        else:
            self._clean = self.cleaner.clean(self.raw())
            if cache is not None:
                cache.parent.mkdir(parents=True, exist_ok=True)
                self._clean.write_parquet(cache)
        return self._clean

    def build_cache(self) -> Path:
        """Rebuild the panel from the raw files and write the cache."""
        if self.config.cache_path is None:
            raise ValueError("No cache_path configured")
        self.clean(refresh=True)
        return self.config.cache_path

    def to_pandas(self) -> pd.DataFrame:
        """Cleaned panel as pandas with a UTC-aware ``DateUTC`` index."""
        df = self.clean().select("DateUTC", *PANDAS_COLUMNS).to_pandas()
        return df.set_index("DateUTC")

    def series(
        self,
        start: datetime | pd.Timestamp | None = None,
        end: datetime | pd.Timestamp | None = None,
    ) -> pd.Series:
        """Hourly ``Value`` series on a naive-UTC index for ``[start, end)``.

        ``start``/``end`` may be naive (interpreted as UTC) or tz-aware.
        Raises if the requested period is not fully covered.
        """
        y = self.to_pandas()["Value"]
        y.index = y.index.tz_convert(None)
        start_ts = _naive_utc(start) if start is not None else y.index[0]
        end_ts = (
            _naive_utc(end)
            if end is not None
            else y.index[-1] + pd.Timedelta(1, FREQUENCY)
        )

        y = y.loc[(y.index >= start_ts) & (y.index < end_ts)].asfreq(FREQUENCY)
        expected = pd.date_range(
            start_ts, end_ts, freq=FREQUENCY, inclusive="left", name="DateUTC"
        )
        if not y.index.equals(expected) or y.isna().any():
            raise ValueError(
                f"Panel does not fully cover [{start_ts}, {end_ts})"
            )
        return y

    def splits(self, split: DataSplit = DATA_SPLIT) -> dict[str, pd.Series]:
        """Train, validation and test series for the given split."""
        return {
            name: self.series(start, end)
            for name, (start, end) in split.periods().items()
        }


def _naive_utc(value: datetime | pd.Timestamp) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_convert("UTC").tz_localize(None) if ts.tzinfo else ts

