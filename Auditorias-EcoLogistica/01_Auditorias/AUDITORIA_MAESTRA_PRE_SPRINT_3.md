# AUDITORIA_MAESTRA_PRE_SPRINT_3

**Proyecto:** EcoLogística Huancayo — DistriRápido S.A.C.  
**Fecha:** 26 de octubre de 2026  
**Modalidad:** consolidación de auditorías y verificación selectiva, sin ejecutar pruebas, builds, migraciones, instalaciones ni modificar el código.  
**Fuentes primarias:** `Auditorias-EcoLogistica/AUDITORIA_01_ESTADO_REPOSITORIO.md`, `AUDITORIA_02_DOCUMENTACION.md`, `AUDITORIA_03_CODIGO_ARQUITECTURA.md` y `AUDITORIA_04_ESTABILIDAD.md`.  
**Evidencia complementaria:** informes versionados de DoD/QA, CI y rendimiento en la raíz del repositorio, y verificación estática puntual de rutas y configuraciones citadas abajo.

## Alcance, evidencia y límite de certeza

Las cuatro auditorías requeridas están presentes y fueron usadas. Esta auditoría no vuelve a ejecutar pruebas: la suite crea y reinicializa `ecologistica_test`, y la restricción de conservación del estado excluye esa operación. Por ello, un resultado histórico de prueba se trata como evidencia fechada, no como estado ejecutado nuevamente hoy.

No se identificó ningún hecho que justifique eliminar código o documentación de forma inmediata. Las recomendaciones de archivo o eliminación son propuestas futuras condicionadas a las verificaciones expresadas en cada hallazgo.

## Fase 1 — Estado general

### 1. Arquitectura actual

La aplicación operativa es la ubicada en la raíz del repositorio:

```text
React + TypeScript + Vite (`src/`, `index.html`)
  → Nginx (`frontend/nginx.conf`)
  → FastAPI (`app/main.py`, routers v1)
  → SQLAlchemy async + PostgreSQL 15/PostGIS 3.4
```

`docker-compose.yml` orquesta los servicios `db`, `backend` y `frontend`; `backend/entrypoint.sh` espera la base y ejecuta la inicialización/migraciones internas. El backend separa routers (`app/api/v1`), dominio/ORM, schemas, servicios, configuración y datos geográficos. El frontend activo está en `src/`, no en el subárbol con igual nombre del proyecto.

La arquitectura es coherente para un MVP: frontend, API, persistencia y servicios están separados. Sus límites de mantenibilidad son claros: `app/services/genetic_solver.py` concentra demasiadas responsabilidades; `app/api/v1/routes.py` mezcla transporte, persistencia y lógica; WebSocket consume helpers privados de HTTP; y ETA consume helpers privados del solver.

### 2. Organización del repositorio

| Área | Estado verificable | Dictamen |
|---|---|---|
| `app/` | Backend FastAPI activo, importado por entrada, Docker y tests. | CONSERVAR |
| `src/` | Frontend React/TypeScript activo, compilado por Vite/Docker. | CONSERVAR |
| `tests/` y `src/lib/orderWindow.test.ts` | 21 módulos Python y una prueba Vitest; CI los invoca. | CONSERVAR |
| `backend/`, `frontend/`, `docker-compose.yml` | Infraestructura activa. | CONSERVAR |
| `docs/` | Baselines, planificación, entregables y evidencia. | CONSERVAR / ACTUALIZAR selectivamente |
| `EcologisticaJunin/` | Prototipo independiente, no usado por Docker, CI, tests ni imports. | CANDIDATO A ARCHIVAR |
| `Auditorias-EcoLogistica/` | Evidencia de auditoría, incluida esta consolidación. | CONSERVAR |

No se reportaron caches, builds, logs, backups o temporales versionados. El estado Git registrado por Auditoría 01 era limpio; esta auditoría no ejecutó operaciones Git modificadoras.

### 3. Estado documental

La documentación tiene buena cobertura y trazabilidad académica, pero carece de una fuente única de estado técnico vigente. El problema no es la cantidad de documentos, sino la mezcla de baselines, planes históricos, resultados y afirmaciones de arquitectura que ya no describen el runtime.

