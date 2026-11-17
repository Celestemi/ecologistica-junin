"""OSRM: distancias, duración y geometría vial."""

from __future__ import annotations

import json
from io import StringIO
from unittest.mock import patch
from time import monotonic

import pytest

from app.services.osrm_client import OsrmLegCache, OsrmRouteLeg, fetch_driving_leg
from app.services.routing_matrix import prepare_osrm_routing


def _osrm_ok_payload() -> dict:
    return {
        "code": "Ok",
        "routes": [
            {
                "distance": 2500.0,
                "duration": 360.0,
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-75.212, -12.052],
                        [-75.210, -12.060],
                        [-75.205, -12.065],
                    ],
                },
            }
        ],
    }


def test_fetch_driving_leg_parses_geometry_and_units() -> None:
    payload = StringIO(json.dumps(_osrm_ok_payload()))

    class FakeResponse:
        def __enter__(self):
            return payload

        def __exit__(self, *args: object) -> None:
            return None

    with patch("app.services.osrm_client.urlopen", return_value=FakeResponse()):
        leg = fetch_driving_leg(
            "https://router.test",
            -12.052,
            -75.212,
            -12.065,
            -75.205,
            timeout_seconds=2.0,
        )
    assert leg is not None
    assert leg.distance_km == pytest.approx(2.5)
    assert leg.duration_minutes == pytest.approx(6.0)
    assert len(leg.coordinates) == 3
    assert leg.coordinates[0] == pytest.approx((-75.212, -12.052))


def test_osrm_cache_reuses_legs() -> None:
    cache = OsrmLegCache("https://router.test", timeout_seconds=1.0)
    fake = OsrmRouteLeg(
        distance_km=1.0,
        duration_minutes=2.0,
        coordinates=((-75.21, -12.05), (-75.20, -12.06)),
    )
    with patch("app.services.osrm_client.fetch_driving_leg", return_value=fake) as mocked:
        first = cache.get_leg(-12.05, -75.21, -12.06, -75.20)
        second = cache.get_leg(-12.05, -75.21, -12.06, -75.20)
    assert first is second
    mocked.assert_called_once()


def test_prepare_osrm_routing_without_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OSRM_BASE_URL", "")
    from app.core.config import get_settings

    get_settings.cache_clear()
    adjuster, cache = prepare_osrm_routing()
    assert adjuster is None
    assert cache is None
    get_settings.cache_clear()


def test_geometry_requests_respect_the_shared_optimizer_deadline():
    cache = OsrmLegCache("https://router.test", timeout_seconds=15.0)
    cache._deadline = monotonic() + 1.0
    with patch("app.services.osrm_client.fetch_driving_leg", return_value=None) as mocked:
        cache.get_leg(-12.05, -75.21, -12.06, -75.20)
        assert 0 < mocked.call_args.kwargs["timeout_seconds"] <= 1.0
    cache._deadline = monotonic() - 1
    with patch("app.services.osrm_client.fetch_driving_leg") as mocked:
        assert cache.get_leg(-12.03, -75.21, -12.06, -75.20) is None
        mocked.assert_not_called()


def test_solver_fetches_geometry_only_for_the_winning_route():
    from tests.test_optimizer_us007 import _depot, _order, _vehicle
    from app.services.genetic_solver import solve_vrptw

    orders = [_order(i, lon=-75.20 + i * 0.001, lat=-12.04, start_h=8, end_h=18) for i in range(1, 5)]
    cache = OsrmLegCache("https://router.test", timeout_seconds=1)
    leg = OsrmRouteLeg(distance_km=1, duration_minutes=2, coordinates=((-75.21, -12.05), (-75.20, -12.04)))
    with patch.object(cache, "prepare_distance_matrix"), patch.object(cache, "get_matrix_leg", return_value=(1, 2)), \
         patch.object(OsrmLegCache, "matrix_prepared", property(lambda self: True)), \
         patch("app.services.osrm_client.fetch_driving_leg", return_value=leg) as mocked:
        result = solve_vrptw(orders, [_vehicle()], _depot(), routing_cache=cache,
                            distance_adjuster=lambda *args: 1, generations=8, population_size=8)
    assert result.feasible
    assert mocked.call_count == len(orders) + 1
    assert all(stop.leg_coordinates for itinerary in result.itineraries for stop in itinerary.stops
               if stop.stop_type.value != "depot_start")
