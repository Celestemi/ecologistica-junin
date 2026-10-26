# Verificación integral — Sprint 2 (QA / auditoría técnica)

**Proyecto:** EcoLogística Huancayo — DistriRápido S.A.C.  
**Fecha de verificación:** 2026-10-26  
**Alcance:** US-005, US-007, US-008, US-009, EN-001 (+ regresión Sprint 1 y DoD global)  
**Auditor:** agente QA (revisión de código + pruebas ejecutadas en entorno local)  
**Restricciones respetadas:** no se modificaron informes oficiales de cierre del sprint; no commits ni push.

---

## 1. Resumen ejecutivo

| Historia | Clasificación global |
|----------|----------------------|
| **US-005** | **Implementada, pendiente de validación** (código + migración 007; pruebas API no ejecutadas por ausencia de PostGIS) |
| **US-007** | **Parcial** (precheck 409, jornada, metadatos RN-008 en código; umbrales Gold 15 %/10 % informativos; 1 prueba unitaria rota por fixture) |
| **US-008** | **Parcial** (validador duro + 409 en API; 1 prueba de precheck volumétrico falla por escenario del test; integración API sin ejecutar) |
| **US-009** | **Parcial** (ETA, estados, recálculo en código; pruebas puras OK; endpoints con BD sin ejecutar) |
| **EN-001** | **Parcial** (SLA de **tiempo** cumplido en benchmark solver; **solución válida** 150×15 no sistemática; HTTP total no medido) |

**DoD global del proyecto:** **no cumplida** en esta verificación (cobertura &lt; 80 %, suite E2E incompleta, Sonar/CodeQL no ejecutado, peer review y staging no verificados).

---

## 2. Entorno y limitaciones de la verificación

| Elemento | Estado | Evidencia |
|----------|--------|-----------|
| PostGIS / Docker | **No disponible** | `docker compose up -d db` → daemon Docker Desktop no en ejecución (`npipe://...dockerDesktopLinuxEngine`) |
| Conexión BD pruebas | **Rechazada** | `ConnectionRefusedError` en `localhost:5433` al usar fixture `client` / `database` |
| Python | 3.14.8 (`uv run pytest`) | Corrida parcial 2026-10-26 |
| Node / Vitest frontend | **No ejecutado** | `npm` no disponible en PATH del host |
| GitHub Actions (`gh`) | **No consultado** | CLI `gh` no instalada; estado del pipeline remoto **no verificado** |
| SonarQube / CodeQL | **No ejecutado** | Job CI condicionado a `vars.SONAR_ENABLED == 'true'`; sin token ni scan local |

**Aislamiento de datos de prueba (control Sprint 1):** **verificado por revisión estática** — `tests/conftest.py` fuerza `DATABASE_URL` → `ecologistica_test` y aborta si el nombre de BD no coincide. **No se pudo confirmar** TRUNCATE/semilla en runtime al no haber servidor PostgreSQL.

---

## 3. Ejecución de pruebas (evidencia real)

### 3.1 Corrida focal Sprint 2 (sin PostGIS)

Comando:

```text
uv run pytest tests/test_solver.py tests/test_hard_constraints_us008.py tests/test_optimizer_us007.py \
  tests/test_solver_sla_en001.py tests/test_unit_services.py tests/test_geocode_us005.py tests/test_eta_us009.py -v
```

| Métrica | Resultado |
|---------|-----------|
| Recolectados | 49 |
| **Passed** | **34** |
| **Failed** | **2** |
| **Errors (setup BD)** | **13** |
| Duración | ~17 s |
| Cobertura backend (`app/`) en esa corrida | **50 %** líneas (`coverage.xml`, timestamp corrida) |

### 3.2 Pruebas aprobadas (muestra representativa)

| Área | Tests |
|------|--------|
| Regresión solver Sprint 1 | `test_solver.py` (5/5) |
| US-008 validador / jornada / solver kg-m³ | 9/12 en archivo (3 requieren BD; 1 fallo precheck) |
| US-007 GA / ahorros / semilla | 5/8 (3 BD; 1 fallo ventanas) |
| EN-001 SLA / benchmark | `test_solver_sla_en001.py` (4/4, incl. `@slow` 150×15) |
| US-004 unitario (regresión) | `test_unit_services.py` (8/8) |
| US-009 ETA matriz / secuencia | 4/6 (2 BD) |

