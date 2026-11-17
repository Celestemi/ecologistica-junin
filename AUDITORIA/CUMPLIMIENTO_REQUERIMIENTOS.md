# Cumplimiento de requerimientos

Fecha: 16/11/2026, America/Lima. Referencia Git: 967efdfac77d14eb0ffb14210637640c13f9c332.
Auditoría de lectura; los resultados se refieren al código y evidencias locales, sin acceso a la BD activa.

## Referencia de alcance y estados

Se evalúa la consigna adjunta: diez RF y siete RNF. El repositorio contiene otro desglose (18 RF atómicos y cinco RNF); no se reduce el alcance solicitado para ajustarlo al código disponible.

| Consigna auditada | Correspondencia aproximada en documentos/código interno |
|---|---|
| RF-01 Flota | RF-001 registro/mantenimiento; RF-002 placa; RF-003 estado. |
| RF-02 Pedidos | RF-004 importación; RF-005 geocodificación; RF-006 ventanas. La consigna agrega prioridad, producto y volumen integral. |
| RF-03 Optimización | RF-007 GA; RF-008 restricciones; RF-009 secuencia/ETA. |
| RF-04 Mapa | RF-010, RF-011 y RF-012 / US-010…012. |
| RF-05 Dashboard | RF-013 y RF-014 / US-013…014. |
| RF-06 PDF | RF-016; RF-017 CSV es requisito adicional del baseline interno. |
| RF-07 Dinámica | RF-018 y lógica realtime. |
| RF-08 Conductores | Diseño ER de conductor y asignaciones parciales; no corresponde al RF-008 interno. |
| RF-09 Clientes | Diseño ER de cliente/preferencias; no corresponde al RF-009 interno. |
| RF-10 Compensación | RF-015 equivalencia de árboles cubre solo parte; restricciones generales mencionan plan. |
| RNF-01 Rendimiento | RNF-001 y RNF-002 internos. |
| RNF-02 Seguridad | RNF-003 interno. |
| RNF-03 Accesibilidad | RNF-005 interno. |
| RNF-04 Escalabilidad | Sin escenario equivalente completo para 1000 pedidos/50 vehículos. |
| RNF-05 Usabilidad | Vista conductor y supuestos de validación con usuarios; no aceptación completa. |
| RNF-06 Disponibilidad | RNF-004 interno aborda offline, no demuestra 99,5 % de disponibilidad. |
| RNF-07 Documentación | DoD y documentos técnicos; manuales incompletos/ausentes. |

Estados usados:

- **Implementado:** requisito completo con evidencia suficiente de funcionamiento y aceptación.
- **Parcial:** hay código funcional conectado o una parte sustantiva implementada, con elementos exigidos faltantes.
- **Pendiente:** no se identifica implementación de la capacidad solicitada.
- **No verificable:** existen medidas/configuración pero no evidencia para confirmar el resultado exigido.

Los estados integrales no deben confundirse con las puntuaciones de implementación. Un RF puede tener 90 % de código estimado y continuar Parcial. No se atribuye un test aprobado solo porque exista su archivo.

## Regla de puntuación reproducible

Para RF y RNF se descomponen diez comprobaciones por requisito, con igual peso: 10 puntos cada una. **A = 10**, implementación identificable que cubre esa subcapacidad; **P = 5**, parte de ella o limitación relevante; **N = 0**, falta o no hay evidencia para otorgar crédito. A **no significa aceptación integral ni ejecución actual verificada**.

Avance de un requisito = 10 × número A + 5 × número P. Los juicios A/P/N se sustentan en la evidencia de cada fila y del informe maestro. Son una estimación ordinal de implementación, no medición de horas, probabilidad de éxito ni porcentaje de conformidad normativa. Diferencias pequeñas entre puntuaciones no tienen precisión estadística.

Funcionamiento integral verificado = número de requisitos completos con evidencia suficiente / número exigido. Los resultados históricos y pruebas parciales no se convierten automáticamente en aceptación integral.

## Tabla obligatoria de RF

