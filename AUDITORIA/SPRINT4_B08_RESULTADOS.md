# Sprint 4 — Resultados del incremento B-08

**Fecha:** 17/11/2026, America/Lima. **Versión del informe:** 1.0.0.
**Referencia previa:** `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1`. Sin commit nuevo.
**Estado:** implementación B-08 y pruebas sin BD completadas; **validación PostGIS pendiente**, por lo que no se declara aceptación integral ni cierre del requisito.

## 1. Objetivo y alcance autorizado

Aplicar una política común de validación antes de persistir/publicar rutas de planificación normal y reoptimización dinámica; impedir éxito ante soluciones inválidas o commit fallido. Solo se trabajó B-08, según [PLAN_SPRINT_4.md](PLAN_SPRINT_4.md) y [BACKLOG_IMPLEMENTACION.md](BACKLOG_IMPLEMENTACION.md).

Se utilizó `C:/Users/Baguette/Documents/Proyectos/ecologistica-junin`, ruta confirmada por el usuario en la fase anterior. La ruta `Proyectos2` repetida en el adjunto no existe en este equipo. Se revisaron también la auditoría, cumplimiento y matriz final; la consigna inicial original sigue sin localizarse, según el inventario de fase 1. No se reconstruyó su contenido ni se cambió el baseline.

Las dependencias permiten este incremento acotado: existen servicio de restricciones, prechequeo, modelo de solución/itinerario, capacidad volumétrica opcional, jornada configurable y filtro de placa. Se mantienen las reglas vigentes: se suma volumen declarado, llegada temprana permite espera y jornada = conducción + servicio, sin espera. No se redefine la jornada ejecutada ni se implementan funcionalidades B-04/05/07/13/24. Las mejoras del solver no son requisito para rechazar una salida inválida antes de publicarla.

## 2. Diagnóstico inicial y control de cambios

Inspección previa: `optimize_routes`, `fleet_map`, `_persist_solution`, `retain_other_vehicles`, `recalculate_route_etas`; `_reroute`, `_on_cancel`, `_apply_reroute`, selección de pedidos, asignaciones y emisión WS; `validate_for_publication`, prechequeo, jornada, ETA/matriz; `LiveReroute`, solver y sus dataclasses; modelos `SolucionRuta`/`RutaDetalle`/`Pedido`/`Vehiculo`; pruebas de restricciones, solver, realtime, ETA y GeoJSON.

Hallazgos:

- Planificación normal usaba `validate_for_publication`, pero el camino dinámico no lo invocaba antes de modificar pedidos/persistir.
- El validador confiaba en excesos y lista de no asignados informados por el solver; no detectaba pedidos omitidos silenciosamente ni contrastaba ETA final con ventana real.
- `_on_cancel` confirmaba cancelación y notificaba antes de saber si el recálculo sería aceptado.
- El mapa fijaba `feasible=True`; el payload dinámico también afirmaba factibilidad cuando no había solución, sin comprobar que el lote obligatorio estuviera vacío.
- Un añadido bloqueado podía anunciarse como incidente sin persistir ese estado, porque la aplicación de excepciones solo buscaba en el catálogo previo.

Git al inicio: ningún archivo rastreado modificado; cuatro documentos de planificación **preexistentes sin rastrear** en AUDITORIA. Se conservaron sin alteración. Se anunció antes de editar el conjunto de cuatro archivos de código y las pruebas correspondientes. No se tocaron cambios ajenos, README ni documentación histórica.

## 3. Archivos modificados y creados

| Archivo | Tipo y propósito |
|---|---|
| `app/services/route_constraints.py` | Modificado: servicio compartido reforzado, excepción de rechazo y clave de evidencia de publicación. |
| `app/services/realtime_router.py` | Modificado: selección común del lote dinámico y factibilidad del evento basada en validación. |
| `app/api/v1/websockets.py` | Modificado: prechequeo/filtro de flota, validación previa, cancelación atómica, excepciones de pedidos y orden commit→notificación. |
| `app/api/v1/routes.py` | Modificado: entrega explícita de validación a persistencia, evidencia por vehículo, mapa sin valor fijo y conservación/invalidez de esa evidencia. |
| `tests/test_hard_constraints_us008.py` | Modificado: fixtures de validador con ventana/estado operativo y bandera factible coherente con el caso de aceptación. No se relajaron aserciones. |
| `tests/test_publication_b08.py` | Nuevo: 28 casos sin BD, incluyendo orquestación con dobles y entidades ORM transitorias. |
| `tests/test_publication_b08_db.py` | Nuevo: 14 casos de API/PostGIS aislado; omitidos en este entorno por indisponibilidad de BD. |
| `AUDITORIA/SPRINT4_B08_RESULTADOS.md` | Nuevo: este informe; único documento nuevo de esta fase. |

