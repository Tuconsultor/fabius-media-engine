# FABIUS Media Engine

**Open-source multimedia link toolkit. AI-assisted contributions are welcome.**

Proyecto independiente, creado para analizar enlaces públicos de **TikTok, Douyin,
Bilibili, LinkedIn y X** y, cuando el recurso sea accesible y su uso esté autorizado,
intentar descargar video, audio o imágenes mediante motores existentes.

> **Estado real: v0.1.0, prototipo para ejecución LOCAL.** El código contiene
> adaptadores funcionales, pero NO se han verificado descargas reales en las cinco
> plataformas ni está preparado para un servidor público. Ver [SECURITY.md](SECURITY.md).

## Funciones

- Validación conservadora de URLs HTTPS, detección de plataforma, normalización de URLs.
- Normalización de enlaces directos a publicaciones de X (`/status/ID`).
- Inspección de metadatos a través de yt-dlp; **inspeccionar no verifica una descarga**.
- Video con yt-dlp; MP3 con yt-dlp + FFmpeg.
- Galerías/imágenes con gallery-dl en archivo ZIP (cuando el extractor lo permite).
- Web responsive y API FastAPI documentada en `/docs`.
- Contribuciones generadas o asistidas por IA **permitidas** en este repositorio.

## Instalación local

Requisitos: **Python 3.11+**, **FFmpeg** en PATH para audio y mezcla de pistas.

```bash
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
python -m pip install -e '.[dev]'
fabius-media
```

Abre `http://127.0.0.1:8080`. El servidor se limita deliberadamente a loopback.

## Pruebas sin acceso a redes sociales

```bash
python -m compileall -q src tests
python -m pytest -q
python -m ruff check src tests
```

## API

- `GET /api/health`: disponibilidad de dependencias locales.
- `POST /api/normalize` con `{"url":"https://x.com/alguien/status/123456789"}`.
- `POST /api/inspect` con `{"url":"https://..."}`.
- `POST /api/download` con `{"url":"https://...","mode":"video"}`;
  `mode` admite `video`, `audio` y `images`.

El programa no admite cookies de sesión ni extracción de contenido privado.
La elegibilidad de los medios depende de permisos y disponibilidad técnica.
El mero hecho de que un URL sea público no concede derechos de reproducción.

## Por qué no alojamos públicamente esta versión

Los descargadores pueden seguir redirecciones hacia otros hosts. Una validación del
hostname inicial **no elimina el riesgo SSRF**. Para internet se requieren controles
a nivel de red, aislamiento de procesos, cuotas, límites de banda y antifraude.
Consulta [SECURITY.md](SECURITY.md).

## Cómo contribuir

Consulta [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md) y
[docs/ROADMAP.md](docs/ROADMAP.md). Aceptamos código generado o asistido por IA,
siempre con revisión humana, evidencia y pruebas.

Nuestro código original: **MIT**. yt-dlp, gallery-dl y FFmpeg conservan sus licencias
independientes. No estamos afiliados a sus desarrolladores ni a las plataformas.
