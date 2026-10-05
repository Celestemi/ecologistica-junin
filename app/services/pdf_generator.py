"""Reporte ejecutivo de sostenibilidad en PDF, con marco ISO 14083.

El documento cubre el periodo pedido, la huella operativa de CO2, el TCO en
soles y la equivalencia local en Quinual y Aliso. La huella usa los factores
g/km de la flota (operación de transporte). No es un inventario de pozo a rueda
ni un certificado de la norma: es el informe de la cadena de última milla.
"""

from __future__ import annotations

import io
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.emissions import quinual_equivalent
from app.models.domain import Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import EstadoPedido, TipoCombustible, TipoParada

LIMA = ZoneInfo("America/Lima")

# Factores de costo del informe. Son supuestos de planificación, no una tarifa.
DIESEL_G_PER_LITER = 2680.0
GASOLINE_G_PER_LITER = 2310.0
GLP_G_PER_LITER = 1660.0
PEN_PER_LITER = {
    TipoCombustible.DIESEL: 4.90,
    TipoCombustible.GASOLINE: 5.40,
    TipoCombustible.GLP: 2.40,
}
GRAMS_PER_LITER = {
    TipoCombustible.DIESEL: DIESEL_G_PER_LITER,
    TipoCombustible.GASOLINE: GASOLINE_G_PER_LITER,
    TipoCombustible.GLP: GLP_G_PER_LITER,
}
GRID_KG_CO2_PER_KWH = 0.150
PEN_PER_KWH = 0.70
MAINTENANCE_PEN_PER_KM = {
    "Combustible": 0.35,
    "Eléctrico": 0.15,
}

GREEN = colors.HexColor("#14532d")
GREEN_SOFT = colors.HexColor("#ecfdf5")
INK = colors.HexColor("#1c1917")
MUTED = colors.HexColor("#57534e")
LINE = colors.HexColor("#d6d3d1")
PAPER = colors.HexColor("#faf7f2")
WHITE = colors.white


@dataclass(frozen=True)
class DeliveryRow:
    """Una entrega completada y sus indicadores de tramo."""

    code: str
    customer: str
    address: str
    completed_on: date | None
    plate: str
    vehicle_class: str
    distance_km: float
    co2_g: float


@dataclass(frozen=True)
class TcoRow:
    """Costo de poseer y operar una clase de vehículo en el periodo."""

    vehicle_class: str
    distance_km: float
    energy_pen: float
    maintenance_pen: float
    co2_kg: float

    @property
    def tco_pen(self) -> float:
        return self.energy_pen + self.maintenance_pen


@dataclass(frozen=True)
class SustainabilityReport:
    """Cifras que el PDF solo maqueta."""

    period_start: date
    period_end: date
    co2_emitted_kg: float
    co2_avoided_kg: float
    distance_km: float
    deliveries: tuple[DeliveryRow, ...]
    tco: tuple[TcoRow, ...]

    @property
    def quinual_trees(self) -> float:
        return quinual_equivalent(max(0.0, self.co2_avoided_kg))


def as_fuel(value: TipoCombustible | str) -> TipoCombustible:
    """Normaliza el combustible venga como enum o como texto guardado."""
    if isinstance(value, TipoCombustible):
        return value
    return TipoCombustible(value)


def vehicle_class(fuel: TipoCombustible | str) -> str:
    """Agrupa la flota en el cuadro de TCO: combustible frente a eléctrico."""
    return "Eléctrico" if as_fuel(fuel) is TipoCombustible.ELECTRIC else "Combustible"


def leg_cost(fuel: TipoCombustible | str, distance_km: float, co2_g: float) -> tuple[float, float]:
    """Energía y mantenimiento en soles de un tramo, a partir de su CO2 y sus km."""
    kind = as_fuel(fuel)
    distance = max(0.0, distance_km)
    grams = max(0.0, co2_g)
    if kind is TipoCombustible.ELECTRIC:
        kilowatt_hours = (grams / 1000.0) / GRID_KG_CO2_PER_KWH
        energy = kilowatt_hours * PEN_PER_KWH
    else:
        energy = (grams / GRAMS_PER_LITER[kind]) * PEN_PER_LITER[kind]
    maintenance = distance * MAINTENANCE_PEN_PER_KM[vehicle_class(kind)]
    return energy, maintenance


