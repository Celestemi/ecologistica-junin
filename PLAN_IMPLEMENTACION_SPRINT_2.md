# Plan de implementación — Sprint 2 (Geocodificación y motor de rutas)

**Proyecto:** EcoLogística Huancayo — DistriRápido S.A.C.  
**Ámbito:** Huancayo, El Tambo y Chilca  
**Fecha de elaboración:** 26 de octubre de 2026  
**Alcance de este documento:** US-005, US-007, US-008, US-009 y EN-001 (34 SP).  
**Fase:** 00 — planificación. No modifica código, documentos originales, esquema ni historial Git.

---

## 1. Objetivo y regla de no regresión

El Sprint 2 cierra la geocodificación espacial de pedidos y endurece el motor de rutas ya existente para que la solución publicada respete capacidad, ventanas, jornada y un presupuesto de tiempo de 45 segundos.

La regla de esta fase es conservar el comportamiento verificable del Sprint 1:

- importación CSV/XLSX con tope de 150 filas e informe por fila;
- alta manual con pin en el mapa;
- ventanas de tiempo y su edición antes de rutear;
- flota con estado operativo y exclusión de mantenimiento e inactivos;
- restricción de placa desactivada hasta validación normativa;
- `POST /api/v1/optimizar-rutas` autenticado solo para el operador;
- reoptimización en vivo de `app/services/realtime_router.py`, que llama al mismo `solve_vrptw`.

Las historias de cartografía interactiva (US-010 a US-012), PWA offline (EN-004), KPI de sostenibilidad (RF-013 / RF-014) y reoptimización por incidentes (US-018 / EN-002 / RNF-002) quedan fuera de este sprint. Se tocan solo donde el motor actual ya las alimenta.

---

## 2. Fuentes y método

Criterios tomados de los documentos originales, sin reinterpretar el texto:

| Fuente | Qué aporta a este sprint |
|--------|--------------------------|
| `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` | Redacción y 2 escenarios BDD de US-005, US-007, US-008, US-009 y EN-001 |
| `docs/01 Inicio/06. Requisitos funcionales V_1_0_0.md` | RF-005, RF-007, RF-008 y RF-009, cada uno con ruta Gold, Feliz e Infeliz |
| `docs/01 Inicio/07. Requisitos no funcionales V_1_0_0.md` | RNF-001: solución válida en ≤ 45 s para 150 pedidos y 15 vehículos |
| `docs/01 Inicio/09. Reglas de negocio V_1_0_4.md` | RN-003, RN-004, RN-005 y RN-008. RN-002 y RN-006 se preservan, no se reabren |
| `docs/01 Inicio/10. Stack tecnológico V_1_0_3.md` | DEAP / OR-Tools, PostGIS 3, Leaflet + OSRM local |
| `docs/01 Inicio/11. Base de datos V_1_0_3.md` | `GEOGRAPHY(Point, 4326)`, `distrito.limite_geom`, `volumen_m3`, `detalle_ruta` |
| `docs/01 Inicio/12. Modelo C4 V_1_0_6.md` | Order Service con GeoPy, motor Google OR-Tools, OSRM local |

La matriz registra **el escenario ágil y el escenario RF**. Donde el backlog exige un umbral (ahorro, OSRM, `GEOGRAPHY`) y el RF atómico es más amplio, ambos quedan como criterios. Las decisiones de la sección 16 dicen cuál se implementa ya y cuál queda explícitamente pendiente de validación.

---

## 3. Estado del código revisado (sin ejecutar migraciones)

| Elemento | Estado observado en el repositorio |
|----------|-----------------------------------|
| Motor | `app/services/genetic_solver.py`: algoritmo genético propio (`ga_vrptw_ox`), población 50, 100 generaciones, cruce OX, torneo, semilla fija. No hay OR-Tools ni DEAP en `pyproject.toml` ni en `backend/requirements.txt`. |
| Distancias | Haversine en Python, 25 km/h. Gancho `distance_adjuster` ya usado por la reoptimización en vivo. No hay cliente OSRM ni servicio OSRM en `docker-compose.yml`. |
| Emisiones del solver | `leg_co2_grams` local: `km × g/km × (1 + penalización × max(0, Δh/100))`. No usa los factores por galón de RN-006. `app/core/emissions.py` tiene otra firma (altitud y combustible) y el solver no la llama. |
| Factibilidad | Blanda. El atraso y el exceso de kg suman penalización. `feasible` es verdadero solo si `late_minutes == 0` y `capacity_excess_kg == 0`. Aun así, `optimize_routes` persiste la corrida y marca los pedidos `assigned`. |
| Capacidad | Solo peso. `capacidad_m3` clasifica vehículos grandes para el Centro Histórico. El pedido no tiene `volumen_m3`. |
| Jornada | `duration_minutes` incluye espera por ventana. No hay corte a 8 horas ni rechazo de una ruta de 8.5 h. |
| Ahorro | CO₂ contra un FIFO por apertura de ventana (`co2_referencia_kg`). No hay porcentaje de distancia ni umbral 15 % / 10 %. |
| Tiempo | No hay presupuesto de 45 s ni devolución de la mejor solución al vencer el límite. |
| Geocodificación | `app/services/geocode.py`: diccionario de hitos (UNCP, Plaza Constitución, Chilca, Calixto, y también San Jerónimo / Tunan, fuera del triángulo distrital). Sin GeoPy ni Nominatim. |
| Pedido sin punto | La importación responde `pendiente_punto` y **no inserta** la fila. El pin de `OrdersDay.tsx` hace `POST /pedidos` después. |
| Cobertura distrital | Caja amplia del valle (`lat` −12.30…−11.70, `lon` −75.50…−74.90) en esquemas e importación. No hay tabla `distrito` ni polígonos. |
| Geometría | `Geometry(POINT, 4326)` y `LINESTRING` vía GeoAlchemy2 (`app/models/domain.py`). No es `GEOGRAPHY`. SRID 4326 en `app/core/config.py`. |
| Optimización API | `POST /api/v1/optimizar-rutas` toma **todos** los pedidos `pending`, no una jornada. Filtra flota `estado_operativo = activo` y luego `filter_vehicles_for_planning`. |
| Secuencia y ETA | `rutas_detalle.secuencia` (depósito en 0, entregas siguientes), `eta`, `tiempo_viaje_min`, `geometria_tramo` como cuerda recta. El seguimiento ya lee el ETA. |
| Migraciones | `app/db/migrations.py` versiones `001`…`006` más `schema_migrations`. `init_db` hace `create_all` y luego esos `ALTER`. No hay Alembic. Este plan no las ejecuta. |
| Pruebas | `tests/conftest.py` reescribe `DATABASE_URL` a `ecologistica_test` y aborta si el nombre final no es ese. CI (`.github/workflows/ci.yml`) levanta PostGIS con la base `ecologistica`; el conftest crea `ecologistica_test` en ese servidor. |
| Pruebas del solver | `tests/test_solver.py`: pendiente, velocidad 25 km/h, atraso con ventanas de un minuto, espera si llega temprano. No cubren capacidad de flota, volumen, 8 h, ahorro ni SLA. |

