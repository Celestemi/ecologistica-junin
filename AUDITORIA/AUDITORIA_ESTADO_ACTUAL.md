# Auditoría del estado actual de EcoLogística

Fecha de corte: 16 de noviembre de 2026 (America/Lima). Versión de auditoría: 1.0.
Proyecto: C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin.
Referencia Git inspeccionada: 967efdfac77d14eb0ffb14210637640c13f9c332.
Alcance: lectura del proyecto y escritura exclusiva de los cinco informes en AUDITORIA.

## Dictamen

El producto tiene una base funcional considerable: flota, pedidos por jornada, importación CSV/XLSX, autenticación, algoritmo genético, mapas, indicadores, PDF y modo conductor con almacenamiento offline. El código conecta estos componentes con persistencia real; no es únicamente una maqueta.

El desarrollo se encuentra en **consolidación del Sprint 3 de la consigna**, con trabajo adelantado y parcial del Sprint 4 en reoptimización. El sprint más avanzado con código es el **4**. **No se acredita ningún sprint completamente terminado** con todos sus entregables y aceptación. Esta conclusión no depende de las semanas transcurridas ni de los nombres de las carpetas históricas.

La estimación general es **53,5 % de avance de implementación**, con incertidumbre técnica y de aceptación; no es un porcentaje de funcionamiento probado. El MVP presenta **67,1 % de implementación parcial estimada**, pero **0 de 7 RF completamente implementados y verificados: 0 % de cumplimiento estricto acreditado**. Cada RF-01 a RF-07 tiene alguna brecha concreta; no se les asigna cero por la mera omisión de pruebas durante esta auditoría. Para alcanzar al menos 70 % se necesitan **5 de 7 completos (71,4 %)**.

La fórmula, las listas de comprobación y el detalle RF/RNF se encuentran en [CUMPLIMIENTO_REQUERIMIENTOS.md](CUMPLIMIENTO_REQUERIMIENTOS.md). Los porcentajes de sprint son 85 %, 70 %, 50 % y 26 %; sus actividades tienen pesos independientes del indicador general.

## Método y límites de verificación

Se inspeccionaron estructura, manifiestos, código backend/frontend, modelos, migraciones, pruebas, configuración de despliegue y documentación. Se cruzaron modelos y esquemas de API con sus consumidores; se siguieron los caminos de planificación, persistencia, recálculo, seguimiento y reporte. Se buscaron módulos de clientes, conductores, tráfico, compensación, aceptación y manuales.

La consigna adjunta es la referencia para RF-01…RF-10, RNF-01…RNF-07 y las cuatro iteraciones. El catálogo del repositorio usa MRF-01…MRF-07, RF-001…RF-018 y RNF-001…RNF-005. **Los identificadores no son equivalentes numéricamente**: por ejemplo, RF-008 interno son restricciones del solver y RF-08 de esta auditoría es gestión de conductores. Se conserva una correspondencia explícita en el informe de cumplimiento.

Jerarquía de evidencia:

1. Comprobación segura ejecutada en esta auditoría.
2. Comportamiento deducible de un camino de código conectado.
3. Artefactos históricos locales, con fecha y límites.
4. Declaraciones documentales sin resultados originales suficientes.

Un test escrito no implica un test aprobado; cobertura no implica aceptación del requisito. Las severidades de analizadores no se confunden con explotación confirmada.

No se inició el sistema, no se llamó a API del proyecto, no se inició Docker, no se conectó a PostgreSQL y no se consultaron registros. No se puede confirmar esquema físico, migraciones aplicadas, datos actuales, certificados, estado del despliegue ni disponibilidad externa. Incluso algunos GET, como la configuración por placa o validación de área, pueden inicializar datos; por eso no se usaron como comprobación de solo lectura.

No se ejecutaron pytest ni inicializadores: tests/conftest.py:60 crea una BD; :73 trunca tablas y actualiza usuarios; :94 y :103 activan las fixtures. Tampoco se ejecutaron npm build, Vitest/coverage, npm audit, SonarScanner, migraciones o instaladores: sus salidas/cachés no estaban garantizadas dentro de AUDITORIA o modificaban el estado. Python no estuvo disponible a través de python: el comando resuelve a un alias de Microsoft Store. No se intentó instalarlo.

No se afirman ausencia de CVE, conformidad legal, certificación ISO, accesibilidad integral ni cumplimiento del SLA.

## Arquitectura y tecnologías