| Código | Requerimiento | Estado | Avance (%) | Sprint | Evidencia | Pendiente |
|---|---|---|---:|---|---|---|
| RF-01 | Gestión de flota | Parcial | 90 | 2 | Vehiculo, VehiculoCreate/Update, desk.create_vehicle/update_vehicle, Fleet.tsx; GET/POST /api/v1/flota y PATCH /flota/{id}; tests/test_fleet_us001.py. | Tipo explícito de vehículo y confirmación integral de los flujos/roles/unidades. |
| RF-02 | Gestión de pedidos | Parcial | 65 | 2 | Pedido; create_order, import_orders, normalize_delivery_window, update_order_location; OrdersDay.tsx; /pedidos, /jornadas/{fecha}/importar. | Prioridad, tipo de producto y volumen consistente en alta/edición/lectura/UI; validación geográfica y aceptación. |
| RF-03 | Generación optimizada | Parcial | 75 | 2 y 4 | solve_vrptw, _evaluate, validate_for_publication; POST /api/v1/optimizar-rutas; tests/test_optimizer_us007.py y test_hard_constraints_us008.py. | Garantizar factibilidad, confianza de matriz, restricciones de conductor, consumo y SLA de lote. |
| RF-04 | Visualización en mapa | Parcial | 80 | 3 | GET /api/v1/rutas/mapa, _feature_collection; MapView, RouteTable, StopDetail; tests de geometría/mapas. | Tráfico real, continuidad de geometría en recálculos y verificación contra backend/OSRM real. |
| RF-05 | Dashboard | Parcial | 55 | 3 | GET /api/v1/indicadores, summarize_indicators; Dashboard.tsx; test_operational_indicators.py. | Ahorro económico, cumplimiento real de entregas, excluir versiones sustituidas y separar unidades de energía. |
| RF-06 | Reportes de sostenibilidad | Parcial | 65 | 3 | sustainability_pdf, load_sustainability_report, build_sustainability_pdf, build_tco; GET /api/v1/reportes/sostenibilidad/pdf; StaffHeader.tsx. | Fechas reales, metodología/factores trazables, conciliación de totales y selección de periodo en UI. |
| RF-07 | Reoptimización dinámica | Parcial | 40 | 4 | /ws/driver/{driver_id}; _on_incident/_on_cancel/_on_add/_reroute; reoptimize_live_route; DriverApp.tsx. | Avería/accidente, redistribución entre vehículos, hora/carga real, publicación válida, persistencia de incidentes y SLA <30 s. |
| RF-08 | Gestión de conductores | Parcial | 25 | Transversal / 2 y 4 | Usuario con rol conductor; AsignacionConductor, assigned_vehicle/conductor_may_drive; vista /conductor. | CRUD de ficha, licencias/vencimientos, disponibilidad, turnos/descansos y administración de asignaciones. |
| RF-09 | Módulo de clientes | Pendiente | 0 | Fuera del núcleo de 4 iteraciones; propuesta posterior al MVP | Pedido.cliente_nombre y seguimiento público son auxiliares; no hay modelo/servicio/API de gestión de clientes. | Entidad cliente, CRUD, contacto/direcciones y preferencias de entrega vinculadas a pedidos. |
| RF-10 | Plan de compensación | Parcial | 25 | 3 y cierre 4; ampliación tras MVP | core.emissions.quinual_equivalent; arboles_quinual_eq en solución/dashboard/PDF. | Plan sobre emisiones residuales, especies/proyectos, cantidad/costo, responsables, calendario y seguimiento verificable. |

Ningún RF integral está acreditado como Implementado. No significa ausencia de módulos funcionales: flota, importación, GA, mapas y PDF sí tienen caminos de código completos para sus subcapacidades básicas.

## Listas de comprobación RF y cálculo

Cada lista tiene exactamente diez elementos; se conserva el orden para reproducir el puntaje.

