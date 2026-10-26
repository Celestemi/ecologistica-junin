# 01. Informe de estado del proyecto — Sprint 2 V_1_0_0.md

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

**Sprint:** 2 — Geocodificación y motor de rutas (VRPTW endurecido)

**Fecha de actualización:** 26 de octubre de 2026

**Evidencias de verificación:** [VERIFICACION_FINAL_SPRINT_2.md](../../../VERIFICACION_FINAL_SPRINT_2.md), [PLAN_IMPLEMENTACION_SPRINT_2.md](../../../PLAN_IMPLEMENTACION_SPRINT_2.md), [REPORTE_RENDIMIENTO_EN_001.md](../../../REPORTE_RENDIMIENTO_EN_001.md), suites en `tests/`.

---

## Objetivo del Sprint 2

Completar la geocodificación espacial de pedidos y endurecer el motor de rutas existente para que la **solución publicada** respete capacidad, ventanas de tiempo, jornada operativa y un **presupuesto de tiempo de 45 segundos**, sin regresionar las capacidades verificables del Sprint 1.

*Fuente:* [PLAN_IMPLEMENTACION_SPRINT_2.md](../../../PLAN_IMPLEMENTACION_SPRINT_2.md) §1.

---

## Estado general del Sprint 2

| Dimensión | Estado |
|-----------|--------|
| **Alcance planificado** | US-005, US-007, US-008, US-009, EN-001 — **34 SP** |
| **Implementación funcional en código** | **Avanzada** en las cinco historias; brechas por criterio en [VERIFICACION_FINAL_SPRINT_2.md](../../../VERIFICACION_FINAL_SPRINT_2.md) |
| **Definition of Done global** ([DoD §2](../../02%20Planificacion/01_transformando_a_agil_v_1_0_0.md)) | **No cumplida** |
| **Pruebas automatizadas E2E (PostGIS)** | **No ejecutadas** en la verificación 2026-10-26 (Docker/PostGIS no disponible en host de auditoría) |
| **Cobertura ≥ 80 %** | **No alcanzada** (~50 % backend en corrida focal; frontend sin medición) |
| **Ceremonia Scrum (Review / Retro)** | **No documentada** en este repositorio; retrospectiva Sprint 2 preparada como **borrador técnico** pendiente de validación del equipo |

**Veredicto de gestión:** el Sprint 2 se considera **entregado en implementación técnica parcial**, con **validación integral y cierre DoD pendientes**. **No** se declara el 100 % de finalización del alcance (34 SP) en sentido *Done*.

---

## Historias y habilitadores — planificación vs evidencia

| ID | Trazado | SP | Implementación técnica (resumen) | Pruebas (evidencia 2026-10-26) | Estado documental |
|----|---------|-----|----------------------------------|--------------------------------|-------------------|
| **US-005** | RF-005 | 5 | Migración **007**, `estado_ubicacion`, polígono/`operating_area`, persistencia pendiente, `PATCH` ubicación, exclusión del lote a optimizar | `tests/test_geocode_us005.py` — **6 ERROR** (sin BD) | **Implementada — validación pendiente** |
| **US-007** | RF-007 / RN-008 | 13 | Precheck flota, 409, filtro jornada/fecha, metadatos ahorro vs línea base secuencial, `no_asignados` | 5 PASS unitarios; 2 ERROR API; 1 **FAIL** fixture ventanas | **Parcial** |
| **US-008** | RF-008 / RN-003 / RN-004 | 5 | `route_constraints.py`, `validate_for_publication`, jornada 8 h, HTTP **409** sin persistir infactible | 9 PASS; 3 ERROR API; 1 **FAIL** precheck volumen (test) | **Parcial** |
| **US-009** | RF-009 / RN-005 | 3 | Migración **008**, `EstadoEta`, secuencia entrega, recálculo ETAs, matriz con celda nula | 4 PASS unitarios; 2 ERROR API | **Parcial** |
| **EN-001** | RNF-001 / RF-007 | 8 | Presupuesto 45 s, GA escalado, benchmark 150×15, `REPORTE_RENDIMIENTO_EN_001.md` | `test_solver_sla_en001.py` **4/4 PASS**; solución **válida** 150×15 no sistemática | **Parcial** |

**Total comprometido:** 34 SP.

**Acreditación:**

| Concepto | SP |
|----------|-----|
| *Done* (DoD global + criterios verificados) | **0** |
| Implementación en repo con validación pendiente / parcial | **34** (no equivale a cierre académico *Done*) |

---

## Criterios de aceptación (referencia)

Los escenarios BDD oficiales están en [01_transformando_a_agil_v_1_0_0.md](../../02%20Planificacion/01_transformando_a_agil_v_1_0_0.md) (US-005, US-007, US-008, US-009, EN-001). La matriz detallada **criterio × evidencia × prueba** figura en [VERIFICACION_FINAL_SPRINT_2.md](../../../VERIFICACION_FINAL_SPRINT_2.md) §11.

