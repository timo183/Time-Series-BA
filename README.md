# Electricity load preprocessing

Run from the repository root:

```sh
uv run python -m ingestion   # rebuild data/processed/panel.parquet from data/raw/
uv run pytest
```

In a notebook or pipeline:

```python
from ingestion import LoadPanel

panel = LoadPanel()
df = panel.to_pandas()   # cleaned panel, UTC-aware DateUTC index
y = panel.series()       # hourly Value series, naive UTC, gap-free
splits = panel.splits()  # {"train", "validation", "test"} from config.py
```

`LoadPanel` reads the eight yearly ENTSO-E CSV exports (2019–2026) for Germany,
cleans them with `PanelCleaner` and caches the result as parquet. Later calls
read the cache; use `panel.clean(refresh=True)` after changing raw data or
cleaning rules.

`DateUTC` is parsed day-first (`DD-MM-YYYY` / `DD/MM/YYYY`) and interpreted as
the UTC interval start, following the export column name. This remains a source
assumption; the historical CET/CEST documentation alone does not establish the
CSV export's time zone. Timestamps are never rounded.

The six identified spring-transition conflicts in 2019–2024 are corrected from
03:00 to 02:00 only for intervals labelled 02:00–03:00. `DateUTC_original` and
`timestamp_corrected` preserve the audit trail. No load values are interpolated
or averaged. Unknown conflicts, invalid values, coverage other than 100 %,
duplicate timestamps and missing hours stop the run.

The panel window (`START_DATETIME`–`END_DATETIME`, inclusive) follows the split
dates in `config.py` (`TRAIN_START`, `VALIDATION_START`, `TEST_START`,
`TEST_END`, all `DD-MM-YYYY` at 00:00 UTC, each period half-open).

Tests under `tests/` use in-memory fixtures and do not need the local datasets.
