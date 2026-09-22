# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Python 3.12 time-series analysis project for German electricity-load data.

- `ingestion/` reads raw CSV/XLSX inputs and creates `data/processed/panel.csv`.
- `common/` contains reusable data-loading helpers.
- `eda/` holds exploratory notebooks and plotting/statistical utilities.
- `quality_check/` contains data-validation functions and their current pytest test module.
- `modeling/` is reserved for forecasting or statistical model code.
- `main.py` is the lightweight application entry point.
- `pyproject.toml` and `uv.lock` define the environment; `data/` is intentionally Git-ignored.

Keep reusable logic in Python modules rather than notebooks. Do not commit generated datasets, caches, or virtual environments.

## Build, Test, and Development Commands

- `uv sync` installs the locked runtime and development dependencies.
- `uv run python main.py` runs the current entry point.
- `uv run python ingestion/load_raw.py` builds the processed panel from files in `data/raw/`.
- `uv run pytest quality_check/test_panel.py` runs the existing automated test directly.
- `uv run pytest` runs configured discovery after tests are placed under the `tests/` directory specified in `pyproject.toml`.

Run commands from the repository root so relative data paths resolve correctly.

## Coding Style & Naming Conventions

Follow PEP 8 with four-space indentation. Use `snake_case` for modules, functions, and variables; `UPPER_CASE` for constants; and descriptive names for DataFrames and time-series fields. Preserve the source schema names `DateUTC` and `Value` where they cross module boundaries. Add type hints to new public functions and concise docstrings where behavior, accepted data shape, or time-zone handling is not obvious. No formatter or linter is currently configured, so keep imports grouped and code consistent with the existing modules.

## Testing Guidelines

Use pytest and name files `test_*.py` and test functions `test_*`. Prefer small in-memory pandas or Polars fixtures; tests should not depend on ignored local datasets. Cover edge cases such as missing timestamps, duplicates, invalid dates, interval boundaries, and time-zone-aware input. There is no formal coverage threshold, but new transformations should include focused regression tests.

## Commit & Pull Request Guidelines

Recent commits use short, lowercase, action-oriented subjects such as `added data quality checks` and `fixed loading`. Keep each commit focused and avoid committing notebook output or data artifacts. Pull requests should explain the change, identify affected data assumptions, list commands run, and link any related issue. Include plots or notebook screenshots when analytical output changes.
