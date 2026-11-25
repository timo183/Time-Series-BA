"""Plotting and test helpers for the exploratory analysis of the load series.

All functions take the hourly ``Value`` series in MW on a naive-UTC index (as
returned by ``LoadPanel.series()`` / ``LoadPanel.splits()``), plot in GW with
German labels and return the matplotlib ``Figure``. Pass ``save_path`` (``.png``)
to write the figure for the thesis.
"""

import warnings
from pathlib import Path

import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.seasonal import MSTL, DecomposeResult
from statsmodels.tsa.stattools import adfuller, kpss

LOCAL_TZ = "Europe/Berlin"
FIG_WIDTH = 6.3  # inches, text width of the thesis
DPI = 300

THESIS_STYLE = {
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#d9d9d9",
    "grid.linewidth": 0.5,
    "axes.axisbelow": True,
}
LINE_COLOR = "#1f3a5f"
LIGHT_COLOR = "#b4bcc6"

WEEKDAY_LABELS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
MONTH_LABELS = [
    "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
    "Jul", "Aug", "Sep", "Okt", "Nov", "Dez",
]
SPLIT_COLORS = {"train": "#ffffff", "validation": "#eeeeee", "test": "#dcdcdc"}
SPLIT_LABELS = {"train": "Training", "validation": "Validierung", "test": "Test"}


def _save(fig: Figure, save_path: "str | Path | None") -> None:
    if save_path is not None:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=DPI, bbox_inches="tight")


def _calendar_frame(y: pd.Series) -> pd.DataFrame:
    """Load in GW with hour, weekday (0 = Monday) and month in German local time.

    Calendar profiles use local time because consumption follows the clock on
    the wall: in UTC the daily peaks would shift by one hour during summer time.
    """
    local_index = y.index.tz_localize("UTC").tz_convert(LOCAL_TZ)
    return pd.DataFrame(
        {
            "GW": y.to_numpy() / 1000,
            "hour": local_index.hour,
            "weekday": local_index.dayofweek,
            "month": local_index.month,
        },
        index=y.index,
    )


def plot_load_overview(
    y: pd.Series,
    split: "DataSplit | None" = None,
    zoom_start: str = "2023-03-06",
    zoom_days: int = 14,
    save_path: "str | Path | None" = None,
) -> Figure:
    """Two-panel overview of the hourly load series.

    (a) Whole period as daily mean (light) with a 28-day rolling mean (dark);
        if ``split`` is given, the train/validation/test periods are shaded.
    (b) Hourly values for ``zoom_days`` days from ``zoom_start`` (UTC) to show
        the daily and weekly cycle that is hidden in (a).
    """
    gw = y / 1000
    daily = gw.resample("D").mean()
    rolling = daily.rolling(28, center=True, min_periods=14).mean()

    zoom_start_ts = pd.Timestamp(zoom_start)
    zoom = gw.loc[zoom_start_ts : zoom_start_ts + pd.Timedelta(days=zoom_days)]

    with mpl.rc_context(THESIS_STYLE):
        fig, (ax_full, ax_zoom) = plt.subplots(
            2, 1, figsize=(FIG_WIDTH, 5.2), gridspec_kw={"height_ratios": [3, 2]}
        )

        if split is not None:
            for name, (start, end) in split.periods().items():
                start = pd.Timestamp(start).tz_localize(None)
                end = pd.Timestamp(end).tz_localize(None)
                ax_full.axvspan(start, end, color=SPLIT_COLORS[name], zorder=0, lw=0)
                ax_full.text(
                    start + (end - start) / 2, 1.01, SPLIT_LABELS[name],
                    transform=ax_full.get_xaxis_transform(),
                    ha="center", va="bottom", fontsize=8,
                )
                ax_full.axvline(start, color="#808080", lw=0.6, ls="--", zorder=1)

        ax_full.plot(daily.index, daily, color=LIGHT_COLOR, lw=0.5,
                     label="Tagesmittel")
        ax_full.plot(rolling.index, rolling, color=LINE_COLOR, lw=1.4,
                     label="Gleitender 28-Tage-Mittelwert")
        ax_full.set_ylabel("Last [GW]")
        x_end = daily.index[-1]
        if split is not None:
            x_end = min(x_end, pd.Timestamp(split.test_end).tz_localize(None))
        ax_full.set_xlim(daily.index[0], x_end)
        ax_full.xaxis.set_major_locator(mdates.YearLocator())
        ax_full.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax_full.legend(loc="lower left", frameon=True, framealpha=0.9,
                       edgecolor="none")
        ax_full.set_title("(a) Gesamtzeitraum", loc="left",
                          pad=14 if split is not None else 6)

        ax_zoom.plot(zoom.index, zoom, color=LINE_COLOR, lw=0.9)
        ax_zoom.set_ylabel("Last [GW]")
        ax_zoom.set_xlim(zoom.index[0], zoom.index[-1])
        ax_zoom.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax_zoom.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m."))
        ax_zoom.xaxis.set_minor_locator(mdates.DayLocator())
        end_label = zoom.index[-1].strftime("%d.%m.%Y")
        ax_zoom.set_title(
            f"(b) Stündliche Werte, {zoom.index[0]:%d.%m.}–{end_label}",
            loc="left",
        )
        ax_zoom.set_xlabel("Zeit (UTC)")

        fig.tight_layout()
        _save(fig, save_path)
    return fig