La semilla de desarrollo (`app/db/init_db.py`) tiene un depósito en El Tambo, dos vehículos activos de muestra y cinco pedidos con coordenadas. `tests/test_api.py` espera que optimizar esa semilla responda 201, use 2 vehículos, deje la bandeja de pendientes vacía y permita un segundo `POST` en 404.

---

## 4. Matriz de requisitos

Leyenda: **Hecho** = el criterio ya se cumple en código y hay una prueba o un flujo que lo demuestra. **Parcial** = hay una pieza usable y una brecha concreta. **Pendiente** = no está.

### US-005 — Geocodificación y ubicación espacial (RF-005) — 5 SP

| ID | Criterio | Fuente | Estado | Evidencia o brecha |
|----|----------|--------|--------|-------------------|
| US5-G | Dirección válida en Huancayo → punto `GEOGRAPHY(Point, 4326)` visible en el mapa | US Esc. 1 | Parcial | Se guarda un `POINT` 4326 si el CSV trae coordenadas, si el texto contiene un hito o si el operador clava el pin. El tipo SQL es `geometry`, no `geography`. El mapa de rutas muestra pedidos ya persistidos. |
| US5-F | El operador corrige el punto y el sistema guarda las coordenadas nuevas | RF Feliz | Parcial | `PinMap` + `POST /pedidos` cubre la fila que **aún no existe**. No hay `PATCH` de coordenadas de un pedido ya guardado. |
| US5-I | Fuera de Huancayo, El Tambo o Chilca, o no ubicable → **Pendiente de validación** y bloqueo en la ruta | US Esc. 2 / RF Infeliz | Parcial | `pendiente_punto` no persiste el pedido, así que no puede entrar al optimizador, pero tampoco queda un registro marcado. La caja del Mantaro acepta puntos fuera de los tres distritos. San Jerónimo está en el diccionario. |
| US5-MAP | El punto de entrega se muestra en el mapa | RF Gold | Parcial | `src/components/Map.tsx` pinta paradas de la solución y pedidos sueltos si el GeoJSON los trae. No hay capa de “pendientes de validación”. |
| US5-POSTGIS | Asociación lat/lon dentro del área de aplicación | RF descripción | Parcial | `point_wkt` + índice espacial de GeoAlchemy2. Sin `ST_Contains` contra límites distritales. |

### US-007 — Rutas sostenibles VRPTW + Green VRP (RF-007, RN-008, RNF-001) — 13 SP

| ID | Criterio | Fuente | Estado | Evidencia o brecha |
|----|----------|--------|--------|-------------------|
| US7-G | Hasta 150 pedidos y 15 vehículos con capacidad suficiente → rutas que respetan ventanas y capacidad, con ahorro ≥ 15 % de distancia y ≥ 10 % de CO₂ | US Esc. 1 | Parcial | El GA produce una asignación y compara CO₂ con un FIFO. No calcula ahorro de kilómetros ni exige los umbrales. No hay escenario de 150×15. |
| US7-F | Menos pedidos y vehículos que el máximo → rutas válidas con los recursos disponibles | RF Feliz | Hecho | Semilla de 5 pedidos y 2 vehículos: `test_optimize_routes_returns_geojson_and_then_404`. |
| US7-I | Demanda de peso o volumen por encima de toda la flota → no hay solución factible y se detalla el exceso no asignable | US Esc. 2 / RF Infeliz | Pendiente | El reparador mete los pedidos sobrantes en el vehículo de mayor kg. La API responde 201, persiste y asigna. El panel solo avisa si `feasible` es falso. No hay desglose de kg ni de m³. |
| US7-RF-G | Lote válido y flota suficiente → asignación y secuencia que respetan las restricciones | RF Gold | Parcial | Ventanas y peso son penalizaciones, no restricciones duras de publicación. |
| US7-RN8 | Ahorro mínimo frente a la línea base secuencial | RN-008 | Pendiente | La referencia es un FIFO por ventana, no una línea base secuencial, y solo en CO₂. |
| US7-FLOTA | Usar solo vehículos activos y, si la regla está validada, fuera de restricción de placa | Integración US-002 / US-003 | Hecho | `_require_vehicles` y `filter_vehicles_for_planning`. Hay que no romperlo. |
| US7-DIA | El lote es el de la jornada pedida, no todos los `pending` históricos | Operación diaria (RF-007, US-004) | Pendiente | `_require_pending_orders` no filtra por `jornada_id` ni por fecha. |

