"""GeoJSON de rutas: solo geometría vial, sin cuerdas."""

from types import SimpleNamespace

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