Los cinco informes originales y los cuatro documentos de fase 1 permanecieron intactos. No se eliminaron archivos ni se modificaron dependencias, modelos, migraciones, autenticación o frontend.

## 4. Cambios implementados

### 4.1 Una sola validación de publicación

Se reutiliza `validate_for_publication` en ambos caminos. Ahora:

- Comprueba vehículo conocido, activo y operativo entre los elegibles; el dinámico aplica también el filtro de placa vigente y `precheck_fleet_capacity` existentes.
- Calcula peso y volumen declarado desde pedidos del itinerario y capacidades actuales; también rechaza excesos ya informados por el solver. No presume volumen cero como dato real ni añade un requisito de captura de volumen que corresponde a B-05.
- Recalcula conducción+servicio con el límite configurado; contrasta ETA con fin de ventana usando la misma tolerancia del servicio ETA. Llegar temprano conserva espera válida. ETA ausente o matriz no confiable impiden acreditar ventana.
- Exige cobertura del lote obligatorio, aun si el solver olvida incluir un pedido en `unassigned_order_ids`; rechaza duplicados, pedidos ajenos, código inconsistente y vehículo repetido/desconocido.
- Rechaza salida declarada infactible o con indicadores duros incompatibles. No modifica ni reemplaza el GA.
- Admite `solution=None` únicamente si no queda ningún pedido requerido; no equivale a aceptar la desaparición de pendientes.

`_persist_solution` requiere ahora el resultado de validación y rechaza un resultado negativo antes de añadir entidades o cambiar asignaciones. Los dos llamadores internos proporcionan la validación del lote completo.

### 4.2 Diferencias dinámicas explícitas y transacción

`select_reroute_orders` concentra la selección que ya existía: pendientes/añadidos, excluyendo cancelaciones explícitas y paradas realmente bloqueadas por el modelo de incidentes. La usan el generador y la orquestación. Se valida **todo el lote activo requerido**, no solo la secuencia que devuelve el solver. Además se verifica que secuencia, bloqueados y retirados coincidan con esa selección y la solución validada. Un solver no puede justificar omisiones inventando exclusiones.

El caso dinámico sigue siendo de un vehículo y utiliza el origen GPS existente; la redistribución avanzada, hora operativa acumulada y destino real son deuda B-24. No se añadieron tolerancias especiales al validador para que el recálculo pasara.

Cancelación, incidentes de pedidos, asignaciones y solución se confirman en la misma transacción del recálculo aceptado. Los añadidos bloqueados se buscan también en el catálogo de añadidos; los activos solo pasan a asignados al persistir el plan validado. Si se rechaza la solución, no se llega a esos cambios ni a commit. Al fallar la transacción, el contexto SQLAlchemy cierra/revierte; los tests PostGIS propuestos comprueban también fallo después de flush.

La secuencia en memoria y los eventos `route_update`, cancelado/asignado/incidente de pedidos y ETA del nuevo plan se actualizan/emiten **después del commit**. Ante rechazo WS se emite error, sin éxito de ruta. El aviso de un incidente vial de `_on_incident` continúa siendo un evento independiente en memoria y puede existir aunque no se encuentre nueva ruta; no afirma éxito del recálculo. Su durabilidad/gestión corresponde a B-25.

### 4.3 Factibilidad publicada y mapa

Las soluciones nuevas guardan en `metadatos_ga` la lista `vehiculos_validados_publicacion`. No se requiere migración: es una clave dentro del JSONB ya existente.

El mapa agrega evidencia **por vehículo mostrado**, en lugar de usar `True` fijo o la bandera de una única solución. Al retener vehículos de un plan anterior, solo conserva acreditación para aquellos que ya la tenían; copiar un plan histórico no lo valida. El recálculo independiente de ETAs invalida la acreditación anterior, porque sus tiempos cambiaron sin pasar por la política de nueva publicación. No se modifica su algoritmo ni se pretende resolver B-13 con ello.

### 4.4 Contrato de API

- HTTP conserva endpoints, formatos y estados principales: planificación aceptada 201; rechazo de publicación 409 con detalle estructurado. Puede haber nuevos rechazos antes ignorados, especialmente ETA no verificable, omisiones y asignación inconsistente.
- WS conserva `type=error` y `detail` de texto; agrega `validation` con diagnóstico estructurado de dominio. No emite `route_update` exitoso cuando rechaza.
- `route_update.feasible` procede del resultado compartido, incluso para una ruta vacía aceptada por no tener obligaciones restantes.
- `GET /api/v1/rutas/mapa` conserva la forma y booleano `metadata.feasible`. **Cambio de comportamiento:** devuelve false si cualquiera de los vehículos mostrados carece de evidencia de validación vigente. En rutas históricas o tras recálculo de ETA, false significa que la factibilidad no está acreditada por esta política, no que se haya probado una violación concreta. No se reescribieron datos antiguos para fabricar esa acreditación.
- `_persist_solution` y `route_payload` cambian firmas internas para requerir `publication`; no son endpoints públicos.