### US-008 — Restricciones duras de capacidad y jornada (RF-008, RN-003, RN-004) — 5 SP

| ID | Criterio | Fuente | Estado | Evidencia o brecha |
|----|----------|--------|--------|-------------------|
| US8-G | Ningún vehículo supera el 100 % de peso/volumen y la conducción total es ≤ 8 h | US Esc. 1 | Parcial | El peso excedido baja el fitness y marca `feasible=false`, pero la ruta se publica. Volumen y 8 h no se validan. |
| US8-F | Si un pedido cabe en más de un vehículo, la asignación elegida no viola las duras | RF Feliz | Parcial | El GA puede preferir otro vehículo; no hay un validador que descarte la asignación ilegal antes de publicarla. |
| US8-I | Una propuesta de 8.5 h, o que supere capacidad o jornada, se rechaza y la carga se divide | US Esc. 2 / RF Infeliz | Pendiente | No existe validador de jornada ni reparto del tramo sobrante. |
| US8-RN3 | Conducción y servicio ≤ 8 h diarias, continuas o discontinuas, por conductor | RN-003 | Pendiente | Norma marcada `[PENDIENTE DE VALIDACIÓN NORMATIVA]`. El producto del sprint sí exige el límite. Ver D-04. |
| US8-RN4 | Suma de kg y de m³ ≤ 100 % de la capacidad nominal | RN-004 | Parcial | Kg sí, como penalización. m³ del pedido no existe. |
| US8-RN5 | El ETA cae dentro de `[ventana_inicio, ventana_fin]` | RN-005, compartida con US-009 | Parcial | Llegar tarde se penaliza; llegar temprano espera. Una solución tardía igual se guarda. |

### US-009 — Secuencia de paradas y ETA (RF-009, RN-005) — 3 SP

| ID | Criterio | Fuente | Estado | Evidencia o brecha |
|----|----------|--------|--------|-------------------|
| US9-G | Ruta de 10 paradas → orden de visita 1…10 y ETA dentro de la ventana | US Esc. 1 | Parcial | La secuencia de entregas empieza en 1 porque el depósito ocupa la 0. El ETA se calcula con haversine. No hay prueba de 10 paradas ni de ETA dentro de ventana en API. |
| US9-F | Una modificación válida de la secuencia antes del despacho recalcula los ETA | RF Feliz | Pendiente | No hay endpoint para reordenar paradas. Solo una corrida nueva del GA, que además exige pedidos `pending` y la corrida anterior ya los pasó a `assigned`. |
| US9-I | Si falta la matriz de tiempo/distancia, se advierte, la parada queda en revisión y no se publica un ETA erróneo | US Esc. 2 / RF Infeliz | Pendiente | Siempre hay matriz haversine. `geometria_tramo` es la cuerda. No hay estado “en revisión” ni ETA nulo por matriz ausente. El texto ágil nombra OSRM local. Ver D-03. |
| US9-RF-G | Al cerrar la optimización se muestra secuencia y un ETA por parada | RF Gold | Hecho | `RutaDetalle.secuencia` y `eta`; mapa, sidebar y seguimiento los leen. |

### EN-001 — SLA de generación ≤ 45 s (RNF-001, RF-007) — 8 SP

| ID | Criterio | Fuente | Estado | Evidencia o brecha |
|----|----------|--------|--------|-------------------|
| EN1-1 | Escenario de 150 pedidos y 15 vehículos en Huancayo: respuesta total ≤ 45.0 s | EN Esc. 1 / RNF-001 | Pendiente | No hay prueba de carga. El GA es Python puro, 100×50 evaluaciones, sin tope de reloj. |
| EN1-2 | Si el cálculo supera 45 s, se devuelve la mejor solución factible hallada y el servicio no cae | EN Esc. 2 | Pendiente | El ciclo corre todas las generaciones. Una excepción no prevista del solver cae al manejador 500 de `routes.py`. |
| EN1-VAL | La solución devuelta dentro del SLA sigue siendo válida (ventanas, capacidad, jornada) | RNF-001 “solución válida” | Pendiente | Depende de US-008. Un atajo que publique una ruta ilegal cumpliría el reloj y fallaría el RNF. |

---

## 5. Qué ya está desarrollado y qué falta

### Ya sirve como base y no debe reescribirse

- Persistencia de puntos WGS84, depósito, flota, pedidos, solución y detalle de paradas.
- Algoritmo genético con semillas FIFO, ecológica, vecino más cercano y aleatoria; cruce OX; reparación para que cada pedido aparezca una vez.
- Espera si el vehículo llega antes de la ventana (`test_early_arrival_waits_without_lateness`).
- Filtro de flota activa y de placa antes de llamar al solver.
- Informe de importación con fila `pendiente_punto` y corrección manual en Leaflet.
- GeoJSON de la corrida, KPIs de CO₂ y equivalente Quinual, bitácora `optimizar_rutas`.
- Aislamiento de la base de pruebas en `ecologistica_test`.

### Incompleto y es el trabajo del sprint

1. **US-005.** Persistir el pedido no ubicado, clasificarlo, limitarlo a los tres distritos, permitir corregir un punto ya guardado y dejarlo fuera de `_require_pending_orders` hasta que esté validado.
2. **US-008.** Validador duro, aparte del fitness, para kg, m³ cuando exista el dato, ventanas y 8 h de conducción más servicio. La publicación solo acepta soluciones que pasen el validador.
3. **US-007.** Prechequeo de capacidad de flota con exceso detallado; línea base secuencial; porcentajes de ahorro; alcance por jornada; no asignar pedidos si la corrida es infactible.
4. **US-009.** Orden de entrega explícito, ETA coherente con la ventana, recálculo si la secuencia cambia antes del despacho, y marca de revisión cuando falte una celda de la matriz.
5. **EN-001.** Presupuesto de 45 s dentro de `solve_vrptw`, devolución de la mejor solución factible y prueba del escenario 150×15.

