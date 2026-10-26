# AUDITORIA_04_ESTABILIDAD

**Proyecto:** EcoLogística Huancayo — DistriRápido S.A.C.  
**Fecha de auditoría recuperada:** 26/10/2026  
**Modalidad original:** revisión estática y documental; no se ejecutaron pruebas, benchmarks, instalaciones, migraciones ni operaciones con base de datos.  
**Alcance:** estabilidad heredada de Sprint 1 y Sprint 2, y preparación para Sprint 3.

> Este archivo recupera el informe emitido previamente. No constituye una nueva auditoría ni actualiza sus resultados.

## Resumen ejecutivo y veredicto

**Veredicto: No preparado** para declarar Sprint 3 evaluable o para cerrar formalmente los Sprints 1 y 2.

El repositorio contiene una base funcional amplia y correcciones posteriores a observaciones tempranas, pero no existe evidencia suficiente de regresión integral, seguridad evaluada, factibilidad válida 150×15, Quality Gate, cobertura DoD, CI verde o staging verificable.

El desarrollo funcional de Sprint 3 puede comenzar solamente si se reserva capacidad explícita para cerrar los bloqueos de calidad heredados. No está sustentado comenzar sus evaluaciones formales ni afirmar preparación formal.

---

## 1. Cumplimiento del Sprint 1

Las historias tienen implementación estática y pruebas dedicadas:

| Historia | Resultado recuperado | Evidencia principal |
|---|---|---|
| US-001 | Implementada estáticamente | Flota, capacidades, modelo/rendimiento, RBAC y estado inicial; `tests/test_fleet_us001.py`. |
| US-002 | Implementada estáticamente | Configuración de restricción por placa, validación normativa, auditoría y filtrado; `tests/test_plate_restriction_us002.py`. |
| US-003 | Implementada estáticamente | Estados Activo/Mantenimiento/Inactivo, historial y exclusión de ruteo; `tests/test_vehicle_state_us003.py`. |
| US-004 | Implementada estáticamente | Importación CSV/XLSX, tope de 150 filas y reporte por fila; `tests/test_import_us004.py`. |
| US-006 | Implementada estáticamente | Validación y edición de ventanas antes de rutear; `tests/test_order_window_us006.py`. |
| EN-003 | Parcialmente acreditada | bcrypt, JWT, RBAC, bloqueo tras tres intentos, bitácora y seguimiento por token; `tests/test_auth.py`, `tests/test_security_en003.py`. |

### Estado de cierre

Sprint 1 **no cumple la Definition of Done global**. No hay evidencia verificable de:

1. Suite E2E verde con PostGIS.
2. Cobertura >=80 % en backend y frontend.
3. SonarQube o CodeQL ejecutado y sin vulnerabilidades críticas/altas.
4. Peer review registrado.
5. Staging desplegado y verificado.

Fuente recuperada: `REPORTE_VERIFICACION_DOD_SPRINT_1.md`.

---

## 2. Cumplimiento del Sprint 2

| Historia | Estado sustentado | Evidencia/limitación recuperada |
|---|---|---|
| US-005 — Geocodificación | Implementada estáticamente; validación pendiente | Geocodificación, área de operación y PATCH de ubicación existen. Falta E2E PostGIS. |
| US-007 — Rutas sostenibles | Parcial | Restricciones y metadatos existen; ahorro >=15 % de distancia y >=10 % CO₂ es informativo, no garantizado como veto. |
| US-008 — Restricciones duras | Parcial | Validadores y respuesta 409 existen; falta evidencia API/E2E. |
| US-009 — Secuencia y ETA | Parcial | Secuencia, ETA, estados y recálculo implementados; integración no validada completamente. |
| EN-001 — SLA <=45 s | Parcial | Tiempo del solver medido; no quedó acreditada solución válida 150×15 ni tiempo HTTP total. |

### Evidencia de ejecución histórica

El informe `VERIFICACION_FINAL_SPRINT_2.md`, fechado el 26/10/2026, reportó una corrida focal de 49 pruebas:

