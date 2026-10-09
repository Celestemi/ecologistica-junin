"""Informe PDF de sostenibilidad y su descarga HTTP."""

from datetime import date

import pytest
from httpx import AsyncClient

from app.models.enums import TipoCombustible
from app.services.pdf_generator import (
    DeliveryRow,
    SustainabilityReport,
    build_sustainability_pdf,
    build_tco,
    leg_cost,
)


def _report() -> SustainabilityReport:
    deliveries = (
        DeliveryRow(
            code="PED-001",
            customer="Bodega La Colmena",
            address="Plaza Constitución",
            completed_on=date(2026, 10, 6),
            plate="W4U-158",
            vehicle_class="Combustible",
            distance_km=3.2,
            co2_g=740,
        ),
    )
    legs = [
        (TipoCombustible.DIESEL, 10.0, 2200.0),
        (TipoCombustible.ELECTRIC, 10.0, 380.0),
    ]
    return SustainabilityReport(
        period_start=date(2026, 10, 1),
        period_end=date(2026, 10, 6),
        co2_emitted_kg=3.9,
        co2_avoided_kg=5.8,
        distance_km=50.1,
        deliveries=deliveries,
        tco=build_tco(legs),
    )


def test_leg_cost_splits_fuel_and_electricity() -> None:
    diesel_energy, diesel_maintenance = leg_cost(TipoCombustible.DIESEL, 10.0, 2200.0)
    electric_energy, electric_maintenance = leg_cost(TipoCombustible.ELECTRIC, 10.0, 380.0)
    assert diesel_energy == pytest.approx((2200.0 / 2680.0) * 4.90)
    assert diesel_maintenance == pytest.approx(3.50)
    assert electric_energy == pytest.approx((0.380 / 0.150) * 0.70)
    assert electric_maintenance == pytest.approx(1.50)


def test_pdf_bytes_include_the_iso_frame_and_tco() -> None:
    pdf = build_sustainability_pdf(_report())
    assert pdf.startswith(b"%PDF")
    assert b"ISO 14083" in pdf
    assert b"TCO" in pdf
    combustible, electric = build_tco(
        [
            (TipoCombustible.DIESEL, 10.0, 2200.0),
            (TipoCombustible.ELECTRIC, 10.0, 380.0),
        ]
    )
    assert combustible.vehicle_class == "Combustible"
    assert electric.vehicle_class == "Eléctrico"
    assert combustible.tco_pen > electric.tco_pen
    assert _report().quinual_trees == pytest.approx(5.8 / 12.0)


@pytest.mark.asyncio
async def test_sustainability_pdf_endpoint(client: AsyncClient) -> None:
    from tests.helpers import login_headers

    gerente = await login_headers(client, "gerente@distrirapido.pe", "Gerente.2026")
    response = await client.get("/api/v1/reportes/sostenibilidad/pdf", headers=gerente)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
    assert "attachment;" in response.headers["content-disposition"]

    anonymous = await client.get("/api/v1/reportes/sostenibilidad/pdf")
    assert anonymous.status_code == 401

    conductor = await login_headers(client, "conductor@distrirapido.pe", "Conductor.2026")
    denied = await client.get("/api/v1/reportes/sostenibilidad/pdf", headers=conductor)
    assert denied.status_code == 403

    inverted = await client.get(
        "/api/v1/reportes/sostenibilidad/pdf",
        params={"fecha_inicio": "2026-10-10", "fecha_fin": "2026-10-01"},
        headers=gerente,
    )
    assert inverted.status_code == 400
