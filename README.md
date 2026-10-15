# SEHAT — Smart, Equitable Healthcare Access & Tracking

**Backend** · FastAPI API powering the SEHAT healthcare accessibility platform.

Smart India Hackathon 2026 · Problem Statement SIH26133 · Theme: MedTech/Biotech/HealthTech · Team Code Crew

🔗 **Live API:** [sehat-backend-5ii6.onrender.com](https://sehat-backend-5ii6.onrender.com) · **Interactive docs:** [/docs](https://sehat-backend-5ii6.onrender.com/docs)
🔗 **Frontend repo:** [Sehat-Frontend](https://github.com/vikasshukla01/Sehat-Frontend) · **App:** [sehat-frontend-eight.vercel.app](https://sehat-frontend-eight.vercel.app)

> This runs on Render's free tier, which sleeps after 15 minutes of inactivity. The first request after a while takes 30–50 seconds to wake it up — hit `/health` once before a live demo to warm it up.

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/triage` | Non-diagnostic symptom triage. Body: `{"text": "...", "lang": "en"}` |
| POST | `/passport/token` | Generate a short-lived (15 min) QR token for a patient. Body: `{"patientId": "..."}` |
| GET | `/passport/verify/{token}` | Doctor-side: resolve a scanned token back to a patient ID |
| GET | `/care/nearby?lat=..&lng=..` | Nearby facilities sorted by distance, with coordinates for mapping |
| GET | `/community/reports` | List community reports (road hazards, health camps, Q&A) |
| POST | `/community/reports` | Create a community report |

Try any of these live at [`/docs`](https://sehat-backend-5ii6.onrender.com/docs) — FastAPI generates an interactive Swagger UI automatically.

## Tech stack

- **FastAPI** — async Python web framework, auto-generated OpenAPI docs
- **Pydantic** — request/response validation
- **qrcode[pil]** — generates the actual QR image server-side, returned as base64 PNG
- **In-memory store** (`app/store.py`) — zero database setup for the hackathon prototype; swappable for Postgres without touching any router

## Design notes

- **Triage is rule-based, not a black-box ML model** (`app/triage_engine.py`). It maps symptom keywords (in English and Hindi, extensible to more languages) to an urgency level — `emergency` / `urgent` / `moderate` / `self_care` — and always returns "this is not a diagnosis." This is a deliberate choice: it's fully explainable for an AI-safety conversation with judges, needs no paid API key or GPU, and is honest about what it actually does — it routes people to the right *kind* of care, it doesn't diagnose them.
- **The QR passport stores a token, not medical records** (`app/routers/passport.py`). The token expires after 15 minutes and only resolves to a patient ID server-side when a doctor scans it and calls `/passport/verify` — nothing sensitive is ever encoded in the QR image itself.
- **Nearby care includes real coordinates** (`app/store.py`), so the frontend can plot facilities and the patient's location on an actual map rather than just listing distances.

## Project structure

```
app/
├── main.py                  # FastAPI app, CORS, router registration
├── store.py                 # in-memory data + haversine distance calc
├── triage_engine.py         # rule-based symptom → urgency mapping
└── routers/
    ├── triage.py
    ├── passport.py
    ├── care.py
    └── community.py
```

## Running locally (optional — Render builds this for you)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Deployment

Deployed on [Render](https://render.com) (free tier), connected directly to this GitHub repo. Every push to `main` redeploys automatically.

Two things worth knowing if you fork this:
- **`runtime.txt` pins Python 3.11.9.** Render's current default Python has no prebuilt wheel yet for this project's pinned `pydantic-core`, which otherwise triggers a Rust source build that fails on Render's read-only filesystem. If `runtime.txt` doesn't take effect for your service, set the `PYTHON_VERSION` environment variable in Render's dashboard to the same value — that's the more reliable override.
- **Set `ALLOWED_ORIGINS`** (Render → Environment) to your frontend's deployed URL (e.g. `https://sehat-frontend-eight.vercel.app`) to restrict CORS. It defaults to `*` (allow all) so a first deploy isn't blocked before the frontend URL is known.
