import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

from eda.utils import (
    _calendar_frame,
    fit_mstl,
    plot_acf_pacf,
    plot_hour_weekday_heatmap,
    plot_load_overview,
    plot_mstl,
    plot_seasonal_boxplots,
    stationarity_latex,
    stationarity_tests,
)


@pytest.fixture(scope="module")
def hourly_load() -> pd.Series:
    """Ten weeks of synthetic hourly load in MW with daily and weekly cycles."""
    index = pd.date_range("2023-02-27", periods=70 * 24, freq="h", name="DateUTC")
    t = np.arange(len(index))
    rng = np.random.default_rng(0)
    values = (
        55_000
        + 8_000 * np.sin(2 * np.pi * t / 24)
        + 4_000 * np.sin(2 * np.pi * t / 168)
        + rng.normal(0, 500, len(t))
    )
    return pd.Series(values, index=index, name="Value")


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_calendar_frame_uses_local_time():
    index = pd.DatetimeIndex(["2023-07-03 12:00", "2023-01-02 12:00"])
    frame = _calendar_frame(pd.Series([1000.0, 2000.0], index=index))

    assert frame["hour"].tolist() == [14, 13]  # CEST and CET
    assert frame["weekday"].tolist() == [0, 0]
    assert frame["month"].tolist() == [7, 1]
    assert frame["GW"].tolist() == [1.0, 2.0]


def test_calendar_frame_crosses_midnight_into_next_day():
    index = pd.DatetimeIndex(["2023-12-31 23:00"])  # Sunday 23:00 UTC
    frame = _calendar_frame(pd.Series([1.0], index=index))

    assert frame[["hour", "weekday", "month"]].iloc[0].tolist() == [0, 0, 1]


@pytest.mark.parametrize(
    "plot",
    [plot_hour_weekday_heatmap, plot_seasonal_boxplots, plot_load_overview],
)
def test_plots_return_figure_and_write_png(plot, hourly_load, tmp_path):
    path = tmp_path / "figure.png"
    fig = plot(hourly_load, save_path=path)

    assert isinstance(fig, Figure)
    assert path.stat().st_size > 0


def test_acf_pacf_writes_png(hourly_load, tmp_path):
    path = tmp_path / "acf.png"
    fig = plot_acf_pacf(hourly_load, lags=48, save_path=path)

    assert len(fig.axes) == 4
    assert path.stat().st_size > 0


def test_mstl_components_and_plots(hourly_load, tmp_path):
    result = fit_mstl(hourly_load, periods=(24, 168))
    assert list(result.seasonal.columns) == ["seasonal_24", "seasonal_168"]

    overview, profiles = plot_mstl(
        result,
        overview_path=tmp_path / "overview.png",
        profiles_path=tmp_path / "profiles.png",
    )

    assert len(overview.axes) == 4
    assert len(profiles.axes) == 1  # only the daily component is "shorter"
    assert len(profiles.axes[0].lines) == 1 + 1  # one full year + zero line
    assert (tmp_path / "overview.png").exists()
    assert (tmp_path / "profiles.png").exists()


def test_stationarity_tests_table(hourly_load):
    table = stationarity_tests(hourly_load)

    assert len(table) == 6
    assert table["Test"].tolist() == ["ADF", "KPSS"] * 3
    assert table["Reihe"].unique().tolist() == ["Originalreihe", "Δ1", "Δ168"]
    assert set(table["Entscheidung"]) <= {"H0 verworfen", "H0 beibehalten"}
    assert table["p-Wert"].between(0, 1).all()


def test_stationarity_latex_has_one_row_per_test(hourly_load):
    latex = stationarity_latex(stationarity_tests(hourly_load))

    assert latex.startswith(r"\begin{tabular}")
    assert latex.count(r"\\") == 7  # header + 6 rows
    assert r"$\Delta_{168}$" in latex