def build_tco(legs: Sequence[tuple[TipoCombustible | str, float, float]]) -> tuple[TcoRow, ...]:
    """Suma km, soles y CO2 por clase de vehículo."""
    buckets = {
        "Combustible": {"km": 0.0, "energy": 0.0, "maintenance": 0.0, "co2_g": 0.0},
        "Eléctrico": {"km": 0.0, "energy": 0.0, "maintenance": 0.0, "co2_g": 0.0},
    }
    for fuel, distance_km, co2_g in legs:
        bucket = buckets[vehicle_class(fuel)]
        energy, maintenance = leg_cost(fuel, distance_km, co2_g)
        bucket["km"] += max(0.0, distance_km)
        bucket["energy"] += energy
        bucket["maintenance"] += maintenance
        bucket["co2_g"] += max(0.0, co2_g)
    return tuple(
        TcoRow(
            vehicle_class=label,
            distance_km=values["km"],
            energy_pen=values["energy"],
            maintenance_pen=values["maintenance"],
            co2_kg=values["co2_g"] / 1000.0,
        )
        for label, values in buckets.items()
    )


async def load_sustainability_report(
    session: AsyncSession,
    period_start: date | None,
    period_end: date | None,
) -> SustainabilityReport:
    """Arma el informe con las soluciones y las entregas completadas del periodo."""
    start, end = await _resolve_period(session, period_start, period_end)
    solutions = list(
        (
            await session.scalars(
                select(SolucionRuta)
                .where(
                    SolucionRuta.fecha_operacion >= start,
                    SolucionRuta.fecha_operacion <= end,
                )
                .options(
                    selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.vehiculo),
                    selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.pedido),
                )
                .order_by(SolucionRuta.fecha_operacion, SolucionRuta.id)
            )
        ).all()
    )
    emitted = sum(solution.co2_estimado_kg for solution in solutions)
    avoided = sum(solution.co2_evitado_kg for solution in solutions)
    distance = sum(solution.distancia_total_km for solution in solutions)
    legs: list[tuple[TipoCombustible | str, float, float]] = []
    deliveries = _completed_deliveries(solutions, start, end)
    for solution in solutions:
        for detail in solution.detalles:
            vehicle = detail.vehiculo
            if vehicle is None:
                continue
            legs.append((vehicle.tipo_combustible, detail.distancia_tramo_km, detail.co2_tramo_g))
    return SustainabilityReport(
        period_start=start,
        period_end=end,
        co2_emitted_kg=emitted,
        co2_avoided_kg=avoided,
        distance_km=distance,
        deliveries=tuple(deliveries),
        tco=build_tco(legs),
    )


