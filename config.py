from datetime import UTC, datetime
from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent

DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final[Path] = DATA_DIR / "processed"
PANEL_PATH: Final[Path] = PROCESSED_DATA_DIR / "panel.csv"


START_DATETIME: Final[datetime] = datetime(2015, 1, 1, 1, 0, tzinfo=UTC)
END_DATETIME: Final[datetime] = datetime(2026, 3, 31, 23, 0, tzinfo=UTC)

DATETIME_COLUMN: Final[str] = "DateUTC"
FREQUENCY: Final[str] = "h"
