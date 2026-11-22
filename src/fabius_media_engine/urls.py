"""Conservative URL validation for the initial five-platform prototype.

This is an application input gate, NOT a complete SSRF mitigation strategy.
A public deployment must also restrict outbound traffic at network level.
"""

from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit
import re

_DOMAINS = {
    "tiktok": ("tiktok.com",),
    "douyin": ("douyin.com", "iesdouyin.com"),
    "bilibili": ("bilibili.com", "b23.tv"),
    "linkedin": ("linkedin.com",),
    "x": ("x.com", "twitter.com"),
}
_X_STATUS = re.compile(r"^/(?:i/web/|[^/]+/)?status/(\d+)(?:/.*)?$", re.IGNORECASE)


class InvalidMediaURL(ValueError):
    """URL cannot be accepted by this prototype."""


@dataclass(frozen=True)
class MediaURL:
    original: str
    normalized: str
    provider: str


def parse_media_url(value: str) -> MediaURL:
    if not isinstance(value, str) or not 8 <= len(value) <= 2048:
        raise InvalidMediaURL("El enlace debe tener entre 8 y 2048 caracteres.")
    value = value.strip()
    try:
        parts = urlsplit(value)
        host = (parts.hostname or "").lower().rstrip(".")
        port = parts.port
    except ValueError as exc:
        raise InvalidMediaURL("Enlace inválido.") from exc

    if parts.scheme != "https":
        raise InvalidMediaURL("Usa enlaces HTTPS.")
    if not host or parts.username or parts.password or port not in (None, 443):
        raise InvalidMediaURL("El enlace contiene credenciales, un puerto no permitido o no tiene host.")
    if any(ch in value for ch in ("\x00", "\r", "\n", "\t")):
        raise InvalidMediaURL("El enlace contiene caracteres no permitidos.")
    provider = next(
        (
            name
            for name, domains in _DOMAINS.items()
            if any(host == domain or host.endswith("." + domain) for domain in domains)
        ),
        None,
    )
    if provider is None:
        raise InvalidMediaURL("Plataforma no admitida en esta versión.")
    normalized = urlunsplit(("https", host, parts.path or "/", parts.query, ""))
    if provider == "x":
        match = _X_STATUS.match(parts.path)
        if match:
            normalized = f"https://x.com/i/status/{match.group(1)}"
    return MediaURL(original=value, normalized=normalized, provider=provider)
