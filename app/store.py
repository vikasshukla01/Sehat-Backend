"""
In-memory data store.

This is intentionally NOT a database. For the hackathon prototype it lets the
whole backend run for free with zero setup (no Postgres to provision, no
connection strings to manage). Data resets whenever the server restarts.

To move to a real database later: swap the dictionaries below for SQLAlchemy
models + a Postgres connection, and keep every router's function signature
the same — nothing else in the app needs to change.
"""

from datetime import datetime, timedelta
from typing import Optional
import secrets

# token -> {"patient_id": str, "created_at": datetime, "expires_at": datetime, "consent": bool}
PASSPORT_TOKENS: dict[str, dict] = {}

# demo facilities — nearby-care mock "database"
FACILITIES = [
    {"id": 1, "name": "Primary Health Centre, Rampur", "type": "PHC", "lat": 26.85, "lng": 80.95, "services": ["general", "maternal care"]},
    {"id": 2, "name": "Community Health Centre, Bilaspur", "type": "CHC", "lat": 26.90, "lng": 81.02, "services": ["general", "emergency", "pediatrics"]},
    {"id": 3, "name": "District Hospital", "type": "Hospital", "lat": 26.80, "lng": 80.88, "services": ["general", "emergency", "surgery", "maternal care"]},
]

# community-reported road/health items
COMMUNITY_REPORTS: list[dict] = []


def create_passport_token(patient_id: str, ttl_minutes: int = 15) -> dict:
    token = secrets.token_urlsafe(16)
    now = datetime.utcnow()
    record = {
        "patient_id": patient_id,
        "created_at": now,
        "expires_at": now + timedelta(minutes=ttl_minutes),
        "consent": True,
    }
    PASSPORT_TOKENS[token] = record
    return {"token": token, **record}


def get_passport_token(token: str) -> Optional[dict]:
    record = PASSPORT_TOKENS.get(token)
    if not record:
        return None
    if datetime.utcnow() > record["expires_at"]:
        del PASSPORT_TOKENS[token]
        return None
    return record


def haversine_km(lat1, lng1, lat2, lng2) -> float:
    from math import radians, sin, cos, sqrt, atan2

    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))
