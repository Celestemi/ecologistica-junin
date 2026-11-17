[Volver al README principal](../../README.md)

> **Actualización documental r3 — 17/11/2026.** El [estado técnico vigente](../ESTADO_TECNICO_VIGENTE.md) contiene la medición frontend nueva y sus límites. El texto r2 que sigue se conserva como registro histórico; sus pruebas backend, SW, análisis de seguridad y aceptaciones no se reejecutaron en r3. No constituye cierre aprobado.

# Reporte de Estado del Proyecto (Status Report)

<!-- complemento-r4:inicio -->
> **Complementación documental r4 — 17/11/2026.** El apartado siguiente aporta propuestas y datos simulados para completar vacíos. No declara nuevas pruebas, gastos ni aprobaciones reales. [Escenario común](../COMPLEMENTO_CONTEXTUAL_DEL_PROYECTO.md).

## Complementación r4: estado del escenario académico

**Corte documental:** 17/11/2026. **Corte económico del ejercicio:** 16/11/2026. Las cifras siguientes son simuladas y completan la práctica de gestión, sin contabilizar gasto ni aceptación reales.

| Campo antes sin información | Contenido del escenario |
|---|---|
| Actividades y siguiente hito | Datos/matriz 18–20/11; validación 23–25/11; ensayo 26/11; revisión 27/11; propuesta de cierre 30/11. |
| Dependencia principal | Datos y entorno → integración → revisión → transferencia; sin duración crítica calculada. |
| Fondos del periodo 10–16/11 | AC simulado USD 14 700; acumulado USD 112 700. |
| Costo y avance del periodo | PV USD 12 000; EV USD 13 440; CV = −USD 1 260; SPI del periodo 1,12 y CPI del periodo 0,9143. |
| Situación acumulada | PV USD 112 000; EV USD 107 520; SV = −USD 4 480 y CV = −USD 5 180. |
| Próximo periodo | Presupuesto temporal restante hasta BAC USD 22 400; costo por completar proyectado por CPI USD 28 175. Son magnitudes distintas. |
| Causa ilustrativa de desviación | Supuesto: mayor esfuerzo de integración/revisión y trabajo aún por aceptar. No se atribuyen horas o causas económicas reales. |
| Acción propuesta | Priorizar revisión y bloqueos; controlar cambios y registrar costos por paquete y periodo. |

La PM coordina; QA consolida evidencia; Backend/Frontend corrigen; DevOps prepara entorno. El escenario no cuantifica consumo de contingencia: para hacerlo se necesita registro separado de autorización y uso. Las suites r2/r3 del texto histórico no se suman ni se reejecutaron en r4.
<!-- complemento-r4:fin -->

---


> **Revisión técnica r2 — 17/11/2026, America/Lima.** Se conserva versión base 1.0.0 y nombre exigido por la plantilla. Referencia vigente: main / b47d5eb7cda26444c56460ea74591cc5f973e0b3 + correcciones sin commit. [Control de implementación](../../AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md) y [resultados actuales](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md). El estado es borrador, sin aceptación administrativa. Los resultados previos se conservan en sus fuentes y en el historial al final.

- **Proyecto:** EcoLogística Junín — adaptación documentada como EcoLogística Huancayo.
- **Fecha de Corte:** 17/11/2026, America/Lima.
- **Versión:** 1.0.0.

**Borrador verificable; cierre pendiente de aprobación.** Plantilla 5.1 del HTML final. Este corte incorpora correcciones autorizadas y pruebas actuales; no delimita retrospectivamente periodos financieros inexistentes.

## 1. Información de Alcance

- **Logros completados:** 210 backend aprobadas; 70/70 frontend y 4/4 SW. Backend 84,37 % líneas / 63,83 % ramas / 80,22 % combinado; frontend 80,47 % líneas / 71,55 % ramas. AF-01/02/03 corregidos y probados en REST/WS; AF-24 resuelto con paginación/cursor. B-08 conserva 28 unidades y 14 integraciones. Flujo TCP HTTP/WS + PostGIS real pasó 10 pasos con datos sintéticos, sin navegador. No equivale a RF íntegro aceptado. [Resultados vigentes](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md).
- **Cambios al alcance (adiciones, eliminaciones o modificaciones):** no hay rebaseline ni exenciones aprobadas. Se corrigieron defectos dentro del alcance autorizado, sin cambiar stack. La importación CSV ya existía; se rectifica su falsa ausencia en la auditoría. La adaptación geográfica sigue sustentada por acta/enfoque, no por una consigna inicial no localizada.
- **Información de calidad (defectos o incidentes detectados):** suites actuales verdes; P0 originales de autorización/terminalidad/privacidad corregidos. Persisten condiciones parciales de factores/versiones, comprobantes, dinámica durable, alcance, infraestructura y aceptación. Dependencia opentelemetry-api parcheada 1.45.1→1.45.2; SCA actual sin avisos. [Matriz vigente](../../AUDITORIA/MATRIZ_PRUEBAS_ACTUALIZADA.md).