### 3.3 Pruebas fallidas (detalle)

| Test | Resultado | Causa observada |
|------|-----------|-----------------|
| `test_precheck_volume_exact_and_over` | **FAILED** | Segundo caso: 1 pedido con 6 m³ en flota 10 m³ → `feasible=True` (correcto según `precheck_fleet_capacity`); el test espera `False`. **Probable defecto del test** (debería usar demanda &gt; 10 m³). |
| `test_infeasible_windows_not_marked_feasible` | **FAILED** | `start_h=8, end_h=8` → ventana nula; `solve_vrptw` lanza `ValueError: ventana invertida` antes de evaluar factibilidad. **Fixture del test incompatible** con validación de ventanas del solver. |

### 3.4 Errores por dependencia de BD (no ejecutadas)

13 tests con **ERROR en setup** (`asyncpg.connect` → `ConnectionRefusedError`):

- US-005: 6 tests en `tests/test_geocode_us005.py`
- US-007: `test_optimize_seed_metadata_rn008`, `test_jornada_filter_excludes_other_days`
- US-008: `test_seed_optimize_regression_sprint1`, `test_fleet_insufficient_409_without_persisting`, `test_import_optional_volume_persisted`
- US-009: `test_optimize_geojson_eta_fields`, `test_recalculate_etas_endpoint`

### 3.5 Regresión Sprint 1 (suite completa)

| Control | Estado |
|---------|--------|
| Inventario total pytest | **114** tests (`pytest --collect-only`) |
| Suite completa con BD | **No ejecutada** (mismos 58+ errores de setup esperados sin PostGIS) |
| Archivos Sprint 1 no re-ejecutados aquí | `test_api.py`, `test_day.py`, `test_import_us004.py`, `test_fleet_us001.py`, `test_plate_restriction_us002.py`, `test_vehicle_state_us003.py`, `test_order_window_us006.py`, `test_security_en003.py`, `test_auth.py`, `test_realtime.py`, `test_pdf.py` |

**Conclusión regresión:** no hay evidencia de suite Sprint 1 en verde en este entorno; CI (`.github/workflows/ci.yml`) está **preparado** con servicio PostGIS en puerto 5432, pero **no se comprobó** ejecución remota.

### 3.6 Frontend

| Métrica | Estado |
|---------|--------|
| `npm run test:coverage` | **No ejecutado** (npm ausente) |
| Cobertura frontend DoD ≥ 80 % | **Sin medición** |

---

## 4. Cobertura de pruebas

| Ámbito | Medición | Umbral DoD | Cumple |
|--------|----------|------------|--------|
| Backend (`app/`) | **50 %** líneas (corrida focal con cov); **~57 %** en `coverage.xml` posterior a collect-only | ≥ 80 % | **No** |
| Módulos bien cubiertos | `genetic_solver.py` ~95 %, `route_constraints.py` ~90 % en corrida focal | — | — |
| Módulos críticos bajos | `routes.py` ~21 %, `order_import.py` ~26 %, `websockets.py` ~12 % | — | Riesgo |
| Frontend | Sin corrida | ≥ 80 % | **No verificado** |

Configuración: `pyproject.toml` (`--cov=app`), exclusiones documentadas `app/db/init_db.py` en `sonar-project.properties`.

---

## 5. Análisis estático, seguridad y calidad

| Control DoD | Estado | Evidencia |
|-------------|--------|-----------|
| SonarQube | **No ejecutado** | `sonar-project.properties` presente; job en CI solo si `SONAR_ENABLED` |
| CodeQL | **No configurado / no ejecutado** | Sin workflow CodeQL en repo |
| Vulnerabilidades críticas/altas | **Sin scan** | No afirmar 0 hallazgos |
| Deuda bloqueante Sonar | **Sin scan** | — |
| Revisión estática manual | Parcial | EN-003: `require_roles` en optimizar; guardias BD en conftest; HTTPS redirect middleware presente |

**Calidad de código (observación):** separación clara `route_constraints` vs GA; API documentada con `summary`/`responses` en `routes.py`. **Riesgo:** capa API con baja cobertura y mucha lógica en `routes.py`.

---

## 6. Migraciones y modelos