Las fuentes oficiales recomendadas por dominio son: requisitos/reglas (`docs/01 Inicio/06`, `07`, `09`), backlog y DoD (`docs/02 Planificacion/01...`), arquitectura objetivo (`10`, `11`, `12`), estado técnico real S2 (`VERIFICACION_FINAL_SPRINT_2.md`), rendimiento (`REPORTE_RENDIMIENTO_EN_001.md`) y estado/incidencias de cada Sprint en sus respectivos documentos.

### 4. Estado de Sprints 1 y 2

Sprint 1 está implementado estáticamente para US-001, US-002, US-003, US-004, US-006 y parcialmente EN-003; conserva pruebas dedicadas. Sin embargo, `REPORTE_VERIFICACION_DOD_SPRINT_1.md` concluye que no acreditó DoD global: sin E2E PostGIS verde, cobertura >=80 % en backend/frontend, Quality Gate/CodeQL, peer review y staging exitoso.

Sprint 2 implementa estáticamente US-005, US-007, US-008, US-009 y EN-001, pero su cierre es parcial. `VERIFICACION_FINAL_SPRINT_2.md` registró 34 PASS, 2 FAIL de fixtures y 13 errores de setup por ausencia de PostGIS; `REPORTE_AUDITORIA_CI.md` registra la corrección focal posterior de esos dos fixtures y cuatro pruebas PASS. Eso no sustituye una corrida completa con PostGIS ni evidencia de GitHub Actions verde. EN-001 acreditó tiempo del solver (~0,89 s promedio en 150×15), no una solución factible constante 150×15 ni tiempo HTTP total.

### 5. Calidad del código

Hay separación de responsabilidades razonable en la mayoría de servicios y modelos. Son positivos `route_constraints.py`, servicios pequeños de RBAC/placa/ventana/estado y el aislamiento explícito de pruebas. La calidad queda limitada por alta complejidad y acoplamientos internos no contractuales:

- `app/services/genetic_solver.py` reúne matriz, geometría, GA, evaluación, restricciones, ETA y serialización.
- `app/api/v1/routes.py` reúne endpoints, consultas, persistencia y reglas.
- `app/api/v1/websockets.py` importa `_persist_solution` y `retain_other_vehicles` desde `routes.py`.
- `app/services/sequence_eta.py` usa `_build_problem` y `_schedule_vehicle` del solver.
- El cálculo de CO₂ existe tanto en `app/core/emissions.py` como en `app/services/genetic_solver.py`.

No hay evidencia de dependencias frontend claramente sin uso. `tzdata` no tuvo import directo detectado, pero puede ser transitiva/necesaria para zonas horarias: no debe retirarse sin prueba controlada.

### 6. Pruebas existentes

Existen pruebas de API, auth/RBAC, flota, restricciones de placa, estados, importación, ventanas, geocodificación, solver, restricciones duras, ETA, rendimiento, PDF, tiempo real y migraciones. La configuración usa Pytest/Coverage y Vitest/V8; CI define backend con PostGIS, frontend, Sonar condicional y un job de staging manual.

La evidencia histórica es insuficiente para declarar regresión completa: cobertura backend histórica aproximada 50–58 %, frontend sin medición archivada >=80 %, `--cov-fail-under=0`, Sonar/CodeQL sin ejecución acreditada y cobertura baja/no confirmada en routers, WebSocket, importación, realtime/PDF y middleware de seguridad.

### 7. Seguridad

Controles presentes: JWT HS256 con expiración, bcrypt, RBAC, bloqueo tras tres intentos, token opaco de tracking, validación central de secreto fuera de demo y validación Pydantic. Los tests fuerzan base `ecologistica_test` y validan ese nombre antes de operaciones destructivas.

Brechas verificadas o no acreditadas:

- `docker-compose.yml` y `.env.example` contienen valores previsibles solo apropiados para desarrollo; `APP_ENVIRONMENT=demo`, cuentas demo y `FORCE_HTTPS=false` son valores por defecto.
- Nginx activo opera HTTP; TLS queda en `frontend/nginx-ssl.conf.example` y no hay despliegue TLS acreditado.
- WebSocket lleva token en query string y no hay evidencia de control de Origin, rate limiting o pruebas dinámicas de abuso.
- No hay ejecución acreditada de Sonar, CodeQL, OWASP ni escaneo de dependencias; `REPORTE_AUDITORIA_CI.md` anotó históricamente cinco vulnerabilidades transitivas de npm sin evidencia posterior de resolución.
- La documentación menciona JWT de 15 minutos mientras `app/core/config.py` usa 12 horas por defecto.