**Decisiones técnicas aprobadas en planificación** (no confundir con el backlog ágil literal): motor **genético propio** (no OR-Tools), `geometry` 4326 vs `GEOGRAPHY`, OSRM **opcional/apagado** por defecto — ver [PLAN_IMPLEMENTACION_SPRINT_2.md](../../../PLAN_IMPLEMENTACION_SPRINT_2.md) §7 y §14 (D-01, D-03, D-06).

---

## Pruebas ejecutadas (evidencia real)

| Corrida | Alcance | Resultado |
|---------|---------|-----------|
| Subconjunto Sprint 2 (sin PostGIS) | 49 tests (`test_solver`, US-005/007/008/009, EN-001, unitarios) | **34 passed**, **2 failed**, **13 errors** (setup BD) |
| Inventario total pytest | 114 tests | Suite completa **no ejecutada** sin PostGIS |
| Frontend Vitest | `npm run test:coverage` | **No ejecutado** (npm no disponible en host de verificación) |
| Regresión Sprint 1 | `test_api.py`, import, flota, etc. | **No re-ejecutada** en la misma sesión |

Comando documentado en [VERIFICACION_FINAL_SPRINT_2.md](../../../VERIFICACION_FINAL_SPRINT_2.md) §3.1.

---

## Métricas de rendimiento (EN-001)

| Métrica | Objetivo | Medido | Fuente |
|---------|----------|--------|--------|
| Tiempo solver 150×15 | ≤ 45 s | Media **~0,89 s** | [REPORTE_RENDIMIENTO_EN_001.md](../../../REPORTE_RENDIMIENTO_EN_001.md) §4.1 |
| Solución **válida** (factible dura) 150×15 | Sí (RNF-001) | `feasible=false` en 0/5 repeticiones sintéticas | Idem |
| Tiempo HTTP `POST /optimizar-rutas` | ≤ 45 s | **No medido** | Sin PostGIS en verificación |

---

## Problemas y acciones correctivas (resumen)

| Problema | Acción correctiva propuesta |
|----------|----------------------------|
| 13 tests de integración bloqueados sin PostGIS | Levantar `docker compose up -d db`; ejecutar `uv run pytest --cov=app` (114 tests) |
| 2 tests unitarios fallidos | Corregir fixtures en `test_precheck_volume_exact_and_over` y `test_infeasible_windows_not_marked_feasible` |
| Cobertura &lt; 80 % | Ampliar pruebas httpx en `routes.py` y capa import |
| EN-001 validez vs tiempo | Afinar instancia benchmark / GA manteniendo US-008 |
| DoD global (IMP-009 heredado) | CI verde, Sonar, PR, staging — ver Sprint 1 + [02_registro_de_impedimentos_v_1_0_0.md](02_registro_de_impedimentos_v_1_0_0.md) |

*Las acciones son **propuestas técnicas** salvo que el equipo las registre en acta.*

---

## Demostración y aprobaciones

**No** se registra en el repositorio una Sprint Review con fecha, asistentes o acta firmada. **No** se declara despliegue en staging verificado. Evidencias disponibles: código, migraciones 007–008, reportes en raíz del repo y corrida pytest parcial citada arriba.

---

## Pendientes para sprints futuros

1. Cierre DoD global (cobertura, Sonar/CodeQL, peer review, staging) — continúa **IMP-009** del Sprint 1.
2. **US-010 … US-012** (cartografía), **EN-004** (PWA offline), KPI RF-013/014 según roadmap en [03_revision_del_sprint_v_1_0_1.md](../03_revision_del_sprint_v_1_0_1.md).
3. GeoJSON distrital oficial (decisión **D-05** del plan Sprint 2) antes de filtro en producción.
4. Revalidación **IMP-004** / RNF-001 sobre GA con criterio “solución válida” cerrado.

---

## Referencias cruzadas

| Documento | Enlace |
|-----------|--------|
| Revisión Sprint 2 | [03_revision_del_sprint_v_1_0_0.md](03_revision_del_sprint_v_1_0_0.md) |
| Impedimentos Sprint 2 | [02_registro_de_impedimentos_v_1_0_0.md](02_registro_de_impedimentos_v_1_0_0.md) |
| Retrospectiva Sprint 2 (borrador) | [04_retrospectiva_del_sprint_v_1_0_0.md](04_retrospectiva_del_sprint_v_1_0_0.md) |
| Sprint 1 (sin modificar) | [01_informe_de_estado_del_proyecto_v_1_0_1.md](../01_informe_de_estado_del_proyecto_v_1_0_1.md) |
| DoD global | [01_transformando_a_agil_v_1_0_0.md](../../02%20Planificacion/01_transformando_a_agil_v_1_0_0.md) §2 |

---

[← Volver al README](../../../README.md)