## 5. Pruebas creadas y relación con los diez escenarios

| Escenario solicitado | Evidencia ejecutada sin BD | Evidencia PostGIS preparada / estado |
|---|---|---|
| 1. Solución válida publicable | Caso factible real del solver y validador; persistencia ORM transitoria y mapa | `test_api_database_and_map_agree_after_valid_publication`: no verificado. |
| 2. Exceso de peso | Capacidad actual contra pedidos, aunque las banderas del solver no lo indiquen; regresiones previas | Rechazo HTTP y dinámico, sin cambios BD: no verificados. |
| 3. Exceso de volumen | Mismo control; prechequeo dinámico impide incluso ejecutar worker | Rechazo HTTP y dinámico: no verificados. |
| 4. Entrega fuera de ventana | ETA tardía con penalización cero se rechaza; ETA nula/matriz no fiable también | Rechazo HTTP y dinámico: no verificados. |
| 5. Jornada excedida | Se recomputa desde paradas, no solo bandera resumida | Rechazo HTTP y dinámico: no verificados. |
| 6. Obligatorios no asignados | Omisión con lista no asignada vacía, duplicados y pedido/vehículo ajenos | Rechazo HTTP y dinámico: no verificados. |
| 7. Dinámica inválida | Rechazo previo a persistencia; exclusión injustificada y placa no apta | Cinco variantes dinámicas con BD: no verificadas. |
| 8. Sin cambios parciales | Dobles prueban que rechazo no llama persistencia/commit ni cambia secuencia; cancelación no se confirma primero | Snapshot de planes/detalles/estados; cancelación rechazada y commit fallido tras flush: no verificados. |
| 9. Notificar tras persistencia | Se comprueba orden persist→commit→publish y ausencia de éxito si commit falla | Callback consulta desde conexión independiente antes de aceptar notificación: no verificado. |
| 10. API/BD/mapa coherentes | ORM transitorio+GeoJSON prueban bandera por evidencia, legado, copia de vehículos y cambio ETA | API 201/409, filas/estados y mapa tras publicación: no verificados. Totales ambientales/versiones completos siguen en B-13. |

Estos resultados no equiparan dobles con PostgreSQL ni tipado/inspección con aceptación E2E.

## 6. Ejecución y resultados

Entorno disponible: `.venv/Scripts/python.exe`, **Python 3.11.17**, **pytest 9.1.1**. No se usó el alias `python` de WindowsApps ni se instaló intérprete/dependencia.

1. Regresión previa a editar código: nueve pruebas de restricciones sin BD aprobadas, tres de integración excluidas.
2. Primera ejecución de los 18 casos nuevos iniciales contra código anterior: **13 fallidas y 5 aprobadas**. Reprodujeron capacidad basada solo en banderas, ventana no contrastada, omisiones/duplicados, elegibilidad y publicación/cancelación dinámica sin validación. Luego se aplicó la corrección y se añadieron pruebas de las otras ramas del incremento.
3. Ejecución final conjunta: **67 aprobadas, 0 fallidas, 14 omitidas y 9 deseleccionadas; una advertencia**. Las 67 incluyen 28 casos nuevos sin BD y 39 regresiones existentes de restricciones, solver, realtime, ETA, geometría y servicios auxiliares.
4. Las 14 nuevas pruebas de integración se recopilaron pero quedaron **no verificadas**. Las nueve existentes deseleccionadas requieren el fixture `client`/PostGIS y tampoco se acreditan como aprobadas.
5. `git diff --check`: sin errores de whitespace. Revisión del diff y búsqueda limitada de claves privadas/tokens GitHub/claves AWS en archivos afectados: sin coincidencias. No se afirma auditoría exhaustiva de secretos; las pruebas de integración usan las cuentas demo ya existentes de la semilla descartable, no credenciales productivas.

Comando final, desde la raíz en PowerShell, sin cobertura ni caché de pytest:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& '.venv\Scripts\python.exe' -B -m pytest -o addopts= -p no:cacheprovider tests/test_publication_b08.py tests/test_publication_b08_db.py tests/test_hard_constraints_us008.py tests/test_solver.py tests/test_realtime.py tests/test_optimizer_us007.py tests/test_eta_us009.py tests/test_route_geometry_geojson.py tests/test_unit_services.py -k 'not seed_optimize_regression and not fleet_insufficient_409 and not import_optional_volume and not driver_socket_rejects and not tracking_desk_receives and not optimize_geojson_eta and not recalculate_etas_endpoint and not optimize_seed_metadata and not jornada_filter_excludes' -q -rs
```

La advertencia procede de `tests/test_realtime.py`: deprecación de Starlette TestClient con httpx. No fue fallo ni motivó cambios de bibliotecas ajenos a B-08.

### Motivo exacto de la validación BD pendiente

`docker version` y `docker ps` no pudieron contactar `npipe:////./pipe/dockerDesktopLinuxEngine`: el conducto del motor no existe/daemon no disponible. Tampoco se detectó PostgreSQL escuchando en 5432/5433; las nuevas pruebas verifican conectividad al host/puerto configurado y marcan skip al no estar disponible.

