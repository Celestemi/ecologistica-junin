[Volver al README principal](../../README.md)

# Reporte Final del Proyecto (Final Project Report)

> **Revisión técnica r2 — 17/11/2026, America/Lima.** Se conserva versión base 1.0.0 y nombre exigido por la plantilla. Referencia vigente: main / b47d5eb7cda26444c56460ea74591cc5f973e0b3 + correcciones sin commit. [Control de implementación](../../AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md) y [resultados actuales](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md). El estado es borrador, sin aceptación administrativa. Los resultados previos se conservan en sus fuentes y en el historial al final.

**Proyecto:** EcoLogística Junín / Huancayo. **Fecha de Cierre:** No disponible en los registros revisados; **cierre pendiente de aprobación**. **Versión:** 1.0.0.

**Borrador de situación de cierre, no acta de aceptación.** Plantilla 5.6. Corte técnico vigente b47d5eb + correcciones sin commit; referencia previa HEAD 61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1 + B-08 sin commit preservada. [Resultados](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md) y [matriz vigente](../../AUDITORIA/MATRIZ_PRUEBAS_ACTUALIZADA.md).

## 1. Descripción General del Proyecto

Plataforma web de rutas sostenibles para el caso académico DistriRápido S.A.C., con flota/pedidos, GA para VRPTW/Green VRP, mapa/tabla, conductor, indicadores y PDF. El [acta 25/08/2026](../01%20Inicio/02.%20Acta%20de%20constituci%C3%B3n%20V_1_0_0.md) y el [enfoque](../01%20Inicio/01.%20Selecci%C3%B3n%20del%20enfoque%20del%20proyecto%20V_1_0_0.md) documentan adaptación a Huancayo, El Tambo y Chilca. No se presenta esa geografía como requisito literal original de Lima: la consigna inicial fuente no fue localizada. No se inventan entrevistas ni cliente real participante.

## 2. Resumen de Desempeño

### 2.1 Alcance (Predictivo y Adaptativo)

- **Objetivos y criterios de éxito:** acta busca≥15% reducción de distancia frente a secuencia,≥10% CO₂ mensual,≥90% ventanas y MVP≥70% RF-01…07; requiere contrastar fuente original ausente. Predictivo: arquitectura/requisitos/hitos y presupuesto; adaptativo: historias e incrementos con DoD.
- **Evidencia de cumplimiento:** 210 backend aprobadas; 70/70 frontend y 4/4 SW. Backend 84,37 % líneas / 63,83 % ramas / 80,22 % combinado; frontend 80,47 % líneas / 71,55 % ramas; P0 AF-01/02/03 y AF-24 corregidos con evidencia. Flujo HTTP/WS + BD real de 10 pasos pasó; frontend accesible por HTTP/proxy, sin navegador. SLA 150×15 factible probado en escenario sintético favorable, no universal. RF/RNF y metas operativas no se declaran aceptados por conteos.
- **Variaciones, causas y su impacto:** hay implementación parcial y desalineación documental de Done; faltan módulos/condiciones y evidencia real de aceptación. Cambios de alcance/exenciones aprobadas no disponibles. El crecimiento de código no constituye aprobación de rebaselining.

### 2.2 Calidad

- **Requisitos y criterios de aceptación:** DoD histórica≥80% por capa, análisis sin vulnerabilidades altas/críticas/deuda bloqueante, PR por par, staging automatizado, API actualizada y RF/RNF aceptados.
- **Resultados de verificación y validación:** 210 backend/70 frontend/4 SW verdes; gates 80 % combinado backend y 80 % líneas frontend pasan. SCA npm y OSV sin avisos tras parche transitivo 1.45.2. Build actual/PWA y flujo TCP pasan. No certifica E2E navegador, WCAG integral, OSRM/TLS, disponibilidad productiva ni aceptación por tercero.
- **Requisitos eximidos o variaciones:** no disponibles en registros revisados como exenciones aprobadas. Mantener pendientes explícitos; no excluirlos para obtener un porcentaje favorable.

### 2.3 Cronograma

| Hito / Entrega | Enfoque | Fecha Planificada | Fecha Real | Variación / Impacto |
|---|---|---|---|---|
| Cierre de Inicio / Iteración 1 | Predictivo con preparación adaptativa | Acta:semanas 2/3; fecha calendario aprobada no disponible | No disponible como aceptación real | No calculable en días; artefactos presentes no prueban aprobación. |
| Flota/pedidos/GA — Iteración 2 | Adaptativo | Semana 7; calendario detallado no disponible | No disponible como cierre aceptado | Persisten brechas de datos/DoD. |
| Mapa/KPI/tráfico — Iteración 3 | Adaptativo | Semana 11; calendario detallado no disponible | No disponible como aceptación integral | Revisión declara cumplimiento, README/auditoría mantienen pendientes; conciliar. |
| Optimización avanzada/aceptación/documentación — Iteración 4 | Híbrido | Semana 14; fecha final confirmada no disponible | No disponible; validación de casos ejecutada 17/11/2026 | Cierre bloqueado; el corte de pruebas no es fecha de cierre del proyecto. |

