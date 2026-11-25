from datetime import UTC, datetime, timedelta
from pathlib import Path

import polars as pl
import pytest

HEADER = [
    "MeasureItem",
    "DateUTC",
    "DateShort",
    "TimeFrom",
    "TimeTo",
    "CountryCode",
    "Cov_ratio",
    "Value",
    "Value_ScaleTo100",
]


def write_export(
    path: Path,
    start: datetime,
    hours: int,
    separator: str = "\t",
    date_sep: str = "-",
    time_seconds: bool = False,
    countries: tuple[str, ...] = ("DE", "AT"),
) -> Path:
    """Write a tiny ENTSO-E style export to ``path``."""
    time_fmt = "%H:%M:%S" if time_seconds else "%H:%M"
    day_fmt = f"%d{date_sep}%m{date_sep}%Y"
    lines = [separator.join(HEADER)]
    for i in range(hours):
        ts = start + timedelta(hours=i)
        for country in countries:
            value = 1000.0 + i if country == "DE" else 1.0
            lines.append(
                separator.join(
                    [
                        "Monthly Hourly Load Values",
                        ts.strftime(f"{day_fmt} %H:%M"),
                        ts.strftime(day_fmt),
                        ts.strftime(time_fmt),
                        (ts + timedelta(hours=1)).strftime(time_fmt),
                        country,
                        "100",
                        f"{value:.1f}",
                        f"{value:.1f}",
                    ]
                )
            )
    path.write_text("\n".join(lines) + "\n")
    return path


def hourly_frame(start: datetime, hours: int, **overrides) -> pl.DataFrame:
    """In-memory panel in the ``EntsoeCsvSource`` output schema."""
    stamps = [start + timedelta(hours=i) for i in range(hours)]
    df = pl.DataFrame(
        {
            "DateUTC": stamps,
            "Value": [1000.0 + i for i in range(hours)],
            "Cov_ratio": [100.0] * hours,
            "TimeFrom": [ts.time() for ts in stamps],
            "TimeTo": [(ts + timedelta(hours=1)).time() for ts in stamps],
            "Source": ["test.csv"] * hours,
        },
        schema_overrides={"DateUTC": pl.Datetime("ms", "UTC")},
    )
    return df.with_columns(**overrides) if overrides else df


@pytest.fixture
def start() -> datetime:
    return datetime(2023, 1, 1, tzinfo=UTC)