def plot_hour_weekday_heatmap(
    y: pd.Series, save_path: "str | Path | None" = None
) -> Figure:
    """Mean load per local hour of day (rows) and weekday (columns)."""
    frame = _calendar_frame(y)
    table = frame.pivot_table(index="hour", columns="weekday", values="GW",
                              aggfunc="mean")

    with mpl.rc_context({**THESIS_STYLE, "axes.grid": False}):
        fig, ax = plt.subplots(figsize=(FIG_WIDTH, 4.6))
        sns.heatmap(
            table, ax=ax, cmap="cividis", linewidths=0.3, linecolor="white",
            cbar_kws={"label": "Mittlere Last [GW]"},
        )
        ax.set_xticklabels(WEEKDAY_LABELS, rotation=0)
        ax.set_yticks(np.arange(0, 24, 2) + 0.5, range(0, 24, 2), rotation=0)
        ax.invert_yaxis()  # 0 Uhr unten, 23 Uhr oben
        ax.set_xlabel("Wochentag")
        ax.set_ylabel("Stunde (MEZ/MESZ)")
        fig.tight_layout()
        _save(fig, save_path)
    return fig


def plot_seasonal_boxplots(
    y: pd.Series, save_path: "str | Path | None" = None
) -> Figure:
    """Boxplots of the hourly load by local hour, weekday and month."""
    frame = _calendar_frame(y)
    panels = [
        ("hour", "(a) Nach Stunde", "Stunde (MEZ/MESZ)", None),
        ("weekday", "(b) Nach Wochentag", "Wochentag", WEEKDAY_LABELS),
        ("month", "(c) Nach Monat", "Monat", MONTH_LABELS),
    ]
    box_kwargs = {
        "color": LIGHT_COLOR,
        "linewidth": 0.6,
        "fliersize": 0.8,
        "flierprops": {"alpha": 0.3, "markeredgecolor": "#808080"},
        "medianprops": {"color": LINE_COLOR, "linewidth": 1.2},
    }

    with mpl.rc_context(THESIS_STYLE):
        fig, axes = plt.subplots(3, 1, figsize=(FIG_WIDTH, 7.0))
        for ax, (column, title, xlabel, ticklabels) in zip(axes, panels):
            sns.boxplot(data=frame, x=column, y="GW", ax=ax, **box_kwargs)
            if ticklabels is not None:
                ax.set_xticks(range(len(ticklabels)), ticklabels)
            ax.set_title(title, loc="left")
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Last [GW]")
            ax.grid(axis="x", visible=False)
        fig.tight_layout()
        _save(fig, save_path)
    return fig


def fit_mstl(
    y: pd.Series, periods: tuple[int, ...] = (24, 168, 8766)
) -> DecomposeResult:
    """Additive MSTL decomposition with daily, weekly and yearly periods.

    Non-robust STL is used because the yearly period (8766 h) makes the robust
    iterations very slow; on the five training years the fit takes ~3 minutes.
    """
    return MSTL(y, periods=periods, stl_kwargs={"robust": False}).fit()


