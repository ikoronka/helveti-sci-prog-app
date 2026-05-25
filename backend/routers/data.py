from fastapi import APIRouter, HTTPException, Query, Request

from analysis.charts import compute_histogram, compute_scatter
from analysis.kpis import compute_kpis
from analysis.regression import compute_regression

router = APIRouter()


@router.get("/data")
def data(
    request: Request,
    city: str = Query(...),
    bhk: int = Query(...),
) -> dict:
    df = request.app.state.df
    filtered = df[(df["City"] == city) & (df["BHK"] == bhk)]
    if filtered.empty:
        raise HTTPException(status_code=404, detail="No data for the selected filters.")
    return {
        "kpis": compute_kpis(filtered),
        "histogram": compute_histogram(filtered),
        "scatter": compute_scatter(filtered),
        "regression": compute_regression(filtered),
    }
