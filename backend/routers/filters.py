from fastapi import APIRouter, Request

from analysis.filters import get_filter_options

router = APIRouter()


@router.get("/filters")
def filters(request: Request) -> dict:
    df = request.app.state.df
    return get_filter_options(df)