| Resultado | Cantidad |
|---|---:|
| PASS | 34 |
| FAIL | 2 |
| ERROR de setup BD | 13 |
| Duración reportada | ~17 s |
| Cobertura backend de esa corrida focal | 50 % líneas |

Los 13 errores se atribuyeron a la ausencia de PostGIS/Docker en el entorno de verificación. El informe posterior `REPORTE_AUDITORIA_CI.md` documentó correcciones de los dos fixtures de prueba entonces fallidos y cuatro pruebas focales PASS, pero no sustituyó la falta de corrida integral con PostGIS ni acreditó una ejecución real de GitHub Actions.

---

## 3. Pruebas automatizadas existentes y regresión

### Inventario funcional

| Área | Pruebas disponibles |
|---|---|
| API/regresión general | `tests/test_api.py` |
| Autenticación/RBAC | `tests/test_auth.py`, `tests/test_security_en003.py` |
| Sprint 1 | `test_fleet_us001.py`, `test_plate_restriction_us002.py`, `test_vehicle_state_us003.py`, `test_import_us004.py`, `test_order_window_us006.py` |
| Sprint 2 | `test_geocode_us005.py`, `test_optimizer_us007.py`, `test_hard_constraints_us008.py`, `test_eta_us009.py`, `test_solver_sla_en001.py` |
| Solver y servicios puros | `test_solver.py`, `test_unit_services.py` |
| Tiempo real | `test_realtime.py` |
| Migraciones | `test_db_migrations.py` |
| PDF | `test_pdf.py` |

Hay pruebas de regresión para solver, migraciones, API, tiempo real y PDF. Su eficacia end-to-end **no fue acreditada**, dado que la suite completa dependiente de PostGIS no fue ejecutada en el contexto documentado.

### Dependencia de base de datos y riesgo de ejecución

`tests/conftest.py` fuerza `DATABASE_URL` a `ecologistica_test`, aborta si el nombre no coincide y crea/reinicializa esa base. La fixture ejecuta `TRUNCATE` sobre tablas operativas de **la BD de pruebas** y restablece la semilla.

Conclusión recuperada:

- Protege la base de desarrollo mediante una guardia explícita.
- Requiere PostGIS disponible y privilegios para crear la BD `ecologistica_test`.
- Es destructiva exclusivamente dentro de dicha BD de pruebas; por eso no se ejecutó en la auditoría de solo lectura.

---

## 4. Cobertura de código

| Ámbito | Configuración/evidencia | Estado recuperado |
|---|---|---|
| Backend | `pytest-cov`, `--cov=app`, cobertura de ramas, XML `coverage.xml` | Cobertura histórica parcial aproximada 50–58 %, no >=80 %. |
| Frontend | Vitest + V8; salida prevista `coverage/frontend/lcov.info` | Sin métrica archivada de cumplimiento >=80 % en la auditoría Sprint 2. |
| Umbral | `pyproject.toml` tiene `--cov-fail-under=0` | El pipeline no bloquea por cobertura insuficiente. |

La DoD exige >=80 % en backend y frontend. Módulos identificados con cobertura baja o no confirmada: `app/api/v1/routes.py`, `app/api/v1/websockets.py`, `app/api/v1/desk.py`, `app/api/v1/plate_restrictions.py`, `app/services/order_import.py`, `app/services/access.py`, `app/services/realtime_router.py`, `app/services/pdf_generator.py`, `app/middleware/https_redirect.py` y `app/core/security_boot.py`.

---

## 5. Seguridad, JWT, autorización y tracking

