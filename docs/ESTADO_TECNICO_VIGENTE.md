# Estado técnico vigente y trazabilidad pre-Sprint 3

**Fecha de consolidación:** 26 de octubre de 2026. Este documento distingue el estado real de las propuestas históricas; no sustituye requisitos, planes ni evidencias originales.

## Fuentes de verdad

| Dominio | Fuente primaria |
|---|---|
| Requisitos y reglas | Documentos 06, 07 y 09 de `docs/01 Inicio/` |
| Backlog, BDD y DoD | `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` |
| Arquitectura implementada | `app/`, `src/`, `docker-compose.yml`, `package.json`, `pyproject.toml` |
| Evidencia S1 | `Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_VERIFICACION_DOD_SPRINT_1.md` |
| Evidencia S2 | `Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md` |
| Rendimiento EN-001 | `Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_RENDIMIENTO_EN_001.md` |

## Arquitectura prevista frente a implementada

| Tema | Previsto históricamente | Implementado/verificado | Estado |
|---|---|---|---|
| Optimización | OR-Tools/DEAP | Algoritmo genético propio en `app/services/genetic_solver.py`. | IMPLEMENTADO; desviación documentada. |
| Geodatos | `GEOGRAPHY` PostGIS | `geometry` SRID 4326 según implementación y verificación S2. | PARCIAL; decisión pendiente. |
| OSRM | Servicio local | Opcional, apagado por defecto y ausente de Compose. | PENDIENTE / opcional. |
| Redis/Celery | Tareas asíncronas | No declarados como servicios o dependencias activos. | PENDIENTE. |
| PWA offline | IndexedDB y Service Workers | No hay evidencia reproducible de entrega. | NO VERIFICADO. |
| Seguridad | JWT, RBAC y TLS | JWT/RBAC/bcrypt presentes; TLS productivo no acreditado. | PARCIAL. |

## Matriz de trazabilidad

| Requisito | Historia | Sprint | Implementación | Evidencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| RF-001 a RF-004, RF-006 | US-001 a US-004, US-006 | 1 | Flota, placa, estados, importación y ventanas en `app/`. | Reporte DoD S1 y suites dedicadas. | IMPLEMENTADO | E2E PostGIS/DoD global no acreditados. |
| RNF-003 | EN-003 | 1 | JWT, bcrypt, RBAC, bloqueo e historial. | Reporte DoD S1. | PARCIAL | TLS y validación integral pendientes. |
| RF-005 | US-005 | 2 | Geocodificación, área operativa y PATCH de ubicación. | Verificación S2. | IMPLEMENTADO | Pruebas API/PostGIS no acreditadas. |
| RF-007 | US-007 | 2 | Solver GA, baseline y metadatos ambientales. | Verificación S2 y EN-001. | PARCIAL | Factibilidad E2E pendiente. |
| RF-008 | US-008 | 2 | Capacidad, jornada, ventanas y 409. | Verificación S2. | PARCIAL | Persistencia/no publicación requiere E2E. |
| RF-009 | US-009 | 2 | Secuencia, ETA y recálculo. | Verificación S2. | PARCIAL | Integración/UI no acreditadas. |
| RNF-001 | EN-001 | 2 | Presupuesto y benchmark 150×15. | Reporte EN-001. | PARCIAL | Tiempo solver cumple; factibilidad constante y HTTP total no. |
| RF-010 a RF-015 / EN-004 | US-010 a US-015 / EN-004 | 3 | Fuera de evidencia S1/S2. | Backlog y auditorías. | PENDIENTE | No declarar PWA offline ni indicadores como terminados. |

## Condiciones de preparación

El cierre formal requiere suite E2E PostGIS, evidencia de cobertura conforme a DoD o revisión formal del umbral, análisis de seguridad, CI/staging verificables y medición HTTP/factibilidad válida de EN-001. Estas condiciones no impiden desarrollo funcional aislado de Sprint 3; delimitan evidencia pendiente.
