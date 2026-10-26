"""US-004 / RF-004 — importación masiva de pedidos."""

import base64
import io

import pytest
from httpx import AsyncClient
from openpyxl import Workbook
from sqlalchemy import text

from app.core.database import engine
from tests.helpers import login_headers

DAY = "2026-11-01"
HEADER = "codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon,altitud"


def _csv_line(code: str, **overrides: str) -> str:
    defaults = {
        "cliente": "Cliente Demo",
        "direccion": "Plaza Constitución, Huancayo",
        "peso_kg": "10",
        "hora_inicio": "09:00",
        "hora_fin": "12:00",
        "lat": "-12.06513",
        "lon": "-75.20486",
        "altitud": "3271",
    }
    defaults.update(overrides)
    return (
        f"{code},{defaults['cliente']},\"{defaults['direccion']}\","
        f"{defaults['peso_kg']},{defaults['hora_inicio']},{defaults['hora_fin']},"
        f"{defaults['lat']},{defaults['lon']},{defaults['altitud']}"
    )


def _csv_body(lines: list[str]) -> str:
    return HEADER + "\n" + "\n".join(lines)


def _xlsx_base64(rows: list[list[object]]) -> str:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADER.split(","))
    for row in rows:
        sheet.append(row)
    buffer = io.BytesIO()
    workbook.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


@pytest.mark.asyncio
async def test_valid_csv_import_summary(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    body = _csv_body([_csv_line("IMP-001"), _csv_line("IMP-002", cliente="Otro")])
    response = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": body}, headers=headers)
    assert response.status_code == 200
    report = response.json()
    assert report["aceptados"] == 2
    assert report["total_filas"] == 2
    assert "2 aceptados" in report["resumen"]


@pytest.mark.asyncio
async def test_empty_file_is_rejected_atomically(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    before = await client.get(f"/api/v1/jornadas/{DAY}", headers=headers)
    assert before.status_code == 200
    count_before = len(before.json()["pedidos"])
    denied = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": "   "}, headers=headers)
    assert denied.status_code == 400
    after = await client.get(f"/api/v1/jornadas/{DAY}", headers=headers)
    assert len(after.json()["pedidos"]) == count_before


@pytest.mark.asyncio
async def test_missing_header_columns_rejects_file(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    bad = "codigo,cliente\nPED-1,Cliente\n"
    denied = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": bad}, headers=headers)
    assert denied.status_code == 400
    assert "columnas" in denied.json()["detail"].casefold()


@pytest.mark.asyncio
async def test_row_missing_weight_is_rejected_partially(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    body = _csv_body([_csv_line("IMP-010"), _csv_line("IMP-011", peso_kg="")])
    response = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": body}, headers=headers)
    assert response.status_code == 200
    rows = {row["codigo_pedido"]: row for row in response.json()["filas"]}
    assert response.json()["aceptados"] == 1
    assert rows["IMP-011"]["campo"] == "peso_kg"
    assert rows["IMP-011"]["resultado"] == "rechazado"


@pytest.mark.asyncio
async def test_invalid_weight_type_and_window(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    body = _csv_body(
        [
            _csv_line("IMP-020", peso_kg="abc"),
            _csv_line("IMP-021", hora_inicio="12:00", hora_fin="09:00"),
        ]
    )
    response = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": body}, headers=headers)
    assert response.status_code == 200
    assert response.json()["aceptados"] == 0
    assert response.json()["rechazados"] == 2


@pytest.mark.asyncio
async def test_duplicate_in_file_and_database(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    body = _csv_body([_csv_line("DUP-001"), _csv_line("DUP-001", cliente="Repetido")])
    first = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": body}, headers=headers)
    assert first.status_code == 200
    assert first.json()["aceptados"] == 1
    assert first.json()["filas"][1]["motivo"] == "El código DUP-001 está duplicado en el archivo."

    repeat = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": _csv_body([_csv_line("DUP-001")])},
        headers=headers,
    )
    assert repeat.status_code == 200
    assert repeat.json()["aceptados"] == 0
    assert "Ya existe" in repeat.json()["filas"][0]["motivo"]


@pytest.mark.asyncio
async def test_max_150_rows_and_reject_151(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    lines = [_csv_line(f"MAX-{index:03d}") for index in range(150)]
    ok = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": _csv_body(lines)}, headers=headers)
    assert ok.status_code == 200
    assert ok.json()["aceptados"] == 150

    too_many = lines + [_csv_line("MAX-151")]
    denied = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": _csv_body(too_many)},
        headers=headers,
    )
    assert denied.status_code == 400
    assert "150" in denied.json()["detail"]


@pytest.mark.asyncio
async def test_xlsx_import(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    payload = _xlsx_base64(
        [
            [
                "XLS-001",
                "Cliente XLS",
                "Plaza Constitución, Huancayo",
                12,
                "09:00",
                "12:00",
                -12.06513,
                -75.20486,
                3271,
            ]
        ]
    )
    response = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"xlsx_base64": payload},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["aceptados"] == 1


@pytest.mark.asyncio
async def test_corrupt_xlsx(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    corrupt = base64.b64encode(b"not-a-workbook").decode("ascii")
    denied = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"xlsx_base64": corrupt},
        headers=headers,
    )
    assert denied.status_code == 400


@pytest.mark.asyncio
async def test_auditor_denied(client: AsyncClient) -> None:
    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    denied = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": _csv_body([_csv_line("AUD-001")])},
        headers=auditor,
    )
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_jornada_link_persisted(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    code = "JOR-001"
    await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": _csv_body([_csv_line(code)])},
        headers=headers,
    )
    async with engine.connect() as connection:
        row = (
            await connection.execute(
                text(
                    "SELECT j.fecha FROM pedidos p "
                    "JOIN jornadas j ON j.id = p.jornada_id "
                    "WHERE p.codigo_pedido = :code"
                ),
                {"code": code},
            )
        ).one()
    assert str(row.fecha) == DAY


@pytest.mark.asyncio
async def test_import_then_optimize_on_other_day(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    day_opt = "2026-10-06"
    imported = await client.post(
        f"/api/v1/jornadas/{day_opt}/importar",
        json={"csv": _csv_body([_csv_line("OPT-900")])},
        headers=headers,
    )
    assert imported.status_code == 200
    optimized = await client.post("/api/v1/optimizar-rutas", headers=headers)
    assert optimized.status_code == 201
