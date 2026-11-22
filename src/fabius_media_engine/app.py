"""Local demonstration API. NOT hardened for internet-facing deployment."""

from __future__ import annotations

import asyncio
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

from . import __version__
from .engine import (
    MediaEngineError,
    download_images,
    download_video_or_audio,
    inspect_media,
    installed_engines,
)
from .urls import InvalidMediaURL, parse_media_url

app = FastAPI(
    title="FABIUS Media Engine",
    version=__version__,
    description="Prototipo local abierto a contribuciones mediante inteligencia artificial.",
)
_STATIC = Path(__file__).parent / "static"
_SEMAPHORE = asyncio.Semaphore(2)


class URLRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2048)


class DownloadRequest(URLRequest):
    mode: str = Field(pattern=r"^(video|audio|images)$")


def _parse(url: str):
    try:
        return parse_media_url(url)
    except InvalidMediaURL as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/", include_in_schema=False)
async def homepage():
    return FileResponse(_STATIC / "index.html")


@app.get("/static/app.js", include_in_schema=False)
async def javascript():
    return FileResponse(_STATIC / "app.js", media_type="text/javascript")


@app.get("/static/styles.css", include_in_schema=False)
async def stylesheet():
    return FileResponse(_STATIC / "styles.css", media_type="text/css")


@app.get("/api/health")
async def health():
    return {"status": "development", "version": __version__, "engines": installed_engines()}


@app.post("/api/normalize")
async def normalize(request: URLRequest):
    url = _parse(request.url)
    return {"provider": url.provider, "normalized_url": url.normalized}


@app.post("/api/inspect")
async def inspect(request: URLRequest):
    url = _parse(request.url)
    async with _SEMAPHORE:
        try:
            return await asyncio.to_thread(inspect_media, url)
        except MediaEngineError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/download")
async def download(request: DownloadRequest):
    url = _parse(request.url)
    folder = Path(tempfile.mkdtemp(prefix="fabius-media-"))
    try:
        async with _SEMAPHORE:
            if request.mode == "images":
                result = await asyncio.to_thread(download_images, url, folder)
            else:
                result = await asyncio.to_thread(download_video_or_audio, url, folder, request.mode)
        return FileResponse(
            result.file_path,
            media_type=result.content_type,
            filename=result.download_name,
            background=BackgroundTask(shutil.rmtree, folder, ignore_errors=True),
        )
    except MediaEngineError as exc:
        shutil.rmtree(folder, ignore_errors=True)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception:
        shutil.rmtree(folder, ignore_errors=True)
        raise
