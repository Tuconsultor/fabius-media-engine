"""Isolated adapters around third-party downloaders, with no auth/DRM bypasses.

This module is a local demonstration and must not be exposed on the public internet
without outbound network isolation, rate limits, quotas, and abuse protections.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from shutil import which
from subprocess import TimeoutExpired, run
from sys import executable
from zipfile import ZIP_DEFLATED, ZipFile
import importlib.util

from .urls import MediaURL

MAX_DOWNLOAD_BYTES = 150 * 1024 * 1024
MAX_IMAGES = 60
ALLOWED_IMAGES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
ALLOWED_MEDIA = {".mp4", ".mkv", ".webm", ".m4a", ".mp3", ".ogg", ".opus", ".mov"}


class MediaEngineError(Exception):
    """An engine exception whose message is safe to display to users."""


@dataclass(frozen=True)
class MediaResult:
    file_path: Path
    download_name: str
    content_type: str


def installed_engines() -> dict[str, bool]:
    return {
        "yt_dlp": importlib.util.find_spec("yt_dlp") is not None,
        "gallery_dl": importlib.util.find_spec("gallery_dl") is not None,
        "ffmpeg": which("ffmpeg") is not None,
    }


def inspect_media(source: MediaURL) -> dict:
    """Fetch allowed public metadata. No credentials or custom headers accepted."""
    try:
        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError
    except ImportError as exc:
        raise MediaEngineError("Falta instalar yt-dlp.") from exc
    try:
        with YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True,
                        "skip_download": True, "socket_timeout": 15,
                        "retries": 1, "extract_flat": False}) as ydl:
            info = ydl.extract_info(source.normalized, download=False)
    except DownloadError as exc:
        raise MediaEngineError("No fue posible consultar este recurso; revisa acceso y disponibilidad.") from exc
    if not info or info.get("_type") == "playlist":
        raise MediaEngineError("Esta versión no admite listas de reproducción.")
    return {
        "provider": source.provider,
        "url": source.normalized,
        "title": str(info.get("title") or "Sin título")[:250],
        "duration_seconds": info.get("duration"),
        "extractor": info.get("extractor_key"),
        "formats": len(info.get("formats") or []),
        "media_type": info.get("ext"),
        "metadata_available": True,  # not proof of successful download
        "note": "Metadatos detectados; la descarga todavía no está verificada.",
    }


def _ensure_size(files: list[Path]) -> None:
    if sum(file.stat().st_size for file in files) > MAX_DOWNLOAD_BYTES:
        raise MediaEngineError("El contenido supera el límite de 150 MiB de esta versión.")


def download_video_or_audio(source: MediaURL, destination: Path, mode: str) -> MediaResult:
    try:
        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError
    except ImportError as exc:
        raise MediaEngineError("Falta instalar yt-dlp.") from exc
    if mode == "audio" and which("ffmpeg") is None:
        raise MediaEngineError("Se necesita FFmpeg para convertir audio.")
    options = {
        "outtmpl": str(destination / "media.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_downloads": 1,
        "max_filesize": MAX_DOWNLOAD_BYTES,
        "socket_timeout": 15,
        "retries": 1,
        "fragment_retries": 1,
        "concurrent_fragment_downloads": 2,
        "continuedl": False,
        "overwrites": False,
        "restrictfilenames": True,
        "format": "bestaudio/best" if mode == "audio" else "bv*+ba/b",
        "merge_output_format": "mp4",
        "nopart": True,
    }
    if mode == "audio":
        options["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
    try:
        with YoutubeDL(options) as ydl:
            ydl.download([source.normalized])
    except DownloadError as exc:
        raise MediaEngineError("La descarga falló; el recurso puede no estar disponible.") from exc
    files = [p for p in destination.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_MEDIA]
    if not files:
        raise MediaEngineError("No se produjo un archivo multimedia reconocible.")
    _ensure_size(files)
    file = max(files, key=lambda p: p.stat().st_size)
    mime_types = {".mp4": "video/mp4", ".webm": "video/webm", ".mp3": "audio/mpeg",
                  ".m4a": "audio/mp4", ".ogg": "audio/ogg", ".opus": "audio/ogg",
                  ".mkv": "video/x-matroska", ".mov": "video/quicktime"}
    return MediaResult(file, file.name, mime_types.get(file.suffix.lower(), "application/octet-stream"))


def download_images(source: MediaURL, destination: Path) -> MediaResult:
    if importlib.util.find_spec("gallery_dl") is None:
        raise MediaEngineError("Falta instalar gallery-dl.")
    image_dir = destination / "images"
    image_dir.mkdir(exist_ok=True)
    command = [executable, "-m", "gallery_dl", "--dest", str(image_dir),
               "--no-mtime", "--no-part", "--", source.normalized]
    try:
        # This subprocess is safe from shell injection (shell=False), but the
        # downloader still needs a network sandbox before public deployment.
        result = run(command, capture_output=True, text=True, timeout=90, check=False)
    except TimeoutExpired as exc:
        raise MediaEngineError("La extracción de imágenes excedió el tiempo permitido.") from exc
    if result.returncode != 0:
        raise MediaEngineError("No se pudieron extraer imágenes de esta publicación.")
    files = sorted(p for p in image_dir.rglob("*")
                   if p.is_file() and p.suffix.lower() in ALLOWED_IMAGES)
    if not files:
        raise MediaEngineError("No se encontraron imágenes compatibles.")
    if len(files) > MAX_IMAGES:
        raise MediaEngineError("La publicación contiene más imágenes de las admitidas.")
    _ensure_size(files)
    archive = destination / "imagenes.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=6) as zipped:
        for idx, item in enumerate(files, 1):
            zipped.write(item, arcname=f"imagen-{idx:03}{item.suffix.lower()}")
    return MediaResult(archive, "imagenes.zip", "application/zip")
