# Electricity load preprocessing

Run from the repository root:

```sh
uv run python -m preprocessing.data_cleaning
uv run pytest
```

The cleaning pipeline reads `data/silver/panel.csv` and writes
`data/gold/panel.csv` only after validation succeeds. Existing Gold is replaced.
Naive `DateUTC` timestamps are interpreted as UTC interval starts, following
the export column name. This remains a source assumption; the historical
CET/CEST documentation alone does not establish the CSV export's time zone.
Timezone-aware timestamps are converted to UTC. Timestamps are never rounded.

Exact duplicates include the timestamp. The six identified spring-transition
conflicts in 2019–2024 are corrected from 03:00 to 02:00 only for intervals
labelled 02:00–03:00. `DateUTC_original` and `timestamp_corrected` preserve the
audit trail. No load values are interpolated or averaged. Unknown conflicts,
invalid values, remaining duplicate timestamps, and missing hours stop the run.

The configured start and end in `config.py` are inclusive. Cleaning sorts and
clips to this period. Gold retains `TimeFrom` and `TimeTo`; audit and interval
columns should not automatically be treated as ML features.

`tests/test_data_cleaning.py` uses in-memory fixtures. Silver/Gold integration
tests require the local datasets; generate Gold before running the full suite.
