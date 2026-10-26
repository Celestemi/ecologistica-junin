# Reporte de rendimiento — EN-001 / RNF-001

**Proyecto:** EcoLogística Huancayo  
**Artefacto:** Motor de optimización (`app/services/genetic_solver.py`, GA `ga_vrptw_ox`)  
**Requisito:** RNF-001 — generación de ruta válida para hasta **150 pedidos** y **15 vehículos** en **≤ 45 s**  
**Fecha de medición:** 2026-10-26  
**Sin alteración artificial de métricas.**

---

## 1. Criterios de aceptación (fuente documental)

| ID | Criterio |
|----|----------|
| **RNF-001** | Escenario hasta 150×15: tiempo de generación de una **solución válida** ≤ **45 s** |
| **EN-001 Esc. 1** | Llamada de optimización: tiempo total de respuesta **T ≤ 45 s** |
| **EN-001 Esc. 2** | Si se supera el umbral, devolver la **mejor solución factible** encontrada sin caída del servicio |

**Alcance de esta medición:** solver Python (GA + líneas base FIFO/secuencial). La capa HTTP + PostGIS se documenta como protocolo; no se midió en esta corrida por ausencia de PostGIS en el host de benchmark (pruebas de API requieren `docker compose`).

---

## 2. Protocolo de pruebas

### 2.1 Dataset reproducible

Módulo: `app/services/optimizer_benchmark.py`

| Escenario | Pedidos | Vehículos | Notas |
|-----------|---------|-----------|--------|
| `feasible_150x15` | 150 | 15 | Coordenadas aleatorias en caja Huancayo; ventanas amplias; 8 kg/pedido |
| `medium_50x8` | 50 | 8 | Misma semilla base |
| `small_5x2` | 5 | 2 | Regresión rápida |
| `restricted_tight_windows` | 30 | 5 | Ventanas de 2 min (estrés RN-005) |
| `overloaded_*` (precheck) | 150 | 15 | 200 kg/pedido → infactible de flota (sin solver) |

**Semilla maestra:** `901_001` (`BENCHMARK_SEED` en tests).

### 2.2 Inicio / fin de medición

| Métrica | Inicio | Fin |
|---------|--------|-----|
| **`solver_elapsed_seconds`** | Antes de `_build_problem` | Tras evaluar líneas base FIFO y secuencial |
| **`ga_elapsed_seconds`** | Igual | Fin del bucle GA (antes de baselines) |
| **HTTP total (protocolo)** | Entrada a `POST /optimizar-rutas` | Respuesta JSON completa (incl. persistencia) |

### 2.3 Repeticiones

- **5 repeticiones** por escenario (`EN001_REPEATS=5`).
- Comando: `EN001_WRITE=1 uv run pytest tests/test_solver_sla_en001.py -m slow`

### 2.4 Entorno de ejecución

| Campo | Valor |
|-------|--------|
| SO | Windows 11 (10.0.26200) |
| Python | 3.14.8 (uv, proyecto `ecologistica-huancayo`) |
| CPU | (host local del desarrollador; no contenedor CI) |
| `OPTIMIZER_TIME_BUDGET_SECONDS` | 45 (default) |
| GA 150×15 | `generations=32`, `population=24` (`resolve_ga_parameters`) |
| OSRM | Desactivado (`OSRM_BASE_URL` vacío) |

---

## 3. Análisis de rendimiento (profiling)

**Método:** `cProfile` sobre 1 corrida 150×15 (32 gen × 24 pop).

**Cuellos de botella (tiempo acumulado):**

1. **`_evaluate` → `_schedule_vehicle` → `_visit`** (~85 % del GA): simulación VRPTW por individuo.
2. **`_Problem.__init__`**: matrices Haversine + cruce Centro Histórico (~19 % en una corrida fría).
3. **`leg_enters_historic_center` / `_segments_intersect`**: costo geométrico por tramo.

**No dominan en esta corrida:** precheck (`route_constraints`), serialización JSON, persistencia SQL (fuera del solver).

**Mejoras aplicadas (Fase 3):**

- Caché de evaluaciones por firma de rutas (existente; se evita `_repair` duplicado).
- `orders_by_id` precalculado en `_Problem`.
- Población inicial reducida para lotes > 60 pedidos (solo semillas FIFO + secuencial).
- Parámetros GA escalados por tamaño (`optimizer_runtime.py`).
- **Presupuesto de 45 s** con parada por reloj y retorno de mejor **factible** si aplica (EN-001 Esc. 2).
- Parada anticipada por estancamiento de solución factible (`optimizer_stagnation_generations=6`).

**Pendiente (no implementado para no sacrificar reglas de negocio):**

- Vectorizar Haversine / cachear `enters_historic` de forma más agresiva.
- Reducir penalización histórica en evaluación masiva (cambiaría rutas semilla).
- OR-Tools / DEAP (no requerido por criterio; ver IMP-004 histórico).

