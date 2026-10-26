# 03. Revisión del Sprint V_1_0_1.md

> **Control de versiones:** sustituye a `03_revision_del_sprint_v_1_0_0.md` (2026-10-26). La V_1_0_0 declaraba 100 % SP y DoD cumplida; esta versión alinea el acta con el código y con [REPORTE_VERIFICACION_DOD_SPRINT_1.md](../../REPORTE_VERIFICACION_DOD_SPRINT_1.md).

# Revisión del sprint

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

**Sprint:** 1 — Fundación, Flota y Pedidos

**Fecha de revisión documental:** 26 de octubre de 2026

---

## Resumen ejecutivo

| Indicador | V_1_0_0 (histórico) | V_1_0_1 (evidencia repo) |
|-----------|---------------------|---------------------------|
| Alcance comprometido | 20 SP | 20 SP (sin cambio) |
| Implementación en código | Declarada completa | **Avanzada** para las 6 historias del alcance |
| DoD global §2 | Declarada cumplida | **No cumplida** (cobertura, Sonar, PR, staging) |
| Suite automatizada | No detallada | **Escrita**; ejecución E2E **no verificada** sin PostGIS/CI |
| Sprint Demo en staging | Narrativa detallada | **No reafirmada** — ver § Demostración |

---

## Matriz de historias del Sprint 1

Leyenda de **estado final:** *Implementado* = entregable técnico en repo; *Done (DoD)* = cumple los 5 criterios globales de calidad.

| ID | Descripción (título) | SP | Criterios de aceptación (resumen trazable) | Evidencia técnica | Resultado de pruebas | Estado final | Pendientes |
|----|----------------------|-----|-------------------------------------------|-------------------|----------------------|--------------|------------|
| **EN-003** | Seguridad transversal, JWT, RBAC, seguimiento por token (RNF-003) | 5 | BDD EN-003 (HTTPS/TLS, hash, JWT, RBAC auditor); RN-001 bloqueo 3 intentos | `app/api/v1/auth.py`, `app/services/access.py`, `app/services/passwords.py`, `app/services/tokens.py`, `app/services/tracking_tokens.py`, `app/middleware/https_redirect.py`, `app/core/security_boot.py`, `tests/test_auth.py`, `tests/test_security_en003.py` | Suite **no ejecutada E2E** (58 errores setup sin PostGIS); lógica parcial cubierta en diseño de tests | **Implementado parcial** — no *Done* | TLS 1.3 en **runtime** (nginx/cert prod); alinear JWT doc (**15 min**) vs `auth_token_hours=12`; Sonar/OWASP; revisar endpoints públicos |
| **US-001** | Registro y mantenimiento de flota (RF-001) | 3 | BDD US-001 + RF-001 (CRUD, capacidad, combustible, RN-006) | `app/models/domain.py`, desk/flota API, `src/pages/Fleet.tsx`, migraciones/init | `test_fleet_us001.py`, `test_day.py` — no verde en auditoría | **Implementado** — no *Done* | Ejecutar tests + cobertura API flota |
| **US-002** | Restricciones por placa (RF-002 / RN-002) | 2 | Parametrización por dígito/distrito; **no activar** sin validación normativa | `app/models/restrictions.py`, `plate_restrictions` router, optimizador, `PlateRestrictions.tsx` | `test_plate_restriction_us002.py` | **Implementado** — no *Done* | **IMP-005:** validación legal RN-002; pruebas E2E verdes |
| **US-003** | Estado operativo vehículo (RF-003) | 2 | Activo/Mantenimiento/Inactivo, historial, exclusión en rutas | `app/services/vehicle_state.py`, `EstadoOperativoVehiculo`, `Fleet.tsx` | `test_vehicle_state_us003.py` | **Implementado** — no *Done* | Suite verde + DoD |
| **US-004** | Importación masiva pedidos (RF-004) | 5 | CSV/XLSX, máx. 150, informe por fila, jornada | `app/services/order_import.py`, `OrdersDay.tsx`, `DayImport` | `test_import_us004.py`, `test_day.py` | **Implementado** — no *Done* | US-005 (geocodificación RF-005) en backlog |
| **US-006** | Ventanas de entrega (RF-006 / RN-005) | 3 | Ventanas en alta/import; edición vía PATCH antes de ruta | `app/services/order_window.py`, `PATCH /api/v1/pedidos/{id}`, UI | `test_order_window_us006.py`, `test_api.py`, `src/lib/orderWindow.test.ts` | **Implementado** — no *Done* | Ejecutar vitest en CI; cobertura FE |

