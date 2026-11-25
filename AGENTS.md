# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Python 3.12 time-series analysis project for German electricity-load data.

- `ingestion/` builds the cleaned load panel: `sources.py` reads the raw ENTSO-E CSVs, `cleaning.py` (`PanelCleaner`) validates and corrects them, and `panel.py` (`LoadPanel`) is the entry point for notebooks and pipelines (`to_pandas()`, `series()`, `splits()`). The cleaned panel is cached in `data/processed/panel.parquet`.
- `config.py` holds paths, the panel window and the train/validation/test split dates (`DD-MM-YYYY`).
- `common/` contains shared helpers such as logging configuration.
- `eda/` holds exploratory notebooks and plotting/statistical utilities.
- `modeling/` contains the forecasting models; `run_benchmark.py` and `run_forecasting.py` evaluate them.
- `main.py` is the lightweight application entry point.
- `pyproject.toml` and `uv.lock` define the environment; `data/` is intentionally Git-ignored.

Keep reusable logic in Python modules rather than notebooks. Do not commit generated datasets, caches, or virtual environments.

## Build, Test, and Development Commands

- `uv sync` installs the locked runtime and development dependencies.
- `uv run python main.py` runs the current entry point.
- `uv run python -m ingestion` rebuilds the panel cache from the files in `data/raw/`.
- `uv run pytest` runs all tests under `tests/`.

Run commands from the repository root so relative data paths resolve correctly.

## Coding Style & Naming Conventions

Follow PEP 8 with four-space indentation. Use `snake_case` for modules, functions, and variables; `UPPER_CASE` for constants; and descriptive names for DataFrames and time-series fields. Preserve the source schema names `DateUTC` and `Value` where they cross module boundaries. Add type hints to new public functions and concise docstrings where behavior, accepted data shape, or time-zone handling is not obvious. No formatter or linter is currently configured, so keep imports grouped and code consistent with the existing modules.

## Testing Guidelines

Use pytest and name files `test_*.py` and test functions `test_*`. Prefer small in-memory pandas or Polars fixtures; tests should not depend on ignored local datasets. Cover edge cases such as missing timestamps, duplicates, invalid dates, interval boundaries, and time-zone-aware input. There is no formal coverage threshold, but new transformations should include focused regression tests.

## Commit & Pull Request Guidelines

Recent commits use short, lowercase, action-oriented subjects such as `added data quality checks` and `fixed loading`. Keep each commit focused and avoid committing notebook output or data artifacts. Pull requests should explain the change, identify affected data assumptions, list commands run, and link any related issue. Include plots or notebook screenshots when analytical output changes.