| RF | Diez comprobaciones de implementación | A / P / N | Resultado |
|---|---|---|---:|
| 01 | Alta A; lectura A; edición A; estados A; placa única A; capacidades kg/m3 A; combustible A; rendimiento A; factor de emisión A; tipo de vehículo N. | 9 / 0 / 1 | 90 |
| 02 | Alta A; listado/jornada A; importación A; dirección A; coordenadas/corrección A; ventanas A; volumen P; prioridad N; tipo producto N; edición integral de atributos N. | 6 / 1 / 3 | 65 |
| 03 | GA conectado A; distancia A; viaje/servicio A; peso A; volumen declarado A; ventanas/penalización A; CO2 A; conductor/jornada P; objetivo de consumo N; factibilidad garantizada con datos viales y restricciones completas N. | 7 / 1 / 2 | 75 |
| 04 | Mapa interactivo A; puntos A; trazado vial opcional A; filtros A; detalle A; ETA A; tabla alternativa A; aviso/reintento de fallo A; capa de tráfico N; coherencia vial entre todas las versiones/recálculos N. | 8 / 0 / 2 | 80 |
| 05 | Distancia calculada A; duración A; CO2 A; referencia secuencial A; filtros/estado sin datos A; consumo P; ahorro económico N; puntualidad real N; agregación sin doble conteo N; actualización por cada versión de solución N. | 5 / 1 / 4 | 55 |
| 06 | PDF binario A; descarga autenticada A; periodo backend A; tabla ambiental A; TCO estimado A; equivalencia A; entregas completadas P; fecha real de entrega N; totales/versiones conciliados N; factores y selección de periodo coherentes y trazables N. | 6 / 1 / 3 | 65 |
| 07 | Canal de eventos A; incidente manual A; cancelación/inserción A; recálculo de secuencia A; redistribución flota N; avería/accidente explícitos N; validación/publicación común N; reloj/carga ejecutada N; incidentes durables N; presupuesto/aceptación <30 s N. | 4 / 0 / 6 | 40 |
| 08 | Rol conductor A; asignación autenticada consultable A; vista de trabajo P; alta ficha N; edición/baja ficha N; licencia N; vigencia licencia N; disponibilidad N; horarios/descansos N; administrador de asignaciones N. | 2 / 1 / 7 | 25 |
| 09 | Entidad N; alta N; consulta/listado del maestro N; edición N; baja N; contacto N; múltiples direcciones N; preferencias N; enlace cliente-pedido N; aceptación del módulo N. | 0 / 0 / 10 | 0 |
| 10 | Emisiones estimadas A; equivalencia matemática A; factor configurable P; cálculo de residual a compensar N; proyecto/especie N; plan de ejecución N; costo N; responsable N; calendario N; evidencia de compensación N. | 2 / 1 / 7 | 25 |

El crédito por volumen en RF-03 solo cubre datos declarados. La revisión de confianza de matriz y el carácter nullable impiden declarar garantía integral. La vista de conductor recibe crédito parcial en RF-08 porque sirve a la operación, pero no reemplaza su gestión administrativa.

## Archivos, clases, métodos y rutas por RF

Todos los endpoints REST siguientes tienen prefijo /api/v1. Son rutas leídas en fuente, no verificadas mediante llamadas durante esta auditoría.

### RF-01

- app/models/domain.py:98 Vehiculo; app/schemas/logistics.py:61 VehiculoCreate y :92 VehiculoUpdate.
- app/api/v1/desk.py:138 list_fleet, :154 create_vehicle, :202 update_vehicle y :255 vehicle_history.
- app/services/vehicle_state.py:45 apply_operational_state; app/services/plate_restriction.py filter_vehicles_for_planning.
- GET/POST /flota; PATCH /flota/{vehiculo_id}; GET /flota/{vehiculo_id}/historial; GET /vehiculos. GET/PATCH /restricciones-placa e historial.
- src/pages/Fleet.tsx, PlateRestrictions.tsx, src/api.ts. Tests de flota, placa y estado.
- Crear corresponde a admin, modificar a admin/operador; no se confunde permiso de UI con autorización backend. Falta tipo_vehiculo que sí figura en ER previsto.