def build_sustainability_pdf(report: SustainabilityReport) -> bytes:
    """Devuelve el PDF del informe listo para el stream HTTP."""
    buffer = io.BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=22 * mm,
        bottomMargin=16 * mm,
        title="Informe de sostenibilidad EcoLogística Huancayo",
        author="EcoLogística Huancayo",
        pageCompression=0,
    )
    styles = _styles()
    period = _period_label(report.period_start, report.period_end)
    story: list[Flowable] = [
        _masthead(period),
        Spacer(1, 6 * mm),
        Paragraph("Informe de sostenibilidad de la cadena de transporte", styles["h1"]),
        Paragraph(
            "Última milla urbana en el Valle del Mantaro. Marco de reporte alineado a ISO 14083: "
            "periodo, dato de actividad, resultado de CO2 y metodología.",
            styles["lead"],
        ),
        Spacer(1, 4 * mm),
        _section("1. Huella de carbono", styles),
        Paragraph(
            "CO2 de la operación de transporte calculado con los factores g/km de cada vehículo, "
            "incluida la penalización por pendiente. El CO2 evitado se mide contra el reparto FIFO.",
            styles["body"],
        ),
        Spacer(1, 2 * mm),
        _carbon_table(report),
        Spacer(1, 5 * mm),
        _section("2. TCO por tipo de vehículo", styles),
        Paragraph(
            "Total Cost of Ownership del periodo, en soles. La energía sale del CO2 del tramo: "
            "litros para diésel, gasolina y GLP, y kWh de red para el eléctrico. "
            "El mantenimiento es un supuesto por kilómetro.",
            styles["body"],
        ),
        Spacer(1, 2 * mm),
        _tco_table(report.tco),
        Paragraph(_tco_assumptions(), styles["note"]),
        Spacer(1, 5 * mm),
        _section("3. Equivalencia ecológica local", styles),
        Paragraph(
            f"El CO2 evitado equivale a <b>{_num(report.quinual_trees, 2)}</b> árboles "
            "Quinual o Aliso sembrados en el Valle del Mantaro. "
            "Las dos especies comparten el factor local de 12 kg de CO2 al año por árbol; "
            "no se suman entre sí.",
            styles["body"],
        ),
        Spacer(1, 2 * mm),
        _equivalence_table(report),
        Spacer(1, 5 * mm),
        _section("4. Entregas completadas", styles),
        Paragraph(
            f"{len(report.deliveries)} envíos con estado entregado en el periodo. "
            f"Actividad de las soluciones: {_num(report.distance_km, 1)} km.",
            styles["body"],
        ),
        Spacer(1, 2 * mm),
        _delivery_table(report.deliveries, styles),
        Spacer(1, 6 * mm),
        Paragraph("Metodología", styles["h2"]),
        Paragraph(
            "Organización informante: EcoLogística Huancayo. Cadena: reparto urbano de última milla "
            "con origen en el depósito de El Tambo. Gases: CO2 operativo de la flota. "
            "El eléctrico usa 0,150 kg CO2/kWh de la red para traducir esa huella a energía. "
            "Este PDF no sustituye una verificación externa de ISO 14083.",
            styles["note"],
        ),
    ]
    document.build(story, onFirstPage=_page, onLaterPages=_page)
    return buffer.getvalue()


class BrandMark(Flowable):
    """Isotipo vectorial: hoja sobre el verde del valle."""

    def __init__(self, size: float = 28) -> None:
        super().__init__()
        self.width = size
        self.height = size

    def draw(self) -> None:
        canvas = self.canv
        side = self.width
        canvas.setFillColor(GREEN)
        canvas.roundRect(0, 0, side, side, 4, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#d1fae5"))
        path = canvas.beginPath()
        path.moveTo(side * 0.50, side * 0.18)
        path.curveTo(side * 0.18, side * 0.40, side * 0.22, side * 0.78, side * 0.50, side * 0.84)
        path.curveTo(side * 0.78, side * 0.78, side * 0.82, side * 0.40, side * 0.50, side * 0.18)
        canvas.drawPath(path, fill=1, stroke=0)
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(0.8)
        canvas.line(side * 0.50, side * 0.22, side * 0.50, side * 0.72)


def _masthead(period: str) -> Table:
    styles = _styles()
    title = Paragraph(
        "EcoLogística Huancayo<br/>"
        "<font size='8' color='#57534e'>Informe ejecutivo de sostenibilidad</font>",
        styles["brand"],
    )
    when = Paragraph(period, styles["brand_meta"])
    table = Table(
        [[BrandMark(32), title, when]],
        colWidths=[16 * mm, 110 * mm, 52 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LINEBELOW", (0, 0), (-1, -1), 1.2, GREEN),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
            ]
        )
    )
    return table