| Capa | Tecnología y ubicación | Conexión efectiva |
|---|---|---|
| SPA | React 18, TypeScript, Vite 7, Tailwind 4; src/main.tsx, src/App.tsx | Selección de pantallas por pathname, carga lazy y restricciones de navegación por rol. |
| API cliente | src/api.ts | fetch a /api/v1; JWT Bearer; descarga PDF y manejo 401/403. |
| Mapas | Leaflet 1.9/react-leaflet 4; Map.tsx y PinMap.tsx | Teselas OpenStreetMap; GeoJSON producido por backend. |
| Backend | FastAPI, Pydantic 2; app/main.py y app/api/v1 | REST y WebSockets en el mismo proceso ASGI. OpenAPI condicional al entorno. |
| Negocio | app/services | Importación, ventanas, estados, seguridad, solver, indicadores, PDF y seguimiento. |
| Persistencia | SQLAlchemy 2 async, asyncpg, GeoAlchemy2, Shapely | PostgreSQL/PostGIS; Geometry SRID 4326 y JSONB. |
| Optimización | GA propio en genetic_solver.py | Matriz Haversine por defecto u OSRM opcional; ejecución en un hilo acotado. |
| Tiempo real | websockets.py y realtime_router.py | GPS e incidentes en memoria; cambios de pedidos y nuevas soluciones en BD. |
| Reportes | ReportLab, pdf_generator.py | PDF en BytesIO, devuelto por StreamingResponse. |
| Offline | IndexedDB, public/sw.js, vite.config.ts | Cola de entregas por usuario y caché del shell; sincronización mediante ventanas abiertas. |
| Operación | Docker Compose, Uvicorn, Nginx | Nginx sirve SPA y proxy /api, /ws; PostGIS con volumen; SonarQube adicional. |
| Calidad | pytest, Vitest, Testing Library, coverage, SonarQube | Workflow CI con PostgreSQL, SCA Python y análisis Sonar opcional. |

Flujo normal: pedidos manuales o importados → validación de ventanas y punto → selección de jornada/flota activa → filtro de placa → prechequeo de capacidad → GA → validación para publicación → SolucionRuta/RutaDetalle y pedidos assigned → GeoJSON/tabla/conductor → entrega → indicadores/PDF.

Flujo de incidentes: mensaje WebSocket → estado en memoria → recálculo de un vehículo → persistencia de otra solución y copia parcial de otros vehículos → notificaciones. Este camino no aplica todos los controles del planificador normal.

La arquitectura activa es un **monolito modular con SPA**, no microservicios. Redis, Celery, OR-Tools y DEAP aparecen en planificación histórica, pero no en dependencias/runtime activos. No existe servicio OSRM local en Compose; se apunta por defecto a un endpoint público de demostración.

## Módulos y conexiones reales

| Módulo | Código conectado | Estado observado |
|---|---|---|
| Acceso | auth.py, deps.py, access.py, passwords.py, tokens.py; Login.tsx y session.ts | Login, JWT, bcrypt, bloqueo y roles; administración del ciclo de vida de usuarios ausente. |
| Flota | domain.Vehiculo; desk.create_vehicle/update_vehicle; Fleet.tsx | Alta, edición, inactivación/mantenimiento e historial; falta tipo explícito de vehículo exigido en el baseline. |
| Pedidos | Pedido; routes.create_order/update_order_window/update_order_location; order_import.py; OrdersDay.tsx | Importación y geocodificación limitada conectadas; faltan prioridad, producto y volumen consistente en alta/lectura/UI. |
| Optimización | solve_vrptw → validate_for_publication → _persist_solution | Motor real, con restricciones y baselines; no acredita SLA válido 150×15. |
| Mapa | /rutas/mapa; _feature_collection; MapView, RouteTable y StopDetail | Puntos, filtros, ETA y trazado cuando hay geometría vial. Sin OSRM se ocultan las líneas y se advierte; no se dibujan rectas como calles. |
| Dashboard | /indicadores → summarize_indicators → Dashboard.tsx | Datos calculados desde soluciones persistidas; faltan ahorro monetario y cumplimiento real. |
| PDF | /reportes/sostenibilidad/pdf → load_sustainability_report/build_sustainability_pdf; StaffHeader.tsx | Descarga real implementada; cifras y periodo necesitan correcciones. |
| Conductor | /rutas/activas y /pedidos/{codigo}/entrega; DriverApp.tsx | Ruta, GPS, incidentes y entrega offline; firma/foto son solo interfaz sin conservación del comprobante. |
| Seguimiento | REST público con token opaco y WS por pedido | REST minimiza datos; WS no aplica la misma minimización. |
| Clientes | Nombre embebido en Pedido y seguimiento público | No hay gestión de clientes ni preferencias. |
| Compensación | quinual_equivalent y presentación en dashboard/PDF | Equivalencia de emisiones evitadas; no hay plan de compensación de emisiones residuales. |

