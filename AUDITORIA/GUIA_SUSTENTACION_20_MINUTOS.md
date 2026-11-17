# Guía de sustentación — 20 minutos

Corte 17/11/2026, America/Lima; V_1_0_0. Preparación de fase 5 autorizada por [control de puertas](CONTROL_FASES_3_4_5.md). **Guion preparado, no ensayo ejecutado ni sustentación aprobada.** Cierre técnico/administrativo pendiente. Responsables de exposición y de demo: por confirmar por el equipo.

## 1. Condiciones antes de ensayar

- Seleccionar árbol/commit candidato y resolver o declarar las brechas de [defectos](SPRINT4_DEFECTOS_PENDIENTES.md); no presentar una aceptación inexistente. DEF-02/03/04 impiden un cierre técnico aprobado.
- Preparar un entorno local descartable nuevo, BD exclusiva y datos sintéticos; ningún acceso a producción. La BD temporal de fase 3 ya fue retirada y no es un despliegue disponible para la presentación.
- Habilitar sesiones separadas de admin, operador y conductor; credenciales demo solo en entorno aislado, nunca visibles en diapositivas/DevTools/video. Admin crea flota, operador optimiza; no atribuir esos permisos al gerente/auditor.
- Congelar jornada/dataset y verificar solución factible antes del ensayo; dejar explícito qué se precargó. No usar el benchmark 150 ×15 inválido como demostración de éxito.
- Comprobar OSRM/teselas reales o anunciar alternativa tabular/geodésica; no llamar tráfico real a incidentes manuales. Ensayar con el mismo candidato y datos que se mostrarán.
- Verificar corrida frontend verde, persistencia al recargar, ventana/estado de entrega y conciliación KPI/PDF; conservar los resultados de fase 3 aunque una corrida posterior mejore.
- Los componentes y API se comprobaron por separado; **el recorrido continuo en navegador aún no está observado**. Todo paso UI de §3 es plan condicionado a ese ensayo, no funcionalidad íntegra aceptada.

## 2. Bloque de gestión y cierre — 10 minutos

Los textos son notas de exposición con tiempos máximos propuestos. Ensayar ritmo y transiciones; no alargar el bloque técnico para compensar datos financieros ausentes.

| Tiempo | Mensaje y narración propuesta | Apoyo y fuente real | Quién |
|---|---|---|---|
|0:00–1:00|«EcoLogística aborda la planificación del reparto con capacidad, ventanas de entrega y estimaciones ambientales. Nuestro caso académico se adaptó a Huancayo, El Tambo y Chilca; presentamos lo que existe, sus verificaciones y lo que aún impide cerrar.» Explicar problema/público sin entrevistas no realizadas.|Acta/visión/enfoque; reporte final§1. Adaptación documentada, fuente original de Lima no localizada.|PM/expositor por confirmar.|
|1:00–2:30|«La gestión es híbrida: objetivos, arquitectura, presupuesto e hitos establecen referencia predictiva; historias e incrementos se validan de forma adaptativa. Código escrito, test aprobado y requisito aceptado son estados distintos.» Mostrar mapeo de catálogos y deuda, no porcentaje financiero inventado.|Reporte final§2.1, matriz RF/RNF y planSprint 4.|PM+técnico por confirmar.|
|2:30–4:00|«El acta programa cuatro iteraciones en14 semanas, con hitos 3/7/11/14. Faltan fechas base/reales comparables y aceptación para calcular atraso exacto. La dependencia de PostGIS que bloqueaba B-08 se superó hoy; siguen bloqueantes funcionales y de evidencia.» No señalar ruta crítica no calculada.|Reportes 01/02/06; IMP histórico y resultadoactual 14 B-08.|PM por confirmar.|
|4:00–5:30|«Hay un modelo estimado de USD 134.400, no evidencia de BAC aprobado ni de costos ejecutados. No hemos transformado SP, cobertura o implementación en EV. Sin PV temporal, aceptación valorada y AC sustentado no es responsable publicar SPI/CPI o EAC numéricos.» Mostrar fórmulas y registros que faltan.|Reporte 03, presupuesto 15/09/2026 e inventarioeconómico.|Responsable económico por confirmar.|
|5:30–7:00|«La validación actual aprobó 185 casos backend con PostGIS aislado, incluidas 14 pruebas B-08; frontend 68/69 y4 SW. El caso de flota falló por contrato de argumentos. Cobertura: backend 83,27% líneas, frontend 78,80%; los denominadores y modalidades están publicados.» Aclarar que no es certificación ni E2 E del navegador.|Resultados/JUnit/JSON y reporte 02§calidad.|QA por confirmar.|
|7:00–8:30|«La prioridad es autorización vigente, terminalidad y privacidad WS, además de coherencia de versiones/entregas. Un benchmark rápido no es éxito: nuestras tres muestras asignaron 150 pero fueron infactibles. La respuesta es corregir y validar, no relajar la política de publicación.»|DefectosDEF-02/03/04/06/07/10; reportes 01/04.|Técnico+PM por confirmar.|
|8:30–10:00|«Los siete documentos preservan la plantilla pero siguen como borradores donde faltan datos. No hay satisfacción ni acta de cierre inventadas. El aprendizaje es vincular cada afirmación con evidencia y aceptación. La siguiente demostración se limita al candidato/entorno ensayado; indicaremos los límites y pendientes.» Transición al operador de demo.|Reportes 05/06/07, checklist y matriz aceptación.|PM y operador de demo por confirmar.|