### 8. Preparación para Sprint 3

**Preparado condicionalmente para iniciar desarrollo funcional**, porque hay una base de mapa, GeoJSON, secuencia/ETA, tracking y cálculos ambientales. **No preparado para evaluación formal, declaración de cierre ni para ignorar deuda heredada.**

Antes de comprometer historias que dependan de resultados de S2 deben reservarse capacidad y criterios de salida para: E2E con PostGIS, cobertura/gates, escaneo de seguridad, CI real, decisión OSRM/ETA, validación de EN-001 y corrección documental. Los bloqueos no impiden escribir código S3 aislado, pero sí bloquean afirmar calidad integral o cierre de S1/S2/S3.

## Fase 2 — Matriz maestra de limpieza

| ID | Ruta exacta | Tipo | Problema identificado y evidencia | Referencias/dependencias | Acción | Riesgo del cambio | Prioridad | Confianza |
|---|---|---|---|---|---|---|---|---|
| M-01 | `README.md` | Markdown | Presenta `EcologisticaJunin/` como «Código Fuente» y lista OR-Tools/DEAP/Celery/Redis/PWA; el runtime activo es `app/` + `src/`, sin esas dependencias/servicios. | Enlaces de onboarding; `sonar-project.properties`; Docs 10/12. | ACTUALIZAR | Medio: enlaces/documentación de evaluación. | Crítica | Alta |
| M-02 | `EcologisticaJunin/` | Árbol Python/JS | MVP CRUD en memoria; no figura en Compose, CI, tests ni imports. Solo README lo referencia y Sonar lo excluye. | `README.md`; posible valor académico/histórico. | ARCHIVAR | Alto si se elimina trazabilidad. | Alta | Alta |
| M-03 | `EcologisticaJunin/backend/.gitkeep` | Archivo vacío | Directorio no vacío; no aporta estructura por sí mismo. | Decisión M-02. | CANDIDATO A ELIMINAR | Bajo técnico; no hacerlo aislado del archivo histórico. | Baja | Alta |
| M-04 | `EcologisticaJunin/frontend/.gitkeep` | Archivo vacío | Mismo caso M-03. | Decisión M-02. | CANDIDATO A ELIMINAR | Bajo técnico. | Baja | Alta |
| M-05 | `docs/01 Inicio/12. Modelo C4 V_1_0_6.md` | Markdown | Nombre V_1_0_6, encabezado V_1_0_3; arquitectura describe componentes no evidenciados como actuales. | Directrices 00; README; Docs 10/11; S2. | CORREGIR | Bajo técnico, medio de trazabilidad. | Alta | Alta |
| M-06 | `docs/01 Inicio/00. Directrices y Auditoria V_1_0_3.md` | Markdown | Exige nombres V_1_0_3 para RF/RNF/C4/restricciones, pero archivos reales usan V_1_0_0, V_1_0_6 y V_1_0_4. | Docs 06–13. | ACTUALIZAR | Bajo. | Alta | Alta |
| M-07 | `docs/03 Implementación/Sprint 1/*.md` | Markdown | Cuatro documentos usan `../../` a raíz; desde `Sprint 1/` se requiere `../../../`. | README, plan S1, DoD S1. | CORREGIR | Bajo; verificar cada enlace. | Alta | Alta |
| M-08 | `docs/03 Implementación/Sprint 2/*.md` | Markdown | Enlaces a S1 omiten el directorio hermano `Sprint 1/`. | Cuatro documentos S2; informes S1. | CORREGIR | Bajo. | Alta | Alta |
| M-09 | `README.md` | Markdown | Enlaza cuatro versiones S1 V_1_0_0 que no existen; las V_1_0_1 indican sustitución. | `docs/03 Implementación/Sprint 1/`. | CORREGIR | Bajo; recuperar versiones antiguas antes de borrar referencias históricas. | Alta | Alta |
| M-10 | `docs/01 Inicio/10. Stack tecnológico V_1_0_3.md`; `docs/01 Inicio/11. Base de datos V_1_0_3.md`; `docs/01 Inicio/12. Modelo C4 V_1_0_6.md` | Markdown | Conflictos: OR-Tools/DEAP vs GA propio, GEOGRAPHY vs `geometry` 4326, OSRM/PWA como activos vs opcionales/no acreditados. | `PLAN_IMPLEMENTACION_SPRINT_2.md`; `VERIFICACION_FINAL_SPRINT_2.md`; manifests. | ACTUALIZAR | Medio: no reescribir baseline sin marcar objetivo/real. | Crítica | Alta |
| M-11 | `docs/03 Implementación/Sprint 1/02_registro_de_impedimentos_v_1_0_1.md` | Markdown | Declara resuelta PWA offline/IndexedDB/Service Workers; S2 deja EN-004 fuera de alcance/no verificado. | Docs 10; S2; EN-004. | CORREGIR | Medio: historial debe conservar afirmación original y su corrección. | Alta | Alta |
| M-12 | `PLAN_IMPLEMENTACION_SPRINT_1.md`; `PLAN_IMPLEMENTACION_SPRINT_2.md`; `REPORTE_AUDITORIA_CI.md` | Markdown | Planes retrospectivos y auditoría de correcciones pasadas: útiles como evidencia, no como estado actual. | QA S1/S2, README. | ARCHIVAR | Bajo si quedan indexados; alto si se pierden decisiones. | Media | Alta |
| M-13 | `app/services/genetic_solver.py`; `app/core/emissions.py` | Python | Dos implementaciones de `leg_co2_grams`; la de core incorpora ajuste que solver no necesariamente comparte. | PDF, API, optimización, pruebas de emisiones. | REFAC TORIZAR | Alto: cambia métricas de CO₂ y resultados. | Alta | Alta |
| M-14 | `app/api/v1/routes.py`; `app/api/v1/websockets.py` | Python | WebSocket depende de helpers privados de router HTTP; acoplamiento inverso. | Reoptimización, persistencia, realtime. | REFAC TORIZAR | Alto: puede romper publicación/reoptimización. | Alta | Alta |
| M-15 | `app/services/genetic_solver.py`; `app/services/sequence_eta.py` | Python | ETA usa `_build_problem` y `_schedule_vehicle`, APIs privadas del solver. | Recálculo ETA, US-009. | REFAC TORIZAR | Alto. | Alta | Alta |
| M-16 | `pyproject.toml`; `uv.lock`; `backend/requirements.txt`; `backend/Dockerfile`; `.github/workflows/ci.yml` | Configuración | Dos manifiestos Python; Docker/CI instalan requirements y no consumen `uv.lock`; requirements mezcla runtime y QA, rangos sin topes. | Imagen backend, CI, reproducibilidad. | FUSIONAR | Alto: afecta builds y CI. | Alta | Alta |
| M-17 | `app/core/config.py`; `.env.example`; `docker-compose.yml`; `docs/01 Inicio/07. Requisitos no funcionales V_1_0_0.md` | Config/Markdown | JWT 12 h por defecto vs referencia documental de 15 min; defaults demo/secret conocidos solo seguros localmente. | Auth, TLS, despliegue. | CORREGIR | Alto si se cambia TTL sin UX/refresh. | Crítica | Alta |
| M-18 | `frontend/nginx.conf`; `frontend/nginx-ssl.conf.example`; `docker-compose.yml`; `docs/deploy/TLS_VERIFICACION.md` | Nginx/YAML/Markdown | HTTP activo, TLS solo plantilla y `FORCE_HTTPS=false`; no hay evidencia de TLS desplegado. | WebSocket, URLs, proxy/staging. | REQUIERE VERIFICACIÓN | Alto: cambios de protocolo afectan cliente y WSS. | Crítica | Alta |
| M-19 | `.github/workflows/ci.yml`; `pyproject.toml`; `sonar-project.properties` | YAML/TOML/properties | Sonar condicional/no ejecutado, staging es placeholder, cobertura gate es 0, CodeQL/linter ausentes. | DoD, cobertura, secretos externos. | ACTUALIZAR | Medio/alto: puede bloquear pipeline inicialmente. | Crítica | Alta |
| M-20 | `src/api.ts` | TypeScript | `fetchTracking` no tiene consumidor productivo detectado; existe `fetchPublicTracking` usado para seguimiento. | Endpoint interno/futuras pantallas. | REQUIERE VERIFICACIÓN | Bajo/medio: posible consumidor externo. | Baja | Media |
| M-21 | `app/core/emissions.py`; `app/services/routing_matrix.py`; `app/services/route_constraints.py`; `app/schemas/logistics.py` | Python | `altitude_emission_factor`, `geodesic_adjuster`, `hard_feasible`, `avoided_co2_to_quinual` sin referencias productivas detectadas. | Contratos externos, material docente, futuras historias. | REQUIERE VERIFICACIÓN | Medio. | Baja | Media |
| M-22 | `REPORTE_VERIFICACION_DOD_SPRINT_1.md`; `VERIFICACION_FINAL_SPRINT_2.md`; `REPORTE_RENDIMIENTO_EN_001.md` | Markdown | Resultados parciales son evidencia válida, pero no certifican DoD, E2E, factibilidad 150×15 o HTTP. | DoD; CI; PostGIS. | CONSERVAR | Alto si se confunden con certificación; no deben borrarse. | Crítica | Alta |

