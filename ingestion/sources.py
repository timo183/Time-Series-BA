"""Readers for the raw ENTSO-E "Monthly Hourly Load Values" exports."""

from dataclasses import dataclass
from pathlib import Path

import polars as pl

from config import COUNTRY_CODE

FLOAT_OVERRIDES = {
    "Cov_ratio": pl.Float64,
    "Value": pl.Float64,
    "Value_ScaleTo100": pl.Float64,
}

# All exports are day-first; 2021/2022 use slashes, the other years dashes.
DATETIME_FORMATS = ("%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M")
TIME_FORMATS = ("%H:%M", "%H:%M:%S")

PANEL_COLUMNS = ("DateUTC", "Value", "Cov_ratio", "TimeFrom", "TimeTo", "Source")


def _parse_datetime(column: str) -> pl.Expr:
    return pl.coalesce(
        pl.col(column).str.strptime(pl.Datetime("ms"), fmt, strict=False)
        for fmt in DATETIME_FORMATS
    ).dt.replace_time_zone("UTC")


def _parse_time(column: str) -> pl.Expr:
    return pl.coalesce(
        pl.col(column).str.strptime(pl.Time, fmt, strict=False) for fmt in TIME_FORMATS
    )


@dataclass(frozen=True)
class EntsoeCsvSource:
    """One yearly ENTSO-E CSV export, reduced to a single country.

    ``load`` returns the columns in ``PANEL_COLUMNS``. ``DateUTC`` is
    time-zone aware (UTC) and ``Source`` holds the file name for traceability.
    """

    path: Path
    country: str = COUNTRY_CODE

    def _read(self) -> pl.DataFrame:
        df = pl.read_csv(
            self.path,
            separator="\t",
            schema_overrides=FLOAT_OVERRIDES,
            infer_schema_length=0,
        )
        if "CountryCode" not in df.columns:  # 2021/2022 are ;-separated
            df = pl.read_csv(
                self.path,
                separator=";",
                schema_overrides=FLOAT_OVERRIDES,
                infer_schema_length=0,
            )
        if "CountryCode" not in df.columns:
            raise ValueError(f"{self.path.name}: unknown CSV layout")
        return df

    def load(self) -> pl.DataFrame:
        df = self._read().filter(pl.col("CountryCode") == self.country)
        df = df.select(
            _parse_datetime("DateUTC").alias("DateUTC"),
            pl.col("Value").cast(pl.Float64),
            pl.col("Cov_ratio").cast(pl.Float64),
            _parse_time("TimeFrom").alias("TimeFrom"),
            _parse_time("TimeTo").alias("TimeTo"),
            pl.lit(self.path.name).alias("Source"),
        )
        unparsed = df.filter(
            pl.any_horizontal(pl.col("DateUTC", "TimeFrom", "TimeTo").is_null())
        )
        if unparsed.height:
            raise ValueError(
                f"{self.path.name}: {unparsed.height} rows with unparseable "
                "DateUTC/TimeFrom/TimeTo"
            )
        return df
