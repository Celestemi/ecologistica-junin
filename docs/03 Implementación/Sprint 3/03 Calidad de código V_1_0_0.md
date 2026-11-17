# Evaluación de Calidad de Código — SonarQube

<!-- complemento-r4:inicio -->
> **Complementación documental r4 — 17/11/2026.** El apartado siguiente aporta propuestas y datos simulados para completar vacíos. No declara nuevas pruebas, gastos ni aprobaciones reales. [Escenario común](../../COMPLEMENTO_CONTEXTUAL_DEL_PROYECTO.md).

## Complementación r4: ficha de análisis y tratamiento de hallazgos

Se propone una nueva ventana de análisis del 23 al 25/11/2026, con QA/DevOps como responsables funcionales. No se asigna una fecha ficticia al escaneo histórico. La ficha de la próxima ejecución debe contener versión/commit, fecha/hora, herramienta/versión, configuración, exclusiones justificadas, denominadores, gate y exportación íntegra.

| Grupo de hallazgos históricos | Tratamiento propuesto | Criterio de salida |
|---|---|---|
| Ordenación sin comparador | Revisar el orden requerido y usar comparación explícita si aplica. | Caso representativo y revisión del resultado. |
| Posible falso positivo en OpenAPI | Contrastar firma de la dependencia instalada y explicar contexto. | Decisión de revisión registrada; no ocultar el aviso sin motivo. |
| PRNG del algoritmo | Separar aleatoriedad de simulación de generación de secretos. | Revisión contextual con fuente y uso identificado. |
| HTTP local | Mantener perfil demo explícito y validar HTTPS en entorno de entrega. | Comprobación del entorno; no inferir TLS del código. |
| Rechazos de cola offline | Normalizar errores y probar persistencia/reconexión. | Sin pérdida ni duplicado y mensajes recuperables. |

Las métricas y conteos originales no se modifican: no hay nueva corrida SonarQube en r4. La información SCM faltante se completa mediante versionado y revisión reales cuando se integren cambios, sin inventar autoría.
<!-- complemento-r4:fin -->

---


> **Aclaración r3 — 17/11/2026:** las cifras SonarQube de este documento pertenecen a un registro anterior. No se reejecutó el analizador ni se confirmó su Quality Gate sobre el árbol actual. La evidencia nueva es [Vitest/V8](../../evidencias/2026-11-17/frontend.json): 86/86 casos, 81,35 % de líneas y 73,93 % de ramas frontend. Son métricas de herramienta y alcance diferentes; no sustituyen el 82,1 % global histórico ni se promedian con él.

**Versión documental:** V_1_1_0

**Nombre del Proyecto:** EcoLogística Huancayo  
**Fecha de Análisis:** fecha exacta del escaneo histórico no acreditada en este documento; aclaración documental del 17/11/2026.
**Versión del Análisis:** V_1_1_0

## 1. Resumen del Quality Gate reportado históricamente

- **Estado del Quality Gate:** PASSED (`OK`).
- **Porcentaje de Cobertura Global (Coverage):** 82.1%.
- **Cobertura de Líneas:** 85.4%.
- **Cobertura de Ramas:** 69.7%.
- **Cobertura de Código Nuevo:** 82.0%.
- **Duplicación de Código:** 0.0%.

El registro anterior declara SonarQube Community Build 26.10.0.133078 localmente mediante Docker Desktop y SonarScanner CLI 8.1.0.6389, con 125 archivos y reportes `coverage.xml` de pytest-cov y `coverage/frontend/lcov.info` de Vitest desde `/usr/src`. Registra 82.0% de cobertura en código nuevo, 0.0% de duplicación y 0 violaciones nuevas. La actualización r3 no recuperó una exportación autenticada que permita verificar ese escaneo ni su fecha; se conserva como antecedente declarado. Su gate no acredita resolución de las 30 incidencias históricas.

### Comparación con el análisis anterior

| Métrica | Referencia histórica anterior | Análisis histórico registrado | Variación reportada |
|---|---:|---:|---:|
| Cobertura global | 62.0% | **82.1%** | +20.1 pp |
| Cobertura de líneas | 61.7% | **85.4%** | +23.7 pp |
| Cobertura de ramas | 63.2% | **69.7%** | +6.5 pp |
| Cobertura de código nuevo | 65.3% | **82.0%** | +16.7 pp |
| Duplicación | 0.0% | **0.0%** | Sin cambio |

La mejora proviene de pruebas reales del frontend para páginas operativas, seguimiento público, despacho, barra lateral, modo conductor y mapas. La cobertura frontend medida por Vitest alcanzó 90.91%; SonarQube combina esta medición con la cobertura del backend y obtiene 82.1% global.

