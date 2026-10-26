# Reporte de verificación — Definition of Done Sprint 1

**Proyecto:** EcoLogística Huancayo  
**Fecha:** 2026-10-26  
**Alcance:** EN-003, US-001, US-002, US-003, US-004, US-006  
**Fuente DoD:** `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` §2 (criterios 1–5, sin reinterpretación)

---

## 1. Definition of Done documental (referencia)

| # | Criterio DoD global |
|---|---------------------|
| 1 | Cobertura de pruebas automáticas **≥ 80 %** en backend (FastAPI) y frontend (React/PWA). |
| 2 | Análisis estático (SonarQube/CodeQL): **0** vulnerabilidades críticas/altas y **0** deuda bloqueante. |
| 3 | **Peer review:** PR revisado y aprobado por un par antes de integrar a `main`/`develop`. |
| 4 | **CI/CD:** despliegue automatizado exitoso en **Staging / Pruebas**. |
| 5 | **Documentación:** OpenAPI/Swagger y docstrings alineados con el código. |

---

## 2. Fase 1 — Seguridad de las pruebas

| Control | Estado | Evidencia |
|---------|--------|-----------|
| BD aislada `ecologistica_test` | **Implementado** | `tests/conftest.py` fuerza `DATABASE_URL` → `ecologistica_test` antes de importar la app. |
| Guardia anti-TRUNCATE en BD prod | **Implementado** | `_assert_test_database_isolated()` en carga y antes de `_reset_seed()`. |
| TRUNCATE solo tablas operativas | **Implementado** | No trunca `usuarios`; reinicia semilla vía `init_database()`. |
| Creación de BD de prueba | **Implementado** | `_ensure_test_database()` crea `ecologistica_test` si no existe (conexión a `postgres`). |

**Riesgo residual:** quien exporte `DATABASE_URL=.../ecologistica` y ejecute pytest **sin** pasar por `conftest` podría dañar datos; la guardia mitiga si la URL no termina en `ecologistica_test`.

---

## 3. Fase 2 — Pruebas funcionales por historia

### Inventario de suites

| Historia | Archivos de prueba | Positivas / negativas / RBAC |
|----------|-------------------|------------------------------|
| **EN-003** | `tests/test_security_en003.py`, `tests/test_auth.py` | Anónimo, auditor, tokens, conductor, seguimiento público |
| **US-001** | `tests/test_fleet_us001.py`, `tests/test_day.py` (flota) | Alta, duplicado, RBAC, optimizador |
| **US-002** | `tests/test_plate_restriction_us002.py` | Regla pendiente, activación, optimizador, auditor |
| **US-003** | `tests/test_vehicle_state_us003.py` | Transiciones, historial, ruta histórica |
| **US-004** | `tests/test_import_us004.py`, `tests/test_day.py` | CSV/XLSX, 150 filas, duplicados, permisos |
| **US-006** | `tests/test_order_window_us006.py`, `tests/test_api.py` | Ventana válida/inválida, ruta activa, cerrado |
| **Regresión** | `tests/test_api.py`, `tests/test_solver.py`, `tests/test_realtime.py`, `tests/test_pdf.py` | Optimización, solver, WS, PDF |
| **Unitarias (sin BD)** | `tests/test_unit_services.py` | Import CSV, ventanas, placa, estados |

### Ejecución en este entorno

| Métrica | Resultado |
|---------|-----------|
| **PostGIS disponible** | No (`ConnectionRefusedError` en `localhost:5433`; Docker Desktop detenido). |
| **Integración (client fixture)** | **58 errores** de setup (sin BD). |
| **Sin BD** | **13 passed** (`test_solver.py` + `test_unit_services.py`). |
| **Conclusión** | La suite funcional **no pudo validarse de extremo a extremo** aquí; el pipeline CI (`.github/workflows/ci.yml`) está preparado para ejecutarla con servicio PostGIS. |

---

## 4. Fase 3 — Cobertura

### Configuración implementada

