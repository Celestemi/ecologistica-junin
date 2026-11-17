# Solicitud de datos EVM y control temporal — pendiente de aportación real

17/11/2026; revisión1. Fuente: HTML final §§2.1–2.3/5.1–5.3 y AF-04/16/17. No es un presupuesto aprobado,un registro de gasto ni una reconstrucción histórica. Propietarios indicados abajo son **roles propuestos por confirmar**,no personas designadas ni firmantes.

El modelo existente USD134400 / PEN499968 a conversión histórica3,72 suma correctamente como estimación; no se adopta como BAC,AC o autorización de reserva. Tests,commits,porcentajes técnicos y SP no son EV. No se inventan cortes anteriores.

| Campo requerido | Valor al corte | Propietario propuesto | Fuente que se necesita | Periodo/unidad | Comprobante mínimo |
|---|---|---|---|---|---|
| BAC,alcance,moneda y reserva |NO DISPONIBLE como aprobación |Patrocinador/PM/finanzas |Baseline de costo aprobada con versión |Proyecto/moneda única |Documento y aprobación auténticos |
| Fechas de corte actual/anterior |NO DISPONIBLES financieras |PM/finanzas |Calendario de reporting |Fechas,zona,regla acumulación |Registro fechado |
| Distribución presupuesto por EDT/paquete |NO DISPONIBLE |PM/planificación |Presupuesto aprobado por trabajo |Moneda y versión |Conciliación con BAC |
| Cronograma temporal y PV |NO DISPONIBLE |Planificación |Baseline aprobada,cambios y replanificaciones |Periodo actual/acumulados actual y previo |Asignación por fecha y paquete |
| Trabajo aceptado y regla EV |NO DISPONIBLE valorizado |Aceptante/PM |Actas/revisiones con criterios de aceptación y valor presupuestado |Tres cortes;moneda base |Aceptación real por entregable |
| Horas ejecutadas |NO DISPONIBLES |Equipo/finanzas |Partes de horas reales |Persona/paquete/fecha/unidad |Registro validado,sin inferir commits |
| Tarifas efectivas y devengos |NO DISPONIBLES |Finanzas |Contratos/comprobantes reales autorizados |Moneda/fecha/impuestos |Soporte conciliable con AC |
| Gastos y obligaciones pendientes |NO DISPONIBLES |Finanzas |Libro de gastos/facturas/devengos |Tres cortes |Comprobantes sin exponer datos sensibles innecesarios |
| Cambios/rebaseline aprobados |NO DISPONIBLES |Control de cambios/PM |Solicitud,impacto,aprobación y versión |Antes/después/vigencia |Historial real |
| Uso de contingencia/reserva |NO DISPONIBLE |Autoridad de reserva |Autorizaciones/ejecución |Moneda/periodo |Saldo y movimientos |
| Costo final y tolerancia |NO DISPONIBLES |PM/finanzas/aceptante |Liquidación/obligaciones/tolerancia aprobada |Cierre |Conciliación y aprobación |
| Look Ahead de actividades/costos |NO DISPONIBLE costeado |PM/equipo |Selección/capacidad/estimaciones validadas |Próximo periodo |Desglose y responsable |
| Hitos/dependencias/ruta crítica |NO DISPONIBLES completos |Planificación |Baseline y calendario/fechas reales |Fecha prevista/real |Evidencia por hito y cambio |

## Hoja prospectiva de recolección, sin datos imputados

| Corte real | EDT/entregable | Baseline/moneda | PV periodo | EV periodo y aceptante real | AC periodo y soporte | Acumulados anterior/actual | Revisor/fecha |
|---|---|---|---|---|---|---|---|
|Pendiente de completar por responsable real |Pendiente |Pendiente |No disponible |No disponible |No disponible |No disponibles |No designado/pendiente |

No completar esa fila con un ejemplo numérico que parezca ejecución. Agregar filas solo con registros auténticos; si se usa simulación para enseñar,guardarla separada y etiquetada,no incorporarla al cierre.

## Validación al recibir datos

1. Confirmar versión,alcance,moneda,periodos y aprobación;conciliar suma de paquetes con BAC y distinguir reservas.
2. Verificar PV/EV/AC de periodo,acumulado actual y acumulado anterior;las magnitudes aditivas deben conciliar.
3. Recalcular SV=EV−PV,CV=EV−AC,SPI=EV/PV,CPI=EV/AC;índices no se suman.
4. Porcentajes100×PV/BAC,100×EV/BAC,100×AC/BAC. Denominador0/ausente→NO CALCULABLE,no0/1/infinito.
5. EAC1=BAC/CPI;EAC2=BAC/(CPI×SPI);EAC3=AC+(BAC−EV)/(CPI×SPI). Justificar hipótesis seleccionada con causas reales,no elegir la menor.
6. Conectar causas,impactos y acciones con soporte;SV es presupuesto,no días de atraso.
7. Actualizar D01/D02/D03/D04/D06 solo después de revisión real. La entrega de esta solicitud no resuelve AF-04/16/17.

[Control de implementación](CONTROL_CORRECCIONES_SPRINT4.md).