**Total:** 20 SP comprometidos. **0 SP** en estado *Done (DoD)*; **20 SP** en *implementado / validación pendiente*.

---

## Demostración del trabajo completado

### Registro histórico (V_1_0_0)

La revisión **V_1_0_0** describió una *Sprint Demo* en staging con escenarios de fuerza bruta, RBAC auditor, flota, importación de 150 pedidos y restricciones por placa. Ese texto se **conserva como acta académica previa** pero **no constituye evidencia verificable** en el repositorio al 2026-10-26 (sin artefactos de despliegue, grabación ni acta firmada adjunta).

### Evidencia verificable disponible (2026-10-26)

1. **Inspección de código y OpenAPI:** endpoints de auth, flota, jornada/import, restricciones-placa, PATCH pedidos registrados en routers FastAPI (`/docs`).
2. **Pruebas automatizadas:** inventario en `REPORTE_VERIFICACION_DOD_SPRINT_1.md` §3; 13 tests pasaron sin BD; integración pendiente de PostGIS.
3. **CI definida:** `.github/workflows/ci.yml` (backend + frontend + Sonar opcional + job staging manual) — **ejecución remota no verificada** en la auditoría.

**Observación:** cualquier demostración presencial posterior debe documentarse con fecha, ambiente y asistentes en anexo; no se sustituye por este párrafo.

---

## Pendientes

### Cierre de calidad Sprint 1 (DoD)

Ver [REPORTE_VERIFICACION_DOD_SPRINT_1.md](../../REPORTE_VERIFICACION_DOD_SPRINT_1.md) §11 y impedimento **IMP-009** en `02_registro_de_impedimentos_v_1_0_1.md`.

### Backlog de producto (sin cambio de alcance Sprint 1)

1. **Sprint 2 (Algoritmos y Motor de Optimización):**
   * **US-005 (RF-005):** Geocodificación y ubicación espacial con PostGIS. *(5 SP)*
   * **US-007 (RF-007 / RN-008):** Rutas sostenibles VRPTW + Green VRP. *(13 SP)*
   * **US-008 (RF-008 / RN-003 / RN-004):** Restricciones duras capacidad y jornada 8 h. *(5 SP)*
   * **US-009 (RF-009):** Secuencia de paradas y ETA. *(3 SP)*
   * **EN-001 (RNF-001):** SLA ≤ 45 s (150 pedidos / 15 vehículos). *(8 SP)*

2. **Sprint 3 (Cartografía, PWA, Sostenibilidad):** US-010 … US-015, EN-004.

3. **Sprint 4 (Reportes, Re-optimización, Cierre MVP):** US-016 … US-018, EN-002.

---

## Referencias

| Artefacto | Enlace |
|-----------|--------|
| Informe de estado | `01_informe_de_estado_del_proyecto_v_1_0_1.md` |
| Impedimentos | `02_registro_de_impedimentos_v_1_0_1.md` |
| Retrospectiva | `04_retrospectiva_del_sprint_V_1_0_1.md` |
| Plan de implementación | [PLAN_IMPLEMENTACION_SPRINT_1.md](../../PLAN_IMPLEMENTACION_SPRINT_1.md) |
| DoD | `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` §2 |

---

[← Volver al README](../../README.md)
