# Actualización documental pre-Sprint 3

**Proyecto:** EcoLogística Huancayo  
**Fecha:** 26 de octubre de 2026  
**Alcance:** alineación documental posterior a la reorganización. No se modificaron archivos de código, dependencias, Docker, CI/CD, auditorías originales, bases de datos ni historias del backlog. No se ejecutaron pruebas.

## 1. Resultado

La documentación vigente distingue ahora entre el baseline de requisitos y arquitectura, el runtime identificable y la evidencia histórica de validación. El resultado no cambia el alcance del proyecto ni declara el cierre de Sprints 1 o 2: ambos conservan implementación funcional documentada, pero no cumplen la Definition of Done (DoD) global con la evidencia disponible.

## 2. Documentos revisados

### Auditorías y evidencia

- `01_Auditorias/AUDITORIA_01_ESTADO_REPOSITORIO.md`
- `01_Auditorias/AUDITORIA_02_DOCUMENTACION.md`
- `01_Auditorias/AUDITORIA_03_CODIGO_ARQUITECTURA.md`
- `01_Auditorias/AUDITORIA_04_ESTABILIDAD.md`
- `01_Auditorias/AUDITORIA_MAESTRA_PRE_SPRINT_3.md`
- `02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_1.md`
- `02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_2.md`
- `03_Reportes_Verificacion/REPORTE_VERIFICACION_DOD_SPRINT_1.md`
- `03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md`
- `03_Reportes_Verificacion/REPORTE_RENDIMIENTO_EN_001.md`
- `04_Informes_CI/REPORTE_AUDITORIA_CI.md`

### Documentación de proyecto y contraste técnico

- `README.md`, `docs/ESTADO_TECNICO_VIGENTE.md` y documentos de inicio 00 a 13.
- `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` y planificación relacionada.
- Los ocho documentos de cierre de Sprint 1 y Sprint 2.
- Configuración y estructura activa sólo para contraste: `app/`, `src/`, `tests/`, `docker-compose.yml`, Dockerfiles, manifiestos y workflow CI.

## 3. Documentos modificados en esta actualización

| Documento | Cambio realizado | Motivo |
|---|---|---|
| `README.md` | Sustituye la presentación de PWA como capacidad entregada por estado verificable; enlaza al estado técnico vigente | Evita afirmar offline/IndexedDB/Service Workers sin evidencia. |
| `docs/01 Inicio/00. Directrices y Auditoria V_1_0_3.md` | Registra la coexistencia legítima de versiones históricas, corrige el catálogo de nombres reales y separa baseline de runtime | Resuelve M-05/M-06 sin renombrar o reescribir el historial. |
| `docs/01 Inicio/10. Stack tecnológico V_1_0_3.md` | Recalifica OR-Tools/DEAP, Redis/Celery, OSRM y PWA como planificación; enlaza el estado vigente | Evita presentarlos como runtime activo. |
| `docs/01 Inicio/11. Base de datos V_1_0_3.md` | Corrige enlace a estado vigente y conserva explícita la diferencia `GEOGRAPHY` previsto / `geometry` 4326 documentado | Mantiene la decisión pendiente visible. |
| `docs/01 Inicio/12. Modelo C4 V_1_0_6.md` | Corrige enlace a estado vigente | Mantiene los diagramas como arquitectura prevista, no como inventario de runtime. |
| `docs/03 Implementación/Sprint 2/04_retrospectiva_del_sprint_v_1_0_0.md` | Sustituye la referencia textual a reportes en raíz por su ubicación reorganizada | Corrige la última referencia narrativa detectada a la ubicación anterior. |

Los cambios de enlaces previos en README y documentos S1/S2, así como la creación de `docs/ESTADO_TECNICO_VIGENTE.md`, se encontraron ya presentes en el árbol de trabajo como parte de la reorganización. Esta actualización los conserva y los usa como fuente de estado, sin alterar las cinco auditorías originales.

## 4. Enlaces y referencias corregidos

| Referencia | Estado |
|---|---|
| README → informes y planes S1/S2 | Apunta a `Auditorias-EcoLogistica/02_Planes_Implementacion/` y `03_Reportes_Verificacion/`. |
| Sprint 1 → README e informes | Usa el ascenso de tres niveles y los nuevos destinos. |
| Sprint 2 → planes e informes | Usa rutas centralizadas bajo `Auditorias-EcoLogistica/`. |
| Retrospectiva S2 → reportes de verificación | Referencia narrativa actualizada desde raíz a `03_Reportes_Verificacion/`. |
| Stack, BD y C4 → estado técnico | Enlaces relativos corregidos a `docs/ESTADO_TECNICO_VIGENTE.md`. |