---

## 6. Integración flota, pedidos, geocodificación y optimización

Flujo actual, y el corte que este sprint debe respetar:

```text
Importación / alta
    → pedido con POINT o fila pendiente_punto sin fila en BD
        → POST /optimizar-rutas
            → depósito único
            → vehículos estado_operativo = activo
            → exclusión de placa si la regla está validada y activa
            → todos los pedidos pending
            → solve_vrptw (haversine + GA)
            → soluciones_ruta + rutas_detalle
            → pedidos pasan a assigned
```

Contrato que el Sprint 2 debe dejar:

```text
Pedido geocodificado y dentro del distrito
    → elegible en la jornada indicada
Pedido pendiente de validación o fuera de distrito
    → persistido, visible, excluido del motor
Flota en mantenimiento, inactiva o con placa restringida
    → excluida, igual que hoy
Corrida infactible (peso, volumen o jornada)
    → HTTP 409, nada asignado, detalle del exceso
Corrida factible
    → secuencia, ETA, distancia, CO₂ y porcentajes contra la línea base
Reloj ≥ 45 s
    → mejor factible encontrada, sin 500
```

`realtime_router.reoptimize_live_route` debe seguir llamando a `solve_vrptw` con los mismos argumentos de hoy (`generations`, `population_size`, `seed`, `distance_adjuster`). Los parámetros nuevos (`time_budget_seconds`, matriz externa) tienen que tener default compatible. La reoptimización por incidentes no se rediseña en este sprint: solo no puede romperse.

---

## 7. Motor actual frente a la arquitectura documentada

| Pieza documentada | Qué hay en el repositorio | Lectura para el sprint |
|-------------------|---------------------------|------------------------|
| Google OR-Tools (C4, stack, US-007, EN-001) | No está instalado. El VRPTW lo resuelve el GA propio. | No incorporarlo. El criterio de negocio es la solución válida y el SLA, no el nombre de la librería. |
| DEAP (stack) | No está. El GA ya implementa población, OX, mutación de intercambio, transferencia entre vehículos y torneo. | No incorporarlo. DEAP duplicaría el bucle que ya está probado. |
| GeoPy (C4, Order Service) | No está. Diccionario local + coordenadas del archivo + pin. | No incorporarlo como dependencia obligatoria. Ver D-02. |
| OSRM local (stack, C4, US-009 Esc. 2) | No hay contenedor, extracto OSM ni cliente HTTP. Hay haversine y un gancho `distance_adjuster`. | Dejar el puerto de matriz. OSRM queda apagado por defecto. Ver D-03. |
| PostGIS `GEOGRAPHY(Point, 4326)` | `geometry(Point, 4326)` con índice espacial. | Conservar `geometry` en este sprint. Ver D-01. |
| `distrito.limite_geom` | No existe la tabla. | Polígono de trabajo en un GeoJSON versionado y consulta en Shapely, que ya es dependencia. La tabla PostGIS puede esperar a que el polígono esté validado. |
| Factores RN-006 (kg CO₂/gal y GNV) | El solver usa g/km y pendiente. El modelo de flota tiene `rendimiento_km_gal` (US-001) y no GNV: el enum es diésel, gasolina, GLP y eléctrico. | No cambiar la fórmula de emisión en este sprint. RN-006 está trazado a RF-013, historia posterior. El 10 % de CO₂ se mide con la misma fórmula del GA para que la comparación sea honesta. |
| Centro Histórico | Penalización fuerte a vehículos ≥ 1 000 kg o ≥ 6 m³. | Se conserva. No es criterio de US-007…US-009, pero quitarlo cambiaría las rutas de la semilla y de `test_api.py`. |

### Cómo mejorar el motor sin dependencias nuevas

Trabajar dentro de `genetic_solver.py` y extraer un validador puro, testeable sin base de datos:

1. **Presupuesto de tiempo.** Al inicio de `solve_vrptw`, guardar `perf_counter`. Entre generaciones, si se agotaron 45 s, cortar y devolver el mejor individuo **factible**. Si ninguno lo es, devolver la evaluación con `feasible=false` y un motivo, sin lanzar una excepción genérica.
2. **Restricciones duras fuera del fitness.** El fitness puede seguir guiando la búsqueda. La publicación usa otra función: exceso de kg, exceso de m³ si el pedido trae volumen, minutos tarde, y minutos de viaje más servicio por vehículo. La espera por ventana no cuenta como jornada (D-04).
3. **No reparar a costa de la capacidad.** `_repair` hoy vuelca los pedidos faltantes al vehículo más grande y eso fabrica excesos. El reparador debe dejar un conjunto `no_asignados` en lugar de forzar la carga.
4. **Línea base secuencial.** Además del FIFO actual, construir la referencia que nombra RN-008: orden de entrada (id del pedido dentro de la jornada), empaquetado por vehículos en orden de id, sin reordenar paradas. Publicar `ahorro_distancia_pct` y `ahorro_co2_pct`. El FIFO de ventanas se mantiene como metadato, porque `co2_referencia_kg` ya lo consume el frontend.
5. **Matriz intercambiable.** La matriz haversine sigue siendo la implementación por defecto. Una celda ausente (adaptador que devuelve `None`) marca la parada `revision_eta` y deja `eta` en nulo. Así se prueba US-009 Esc. 2 sin levantar OSRM.
6. **Parámetros del GA.** Subir población o generaciones solo si el escenario 150×15 no alcanza factibilidad dentro de 45 s. El primer ajuste es el corte por reloj y una parada anticipada cuando ya hay una solución factible estable, no una librería nueva.

