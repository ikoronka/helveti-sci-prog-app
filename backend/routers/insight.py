from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class InsightRequest(BaseModel):
    city: str
    bhk: int
    n_samples: int
    slope: float
    r_squared: float
    p_value: float


@router.post("/insight")
def insight(body: InsightRequest, request: Request) -> dict:
    llm = request.app.state.llm
    conclusion = llm.generate_conclusion(
        city=body.city,
        bhk=body.bhk,
        n_samples=body.n_samples,
        slope=body.slope,
        r_squared=body.r_squared,
        p_value=body.p_value,
    )
    return {"conclusion": conclusion}