| Hallazgo/control | Impacto | Evidencia recuperada |
|---|---|---|
| TLS no activado por defecto en Compose | Alto | `frontend/nginx.conf` escucha HTTP:80; `FORCE_HTTPS=false`; TLS queda como plantilla en `frontend/nginx-ssl.conf.example`. |
| JWT | Mitigado parcialmente | `app/services/tokens.py`: HS256, `exp`, algoritmo restringido; `app/api/deps.py` valida sesión y usuario activo. Duración predeterminada de 12 h. |
| Desalineación JWT | Medio | La revisión documental menciona 15 min, mientras `auth_token_hours=12` es el valor predeterminado. |
| RBAC REST | Mitigado parcialmente | `require_roles` protege operaciones y registra rechazos en bitácora; falta validación E2E integral. |
| Bloqueo de acceso | Mitigado | `app/services/access.py`: tres intentos fallidos y bloqueo de 15 min. |
| WebSockets | Medio | JWT/rol en canales de personal, límite de 8,000 caracteres y validación de GPS. El token viaja en query string; no se observó control de `Origin`, rate limiting ni pruebas dinámicas de abuso. |
| Tracking público | Medio | Token UUID opaco y redondeo de coordenadas en `app/services/tracking_tokens.py`; no hay prueba dinámica de enumeración, revocación o expiración. |
| Secretos | Medio | `app/core/security_boot.py` rechaza secreto por defecto y cuentas demo fuera de demo. Compose y `.env.example` contienen credenciales predecibles de desarrollo. |
| Validación de entradas | Mitigado parcialmente | Pydantic, ventanas temporales, límite de mensajes y validación de coordenadas; faltan fuzzing y pruebas dinámicas. |
| Trazabilidad | Parcial | Bitácora de accesos y operaciones; sin evidencia de cobertura total de eventos críticos ni políticas de retención/inmutabilidad. |

No se declaró seguridad completa: faltan pruebas dinámicas TLS, autenticación, autorización, WebSockets, OWASP y dependencias.

---

## 6. SonarQube, CodeQL y calidad

| Control | Estado recuperado |
|---|---|
| SonarQube | Configurado en `sonar-project.properties`; fuentes `app,src`, pruebas y rutas de cobertura declaradas. No ejecutado. |
| Job Sonar | Definido en `.github/workflows/ci.yml`; exige `SONAR_ENABLED=true`, `SONAR_TOKEN` y `SONAR_HOST_URL`. |
| Quality Gate | No existe evidencia de resultado. |
| CodeQL | No configurado ni ejecutado. |
| Linters | No se observó configuración/ejecución de Ruff, Flake8, ESLint u otro linter equivalente. |
| Dependencias | Sin escaneo integrado acreditado. `REPORTE_AUDITORIA_CI.md` registró históricamente 5 vulnerabilidades transitivas detectadas por `npm audit`, sin resolución/evidencia actual. |

La herramienta configurada no equivale a herramienta ejecutada satisfactoriamente.

---

## 7. CI/CD, staging y reportes

### CI configurada

`.github/workflows/ci.yml` define:

| Job | Contenido | Estado de evidencia |
|---|---|---|
| `backend` | PostGIS 15-3.4, dependencias Python, pytest y cobertura | Configurado; ejecución remota no verificada. |
| `frontend` | Node 22, `npm ci`, `npm run test:coverage`, `npm run build` | Configurado; ejecución remota no verificada. |
| `sonar` | Descarga artefactos y escaneo condicional | Configurado; no ejecutado. |
| `deploy-staging` | `workflow_dispatch`, environment staging | Placeholder: no realiza despliegue real. |

### Reportes y validez

| Archivo | Fecha | Alcance | Validez recuperada |
|---|---|---|---|
| `REPORTE_VERIFICACION_DOD_SPRINT_1.md` | 26/10/2026 | DoD y Sprint 1 | Válido para registrar brechas; no certifica cierre. |
| `VERIFICACION_FINAL_SPRINT_2.md` | 26/10/2026 | Sprint 2, corrida parcial | Válido como fotografía parcial; no acredita E2E ni DoD. |
| `REPORTE_RENDIMIENTO_EN_001.md` | 26/10/2026 | Solver local | Válido para tiempo del solver; insuficiente para EN-001 completo. |
| `REPORTE_AUDITORIA_CI.md` | 26/10/2026 | Correcciones CI focales | Acredita correcciones y frontend local; no acredita Actions real, cobertura DoD ni staging. |

