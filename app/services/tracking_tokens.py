"""Tokens opacos para seguimiento público (Ley N° 29733 — minimización)."""

from __future__ import annotations

import re
import uuid

_TOKEN_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def new_tracking_token() -> str:
    return str(uuid.uuid4())


def is_tracking_token(value: str) -> bool:
    return bool(_TOKEN_RE.match(value))


def delivery_zone_hint(address: str) -> str:
    lowered = address.casefold()
    for district in ("Huancayo", "El Tambo", "Chilca"):
        if district.casefold() in lowered:
            return f"Zona de entrega: {district}"
    return "Zona de entrega: valle del Mantaro"


def approximate_coordinate(value: float) -> float:
    """Redondeo ~1,1 km para no exponer la puerta exacta en el canal público."""
    return round(value, 2)
