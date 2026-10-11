from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from app.store import COMMUNITY_REPORTS

router = APIRouter(prefix="/community", tags=["community"])


class ReportRequest(BaseModel):
    kind: str  # "road_hazard" | "health_camp" | "question"
    text: str
    lat: float | None = None
    lng: float | None = None


@router.get("/reports")
def list_reports():
    return COMMUNITY_REPORTS


@router.post("/reports")
def create_report(payload: ReportRequest):
    report = {
        "id": len(COMMUNITY_REPORTS) + 1,
        "kind": payload.kind,
        "text": payload.text,
        "lat": payload.lat,
        "lng": payload.lng,
        "createdAt": datetime.utcnow().isoformat(),
    }
    COMMUNITY_REPORTS.append(report)
    return report