### RF-02

- app/models/domain.py:150 Pedido; logistics.py:488 PedidoCreateRequest, :153 PedidoRead y PedidoWindowUpdate/LocationUpdate.
- routes.py:198 create_order, :274 update_order_window, :322 update_order_location y :175 list_pending_orders.
- desk.py:68 read_day, :103 import_day; order_import.py import_orders/parse_csv/parse_xlsx; geocode.py locate_address/resolve_from_address; order_window.py normalize_delivery_window; operating_area.py point_in_operating_area.
- GET/POST /pedidos; PATCH /pedidos/{pedido_id}; PATCH /pedidos/{pedido_id}/ubicacion; GET /jornadas/{fecha}; POST /jornadas/{fecha}/importar.
- src/pages/OrdersDay.tsx y components/PinMap.tsx, src/types.ts y api.ts. Tests API, importación, geocodificación y ventanas.
- Volumen se persiste al importar, pero no se publica en PedidoRead ni se admite en alta estándar. La clase PedidoCreate con GeoJSON convive con PedidoCreateRequest lat/lon; el POST activo usa esta última.

### RF-03

- genetic_solver.py:446 solve_vrptw y dataclasses RouteSolution/VehicleItinerary/StopItinerary.
- route_constraints.py:110 precheck_fleet_capacity y :151 validate_for_publication; optimizer_runtime.py:22 run_optimizer_in_worker y :40 resolve_ga_parameters; routing_matrix.py prepare_osrm_routing; osrm_client.py OsrmLegCache.
- routes.py:659 optimize_routes y :1008 _persist_solution; POST /optimizar-rutas, parámetro fecha opcional. POST /soluciones/{solution_id}/recalcular-etas recalcula tiempos de una secuencia.
- App.tsx, Sidebar.tsx y src/api.ts optimizeRoutes. La UI principal no pasa fecha; se optimiza la jornada pendiente más antigua, aunque haya pedidos cargados para otro día.
- Tests solver, optimizer, restricciones, SLA y ETA. Ver evaluación detallada del algoritmo en el informe maestro.

### RF-04

- routes.py:530 fleet_map, :897 _fleet_groups; schemas/logistics.py _feature_collection y OptimizedRouteResponse.from_solution.
- GET /rutas/mapa; GET /rutas/activas para detalle; resultado de POST /optimizar-rutas.
- src/components/Map.tsx:78 MapView; :66 lineFeatures limita geometría a road; RouteTable.tsx:11 y :52 StopDetail; lib/routePresentation.ts.
- Trazado OSRM, puntos/colores, selección/filtros, ETA en tabla/detalle, fallback de teselas. Sin OSRM faltan líneas viales y se indica la limitación.
- Tests maps.test.tsx, routePresentation.test.ts, App.test.tsx y test_route_geometry_geojson.py. No hay capa ni API externa de tráfico.

### RF-05

- routes.py:569 operational_indicators; operational_indicators.py:45 summarize_indicators y clase IndicatorSummary; logistics.py OperationalIndicatorsRead.
- GET /indicadores?fecha_inicio=...&fecha_fin=...
- src/components/Dashboard.tsx y api.ts:269 fetchOperationalIndicators.
- Baseline secuencial guardado en metadatos, ahorros relativos, CO2 evitado contra FIFO y consumo derivado del rendimiento. Son cálculos de planes, no telemetría de ejecución.
- test_operational_indicators.py prueba fórmula y ausencia de línea base, sin cubrir deduplicación de recálculos/mezcla de combustibles.

### RF-06

