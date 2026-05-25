import pandas as pd
from scipy import stats


def compute_regression(df: pd.DataFrame) -> dict:
    clean = df[["Size", "Rent"]].dropna()
    result = stats.linregress(clean["Size"], clean["Rent"])
    return {
        "slope": round(float(result.slope), 4),
        "intercept": round(float(result.intercept), 4),
        "r_squared": round(float(result.rvalue**2), 4),
        "p_value": float(result.pvalue),
        "std_err": round(float(result.stderr), 4),
    }
