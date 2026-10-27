"""Pruebas unitarias de límites para emisiones, geometría y configuración."""

from types import SimpleNamespace

import pytest
from shapely.geometry import Point

from app.core import emissions, geo
from app.core.config import Settings
from app.models.enums import TipoCombustible


def _emission_settings(**overrides: float) -> SimpleNamespace:
    values = {
        "altitude_min_m": 3200.0,
        "altitude_max_m": 3450.0,
        "altitude_emission_uplift": 0.08,
        "electric_altitude_share": 0.25,
        "quinual_kg_co2_per_year": 12.0,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


@pytest.mark.parametrize(
    ("altitude", "fuel", "expected"),
    [
        (3000.0, TipoCombustible.DIESEL, 1.0),
        (3200.0, TipoCombustible.GASOLINE, 1.0),
        (3325.0, TipoCombustible.GLP, 1.04),
        (3450.0, TipoCombustible.DIESEL, 1.08),
        (3600.0, TipoCombustible.ELECTRIC, 1.02),
    ],
)
def test_altitude_emission_factor_clamps_and_distinguishes_fuels(
    monkeypatch: pytest.MonkeyPatch,
    altitude: float,
    fuel: TipoCombustible,
    expected: float,
) -> None:
    monkeypatch.setattr(emissions, "get_settings", lambda: _emission_settings())
    assert emissions.altitude_emission_factor(altitude, fuel) == pytest.approx(expected)


def test_altitude_factor_handles_an_invalid_configured_span(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        emissions,
        "get_settings",
        lambda: _emission_settings(altitude_min_m=3450.0, altitude_max_m=3200.0),
    )
    assert emissions.altitude_emission_factor(3300.0, TipoCombustible.DIESEL) == 1.0


def test_leg_co2_rejects_each_negative_input_and_ignores_descent(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(emissions, "get_settings", lambda: _emission_settings())
    common = dict(
        distance_km=2.0,
        base_g_per_km=200.0,
        slope_penalty=0.05,
        slope_pct=-4.0,
        altitude_m=3200.0,
        fuel=TipoCombustible.DIESEL,
    )
    assert emissions.leg_co2_grams(**common) == pytest.approx(400.0)
    assert emissions.leg_co2_grams(**{**common, "slope_pct": 3.0}) == pytest.approx(460.0)
    for field in ("distance_km", "base_g_per_km", "slope_penalty"):
        with pytest.raises(ValueError, match="no negativas"):
            emissions.leg_co2_grams(**{**common, field: -0.01})


def test_quinual_equivalent_validates_input_and_factor(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(emissions, "get_settings", lambda: _emission_settings())
    assert emissions.quinual_equivalent(24.0) == 2.0
    with pytest.raises(ValueError, match="no puede ser negativo"):
        emissions.quinual_equivalent(-1.0)
    monkeypatch.setattr(
        emissions,
        "get_settings",
        lambda: _emission_settings(quinual_kg_co2_per_year=0.0),
    )
    with pytest.raises(ValueError, match="debe ser positivo"):
        emissions.quinual_equivalent(1.0)


def test_geo_conversions_cover_dict_shapely_wkt_and_invalid_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(geo, "get_settings", lambda: SimpleNamespace(storage_srid=4326))
    value = {"type": "Point", "coordinates": [-75.2, -12.1]}
    assert geo.geometry_to_geojson(value) is value
    assert geo.geometry_to_geojson(Point(-75.2, -12.1))["type"] == "Point"
    assert geo.geometry_to_geojson(geo.point_wkt(-75.2, -12.1))["coordinates"] == pytest.approx((-75.2, -12.1))
    with pytest.raises(TypeError, match="No se pudo convertir"):
        geo.geometry_to_geojson(object())


def test_linestring_helpers_validate_and_preserve_coordinate_order(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(geo, "get_settings", lambda: SimpleNamespace(storage_srid=4326))
    coordinates = [[-75.2, -12.1], [-75.3, -12.2]]
    line = geo.linestring_geojson(coordinates)
    assert line["type"] == "LineString"
    assert line["coordinates"] == ((-75.2, -12.1), (-75.3, -12.2))
    wkt = geo.linestring_wkt([(-75.2, -12.1), ["-75.3", "-12.2"]])
    assert wkt.desc == "LINESTRING(-75.2 -12.1, -75.3 -12.2)"
    assert wkt.srid == 4326
    with pytest.raises(ValueError, match="al menos dos"):
        geo.linestring_geojson([[0.0, 0.0]])
    with pytest.raises(ValueError, match="al menos dos"):
        geo.linestring_wkt([(0.0, 0.0)])


def test_settings_encode_database_parts_and_derive_demo_accounts() -> None:
    settings = Settings(
        _env_file=None,
        db_user="qa user",
        db_password="p@ss/word",
        db_host="db",
        db_port=5432,
        db_name="eco",
        database_url="",
        app_environment="production",
        allow_demo_accounts=None,
    )
    assert settings.database_url == "postgresql+asyncpg://qa%20user:p%40ss%2Fword@db:5432/eco"
    assert settings.allow_demo_accounts is False
    assert Settings(_env_file=None, app_environment="demo", allow_demo_accounts=None).allow_demo_accounts is True


def test_settings_token_lifetime_and_cors_boundaries() -> None:
    assert Settings(_env_file=None, auth_token_minutes=0).token_lifetime_seconds() == 60
    assert Settings(_env_file=None, auth_token_minutes=15).token_lifetime_seconds() == 900
    assert Settings(_env_file=None, auth_token_minutes=None, auth_token_hours=0).token_lifetime_seconds() == 3600
    settings = Settings(_env_file=None, cors_origins=" https://example.com, ,http://localhost ")
    assert settings.allowed_origins() == ["https://example.com", "http://localhost"]
