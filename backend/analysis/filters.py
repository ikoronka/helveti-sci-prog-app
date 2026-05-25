import pandas as pd


def get_filter_options(df: pd.DataFrame) -> dict:
    cities = sorted(df["City"].dropna().unique().tolist())
    bhk_min = int(df["BHK"].min())
    bhk_max = int(df["BHK"].max())
    return {"cities": cities, "bhk_min": bhk_min, "bhk_max": bhk_max}