- routes.py:414 sustainability_pdf; pdf_generator.py:100 SustainabilityReport, :128 leg_cost, :142 build_tco, :167 load_sustainability_report, :212 build_sustainability_pdf y :633 _completion_day.
- GET /reportes/sostenibilidad/pdf con fecha_inicio/fecha_fin opcionales.
- src/components/StaffHeader.tsx ofrece Informe PDF; api.ts:325 downloadSustainabilityPdf solicita sin pasar el periodo visible del dashboard.
- tests/test_pdf.py valida cabecera PDF, texto ISO y costos con datos de prueba; no certifica metodología. El PDF declara su límite de verificación externa.
- Falta conciliación de TCO/detalle/cabecera, fecha real, factores versionados y metodología verificable. Exportación CSV RF-017 interna tampoco tiene endpoint identificado; se agrega como pendiente del baseline, sin aumentar denominador de diez RF.

### RF-07

- websockets.py:86 driver_socket, :225 _on_incident, :241 _on_cancel, :253 _on_add, :264 _reroute; realtime_router.py:354 reoptimize_live_route; routes.py:926 retain_other_vehicles.
- /ws/driver/{driver_id}?token=... y /ws/tracking/{order_code}; eventos position, incident, cancel_order y add_order. No existe endpoint REST integral de replanificación de toda la flota.
- DriverApp.tsx publica tráfico/bloqueo/cliente ausente y escucha route_update.
- tests/test_realtime.py cubre ajustes, cancelación/bloqueo/inserción y fanout. No demuestra avería ni redistribución multivehículo ni SLA de 30 s.
- Incidentes manuales en memoria y recálculo de un solo vehículo; no confundido con integración externa de tráfico.

### RF-08

- identity.py:32 Usuario, enums.RolUsuario.CONDUCTOR; operations.py:29 AsignacionConductor; driver_assignment.py:13 assigned_vehicle y :30 conductor_may_drive.
- init_db.py:192 ensure_demo_driver_assignment solo crea asignación demo si procede.
- /auth/yo, /vehiculos y /rutas/activas soportan la operación; no se identifican POST/PATCH /conductores ni API administrativa de asignaciones.
- DriverApp.tsx y pruebas de autorización del conductor. Sin licencia, vigencia, horarios ni ficha.
- No se confunde inactivar un vehículo con disponibilidad de una persona.

### RF-09

- Solo Pedido.cliente_nombre, direccion_referencia y canales de seguimiento; documento ER previsto contiene cliente.
- GET /seguimiento/publico/{token} y src/pages/Tracking.tsx sirven al cliente para seguimiento, no constituyen CRUD de clientes.
- Sin clase Cliente, tabla activa, API /clientes, preferencias ni FK cliente-pedido. Estado Pendiente.

### RF-10

- emissions.py:59 quinual_equivalent; domain.SolucionRuta.arboles_quinual_eq; genetic_solver.py:1295 _to_solution; config.py:80 factor configurable.
- Presentación en /indicadores y /reportes/sostenibilidad/pdf; Dashboard.tsx y pdf_generator.py.
- Equivalencia = CO2 evitado / factor anual. No es una propuesta ejecutable para compensar emisiones residuales ni prueba de árboles plantados.
- Sin clases/rutas de plan, proyectos, costos o seguimiento. El texto PDF fija 12 kg/año aunque la configuración puede cambiar.

## Requerimientos no funcionales

| Código | Requisito | Estado | Avance estimado (%) | Evidencia | Brecha para aceptación |
|---|---|---|---:|---|---|
| RNF-01 | Generación válida 150×15 ≤45 s; reoptimizar <30 s | Parcial | 45 | Presupuesto GA, escalado, un worker, benchmarks y prueba SLA. | Test no exige factibilidad/150 asignaciones; sin HTTP total/OSRM real ni presupuesto específico 30 s. |
| RNF-02 | Seguridad | Parcial | 55 | bcrypt, JWT, roles/objeto parciales, bloqueo, cabeceras, CORS, guardas no demo. | Fugas WS, permisos históricos, TLS efectivo no verificado, revocación/límites y SCA integral actual ausentes. |
| RNF-03 | WCAG 2.1 AA | Parcial | 50 | HTML es, labels, foco, diálogo, tabla y documento de revisión WCAG. | Fallos históricos de contraste/región en operador; sin evaluación manual completa de todos los procesos. |
| RNF-04 | 1000 pedidos/día y 50 vehículos | No verificable | 30 | Monolito modular, BD async, paginación y worker acotado. | Sin carga objetivo, coordinación distribuida/estado compartido, índices medidos ni capacidad dimensionada. |
| RNF-05 | Usabilidad para conductores | Parcial | 60 | Vista simple, acciones grandes, detalle, enlace navegación, avisos, cola offline. | Sin evaluación con usuarios representativos; GPS sustituto y firma/foto no persistida; conflictos de sincronización. |
| RNF-06 | Disponibilidad 99,5 % en horario operativo | No verificable | 15 | Healthchecks y volumen PostgreSQL; soporte offline parcial. | Sin SLI/SLO medido, alertas, redundancia, recuperación, backups probados ni SLA externo. |
| RNF-07 | Documentación | Parcial | 45 | Requisitos, C4/ER, API en código, README y reportes de calidad. | Manual usuario/admin, operación, API exportada, coherencia y aceptación documental final. |

