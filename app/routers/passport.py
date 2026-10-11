import base64
import io

import qrcode
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.store import create_passport_token, get_passport_token

router = APIRouter(prefix="/passport", tags=["passport"])


class TokenRequest(BaseModel):
    patientId: str


class TokenResponse(BaseModel):
    token: str
    qrImageBase64: str
    expiresInMinutes: int = 15


@router.post("/token", response_model=TokenResponse)
def generate_token(payload: TokenRequest):
    """
    Generates a short-lived token (not raw medical data) and a QR image
    encoding that token. A doctor scanning the QR gets the token, then calls
    /passport/verify with it — only then, with the patient's consent already
    implied by them showing the QR, does the backend resolve it to a record.
    """
    record = create_passport_token(payload.patientId)
    token = record["token"]

    img = qrcode.make(token)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return TokenResponse(token=token, qrImageBase64=qr_base64)


class VerifyResponse(BaseModel):
    valid: bool
    patientId: str | None = None


@router.get("/verify/{token}", response_model=VerifyResponse)
def verify_token(token: str):
    """Doctor-side lookup: resolve a scanned token back to a patient id."""
    record = get_passport_token(token)
    if not record:
        raise HTTPException(status_code=404, detail="Token invalid or expired")
    return VerifyResponse(valid=True, patientId=record["patient_id"])