def plot_mstl(
    result: DecomposeResult,
    overview_path: "str | Path | None" = None,
    profiles_path: "str | Path | None" = None,
) -> tuple[Figure, Figure]:
    """Plot an MSTL result as two figures.

    The overview shows observed series, trend, the longest seasonal component
    and the remainder over the whole period (daily means for readability, the
    remainder hourly). The profiles figure shows the shorter seasonal components
    (daily, weekly) averaged per local hour of day / hour of week, one line per
    year, so that changes of the pattern across years become visible.
    """
    seasonal = result.seasonal
    if isinstance(seasonal, pd.Series):
        seasonal = seasonal.to_frame()
    seasonal = seasonal / 1000
    periods = sorted(int(c.split("_")[-1]) for c in seasonal.columns)
    longest, shorter = periods[-1], periods[:-1]

    def label(period: int) -> str:
        names = {24: "Tag", 168: "Woche", 8766: "Jahr"}
        name = names.get(period)
        return f"Saison {name} ({period} h)" if name else f"Saison {period} h"

    overview = [
        ("Beobachtet", result.observed / 1000),
        ("Trend", result.trend / 1000),
        (label(longest), seasonal[f"seasonal_{longest}"]),
        ("Rest", result.resid / 1000),
    ]

    with mpl.rc_context(THESIS_STYLE):
        fig_overview, axes = plt.subplots(
            len(overview), 1, figsize=(FIG_WIDTH, 6.5), sharex=True
        )
        for ax, (name, component) in zip(axes, overview):
            if name == "Rest":
                ax.plot(component.index, component, color=LINE_COLOR, lw=0.2)
            else:
                daily = component.resample("D").mean()
                ax.plot(daily.index, daily, color=LINE_COLOR, lw=0.7)
            ax.set_ylabel(f"{name}\n[GW]")
        axes[-1].xaxis.set_major_locator(mdates.YearLocator())
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        axes[-1].set_xlabel("Zeit (UTC)")
        axes[0].set_xlim(result.observed.index[0], result.observed.index[-1])
        fig_overview.align_ylabels(axes)
        fig_overview.tight_layout()
        _save(fig_overview, overview_path)

        fig_profiles = _plot_seasonal_profiles_by_year(seasonal, shorter, label)
        _save(fig_profiles, profiles_path)
    return fig_overview, fig_profiles


def _plot_seasonal_profiles_by_year(
    seasonal: pd.DataFrame, periods: list[int], label
) -> Figure:
    """Mean seasonal component per local hour of day/week, one line per year."""
    local_index = seasonal.index.tz_localize("UTC").tz_convert(LOCAL_TZ)
    position = {
        24: pd.Index(local_index.hour),
        168: pd.Index(local_index.dayofweek * 24 + local_index.hour),
    }
    years = pd.Index(local_index.year, name="year")
    # In local time the last UTC hour can spill into the next year; skip such
    # fragments shorter than one week.
    counts = years.value_counts()
    full_years = sorted(counts[counts >= 168].index)
    colors = mpl.colormaps["cividis"](np.linspace(0.05, 0.9, len(full_years)))

    fig, axes = plt.subplots(
        len(periods), 1, figsize=(FIG_WIDTH, 2.2 * len(periods) + 0.6),
        squeeze=False,
    )
    axes = axes[:, 0]
    for ax, period in zip(axes, periods):
        component = seasonal[f"seasonal_{period}"]
        x = position.get(period, pd.Index(np.arange(len(component)) % period))
        profile = component.groupby([years, x]).mean().unstack(0)
        for color, year in zip(colors, full_years):
            ax.plot(profile.index, profile[year], color=color, lw=1.0,
                    label=str(year))
        ax.axhline(0, color="#808080", lw=0.5)
        ax.set_ylabel(f"{label(period)}\n[GW]")
        ax.set_xlim(profile.index[0], profile.index[-1])
        if period == 24:
            ax.set_xticks(range(0, 24, 2))
            ax.set_xlabel("Stunde (MEZ/MESZ)")
        elif period == 168:
            ax.set_xticks(range(0, 168, 24), [f"{d} 0 Uhr" for d in WEEKDAY_LABELS])
            ax.set_xticks(range(0, 168, 6), minor=True)
            ax.set_xlabel("Wochenstunde (MEZ/MESZ)")
        else:
            ax.set_xlabel("Position in der Periode [h]")
    axes[0].legend(title="Jahr", ncol=len(full_years), loc="lower center",
                   bbox_to_anchor=(0.5, 1.02), frameon=False)
    fig.align_ylabels(axes)
    fig.tight_layout()
    return fig


