from fastapi import APIRouter, Query

from app.store import FACILITIES, haversine_km

router = APIRouter(prefix="/care", tags=["care"])


@router.get("/nearby")
def nearby_care(lat: float = Query(...), lng: float = Query(...)):
    results = []
    for f in FACILITIES:
        distance = haversine_km(lat, lng, f["lat"], f["lng"])
        results.append(
            {
                "name": f["name"],
                "type": f["type"],
                "distanceKm": round(distance, 1),
                "services": f["services"],
            }
        )
    results.sort(key=lambda r: r["distanceKm"])
    return results