No se declara un módulo completo por existir su pantalla. Los flujos básicos citados están implementados en código; ninguno de los diez RF integrales alcanza aceptación completa acreditada.

## Algoritmo de optimización

### Identificación y funcionamiento

Es un **algoritmo genético real**, no GA simulado, ni Tabú, SA o ACO. Evidencias principales: genetic_solver.py:446 solve_vrptw; :684 _initial_population; :869 _order_crossover; :884 _ox_permutation; :899 _swap_mutation; :909 _transfer_mutation; :926 _tournament; :931 _evaluate.

Un individuo distribuye ids de pedidos en una secuencia por vehículo. Se crean semillas FIFO, secuencial, ecológica y vecino cercano; para más de 60 pedidos se simplifican las semillas. Se completa la población con individuos aleatorios, se repara la representación, se evalúa y se seleccionan padres por torneo. El cruce OX conserva orden; las mutaciones intercambian visitas o transfieren una a otro vehículo. Hay elitismo de un individuo, caché de evaluaciones, semilla reproducible, presupuesto temporal y parada por estancamiento factible.

Los defaults son 100 generaciones y población 50; resolve_ga_parameters reduce 150 pedidos a 32 generaciones y población 24. El vehículo_count se ignora al ajustar estos parámetros. El motor minimiza una suma ponderada, no un frente multiobjetivo:

fitness = km + 25 × CO2_kg + 80 × minutos_tarde + 200 × exceso_kg + 250 × exceso_m3 + 120 × exceso_jornada_min + 8000 × no_asignados + 4000 × entradas_históricas.

Las rutas por FIFO y secuencial son comparaciones reales y semillas, no la totalidad del mecanismo de generación. La función _repair mantiene pertenencia y distribución; no constituye un reparador suficiente de factibilidad temporal.

### Restricciones y objetivos

| Aspecto solicitado | Tratamiento real | Límite |
|---|---|---|
| Distancia | Matriz Haversine o distancia OSRM; objetivo directo | Haversine no representa kilómetros viales. |
| Tiempo | OSRM o 25 km/h; servicio fijo 5 min, espera y ETA | No hay tiempos por producto/cliente; origen temporal de recálculo incorrecto. |
| Capacidad | Peso y volumen declarado; penalización y bloqueo normal | Volumen puede ser nulo; no se garantiza capacidad volumétrica total. |
| Ventanas | Clasificación, espera, penalización de retraso; bloqueo normal | Celdas no confiables asignan late_minutes=0 y omiten la comprobación efectiva. |
| Combustible | Tipo influye en factores de emisión | Rendimiento no entra en el objetivo; consumo se estima después. |
| CO2 | g/km por vehículo y recargo por desnivel positivo | Fórmula distinta de core/emissions; sin calibración local acreditada. |
| Retrasos | Penalización 80/min y rechazo normal | Reoptimización omite validate_for_publication. |
| Conductores | Límite global conducción+servicio de 480 min | Sin licencia, disponibilidad individual, descanso ni jornada acumulada; espera excluida. |
| Tráfico | Eventos manuales: multiplicador 1,8 y rodeo 2×radio | Sin proveedor de tráfico; el ajuste altera distancia para representar lentitud. |
| Operación/ambiente | Activo/mantenimiento, placa validada, centro histórico aproximado | Centro histórico es penalización blanda; no hay restricciones por red vial/zonas oficiales. |

### Limitaciones comprobadas por inspección

