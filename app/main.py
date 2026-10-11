import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import triage, passport, care, community

app = FastAPI(
    title="SEHAT API",
    description="Backend for SEHAT - Smart, Equitable Healthcare Access & Tracking (SIH26133)",
    version="0.1.0",
)

# Comma-separated list of allowed frontend origins, set as an env var on
# Render (e.g. "https://sehat-frontend-eight.vercel.app"). Falls back to
# allowing everything so local development / first deploys aren't blocked —
# tighten this once your Vercel URL is fixed.
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in allowed_origins.split(",")] if allowed_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router)
app.include_router(passport.router)
app.include_router(care.router)
app.include_router(community.router)


@app.get("/")
def root():
    return {"service": "SEHAT API", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}
