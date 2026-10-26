"""GeoJSON de rutas: solo geometría vial, sin cuerdas."""

from types import SimpleNamespace
from unittest.mock import patch

from app.api.v1.routes import _solution_has_road_geometry
from app.schemas.logistics import _merge_road_segments


def test_merge_road_segments_skips_chords() -> None:
    ordered = [
        SimpleNamespace(
            geometria_tramo={
                "type": "LineString",
                "coordinates": [[-75.21, -12.05], [-75.20, -12.06]],
            }
        ),
        SimpleNamespace(geometria_tramo=None),
    ]
    merged = _merge_road_segments(ordered)  # type: ignore[arg-type]
    assert merged == [[-75.21, -12.05], [-75.20, -12.06]]


def test_merge_road_segments_concatenates_legs() -> None:
    ordered = [
        SimpleNamespace(
            geometria_tramo={
                "type": "LineString",
                "coordinates": [[-75.21, -12.05], [-75.20, -12.06]],
            }
        ),
        SimpleNamespace(
            geometria_tramo={
                "type": "LineString",
                "coordinates": [[-75.20, -12.06], [-75.19, -12.07]],
            }
        ),
    ]
    merged = _merge_road_segments(ordered)  # type: ignore[arg-type]
    assert len(merged) == 3
    assert merged[-1] == [-75.19, -12.07]


def test_solution_has_road_geometry_accepts_shapely_tuple_coordinates() -> None:
    """PostGIS devuelve coordenadas como tuplas; no deben marcar la ruta como sin vía."""
    detail = SimpleNamespace(geometria_tramo=object())
    solution = SimpleNamespace(detalles=[detail])
    segment = {
        "type": "LineString",
        "coordinates": ((-75.21, -12.05), (-75.20, -12.06), (-75.19, -12.07)),
    }
    with patch("app.api.v1.routes.geometry_to_geojson", return_value=segment):
        assert _solution_has_road_geometry(solution) is True  # type: ignore[arg-type]