### 2.4 Costo

- **Presupuesto aprobado (y rango de tolerancia):** no disponible como aprobación vigente. Modelo estimado USD 134.400 y3000 h; acta conserva referencia pendiente de validación local; tolerancia no documentada.
- **Costo final real del proyecto:** no disponible: faltan horas ejecutadas, devengos/soportes/AC y conciliación de obligaciones.
- **Análisis de variaciones e impacto:** no calculable. [EVM](03%20Reporte%20de%20An%C3%A1lisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md) conserva fórmulas sin fabricar entradas. Costos logísticos de combustible no son AC del desarrollo.

## 3. Resumen de Riesgos, Incidentes e Impedimentos

| ID / Descripción | Tipo (Riesgo/Incidente/Impedimento) | Impacto Real | Respuesta Aplicada |
|---|---|---|---|
| IMP-010 / entorno de prueba antes no disponible | Impedimento histórico |14 casos B-08 no se habían ejecutado en fase 2 |En este corte se creó PostGIS descartable y14 casos aprobaron; no se reescribe informe anterior. |
| DEF-01 / contrato de prueba historial (AF-24) | Incidente histórico de validación |Un caso frontend fallaba en corte previo; ahora 70/70 pasan |Contrato 20+1 y cursor verificados, manteniendo mantenimiento/edición; corregido en ciclo autorizado. |
| DEF-02/03/04 / autorización, terminalidad y privacidad (AF-01/02/03) | Defectos del corte previo |Riesgos de integridad/privacidad detectados, sin explotación de datos reales |Corregidos y probados con reasignación, carrera, terminales y canales públicos separados; revisión de entorno/riesgo residual pendiente. |
| DEF-10 / factibilidad y SLA | Riesgo técnico/aceptación |Tres resultados aleatorios previos infactibles; no se elimina ese antecedente |Nuevo escenario sintético con testigo independiente: 150 únicos factibles en 1,7821 s API ASGI; dinámica .2373 s pipeline. Sin OSRM/red ni prueba universal. |
| DEF-14 / registros económicos y aceptación ausentes | Impedimento de gestión |EVM y cierre administrativo no acreditables |Campos no disponibles explícitos; solicitar soportes/aprobación. |

Registro histórico RIE-001…010 y otras incidencias se conservan; esta tabla no afirma que sus planes preventivos fueron aplicados sin evidencia. [Defectos vigentes](../../AUDITORIA/SPRINT4_DEFECTOS_PENDIENTES.md).

## 4. Evaluación del Éxito y Cierre

- **Satisfacción de los interesados (Stakeholders):** no disponible; faltan encuesta/escala/muestra/fecha y aceptación real. La matriz de interesados no es satisfacción medida.
- **Satisfacción y reconocimiento del equipo:** no disponibles como medición/reunión real; no inferir por resultados de tests o retrospectivas genéricas.
- **Transición operativa y cierre administrativo:** pendientes de aprobación. Se prepararon runbook, guía por roles y protocolos reproducibles; falta validación por tercero, receptor/soporte, obligaciones económicas y acta real. [Runbook](../../AUDITORIA/RUNBOOK_TECNICO_POST_CORRECCIONES.md), [solicitud humana](../../AUDITORIA/SOLICITUD_EVIDENCIAS_HUMANAS.md). No se declara éxito integral.

## Historial de revisiones del borrador

| Versión base / revisión | Fecha | Cambio y fuente |
|---|---|---|
|1.0.0 / r0 |17/11/2026, corte previo |Contenido previo conservado en Git b47d5eb y snapshot de bytes/hash [docs_cierre_antes_r1.json](../../AUDITORIA/CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json); auditorías originales sin editar. |
|1.0.0 / r1 técnica |17/11/2026, post auditoría |Actualización autorizada con evidencia nueva, corrección de referencias corruptas y límites explícitos. No cambia baseline aprobada ni constituye aceptación/cierre. |
|1.0.0 / r2 técnica |17/11/2026, validación final |210 backend/70 frontend/4 SW; cobertura final y escape literal en PDF. Evidencia r1 preservada en CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r2.json. Sin aceptación administrativa. |

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**. El ensayo técnico en vivo de diez minutos continúa pendiente de observación real.
