[Volver al README principal](../../README.md)

# Reporte Final del Proyecto (Final Project Report)

**Proyecto:** EcoLogística Junín / Huancayo. **Fecha de Cierre:** No disponible en los registros revisados; **cierre pendiente de aprobación**. **Versión:** 1.0.0.

**Borrador de situación de cierre, no acta de aceptación.** Plantilla 5.6; corte 17/11/2026, America/Lima. Referencia HEAD 61 f0 e1 e con B-08 sin commit. [Resultados actuales](../../AUDITORIA/SPRINT4_RESULTADOS_PRUEBAS.md) y [matriz integral](../../AUDITORIA/SPRINT4_MATRIZ_ACEPTACION.md).

## 1. Descripción General del Proyecto

Plataforma web de rutas sostenibles para el caso académico DistriRápido S.A.C., con flota/pedidos, GA para VRPTW/Green VRP, mapa/tabla, conductor, indicadores y PDF. El [acta 25/08/2026](../01%20Inicio/02.%20Acta%20de%20constituci%C3%B3n%20V_1_0_0.md) y el [enfoque](../01%20Inicio/01.%20Selecci%C3%B3n%20del%20enfoque%20del%20proyecto%20V_1_0_0.md) documentan adaptación a Huancayo, El Tambo y Chilca. No se presenta esa geografía como requisito literal original de Lima: la consigna inicial fuente no fue localizada. No se inventan entrevistas ni cliente real participante.

## 2. Resumen de Desempeño

### 2.1 Alcance (Predictivo y Adaptativo)

- **Objetivos y criterios de éxito:** acta busca≥15% reducción de distancia frente a secuencia,≥10% CO₂ mensual,≥90% ventanas y MVP≥70% RF-01…07; requiere contrastar fuente original ausente. Predictivo: arquitectura/requisitos/hitos y presupuesto; adaptativo: historias e incrementos con DoD.
- **Evidencia de cumplimiento:**185 backend aprobadas,68/69 frontend y4 SW; 14 casos B-08 PostGIS acreditan escenarios de publicación/rollback. No se acredita ningún RF integral completo debido a brechas concretas de datos, seguridad, cifras o alcance. No confundir conteos con aceptación ni ahorro operativo.
- **Variaciones, causas y su impacto:** hay implementación parcial y desalineación documental de Done; faltan módulos/condiciones y evidencia real de aceptación. Cambios de alcance/exenciones aprobadas no disponibles. El crecimiento de código no constituye aprobación de rebaselining.

### 2.2 Calidad

- **Requisitos y criterios de aceptación:** DoD histórica≥80% por capa, análisis sin vulnerabilidades altas/críticas/deuda bloqueante, PR por par, staging automatizado, API actualizada y RF/RNF aceptados.
- **Resultados de verificación y validación:** backend 83,27% líneas/59,98% ramas/78,68% combinado; frontend 78,80% líneas/70,80% ramas. DEF-01 falla; DEF-02/03/04 y otras brechas permanecen. Los tests actuales no acreditan certificación, E2 E navegador, SLA con OSRM ni disponibilidad.
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
| DEF-01 / contrato de prueba historial | Incidente de validación |1 caso frontend fallido; suite no verde |Registrado con fuente; no corregido por restricción de fases actuales. |
| DEF-02/03/04 / autorización, terminalidad y privacidad | Riesgos/defectos de diseño detectados |Cierre técnico bloqueado; no explotación de datos reales observada |Documentados; B-09/10 pendientes. B-08 no los resuelve. |
| DEF-10 / factibilidad y SLA | Riesgo técnico/aceptación |Tres resultados de solver inválidos; no prueba de SLA HTTP |Medidos y declarados insuficientes; no se relaja el validador. |
| DEF-14 / registros económicos y aceptación ausentes | Impedimento de gestión |EVM y cierre administrativo no acreditables |Campos no disponibles explícitos; solicitar soportes/aprobación. |

Registro histórico RIE-001…010 y otras incidencias se conservan; esta tabla no afirma que sus planes preventivos fueron aplicados sin evidencia. [Defectos vigentes](../../AUDITORIA/SPRINT4_DEFECTOS_PENDIENTES.md).

## 4. Evaluación del Éxito y Cierre

- **Satisfacción de los interesados (Stakeholders):** no disponible; faltan encuesta/escala/muestra/fecha y aceptación real. La matriz de interesados no es satisfacción medida.
- **Satisfacción y reconocimiento del equipo:** no disponibles como medición/reunión real; no inferir por resultados de tests o retrospectivas genéricas.
- **Transición operativa y cierre administrativo:** pendientes de aprobación; faltan manuales/runbook consolidado, responsables de soporte, transferencia, obligaciones económicas y acta real. Existen avances técnicos, pero no se declara éxito integral o proyecto cerrado.