---

## 8. Calidad y deuda técnica

Deuda identificada:

1. Cobertura insuficiente y sin gate obligatorio.
2. Capas API, WebSocket y rutas con cobertura baja/no acreditada.
3. Sonar/CodeQL sin ejecución; no hay Quality Gate.
4. Staging es un placeholder y no prueba un despliegue.
5. Discrepancia documental de expiración JWT: 15 min versus 12 h.
6. Geometría almacenada como `geometry` cuando documentación histórica esperaba `GEOGRAPHY`.
7. OSRM no desplegado; puede requerirse ETA en revisión ante matriz no confiable.
8. Polígono operativo oficial pendiente.
9. Jornada de 8 h aplicada con validación normativa aún pendiente.

---

## 9. Docker y dependencias

| Área | Resultado recuperado |
|---|---|
| PostGIS | Dependencia crítica para E2E; su indisponibilidad causó errores de setup históricos. |
| Docker Compose | Expone DB en 5433, backend 8000 y frontend HTTP 8080; usa valores de desarrollo. |
| Backend Dockerfile | Imagen `python:3.11-slim`, limpieza de listas APT y `pip --no-cache-dir`; no se observó usuario no-root, scan de imagen o pin por digest. |
| Frontend Dockerfile | Node 22 Alpine para build y nginx 1.27 Alpine; despliegue por HTTP en configuración activa. |
| Hardening runtime | No se evidenciaron escaneo de contenedor, política de secretos o controles de ejecución no-root. |
| Sonar | Requiere servidor y secretos externos. |
| OSRM | Opcional; vacío equivale a Haversine para distancias/ETA. |

---

## 10. Motor de optimización y restricciones Sprint 2

La auditoría estática identificó estas implementaciones:

| Capacidad requerida | Evidencia recuperada | Estado de validación |
|---|---|---|
| Capacidad kg/m³ | `precheck_fleet_capacity`, `validate_for_publication`, pruebas `test_hard_constraints_us008.py` | Implementada; E2E 409/no persistencia pendiente. |
| Ventanas horarias | Solver VRPTW y validadores de ventanas | Pruebas unitarias parciales; integración pendiente. |
| Jornada configurable | `max_shift_minutes`, `enforce_shift_limit`, cálculo de jornada | Implementada; validación normativa pendiente. |
| Factibilidad | Flag `feasible`, validadores y 409 para infactible | Parcial: falta validación API completa. |
| Cálculos ambientales | Emisiones y baseline secuencial/fifo | Existe; metas de ahorro informativas, no garantía Gold. |
| Persistencia | Soluciones/rutas/detalles y migraciones 007/008 | Revisión estática; migraciones/E2E no acreditadas en el entorno histórico. |
| Secuencia de entregas | `secuencia_entrega`, detalles de ruta | Implementada; integración pendiente. |
| ETA | `eta_schedule.py`, `sequence_eta.py`, estado ETA, recálculo | Implementada parcialmente; UI/integración y OSRM sin verificación. |

El motor usa un GA VRPTW (`app/services/genetic_solver.py`), no OR-Tools. La discrepancia documental fue registrada como impedimento histórico y debe mantenerse visible en la trazabilidad.

---

## 11. Rendimiento EN-001

Fuente: `REPORTE_RENDIMIENTO_EN_001.md` y `tests/test_solver_sla_en001.py`.

| Criterio | Objetivo | Resultado documentado | Estado |
|---|---|---|---|
| Tiempo de solver 150×15 | <=45 s | Media ~0.89 s en cinco repeticiones | Cumple tiempo del solver. |
| Solución válida 150×15 | Factible dura | `feasible=false` en 0/5 repeticiones del dataset sintético | No acreditado. |
| Tiempo HTTP total | <=45 s | No medido por ausencia de PostGIS/API | Pendiente. |
| Timeout | Mejor solución factible sin caída | Presupuesto implementado; evidencia parcial | Parcial. |

Conclusión recuperada: cumplir el reloj no sustituye una solución válida ni la publicación posterior a restricciones duras.