---

## 4. Resultados de benchmark (solver)

Fuente: `en001_benchmark_last.json` generado en la misma fecha.

### 4.1 Escenario RNF-001 — 150 pedidos × 15 vehículos

| Métrica | Valor |
|---------|--------|
| Repeticiones | 5 |
| **Solver media (s)** | **0,888** |
| Solver mediana (s) | 0,871 |
| Solver máx (s) | 0,950 |
| **Cumple SLA ≤ 45 s (tiempo)** | **Sí** |
| Generaciones ejecutadas | 32 (tope) |
| `stop_reason` | `generations_complete` |
| Pedidos asignados | 150 |
| No asignados | 0 |
| Distancia (última corrida) | 685,6 km |
| CO₂ estimado | 150,07 kg |
| **`feasible` (flags duros GA)** | **No** (0/5 repeticiones) |

**Interpretación:** El **tiempo** RNF-001 se cumple con amplio margen (~1 s vs 45 s). La bandera **`feasible`** del GA indica que, con ventanas sintéticas aleatorias y 32 generaciones, no siempre se alcanza factibilidad dura (ventanas/jornada) **antes** de la validación US-008 en API. En producción, `validate_for_publication` + HTTP **409** impiden persistir rutas ilegales.

### 4.2 Otros escenarios

| Escenario | Solver max (s) | SLA 45 s | Asignados | `feasible` (última) |
|-----------|----------------|----------|-----------|---------------------|
| 50×8 | 1,04 | Sí | 50 | No (80 % factible en repeticiones) |
| 5×2 | 0,025 | Sí | 5 | Sí |
| 30×5 ventanas tight | 0,62 | Sí | 30 | No |

### 4.3 Profiling puntual (1× 150×15)

| Métrica | Valor |
|---------|--------|
| `solver_elapsed_seconds` | 1,787 |
| `ga_elapsed_seconds` | 1,786 |
| Llamadas a funciones | ~3,96 M |

---

## 5. EN-001 Escenario 2 — control de tiempo

Implementado en `solve_vrptw(..., time_budget_seconds=45)`:

- Si `perf_counter()` supera el presupuesto → `stop_reason=time_budget`.
- Se devuelve el mejor individuo **factible** acumulado si existe; si no, el mejor por fitness.
- No se lanza excepción no controlada (FastAPI no cae por timeout de solver).

En las corridas medidas **no se activó** el tope de 45 s (el GA terminó mucho antes).

---

## 6. Distinción solver vs HTTP

| Capa | Incluye | Medido aquí |
|------|---------|-------------|
| Solver | Matrices, GA, baselines RN-008 | **Sí** |
| API | Precheck, `validate_for_publication`, persistencia, GeoJSON | **No** (requiere PostGIS) |

Metadatos expuestos tras optimizar: `solver_elapsed_seconds`, `ga_elapsed_seconds`, `optimizer_stop_reason`.

---

## 7. Regresión (Fase 5)

| Suite | Resultado (host sin Docker DB) |
|-------|--------------------------------|
| `tests/test_solver.py` | OK (tras `volumen_m3` en fixtures) |
| `tests/test_solver_sla_en001.py` (no slow) | OK |
| `tests/test_solver_sla_en001.py` (-m slow) | OK — SLA tiempo 150×15 |
| Tests API (US-005/007/008/009) | Requieren PostGIS (`ConnectionRefused` sin `db`) |

---

## 8. Conclusión EN-001 / RNF-001

| Pregunta | Respuesta |
|----------|-----------|
| ¿150×15 en ≤ 45 s (solver)? | **Sí** — ~0,9–1,8 s en el entorno medido |
| ¿Solución válida (restricciones duras) en el benchmark 150×15? | **Parcial** — asignación completa pero `feasible=false`; requiere más calidad de instancia o iteraciones, no más reloj |
| ¿Timeout seguro (Esc. 2)? | **Implementado** |
| ¿Métricas fabricadas? | **No** — ver JSON y comando de reproducción |

**Brechas pendientes:**

1. Medición **HTTP end-to-end** en CI con PostGIS (Docker).
2. Ajuste fino GA / instancias de prueba para **factibilidad** sistemática a 150×15 manteniendo SLA (sin relajar US-008).
3. Optimización micro: intersección Centro Histórico en evaluación masiva.

---

## 9. Reproducción

```powershell
cd ecologistica-junin
$env:EN001_WRITE = "1"
$env:EN001_REPEATS = "5"
uv run pytest tests/test_solver_sla_en001.py -m slow -q
```

Archivo de salida: `en001_benchmark_last.json` (raíz del repo, gitignored recomendado).

```powershell
uv run pytest tests/test_solver_sla_en001.py tests/test_solver.py -q -k "not slow"
```
