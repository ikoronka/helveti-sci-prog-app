import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "avg_rent": round(float(df["Rent"].mean()), 2),
        "median_size": round(float(df["Size"].median()), 2),
        "count": int(len(df)),
    }