---

## 12. Riesgos de regresión

1. Proteger endpoints operativos con JWT puede afectar mapa, sidebar o conductor si el cliente no remite Bearer correctamente.
2. Cambios de estado de vehículo pueden alterar selección de flota y rutas históricas.
3. Restricción de placa activa modifica disponibilidad previa al solver y debe conservar comportamiento cuando está desactivada.
4. Tope de 150, importación XLSX y persistencia de jornadas pueden rechazar flujos antes válidos si no se prueban E2E.
5. Ajustes de ventana y ETA afectan factibilidad, espera y publicación de rutas.
6. Migraciones SQL son un punto de alto riesgo: hubo corrección del divisor de bloques `DO $$`; existe prueba específica `tests/test_db_migrations.py`, pero falta una corrida integral contra PostGIS.
7. Activar TLS modifica proxy, URLs absolutas, cookies y WebSocket (`wss`).
8. Reducir vida de JWT cambia la experiencia de sesión y requeriría refresh o reingreso.
9. Poner umbrales de ahorro como veto podría bloquear días ya compactos; la decisión vigente documentada era informar el resultado.

---

## 13. Problemas bloqueantes

1. **Definition of Done incumplida:** cobertura, análisis estático, peer review, CI verde y staging carecen de evidencia válida.
2. **E2E con PostGIS no acreditado:** bloquea la validación de US-005, US-007, US-008, US-009 y la regresión total de Sprint 1.
3. **EN-001 no cerrado:** el solver fue rápido, pero no acreditó solución válida 150×15 ni tiempo HTTP total.
4. **Evaluación Sonar/OWASP sin evidencia:** Sonar no se ejecutó y CodeQL no está configurado.
5. **TLS no desplegado/verificado:** la ruta activa por defecto permanece HTTP local.

---

## 14. Preparación para Sprint 3

La planificación separa dos alcances:

| Alcance | Preparación recuperada |
|---|---|
| Funcional: mapa, detalle de paradas y vista resiliente/tabular; PWA offline; indicadores de sostenibilidad — US-010 a US-014 y EN-004 | **Preparado con observaciones técnicas, no para cierre.** Hay base de mapa, GeoJSON, secuencia/ETA, tracking y cálculos ambientales, pero sus dependencias Sprint 2 no están validadas E2E. |
| Evaluativo: SonarQube, OWASP, WCAG, revisión y retrospectiva | **No preparado.** Faltan scanner habilitado, Quality Gate, auditoría de dependencias/OWASP, evidencia WCAG/Lighthouse y pipeline/staging verificable. |

### Recomendaciones emitidas anteriormente

1. Ejecutar la suite completa en PostGIS y archivar resultado/artefactos de cobertura.
2. Alcanzar y convertir en gate el umbral DoD de cobertura backend y frontend.
3. Habilitar SonarQube y archivar Quality Gate; o incorporar/ejecutar CodeQL como alternativa definida por la DoD.
4. Ejecutar revisión OWASP y auditoría de dependencias; resolver o aceptar formalmente los hallazgos.
5. Configurar y verificar TLS real, redirección HTTP→HTTPS y WebSocket seguro.
6. Ejecutar CI real, registrar peer review y disponer de un staging verificable antes del cierre.
7. Medir EN-001 de extremo a extremo, con PostGIS/API, y demostrar una instancia factible 150×15 dentro del SLA.
8. Mantener pruebas de regresión de migraciones, restricciones, secuencia/ETA y control de acceso al implementar Sprint 3.
9. Ejecutar evaluación Lighthouse/WCAG antes de declarar el alcance accesible del modo conductor.

## Declaración final recuperada

No se declararon exitosas pruebas no ejecutadas, ni seguridad completa sin análisis dinámico, ni Quality Gate sin escaneo, ni staging sin despliegue. La conclusión original fue **No preparado** para evaluación/cierre formal de Sprint 3; posible inicio funcional condicionado a un plan explícito de saneamiento de calidad heredada.
