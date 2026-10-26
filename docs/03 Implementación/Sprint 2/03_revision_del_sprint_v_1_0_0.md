# 03. Revisión del Sprint 2 V_1_0_0.md

# Revisión del sprint

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

**Sprint:** 2 — Geocodificación y motor de rutas

**Fecha de revisión documental:** 26 de octubre de 2026

**Nota:** este documento consolida el **resultado verificable** del incremento. **No** sustituye una Sprint Review presencial ni incluye lista de asistentes o minuta de demo si no existen en el repositorio.

---

## Resumen ejecutivo

| Indicador | Valor (evidencia repo 2026-10-26) |
|-----------|-------------------------------------|
| Alcance comprometido | **34 SP** (US-005, US-007, US-008, US-009, EN-001) |
| Implementación en código | **Avanzada** en las cinco historias |
| Criterios de aceptación | **Parcialmente cumplidos**; ver matriz abajo |
| DoD global §2 | **No cumplida** |
| Pruebas automatizadas | **34 PASS / 2 FAIL / 13 ERROR** (subset 49 tests, sin PostGIS) |
| EN-001 tiempo (solver) | **Cumple** ≤ 45 s; validez 150×15 **no sistemática** |

---

## Objetivo del sprint (recordatorio)

Endurecer geocodificación, restricciones duras, secuencia/ETA y SLA del motor, manteniendo regresión Sprint 1 — [PLAN_IMPLEMENTACION_SPRINT_2.md](../../../Auditorias-EcoLogistica/02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_2.md) §1.

---

## Matriz de historias del Sprint 2

Leyenda **estado final:** *Implementado* = entregable en repo; *Done (DoD)* = cumple los 5 criterios globales de calidad; *Parcial* = brechas de criterio o prueba.

| ID | Descripción (título) | SP | Criterios de aceptación (resumen BDD) | Evidencia técnica | Resultado de pruebas | Estado final | Pendientes |
|----|----------------------|-----|----------------------------------------|-------------------|----------------------|--------------|------------|
| **US-005** | Geocodificación y ubicación espacial (RF-005) | 5 | Esc. 1: coordenadas y mapa; Esc. 2: fuera de cobertura → pendiente validación, bloqueo en ruta | Migración **007**, `app/services/geocode.py`, `operating_area.py`, `order_location.py`, `PATCH` ubicación, `tests/test_geocode_us005.py` | 6 tests **ERROR** (BD) | **Implementada — validación pendiente** | E2E; polígono oficial D-05; tipo `geometry` vs doc `GEOGRAPHY` |
| **US-007** | Rutas sostenibles VRPTW + Green VRP (RF-007, RN-008) | 13 | Esc. 1: hasta 150×15, ventanas/capacidad, ahorro ≥15 % km y ≥10 % CO₂; Esc. 2: exceso flota → no factible detallado | `genetic_solver.py`, `optimize_routes` precheck/409, metadatos RN-008, filtro jornada, `tests/test_optimizer_us007.py` | 5 PASS; 2 ERROR API; 1 FAIL ventanas | **Parcial** | Umbrales Gold informativos (D-06); escenario 150×15 Gold; corregir test ventanas |
| **US-008** | Restricciones duras capacidad y jornada (RF-008, RN-003, RN-004) | 5 | Esc. 1: ≤100 % peso/volumen, ≤8 h; Esc. 2: rechazo 8,5 h / exceso | `app/services/route_constraints.py`, `validate_for_publication`, 409 en `routes.py`, `tests/test_hard_constraints_us008.py` | 9 PASS; 3 ERROR API; 1 FAIL precheck test | **Parcial** | E2E 409 sin persistir; RF infeliz “dividir carga” no verificado |
| **US-009** | Secuencia y ETA (RF-009, RN-005) | 3 | Esc. 1: orden 1…10 y ETA en ventana; Esc. 2: sin matriz → revisión, ETA nulo | Migración **008**, `eta_schedule.py`, `sequence_eta.py`, `routing_matrix.py`, `POST .../recalcular-etas`, `tests/test_eta_us009.py` | 4 PASS; 2 ERROR API | **Parcial** | OSRM local no desplegado (D-03); UI Sidebar no probada en esta verificación |
| **EN-001** | SLA generación ≤ 45 s (RNF-001) | 8 | Esc. 1: 150×15, T ≤ 45 s; Esc. 2: timeout → mejor factible | `optimizer_runtime.py`, presupuesto GA, `optimizer_benchmark.py`, `REPORTE_RENDIMIENTO_EN_001.md`, `tests/test_solver_sla_en001.py` | **4/4 PASS** (incl. slow) | **Parcial** | HTTP total no medido; `feasible=false` 150×15 sintético |

