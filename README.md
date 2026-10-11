# SEHAT — Backend API

FastAPI backend for the SEHAT healthcare accessibility platform (Smart India Hackathon 2026, PS ID SIH26133).

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/triage` | Non-diagnostic symptom triage. Body: `{"text": "...", "lang": "en"}` |
| POST | `/passport/token` | Generate a short-lived QR token for a patient. Body: `{"patientId": "..."}` |
| GET | `/passport/verify/{token}` | Doctor-side: resolve a scanned token |
| GET | `/care/nearby?lat=..&lng=..` | Nearby facilities sorted by distance |
| GET | `/community/reports` | List community reports (road hazards, camps, Q&A) |
| POST | `/community/reports` | Create a community report |

Interactive docs (auto-generated): `/docs`

## Design notes

- **Triage is rule-based, not a black-box ML model** (`app/triage_engine.py`). It maps keywords to an urgency level and always says "this is not a diagnosis." This is deliberate — it's explainable to hackathon judges asking about AI safety, and needs no paid API key.
- **The QR passport stores a token, not medical records** (`app/routers/passport.py`). The token expires after 15 minutes and only resolves to a patient ID server-side.
- **Storage is in-memory** (`app/store.py`) so the whole thing runs free with zero database setup. Swap it for Postgres later without touching the routers.

## Running locally (optional — Render builds this for you)
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Deployment
Deployed on [Render](https://render.com) (free tier), connected directly to this GitHub repo via `render.yaml`. Every push to `main` redeploys automatically.

Set the `ALLOWED_ORIGINS` environment variable in Render to your frontend's Vercel URL so the browser is allowed to call this API.
