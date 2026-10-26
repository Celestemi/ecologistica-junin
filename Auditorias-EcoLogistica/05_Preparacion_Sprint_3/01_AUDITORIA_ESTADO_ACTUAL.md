# Auditoría de estado actual pre-Sprint 3

**Proyecto:** EcoLogística Huancayo  
**Fecha de auditoría:** 26 de octubre de 2026  
**Alcance:** revisión estática y de configuración posterior a la reorganización documental. No se ejecutaron pruebas, contenedores, migraciones ni comandos que escriban en PostgreSQL. No se modificó ningún archivo existente; este es el único archivo creado.

## Veredicto ejecutivo

El repositorio es **apto con condiciones para iniciar desarrollo acotado de Sprint 3**, pero **no está preparado para declarar cierre formal, despliegue staging ni calidad certificada**. La reorganización documental está físicamente aplicada y los enlaces Markdown operativos revisados apuntan a los nuevos destinos, pero todavía no está consolidada en Git: los orígenes aparecen eliminados y `Auditorias-EcoLogistica/` aparece sin seguimiento. Persisten bloqueos de validación integral con PostGIS, calidad/CI, seguridad de despliegue y factibilidad de EN-001.

## Método y fuentes revisadas

Se inspeccionaron el árbol completo versionado, `git status`, manifiestos, Docker/Compose, workflow CI, configuración Sonar, backend `app/`, frontend `src/`, pruebas `tests/`, documentación de requisitos/Sprints y los cinco informes anteriores:

1. `Auditorias-EcoLogistica/01_Auditorias/AUDITORIA_01_ESTADO_REPOSITORIO.md`
2. `Auditorias-EcoLogistica/01_Auditorias/AUDITORIA_02_DOCUMENTACION.md`
3. `Auditorias-EcoLogistica/01_Auditorias/AUDITORIA_03_CODIGO_ARQUITECTURA.md`
4. `Auditorias-EcoLogistica/01_Auditorias/AUDITORIA_04_ESTABILIDAD.md`
5. `Auditorias-EcoLogistica/01_Auditorias/AUDITORIA_MAESTRA_PRE_SPRINT_3.md`

No se afirmó como corregido ningún comportamiento que requiera ejecución. En particular, `tests/conftest.py` crea/usa `ecologistica_test`, ejecuta `TRUNCATE` y siembra datos: la suite no se ejecutó por la restricción de no modificar bases de datos.

## Implementación activa identificada

| Área | Implementación activa | Evidencia estática |
|---|---|---|
| Backend | FastAPI async, SQLAlchemy/GeoAlchemy, PostgreSQL/PostGIS | `app/main.py`, `app/api/v1/`, `app/models/`, `app/services/`, `app/db/` |
| Frontend | React 18, TypeScript, Vite, Leaflet y Recharts | `src/`, `package.json`, `vite.config.ts` |
| Persistencia y migraciones | Modelos SQLAlchemy, `create_all` y migraciones SQL propias, sin Alembic | `app/db/init_db.py`, `app/db/migrations.py` |
| Pruebas | 21 módulos Python y un test Vitest configurado | `tests/`, `src/lib/orderWindow.test.ts`, `vitest.config.ts` |
| Infraestructura | Compose: PostGIS 15-3.4, FastAPI y Nginx; imágenes separadas | `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile` |
| CI/CD | GitHub Actions para pytest/cobertura, Vitest/build; Sonar condicional; staging placeholder | `.github/workflows/ci.yml` |

## Reorganización documental y enlaces

La estructura actual contiene `01_Auditorias`, `02_Planes_Implementacion`, `03_Reportes_Verificacion`, `04_Informes_CI` y `05_Preparacion_Sprint_3`. Los planes y reportes se encuentran en esos destinos y README/Sprint 1/Sprint 2 enlazan mayoritariamente a ellos. No existe ya el directorio físico `EcologisticaJunin/`; tampoco hay referencias de ejecución (Compose, CI, imports o manifiestos) a él. La comprobación automática de rutas con nombres acentuados produjo falsos positivos de codificación en la consola Windows; los 12 destinos señalados en README se contrastaron manualmente contra las rutas Unicode existentes.

Hallazgos de reorganización:

| ID | Hallazgo | Evidencia | Prioridad | Riesgo | Ruta afectada | Estado actual | Acción recomendada |
|---|---|---|---|---|---|---|---|
| R-01 | Reubicación no consolidada en Git | `git status --short`: orígenes `D`, `Auditorias-EcoLogistica/` y `docs/ESTADO_TECNICO_VIGENTE.md` como `??` | Alta | Alto: una confirmación incompleta puede perder destinos o publicar borrados sin sus reemplazos | Raíz y `Auditorias-EcoLogistica/` | PENDIENTE | Revisar el diff completo y confirmar en un único cambio posterior autorizado. |
| R-02 | Referencias Markdown de navegación actualizadas | README y documentos S1/S2 usan `Auditorias-EcoLogistica/02_*` y `03_*`; los archivos destino existen | Media | Bajo | `README.md`, `docs/03 Implementación/` | CORREGIDO | Mantener comprobación de enlaces en CI o pre-commit. |
| R-03 | Referencia textual antigua a reportes en raíz | La retrospectiva S2 afirma que los reportes están “en raíz”, aunque los enlaces son correctos | Baja | Bajo: confusión de navegación | `docs/03 Implementación/Sprint 2/04_retrospectiva_del_sprint_v_1_0_0.md` | PENDIENTE | Corregir la frase en una actualización documental posterior. |
| R-04 | Enlaces históricos dentro de auditorías | La maestra conserva rutas pre-reorganización como fuentes primarias; son contexto histórico, no enlaces operativos | Baja | Bajo | `01_Auditorias/AUDITORIA_MAESTRA_PRE_SPRINT_3.md` | PARCIAL | Añadir una nota de ubicación histórica o mantenerlo explícitamente como registro previo. |

## Matriz de contraste de hallazgos anteriores

Estados: **CORREGIDO** = evidencia estática actual suficiente; **PENDIENTE** = incumplimiento confirmado; **PARCIAL** = avance sin cierre demostrable; **NO VERIFICADO** = exige ejecución, entorno o evidencia externa no disponible.

