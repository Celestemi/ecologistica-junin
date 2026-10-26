"""Pruebas unitarias sin base de datos (complemento de cobertura DoD)."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi import HTTPException

from app.models.enums import EstadoOperativoVehiculo, EstadoPedido
from app.models.restrictions import RestriccionPlacaConfig, RestriccionPlacaRegla
from app.services.order_import import parse_csv, parse_xlsx
from app.services.order_window import assert_window_editable, normalize_delivery_window
from app.services.plate_restriction import (
    ultimo_digito_placa,
    vehicle_excluded,
    regla_aplicable,
)
from app.services.vehicle_state import apply_operational_state, assert_transition, sync_activo_flag
from types import SimpleNamespace

LIMA = ZoneInfo("America/Lima")


def test_parse_csv_rejects_empty_and_missing_columns() -> None:
    assert parse_csv("")[1] == "El archivo no tiene filas."
    rows, err = parse_csv("codigo,cliente\nX,Y\n")
    assert rows == []
    assert err and "columnas" in err.casefold()


def test_parse_csv_accepts_valid_row() -> None:
    raw = (
        "codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin\n"
        "P-1,Cliente,Calle 1,10,09:00,12:00\n"
    )
    rows, err = parse_csv(raw)
    assert err is None
    assert len(rows) == 1
    assert rows[0]["codigo"] == "P-1"


def test_parse_csv_rejects_more_than_150_rows() -> None:
    lines = ["codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin"]
    lines.extend(f"P-{i},C,D,1,09:00,10:00" for i in range(151))
    rows, err = parse_csv("\n".join(lines))
    assert rows == []
    assert err and "150" in err


def test_parse_xlsx_corrupt_bytes() -> None:
    rows, err = parse_xlsx(b"not-excel")
    assert rows == []
    assert err and "corrupto" in err.casefold()


def test_normalize_delivery_window_rejects_equal_and_inverted() -> None:
    start = datetime(2026, 10, 1, 9, 0, tzinfo=LIMA)
    end = datetime(2026, 10, 1, 9, 0, tzinfo=LIMA)
    with pytest.raises(ValueError):
        normalize_delivery_window(start, end)
    with pytest.raises(ValueError):
        normalize_delivery_window(
            datetime(2026, 10, 1, 12, 0, tzinfo=LIMA),
            datetime(2026, 10, 1, 9, 0, tzinfo=LIMA),
        )


def test_assert_window_editable_blocks_closed_and_routed() -> None:
    pending = SimpleNamespace(codigo_pedido="P1", estado=EstadoPedido.PENDING)
    assert_window_editable(pending)  # no raise
    assigned = SimpleNamespace(codigo_pedido="P2", estado=EstadoPedido.ASSIGNED)
    with pytest.raises(HTTPException) as exc:
        assert_window_editable(assigned)
    assert exc.value.status_code == 409


def test_plate_digit_and_exclusion() -> None:
    assert ultimo_digito_placa("W4U-158") == 8
    config = RestriccionPlacaConfig(
        ambito="Huancayo",
        etiqueta_validacion="x",
        validada_normativamente=True,
        activa=True,
    )
    config.reglas = [RestriccionPlacaRegla(config_id=1, ultimo_digito=8, dias_semana=[2])]
    assert regla_aplicable(config) is True
    hit = vehicle_excluded("W4U-158", date(2026, 10, 6), config.reglas)
    assert hit is not None
    assert hit.ultimo_digito == 8


def test_vehicle_state_transitions() -> None:
    vehicle = SimpleNamespace(
        id=1,
        placa="X",
        estado_operativo=EstadoOperativoVehiculo.ACTIVO,
        activo=True,
    )
    with pytest.raises(HTTPException):
        assert_transition(EstadoOperativoVehiculo.INACTIVO, EstadoOperativoVehiculo.MANTENIMIENTO)
    assert_transition(EstadoOperativoVehiculo.ACTIVO, EstadoOperativoVehiculo.MANTENIMIENTO)
    history = apply_operational_state(
        vehicle,
        EstadoOperativoVehiculo.MANTENIMIENTO,
        correo="op@test",
        motivo="Frenos",
    )
    sync_activo_flag(vehicle)
    assert vehicle.activo is False
    assert history.estado_nuevo == "mantenimiento"