- La comprobación de presupuesto en :541 ocurre entre generaciones. Construcción inicial de población, evaluación de generación, baselines finales y solicitudes de geometría no tienen una interrupción global estricta. _Problem.leg_coordinates:357 llama a get_leg para los candidatos; osrm_client.py:129 obtiene geometría por HTTP sin deadline global. El SLA HTTP no se deduce del presupuesto de 45 s.
- tests/test_solver_sla_en001.py:64 solo exige tiempo, alguna asignación y generaciones; no exige feasible ni 150 asignaciones. El informe de benchmark :86 registra resultados pero solo afirma que hay filas. Aprobar esos tests no acredita RNF-01.
- La revisión histórica Sprint 2 reporta tiempo aproximado de 0,89 s y falta de factibilidad sistemática. El informe original referenciado está eliminado previamente; no se adopta ese número como una medición actual ni se concluye que todos los conjuntos 150×15 sean infactibles.
- _schedule_vehicle:1022 fija la salida según la primera ventana, sin parámetro now. El recálculo mueve el depósito al GPS actual, pero no fija la hora actual ni conserva el depósito real como destino; puede programar en el pasado y regresar al punto GPS.
- solve_vrptw conserva best_feasible, pero al terminar normalmente selecciona min(population) salvo salida por presupuesto. Al ser las penalizaciones finitas, no existe garantía de escoger una solución factible encontrada.
- Los ahorros del 15 % en km y 10 % en CO2 son indicadores informativos. No se imponen como validación dura ni se acreditan con serie operativa mensual.
- La línea base secuencial conserva el orden recibido, aunque su docstring dice por id; _require_pending_orders ordena por ventana e id. Debe fijarse y documentarse una comparación consistente.

Mejoras necesarias: factibilidad antes de calidad, reparación temporal/capacidad, publicación común para ambos caminos, estado inicial real de recálculo, red vial confiable, presupuesto extremo a extremo y benchmarks con referencia factible, múltiples semillas y resultados auditables. Evaluar búsqueda local/2-opt o warm start después de corregir estas garantías; no es obligatorio reemplazar el GA por otra biblioteca.

## Base de datos

### Esquema declarado

Son **14 tablas ORM**, más schema_migrations creada por el migrador. Son tablas declaradas, no un inventario confirmado de una instancia activa.

| Tabla | Modelo | Relaciones y propósito |
|---|---|---|
| depositos | domain.Deposito | Vehículos y soluciones referencian depósito. |
| vehiculos | domain.Vehiculo | FK a depósito; detalles, historial y asignaciones referencian vehículo. |
| pedidos | domain.Pedido | FK opcional jornada; detalles referencian pedido; cliente solo como nombre. |
| soluciones_ruta | domain.SolucionRuta | FK depósito; metadatos GA JSONB, totales y referencia. |
| rutas_detalle | domain.RutaDetalle | FK solución/vehículo/pedido; secuencia, geometría, ETA y emisiones. |
| usuarios | identity.Usuario | Roles, hash, bloqueo, activo; bitácora y asignaciones. |
| bitacora | identity.Bitacora | FK usuario SET NULL; acción, fecha y detalle. |
| jornadas | operations.Jornada | Fecha única; pedidos asociados opcionalmente. |
| asignaciones_conductor | operations.AsignacionConductor | FK usuario y vehículo CASCADE; activa. |
| area_operacion | operations.AreaOperacion | Multipolígono operativo; sin catálogo distrital. |
| historial_vehiculo | operations.HistorialVehiculo | FK vehículo; cambios operativos y actor. |
| restriccion_placa_config | restrictions.RestriccionPlacaConfig | Configuración/validación y reglas. |
| restriccion_placa_reglas | restrictions.RestriccionPlacaRegla | FK configuración CASCADE; dígito y días. |
| historial_restriccion_placa | restrictions.HistorialRestriccionPlaca | Auditoría de parametrización por placa. |

Hay claves foráneas, placa/código/correo únicos, checks positivos, ventanas ordenadas, coherencia entre ubicación y estado, índices espaciales y de estados. RutaDetalle impide repetir secuencia por vehículo/solución y pedido por solución. Esto es evidencia de diseño de integridad, no validación de registros existentes.

### Migraciones y consistencia

app/db/migrations.py contiene ocho migraciones SQL versionadas: token; asignaciones; modelo/rendimiento; estado operativo; historial; placa; geocodificación/volumen/área; ETA. El migrador registra versiones en schema_migrations. No usa Alembic ni muestra downgrades. init_db.py:219 combina extensión PostGIS, create_all, ALTER jornada y migraciones, seguido de semillas/backfills.

Hallazgos de diseño:

- Geometría de tramo en domain.py:303 carece de migración ALTER equivalente. Una instalación antigua que no tenga esa columna no se actualiza mediante create_all; el error operativo depende del esquema instalado, no consultado.
- La migración 002 crea índice único parcial de conductor activo por usuario; el modelo ORM no lo declara. La integridad difiere si alguien inicializa solo metadata sin migraciones.
- No hay unicidad de vehículo por asignación activa ni validación SQL de que usuario.rol sea conductor. La regla de exclusividad debe definirse y luego validarse.
- Faltan entidad cliente/preferencias, ficha conductor/licencias/turnos y vínculo conductor-ruta, incidentes durables, eventos de entrega con hora/comprobante, y plan de compensación.
- Pedido no almacena prioridad ni tipo_producto; volumen nullable existe en BD/importación pero no en PedidoCreateRequest, PedidoRead y tipos/UI completos.
- Vehiculo no tiene tipo_vehiculo explícito. Para eléctricos exige rendimiento_km_gal; el dashboard estima galones para toda la flota. Se necesitan unidades por energía.
- Faltan criterios de versión vigente/ejecutada para agregar soluciones: estado tiene computed/published/archived, pero no se aplica un ciclo que excluya planes sustituidos de KPI/PDF.
- Hay riesgo de concurrencia de planificación: el semáforo cubre el cálculo en un proceso, no selección/persistencia transaccional de pedidos ni múltiples workers. No se encontraron locks/versiones para esa reserva.
- Índices para fecha/jornada, búsquedas históricas y selección de solución vigente requieren evaluación con EXPLAIN/carga; no se afirma lentitud medida.
- El diseño previsto de docs/01 Inicio/11 incluye cliente, conductor, distritos, incidentes y KPI separados, distintos de los modelos activos. Geometry/Haversine frente a GEOGRAPHY/UTM debe documentarse como decisión; no se sostiene que Geometry sea inválido por sí mismo.

## Catálogo de problemas y recomendaciones

“Confirmado” significa que el código o artefacto exhibe la condición. El impacto operativo se distingue cuando depende de un escenario aún no ejecutado.

