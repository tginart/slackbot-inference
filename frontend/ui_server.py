#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "index.html"

BACKEND_URL = os.environ.get("INFERENCE_URL", "http://localhost:8080").rstrip("/")
BACKEND_TIMEOUT = float(os.environ.get("INFERENCE_TIMEOUT", "600"))

app = FastAPI(title="Dictation UI")


@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_PATH.read_text(encoding="utf-8")


@app.get("/health")
async def health():
    return {"status": "ok", "backend": BACKEND_URL}


@app.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(..., description="Audio file (.wav or .webm)"),
    context: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
):
    try:
        audio_bytes = await audio.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read audio: {exc}") from exc

    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio upload")

    print({
        "endpoint": "/transcribe",
        "backend_url": BACKEND_URL,
        "audio_filename": audio.filename,
        "audio_content_type": audio.content_type,
        "audio_size_bytes": len(audio_bytes),
        "context": context,
        "language": language,
    })

    files = {
        "audio": (
            audio.filename or "dictation.webm",
            audio_bytes,
            audio.content_type or "application/octet-stream",
        )
    }
    data = {}
    if context:
        data["context"] = context
    if language:
        data["language"] = language

    try:
        async with httpx.AsyncClient(timeout=BACKEND_TIMEOUT) as client:
            resp = await client.post(f"{BACKEND_URL}/transcribe", data=data, files=files)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Backend unavailable: {exc}") from exc

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "application/json"),
    )


if __name__ == "__main__":
    host = os.environ.get("UI_HOST", "0.0.0.0")
    port = int(os.environ.get("UI_PORT", "8081"))
    uvicorn.run(app, host=host, port=port)
