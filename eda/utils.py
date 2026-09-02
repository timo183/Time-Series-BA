import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller


def plot_yearly_seasonality(df: DataFrame):
    np.random.seed(42)

    df_plot = (
        df[["month", "year", "Value"]]
        .dropna()
        .groupby(["month", "year"], as_index=False)["Value"]
        .mean()
        .sort_values(["year", "month"])
    )

    years = sorted(df_plot["year"].unique())

    colors = np.random.choice(
        list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False
    )

    fig, ax = plt.subplots(figsize=(16, 12))

    for i, year in enumerate(years):
        d = df_plot[df_plot["year"] == year]

        ax.plot(d["month"], d["Value"], color=colors[i], linewidth=1.5)

        # actual final observation for this year
        last = d.iloc[-1]

        ax.annotate(
            str(year),
            xy=(last["month"], last["Value"]),
            xytext=(10, 0),
            textcoords="offset points",
            color=colors[i],
            fontsize=11,
            va="center",
            ha="left",
            clip_on=False,
        )

    # Important: extra space for labels
    ax.set_xlim(1, 13)

    ax.set_title("Seasonal Plot - Monthly Consumption", fontsize=20)

    ax.set_xlabel("Month")
    ax.set_ylabel("Consumption [MW]")

    fig.tight_layout()

    plt.show()


def plot_weekly_seasonality(df: DataFrame):
    """Plot mean consumption for each weekday, separated by year."""
    df_plot = df.copy()

    # Derive the required fields from the DatetimeIndex when necessary.
    if "year" not in df_plot.columns:
        df_plot["year"] = df_plot.index.year
    if "day" not in df_plot.columns:
        df_plot["day"] = df_plot.index.dayofweek

    df_plot = (
        df_plot[["day", "year", "Value"]]
        .dropna()
        .groupby(["day", "year"], as_index=False)["Value"]
        .mean()
        .sort_values(["year", "day"])
    )

    years = sorted(df_plot["year"].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

    fig, ax = plt.subplots(figsize=(12, 7))

    for color, year in zip(colors, years):
        yearly_data = df_plot[df_plot["year"] == year]
        ax.plot(
            yearly_data["day"],
            yearly_data["Value"],
            color=color,
            linewidth=1.5,
            marker="o",
            label=str(year),
        )

    ax.set_xticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    ax.set_title("Weekly Seasonality of Consumption", fontsize=20)
    ax.set_xlabel("Day of week")
    ax.set_ylabel("Mean consumption [MW]")
    ax.legend(title="Year", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    plt.show()


def plot_daily_seasonality(df: DataFrame):
    """Plot mean consumption for each hour of the day, separated by year."""
    df_plot = df.copy()

    # Derive the required fields from the DatetimeIndex when necessary.
    if "year" not in df_plot.columns:
        df_plot["year"] = df_plot.index.year
    if "hour" not in df_plot.columns:
        df_plot["hour"] = df_plot.index.hour

    df_plot = (
        df_plot[["hour", "year", "Value"]]
        .dropna()
        .groupby(["hour", "year"], as_index=False)["Value"]
        .mean()
        .sort_values(["year", "hour"])
    )

    years = sorted(df_plot["year"].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

    fig, ax = plt.subplots(figsize=(12, 7))

    for color, year in zip(colors, years):
        yearly_data = df_plot[df_plot["year"] == year]
        ax.plot(
            yearly_data["hour"],
            yearly_data["Value"],
            color=color,
            linewidth=1.5,
            label=str(year),
        )

    ax.set_xticks(range(0, 24, 2))
    ax.set_xlim(0, 23)
    ax.set_title("Daily Seasonality of Consumption", fontsize=20)
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Mean consumption [MW]")
    ax.legend(title="Year", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    plt.show()


def check_stationarity(timeseries):
    result = adfuller(timeseries, autolag="AIC")
    p_value = result[1]
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {p_value}")
    print("Stationary" if p_value < 0.05 else "Non-Stationary")


def identifying_model_parameters(df: DataFrame):
    plot_acf(df)
    plot_pacf(df)
    plt.show()