## Fase 3 — Documentación

### Redundancia, obsolescencia e incompletitud

No son redundantes para eliminar los informes oficiales de Sprint, QA, rendimiento y planes: tienen propósitos distintos (estado, intención, evidencia o decisión). Sí se repite el estado de las brechas S1/S2. La repetición debe resolverse por jerarquía de fuente, no por borrado.

| Clase | Rutas | Diagnóstico específico | Tratamiento |
|---|---|---|---|
| Redundancia legítima | Informes S1/S2, planes S1/S2, QA/DoD/rendimiento | Comparten brechas, pero cada uno aporta evidencia distinta. | CONSERVAR; enlazar a fuente primaria. |
| Obsoleta frente al runtime | `README.md`, Docs 10 y 12 | Describen prototipo/OR-Tools/DEAP/Redis/Celery/OSRM/PWA como vigentes. | ACTUALIZAR distinguiendo objetivo, implementado y pendiente. |
| Contradictoria | Doc 11 y plan/verificación S2 | `GEOGRAPHY` previsto versus `geometry` 4326 implementado/documentado para S2. | ACTUALIZAR tras decisión arquitectónica. |
| Incompleta | `docs/deploy/TLS_VERIFICACION.md`, `docs/qa/COMANDOS_CALIDAD.md` | Sin evidencia de TLS activo; comandos QA deben advertir que pruebas escriben en BD de test. | ACTUALIZAR. |
| Sin propósito operativo claro | `EcologisticaJunin/` como código referenciado en README | Es prototipo, no runtime; su propósito histórico no está declarado. | ARCHIVAR con manifiesto histórico, no eliminar aún. |
| Temporal/histórica | `REPORTE_AUDITORIA_CI.md`; planes S1/S2 | Documentan una fotografía y correcciones pasadas; no son estado actual. | ARCHIVAR históricamente y mantener índice. |
| Versionamiento contradictorio | Docs 00 y 12; README enlaces S1 | V_1_0_6/V_1_0_3, convenciones variadas y destinos V_1_0_0 ausentes. | CORREGIR enlaces/metadatos; recuperar desde Git si la historia debe preservarse. |