| ID previo | Hallazgo contrastado | Evidencia actual | Prioridad | Riesgo | Ruta afectada | Estado actual | Acción recomendada |
|---|---|---|---|---|---|---|---|
| M-01 | README describía prototipo y componentes no activos | README ahora identifica `app/` y `src/`, GA propio, OSRM opcional, Redis/Celery no implementados y PWA no verificada | Crítica | Trazabilidad | `README.md` | CORREGIDO | Mantenerlo alineado con runtime. |
| M-02 | Prototipo `EcologisticaJunin/` no operativo | Directorio ausente; Git muestra sus nueve archivos como eliminados; `REPORTE_SANEAMIENTO_DOCUMENTAL.md` documenta retiro previo | Alta | Trazabilidad histórica | `EcologisticaJunin/` | PARCIAL | Consolidar la reubicación/eliminación autorizada en Git y conservar evidencia histórica suficiente. |
| M-03 | `.gitkeep` backend legado | Archivo y directorio legado ausentes | Baja | Bajo | `EcologisticaJunin/backend/.gitkeep` | CORREGIDO | Sin acción técnica adicional. |
| M-04 | `.gitkeep` frontend legado | Archivo y directorio legado ausentes | Baja | Bajo | `EcologisticaJunin/frontend/.gitkeep` | CORREGIDO | Sin acción técnica adicional. |
| M-05 | Versión/encabezado C4 y estado de arquitectura | Archivo se denomina V_1_0_6 y la documentación vigente distingue arquitectura prevista/real | Alta | Trazabilidad | `docs/01 Inicio/12. Modelo C4 V_1_0_6.md`, `docs/ESTADO_TECNICO_VIGENTE.md` | PARCIAL | Verificar coherencia completa del contenido C4, no solo encabezado. |
| M-06 | Convenciones de versiones documentales incoherentes | Persisten nombres V_1_0_0, V_1_0_3, V_1_0_4 y V_1_0_6 frente a directrices | Alta | Trazabilidad | `docs/01 Inicio/00.*`, documentos 06–13 | PENDIENTE | Definir excepción/versionado y actualizar directriz o metadatos. |
| M-07 | Enlaces Sprint 1 a raíz incorrectos | Enlaces revisados usan `../../../Auditorias-EcoLogistica/...`; destinos existen | Alta | Navegación | `docs/03 Implementación/Sprint 1/` | CORREGIDO | Añadir verificación automatizada de enlaces. |
| M-08 | Enlaces Sprint 2 al hermano Sprint 1 incorrectos | Enlaces de S2 revisados usan rutas actuales y los destinos existen | Alta | Navegación | `docs/03 Implementación/Sprint 2/` | CORREGIDO | Añadir verificación automatizada de enlaces. |
| M-09 | README enlazaba versiones S1 inexistentes | README enlaza V_1_0_1 existentes y explica sustitución de V_1_0_0 | Alta | Navegación | `README.md` | CORREGIDO | Mantener nota de trazabilidad. |
| M-10 | Arquitectura planificada contradice runtime | Documento vigente registra GA, `geometry` 4326, OSRM opcional, Redis/Celery ausentes y PWA no acreditada; decisión `geometry`/`GEOGRAPHY` sigue abierta | Crítica | Diseño/datos | Docs 10–12, `docs/ESTADO_TECNICO_VIGENTE.md` | PARCIAL | Formalizar decisión espacial y actualizar baseline histórica sin reescribirla. |
| M-11 | PWA offline declarada resuelta sin evidencia | Estado vigente y README la marcan no verificada; el historial S1 conserva formulación previa | Alta | Alcance | Docs S1, README, estado vigente | PARCIAL | Corregir explícitamente el registro histórico o anexar fe de erratas trazable. |
| M-12 | Planes/CI eran evidencia histórica en raíz | Están separados en `02_Planes_Implementacion/` y `04_Informes_CI/`, e indexados | Media | Pérdida de contexto | `Auditorias-EcoLogistica/02_*`, `04_*` | CORREGIDO | Consolidar en Git. |
| M-13 | Dos cálculos de CO2 | `leg_co2_grams` existe en `app/core/emissions.py` y `app/services/genetic_solver.py` | Alta | Métricas ambientales divergentes | Ambos módulos | PENDIENTE | Definir contrato único y pruebas de regresión antes de refactorizar. |
| M-14 | WebSocket importa helpers privados HTTP | `websockets.py` importa `_persist_solution` y `retain_other_vehicles` desde `routes.py` | Alta | Reoptimización/realtime | `app/api/v1/websockets.py`, `routes.py` | PENDIENTE | Extraer servicio de publicación/persistencia con API pública. |
| M-15 | ETA depende de privados del solver | `sequence_eta.py` importa `_build_problem` y `_schedule_vehicle` | Alta | ETA/US-009 | `app/services/sequence_eta.py`, `genetic_solver.py` | PENDIENTE | Estabilizar interfaz de solver antes de ampliar Sprint 3. |
| M-16 | Dos fuentes Python y runtime con QA | Docker/CI instalan `backend/requirements.txt`; `uv.lock` no participa; requirements incluye pytest, coverage, httpx y openpyxl | Alta | Reproducibilidad/superficie producción | `pyproject.toml`, `uv.lock`, `backend/requirements.txt`, Docker, CI | PENDIENTE | Elegir fuente de verdad, fijar versiones y separar runtime/dev. |
| M-17 | JWT/documentación/defaults demo | `AUTH_TOKEN_HOURS=12`, demo y clave conocida por defecto; no hay evidencia de perfil de producción desplegado | Crítica | Seguridad | `.env.example`, Compose, `app/core/config.py` | PARCIAL | Definir perfil producción, secretos, TTL/refresh y actualizar RNF. |
| M-18 | TLS no acreditado | Compose expone HTTP; `FORCE_HTTPS=false`; Nginx TLS es plantilla | Crítica | Confidencialidad/WSS | Compose, Nginx, docs TLS | NO VERIFICADO | Configurar y probar HTTPS/WSS en staging antes de despliegue. |
| M-19 | Gates CI/calidad incompletos | Sonar depende de variable; staging no despliega; `--cov-fail-under=0`; no hay linter/CodeQL configurado | Crítica | Calidad de entrega | CI, `pyproject.toml`, Sonar | PENDIENTE | Añadir gates progresivos, lint/seguridad, Sonar efectivo y despliegue verificable. |
| M-20 | `fetchTracking` sin consumidor | `src/api.ts` la exporta; `Tracking.tsx` consume `fetchPublicTracking`, no `fetchTracking` | Baja | API muerta | `src/api.ts` | PENDIENTE | Confirmar consumidores externos y retirar o documentar sólo tras decisión. |
| M-21 | Utilidades sin consumidor detectado | Persisten `altitude_emission_factor`, `geodesic_adjuster`, `hard_feasible`, `avoided_co2_to_quinual`; no se acreditó uso productivo | Baja | Deuda/código huérfano | `app/core/`, `app/services/`, `app/schemas/` | NO VERIFICADO | Hacer análisis de consumidores/contratos antes de eliminar. |
| M-22 | Evidencia S1/S2 parcial no equivale a cierre | Informes continúan declarando E2E, cobertura, CI, factibilidad y HTTP pendientes | Crítica | Aceptación errónea | Reportes S1/S2/EN-001 | PENDIENTE | Ejecutar validación aislada con PostGIS y archivar resultados. |

## Sprints 1 y 2: requisito, código y prueba