def _carbon_table(report: SustainabilityReport) -> Table:
    avoided_share = 0.0
    reference = report.co2_emitted_kg + report.co2_avoided_kg
    if reference > 0:
        avoided_share = report.co2_avoided_kg / reference * 100.0
    rows = [
        ["Indicador", "Valor"],
        ["CO2 emitido (ruta eco)", f"{_num(report.co2_emitted_kg)} kg"],
        ["CO2 evitado frente al FIFO", f"{_num(report.co2_avoided_kg)} kg"],
        ["Reducción sobre la referencia", f"{_num(avoided_share, 1)} %"],
        ["Distancia de las soluciones", f"{_num(report.distance_km, 1)} km"],
    ]
    return _data_table(rows, [110 * mm, 68 * mm])


def _tco_table(rows: Sequence[TcoRow]) -> Table:
    header = ["Clase", "Km", "Energía (S/)", "Manten. (S/)", "TCO (S/)", "CO2 (kg)"]
    body = [header]
    for row in rows:
        body.append(
            [
                row.vehicle_class,
                _num(row.distance_km, 1),
                _num(row.energy_pen),
                _num(row.maintenance_pen),
                _num(row.tco_pen),
                _num(row.co2_kg),
            ]
        )
    table = _data_table(body, [32 * mm, 24 * mm, 32 * mm, 32 * mm, 28 * mm, 30 * mm])
    return table


def _equivalence_table(report: SustainabilityReport) -> Table:
    trees = _num(report.quinual_trees, 2)
    rows = [
        ["Especie local", "Factor", "Equivalente del periodo"],
        ["Quinual", "12 kg CO2 / año", f"{trees} árboles"],
        ["Aliso", "12 kg CO2 / año", f"{trees} árboles"],
    ]
    return _data_table(rows, [50 * mm, 64 * mm, 64 * mm])


def _delivery_table(deliveries: Sequence[DeliveryRow], styles: dict[str, ParagraphStyle]) -> Table:
    header = [
        Paragraph(text, styles["th"])
        for text in ["Pedido", "Cliente", "Fecha", "Placa", "Km", "CO2 (g)"]
    ]
    body: list[list[object]] = [header]
    if not deliveries:
        body.append(
            [
                Paragraph("Sin entregas completadas en el periodo.", styles["td"]),
                "",
                "",
                "",
                "",
                "",
            ]
        )
    for row in deliveries:
        completed = row.completed_on.strftime("%d/%m/%Y") if row.completed_on else "—"
        body.append(
            [
                Paragraph(row.code, styles["td"]),
                Paragraph(f"{row.customer}<br/>{row.address}", styles["td"]),
                Paragraph(completed, styles["td"]),
                Paragraph(f"{row.plate}<br/>{row.vehicle_class}", styles["td"]),
                Paragraph(_num(row.distance_km, 1), styles["td_right"]),
                Paragraph(_num(row.co2_g, 0), styles["td_right"]),
            ]
        )
    table = Table(body, colWidths=[24 * mm, 62 * mm, 24 * mm, 28 * mm, 18 * mm, 22 * mm], repeatRows=1)
    style = _grid_style()
    if not deliveries:
        style.add("SPAN", (0, 1), (-1, 1))
    table.setStyle(style)
    return table


def _data_table(rows: list[list[str]], widths: list[float]) -> Table:
    table = Table(rows, colWidths=widths, repeatRows=1)
    table.setStyle(_grid_style())
    return table


def _grid_style() -> TableStyle:
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("TEXTCOLOR", (0, 1), (-1, -1), INK),
            ("BACKGROUND", (0, 1), (-1, -1), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREEN_SOFT]),
            ("GRID", (0, 0), (-1, -1), 0.3, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )


def _section(title: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph(title, styles["h2"])


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "brand": ParagraphStyle(
            "brand",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=16,
            textColor=GREEN,
        ),
        "brand_sub": ParagraphStyle(
            "brand_sub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=MUTED,
        ),
        "brand_meta": ParagraphStyle(
            "brand_meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            alignment=TA_RIGHT,
            textColor=INK,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=INK,
            spaceAfter=2,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=GREEN,
            spaceBefore=0,
            spaceAfter=2,
        ),
        "lead": ParagraphStyle(
            "lead",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=INK,
            alignment=TA_LEFT,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            spaceBefore=2,
        ),
        "th": ParagraphStyle(
            "th",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=WHITE,
        ),
        "td": ParagraphStyle(
            "td",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=INK,
        ),
        "td_right": ParagraphStyle(
            "td_right",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            alignment=TA_RIGHT,
            textColor=INK,
        ),
    }


