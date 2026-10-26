# 01. Informe de estado del proyecto V_1_0_1.md

> **Control de versiones:** sustituye a `01_informe_de_estado_del_proyecto_v_1_0_0.md` (2026-10-26). La versión anterior reflejaba un cierre optimista no sustentado en la verificación DoD.

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

**Fecha de actualización:** 26 de octubre de 2026

**Evidencias de verificación:** [REPORTE_VERIFICACION_DOD_SPRINT_1.md](../../REPORTE_VERIFICACION_DOD_SPRINT_1.md), [PLAN_IMPLEMENTACION_SPRINT_1.md](../../PLAN_IMPLEMENTACION_SPRINT_1.md), suites en `tests/`.

---

## Estado general del Sprint 1 (Fundación, Flota y Pedidos)

| Dimensión | Estado |
|-----------|--------|
| **Implementación funcional en código** | Avanzada para el alcance comprometido (EN-003, US-001, US-002, US-003, US-004, US-006). |
| **Definition of Done global** (`docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` §2) | **No cumplida** al cierre documental de esta versión. |
| **Pruebas automatizadas E2E** | Escritas; ejecución integral **pendiente** de entorno PostGIS/CI verificado (ver reporte DoD). |
| **Cobertura ≥ 80 %** | **No alcanzada** en mediciones disponibles (~46–58 % backend parcial; frontend no medido). |

**Veredicto de gestión:** el Sprint 1 se considera **entregado en implementación**, con **validación de calidad y cierre DoD pendientes**. No se declara el 100 % de finalización del alcance comprometido (20 SP) en sentido *Done*.

---

## Historias y habilitadores — implementación vs validación

| ID | Trazado | Puntos | Implementación técnica | Pruebas (evidencia) | Estado documental |
|----|---------|--------|------------------------|---------------------|-------------------|
| **EN-003** | RNF-003 | 5 SP | JWT, bcrypt, RBAC, bitácora, tokens de seguimiento, middleware HTTPS boot, tests de seguridad | `test_security_en003.py`, `test_auth.py` — **no ejecutados E2E** sin BD en verificación 2026-10-26 | **Parcial** — TLS en runtime (nginx/cert) pendiente de despliegue |
| **US-001** | RF-001 | 3 SP | CRUD flota, modelo/rendimiento, migración, `Fleet.tsx` | `test_fleet_us001.py` — pendiente ejecución verde | **Implementado** — DoD pendiente |
| **US-002** | RF-002 / RN-002 | 2 SP | API/UI parametrización, RN-002 desactivada por defecto, filtro en optimizador si validada+activa | `test_plate_restriction_us002.py` | **Implementado** — validación **normativa** RN-002 sigue pendiente (IMP-005) |
| **US-003** | RF-003 | 2 SP | Estados Activo/Mantenimiento/Inactivo, historial, exclusión en rutas | `test_vehicle_state_us003.py` | **Implementado** — DoD pendiente |
| **US-004** | RF-004 | 5 SP | CSV + XLSX, límite 150, informe por fila, jornada | `test_import_us004.py`, `test_day.py` | **Implementado** — DoD pendiente |
| **US-006** | RF-006 / RN-005 | 3 SP | Ventanas en alta/import; `PATCH /api/v1/pedidos/{id}`; UI edición | `test_order_window_us006.py`, `test_api.py` | **Implementado** — DoD pendiente |

**Total comprometido:** 20 SP. **Acreditación DoD:** 0 SP en estado *Done* formal; 20 SP en estado *implementado / validación pendiente*.

---

## Demostración y evidencias disponibles

La versión **V_1_0_0** de este informe y de la revisión del sprint describían una *Sprint Demo* ante stakeholders y despliegue en staging **sin dejar trazabilidad verificable** en el repositorio analizado (2026-10-26).

En esta versión **no se reafirma** esa demostración. Evidencias **disponibles** en el repo:

- Ejecución local/manual de la aplicación (FastAPI `/docs`, frontend Vite).
- Suites automatizadas listadas en `REPORTE_VERIFICACION_DOD_SPRINT_1.md`.
- Pipeline CI definido en `.github/workflows/ci.yml` (**sin ejecución remota verificada** en la auditoría).

Cualquier minuta o acta de demo presencial debe adjuntarse aparte; no se inventa en este documento.

---

## Pendientes (backlog y cierre de calidad Sprint 1)

### Cierre DoD (bloqueantes)

1. Ejecutar `pytest` con PostGIS (`ecologistica_test`) y obtener suite **verde**.
2. Alcanzar cobertura **≥ 80 %** backend y frontend (DoD §2.1).
3. Ejecutar SonarQube o CodeQL y registrar Quality Gate (0 críticas/altas).
4. Pull Request con **peer review** documentado.
5. Pipeline CI exitoso y despliegue **staging** con credenciales configuradas.

### Producto (Sprint 2+)

* **US-005 (RF-005):** Geocodificación y ajuste fino espacial (complemento a importación).
* **US-007 … US-009, EN-001, EN-004:** según roadmap en revisión del sprint V_1_0_1.

---

## Referencias cruzadas

| Documento | Versión |
|-----------|---------|
| Revisión del Sprint | `03_revision_del_sprint_v_1_0_1.md` |
| Impedimentos | `02_registro_de_impedimentos_v_1_0_1.md` |
| Retrospectiva | `04_retrospectiva_del_sprint_V_1_0_1.md` |
| DoD global | `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` §2 |

---

[← Volver al README](../../README.md)