| Versión | Contenido | Compatibilidad |
|---------|-----------|----------------|
| **007** | `estado_ubicacion`, `volumen_m3` nullable, `ubicacion`/`altitud` nullable si pendiente, `area_operacion`, CHECK estado | Alineado con US-005 / US-008 volumen opcional |
| **008** | `estado_eta`, espera/tarde ventana, `secuencia_entrega`, `modelo_distancia` en `rutas_detalle` | Alineado con US-009 |

**Verificación runtime:** migraciones **no aplicadas** en este entorno (sin BD). Compatibilidad revisada por lectura de `app/db/migrations.py` y modelos/enums (`EstadoEta`, `ModeloDistancia`, `EstadoUbicacion`).

---

## 7. OpenAPI y docstrings

| Aspecto | Estado |
|---------|--------|
| Endpoints Sprint 2 | `PATCH` ubicación pedido, `POST /optimizar-rutas` (409 infactible), `POST /soluciones/{id}/recalcular-etas` con `summary` y códigos HTTP |
| Swagger `/docs` | **No abierto** en browser en esta verificación |
| Docstrings servicios clave | Presentes en `genetic_solver.solve_vrptw`, `route_constraints`, `routes.py` (recalcular ETAs) |

**Pendiente:** validación manual de que el esquema OpenAPI generado coincide con payloads reales (requiere app levantada).

---

## 8. Pipeline CI/CD y staging

| Elemento | Evidencia en repo | Verificación runtime |
|----------|-------------------|----------------------|
| CI backend | PostGIS 15-3.4, `pytest --cov`, Python 3.11 | **No** (sin `gh`) |
| CI frontend | `npm ci`, `test:coverage`, `build` | **No** |
| Deploy staging | Job placeholder `workflow_dispatch` | **No despliegue verificable** |
| Peer review PR | — | **No revisado** (sin evidencia de aprobación humana) |

---

## 9. EN-001 — métricas de rendimiento

Fuente: `REPORTE_RENDIMIENTO_EN_001.md` + ejecución local `tests/test_solver_sla_en001.py` (4 passed, incl. escenario `@slow`).

| Criterio | Objetivo | Medido | Cumple |
|----------|----------|--------|--------|
| RNF-001 tiempo solver 150×15 | ≤ 45 s | Media **~0,89 s** (5 repeticiones) | **Sí** |
| RNF-001 solución **válida** | Factible dura | `feasible=false` en 0/5 repeticiones (dataset sintético) | **No** |
| EN-001 Esc. 1 HTTP total | T ≤ 45 s | **No medido** (sin PostGIS / sin `POST /optimizar-rutas`) | **Pendiente** |
| EN-001 Esc. 2 timeout | Mejor factible, sin caída | Implementado en GA (`optimizer_time_budget_seconds`); test de reloj simulado en suite parcial | **Parcial** (código + reporte; no E2E) |

**Nota:** con US-008, una corrida GA infactible en API debe responder **409** y no persistir; el SLA de tiempo no implica publicación automática.

---

## 10. Restricciones duras en rutas (US-008 / US-007)

| Control | Implementación (código) | Prueba ejecutada |
|---------|-------------------------|------------------|
| Precheck flota kg/m³ | `precheck_fleet_capacity` → 409 en `optimize_routes` | Unitarias OK excepto volumen “over” |
| Validación publicación | `validate_for_publication` (peso, m³, ventanas, jornada) → 409 | Varias unitarias OK |
| No persistir infactible | `routes.py` retorna 409 antes de asignar | **No** (tests API con ERROR) |
| Jornada 8 h | `compute_shift_minutes` sin espera en ventana | Unitarias OK |
| GA + ventanas | Penalización / flag `feasible` | Regresión `test_solver.py` OK |

---

## 11. Matriz Historia × Criterio

Leyenda **Estado:** ✅ verificado en prueba | 🔶 implementado, prueba no corrida | ⚠️ parcial | ❌ no implementado / incumplido  
**Prueba:** archivo o comando; **Resultado:** solo si se ejecutó.

### US-005 — Geocodificación (RF-005)

