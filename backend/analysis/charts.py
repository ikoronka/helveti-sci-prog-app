import numpy as np
import pandas as pd

HISTOGRAM_BINS = 20


def compute_histogram(df: pd.DataFrame) -> dict:
    values, edges = np.histogram(df["Rent"].dropna(), bins=HISTOGRAM_BINS)
    labels = [f"₹{int(edges[i]):,}–{int(edges[i+1]):,}" for i in range(len(edges) - 1)]
    return {"labels": labels, "values": values.tolist()}


def compute_scatter(df: pd.DataFrame) -> list[dict]:
    clean = df[["Size", "Rent"]].dropna()
    return [{"x": float(row.Size), "y": float(row.Rent)} for row in clean.itertuples()]
