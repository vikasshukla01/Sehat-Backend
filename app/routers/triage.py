from fastapi import APIRouter
from pydantic import BaseModel

from app.triage_engine import run_triage

router = APIRouter(prefix="/triage", tags=["triage"])


class TriageRequest(BaseModel):
    text: str
    lang: str = "en"


class TriageResponse(BaseModel):
    urgency: str
    message: str
    suggestedFacility: str


@router.post("", response_model=TriageResponse)
def submit_triage(payload: TriageRequest):
    result = run_triage(payload.text, payload.lang)
    return TriageResponse(
        urgency=result.urgency,
        message=result.message,
        suggestedFacility=result.suggested_facility_type,
    )