| ID | Condición y evidencia | Impacto | Prioridad | Recomendación |
|---|---|---|---|---|
| H-01 | Confirmado: websockets._reroute:297-309 persiste sin validate_for_publication ni solution.feasible. fleet_map:559 responde feasible=True fijo. | Puede publicar y presentar como válida una ruta infactible. | Alta | Reutilizar prechequeos/validador; rechazar sin persistir y reflejar factibilidad real. |
| H-02 | Confirmado: reoptimize_live_route:397 usa [vehicle]; IncidentKind:42 no incluye avería/accidente. | No redistribuye ante avería ni cubre todos los eventos RF-07. | Alta | Replanificar flota disponible, conservar entregas y carga remanente. |
| H-03 | Confirmado: genetic_solver._schedule_vehicle:1024, realtime_router:387 y :454. | Recálculo sin reloj real y retorno al GPS convertido en depósito. | Alta | Separar origen, destino y hora; conservar trabajo ejecutado. |
| H-04 | Confirmado: genetic_solver._visit:1116-1140 pone atraso cero ante matriz no confiable; route_constraints:206 solo revisa atraso positivo. | Se puede aprobar una ventana no comprobada. | Alta | Estado no publicable o política explícita de estimación y aceptación. |
| H-05 | Confirmado: retain_other_vehicles:940-967 suma km/min pero no CO2 emitido, omite geometria/estados ETA y usa máximos de ahorros. | Totales y detalle divergen después de recálculo. | Alta | Recalcular agregados homogéneos y copiar metadatos completos/versionar plan. |
| H-06 | Confirmado: /indicadores:576 y pdf.load_sustainability_report:174 incluyen todas las soluciones del periodo. | Recuentan planes iniciales y recálculos como actividad adicional; no es consumo ejecutado. | Alta | Definir plan vigente/eventos ejecutados y evitar doble conteo. |
| H-07 | Confirmado: confirm_delivery:503 y _require_order_on_vehicle_route:419 aceptan cualquier asociación histórica. | Si se reasigna un pedido, un conductor anteriormente asociado puede actuar sobre él. No se explotó. | Alta | Autorizar contra asignación y versión vigente del pedido. |
| H-08 | Confirmado: _on_cancel:247 cambia estado sin impedir delivered → cancelled. | Un mensaje válido puede alterar una entrega completada de su ruta. | Alta | Máquina de estados y rechazo de transiciones terminales. |
| H-09 | Confirmado: tracking_socket:128 enlaza token público a canal interno; snapshot:449 y manager.publish:205 envían payload sin minimización. | Expone GPS exacto/identificadores y secuencia de otros pedidos a poseedores del enlace. | Alta | Separar audiencia pública y personal; filtrar campos por destinatario. |
| H-10 | Confirmado: core/emissions.py:38 y genetic_solver.py:404 tienen fórmulas distintas; solo la segunda genera rutas. | La corrección de altitud por combustible está desconectada del optimizador. | Alta | Unificar metodología, unidades, factores y prueba numérica independiente. |
| H-11 | Confirmado: confirm_delivery no guarda body.delivered_at; _completion_day:634 usa ETA o fin de ventana. | PDF atribuye fecha estimada a entrega real; no permite KPI puntualidad real. | Alta | Guardar evento y fecha real; distinguir planificado y ejecutado. |
| H-12 | Confirmado: DriverApp:271 envía solo id/código/hora; modal:474/600 conserva firma/foto en estado local. | “Comprobante” no se almacena ni transmite; la UI aparenta una evidencia inexistente. | Alta | Guardar evidencia real y asociarla al evento/cola o aclarar alcance UI. |
| H-13 | Confirmado: tests/test_solver_sla_en001.py:80-82 omite factibilidad/completitud; geometría HTTP ocurre dentro de evaluaciones. | SLA de solución válida sin probar; presupuesto no es límite extremo a extremo. | Alta | Benchmark factible conocido y medición HTTP incluyendo matriz/geometría/BD. |
| H-14 | Confirmado: falta migración para geometria_tramo; modelos/domain.py:303, migrations.py:8. | Actualización de BD antigua puede fallar al consultar/escribir la columna. Instancia no inspeccionada. | Alta | Migración versionada y prueba de upgrade desde esquema previo. |
| H-15 | Confirmado: volumen fuera del alta/lectura estándar; sin prioridad/producto. | RF-02 incompleto y restricciones volumétricas incompletas. | Alta | Alinear modelo, API, importación y formulario/tipos. |
| H-16 | Confirmado: summarize_indicators:65-72 aplica km/gal sin combustible; PDF usa costos desde CO2 y supuestos constantes. | Galones para eléctricos y costos no conciliados; ahorro económico ausente. | Alta | Separar litros/galones/kWh, fuentes y comparación monetaria consistente. |
| H-17 | Confirmado: Compose:37-44 es demo/HTTP y OSRM público; TLS es archivo .example. | Configuración no acredita seguridad ni disponibilidad productiva. Exposición externa no comprobada. | Alta | Perfil de producción con secretos, TLS/proxy confiable y servicios contratados/controlados. |
| H-18 | Confirmado: public SW actual y dist/sw.js son versiones diferentes; audit-green-build:14 falla. | Artefactos locales no representan la política offline actual. No prueba qué versión está desplegada. | Media | Reconstruir/verificar luego, con autorización para escribir dist; hacer el script robusto. |
| H-19 | Confirmado: FleetState/ConnectionManager son diccionarios/listas en memoria. | Incidentes/posición se pierden al reiniciar y no se comparten entre procesos. | Alta | Estado durable y bus compartido; persistencia/expiración de incidentes. |
| H-20 | Confirmado: no hay módulo clientes, ficha conductor, tráfico externo ni plan de compensación. | RF-08/09/10 y alcance de tráfico sin completar. | Media | Backlog con prioridad posterior al cierre del MVP salvo dependencias del solver. |
| H-21 | Confirmado: pyproject addopts fija cov-fail-under=0; CI no agrega npm audit; deploy-staging solo imprime instrucciones; Sonar opcional. | Calidad mínima/seguridad frontend y despliegue no son gates garantizados. | Alta | Umbrales explícitos, SCA completo y staging reproducible. |
| H-22 | Confirmado: README contradice acta Sprint 3; conteos históricos 136/143 y 67/68; enlaces a documentos eliminados previamente. | No permite acreditar cierre mediante una fuente coherente. | Media | Actualizar trazabilidad después de validar código; conservar fecha, commit y resultados originales. |
| H-23 | Confirmado: optimizer utiliza centro histórico de coordenadas fijas; área dev provisional; geocodificador por seis frases. | Direcciones que contienen “chilca”/“ferrocarril” se concentran en un hito; geografía no validada. | Media | Precisar coincidencia, confirmar pin, usar límites y fuentes verificables. |
| H-24 | Confirmado: WebSocket JWT en URL y comprobado solo al conectar; no hay revocación ni rate limit general. | Riesgo de logs con token, sesiones largas y abuso; no es evidencia de filtración ocurrida. | Alta | Credencial breve de socket, redacción de logs y revalidación/límites. |
| H-25 | Confirmado: Dashboard:29-33 recarga por fechas, no por id/versión de solución; request:43 solo admite detail string. | Optimizar otra vez el mismo día puede dejar KPI viejos; violaciones 409 estructuradas se reducen a error genérico. | Media | Invalidar por versión y presentar mensaje/violaciones de negocio. |
| H-26 | Confirmado: sequence_eta.py:101 cambia km/CO2 detalle sin totales/geometría; programa por depósito/ventana. | Recálculo “solo ETA” deja cabecera y tramos inconsistentes. | Alta | Definir alcance de recálculo y actualizar conjunto coherente en transacción. |
| H-27 | Riesgo de concurrencia identificado: offline.ts:54 y DriverApp:110-118 hacen leer/modificar/escribir cola sin exclusión. | Encolado durante sincronización o dos ventanas pueden perder entradas; no se reprodujo. | Alta | Transacciones por operación, exclusión de sincronización y prueba concurrente. |
| H-28 | Confirmado: PDF:260-263 imprime 12 kg/año fijo aunque cálculo usa configuración; :224 desactiva compresión. | Si cambia factor, texto y cálculo difieren; PDF más pesado. | Media | Usar factor con versión/fecha y compresión adecuada. |
| H-29 | Confirmado: tracking_socket:140 registra channel_code y :150 desconecta order_code original. | En token público, desconexión no retira la suscripción hasta un envío posterior que detecte socket muerto. | Media | Desconectar usando la misma clave y probar limpieza. |
| H-30 | Confirmado: DriverApp:63/232 usa ubicación de la siguiente parada cuando no hay GPS y la publica como position. | Despacho/cliente pueden recibir una posición sintética como ubicación actual. | Alta | Señalar origen/precisión y no publicar coordenada inventada como GPS. |

