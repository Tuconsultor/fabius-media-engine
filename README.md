# FABIUS Media Engine

**Open-source multimedia link toolkit. AI-assisted contributions are welcome.**

Proyecto independiente para analizar enlaces públicos de **TikTok, Douyin, Bilibili, LinkedIn y X** y, cuando el recurso sea accesible y su uso esté autorizado, intentar descargar video, audio o imágenes mediante motores existentes.

> **Estado: v0.1.0, prototipo LOCAL.** Los adaptadores están implementados, pero NO se han verificado descargas reales en las cinco plataformas. **No está preparado para hospedaje público.** Consulta [SECURITY.md](SECURITY.md).

## Funciones

- Validación de URL HTTPS, detección de plataforma y normalización de enlaces.
- Normalización de enlaces directos de X (`/status/ID`).
- Inspección de metadatos mediante yt-dlp (no garantiza que el archivo sea descargable).
- Video con yt-dlp; MP3 con yt-dlp y FFmpeg.
- Imágenes con gallery-dl empaquetadas como ZIP cuando el extractor es compatible.
- Interfaz responsive, API FastAPI y documentación interactiva en `/docs`.
- Contribuciones asistidas por inteligencia artificial **permitidas**.

## Instalación local

Requisitos: **Python 3.11+** y **FFmpeg** instalado en PATH para audio y mezcla de pistas.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
fabius-media
```

Abre `http://127.0.0.1:8080`. Solo se permite loopback.

## Pruebas offline

```bash
python -m compileall -q src tests
python -m pytest -q
python -m ruff check src tests
```

## API

- `GET /api/health`: dependencias disponibles.
- `POST /api/normalize`: `{"url":"https://x.com/user/status/123456"}`.
- `POST /api/inspect`: `{"url":"https://..."}`.
- `POST /api/download`: `{"url":"https://...","mode":"video"}`. Modos: `video`, `audio`, `images`.

No se admiten cookies de sesión ni contenido privado. La disponibilidad técnica y los permisos de reproducción deben comprobarse por separado.

## Seguridad y contribución

**No desplegar esta versión directamente en Internet.** yt-dlp/gallery-dl pueden seguir redirecciones: validar la URL inicial no evita SSRF. Faltan aislamiento de red, cuotas y protección ante abuso. Consulta [SECURITY.md](SECURITY.md).

Lee [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md) y [docs/ROADMAP.md](docs/ROADMAP.md). Se permiten cambios producidos por IA si pasan revisión humana y pruebas.

Nuestro código original se publica bajo MIT. Las dependencias yt-dlp, gallery-dl y FFmpeg conservan sus licencias; no estamos afiliados a esas herramientas ni a las plataformas.