No se inició Docker, no se conectó a BD operativa y no se ejecutó inicialización/migración/semilla. `tests/conftest.py` fuerza `ecologistica_test` antes de importar la aplicación y protege el reset; las nuevas pruebas BD verifican adicionalmente ese nombre. Para ejecutarlas posteriormente se necesita PostGIS accesible y un entorno descartable identificado; las fixtures de ese entorno sí crean/restablecen datos de prueba. No lanzar esa suite sobre una base productiva ni interpretar sus skips como pruebas exitosas.

## 7. Criterios cumplidos y pendientes

**Implementados y comprobados al nivel sin BD disponible:** validador único en ambos caminos; peso/volumen declarado, ventanas/ETA confiable, jornada conforme a regla vigente, cobertura exacta y elegibilidad; rechazo antes de modificar/persistir; cancelación agrupada en la transacción; éxito WS tras commit; mapa sin factibilidad fija; conservación prudente de evidencia por vehículo. Pruebas sin BD y regresiones seleccionadas verdes.

**Pendientes de acreditar:** rollback efectivo PostGIS y constraints reales; persistencia/asignaciones reales; conexión API–BD–mapa; éxito visible desde otra conexión antes de notificar; transporte WebSocket contra servidor real y ensayo UI. Las pruebas preparadas permiten comprobar gran parte de ello, pero no se ejecutaron por indisponibilidad de infraestructura. Por tanto **B-08 no se marca aceptado/cerrado integralmente**.

## 8. Riesgos y problemas que permanecen

- B-09: autorización por asignación vigente, terminalidad de entregas y concurrencia de planificaciones no resueltas. Mover el commit de cancelación fue indispensable para atomicidad B-08; no implementa toda la política de estados/roles.
- B-10/11: privacidad de WS público, limpieza de canales, expiración/revalidación/revocación y límites siguen abiertos. Autenticación no fue modificada.
- B-05: falta de volumen conserva limitación existente; no se puede acreditar capacidad volumétrica de datos desconocidos.
- B-07/21: el algoritmo puede devolver infactibilidad y el SLA completo sigue sin validar. Este incremento la rechaza; no mejora su tasa de factibilidad ni rendimiento.
- B-13: copias, ETA, totales, geometría y deduplicación de actividad aún requieren corrección. Solo se gestionó la evidencia de factibilidad para no afirmar validación sobre un vehículo histórico o tiempos cambiados.
- B-24/25: dinámica de un vehículo, reloj/carga/jornada acumulada, destino, incidentes en memoria y durabilidad siguen pendientes. El aviso vial independiente puede conservarse aunque falle el recálculo.
- Mayor tasa de rechazos visibles es esperable: casos antes publicados indebidamente ahora fallan. No relajar el validador para ocultar defectos del solver/datos.
- Legado sin marca de validación se muestra no acreditado (`feasible=false`); requiere nueva planificación validada o una futura revalidación explícita, nunca backfill ciego de true.

## 9. Integridad y artefactos

Inventario SHA-256 en memoria antes de editar: 407 archivos, excluyendo `.git`, `node_modules` y `.venv`. Tras código y pruebas: 409 archivos; exactamente cinco preexistentes modificados —los cuatro fuentes y el test de restricciones—, dos pruebas nuevas y cero bajas. La única alta documental posterior es este informe: total esperado 410. La comparación preservó los cinco informes originales y los cuatro planes preexistentes, además de README y documentación histórica.

Se desactivaron bytecode, cobertura y caché de pytest en los comandos ejecutados. La comparación no detectó cambios/altas de cachés, coverage, dist ni otros artefactos en el árbol inventariado. No se generaron logs/capturas auxiliares ni se instalaron dependencias. El inventario excluye los árboles indicados y no representa vigilancia de todo el sistema de archivos.

No hubo commit, push, cambios de esquema ni modificaciones a registros productivos. Los archivos nuevos quedan disponibles para revisión del usuario.

## 10. Siguiente paso recomendado

Primero disponer de PostGIS descartable y ejecutar los 14 casos de integración B-08, junto con las nueve regresiones de integración omitidas, antes de aceptar este incremento. Corregir cualquier fallo observado manteniendo el alcance. Después, con revisión del usuario, el siguiente ítem del backlog recomendado es **B-09: autorización vigente y transiciones de estados**. No se inició B-09, B-10, B-11 ni otra tarea.