### Archivos que podrían archivarse o eliminarse posteriormente

- `EcologisticaJunin/`: **ARCHIVAR**, no eliminar. Su contenido es una evidencia del MVP inicial y `README.md` lo enlaza. Puede preservarse como snapshot histórico con una nota de no-ejecución; su funcionalidad ya está representada operacionalmente por `app/` y `src/`.
- `PLAN_IMPLEMENTACION_SPRINT_1.md` y `PLAN_IMPLEMENTACION_SPRINT_2.md`: **ARCHIVAR**, no fusionar ni eliminar. Su contenido contiene decisiones, supuestos y desviaciones que no sustituyen los informes de resultado.
- `REPORTE_AUDITORIA_CI.md`: **ARCHIVAR**, no eliminar. Preserva causa raíz de migraciones y lockfile; no debe usarse para afirmar CI remoto verde.
- `EcologisticaJunin/backend/.gitkeep` y `EcologisticaJunin/frontend/.gitkeep`: candidatos a eliminar **solo si** se confirma que el árbol legado se archiva/conserva sin requerir esos placeholders. Aportan cero contenido propio, pero no justifican una modificación aislada.

Todos los documentos de `docs/01 Inicio/`, los informes oficiales de Sprints, las evidencias Jira, `REPORTE_VERIFICACION_DOD_SPRINT_1.md`, `VERIFICACION_FINAL_SPRINT_2.md` y `REPORTE_RENDIMIENTO_EN_001.md` deben conservarse. Son baseline, evidencia de decisión, alcance o limitaciones; no hay base para eliminarlos.