## 2. Información de Cronograma

- **Actividades/Hitos planificados pero no completados:** aceptación integral, SLA representativo con proveedor, evidencia económica, radiadores y ensayo real de diez minutos. Acta: semana 14; sin calendario aprobado y fechas reales no se calcula atraso.
- **Causa raíz de las desviaciones:** infraestructura impedía verificar B-08 en el corte anterior y hoy se superó con servidor descartable; persisten reglas/cobertura incompletas y datos de gestión ausentes. No se imputa una causa o duración económica no registrada.
- **Impacto en próximos hitos o en la ruta crítica:** impide declarar aceptación integral y demo en vivo verificada. Ruta crítica/días no disponibles; faltan dependencias y fechas base/reales.
- **Acciones correctivas o preventivas planificadas:** revisar incremento corregido y evidencias; completar condiciones parciales de RF, ensayo, revisión humana y fuentes económicas. AF-01/02/03/24 ya tienen corrección probada, no se presentan como tareas futuras sin ejecutar.

## 3. Información de Costos

- **Fondos ejecutados en este periodo:** no disponibles en los registros revisados; faltan horas/devengos/AC sustentados.
- **Causa raíz de la variación (mano de obra, materiales o estimaciones):** no calculable sin registros reales comparables; no inferir costo de commits o tests.
- **Impacto en el presupuesto general o reserva de contingencia:** no calculable; presupuesto USD 134.400 es estimación, no BAC aprobado ni consumo de reserva. [Modelo, 15/09/2026](../02%20Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md).
- **Acciones correctivas o preventivas planificadas:** confirmar aprobación/moneda/reservas y capturar costo por trabajo/periodo con evidencia; no reconstruir horas ficticias.

## 4. Proyección (Look Ahead)

- **Logros/Entregables planificados para el próximo periodo:** propuestas de corrección/aceptación y conciliación económica, radiadores auténticos y ensayo de flujo continuo; periodo/capacidad por confirmar. [Plan](../../AUDITORIA/PLAN_SPRINT_4.md).
- **Costos planificados para el próximo periodo:** no disponibles; faltan selección estimada, capacidad y presupuesto temporal aprobados.

## 5. Riesgos, Incidentes y Comentarios

- **Nuevos riesgos identificados:** aprobar por suites verdes sin cubrir brechas, mezclar coberturas de alcances distintos y presentar EVM sin fuentes.
- **Nuevos incidentes (Issues) surgidos:** AF-24 corregido; nuevas regresiones encontraron riesgo de sustitución de entregas activas y se agregó rechazo 409 probado. SCA detectó aviso moderado transitivo y se parcheó un único paquete. Fallo inicial de caché uv se resolvió sin elevar permisos ni cambiar protecciones.
- **Comentarios relevantes:** pruebas técnicas y smoke/restore descartable no certifican normas, disponibilidad, ahorros mensuales, satisfacción o cierre. [Datos EVM requeridos](../../AUDITORIA/SOLICITUD_DATOS_EVM.md) y [evidencias humanas](../../AUDITORIA/SOLICITUD_EVIDENCIAS_HUMANAS.md).

## Actualización técnica r3: pedidos y puntos de entrega

El formulario de alta, la persistencia y edición del marcador y la visualización conjunta de rutas/pedidos están implementados. La ejecución de este corte aprobó 86/86 pruebas frontend. Cobertura: 81,35 % de líneas y 73,93 % de ramas; quedan 268 líneas y 360 ramas sin cubrir. TypeScript y build terminaron con salida 0. No se reejecutaron backend, SW aislado, seguridad ni aceptación humana. [Detalle y evidencia](../ESTADO_TECNICO_VIGENTE.md).

## Historial de revisiones del borrador

Revisión r3 (17/11/2026): incorporación de evidencia frontend nueva, cifras con denominador y límites, sin modificar costos reales ni aceptación. El registro r2 conserva sus valores históricos.

| Versión base / revisión | Fecha | Cambio y fuente |
|---|---|---|
|1.0.0 / r0 |17/11/2026, corte previo |Contenido previo conservado en Git b47d5eb y snapshot de bytes/hash [docs_cierre_antes_r1.json](../../AUDITORIA/CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json); auditorías originales sin editar. |
|1.0.0 / r1 técnica |17/11/2026, post auditoría |Actualización autorizada con evidencia nueva, corrección de referencias corruptas y límites explícitos. No cambia baseline aprobada ni constituye aceptación/cierre. |
|1.0.0 / r2 técnica |17/11/2026, validación final |210 backend/70 frontend/4 SW; cobertura final y escape literal en PDF. Evidencia r1 preservada en CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r2.json. Sin aceptación administrativa. |

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**. El ensayo técnico en vivo de diez minutos continúa pendiente de observación real.
