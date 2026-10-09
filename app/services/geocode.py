"""Ubica una dirección conocida del valle cuando el CSV no trae coordenadas."""

import unicodedata

# Hitos usados en la semilla y en la carga del día. El orden importa: gana la frase más larga.
_PLACES: tuple[tuple[str, float, float, float], ...] = (
    ("universidad nacional del centro", -12.03305, -75.23733, 3290.0),
    ("plaza constitucion", -12.06513, -75.20486, 3271.0),
    ("san jeronimo", -11.94903, -75.28268, 3274.0),
    ("calixto", -12.06940, -75.20749, 3268.0),
    ("chilca", -12.09820, -75.18680, 3410.0),
    ("tunan", -11.94903, -75.28268, 3274.0),
    ("uncp", -12.03305, -75.23733, 3290.0),
)


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.casefold())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def locate_address(address: str) -> tuple[float, float, float] | None:
    """Devuelve lat, lon y altitud si la dirección nombra un hito del valle."""
    folded = _fold(address)
    for name, lat, lon, altitude in _PLACES:
        if name in folded:
            return lat, lon, altitude
    return None