## Fase 4 — Código y configuración

### Legado y duplicación

El único legado confirmado es `EcologisticaJunin/`: FastAPI CRUD en memoria y React JSX mínimo. No es el origen activo, no tiene dependencia operacional y no debe borrarse sin protección histórica. La única duplicación funcional confirmada dentro de código activo es el cálculo de CO₂ (M-13). La ruta `/vehiculos` y `/flota` no es duplicación: una sirve operación/ruteo y la otra administración/historial.

### Módulos aparentemente innecesarios

No hay módulo que pueda declararse innecesario con certeza. M-20 y M-21 son utilidades sin consumidor productivo detectado, por lo que su estado correcto es **REQUIERE VERIFICACIÓN**, no eliminación. También `tests/__init__.py` se conserva: aunque vacío, puede mantener comportamiento de paquete/importación.

### Dependencias y configuraciones

Las dependencias frontend declaradas sí tienen uso estático. En Python, no se demostró dependencia sin uso inequívoca; `tzdata` requiere comprobación de runtime. La deuda está en las dos fuentes de instalación: `pyproject.toml`/`uv.lock` y `backend/requirements.txt`. Docker y CI instalan el segundo, de modo que el lock Python no asegura la imagen. Además se envían herramientas QA a producción.

### Riesgos de regresión y compatibilidad

- No refactorizar solver/ETA ni HTTP/WebSocket sin pruebas de recálculo, publicación y reoptimización.
- No unificar emisiones sin contrato de resultados y pruebas API/PDF/solver.
- No tocar migraciones manuales ni `create_all` sin upgrade real PostGIS: hubo una corrección de bloques `DO $$` y existe prueba de regresión específica, pero falta validación integral.
- No cambiar TTL JWT, HTTPS o CORS sin validar frontend, proxy, WebSocket y sesión.
- Mantener `route_constraints.py`, migraciones internas, `app/data/operating_area_dev.geojson`, lockfiles, Dockerfiles y manifests hasta completar el plan de validación.

## Fase 5 — Plan de acción futuro

Las etapas describen trabajo posterior; no se ejecutaron en esta auditoría.

| Etapa | Cambios futuros | Verificar antes | Verificar después | Clasificación |
|---|---|---|---|---|
| 1. Riesgo bajo | Corregir enlaces M-07/M-08/M-09, encabezado M-05, y señalar estado histórico de planes/CI. | Inventario de destinos y enlaces desde README/Sprints. | Navegación Markdown completa; ninguna evidencia pierde enlace. | Imprescindible antes de documentación S3. |
| 2. Corrección documental | Actualizar README; separar arquitectura objetivo/implementada/pendiente; decidir `geometry`/`GEOGRAPHY`; corregir PWA y JWT. | Aprobación de responsables de requisitos/arquitectura; contrastar con código y S2. | Una fuente primaria por dominio y sin afirmar capacidades no implementadas. | Imprescindible antes de evaluar S3. |
| 3. Consolidación de código | Extraer servicio de publicación común HTTP/WS; formalizar interfaz solver–ETA; luego modularizar solver y unificar emisiones. | Suite E2E disponible y casos de regresión de rutas, ETA, PDF, WS y CO₂ escritos. | API/WS conservan payload y estado; resultados y métricas no cambian salvo decisión aprobada. | Mejora importante; modularización completa puede esperar si se congela contrato. |
| 4. Seguridad | Elegir perfiles demo/staging/prod; configurar secretos, TLS/WSS, origen WS, rate limiting; evaluar dependencias/OWASP. | Diseño de despliegue/staging, dominios, estrategia de sesión/refresh. | HTTPS real, pruebas de redirect/WSS, scanner con hallazgos resueltos/aceptados y secretos fuera de defaults. | Imprescindible para staging/evaluación; no necesariamente para codificar UI local. |
| 5. Validación funcional | Levantar PostGIS aislado; ejecutar suite completa, migraciones en BD de prueba, frontend coverage, benchmark HTTP 150×15, CI real y peer review. | BD de prueba desechable, variables seguras, versión de dependencias fijada. | Evidencia archivada: suite verde, >=80 % o DoD revisada formalmente, factibilidad 150×15, tiempo HTTP, CI/staging. | Bloqueante para cierre formal y para depender de S2 sin reservas. |
| 6. Herramientas S3 | Activar Sonar o CodeQL, linter Python/TS, gate de cobertura progresivo, artifacts, etiqueta de baseline y matriz requisito→evidencia. | Pipeline verde de base; tokens/secretos de herramientas. | PR reporta análisis, cobertura y trazabilidad; baseline S2 explícitamente marcado parcial. | Imprescindible para evaluación formal de S3. |