| Elemento | Ubicación |
|----------|-----------|
| pytest-cov | `backend/requirements.txt`, `pyproject.toml` `[tool.coverage.*]` |
| Reporte XML backend | `coverage.xml` (generado localmente) |
| Vitest + v8 | `vitest.config.ts`, `npm run test:coverage` |
| Reporte frontend | `coverage/frontend/lcov.info` (previsto en CI) |

### Exclusiones justificadas (denominador)

| Exclusión | Motivo |
|-----------|--------|
| `app/db/init_db.py` | Script CLI de semilla/migración manual; no lógica de negocio en runtime. |

No se aplicaron exclusiones masivas de API o servicios para inflar el porcentaje.

### Mediciones obtenidas (evidencia real)

| Alcance | Comando | Líneas (`app`) | Cobertura | Notas |
|---------|---------|----------------|-----------|--------|
| **Backend — suite completa intentada** | `pytest tests --cov=app` | 3260 stmts | **~58 %** (reporte parcial: tests de integración fallaron al inicio) | XML generado; cifra **no** representa suite verde. |
| **Backend — unit + solver** | `pytest test_unit_services test_solver --cov=app` | 3165 stmts | **46 %** | 13 tests OK, sin PostGIS. |
| **Frontend** | `npm run test:coverage` | — | **No ejecutado** | `npm` no disponible en PATH del agente. |

**DoD ≥ 80 %:** **NO cumplido** (backend y frontend por debajo del umbral documentado).

### Módulos con baja o nula cobertura en medición parcial (prioridad QA)

- `app/api/v1/routes.py`, `websockets.py`, `desk.py`, `plate_restrictions.py` (requieren tests de integración con BD).
- `app/services/order_import.py`, `access.py`, `realtime_router.py`, `pdf_generator.py`.
- `app/middleware/https_redirect.py`, `app/core/security_boot.py` (arranque/TLS).

Se añadió `tests/test_unit_services.py` para reforzar servicios puros sin ampliar exclusiones.

---

## 5. Fase 4 — SonarQube

| Ítem | Estado |
|------|--------|
| `sonar-project.properties` | **Configurado** (fuentes Python/TS, `coverage.xml`, `lcov`) |
| Comando reproducible | `docs/qa/COMANDOS_CALIDAD.md` |
| Job CI `sonar` | **Configurado**; corre solo si `vars.SONAR_ENABLED == 'true'` y secretos `SONAR_TOKEN` / `SONAR_HOST_URL` |
| Escaneo ejecutado | **No** — no hay servidor SonarQube accesible ni token en este entorno |
| Quality Gate / vulnerabilidades | **Sin evidencia** (no inventado) |

**CodeQL:** no configurado en este entrega (DoD permite SonarQube **o** CodeQL; falta al menos uno ejecutado).

---

## 6. Fase 5 — CI/CD

| Ítem | Estado |
|------|--------|
| Workflow `.github/workflows/ci.yml` | **Implementado** |
| Backend: dependencias + pytest + cobertura | **Definido** (PostGIS service) |
| Frontend: `npm ci`, tests, `tsc`/build | **Definido** |
| Sonar (opcional) | **Definido** |
| Deploy staging | **Placeholder** en `workflow_dispatch` + environment `staging`; **no despliega** sin secretos |
| Ejecución en GitHub Actions | **No verificada** en esta sesión (sin push/ejecución remota) |

**DoD despliegue staging exitoso:** **NO cumplido** (pipeline no ejecutado; staging no desplegado).

---

## 7. Fase 6 — Documentación técnica

| Ítem | Estado |
|------|--------|
| OpenAPI `/docs` | FastAPI activo; tags ampliados para `jornada` y `restricciones-placa` en `OPENAPI_TAGS` |
| Endpoints nuevos Sprint 1 | Incluidos en routers (`desk`, `plate_restrictions`, `PATCH /pedidos/{id}`) — documentación vía schemas Pydantic |
| Docstrings | Parcial en servicios nuevos (`order_window`, `order_import` estrategia); no revisión exhaustiva de todo el repo |
| DoD punto 5 | **Parcialmente cumplido** (OpenAPI operativo; docstrings no homogéneos al 100 %) |