No se atribuyen como errores críticos ejecutables los sort() sin comparador reportados por Sonar: las listas de placas son strings y la criticidad del analizador no demuestra un fallo del negocio. El uso de random.Random en GA/benchmark es deliberado y no genera tokens; tracking_tokens.py usa generación opaca mediante secrets. Debe revisarse el hallazgo estático en su contexto.

Duplicación confirmada de lógica: fórmulas de CO2 divergentes y conjuntos de roles duplicados entre desk.py/plate_restrictions.py y rbac.py. Sonar informa 0 % de duplicación histórica, pero eso no elimina duplicación semántica. No se identificó una dependencia runtime que pueda declararse innecesaria con evidencia suficiente; openpyxl sí se utiliza. Hay duplicación de inventario Python entre requirements y pyproject, y Docker instala rangos >= sin usar uv.lock: se requiere reproducibilidad, no una eliminación automática de paquetes.

## Pruebas y evidencia local

| Verificación | Resultado de esta auditoría | Alcance |
|---|---|---|
| node --version | v26.8.2 | Entorno local distinto de Node 22 declarado en CI. |
| node node_modules/typescript/bin/tsc --noEmit --incremental false | Código 0 | Tipado frontend; no build, backend ni comportamiento real. |
| node --test scripts/test-service-worker.mjs | 4 aprobadas, 0 fallidas | VM y cachés en memoria; no navegador/PWA real. |
| node scripts/audit-green-build.mjs | Código 1, TypeError al leer BUILD_ASSETS, línea 14 | Artefacto dist preexistente con SW antiguo. No se reconstruyó. |
| python -B | No disponible mediante el comando python | No se ejecutó código Python. |
| Pytest/BD/solver HTTP | No ejecutados | Fixtures con mutaciones; no se provocaron. |
| Vitest/build/SCA/Docker | No ejecutados | Mantener restricción de escritura y estado. |

Hay 139 definiciones Python test_* y 69 invocaciones it/test en frontend según búsqueda textual; no son conteos de casos ejecutados ni excluyen parametrización. Las pruebas cubren autenticación/RBAC, flota, estados, placa, pedidos, importación, geocodificación, ventanas, solver, capacidad, ETA, OSRM, geometría, PDF, indicadores, realtime, mapas y offline con dobles. No hay suite de aceptación integral contra servicio desplegado ni prueba del objetivo de 1000 pedidos/50 vehículos o disponibilidad 99,5 %.

Artefactos existentes, leídos sin alterarlos:

