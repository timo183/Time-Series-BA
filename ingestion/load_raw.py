import polars as pl
from polars import DataFrame

CSV_FILES_PATH = [
    "monthly_hourly_load_values_2019.csv",
    "monthly_hourly_load_values_2020.csv",
    "monthly_hourly_load_values_2021.csv",
    "monthly_hourly_load_values_2022.csv",
    "monthly_hourly_load_values_2023.csv",
    "monthly_hourly_load_values_2024.csv",
    "monthly_hourly_load_values_2025.csv",
    "monthly_hourly_load_values_2026.csv",
]

XLSX_FILE_PATH = "MHLV_data-2015-2019.xlsx"


def load_2019_2026_file(path: str):
    df: DataFrame = pl.read_csv(f"data/raw/{path}", separator="\t")
    if "CountryCode" not in df.columns:  # 2021/2022 sind mit ; getrennt
        df = pl.read_csv(f"data/raw/{path}", separator=";")
    return df


def load_2015_2019_file(path: str):
    sheets = pl.read_excel(f"data/raw/{path}", sheet_name=["2015-2017", "2018-2019"])
    df1 = sheets["2015-2017"]
    df2 = sheets["2018-2019"]
    df = pl.concat([df1, df2], how="vertical")
    return df


def filter_country(df: DataFrame):
    return df.filter(pl.col("CountryCode") == "DE")


def select_rellevant_columns(df: DataFrame):
    return df.select(["DateUTC", "Value"])


def save_df(df: DataFrame):
    df.write_csv(
        "data/processed/panel.csv",
        separator=";",  # z.B. Semikolon (Excel-Deutschland)
    )


def create_panel():
    dataframes: list[DataFrame] = []

    df = load_2015_2019_file(XLSX_FILE_PATH)
    df = filter_country(df)
    df = select_rellevant_columns(df)
    dataframes.append(df)

    for csv_file_path in CSV_FILES_PATH:
        df = load_2019_2026_file(csv_file_path)
        df = filter_country(df)
        df = select_rellevant_columns(df)
        dataframes.append(df)

    df_gesamt = pl.concat(dataframes, how="vertical")
    save_df(df=df_gesamt)


create_panel()