Los enlaces con nombres acentuados se contrastaron contra los archivos Unicode existentes. La comprobación automática de consola Windows puede emitir falsos positivos por codificación; no se interpretaron como enlaces rotos sin contraste de ruta real.

## 5. Contradicciones documentales resueltas y preservadas

| Tema | Resolución documental | Estado |
|---|---|---|
| OR-Tools/DEAP vs GA propio | OR-Tools/DEAP se mantienen como selección/evaluación histórica; GA propio es el motor implementado | Resuelto documentalmente. |
| Redis/Celery | Se distinguen como servicios planificados, no activos | Resuelto documentalmente. |
| OSRM | Se mantiene como alternativa prevista/opcional; no se presenta como desplegado | Resuelto documentalmente. |
| PWA offline | La vista React de conductor no se equipara a PWA offline/IndexedDB/Service Workers | Resuelto documentalmente. |
| `GEOGRAPHY` vs `geometry` 4326 | Se preserva el diseño original y se marca la decisión arquitectónica como pendiente | Pendiente de decisión. |
| Versiones documentales | Directrices catalogan nombres reales y preservan versión histórica | Resuelto para navegación; historial heterogéneo preservado. |
| Informes S1/S2 vs DoD | Se mantiene explícito que implementación no equivale a *Done* | Resuelto documentalmente; evidencia técnica pendiente. |

## 6. Matriz de estado — Sprint 1

| Historia/requisito | Funcionalidad | Estado de implementación | Evidencia disponible | Validación acreditada | Limitaciones pendientes |
|---|---|---|---|---|---|
| EN-003 / RNF-003 | JWT, bcrypt, RBAC, bitácora y seguimiento por token | PARCIAL | Código auth/acceso, `test_auth.py`, `test_security_en003.py`, reporte DoD S1 | Diseño y pruebas dedicadas documentadas; no E2E PostGIS acreditado | TLS/WSS en runtime, TTL/documentación JWT, análisis de seguridad y DoD. |
| US-001 / RF-001 | Gestión de flota | IMPLEMENTADO | API/UI, migraciones, `test_fleet_us001.py`, `test_day.py` | Implementación estática y pruebas listadas | Ejecución integral, cobertura y DoD. |
| US-002 / RF-002/RN-002 | Restricción por placa parametrizable | IMPLEMENTADO | Router/UI/optimizador, `test_plate_restriction_us002.py` | Implementación documentada | Validación normativa RN-002 y E2E. |
| US-003 / RF-003 | Estado operativo e historial de vehículo | IMPLEMENTADO | Servicio/UI, `test_vehicle_state_us003.py` | Implementación documentada | Suite verde y DoD. |
| US-004 / RF-004 | Importación CSV/XLSX de pedidos | IMPLEMENTADO | Servicio/UI, `test_import_us004.py`, `test_day.py` | Implementación documentada | E2E y cobertura. |
| US-006 / RF-006/RN-005 | Ventanas horarias de entrega | IMPLEMENTADO | Servicio/API/UI, test backend y `src/lib/orderWindow.test.ts` | Implementación documentada | Ejecución Vitest/CI, cobertura frontend y DoD. |

**Estado Sprint 1:** 20 SP implementados o en validación pendiente; **0 SP acreditados como Done** bajo la DoD global. La evidencia histórica no acredita E2E PostGIS, cobertura ≥80 %, análisis estático/seguridad, peer review ni staging.

## 7. Matriz de estado — Sprint 2

| Historia/requisito | Funcionalidad | Estado de implementación | Evidencia disponible | Validación acreditada | Limitaciones pendientes |
|---|---|---|---|---|---|
| US-005 / RF-005 | Geocodificación, área operativa y ubicación | IMPLEMENTADO — validación pendiente | Migración 007, servicios de geocodificación/área, `test_geocode_us005.py` | Código revisado | Pruebas API/PostGIS, polígono oficial y decisión espacial. |
| US-007 / RF-007/RN-008 | Optimización GA y línea base ambiental | PARCIAL | Solver, precheck 409, tests y verificación S2 | Pruebas unitarias parciales documentadas | Factibilidad, fixture de ventanas, E2E y métricas Gold no acreditadas. |
| US-008 / RF-008/RN-003/RN-004 | Restricciones duras de capacidad y jornada | PARCIAL | Validador/publicación, HTTP 409, `test_hard_constraints_us008.py` | Pruebas parciales documentadas | API/PostGIS, persistencia/no publicación y caso de división de carga. |
| US-009 / RF-009/RN-005 | Secuencia, ETA y recálculo | PARCIAL | Migración 008, servicios ETA, `test_eta_us009.py` | Pruebas puras documentadas | Endpoints con BD, UI y OSRM no desplegado. |
| EN-001 / RNF-001 | SLA generación de rutas | PARCIAL | Benchmark y `test_solver_sla_en001.py`; reporte EN-001 | Tiempo interno del solver ~0,89 s histórico; 4/4 pruebas reportadas | Factibilidad constante 150×15 y tiempo HTTP total no acreditados. |