- coverage.xml: fecha interna 2026-10-27 19:15:17 UTC; líneas 3491/4306 = 81,07 %, ramas 576/1044 = 55,17 %.
- coverage/backend-coverage-final.json: cobertura combinada líneas+ramas 76,0187 %. **81,07 % de líneas no equivale a 81,07 % combinado**.
- coverage/frontend/coverage-summary.json: líneas 90,91 %, ramas 84,52 %, funciones 80,65 %.
- .pytest_cache: 136 nodeids y lastfailed vacío. Es caché histórica, no acta de ejecución actual.
- Reporte Sonar documental: 82,1 % global, gate de código nuevo OK, 16 bugs, 10 vulnerabilidades informadas y 4 smells; no se consultó servidor ni se confirmó estado actual. No deben sumarse esas cifras a cobertura de pytest/Vitest.

## Estándares, documentación y restricciones

La matriz completa está en el documento de cumplimiento. Hay medidas parciales de OWASP, accesibilidad y eficiencia, pero ningún estándar se acredita integralmente. WCAG 2.1 AA requiere evaluación de criterios aplicables y procesos completos; el documento histórico de WCAG 2.2 declara 2 tipos/3 nodos con fallos en operador y revisiones manuales pendientes. Lighthouse 100 no es conformidad.

ISO/IEC 25010 se utiliza como marco de calidad; faltan resultados completos y trazables. ISO 14083 se menciona en el PDF, pero solo se modela CO2 operativo con factores asumidos, sin verificación integral de metodología, límites y gases. Green Software presenta reducción de trabajo/transferencia, no una medición energética o SCI acreditada. Los valores digitales hipotéticos en informes previos no son ahorros medidos del proyecto.

Existen acta, visión, requisitos, reglas, stack, modelo C4/ER, planificación, riesgos, presupuesto, revisiones y reportes de calidad. No se encontraron manuales completos de usuario/administración, guía operativa de backup/restore y despliegue productivo ni documentación final consolidada. OpenAPI se genera en código, pero en producción está deshabilitado y no hay exportación versionada verificada. Los manuales no se consideran sustituidos por README.

Fuentes primarias externas consultadas para delimitar las afirmaciones (no se enviaron datos del proyecto):

- [WCAG 2.1, W3C](https://www.w3.org/TR/WCAG21/).
- [OWASP Top 10:2025](https://top10.owasp.org/2025/).
- [ISO/IEC 25010:2023, ficha oficial](https://www.iso.org/standard/78176.html).
- [ISO 14083:2023, ficha oficial](https://www.iso.org/standard/78864.html).
- [Software Carbon Intensity, Green Software Foundation](https://sci.greensoftware.foundation/).

Se consultaron las fichas públicas ISO, no el texto normativo íntegro; no se presenta una auditoría de certificación.

## Prioridad de continuidad

El siguiente trabajo recomendado es un **sprint de cierre del MVP y garantías de integridad**, manteniendo Sprint 3 abierto. Primero impedir publicación de recálculos inválidos y operaciones sobre rutas históricas; luego unificar versiones/totales/fechas reales, completar flota/pedidos y validar el solver 150×15. Cerrar mapas/PDF y aceptación de cinco RF completos antes de invertir en módulos adicionales.

El detalle de tareas y criterios se encuentra en [BACKLOG_IMPLEMENTACION.md](BACKLOG_IMPLEMENTACION.md).

## Control de integridad de la auditoría

Al comienzo ya había **18 eliminaciones** en Git fuera de AUDITORIA: 15 documentos bajo Auditorias-EcoLogistica y docs/ESTADO_TECNICO_VIGENTE.md, docs/deploy/TLS_VERIFICACION.md y docs/qa/COMANDOS_CALIDAD.md. Se conservaron tal como estaban; esta auditoría no los borró ni restauró.

Se tomó una línea base SHA-256 de **193 archivos no ignorados** y se amplió antes de las comprobaciones a **247 archivos** incluyendo dist, coverage y cachés preexistentes. Se excluyeron .git y árboles de dependencias node_modules/.venv. La comparación final y el estado Git se registran en el resumen ejecutivo. Este control acredita los archivos inventariados; no es vigilancia de todo el sistema de archivos.

Los cinco informes se crean directamente en AUDITORIA, sin subcarpetas ni sobrescrituras de documentos previos. No se guardaron secretos, tokens ni registros de personas. No se realizaron operaciones sobre la base de datos.