---

## 8. Matriz por historia (criterio ágil vs evidencia técnica)

Leyenda: **T** = cumplimiento técnico en código | **P** = probado en esta sesión | **N** = pendiente

| Historia | Criterio clave (BDD/resumen) | T | P |
|----------|------------------------------|---|---|
| **EN-003** | Auth JWT, RBAC, seguimiento token, HTTPS boot | Sí | N (sin BD) |
| **US-001** | CRUD flota, campos RF-001, historial | Sí | N |
| **US-002** | RN-002 parametrizada, no activar sin validación | Sí | N |
| **US-003** | Estados operativos + historial + exclusión rutas | Sí | N |
| **US-004** | Import CSV/XLSX, 150, informe por fila | Sí | N |
| **US-006** | Ventanas válidas + PATCH antes de ruta | Sí | N |

---

## 9. DoD global — tabla de cumplimiento

| Criterio DoD | Config implementada | Ejecutada / evidencia | Cumple |
|--------------|---------------------|------------------------|--------|
| 1. Cobertura ≥ 80 % BE + FE | pytest-cov, vitest | BE ~46–58 % medido; FE N/E | **No** |
| 2. Sonar/CodeQL 0 críticas/altas | sonar-project.properties + job CI | Escaneo no ejecutado | **No evaluado** |
| 3. Peer review PR | — | No hubo revisión humana en esta sesión | **No** |
| 4. CI/CD staging OK | workflow + job placeholder | Pipeline no corrido | **No** |
| 5. OpenAPI + docstrings | Tags OpenAPI actualizados | `/docs` no auditado manualmente | **Parcial** |

---

## 10. Hallazgos de seguridad (pruebas)

| Hallazgo | Severidad | Notas |
|----------|-----------|--------|
| TRUNCATE acotado a `ecologistica_test` | Mitigado | Guardia en `conftest.py` |
| Tests sin BD no validan RBAC E2E | Proceso | Requiere CI/local con PostGIS |
| Sonar no ejecutado | Proceso | No se afirma 0 vulnerabilidades |

---

## 11. Requisitos cumplidos vs pendientes

### Cumplidos (infraestructura y diseño)

- Aislamiento de BD de prueba reforzado.
- Suite automatizada ampliada por historia Sprint 1.
- pytest-cov y vitest configurados con reportes reproducibles.
- SonarQube preparado para importar cobertura.
- Pipeline CI multi-job (backend, frontend, sonar opcional, staging manual).
- OpenAPI enriquecido con tags de jornada y restricciones por placa.
- Pruebas unitarias adicionales sin BD.

### Pendientes (bloquean DoD)

1. Ejecutar suite completa con PostGIS y dejar **≥ 80 %** cobertura backend (y frontend).
2. Ejecutar SonarQube o CodeQL y archivar Quality Gate.
3. PR con peer review registrado.
4. Pipeline verde + despliegue staging con credenciales reales.
5. Completar docstrings donde falten en módulos tocados en Sprint 1.

---

## 12. Veredicto de cierre Sprint 1

**Veredicto:** el Sprint 1 **no cumple** la Definition of Done global documentada para declarar las historias **Done** en sentido de calidad de entrega.

**Fundamento:** las funcionalidades US/EN están **implementadas en código** con pruebas automatizadas **escritas**, pero en esta verificación **no se obtuvo** evidencia de suite verde, cobertura ≥ 80 %, análisis estático limpio, revisión por pares ni despliegue staging exitoso.

**Recomendación operativa inmediata:**

1. Levantar PostGIS (`docker compose up -d db`) o usar GitHub Actions.
2. `pytest` completo + subir cobertura en capas API (httpx) donde falte.
3. `npm run test:coverage` y ampliar tests de `src/lib` y componentes críticos.
4. Activar `SONAR_ENABLED` y registrar resultado del Quality Gate.
5. Abrir PR, revisión cruzada y `workflow_dispatch` hacia staging cuando existan secretos.

---

*Este informe no modifica los cuatro documentos oficiales del Sprint 1 en `docs/03 Implementación/`.*