### Cálculo de RNF

| RNF | Diez comprobaciones de implementación/medidas | A / P / N | Resultado |
|---|---|---|---:|
| 01 | Presupuesto A; parámetros escalados A; worker acotado A; dataset 150×15 A; prueba SLA P; validez total N; límite HTTP N; OSRM real medido N; reoptimización <30 N; carga concurrente medida N. | 4 / 1 / 5 | 45 |
| 02 | Hash A; JWT A; RBAC A; bloqueo A; cabeceras/CORS A; autorización de objetos P; TLS efectivo N; minimización WS N; ciclo/revocación sesión N; validación integral SCA/DAST N. | 5 / 1 / 4 | 55 |
| 03 | Semántica/idioma A; etiquetas A; alternativa tabular A; diálogo/foco A; anuncios A; contraste completo N; teclado todos los procesos N; reflow/zoom completo N; lector de pantalla N; acta de criterios AA N. | 5 / 0 / 5 | 50 |
| 04 | Separación modular A; persistencia async A; paginación parcial A; prueba 1000/50 N; concurrencia objetivo N; estado compartido N; dimensionamiento N; índices/EXPLAIN N; contención medida N; recuperación bajo carga N. | 3 / 0 / 7 | 30 |
| 05 | Vista conductor A; controles principales grandes A; próxima parada A; navegación externa A; feedback A; persistencia offline básica A; evaluación con usuarios N; comprobante durable N; errores/conflictos integrales N; GPS fiable N. | 6 / 0 / 4 | 60 |
| 06 | Healthchecks A; volumen persistente P; monitoreo SLI N; alertas N; backups probados N; failover N; reinicio/recuperación documentados N; SLA externo N; staging efectivo N; ventana operativa medida N. | 1 / 1 / 8 | 15 |
| 07 | Requisitos A; C4/ER A; README A; API/docstrings A; reportes técnicos P; manual usuario N; manual admin N; operación/despliegue final N; presentación/aceptación final N; trazabilidad vigente sin contradicciones N. | 4 / 1 / 5 | 45 |

Se otorga crédito por medidas presentes, no por lograr el resultado cuantitativo RNF. Un volumen no sustituye backup; asincronía no acredita escalabilidad; offline no acredita uptime.

## OWASP Top 10:2025

Se utiliza la edición oficial 2025 para evitar mezclar categorías con 2021. La clasificación es una revisión parcial del código, sin pentest ni certificación.