| ID | Criterio (origen) | Estado | Evidencia (código) | Prueba | Resultado | Pendiente |
|----|-------------------|--------|--------------------|--------|-----------|-----------|
| US5-G | Dirección válida → coordenadas y mapa | 🔶 | `geocode.py`, `operating_area.py`, migración 007, `geometry` 4326 | `test_geocode_us005.py` | ERROR (BD) | E2E con PostGIS |
| US5-I | Fuera de cobertura → pendiente validación, excluido de optimizar | 🔶 | `EstadoUbicacion.PENDIENTE_VALIDACION`, import persiste pendiente, filtro lote | idem | ERROR | Validar polígono prod (D-05) |
| US5-F | Operador corrige punto (`PATCH`) | 🔶 | `PATCH` ubicación en `routes.py` | `test_manual_patch_geocodes...` | ERROR | — |
| US5-MAP | Punto en mapa | 🔶 | `Map.tsx`, GeoJSON pedidos | Manual / E2E | No ejecutado | — |
| US5-POSTGIS | Punto en área aplicación | 🔶 | Shapely + `area_operacion` / fixture GeoJSON | idem | ERROR | Tipo `geometry` vs `GEOGRAPHY` (D-01) |
| US5-REG | Import rechaza peso/ventana inválidos | 🔶 | `order_import.py` sin cambio de reglas duras | `test_import_still_rejects...` | ERROR | — |

**Clasificación US-005:** **Implementada, pendiente de validación.**

---

### US-007 — Rutas sostenibles (RF-007, RN-008)

| ID | Criterio | Estado | Evidencia | Prueba | Resultado | Pendiente |
|----|----------|--------|-----------|--------|-----------|-----------|
| US7-F | Lote pequeño factible → rutas válidas | 🔶 | `genetic_solver`, semilla init_db | `test_api.py` / `test_seed_optimize...` | ERROR (BD) | — |
| US7-I | Exceso peso/volumen flota → no factible, detalle | 🔶 | `precheck_fleet_capacity` + 409 | `test_fleet_insufficient_409...` | ERROR | — |
| US7-G | Ahorro ≥ 15 % distancia y ≥ 10 % CO₂ | ⚠️ | Metadatos `ahorro_*_pct`; **no veto** (D-06) | `test_savings_percent_honest...` | **PASS** | Escenario 150×15 con umbrales |
| US7-RN8 | Línea base secuencial | ✅ | FIFO + secuencial en `RouteSolution` | `test_sequential_baseline...` | **PASS** | API metadata |
| US7-DIA | Lote por jornada/fecha | 🔶 | Filtro fecha en optimizar | `test_jornada_filter...` | ERROR | — |
| US7-FLOTA | Solo activos / placa | ✅ | Sin cambio regresivo | Sprint 1 suites | No re-ejecutado | Correr con BD |
| US7-GA | Metaheurística propia (no OR-Tools) | ✅ | `genetic_solver.py` | `test_optimizer_us007.py` | Mayoría PASS | — |

**Clasificación US-007:** **Parcial.**

---

### US-008 — Restricciones duras (RF-008, RN-003, RN-004)

| ID | Criterio | Estado | Evidencia | Prueba | Resultado | Pendiente |
|----|----------|--------|-----------|--------|-----------|-----------|
| US8-G | ≤ 100 % peso/volumen, jornada ≤ 8 h | ⚠️ | `validate_for_publication`, `shift_limit_minutes` | Unitarias validate/shift | **PASS** (varias) | Publicación API |
| US8-I | 8,5 h o exceso → rechazo / no publicar | 🔶 | 409 API | `test_fleet_insufficient...` | ERROR | Reparto automático “divide carga” (RF infeliz) no verificado |
| US8-RN4 | m³ cuando existe dato | ⚠️ | Precheck solo suma pedidos con `volumen_m3` | `test_precheck_volume...` | **FAIL** (test) | Corregir test o exigir volumen |
| US8-RN5 | ETA en ventana (publicación) | 🔶 | Validador ventanas | validate tests | PASS parcial | Integración |
| US8-REG | Espera temprana no atraso | ✅ | `_schedule_vehicle` | `test_early_arrival...` | **PASS** | — |

**Clasificación US-008:** **Parcial.**

---

### US-009 — Secuencia y ETA (RF-009)

| ID | Criterio | Estado | Evidencia | Prueba | Resultado | Pendiente |
|----|----------|--------|-----------|--------|-----------|-----------|
| US9-G | Orden 1…n y ETA en ventana | ⚠️ | `secuencia_entrega`, `eta_schedule` | `test_delivery_sequence...` | **PASS** (solver) | 10 paradas explícitas |
| US9-F | Reordenar → recalcular ETA | 🔶 | `POST .../recalcular-etas`, `sequence_eta.py` | `test_recalculate_etas...` | ERROR | — |
| US9-I | Matriz ausente → revisión, ETA nulo | ✅ | `routing_matrix`, `EstadoEta` | `test_matrix_missing...` | **PASS** | OSRM off by default (D-03) |
| US9-RF-G | Secuencia + ETA al cerrar optimización | 🔶 | Persistencia + GeoJSON | `test_optimize_geojson...` | ERROR | Sidebar UI no probada |

