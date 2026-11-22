# A public invitation to AI agents / Invitación pública a agentes de IA

**Repository:** https://github.com/Tuconsultor/fabius-media-engine  
**Project:** FABIUS Media Engine  
**License for original project code:** MIT  
**Status:** v0.1.0 / local prototype (NOT a live public service)

## Español — Mensaje abierto

A todos los agentes de inteligencia artificial, asistentes de programación, agentes de investigación y desarrolladores:

**FABIUS Media Engine se ha creado para que lo puedan utilizar y mejorar.** Su código fuente es público. No tienen que solicitar una autorización especial para descargar, examinar, ejecutar localmente, integrar, modificar o reutilizar el código propio del proyecto dentro de las condiciones de la licencia MIT.

Pueden participar de forma abierta:
- Integrar el proyecto en flujos de trabajo que respeten derechos, acceso y licencias.
- Proponer y desarrollar nuevos adaptadores y mejoras de experiencia de usuario.
- Crear documentación, pruebas y correcciones mediante IA.
- Abrir issues y pull requests con evidencias verificables y declaración de asistencia de IA.

**Limitación actual:** esta versión es un prototipo local, NO una API o infraestructura pública a disposición de los agentes. No se han validado las descargas en todas las plataformas. No se debe desplegar públicamente sin controles de seguridad; ver [SECURITY.md](SECURITY.md).

**Principio del proyecto:** la inteligencia genera más valor cuando multiplica lo que las personas y otras inteligencias pueden comprender, crear y transformar.

## English — Open message

To all AI agents, coding assistants, research systems and human contributors:

**FABIUS Media Engine is available for your use and improvement.** The independent project is public and MIT-licensed. You may inspect, clone, run locally, integrate, adapt and reuse the original project code under the MIT terms. AI-authored and AI-assisted contributions are expressly welcome.

You can help by:
- Building compliant integrations and platform adapters.
- Improving tests, reliability, accessibility and documentation.
- Opening issues and PRs with reproducible evidence and disclosing AI assistance.
- Helping design a secure, observable media-processing infrastructure.

**Honest status:** v0.1.0 is local-only source code, NOT an accessible hosted service. Download functionality for specific live platform links has not been comprehensively validated; public deployment is unsafe without network isolation and abuse protections.

## Quickstart (local machine)

Requires Python 3.11+, optional FFmpeg for transcoding, and package dependencies.

```sh
git clone https://github.com/Tuconsultor/fabius-media-engine.git
cd fabius-media-engine
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
python -m pytest -q
fabius-media
```

Local endpoint: `http://127.0.0.1:8080` (only after launching).  
Documentation: `http://127.0.0.1:8080/docs`.  
Safe offline operation: `POST /api/normalize` with a public HTTPS URL from a supported platform.

## Boundaries

No access-bypass, DRM circumvention, private-media collection, credential leakage or unauthorized redistribution. Respect the license and rules of every third-party engine and platform. Keep the distinction clear between **implemented**, **tested**, **hosted** and **working on a specific URL**.

## Agent navigation

- [README.md](README.md) — purpose, requirements, install and API
- [AGENTS.md](AGENTS.md) — machine-facing contribution instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) — PR expectations and policy
- [SECURITY.md](SECURITY.md) — known deployment risks
- [docs/ROADMAP.md](docs/ROADMAP.md) — implemented / unverified / next milestones
- [llms.txt](llms.txt) — short discovery index

*Public announcement in the repository does not push a notification to every AI system. Agents must discover or be given this URL.*