### Prioridad de correcciones

**Imprescindibles antes de declarar Sprint 3 preparado formalmente:** M-01, M-05 a M-11, M-17 a M-19, suite PostGIS completa, CI real, seguridad/Quality Gate, medición HTTP y factibilidad válida de EN-001.

**Puede esperar sin borrar deuda, si S3 no altera esos contratos:** archivado físico de M-02, eliminación condicional de M-03/M-04, modularización extensa M-13 a M-15, y evaluación de M-20/M-21. Los cambios de bajo riesgo documentales deben preceder cualquier limpieza física.

## Fase 6 — Veredicto

1. **¿La arquitectura es coherente?** Sí, para un MVP: React/Vite → Nginx → FastAPI → PostGIS, con módulos razonablemente separados. No está suficientemente desacoplada para refactors grandes sin red de regresión.
2. **¿Existen archivos innecesarios?** No hay evidencia para declarar eliminación inmediata. El árbol `EcologisticaJunin/` no es operativo y es el principal candidato a archivo; sus `.gitkeep` son candidatos condicionales.
3. **¿Qué podría eliminarse después?** Solo `EcologisticaJunin/backend/.gitkeep` y `EcologisticaJunin/frontend/.gitkeep`, tras resolver el archivo histórico. Las utilidades M-20/M-21 requieren análisis de consumidores. El prototipo debe archivarse antes de considerar eliminación.
4. **¿Hay documentos redundantes?** Hay repetición de brechas y estado, pero principalmente trazabilidad legítima. No deben fusionarse/eliminarse informes oficiales, planes, QA o rendimiento; debe definirse una jerarquía de fuentes.
5. **¿Qué documentación debe actualizarse?** `README.md`; Docs 00, 10, 11, 12; los cuatro S1 y cuatro S2 por enlaces; el impedimento S1 de PWA; QA/TLS; requisitos/RNF/JWT según decisión aprobada.
6. **¿Hay legado para archivar?** Sí: `EcologisticaJunin/`, preservando su snapshot y corrigiendo antes las referencias de README.
7. **¿Sprints 1 y 2 están suficientemente acreditados?** Implementados estáticamente y parcialmente probados, pero no acreditados contra DoD global. S1 no cerró E2E/cobertura/scan/review/staging; S2 mantiene la misma brecha y EN-001 parcial.
8. **¿Hay bloqueos para Sprint 3?** Para inicio funcional, no absolutos si se reserva saneamiento. Para evaluación formal, cierre o dependencia confiada de S2, sí: E2E PostGIS, cobertura/gates, CI/staging, seguridad y EN-001 válido/HTTP siguen bloqueando.
9. **¿Qué correcciones se priorizan?** Veracidad documental/links, decisión tecnológica y de datos, configuración de seguridad/deploy, validación integral y gates; luego consolidación de servicios y solver.
10. **¿Cuál es el orden más seguro?** Corregir documentación de bajo riesgo → establecer fuentes de verdad y decisiones → validar con PostGIS/CI → habilitar seguridad y quality gates → refactorizar con pruebas → archivar legado y retirar candidatos ya verificados.

## Dictamen final

El repositorio es una base técnicamente viable para Sprint 3, pero su estado correcto es **“implementación post-Sprint 2 con calidad y trazabilidad pendientes”**, no “Sprints 1 y 2 formalmente cerrados”. Ninguna limpieza destructiva está justificada hoy. La primera limpieza segura es documental y reversible; la consolidación de código y el archivo físico del legado deben hacerse solo después de disponer de la validación funcional y de una decisión de gobernanza documental.

