# Retrospectiva del Sprint 2

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Versión:** V_1_0_0 (SemVerDoc — borrador técnico post-verificación, 2026-10-26)

**Sprint:** 2 — Geocodificación y motor de rutas

---

## Aviso sobre la ceremonia

**No consta en el repositorio** evidencia de una retrospectiva Scrum celebrada con el equipo (fecha, participantes, votación, compromisos firmados). El presente documento es un **borrador preparado a partir de hallazgos técnicos** en [VERIFICACION_FINAL_SPRINT_2.md](../../../VERIFICACION_FINAL_SPRINT_2.md), [REPORTE_RENDIMIENTO_EN_001.md](../../../REPORTE_RENDIMIENTO_EN_001.md) y el plan de implementación.

**Pendiente:** validación, enriquecimiento y aprobación por el equipo en sesión de retrospectiva real.

---

## 1. ¿Qué aprendimos? (observaciones técnicas)

- Separar **SLA de tiempo** (EN-001) de **solución publicable** (US-008) evita declarar RNF-001 cumplido solo porque el GA termina en &lt; 1 s; el benchmark 150×15 mostró `feasible=false` con ventanas sintéticas.
- Las **restricciones duras fuera del fitness** (`route_constraints`) son el mecanismo correcto para alinear RF-008 con HTTP 409; la validación E2E sigue dependiendo de PostGIS (IMP-010).
- **US-005** desacopla elegibilidad del optimizador (`pendiente_validacion`) sin reescribir el GA — coherente con el orden del plan Sprint 2.
- Mantener **decisiones explícitas** (D-01…D-08 en plan) reduce conflicto entre documentos de arquitectura (OR-Tools/OSRM/GEOGRAPHY) y el código real.
- Dos tests en rojo por **fixtures inconsistentes** muestran que el gate “suite verde” debe preceder actas de cierre (IMP-011).
- La **DoD global** del Sprint 1 (IMP-009) sigue bloqueando el cierre académico *Done* del Sprint 2 aunque el incremento funcional sea grande.

---

## 2. ¿Qué estamos haciendo bien?

- Trazabilidad **historia → módulo → test** (`test_*_us005.py`, `test_hard_constraints_us008.py`, etc.).
- Reportes de verificación y rendimiento en raíz del repo (`VERIFICACION_FINAL_SPRINT_2.md`, `REPORTE_RENDIMIENTO_EN_001.md`) separados de actas académicas.
- Migraciones versionadas **007** y **008** alineadas con US-005 y US-009.
- Motor genético con presupuesto de tiempo y parámetros escalados (`optimizer_runtime.py`).
- Documentación Sprint 1 preservada (V_1_0_1) sin reescritura retrospectiva.

---

## 3. ¿Qué podemos hacer mejor?

### 3.1 Personas

- Acordar **quién** ejecuta pytest con PostGIS antes de cada cierre de sprint (evitar depender de un único entorno local).

### 3.2 Relaciones

- Alinear expectativas académicas (texto BDD con OR-Tools / OSRM / umbrales 15 %–10 %) con **decisiones de planificación** documentadas, sin presentarlas como incumplimiento no discutido.

### 3.3 Procesos

- Gate de cierre: **114 tests verdes** + cobertura archivada + enlace CI antes de versionar actas al 100 %.
- Corregir tests fallidos en la misma iteración que introducen regresiones de fixture.

### 3.4 Herramientas

- Documentar en README el prerrequisito Docker para integración (refuerzo de propuesta P-01 Sprint 1).
- Ejecutar Vitest en CI para cambios de UI (`OrdersDay`, `Sidebar`) ligados a US-005/US-009.

---

## 4. Propuestas de mejora (borrador — no aprobadas)

*Las filas siguientes son **propuestas técnicas** para discusión en retrospectiva; **no** constituyen compromisos del equipo hasta validación explícita.*

| # | Propuesta | Responsable sugerido | Fecha objetivo sugerida | Resultado verificable |
|---|-----------|----------------------|-------------------------|------------------------|
| P2-01 | Ejecutar suite completa pytest con PostGIS y archivar log | Backend / QA | 10/11/2026 | 114 tests PASS + artefacto CI |
| P2-02 | Corregir IMP-011 (dos tests unitarios) | Backend | 10/11/2026 | PR con tests verdes |
| P2-03 | Medir EN-001 Esc. 1 **HTTP** 150×15 con BD | Backend | 20/11/2026 | Tiempo en informe + 409 si infactible |
| P2-04 | Ajustar benchmark / GA para factibilidad 150×15 manteniendo US-008 | Backend | 30/11/2026 | `feasible=true` en ≥1 repetición documentada |
| P2-05 | Subir cobertura `routes.py` / import hacia DoD 80 % | Backend / QA | 30/11/2026 | `coverage.xml` |
| P2-06 | Importar GeoJSON distrital con fuente (D-05) | Data / PM | 15/12/2026 | Archivo versionado + criterio US5-I prod |
| P2-07 | Cerrar IMP-009 (Sonar, PR, staging) en paralelo | DevOps / PM | 30/11/2026 | Enlaces en informe de estado |

---

## 5. Riesgos residuales (Sprint 2)

| Riesgo | Mitigación en repo | Residual |
|--------|-------------------|----------|
| Publicación de ruta infactible | HTTP 409 + `validate_for_publication` | No probado E2E |
| Regresión Sprint 1 al cambiar optimizador | Tests `test_api.py`, `test_solver.py` | No ejecutados con BD |
| Desalineación doc OR-Tools vs GA | Plan y reportes EN-001 | Comunicación a evaluadores |
| Cobertura insuficiente en API | Tests nuevos Sprint 2 | IMP-012 |

---

## 6. Enlaces

- [Informe de estado Sprint 2](01_informe_de_estado_del_proyecto_v_1_0_0.md)
- [Revisión del Sprint 2](03_revision_del_sprint_v_1_0_0.md)
- [Impedimentos Sprint 2](02_registro_de_impedimentos_v_1_0_0.md)
- [Verificación integral Sprint 2](../../../VERIFICACION_FINAL_SPRINT_2.md)
- [Retrospectiva Sprint 1](../04_retrospectiva_del_sprint_V_1_0_1.md) *(sin modificar)*

---

[← Volver al README](../../../README.md)