OR-Tools o DEAP solo volverían a la mesa si, después de EN-001, el GA no logra una solución factible en el escenario de referencia. Esa puerta queda cerrada durante la implementación ordinaria del sprint.

---

## 8. Archivos involucrados

### A crear en la implementación (no en esta fase)

| Archivo | Historia |
|---------|----------|
| `tests/test_geocode_us005.py` | US-005 |
| `tests/test_optimizer_us007.py` | US-007 |
| `tests/test_hard_constraints_us008.py` | US-008 |
| `tests/test_eta_us009.py` | US-009 |
| `tests/test_solver_sla_en001.py` | EN-001 |
| `app/services/route_constraints.py` | US-008, usado por US-007 |
| `app/data/distritos_huancayo.geojson` | US-005, solo con una fuente citada (D-05) |

### A modificar, con cuidado de no cambiar contratos del Sprint 1

| Archivo | Qué cambia | Qué no puede cambiar |
|---------|------------|----------------------|
| `app/services/geocode.py` | Resultado con estado (ubicado / no ubicable / fuera de distrito) | Los hitos que hoy resuelven la semilla y los CSV de prueba |
| `app/services/order_import.py` | Insertar fila pendiente de validación; no insertar filas rechazadas por campos | Tope 150, atomicidad de archivo mal formado, informe por fila, `pendiente_punto` como nombre de resultado |
| `app/services/genetic_solver.py` | Presupuesto, no asignados, jornada, porcentajes, matriz con huecos | Firma actual con defaults; pruebas de pendiente, espera y velocidad |
| `app/services/realtime_router.py` | Ningún cambio de comportamiento previsto | Llamada actual a `solve_vrptw` |
| `app/api/v1/routes.py` | Filtro de pedidos geocodificados, fecha de jornada, 409 si es infactible, no asignar si `feasible` es falso | 201 de la semilla actual; RBAC de operador; GeoJSON |
| `app/api/v1/desk.py` | Corrección de punto si el flujo de jornada debe vivir ahí | RBAC de importación |
| `app/models/domain.py`, `app/models/enums.py` | Estado de ubicación; volumen opcional | Estados de pedido y de solución ya persistidos |
| `app/schemas/logistics.py` | Campos nuevos opcionales en la respuesta | Caja de coordenadas que ya rechaza puntos absurdos, hasta que el polígono la reemplace solo para el alta de pedidos |
| `app/db/migrations.py` | Versión `007` append-only | No editar `001`…`006` |
| `src/pages/OrdersDay.tsx`, `src/components/PinMap.tsx` | Guardar pin sobre un pedido ya creado; mostrar pendiente de validación | Edición de ventanas (US-006) |
| `src/components/Sidebar.tsx`, `src/types.ts`, `src/components/Dashboard.tsx` | Exceso no asignable, ahorro, parada en revisión | Aviso actual de solución no factible hasta que el 409 lo reemplace |
| `tests/test_api.py`, `tests/test_day.py`, `tests/test_solver.py`, `tests/test_import_us004.py` | Ajustar solo aserciones que el nuevo contrato cambie a propósito | El resto de la suite Sprint 1 |

Archivos que el sprint lee y no debería necesitar editar: `app/services/plate_restriction.py`, `app/services/vehicle_state.py`, `app/services/order_window.py`, `app/core/emissions.py`, `tests/conftest.py`.

---

## 9. Dependencias entre historias

```text
US-006 ventanas (Sprint 1, hecho)
US-002 placa y US-003 estado (Sprint 1, hecho)
US-004 importación (Sprint 1, hecho)
        │
        ▼
     US-005 geocodificación
        │  solo pedidos ubicados y dentro del distrito
        ▼
     US-008 validador duro ─────────────┐
        │                                │
        ▼                                ▼
     US-007 publicación de rutas     US-009 secuencia y ETA
        │                                │
        └────────────┬───────────────────┘
                     ▼
                  EN-001 SLA sobre el motor ya endurecido
```

- US-005 puede empezar sin tocar el GA. El optimizador solo debe ignorar el nuevo estado.
- US-008 se prueba como función pura antes de cablearla a la API, para no mezclar el 409 con la geocodificación.
- US-007 depende de US-005 (elegibilidad) y de US-008 (qué se considera solución válida).
- US-009 depende de la solución que US-007 persiste. El recálculo de una secuencia editada puede hacerse con la matriz ya construida, sin otra corrida del GA.
- EN-001 va al final. Medir 45 s antes de cerrar capacidad, jornada y no asignados produciría un número que deja de valer en cuanto cambie el bucle.

US-010 (mapa por colores) ya tiene un dibujo básico en `Map.tsx`. Este sprint no lo amplía; solo debe seguir recibiendo puntos, líneas y `plate`.

---

## 10. Riesgos técnicos

