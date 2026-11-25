from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent

DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final[Path] = DATA_DIR / "processed"
PANEL_CACHE_PATH: Final[Path] = PROCESSED_DATA_DIR / "panel.parquet"

CSV_FILES: Final[tuple[str, ...]] = tuple(
    f"monthly_hourly_load_values_{year}.csv" for year in range(2019, 2027)
)
COUNTRY_CODE: Final[str] = "DE"

DATETIME_COLUMN: Final[str] = "DateUTC"
FREQUENCY: Final[str] = "h"

# Split dates as DD-MM-YYYY, interpreted as 00:00 UTC. Every split is half-open
# [start, end); TEST_END is exclusive (last hour: 31-03-2026 23:00 UTC).
DATE_FORMAT: Final[str] = "%d-%m-%Y"
TRAIN_START: Final[str] = "01-01-2019"
VALIDATION_START: Final[str] = "01-01-2024"  # 13 weeks of validation
TEST_START: Final[str] = "01-01-2025"  # 52 weeks of test
TEST_END: Final[str] = "01-01-2026"


def parse_date(value: str) -> datetime:
    """Parse a ``DD-MM-YYYY`` string into a UTC-aware datetime at 00:00."""
    return datetime.strptime(value, DATE_FORMAT).replace(tzinfo=UTC)


Period = tuple[datetime, datetime]


@dataclass(frozen=True)
class DataSplit:
    """Train/validation/test boundaries as half-open ``[start, end)`` periods."""

    train_start: datetime
    validation_start: datetime
    test_start: datetime
    test_end: datetime

    def __post_init__(self) -> None:
        if not (
            self.train_start < self.validation_start < self.test_start < self.test_end
        ):
            raise ValueError(
                "Split dates must satisfy "
                "train_start < validation_start < test_start < test_end"
            )

    @classmethod
    def from_strings(
        cls, train_start: str, validation_start: str, test_start: str, test_end: str
    ) -> "DataSplit":
        return cls(
            parse_date(train_start),
            parse_date(validation_start),
            parse_date(test_start),
            parse_date(test_end),
        )

    @property
    def train(self) -> Period:
        return self.train_start, self.validation_start

    @property
    def validation(self) -> Period:
        return self.validation_start, self.test_start

    @property
    def test(self) -> Period:
        return self.test_start, self.test_end

    def periods(self) -> dict[str, Period]:
        return {"train": self.train, "validation": self.validation, "test": self.test}


DATA_SPLIT: Final[DataSplit] = DataSplit.from_strings(
    TRAIN_START, VALIDATION_START, TEST_START, TEST_END
)

# Inclusive bounds of the cleaned panel, aligned with the data split.
START_DATETIME: Final[datetime] = DATA_SPLIT.train_start
END_DATETIME: Final[datetime] = DATA_SPLIT.test_end - timedelta(hours=1)