| Categoría | Evidencia favorable | Brecha o hallazgo | Evaluación |
|---|---|---|---|
| A01 Control de acceso | require_roles, assigned_vehicle y guardas de conductor | Asociación histórica permite actuar tras reasignación; WS público recibe payload interno. | Parcial, brechas confirmadas en código. |
| A02 Configuración | Guardas no demo, CORS y cabeceras | Compose demo/HTTP, TLS solo ejemplo; confianza directa en X-Forwarded-Proto con backend publicado. | Parcial; despliegue externo no inspeccionado. |
| A03 Cadena de suministro | Lockfiles, CI pip-audit y manifiestos | Backend Docker no instala desde lock; sin escaneo actual ni npm audit en workflow. | Pendiente validación integral; no se inventan CVE. |
| A04 Criptografía | bcrypt y JWT HS256 con algoritmo restringido | TLS efectivo y cifrado en reposo no acreditados; secretos demo por defecto. | Parcial. |
| A05 Inyección | ORM y parámetros enlazados | Importadores, campos y WS sin fuzzing/DAST integral. | Evidencia parcial favorable; no se confirmó SQL injection. |
| A06 Diseño inseguro | Separación de roles y validación normal | Recálculo sin validador común y transiciones terminales permitidas. | Parcial con defectos concretos. |
| A07 Autenticación | Bloqueo por cuenta y expiración de JWT | WS valida al conectar; token en URL; sin revocación/rate limit general. | Parcial. |
| A08 Integridad software/datos | Lock frontend, checks y migraciones versionadas | Upgrade incompleto, copia de planes inconsistente; sin garantía de artefactos firmados. | Parcial; no se prueba una intrusión. |
| A09 Registro/alertas | Bitacora y logger de seguridad | Sin centralización/alertas/retención verificadas ni sanitización de URL de socket. | Parcial. |
| A10 Excepciones | Handlers públicos y logging interno | Sin pruebas completas de agotamiento/fallo OSRM; matriz desconocida tratada como atraso cero. | Parcial. |

## Estándares y restricciones

| Marco o restricción | Estado auditado | Evidencia comprobable | Pendiente |
|---|---|---|---|
| W3C, HTML/semántica | Parcialmente atendido | index.html lang=es/UTF-8/viewport; controles/landmarks/labels. | Validar HTML renderizado y ARIA en todas las pantallas. “Cumple W3C” sin especificación concreta no es un criterio verificable. |
| WCAG 2.1 AA | Parcialmente atendido, conformidad no acreditada | Tabla alternativa, foco/modal y evaluación histórica de WCAG 2.2. | Criterios A/AA y procesos completos, contraste, zoom, teclado y tecnología asistiva. |
| ISO/IEC 25010 | Aplicación parcial del marco | Escenarios calidad y pruebas; diseño modular. | Plan de evaluación con métricas/evidencias por atributos y resultados de aceptación. |
| OWASP Top 10 | Parcialmente atendido | Controles de acceso/autenticación y reporte histórico. | Resolver H-07/08/09/17/24 y ejecutar evaluación integral actual. |
| Green Software / SCI | Prácticas parciales; medición pendiente | Lazy loading, abort de lecturas, gzip, caché pública y matriz por bloques. | Energía, límites del sistema, unidad funcional e intensidad de carbono del software. No contar emisiones evitadas de flota como SCI digital. |
| ISO 14083 | Alineamiento declarativo parcial; validación pendiente | PDF presenta periodo, distancia y CO2 estimado. | Verificar metodología completa, límites, gases/unidades, origen de factores, datos ejecutados y calidad; ficha pública no sustituye norma íntegra. |
| Ámbito Huancayo/El Tambo/Chilca | Parcial | Validación PostGIS contra area_operacion. | Reemplazar sobre operativo provisional; no hay límites oficiales incluidos. |
| Restricción por placa | Implementación parametrizada parcial | No activa sin validación registrada, admin valida. | Fuente normativa efectiva y configuración operativa. No se afirma obligación legal de pico y placa. |
| Jornada 480 min | Regla operativa parcial | Conducción+servicio, config y validación normal. | Fuente/aceptación de regla; conductores/esperas/descansos y jornada acumulada. |
| TLS / protección de datos | No verificable integralmente | Configuración defensiva y plantilla HTTPS. | Certificados/comunicaciones reales, políticas/retención y cifrado; no se emite dictamen jurídico. |
| ≥15 % km / ≥10 % CO2 | Metas no acreditadas | GA calcula porcentajes reales contra referencia secuencial. | Comparación válida, escenarios representativos y periodo mensual; no imponer pisos inventados. |
| MVP ≥70 % de RF-01…07 | No acreditado | 0 requisitos íntegros aceptados; código parcial en siete. | Completar y verificar al menos cinco. |

