"""GeoJSON de rutas: solo geometría vial, sin cuerdas."""

from types import SimpleNamespace
from unittest.mock import patch

from app.api.v1.routes import _solution_has_road_geometry
from app.schemas.logistics import _merge_road_segments, _road_coordinate_chains


def test_merge_road_segments_rejects_legacy_geodesic_chords() -> None:
    ordered = [
        SimpleNamespace(
            geometria_tramo={
                "type": "LineString",
                "coordinates": [[-75.21, -12.05], [-75.20, -12.06]],
            }
            ,modelo_distancia="geodesica"
        ),
        SimpleNamespace(geometria_tramo=None, modelo_distancia="osrm"),
    ]
    merged = _merge_road_segments(ordered)  # type: ignore[arg-type]
    assert merged == []


def test_merge_road_segments_concatenates_legs() -> None:
    ordered = [
        SimpleNamespace(
            geometria_tramo={
                "type": "LineString",
                "coordinates": [[-75.21, -12.05], [-75.20, -12.06]],
            }
            ,modelo_distancia="osrm"
        ),
        SimpleNamespace(
            geometria_tramo={
                "type": "LineString",
                "coordinates": [[-75.20, -12.06], [-75.19, -12.07]],
            }
            ,modelo_distancia="osrm"
        ),
    ]
    merged = _merge_road_segments(ordered)  # type: ignore[arg-type]
    assert len(merged) == 3
    assert merged[-1] == [-75.19, -12.07]


def test_road_chains_do_not_bridge_a_missing_leg() -> None:
    ordered = [
        SimpleNamespace(geometria_tramo={"type": "LineString", "coordinates": [[-75.21, -12.05], [-75.20, -12.06]]}, modelo_distancia="osrm"),
        SimpleNamespace(geometria_tramo=None, modelo_distancia="geodesica"),
        SimpleNamespace(geometria_tramo={"type": "LineString", "coordinates": [[-75.19, -12.07], [-75.18, -12.08]]}, modelo_distancia="osrm"),
    ]
    assert _road_coordinate_chains(ordered) == [
        [[-75.21, -12.05], [-75.20, -12.06]],
        [[-75.19, -12.07], [-75.18, -12.08]],
    ]


def test_solution_has_road_geometry_accepts_shapely_tuple_coordinates() -> None:
    """PostGIS devuelve coordenadas como tuplas; no deben marcar la ruta como sin vía."""
    detail = SimpleNamespace(geometria_tramo=object(), modelo_distancia="osrm", secuencia=1)
    solution = SimpleNamespace(detalles=[detail])
    segment = {
        "type": "LineString",
        "coordinates": ((-75.21, -12.05), (-75.20, -12.06), (-75.19, -12.07)),
    }
    with patch("app.schemas.logistics.geometry_to_geojson", return_value=segment):
        assert _solution_has_road_geometry(solution) is True  # type: ignore[arg-type]