def plot_acf_pacf(
    y: pd.Series, lags: int = 336, save_path: "str | Path | None" = None
) -> Figure:
    """ACF and PACF of the raw series and of the seasonal difference (lag 168)."""
    series = [
        ("Originalreihe", y),
        ("Saisonale Differenz $\\Delta_{168}$", y.diff(168).dropna()),
    ]
    style = {"color": LINE_COLOR, "vlines_kwargs": {"colors": LINE_COLOR,
                                                    "linewidth": 0.6}}

    with mpl.rc_context(THESIS_STYLE):
        fig, axes = plt.subplots(2, 2, figsize=(FIG_WIDTH, 4.8), sharex=True)
        for row, (name, values) in enumerate(series):
            plot_acf(values, lags=lags, ax=axes[row, 0], markersize=1.2,
                     zero=False, title="", **style)
            plot_pacf(values, lags=lags, ax=axes[row, 1], markersize=1.2,
                      zero=False, method="ywm", title="", **style)
            axes[row, 0].set_title(f"(ACF) {name}", loc="left")
            axes[row, 1].set_title(f"(PACF) {name}", loc="left")
        for ax in axes.flat:
            ax.set_xticks(range(0, lags + 1, 24))
            ax.set_xlim(0, lags + 1)
            ax.set_ylim(-1.0, 1.05)
            ax.tick_params(axis="x", labelrotation=90)
            ax.axhline(0, color="#808080", lw=0.5)
            for band in ax.collections:
                if band.__class__.__name__ in ("PolyCollection", "FillBetweenPolyCollection"):
                    band.set_facecolor(LIGHT_COLOR)
                    band.set_alpha(0.5)
        for ax in axes[:, 0]:
            ax.set_ylabel("Korrelation")
        for ax in axes[1]:
            ax.set_xlabel("Lag [h]")
        fig.tight_layout()
        _save(fig, save_path)
    return fig


def _kpss(values: pd.Series) -> tuple[float, float, int, str]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", InterpolationWarning)
        stat, p_value, lags, _ = kpss(values, regression="c", nlags="auto")
    p_label = f"{p_value:.3f}"
    for warning in caught:
        if issubclass(warning.category, InterpolationWarning):
            p_label = "≤ 0.010" if p_value <= 0.01 else "≥ 0.100"
    return stat, p_value, lags, p_label


def stationarity_tests(y: pd.Series, alpha: float = 0.05) -> pd.DataFrame:
    """ADF and KPSS tests for the raw series, its first and its weekly difference.

    ADF (constant, lag order by AIC) has a unit root as H0; KPSS (level
    stationarity, automatic bandwidth) has stationarity as H0. KPSS p-values are
    only tabulated between 0.01 and 0.1, values outside are reported as bounds.
    """
    series = {
        "Originalreihe": y,
        "Δ1": y.diff(1).dropna(),
        "Δ168": y.diff(168).dropna(),
    }
    rows = []
    for name, values in series.items():
        stat, p_value, lags, *_ = adfuller(values, autolag="AIC", result_object=False)
        rows.append({
            "Reihe": name, "Test": "ADF", "Statistik": stat, "p-Wert": p_value,
            "p-Wert (Text)": "< 0.001" if p_value < 0.001 else f"{p_value:.3f}",
            "Lags": lags, "H0": "Einheitswurzel",
            "Entscheidung": "H0 verworfen" if p_value < alpha else "H0 beibehalten",
        })
        stat, p_value, lags, p_label = _kpss(values)
        rows.append({
            "Reihe": name, "Test": "KPSS", "Statistik": stat, "p-Wert": p_value,
            "p-Wert (Text)": p_label, "Lags": lags, "H0": "Stationarität",
            "Entscheidung": "H0 verworfen" if p_value < alpha else "H0 beibehalten",
        })
    return pd.DataFrame(rows)


def stationarity_latex(table: pd.DataFrame) -> str:
    """Format the result of :func:`stationarity_tests` as a booktabs table.

    Built by hand so that no optional pandas dependency (jinja2) is needed.
    """
    header = ["Reihe", "Test", "Statistik", "$p$-Wert", "Lags", "Entscheidung"]
    lines = [
        r"\begin{tabular}{llrrrl}",
        r"\toprule",
        " & ".join(header) + r" \\",
        r"\midrule",
    ]
    for _, row in table.iterrows():
        reihe = {"Δ1": r"$\Delta_{1}$", "Δ168": r"$\Delta_{168}$"}.get(
            row["Reihe"], row["Reihe"]
        )
        p_value = (
            row["p-Wert (Text)"]
            .replace("≤", r"$\leq$").replace("≥", r"$\geq$").replace("<", r"$<$")
            .replace(".", "{,}")
        )
        statistik = f"{row['Statistik']:.2f}".replace(".", "{,}")
        cells = [reihe, row["Test"], statistik, p_value, str(row["Lags"]),
                 row["Entscheidung"]]
        lines.append(" & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines)