| Sprint | Alcance/requisitos | Código y pruebas localizadas | Estado de evidencia |
|---|---|---|---|
| Sprint 1 | US-001 a US-004, US-006 y EN-003; flota, placas, estado, importación, ventanas, JWT/RBAC | APIs de flota/pedidos/auth/restricciones, servicios dedicados y tests `test_fleet_us001.py`, `test_plate_restriction_us002.py`, `test_vehicle_state_us003.py`, `test_import_us004.py`, `test_order_window_us006.py`, `test_auth.py`, `test_security_en003.py` | PARCIAL: código y suites dedicadas existen; falta ejecución E2E PostGIS, cobertura DoD, escaneo, revisión y staging acreditados. |
| Sprint 2 | US-005, US-007, US-008, US-009 y EN-001; geocodificación, GA, restricciones duras, ETA y SLA | Servicios de geocodificación/área/solver/ETA y tests `test_geocode_us005.py`, `test_optimizer_us007.py`, `test_hard_constraints_us008.py`, `test_eta_us009.py`, `test_solver_sla_en001.py` | PARCIAL: benchmark histórico acredita tiempo del solver (~0,89 s), no factibilidad constante 150×15, HTTP total ni corrida integral PostGIS. |

## Infraestructura, dependencias, seguridad y cobertura

| Dominio | Estado actual | Riesgo/acción |
|---|---|---|
| Docker/PostGIS | Topología coherente para desarrollo: PostGIS 15-3.4, backend y Nginx; entrypoint aplica inicialización/migraciones | Validar en entorno efímero antes de Sprint 3; no hay evidencia de despliegue. |
| Migraciones | Mecanismo propio con ocho migraciones y tabla `schema_migrations`; `create_all` precede a migraciones | Riesgo de evolución no equivalente a Alembic; requiere prueba de upgrade real contra base vacía y existente. |
| CI/CD | Ejecuta pruebas/cobertura y build, pero no hay evidencia de ejecución remota verde; staging es placeholder | Bloqueo de cierre formal. |
| Cobertura | Backend tiene `--cov-fail-under=0`; Vitest cubre sólo `src/lib/**/*.ts` y hay un test frontend | No cumple un umbral DoD verificable. |
| Seguridad | JWT, bcrypt, RBAC, control de entorno y middleware HTTPS están presentes | Defaults demo y falta TLS/WSS real; no existe evidencia de SCA/OWASP/CodeQL. |
| Dependencias | Frontend declarado/lock presente; Python duplica manifiestos y usa rangos sin topes | Separar dependencias runtime/dev y usar lock efectivo en CI/Docker. |

## Duplicados, obsolescencia y dependencias a revisar (sin eliminar)

1. Duplicación confirmada: cálculo de CO2 entre `app/core/emissions.py` y `app/services/genetic_solver.py`.
2. Configuración duplicada: `pyproject.toml`/`uv.lock` frente a `backend/requirements.txt`; Docker y CI consumen sólo este último.
3. Código potencialmente no consumido: `fetchTracking` y las utilidades M-21; se mantienen como **NO VERIFICADO/PENDIENTE**, no candidatos a eliminación inmediata.
4. Documentación obsoleta: la frase de retrospectiva S2 sobre reportes en raíz; las convenciones de versión de directrices; y las fuentes históricas en auditoría maestra que mencionan rutas anteriores.
5. Dependencias de producción innecesariamente amplias: `pytest`, `pytest-asyncio`, `pytest-cov`, `httpx` y `openpyxl` se instalan en la imagen backend por `requirements.txt`; su necesidad runtime no fue demostrada estáticamente.

## Bloqueos reales para Sprint 3

**Bloquean el cierre formal y cualquier despliegue/staging:**

1. Ejecución completa y aislada contra PostGIS, incluyendo migraciones, API, WebSocket y regresión S1/S2.
2. Evidencia de factibilidad 150×15 y tiempo HTTP total para EN-001, no sólo tiempo interno del solver.
3. Quality gate reproducible: cobertura acordada, lint, análisis de seguridad/dependencias, Sonar/CodeQL y CI remoto verde.
4. TLS/WSS, secretos y perfil de producción/staging comprobados.
5. Consolidación del cambio documental en Git para preservar simultáneamente origen/destino y trazabilidad.

**No bloquean por sí solos el inicio de funcionalidades aisladas de Sprint 3:** refactor de acoplamientos M-13 a M-15, normalización de versiones documentales y revisión de utilidades sin consumidores. Sí deben tratarse antes de alterar los contratos de optimización, ETA o realtime.

## Conclusión fundamentada

La base técnica es funcionalmente reconocible y su arquitectura de desarrollo es coherente: React/Vite → Nginx → FastAPI → PostgreSQL/PostGIS. La reorganización mejora la trazabilidad y corrigió los enlaces operativos principales. No obstante, el estado verificable sigue siendo **post-Sprint 2 parcialmente acreditado**: no existe evidencia nueva de pruebas integrales, CI efectivo, cobertura exigible, seguridad de despliegue ni cumplimiento integral de EN-001. Por tanto, Sprint 3 puede comenzar sólo con un alcance que no dependa de declarar S1/S2 cerrados; la preparación técnica para evaluación, release o cierre formal es **NO APROBADA** hasta resolver los bloqueos enumerados.
