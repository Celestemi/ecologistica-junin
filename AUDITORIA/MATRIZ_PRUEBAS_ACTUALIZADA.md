# Matriz de pruebas por requisito

17/11/2026 America/Lima. Base SHA b47d5eb7cda26444c56460ea74591cc5f973e0b3 + árbol sin commit; manifiesto final identifica fuentes exactas. Todas las referencias son ejecución actual, salvo indicación expresa. No son aceptación formal ni porcentaje de RF.

| Requisito | Hallazgos | Casos positivos/negativos y evidencia | Resultado técnico | Aceptación integral |
|---|---|---|---|---|
| RF-01 Flota |AF-13/24 |tests/test_fleet_us001.py,test_vehicle_state_us003.py,test_plate_restriction_us002.py;fleet.test.tsx mantenimiento/edición y cursor20+1/81 |PASÓ backend+4 componentes de flota |PARCIAL: tipo/dominio completo y validación usuario |
| RF-02 Pedidos |AF-01/02/08/13 |test_import_us004.py (CSV/XLSX YA existentes),geocode,order_window,day; nuevos terminalidad/fecha inválida/idempotencia |PASÓ |PARCIAL: prioridad/producto/volumen E2E |
| RF-03 GA |AF-07/09/10 |solver/optimizer/hard_constraints;28 unidades+14 BD B-08;testigo150×15,factibilidad y persistencia |PASÓ escenario documentado |PARCIAL: representatividad/proveedor/referencia por vehículo |
| RF-04 Mapa |AF-03/07/15 |GeoJSON4,OSRM3 con dobles,mapas4 componentes; TCP E2E mapa con ID de plan; salas públicas aisladas |PASÓ código/GeoJSON |NO VERIFICABLE renderización actual y OSRM/tiles reales |
| RF-05 Dashboard |AF-07/09 |latest snapshot,oráculo eléctrico,TCO,invalidación por id y descargas con periodo; API TCP real |PASÓ |PARCIAL: ahorro/puntualidad/factores y aceptación |
| RF-06 Reportes |AF-08/09/15 |PDF unidades/endpoint;CSV restringido,fecha real+versión de evento,periodo posterior al plan;TCP descargas sintéticas |PASÓ |PARCIAL: factores reales,legado y aceptación visual/metodológica |
| RF-07 Dinámica |AF-01/02/06/07/10/11 |seguridad A→B y carrera,terminalidad,commit/rollback B-08,reloj GPS,snapshot vacío,pipeline<30 s |PASÓ escenarios |PARCIAL: avería multivehículo,carga/jornada acumulada,durabilidad/latencia campo |
| RF-08 Conductores |AF-01/06/14 |rol/asignación vigente y revocación/expiración;vista conductor6 componentes;TCP entrega real |PASÓ partes |BLOQUEADO contrato licencias/turnos/administración completa |
| RF-09 Clientes |AF-14 |nombre en pedido/seguimiento no equivale a maestro;sin suite CRUD/preferencias |NO EJECUTADA integral |BLOQUEADO contrato/fuente aprobada |
| RF-10 Compensación |AF-14 |equivalencia numérica y textos que no afirman plantación |PASÓ equivalencia |BLOQUEADO plan/proyecto/costo/responsable/evidencia reales |
| RNF-01 Rendimiento |AF-10 |API ASGI150×15=1,7821 s,150 únicos factibles;pipeline dinámico .2373 s |PASÓ escenario sintético favorable |PARCIAL: red/OSRM y escenarios representativos |
| RNF-02 Seguridad |AF-01/02/03/06/29 |13 regresiones nuevas + suite previa;REST/WS reales;scan560 blobs;SCA npm0 y OSV0 tras parche |PASÓ alcance descrito |PARCIAL: TLS/proxy/configuración/secretos externos,prueba por pares |
| RNF-03 Accesibilidad |AF-25 |componentes teclado/foco;sin host navegador/pipe tras2 intentos |PARCIAL / NO EJECUTADA visual |NO VERIFICABLE WCAG integral/lector/zoom |
| RNF-04 Escalabilidad |AF-23 |1000 registros/50 activos,80 lecturas a concurrencia8,p95 .2622 s |PASÓ smoke limitado |NO VERIFICABLE capacidad de toda mezcla de negocio |
| RNF-05 Usabilidad |AF-25 |70 componentes/unidades;sin usuarios reales |PASÓ pruebas automatizadas |NO VERIFICABLE tareas con usuarios objetivo |
| RNF-06 Disponibilidad |AF-11/23 |SW4/4,offline5 componentes,backup/restore nuevo y conteos iguales |PASÓ partes |NO VERIFICABLE99,5 % en ventana ni recuperación multiworker/GPS |
| RNF-07 Documentación/DoD |AF-22/26/28/31/32/33 |build,TS,gates80,AST,guía/manual por versión y14 enlaces (fase4 valida de nuevo) |PASÓ checks técnicos señalados |PARCIAL: fuentes históricas,tercero,CI remoto/staging y aceptación |

## Evidencia común y conteos

- Backend: CORRECCIONES_EVIDENCIAS/fase3-parche-backend/backend-junit.xml;209 aprobadas/0 fallidas/0 omitidas.
- Frontend: fase3-final-frontend/frontend-results.json;70 aprobadas/0 fallidas/0 omitidas,15 archivos. Componentes con mocks.
- SW:4 aprobadas. Total283 casos únicos, no suma de todos los intentos.
- Cobertura backend:84,2884 % líneas,63,6731 % ramas,80,1147 % combinado; frontend80,47 % líneas,71,55 % ramas.
- E2E: fase3-e2e/result.json,10 pasos TCP HTTP/WS y BD real,frontend HTTP/proxy, **sin navegador**.
- Carga: fase3-load/result.json;OSV/python-osv.json;npm-audit.json;secret-scan.json.
- Comparación histórica:185 backend y68/69 frontend anteriores se conservan en informes originales, no se suman al corte actual.

Los casos críticos incluyen rechazo por asignación histórica, terminales, payload anidado en ETA pública, exceso de mensajes, expiración inactiva, revocación, cambio de rol, fecha sin zona/futura con rollback,concurrencia de reasignación y snapshot que no resucita rutas. Las fixtures escriben solo en PostGIS nuevo verificado; lo marcado NO EJECUTADA/NO VERIFICABLE no recibe aprobación.

## Adenda de fase5 — 17/11/2026

El corte final agrega regresión de texto literal PDF (RF-06/AF-15),roja antes del escape y verde después. **210 backend,70frontend y4SW pasan;284 casos únicos**. Backend84,3737%líneas/63,8350%ramas/80,2162%combinado;frontend80,47%líneas. E2E TCP repetido con último código:10pasos/0,938784s. JUnit en fase5-final-backend,frontend en fase5-frontend y E2E en fase5-e2e. Los209 y métricas anteriores corresponden al corte fase3 conservado arriba. Estados integrales RF/RNF de esta matriz se mantienen parciales/bloqueados/no verificables según condición;sin nueva aceptación. [Reauditoría final](REAUDITORIA_POST_CORRECCIONES.md).