| ID | Riesgo | Efecto | Mitigación en la implementación |
|----|--------|--------|---------------------------------|
| R-01 | Exigir `GEOGRAPHY` rompe lecturas WKB, índices y `geometria_tramo` | Regresión de mapa, seguimiento y pruebas | D-01: no migrar el tipo en este sprint |
| R-02 | Persistir `pendiente_punto` duplica códigos cuando el pin hace `POST` | El operador no puede guardar el punto | El pin pasa a `PATCH` de coordenadas del pedido ya creado |
| R-03 | Un 409 en corridas infactibles cambia el 201 de pruebas que optimizan la semilla | Falsa regresión de Sprint 1 | La semilla de 5 pedidos debe seguir siendo factible. Los tests de exceso usan un lote aparte |
| R-04 | Contar la espera dentro de las 8 h | Rutas con ventanas separadas se rechazan aunque el manejo sea corto | D-04: jornada = viaje + servicio |
| R-05 | Umbral 15 % / 10 % como veto de publicación | Un día ya compacto no se puede despachar | D-06: el umbral se informa; el veto es solo por restricción dura |
| R-06 | `solve_vrptw` más lento y la reoptimización en vivo hereda el presupuesto de 45 s | El recálculo de un vehículo deja de sentirse inmediato | Presupuesto explícito por llamada. La reoptimización en vivo mantiene un presupuesto corto propio, sin cambiar su contrato |
| R-07 | Polígono distrital incorrecto | Direcciones buenas quedan pendientes, o el valle entero pasa el filtro | D-05: no inventar el límite. Hasta validar el GeoJSON, el filtro nuevo se prueba con un polígono de fixture, no con un contorno aproximado presentado como oficial |
| R-08 | Mezclar pedidos de varias jornadas | Una corrida asigna el día equivocado | `optimizar-rutas` exige la fecha de jornada cuando hay más de un día `pending` |
| R-09 | Volumen obligatorio al estilo del modelo documental | Rompe CSV del Sprint 1, que no trae m³ | Columna nullable. Sin valor, la restricción de volumen no se aplica y el metadato lo dice |
| R-10 | CI crea `ecologistica_test` en el Postgres de servicio | Si alguien apunta pytest a la base de desarrollo, el guardado del conftest debe seguir abortando | No relajar `_assert_test_database_isolated`. No correr migraciones a mano contra `ecologistica` |
| R-11 | Dos fórmulas de CO₂ (`genetic_solver.leg_co2_grams` y `app/core/emissions.py`) | Un “arreglo” de RN-006 cambia el CO₂ de rutas ya comparadas en tests | No unificarlas en este sprint |

---

## 11. Plan de migraciones

No se ejecutan en esta fase. Cuando se implemente, la única versión nueva es append-only en `app/db/migrations.py`, aplicada por el mismo `apply_migrations` que ya corre dentro de `init_database` (desarrollo y `ecologistica_test`).

### `007_geocodificacion_pedido`

Objetivo: poder guardar un pedido sin punto y distinguirlo del pedido ubicado, sin tocar `001`…`006`.

```text
ALTER TABLE pedidos
  ADD COLUMN estado_ubicacion VARCHAR(32) NOT NULL DEFAULT 'geocodificado';

ALTER TABLE pedidos
  ADD COLUMN volumen_m3 DOUBLE PRECISION NULL;

ALTER TABLE pedidos ALTER COLUMN ubicacion DROP NOT NULL;
ALTER TABLE pedidos ALTER COLUMN altitud_msnm DROP NOT NULL;

CHECK (
  estado_ubicacion <> 'geocodificado'
  OR (ubicacion IS NOT NULL AND altitud_msnm IS NOT NULL)
);

CHECK (volumen_m3 IS NULL OR volumen_m3 > 0);
```

Reglas de datos:

- Los pedidos ya sembrados quedan `geocodificado` porque hoy `ubicacion` es obligatoria.
- `pendiente_validacion` admite `ubicacion` nula. El optimizador no los selecciona.
- No se convierte la columna a `geography`.
- No se crea todavía `distrito`, `cliente`, `zona_sensible` ni `kpi_sostenibilidad`. Esas tablas del documento de base de datos pertenecen a historias que este sprint no cierra, y crearlas vacías no acredita US-005.
- `rutas_detalle` no cambia de tipo. Si una parada queda en revisión, `eta` ya es nullable.

`soluciones_ruta` no necesita columnas nuevas para el ahorro: los porcentajes y el motivo de infactibilidad caben en `metadatos_ga` (JSONB), igual que hoy viven generaciones y exclusiones de placa. Así no se migra la tabla de soluciones para un campo de presentación.

Después de la migración, `create_all` en una base nueva debe crear las mismas columnas. El modelo SQLAlchemy se actualiza en el mismo cambio que `007`, para que una base creada desde cero y una base ya migrada coincidan.

Rollback previsto, solo si la versión aún no se usó en un entorno compartido: borrar la fila de `schema_migrations` no deshace el `ALTER`. El rollback real es un script inverso explícito (volver a `NOT NULL` solo donde no haya nulos, eliminar las dos columnas). No forma parte del arranque de US-005.

---

## 12. Estrategia de pruebas

### Aislamiento de base de datos (verificado, no reejecutado)

`tests/conftest.py` hace cuatro cosas que este sprint debe conservar:

1. Lee `DATABASE_URL` (o el default `localhost:5433/ecologistica`) y **reescribe el nombre** a `ecologistica_test` antes de importar la aplicación.
2. Aborta la sesión si el nombre final no es `ecologistica_test`.
3. Crea esa base conectando a la base de mantenimiento `postgres`, solo si no existe.
4. En cada test con `client`, trunca las tablas operativas de **esa** base y vuelve a sembrar con `init_database`.

El workflow de CI declara `DATABASE_URL` hacia `ecologistica` en el servicio PostGIS 15-3.4. El conftest igual mueve la aplicación a `ecologistica_test`. El usuario de la imagen oficial puede crear esa base. No hay que apuntar pytest a la base de desarrollo para “ir más rápido”.

`pytest` no se ejecutó en esta fase, para no crear ni migrar bases. La primera implementación de US-005 sí debe correr la suite existente más `tests/test_geocode_us005.py`.

Cobertura: `pyproject.toml` lleva `--cov-fail-under=0`. Este sprint no sube ese umbral. Cada historia aporta pruebas de sus criterios, no un porcentaje global nuevo.

