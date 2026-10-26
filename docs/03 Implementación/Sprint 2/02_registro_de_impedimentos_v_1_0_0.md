# 02. Registro de Impedimentos — Sprint 2 V_1_0_0.md

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

**Ámbito:** Impedimentos **nuevos o reabiertos** con impacto en el cierre del Sprint 2 (2026-10-26). Los registros **IMP-001 a IMP-009** del Sprint 1 permanecen en [02_registro_de_impedimentos_v_1_0_1.md](../Sprint%201/02_registro_de_impedimentos_v_1_0_1.md) **sin modificación retrospectiva**.

---

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **IMP-009** | 26/10/2026 | *(Heredado Sprint 1)* Brecha DoD: cobertura, Sonar, PR, staging. **Impacto Sprint 2:** las historias US-005…EN-001 no pueden declararse *Done* aunque el código esté escrito. | Alta | Verificación QA | 15/11/2026 | Abierto | — | Ver [REPORTE_VERIFICACION_DOD_SPRINT_1.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_VERIFICACION_DOD_SPRINT_1.md) y [VERIFICACION_FINAL_SPRINT_2.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md) §12. |
| **IMP-004** | 02/09/2026 | *(Reapertura documental)* SLA RNF-001 sobre **OR-Tools** vs **GA actual**. **Impacto Sprint 2:** tiempo solver ≤ 45 s **cumple** en benchmark; criterio “solución válida” 150×15 **no** cumple de forma sistemática en dataset sintético. | Crítica | Verificación técnica | 30/11/2026 | En revalidación | — | Evidencia: [REPORTE_RENDIMIENTO_EN_001.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_RENDIMIENTO_EN_001.md) §4.1; US-008 mitiga publicación ilegal vía HTTP 409. |
| **IMP-010** | 26/10/2026 | **Entorno PostGIS no disponible** en verificación local (Docker Desktop detenido; `ConnectionRefused` en `localhost:5433`). **Impacto:** 13 tests Sprint 2 y suite E2E (~58+ setups) no ejecutados; no hay evidencia de regresión Sprint 1 en la misma sesión. | Alta | Verificación QA | 10/11/2026 | Abierto | — | Mitigación: CI `.github/workflows/ci.yml` con servicio PostGIS; ejecutar `docker compose up -d db` antes de pytest en desarrollo. |
| **IMP-011** | 26/10/2026 | **Dos pruebas unitarias en rojo** en corrida focal: `test_precheck_volume_exact_and_over`, `test_infeasible_windows_not_marked_feasible`. **Impacto:** señal de calidad ambigua en CI si no se corrigen fixtures; no demuestra por sí solo fallo de producción (primer caso: escenario del test inconsistente). | Media | Verificación QA | 15/11/2026 | Abierto | — | Detalle en [VERIFICACION_FINAL_SPRINT_2.md](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md) §3.3. |
| **IMP-012** | 26/10/2026 | **Cobertura backend ~50 %** y frontend **sin medición** en verificación Sprint 2. **Impacto:** incumplimiento DoD §2.1; capa API (`routes.py`) con cobertura baja. | Alta | Verificación QA | 30/11/2026 | Abierto | — | Objetivo ≥ 80 % backend y frontend; archivar `coverage.xml` y `coverage/frontend/lcov.info`. |
| **IMP-013** | 26/10/2026 | **SonarQube / CodeQL no ejecutados** (job Sonar condicionado a `SONAR_ENABLED`; sin workflow CodeQL). **Impacto:** DoD §2.2 sin evidencia; no afirmar 0 vulnerabilidades críticas/altas. | Media | Verificación QA | 30/11/2026 | Abierto | — | `sonar-project.properties` preparado; requiere secretos y pipeline verde. |
| **IMP-005** | 03/09/2026 | *(Referencia)* RN-002 / RN-003 pendientes de validación normativa. **Impacto Sprint 2:** jornada 8 h se aplica en producto (US-008) aunque RN-003 siga marcada normativamente pendiente (decisión **D-04** del plan). | Media | PM / Legal | 12/09/2026 | Pendiente de Validación | — | Sin cambio; ver Sprint 1. |
| **IMP-006** | 04/09/2026 | *(Actualización de estado producto)* Geocodificación OSM imprecisa en periurbano. **Impacto Sprint 2:** US-005 mitiga con hitos, pin manual y `pendiente_validacion`; polígono distrital oficial (**D-05**) aún pendiente para producción. | Alta | Data / Backend | 15/12/2026 | Parcialmente mitigado | — | US-005 implementada; validación E2E pendiente (IMP-010). |

---

## Observaciones sobre la Gestión de Impedimentos (Sprint 2)

1. **IMP-010** bloquea la acreditación de criterios que exigen API + PostGIS (US-005 Esc. 1–2, US-007 409 E2E, US-009 recálculo).
2. **IMP-004** debe leerse junto con **EN-001**: cumplir el reloj no sustituye “solución válida” ni publicación sin pasar US-008.
3. Las resoluciones deben enlazar log de CI, commit o reporte versionado (directriz [00. Directrices y Auditoria V_1_0_3.md](../../01%20Inicio/00.%20Directrices%20y%20Auditoria%20V_1_0_3.md)).

---

[← Volver al README](../../../README.md) · [Informe Sprint 2](01_informe_de_estado_del_proyecto_v_1_0_0.md)
