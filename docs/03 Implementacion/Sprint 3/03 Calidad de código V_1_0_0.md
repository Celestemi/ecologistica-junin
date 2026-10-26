# Evaluación de Calidad de Código — SonarQube

**Nombre del Proyecto:** EcoLogística Huancayo  
**Fecha de Análisis:** 2026-10-26  
**Versión del Análisis:** V_1_0_0

## 1. Resumen Ejecutivo de Quality Gate

- **Estado del Quality Gate:** PASSED.
- **Porcentaje de Cobertura de Pruebas (Coverage):** 61.2%.
- **Duplicación de Código:** 0.0%.

Se ejecutó SonarQube Community Build 26.10.0.133078 localmente mediante Docker Desktop y SonarScanner CLI 8.1.0.6389. El análisis usó `coverage.xml` de pytest-cov y `coverage/frontend/lcov.info` de Vitest. El Quality Gate predeterminado evaluó el código nuevo respecto de la versión anterior y registró 0 violaciones nuevas; no implica que las incidencias históricas del proyecto estén resueltas.

## 2. Métricas Principales

| Categoría | Cantidad Detectada | Severidad (Bloqueante / Alta / Media / Baja) |
|---|---|---|
| Bugs | 16 | 1 bloqueante, 3 altas (críticas), 12 medias (mayores) |
| Vulnerabilidades | 10 | 9 medias (mayores), 1 baja (menor) |
| Code Smells | 4 | 4 medias (mayores) |
| Security Hotspots | 0 | No aplica |

El análisis abarca 11,573 líneas de código (ncloc) y reporta 20 minutos de deuda técnica estimada. Se mantiene la advertencia de SonarQube sobre información de autoría SCM ausente para 17 archivos modificados; no invalida las métricas anteriores, pero limita características dependientes de blame. El análisis de dependencias (SCA) fue omitido por la edición/configuración local, por lo que estas métricas no sustituyen una auditoría de CVE de dependencias.

## 3. Plan de Remediación y Deuda Técnica

- **Deuda Técnica Estimada:** 20 minutos, según SonarQube.
- **Principales hallazgos y acciones correctivas:**
  1. **Tres bugs críticos de ordenamiento (`typescript:S2871`).** Se encuentran en `src/components/Map.tsx:83`, `src/pages/PlateRestrictions.tsx:120` y `src/components/Sidebar.tsx:178`; usan `sort()` sin comparador explícito. Acción pendiente: sustituirlos por un comparador basado en `localeCompare` y cubrir la ordenación. No se aplicó la modificación para no alterar módulos funcionales fuera del alcance de esta evaluación.
  2. **Bug bloqueante señalado por el analizador (`python:S930`) en `app/main.py:68`.** SonarQube marca `summary=app.summary` al invocar `get_openapi`. La aplicación construye y las 118 pruebas backend pasan; FastAPI admite ese argumento en la versión instalada. Se clasifica como posible falso positivo de inferencia de tipo y requiere validación/ajuste de regla antes de modificar código válido.
  3. **Diez vulnerabilidades reportadas.** Nueve (`python:S2245`) corresponden a `random.Random` en `app/services/optimizer_benchmark.py` y `app/services/genetic_solver.py`; las semillas son deliberadamente reproducibles para benchmarks y el algoritmo genético, no para secretos. Acción pendiente: revisión de seguridad y, si se confirma ese contexto, marcar como seguro en SonarQube; usar `secrets` únicamente donde se generen credenciales o tokens. La restante (`python:S5332`, baja) identifica orígenes HTTP locales en `app/core/config.py:35`; debe mantenerse solo en desarrollo y verificarse TLS en staging/producción.
  4. **Cuatro code smells (`typescript:S6671`) en `src/lib/offline.ts` (líneas 23, 33, 43 y 66).** La cola de EN-004 rechaza promesas con valores que no siempre son instancias de `Error`. Acción pendiente: normalizar los motivos de rechazo a `Error` y añadir pruebas de IndexedDB y reconexión; no se cambió el flujo offline durante esta medición.

### Evidencia ejecutada

- `docker compose exec -T backend pytest -q`: 118 pruebas aprobadas; se generó la cobertura Python importada por SonarQube.
- `npm.cmd run test:coverage`: 6 pruebas aprobadas; se generó `coverage/frontend/lcov.info` importado por SonarQube.
- `npm.cmd run build`: compilación de producción aprobada.
- `npm.cmd audit --omit=dev --json`: 0 vulnerabilidades reportadas en dependencias de producción frontend.
- `docker compose exec -T backend pip check`: sin requisitos Python rotos.
- Escaneo final: análisis procesado correctamente por SonarQube local; Quality Gate `OK`/PASSED.