### Pruebas que faltan para acreditar los criterios

| Historia | Prueba nueva | Qué demuestra | Base de datos |
|----------|--------------|---------------|---------------|
| US-005 | Dirección de hito dentro del polígono de fixture → pedido con coordenadas y estado geocodificado | US5-G | Sí, `ecologistica_test` |
| US-005 | Dirección no resoluble o punto fuera del polígono → fila persistida `pendiente_validacion`, ausente del lote de `optimizar-rutas` | US5-I | Sí |
| US-005 | `PATCH` de lat/lon de ese pedido → pasa a geocodificado y ya puede rutearse | US5-F | Sí |
| US-005 | El informe de importación sigue rechazando peso o ventana inválidos sin guardar esas filas | Regresión US-004 | Sí |
| US-007 | Peso total mayor que la suma de la flota activa → 409, mensaje con kg no asignables, pedidos siguen `pending` | US7-I | Sí |
| US-007 | Lote pequeño factible → 201, secuencia y vehículos de la semilla | US7-F, regresión `test_api.py` | Sí |
| US-007 | Metadatos con `ahorro_distancia_pct` y `ahorro_co2_pct` contra la línea base secuencial, en un fixture donde el orden secuencial es a propósito peor | US7-G / RN-008 | No hace falta BD para el cálculo; la API se prueba con el fixture de semilla |
| US-007 | Pedido de otra jornada no entra en la corrida de la fecha pedida | US7-DIA | Sí |
| US-007 | Vehículo en mantenimiento y placa restringida siguen fuera | Regresión US-002 y US-003 | Ya existen `test_vehicle_state_us003.py` y `test_plate_restriction_us002.py`; volver a correrlos |
| US-008 | Asignación con kg o m³ sobre el 100 % no es publicable | US8-G, RN-004 | No |
| US-008 | Itinerario de 8.5 h de viaje+servicio se rechaza y el sobrante queda no asignado o pasa a otro vehículo sin romper las duras | US8-I, RN-003 | No para el validador; sí para el `POST` |
| US-008 | Llegada temprana no suma jornada ni atraso | Regresión de `test_solver.py` | No |
| US-009 | Diez entregas de un vehículo → secuencias de entrega 1…10 y cada ETA dentro de su ventana | US9-G, RN-005 | No, llamando a `solve_vrptw` con presupuesto chico |
| US-009 | Matriz con una celda vacía → esa parada `revision_eta`, `eta` nulo, el resto puede publicarse | US9-I | No |
| US-009 | Reordenar dos paradas antes del despacho recalcula ETA y distancia de tramo | US9-F | Sí |
| EN-001 | Reloj simulado que vence a mitad de generaciones → respuesta con la mejor factible y sin excepción | EN1-2 | No |
| EN-001 | 150 pedidos y 15 vehículos dentro de la caja de Huancayo, presupuesto 45 s, solución factible | EN1-1 | No. Marcada para no correr en cada `pytest` local si el equipo quiere un perfil `sla`. En CI puede correr una vez por workflow porque 45 s cabe en el job |

El escenario EN-001 no debe pegarle a la red ni a OSRM. Coordenadas sintéticas dentro del valle y flota con capacidad de sobra. Si en la primera medición pasa de 45 s, se baja el trabajo por evaluación (corte anticipado, menos individuos repetidos), no se amplía el SLA.

Frontend: `OrdersDay.tsx` cambia el guardado del pin. Esa pantalla se verifica en el navegador al implementar US-005 (guardar un pendiente, verlo en la jornada, corregir el punto, comprobar que optimizar no lo llevó antes de la corrección). El resto del sprint es API y solver; el mapa existente se revisa solo para confirmar que una corrida factible de la semilla sigue dibujando puntos y líneas.

---

## 13. Orden de implementación

Cada paso termina con su prueba nueva en verde y con la suite ya existente sin regresiones en `ecologistica_test`. No se abre el paso siguiente si el anterior deja `POST /optimizar-rutas` de la semilla fuera de 201.

| Paso | Historia | Entrega | Toca el GA |
|------|----------|---------|------------|
| 1 | US-005 | Estado de ubicación, migración `007`, polígono de fixture, exclusión en el lote a optimizar, `PATCH` del pin, pruebas de geocodificación | No |
| 2 | US-008 | `route_constraints.py` y pruebas puras de kg, m³, ventana y 8 h. Todavía no cambia la respuesta HTTP | Solo si hace falta exponer minutos de viaje y de servicio por separado |
| 3 | US-007 | Prechequeo de flota, `no_asignados`, 409, porcentajes de ahorro, filtro por jornada, dejar de asignar corridas infactibles | Sí, el reparador y el objeto `RouteSolution` |
| 4 | US-009 | Secuencia 1…n de entregas, ETA nulo si falta matriz, recálculo al reordenar | Usa la matriz; no cambia el bucle genético |
| 5 | EN-001 | Presupuesto de 45 s, mejor factible, prueba 150×15, presupuesto corto en la reoptimización en vivo | Sí, el corte del bucle |

US-005 es el primer paso porque no depende del rediseño del fitness y porque el motor no debe volver a ver pedidos sin coordenadas confiables.

---

## 14. Decisiones técnicas que requieren validación

Hasta que el equipo las confirme, la implementación debe seguir la recomendación. Ninguna de ellas pide una librería nueva.