**Clasificación US-009:** **Parcial.**

---

### EN-001 — SLA ≤ 45 s (RNF-001)

| ID | Criterio | Estado | Evidencia | Prueba | Resultado | Pendiente |
|----|----------|--------|-----------|--------|-----------|-----------|
| EN1-1 | 150×15, T ≤ 45 s | ⚠️ | GA + `resolve_ga_parameters` | `test_solver_sla_150x15` | **PASS** tiempo | Medir HTTP; factibilidad |
| EN1-2 | Timeout → mejor factible, servicio vivo | 🔶 | Presupuesto en solver | Reporte + código | No test reloj en corrida | Test dedicado |
| EN1-VAL | Solución válida dentro SLA | ❌/⚠️ | US-008 en API | Benchmark JSON | **feasible=false** 150×15 | Afinar GA / dataset |

**Clasificación EN-001:** **Parcial** (tiempo sí; validez y API no cerrados).

---

## 12. Definition of Done — estado real (Sprint 2)

| # | Criterio DoD | Estado | Evidencia |
|---|--------------|--------|-----------|
| 1 | Cobertura ≥ 80 % backend y frontend | **No** | Backend ~50 % medido; frontend sin medir |
| 2 | Sonar/CodeQL 0 críticas/altas, 0 deuda bloqueante | **No verificado** | Sin scan |
| 3 | Peer review aprobado | **No verificado** | Sin PR revisado en esta auditoría |
| 4 | CI/CD staging exitoso | **No verificado** | Placeholder staging; pipeline remoto no consultado |
| 5 | OpenAPI + docstrings alineados | **Parcial** | Anotaciones FastAPI presentes; smoke `/docs` pendiente |

---

## 13. Riesgos pendientes

1. **Suite de integración bloqueada** sin PostGIS local o CI — historias US-005/007/008/009 no cerradas en E2E.
2. **EN-001 “solución válida”** en 150×15 sintético — riesgo de 409 sistemático en API aunque el reloj cumpla.
3. **Dos tests unitarios rotos o mal especificados** — pueden ocultar regresiones en CI si la suite completa no corre.
4. **Cobertura API baja** — cambios en `routes.py` con poca red de seguridad automatizada.
5. **DoD global** — mismo patrón que `REPORTE_VERIFICACION_DOD_SPRINT_1.md`; Sprint 2 no eleva cobertura al umbral.
6. **Desviaciones documentales** — GA vs OR-Tools, `geometry` vs `GEOGRAPHY`, OSRM opcional (aceptado en plan D-01/D-03).

---

## 14. Acciones recomendadas (post-informe, fuera de este commit)

1. Levantar PostGIS (`docker compose up -d db` o CI) y ejecutar **`uv run pytest --cov=app --cov-report=term-missing`** (114 tests).
2. Corregir **`test_precheck_volume_exact_and_over`** (demanda &gt; capacidad) y **`test_infeasible_windows_not_marked_feasible`** (ventanas no nulas).
3. Ejecutar **`npm run test:coverage`** en entorno con Node 22.
4. Habilitar Sonar en CI o scan local; opcional workflow CodeQL.
5. Revisar factibilidad GA 150×15 vs criterio RNF-001 “válida” (instancia benchmark / generaciones).
6. Verificar pipeline GitHub y staging con credenciales reales cuando existan.

---

## 15. Declaración de auditoría

- **No** se declaran exitosas pruebas que no se ejecutaron (13 ERROR por BD, suite Sprint 1 completa sin correr, frontend sin npm).
- **No** se afirma peer review ni despliegue staging exitoso.
- **No** se afirma cumplimiento DoD global del proyecto.
- Clasificaciones basadas en **código revisado**, **34 pruebas PASS** documentadas, **2 FAIL**, **4 EN-001 PASS**, y **`REPORTE_RENDIMIENTO_EN_001.md`**.

---

*Fin del informe `VERIFICACION_FINAL_SPRINT_2.md`.*