## 2. Métricas Principales

| Categoría | Cantidad Detectada | Severidad (Bloqueante / Alta / Media / Baja) |
|---|---|---|
| Bugs | 16 | 1 bloqueante, 3 altas (críticas), 12 medias (mayores) |
| Vulnerabilidades | 10 | 9 medias (mayores), 1 baja (menor) |
| Code Smells | 4 | 4 medias (mayores) |
| Security Hotspots | 0 | No aplica |

El análisis abarca 11,791 líneas de código (ncloc), 7,674 líneas cubribles y 2,065 condiciones. Permanecen sin cubrir 1,121 líneas y 626 condiciones. SonarQube reporta 20 minutos de deuda de mantenibilidad, 100 minutos de esfuerzo de remediación de confiabilidad y 120 minutos de remediación de seguridad.

Calificaciones actuales:

- **Confiabilidad:** E (`reliability_rating = 5.0`).
- **Seguridad:** C (`security_rating = 3.0`).
- **Mantenibilidad:** A (`sqale_rating = 1.0`).

Se mantiene la advertencia sobre información de autoría SCM ausente en los archivos nuevos o todavía no versionados. No invalida cobertura ni incidencias, pero limita las funciones dependientes de `git blame`. El análisis de dependencias SCA fue omitido por la edición/configuración local, por lo que estas métricas no sustituyen una auditoría de CVE.

## 3. Plan de Remediación y Deuda Técnica

- **Deuda Técnica Estimada:** 20 minutos, según SonarQube.
- **Principales hallazgos y acciones correctivas:**
  1. **Tres bugs críticos de ordenamiento (`typescript:S2871`).** Se encuentran en `src/components/Map.tsx:83`, `src/pages/PlateRestrictions.tsx:120` y `src/components/Sidebar.tsx:178`; usan `sort()` sin comparador explícito. Acción pendiente: sustituirlos por un comparador basado en `localeCompare` y cubrir la ordenación. No se aplicó la modificación para no alterar módulos funcionales fuera del alcance de esta evaluación.
  2. **Bug bloqueante señalado por el analizador (`python:S930`) en `app/main.py:68`.** SonarQube marca `summary=app.summary` al invocar `get_openapi`. La aplicación construye y las 136 pruebas backend pasan; FastAPI admite ese argumento en la versión instalada. Se clasifica como posible falso positivo de inferencia de tipo y requiere validación/ajuste de regla antes de modificar código válido.
  3. **Diez vulnerabilidades reportadas.** Nueve (`python:S2245`) corresponden a `random.Random` en `app/services/optimizer_benchmark.py` y `app/services/genetic_solver.py`; las semillas son deliberadamente reproducibles para benchmarks y el algoritmo genético, no para secretos. Acción pendiente: revisión de seguridad y, si se confirma ese contexto, marcar como seguro en SonarQube; usar `secrets` únicamente donde se generen credenciales o tokens. La restante (`python:S5332`, baja) identifica orígenes HTTP locales en `app/core/config.py:35`; debe mantenerse solo en desarrollo y verificarse TLS en staging/producción.
  4. **Cuatro code smells (`typescript:S6671`) en `src/lib/offline.ts` (líneas 23, 33, 43 y 66).** La cola de EN-004 rechaza promesas con valores que no siempre son instancias de `Error`. Acción pendiente: normalizar los motivos de rechazo a `Error` y añadir pruebas de IndexedDB y reconexión; no se cambió el flujo offline durante esta medición.

### Evidencia ejecutada

- Backend completo: 136 pruebas aprobadas; `coverage.xml` fue importado por SonarQube.
- `npm.cmd run test:coverage`: 67 pruebas frontend aprobadas; se generó `coverage/frontend/lcov.info` con 90.91% de cobertura de líneas.
- `npm.cmd run build`: compilación de producción aprobada.
- `npm.cmd audit --omit=dev --json`: 0 vulnerabilidades reportadas en dependencias de producción frontend.
- `docker compose exec -T backend pip check`: sin requisitos Python rotos.
- Escaneo final del sprint: tarea `SUCCESS`, reportes Python y LCOV importados y Quality Gate `OK`/PASSED.

### Cobertura verificada de módulos frontend prioritarios

| Módulo | Cobertura SonarQube | Líneas | Ramas |
|---|---:|---:|---:|
| `src/components/driver/DriverApp.tsx` | 84.2% | 85.3% | 80.1% |
| `src/components/Map.tsx` | 95.7% | 98.3% | 87.7% |
| `src/components/PinMap.tsx` | 100.0% | 100.0% | 100.0% |

[← Volver al README principal](../../../README.md)