No hay estándar integralmente comprobado. Sí hay mecanismos concretos comprobados en fuente y cuatro pruebas de SW aprobadas; ese alcance se informa sin generalizarlo.

Fuentes oficiales para delimitar la evaluación: [WCAG 2.1](https://www.w3.org/TR/WCAG21/), [OWASP 2025](https://top10.owasp.org/2025/), [ISO/IEC 25010](https://www.iso.org/standard/78176.html), [ISO 14083](https://www.iso.org/standard/78864.html) y [SCI](https://sci.greensoftware.foundation/). Las fichas ISO públicas permiten identificar el marco, no certificar conformidad.

## Porcentajes consolidados

| Indicador | Cálculo | Resultado |
|---|---|---:|
| RF-01…10, implementación | (90+65+75+80+55+65+40+25+0+25)/10 | **52,0 %** |
| RNF-01…07, medidas implementadas | (45+55+50+30+60+15+45)/7 | **42,9 %** |
| MVP, implementación parcial estimada | (90+65+75+80+55+65+40)/7 | **67,1 %** |
| MVP, requisitos íntegros verificados | 0/7 ×100 | **0 % acreditado** |
| Umbral mínimo por requisitos completos | techo(0,70×7)=5; 5/7×100 | **71,4 %** |
| Avance general de implementación | 0,70×52 + 0,20×(300/7) + 0,10×85 | **53,5 %** |
| RF integrales verificados entre diez | 0/10 | **0 % acreditado** |
| RNF integrales aceptados entre siete | 0/7 | **0 % acreditado** |

Pesos del avance general: 70 % funcionalidad, 20 % medidas no funcionales y 10 % entregables de análisis/diseño del Sprint 1. Cada RF pesa 7 puntos del total general y cada RNF 20/7; cada actividad Sprint 1 pesa 2. Se eligieron para priorizar producto y calidad conservando crédito para diseño. No son pesos impuestos por la consigna. No se añaden porcentajes de Sprint 2…4 al general porque repetirían las mismas funcionalidades.

El 85 % del Sprint 1 proviene de cinco actividades con peso 20 % y puntuaciones 100, 75, 100, 100 y 50. Véase [ANALISIS_SPRINTS.md](ANALISIS_SPRINTS.md).

No se ofrece un porcentaje agregado de funcionamiento por pantalla: las únicas comprobaciones actuales son tipado y 4 pruebas unitarias del SW; convertirlas a porcentaje del sistema sería engañoso. “0 % acreditado” identifica un resultado de aceptación integral, no que todo el código falle. Las brechas concretas impiden contar como completos los siete RF del MVP incluso si se aceptan los reportes históricos de pruebas.

Ruta sugerida al umbral: cerrar RF-01, RF-02, RF-03, RF-04 y RF-06; luego RF-05 y RF-07. No se habilita una entrega con defectos de seguridad o integridad solo por llegar a cinco RF.

## Evidencia de pruebas y límites

La comprobación actual de tipos pasó; las 4 pruebas scripts/test-service-worker.mjs pasaron. La validación de dist preexistente falló por ausencia del formato BUILD_ASSETS esperado. La suite backend no se ejecutó porque crea/vacía BD; no se instaló Python ni dependencias. Vitest/build/coverage no se ejecutaron para respetar escritura exclusiva en AUDITORIA.

Los artefactos históricos muestran backend 81,07 % líneas / 55,17 % ramas / 76,02 % combinado, frontend 90,91 % líneas / 84,52 % ramas. Son cobertura histórica del 27 de octubre o sin vínculo completo a la revisión actual, no aceptación de los requisitos. La inspección encuentra 139 definiciones Python y 69 invocaciones frontend; la caché enumera 136 casos. Las distintas cifras documentales no se sustituyen por una ejecución inventada.