**Estado Sprint 2:** 34 SP comprometidos; **0 SP acreditados como Done** bajo la DoD global. Los resultados de prueba anteriores se reportan como históricos; esta actualización no ejecutó pruebas ni genera evidencia nueva.

## 8. Estado de la Definition of Done

| Criterio DoD global | Estado verificable |
|---|---|
| Cobertura backend y frontend ≥80 % | NO CUMPLIDA / no acreditada; configuración backend permite fallar con umbral 0. |
| Suite automatizada E2E PostGIS verde | NO VERIFICADA; la evidencia S1/S2 registra ausencia de entorno PostGIS durante auditoría. |
| Análisis estático, seguridad y calidad | NO VERIFICADO; Sonar condicional, sin evidencia de CodeQL/OWASP/SCA ejecutados. |
| Peer review/PR trazable | NO VERIFICADO. |
| CI/CD y staging exitosos | NO VERIFICADO; job staging es placeholder. |

**Veredicto DoD:** no cumplida para Sprint 1 ni Sprint 2.

## 9. Limitaciones funcionales y técnicas

- Pruebas que usan base de datos modifican `ecologistica_test`; no se ejecutaron.
- TLS/WSS productivo no está acreditado; Compose expone HTTP y `FORCE_HTTPS=false` por defecto.
- La migración propia no se ha validado aquí en upgrade real; no se usa Alembic.
- Persisten acoplamientos entre WebSocket/rutas HTTP y ETA/privados del solver, además de cálculo duplicado de CO2.
- `pyproject.toml`/`uv.lock` y `backend/requirements.txt` siguen siendo fuentes Python paralelas; Docker/CI instalan requirements con herramientas de QA.
- Cobertura frontend limitada a `src/lib/**/*.ts`; no hay evidencia de cobertura adecuada de UI.

## 10. Dependencias documentales para Sprint 3

| Historia prevista | Dependencias conocidas que deben respetarse |
|---|---|
| US-010 | Rutas publicadas, geometrías y autenticación/roles; no presupone OSRM activo. |
| US-011 | Secuencia/ETA de US-009 y contrato de datos de ruta; integración UI no acreditada aún. |
| US-012 / RF-012/RNF-004 | Debe proveer vista tabular resiliente; no equivale a implementar PWA offline. |
| US-013 a US-015 | Métricas ambientales y línea base de US-007; primero definir fuente única de CO2 y datos factibles. |
| EN-004 | Es backlog futuro: IndexedDB/PWA/sincronización no está entregado ni debe declararse heredado de S1/S2. |

Antes de declarar una historia S3 *Done* deben definirse los criterios de evidencia y mantenerse separadas las decisiones de producto de las brechas heredadas de DoD.

## 11. Inconsistencias pendientes

1. Decisión arquitectónica formal `geometry` SRID 4326 frente a `GEOGRAPHY` del diseño base.
2. Validación normativa de RN-002 y delimitación/polígono operativo oficial.
3. Reconciliación de la estrategia de dependencias Python y bloqueo efectivo de versiones.
4. Unificación del cálculo de emisiones y reducción de acoplamientos internos antes de cambios que afecten optimización/ETA/realtime.
5. Ejecución verificable de CI, cobertura, seguridad, staging y E2E PostGIS.
6. Consolidación en Git de la reorganización: al momento de la consulta hay orígenes como eliminados y destinos reorganizados sin seguimiento.

## 12. Resultado de `git diff --stat`

Consulta realizada al finalizar las actualizaciones documentales (antes de añadir archivos no rastreados al índice):

```text
29 files changed, 82 insertions(+), 1984 deletions(-)
```

El resultado incluye la reorganización previa: eliminación del prototipo `EcologisticaJunin/`, eliminación de los antiguos archivos raíz y modificaciones de documentos/enlaces. `git diff --stat` no enumera los destinos nuevos no rastreados, incluido este informe; por ello no debe interpretarse como pérdida de los planes o reportes que ahora existen bajo `Auditorias-EcoLogistica/`.

## Conclusión

La documentación queda alineada con el estado verificable conocido: requisitos y decisiones históricas preservados, runtime identificado sin tecnologías planificadas presentadas como activas y limitaciones visibles. Sprint 3 puede planificarse contra esta línea base, pero no debe asumir cierre DoD de Sprints 1/2, PWA offline, OSRM/Redis/Celery desplegados, TLS productivo ni EN-001 integralmente validado.