| ID | Decisión | Recomendación para arrancar | Si se elige lo contrario |
|----|----------|-----------------------------|--------------------------|
| D-01 | ¿Migrar `ubicacion` de `geometry(Point,4326)` a `geography(Point,4326)` para citar el texto de US-005 al pie de la letra? | No en este sprint. El punto ya es WGS84, orden longitud/latitud, con índice espacial. El criterio se acredita guardando lat/lon y comprobando el distrito. Anotar la desviación frente al documento de base de datos. | Hay que reescribir `point_wkt`, los `LINESTRING` y una prueba de ida y vuelta WKB antes de cualquier otra historia. |
| D-02 | ¿Agregar GeoPy y un Nominatim público o local? | No. Cadena: coordenadas del archivo, diccionario de hitos, pin del operador. Lo no resuelto queda `pendiente_validacion`. | Hace falta servicio, política de red y un timeout. No bloquea el esquema de US-005, pero sí el escenario Gold de una calle arbitraria. |
| D-03 | ¿Levantar OSRM local en este sprint? | No. Puerto de matriz con haversine por defecto y celdas vacías para el escenario infeliz. OSRM, cuando exista, se enchufa en `distance_adjuster` sin cambiar el GA. | Implica extracto OSM de Junín, contenedor y tiempo de preprocesado. Es trabajo de plataforma, no de US-009 mínimo. |
| D-04 | ¿Qué entra en las 8 horas? | Viaje más servicio (5 min por parada). La espera por ventana no cuenta. RN-003 sigue marcada como pendiente de validación legal; el sistema igual aplica 8 h porque US-008 lo exige. | Si la validación legal incluye la espera o la jornada partida de otra forma, el validador cambia un solo sumando. |
| D-05 | ¿De dónde sale el polígono de Huancayo, El Tambo y Chilca? | No dibujarlo a ojo. Pedir un GeoJSON con fuente (límite distrital oficial o extracto OSM citado) antes de activar el filtro en producción. Las pruebas usan un polígono pequeño de fixture alrededor de los puntos de la semilla y un punto claramente exterior. | Activar un contorno inventado produciría falsos “fuera de cobertura” (R-07). |
| D-06 | ¿El ahorro ≥ 15 % km y ≥ 10 % CO₂ veta la publicación? | No. Se calcula, se guarda en `metadatos_ga` y se muestra. Se prueba con un fixture que sí supera el umbral. La publicación se veta por capacidad, ventana o jornada. | Un veto en días compactos deja al operador sin ruta aunque la solución sea legal. |
| D-07 | ¿El volumen es obligatorio, como en el `CREATE TABLE pedido` documental? | No. `volumen_m3` nullable. Si viene, RN-004 lo exige al 100 %. Si no viene, el metadato dice que el volumen no participó. El CSV del Sprint 1 no se modifica. | Habría que ampliar el importador y los CSV de prueba, y eso es cambio de US-004, no de US-008. |
| D-08 | ¿OR-Tools o DEAP entran si el GA no gusta estéticamente? | No entran por alineación de nombres con el C4. Solo se reabre la decisión con una medición EN-001 fallida después del paso 5. | Añadir OR-Tools trae ruedas nativas y un segundo modelo de restricciones a mantener junto al GA y a la reoptimización en vivo. |

---

## 15. Efecto sobre el Sprint 1

| Historia Sprint 1 | Superficie que el Sprint 2 puede alterar | Cómo se protege |
|-------------------|------------------------------------------|-----------------|
| EN-003 | `POST /optimizar-rutas` sigue siendo solo operador | No tocar `require_roles` ni los tests de auditor |
| US-001 | La flota y sus capacidades son entrada del validador | No cambiar el CRUD |
| US-002 | El filtro de placa ocurre antes del solver | Dejar `filter_vehicles_for_planning` donde está |
| US-003 | Solo `activo` entra al lote | Seguir filtrando `estado_operativo`, no el booleano suelto |
| US-004 | La fila sin coordenadas pasará a insertarse | Mantener rechazo por campo ausente y el tope de 150. Cambiar el pin a actualización, no a un segundo alta |
| US-006 | El solver sigue leyendo `ventana_inicio` / `ventana_fin` | No relajar el check de ventana invertida. La espera temprana se conserva |
| Seguimiento y mapa | ETA nulo en parada en revisión | El lector de seguimiento ya admite solución parcial; hay que no asumir ETA siempre presente en la UI |
| Reoptimización en vivo | Misma función `solve_vrptw` | Defaults compatibles y presupuesto propio más corto |

---

## 16. ¿El proyecto está preparado para comenzar US-005?

**Sí.** Se puede empezar por US-005 sin modificar el algoritmo genético y sin nuevas dependencias.

Motivos:

- PostGIS ya está en Docker, en el modelo y en la base de pruebas aislada.
- El pedido ya tiene punto WGS84, dirección y altitud.
- La importación ya distingue “sin punto” de “fila inválida”.
- El mapa ya permite clavar un pin; falta persistir el pendiente y actualizar ese registro en lugar de crearlo otra vez.
- El optimizador ya selecciona pedidos por estado, así que excluir `pendiente_validacion` es un filtro localizado.
- Las migraciones `001`…`006` tienen un mecanismo append-only donde cabe `007`.

Condiciones para el primer cambio de código, todas compatibles con empezar ya:

1. Adoptar D-01 y D-02 como están recomendadas (sin `geography` y sin GeoPy).
2. Escribir el polígono de las pruebas como fixture. El GeoJSON oficial (D-05) puede llegar en paralelo y no bloquea los tests.
3. No ejecutar migraciones contra la base de desarrollo `ecologistica` hasta que `007` esté revisada; la suite usa `ecologistica_test`.
4. Correr, en ese momento, `tests/test_day.py`, `tests/test_import_us004.py` y la prueba nueva de US-005 antes de abrir US-008.

US-007, US-008, US-009 y EN-001 no están listas para implementarse en paralelo con el primer corte de geocodificación: dependen de saber qué pedidos son elegibles y de no publicar soluciones ilegales. El orden de la sección 13 las deja en secuencia detrás de US-005.