def _page(canvas, doc) -> None:  # noqa: ANN001 — callback de ReportLab
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(GREEN)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(16 * mm, height - 7.5 * mm, "EcoLogística Huancayo  ·  ISO 14083")
    canvas.drawRightString(width - 16 * mm, height - 7.5 * mm, f"Página {doc.page}")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(16 * mm, 8 * mm, "Huella operativa de la última milla. No es un certificado de verificación.")
    canvas.restoreState()


def _tco_assumptions() -> str:
    return (
        "Supuestos: diésel S/ 4,90/L y 2,68 kg CO2/L; gasolina S/ 5,40/L y 2,31 kg CO2/L; "
        "GLP S/ 2,40/L y 1,66 kg CO2/L; electricidad S/ 0,70/kWh y 0,150 kg CO2/kWh. "
        "Mantenimiento: S/ 0,35/km en combustible y S/ 0,15/km en eléctrico."
    )


def _period_label(start: date, end: date) -> str:
    return f"Del {_date(start)}<br/>al {_date(end)}"


def _date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def _num(value: float, digits: int = 2) -> str:
    sign = "-" if value < 0 else ""
    text = f"{abs(value):,.{digits}f}"
    return sign + text.replace(",", " ").replace(".", ",")


def _completed_deliveries(
    solutions: Sequence[SolucionRuta],
    start: date,
    end: date,
) -> list[DeliveryRow]:
    chosen: dict[int, RutaDetalle] = {}
    for solution in solutions:
        for detail in solution.detalles:
            order = detail.pedido
            if detail.tipo_parada is not TipoParada.DELIVERY or order is None:
                continue
            if order.estado is not EstadoPedido.DELIVERED:
                continue
            completed = _completion_day(detail, order)
            if completed is None or not start <= completed <= end:
                continue
            current = chosen.get(order.id)
            if current is None or detail.id > current.id:
                chosen[order.id] = detail
    rows = [_delivery_row(detail) for detail in chosen.values()]
    rows.sort(key=lambda row: (row.completed_on or date.min, row.code))
    return rows


def _delivery_row(detail: RutaDetalle) -> DeliveryRow:
    order = detail.pedido
    vehicle: Vehiculo | None = detail.vehiculo
    assert order is not None
    fuel = vehicle.tipo_combustible if vehicle is not None else TipoCombustible.DIESEL
    return DeliveryRow(
        code=order.codigo_pedido,
        customer=order.cliente_nombre,
        address=order.direccion_referencia,
        completed_on=_completion_day(detail, order),
        plate=vehicle.placa if vehicle is not None else "—",
        vehicle_class=vehicle_class(fuel),
        distance_km=detail.distancia_tramo_km,
        co2_g=detail.co2_tramo_g,
    )


def _completion_day(detail: RutaDetalle, order: Pedido) -> date | None:
    moment = detail.eta or order.ventana_fin
    if moment is None:
        return None
    if moment.tzinfo is None:
        return moment.date()
    return moment.astimezone(LIMA).date()


async def _resolve_period(
    session: AsyncSession,
    period_start: date | None,
    period_end: date | None,
) -> tuple[date, date]:
    if period_start is not None and period_end is not None and period_end < period_start:
        raise ValueError("La fecha fin debe ser posterior o igual a la fecha de inicio.")
    earliest = await session.scalar(select(func.min(SolucionRuta.fecha_operacion)))
    latest = await session.scalar(select(func.max(SolucionRuta.fecha_operacion)))
    today = datetime.now(LIMA).date()
    start = period_start or earliest or today
    end = period_end or latest or today
    if end < start:
        end = start
    return start, end