**Total:** 34 SP comprometidos. **0 SP** en estado *Done (DoD)*.

---

## Evidencias técnicas consolidadas

| Artefacto | Ubicación |
|-----------|-----------|
| Plan Sprint 2 | [PLAN_IMPLEMENTACION_SPRINT_2.md](../../../Auditorias-EcoLogistica/02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_2.md) |
| Verificación QA | [VERIFICACION_FINAL_SPRINT_2.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md) |
| Rendimiento EN-001 | [REPORTE_RENDIMIENTO_EN_001.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_RENDIMIENTO_EN_001.md) |
| Migraciones | `app/db/migrations.py` (`007_geocodificacion_pedido`, `008_eta_detalle_ruta`) |
| Tests dedicados | `tests/test_geocode_us005.py`, `test_optimizer_us007.py`, `test_hard_constraints_us008.py`, `test_eta_us009.py`, `test_solver_sla_en001.py` |
| CI | `.github/workflows/ci.yml` (**ejecución remota no verificada**) |

---

## Demostración del trabajo completado

**No** se adjunta acta, grabación ni URL de staging demostrada en el repositorio al 2026-10-26.

Evidencias **verificables** sustitutivas de narrativa de demo:

1. Inspección de código y anotaciones OpenAPI en `app/api/v1/routes.py`.
2. Corrida pytest parcial documentada en [VERIFICACION_FINAL_SPRINT_2.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md) §3.
3. Benchmark solver archivable vía `EN001_WRITE=1` y `tests/test_solver_sla_en001.py -m slow`.

---

## Definition of Done — estado al cierre documental Sprint 2

| # | Criterio DoD | Cumple |
|---|--------------|--------|
| 1 | Cobertura ≥ 80 % backend y frontend | **No** |
| 2 | Sonar/CodeQL 0 críticas/altas | **No verificado** |
| 3 | Peer review PR | **No verificado** |
| 4 | CI/CD staging exitoso | **No verificado** |
| 5 | OpenAPI + docstrings | **Parcial** (anotaciones presentes; smoke `/docs` pendiente) |

---

## Pendientes y backlog siguiente

1. Resolver **IMP-010**, **IMP-011**, **IMP-012**, **IMP-013** ([02_registro_de_impedimentos_v_1_0_0.md](02_registro_de_impedimentos_v_1_0_0.md)).
2. Cerrar brecha **IMP-009** (DoD Sprint 1) en paralelo al cierre de calidad Sprint 2.
3. **Sprint 3+:** US-010…US-012, EN-004, RF-013/014 según planificación ágil.

---

## Referencias

| Artefacto | Enlace |
|-----------|--------|
| Informe de estado Sprint 2 | [01_informe_de_estado_del_proyecto_v_1_0_0.md](01_informe_de_estado_del_proyecto_v_1_0_0.md) |
| Retrospectiva (borrador) | [04_retrospectiva_del_sprint_v_1_0_0.md](04_retrospectiva_del_sprint_v_1_0_0.md) |
| Sprint 1 (histórico) | [03_revision_del_sprint_v_1_0_1.md](../Sprint%201/03_revision_del_sprint_v_1_0_1.md) |
| Backlog / DoD | [01_transformando_a_agil_v_1_0_0.md](../../02%20Planificacion/01_transformando_a_agil_v_1_0_0.md) |

---

[← Volver al README](../../../README.md)