**Total:**10:00. Una vez se consigan datos/aceptación reales, actualizar la narración con nuevas versiones; no leer los textos de ausencia como si fueran cumplimiento sobresaliente. No es necesario crear un PPT para usar estos documentos como apoyo; no se generó deck.

## 3. Bloque técnico — 10 minutos, condicionado a ensayo real

Evidencia ya existente: integración backend/PostGIS y componentes con mocks; **no equivale a completar estos pasos en navegador**. Si la puerta técnica no se satisface, presentar el estado de validación y límite con honestidad, sin llamar «demo funcional completa» a una grabación o mocks. Esta alternativa no acredita por sí misma R4.

| Tiempo / duración | Rol y datos sintéticos propuestos | Pasos / pantalla / API | Resultado esperado y evidencia actual | Alternativa ante fallo |
|---|---|---|---|---|
|0:00–1:00 /1:00|Operador, sesión aislada; usuarios preparados sin mostrar claves |Ingresar, identificar rol y jornada; mostrar llamada `/api/v1/auth` correspondiente sin tokens |Login/roles tienen tests; sesión de navegador propuesta debe comprobar UI y API reales |Si no autentica, detener el recorrido; mostrar fallo y evidencia previa identificada, no fingir login. |
|1:00–2:00 /1:00|Admin para alta; operador para edición; vehículo de demo sin placa real |Abrir Flota, consultar y registrar/editar solo donde rol permita; `/api/v1/vehiculos` |Persistencia de API cubierta; UI contiene DEF-01 en su prueba. Exigir corrección/ensayo antes de prometer flujo |No editar datos operativos; ante fallo guardar incidencia y omitir éxito de alta/edición. |
|2:00–3:30 /1:30|Operador; CSV pequeño sintético y jornada fija |Pedidos: importar o registrar, inspeccionar ventanas/ubicación/errores y recargar; endpoints de jornada/pedidos |Casos CSV/XLSX/ventanas/geografía aprobados; captura de navegador real pendiente; no afirmar prioridad/producto completos |Si dato inválido, mostrar rechazo útil; usar solo fixture factible previamente ensayada y declararla precargada. |
|3:30–5:00 /1:30|Operador; lote pequeño factible conocido |Ejecutar optimización, observar HTTP 201 y metadata/versión; contraste con rechazo 409 de caso imposible separado |B-08 prueba publicación/rollback con BD; no presentar SLA 150 ×15 como logrado |Si responde 409, explicar motivos, no mostrarlo como éxito ni alterar capacidades para ocultar el problema. |
|5:00–6:00 /1:00|Operador; misma versión |Mapa/tabla, filtro de vehículo y detalle/ETA; `GET /api/v1/rutas/mapa` |Coherencia de factibilidad en tests B-08; calles requieren OSRM real. Legado sin evidencia puede indicarfalse |Si mapas externos fallan, tabla probada y aviso de fuente; no dibujar rectas como calles ni afirmar tráfico vivo. |
|6:00–7:30 /1:30|Conductor ligado a vehículo de prueba |Abrir ruta activa, entregar pedido propio, recargar y comprobar estado; endpoint de entrega |API y componentes prueban partes; fecha/comprobante durable y reasignación segura siguen pendientes |No mostrar a cliente real ni exponer WS público; si falla entrega, conservar pendiente y reportar, no simular sincronización. |
|7:30–9:00 /1:30|Gerente u operador; mismo rango/jornada |Abrir dashboard y descargar/abrir PDF con el mismo periodo |Endpoint/unitarias pasan; cifras/fechas/factores/versiones requieren conciliación B-12/13/14/17 |Si no concilia, mostrar diferencia como defecto; no presentar ahorro verificado o ISO certificado. |
|9:00–10:00 /1:00|Operador/conductor; solo si ensayo WS fue aceptado |Recálculo de un vehículo o revisión del rechazo seguro; contrastar commit antes de evento |14 tests B-08 acreditan escenarios backend; no multivehículo por avería, <30 s ni UI viva |Si no está suficientemente validado, usar minuto para explicar rechazo/limitación y pendientes. Sin fingir recálculo ni reemplazarlo por mocks. |

**Total:**10:00. Los cambios de rol deben ensayarse con sesiones separadas para no gastar el tiempo en credenciales. La prueba debe mostrar persistencia al recargar y request/respuesta real; no abrir variables de sesión ni tokens en pantalla. No modificar configuraciones para producir un resultado favorable.

## 4. Checklist del ensayo pendiente

Registrar por paso: árbol/commit, fecha/hora, entorno, rol, dataset/hash, acción, resultado esperado/observado, evidencia/captura, duración y defecto. Un tercero debe poder repetir el recorrido desde instrucciones. No hay duración observada todavía; las tablas son asignación propuesta.

Puerta de grabación: ensayo completo aceptado para el alcance presentado, cero bloqueantes de seguridad/integridad de ese alcance, conexión frontend–backend real observada y cifras conciliadas; autorización/participantes reales para presentación. No se logró esa puerta en estas fases. Guion listo como preparación; **demo viva y MP4 pendientes**.
