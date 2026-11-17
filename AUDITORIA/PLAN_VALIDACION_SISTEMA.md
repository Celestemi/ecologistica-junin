# Plan de validación del sistema y de la entrega final

**Corte de planificación:** 17/11/2026, America/Lima. **Versión:** 1.0.0. **Estado:** protocolo propuesto, pendiente de ejecución en una fase de implementación autorizada.

Repositorio: `C:/Users/Baguette/Documents/Proyectos/ecologistica-junin`, confirmado por el usuario; referencia `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1`. Relacionado con [PLAN_SPRINT_4.md](PLAN_SPRINT_4.md), [MATRIZ_CONSIGNA_FINAL.md](MATRIZ_CONSIGNA_FINAL.md) y [EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md](EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md).

**Los escenarios y datasets descritos a continuación son propuestas de validación futura, no pruebas ejecutadas ni resultados históricos.** Hoy no se inicia aplicación, Docker, API, BD, build ni suites con escritura. Crear este plan no acepta requisitos ni autoriza migraciones o alteración de datos.

## 1. Puertas de entrada y entorno seguro de pruebas

Antes de ejecutar V-02…24 en otra fase:

- Acordar requisito/criterio, alcance/capacidad del sprint, responsable y aceptante. Mantener el mapeo RF-01…10 auditados ↔ RF-001…018 internos; no asumir equivalencia numérica.
- Identificar commit candidato, configuración no secreta, versiones reales de Python/Node/BD/OSRM/navegador y SO/hardware. Respetar lockfiles y reproducibilidad; la instalación no pertenece a esta fase.
- Preparar PostGIS **exclusivo de pruebas**, con nombre/host/puerto claramente separados y verificación de conexión; respaldo restaurable y fixtures sintéticas sin datos personales. `tests/conftest.py` crea BD y ejecuta TRUNCATE: nunca apuntar esa suite a datos operativos.
- Revisar inicialización/migraciones antes del arranque. `backend/entrypoint.sh` llama a `app.db.init_db`: arrancar contenedor no es de solo lectura. Upgrade se prueba en copia descartable antes de desplegar.
- Definir dataset, versión/hash, rutas de control, semillas, proveedor/estado de OSRM y tráfico, fecha/huso de la jornada y fuentes de factores. Para medir conectividad real no sustituir API por fixtures ni respuestas de red mockeadas.
- Seleccionar la evidencia pertinente al cambio: unitarias para regla, integración para transacción/BD, E2E para UI↔API y aceptación real para RF. Añadir prueba de regresión que reproduzca cada defecto P0/P1; no duplicar pruebas que solo repiten implementación.
- Definir rutas de artefactos en la futura etapa autorizada, con capturas/logs sin tokens ni información sensible. No generar esos archivos fuera de AUDITORIA en esta fase.

No toda prueba requiere todas las dependencias del backlog; validar componentes temprano y repetir solo lo afectado por cambios o defectos abiertos. Una corrida verde antigua o el badge del README no sustituye la del candidato.

## 2. Datasets propuestos

| Dataset | Propósito / preparación futura | Control de referencia |
|---|---|---|
| DS-01 · flujo pequeño | Jornada fija en zona aceptada, depósito, dos vehículos aptos y pedidos sintéticos con ventanas amplias y capacidades conocidas | Asignación y secuencia factibles calculables manualmente; actores operador, conductor A/B, consulta/auditor y anónimo según RBAC acordado. |
| DS-02 · límites/errores | Casos peso/volumen exactos y por encima, ventanas imposibles, jornada excedida, punto inválido y celda de matriz desconocida | Resultado esperado por regla y motivo de rechazo; no exigir factibilidad de una instancia imposible. |
| DS-03 · versiones/carreras | Plan inicial y dos recálculos, dos operadores concurrentes, cambio de conductor/vehículo, pedidos entregados y cancelados | Libro manual de pedidos/asignaciones vigentes y suma de actividad única; registrar estado antes/después y versión. |
| DS-04 · entrega/offline | Operaciones con IDs distintos y repetidos, fecha real cliente/servidor, firma/foto sintéticas, reconexión y dos pestañas | Lista íntegra de operaciones y comprobantes esperados; un evento por operación aceptada y conflictos explícitos. |
| DS-05 · SLA factible 150×15 | Conjunto de 150 pedidos/15 vehículos con construcción factible conocida, no solo etiqueta «feasible»; fuentes geográficas y matriz verificadas | Solución testigo que respeta capacidad, ventanas, jornada, regreso y elegibilidad; variantes por semillas/datasets identificadas. |
| DS-06 · dinámica | Ruta en ejecución con entregados, pendientes, GPS/hora/carga reales de prueba, avería/bloqueo/cancelación/inserción, flota remanente apta | Subcaso factible e imposible por capacidad; entregados congelados, pendientes y asignación actual identificados. |
| DS-07 · ambientales/reportes | Rutas/versiones conocidas, combustión y eléctrico, factores/unidades documentados, filtros de fechas/vehículos y rango sin datos | Cálculo independiente de km, tiempo, combustible/kWh, CO₂, ahorro/costo y puntualidad con fechas reales. No usar el propio servicio para calcular el oráculo. |
| DS-08 · capacidad/operación | 1000 pedidos diarios/50 vehículos con perfiles de concurrencia, distribución temporal y hardware acordados | Ventana operativa, umbrales de errores/latencias y SLI definidos antes de medir; no sustituye DS-05 ni inventa 99,5 % de disponibilidad. |

Los tamaños salvo los requisitos 150×15/1000×50 son propuestas, no registros del proyecto. Acordar valores y documentar por qué el dataset representa el caso de uso; conservar casos inviables para rechazo explícito.

## 3. Catálogo de validación técnica

### V-01 — Trazabilidad, arquitectura y repositorio

**Relaciona:** B-01/31, G-01; RF/RNF transversales. **Nivel:** inspección + reproducción por tercero.

Revisar catálogo de requisitos, roles, arquitectura efectiva y README; distinguir frontend `src/`, API `app/` y carpetas de despliegue. Conciliar GA/Geometry activos frente a OR-Tools/GEOGRAPHY/Redis/Celery previstos. Validar que el paquete entregado no incluya dependencias, env privados, claves, dumps ni temporales y que el ignore cubra la política acordada; revisar `.env.example` sin valores productivos. Verificar que fuentes requeridas están disponibles y los enlaces resuelven.

**Aceptación:** matriz requisito→criterio→módulo→prueba→resultado→evidencia→aceptante completa para alcance comprometido, sin equivalencias de IDs ambiguas; instrucciones permiten reproducir arranque sin conocimiento tácito. **Evidencia:** inventario de archivos/ignore, revisión de enlaces, versión de arquitectura y ejecución por tercero identificada. No declarar ausencia histórica de secretos por un escaneo de formatos limitado.

### V-02 — Autenticación, roles y ciclo de sesión

**Relaciona:** B-09/11/26; RNF-02 (RNF-003 interno). **Dataset:** DS-01/03. **Nivel:** API/WS + E2E.

Probar por endpoint y objeto: anónimo, token inválido/vencido, usuario inactivo, rol autorizado/no autorizado, conductor A/B, consulta/auditor según matriz aprobada. Probar bloqueo por intentos, expiración y mecanismo de revocación acordado, cambio de rol/asignación después de autenticar y sesión en frontend. Comprobar contraseñas almacenadas como hash y logs/proxy sin token/clave.

**Aceptación:** cada acción permite o rechaza según contrato; REST usa 401/403 cuando corresponda; WS rechaza/cierra con política documentada; vencimiento/revocación aplica a conexiones existentes. No basta ocultar botones. TLS/WSS se verifica en V-17. **Evidencia:** matriz de solicitudes/redactadas y respuestas, actor/objeto/instante y estado persistido sin credenciales.

### V-03 — Privacidad, aislamiento y limpieza WebSocket

**Relaciona:** B-10/11, RF-04/07/09, RNF-02. **Dataset:** DS-01/03. **Nivel:** contrato/integración real.

Abrir seguimiento por token opaco del pedido A y canal autenticado del conductor; emitir posición, ETA, recálculo, cancelación y estado. Inspeccionar snapshot inicial **y todos los mensajes posteriores**. Intentar pedido B/identificador interno; desconectar/reconectar con token opaco y verificar número/clave de suscripciones; expirar autorización durante conexión y probar límites de mensajes/conexiones.

**Aceptación:** seguimiento público solo ve campos públicos acordados del pedido A, sin secuencias ajenas, identificadores internos ni GPS exacto si el contrato público lo excluye; datos privados permanecen en canal interno. Desconexión retira inmediatamente la misma clave registrada y los límites no rompen uso normal. **Evidencia:** esquemas y payloads redactados por evento, contadores de conexión antes/después y prueba de rechazo.

### V-04 — Asignación vigente, transiciones y concurrencia

**Relaciona:** B-09/13; RF-02/07. **Dataset:** DS-03. **Nivel:** transaccional con BD.

Reasignar pedido de vehículo A a B dejando historia; intentar confirmar/cancelar/insertar desde A por REST y WS. Cancelar un entregado y entregar un cancelado. Lanzar dos planificaciones sobre el mismo pedido y repetir operaciones concurrentes.

**Aceptación:** solo asignación **vigente** autoriza; estado terminal no retrocede; no existen dos asignaciones vigentes por pedido; rechazo no cambia estado ni deja reserva parcial. El estado repetido/idempotencia sigue la política acordada. **Evidencia:** consultas de comprobación antes/después, versiones/actores, resultados concurrentes y transiciones permitidas/prohibidas.

### V-05 — Flota, pedidos y contratos integrales

**Relaciona:** B-02/04/05/23, mínimos E-01/02; RF-01/02. **Dataset:** DS-01/02.

Crear/leer/editar/inactivar flota con tipo, capacidades, energía y estado; probar duplicados, valores inválidos, mantenimiento/inactividad, placa condicionada a regla validada y permisos. Crear pedido equivalente manual/CSV/XLSX con prioridad/producto/peso/volumen/ubicación/ventanas; consultar/editar/importar errores y comprobar contrato UI↔API↔BD. Cambiar de jornada y optimizar la elegida. Probar geografía/hitos/pin/punto fuera de área y política de volumen desconocido.

**Aceptación:** campos no se pierden ni se inventan; cada error identifica campo/fila/motivo; alta/importación son equivalentes; inactivo/inapto no entra en ruta; jornada B no usa A. Normativa pendiente no se anuncia como validada. Si se acepta E-01/02, incluir CRUD/turnos/licencias/clientes/preferencias completos; la asignación mínima no los sustituye. **Evidencia:** archivos de entrada sintéticos, respuestas, capturas y registros persistidos.

### V-06 — Esquema, upgrade y recuperación

**Relaciona:** B-06 y cambios de modelo B-04/05/13/14/25. **Nivel:** BD aislada, ejecución futura con escritura explícitamente fuera de esta fase.

Preparar copia del esquema previo con datos sintéticos e instalación vacía; aplicar migraciones en entorno descartable, comparar columnas/índices/constraints incluidas geometría, versiones y entregas; ejecutar segunda aplicación. Verificar bootstrap/semillas separados del arranque productivo y probar restauración del respaldo. Definir recuperación por restore o rollback compatible, sin prometer downgrade seguro automático.

**Aceptación:** upgrade y nueva instalación equivalentes; datos conservados y constraints operativos; aplicación repetida idempotente; recuperación restaura los datos esperados. **Evidencia:** versiones antes/después, diff de esquema, conteos/invariantes y ensayo de restore. No tocar BD operativa.

### V-07 — Factibilidad y publicación atómica

**Relaciona:** B-07/08/23; RF-03/07, RNF-01. **Dataset:** DS-01/02/05. **Nivel:** unidad + API + WS con persistencia.

Forzar exceso de peso/volumen, ventana/jornada incumplida, pedido sin asignar, matriz desconocida, flota no elegible y solución válida; ejercer **planificación normal y dinámica**. Comprobar mejor factible frente a candidato de fitness penalizado inválido y timeout. Inspeccionar plan/estado de pedidos/notificaciones tras fallo y metadata del mapa.

**Aceptación:** ninguna solución inválida se publica, persiste como éxito o cambia pedidos parcialmente; devuelve causas estructuradas, UI las presenta; mapa muestra factibilidad real. Matriz desconocida no implica ventana validada. Caso factible conocido resuelto sin pérdidas, mejor factible preservada; timeout sin solución válida informa error/excepción operativa, no éxito falso. **Evidencia:** oráculo de restricciones, respuesta/WS, transacción/BD antes/después y salida del solver.

### V-08 — Versiones, sumas y actividad única

**Relaciona:** B-13, RF-03…07. **Dataset:** DS-03/07.

Crear plan inicial, entregar parcialmente y efectuar dos recálculos, uno de un solo vehículo con otros retenidos. Comparar detalles/cabecera, flota vigente, geometría/ETAs/estados, indicadores y reportes. Recalcular ETAs sin cambiar actividad ejecutada y consultar distintos periodos.

**Aceptación:** versiones archivadas conservan historia pero no duplican actividad vigente/ejecutada; cada total se deriva del mismo snapshot y unidades; flota retenida preserva datos; plan+dos recálculos no triplica km/CO₂/pedidos. Planificado y ejecutado tienen definiciones distintas y explícitas. **Evidencia:** libro independiente de actividad, consultas/API por versión y conciliación con UI/PDF.

### V-09 — Entrega real, comprobante e idempotencia offline

**Relaciona:** B-09/14/19, RF-02/05/06 y RNF-05/06. **Dataset:** DS-04.

Confirmar entrega online/offline con fecha real, operación y comprobante. Recargar navegador sin red, reconectar, perder respuesta y reintentar misma operación; encolar mientras sincroniza y usar dos pestañas. Probar token vencido, rechazo backend, reasignación durante offline, error de carga del comprobante y salida de sesión con pendientes. Distinguir hora cliente y de recepción servidor con desfase explícito.

**Aceptación:** 100 % de operaciones esperadas del escenario se conserva, sin duplicados ni pérdidas; evento real y comprobante persisten y son consultables según rol; conflictos/rechazos recuperables visibles; no anunciar sincronización exitosa si falló el comprobante; ETA nunca sustituye fecha real. **Evidencia:** lista de IDs y marcas temporales, IndexedDB antes/después, eventos backend y comprobantes sintéticos, capturas y red sin datos privados.

### V-10 — Indicadores ambientales, monetarios y puntualidad

**Relaciona:** B-02/12/13/14/15/17, E-03. **Dataset:** DS-07.

Calcular por separado unidades y resultados esperados desde datos/factores versionados; comparar core/solver/persistencia/KPI/PDF. Probar motor de combustión y eléctrico, pérdidas/ahorros negativos, baseline no disponible, cero actividad y filtro Lima entre días. Cambiar factor actual y comprobar historia. Optimizar dos veces en misma fecha y observar invalidación/actualización UI.

**Aceptación:** fórmula y fuente únicas para cada magnitud, tolerancia numérica acordada según unidad y redondeo; sin galones para eléctricos ni doble actividad; costo/ahorro/puntualidad se basan en datos aplicables y fechas reales. Factor impreso coincide con usado y no reescribe historia. Equivalencia de árboles se identifica como estimación, no plantación/compensación ejecutada. **Evidencia:** hoja de cálculo independiente o cálculo verificable, fuentes/unidades/versión y conciliación. Acordar tolerancias antes de probar, no ajustarlas para ocultar diferencias.

### V-11 — Rendimiento y calidad del GA extremo a extremo

**Relaciona:** B-07/21/28; RF-03, RNF-01. **Dataset:** DS-05 y variantes DS-02.

Verificar primero solución testigo del dataset; medir solicitud HTTP→respuesta y disponibilidad del plan persistido, incluyendo matriz, geometría, búsqueda y BD. Separar tiempo solver de tiempo total, caché fría/caliente y red OSRM. Usar varias semillas; se propone inicialmente cinco repeticiones por escenario, ampliables según variabilidad, **sin tratarlas como garantía estadística universal**. Publicar fallos, no solo éxitos; el caso imposible se mide como rechazo controlado.

**Aceptación para declarar SLA 150×15:** en cada ejecución declarada satisfactoria 150/150 asignados, cero violaciones, resultado válido completo y tiempo HTTP ≤45,0 s. No basta `_assigned_count > 0` ni «cumple_sla=true» con factible=false. Comparar calidad contra baseline definida y factible usando los mismos pedidos/factores; mejora de fitness no compensa infactibilidad. Definir política para timeout, mejor factible y respuesta 503 ante saturación; incluir concurrencia representativa sin bloquear event loop.

**Evidencia:** hardware/SO/versiones/commit, dataset/hash/semillas, configuración/OSRM, inicio/fin, latencias por fase, resultados de restricciones/calidad y errores. Informar cada ejecución y resumen apropiado (p50/p95/máximo cuando la muestra lo permita); no extrapolar percentiles de cinco repeticiones como capacidad garantizada. Comparación GA antes/después con mismo entorno. C-10 es antecedente histórico insuficiente para aprobar esta prueba.

### V-12 — Mapa, tabla y servicios de ruteo

**Relaciona:** B-06/13/16/23, RF-04. **Dataset:** DS-01/03.

Generar ruta con OSRM real configurado, abrir mapa, filtrar vehículo, seleccionar paradas/detalle y contrastar tabla/API. Recálculo de un vehículo debe mantener los otros. Simular fallo de teselas, OSRM no disponible y geometría ausente; probar recuperación y ausencia de GPS.

**Aceptación:** mismas secuencias/cargas/ventanas/ETA/versiones; geometría vial completa cuando se declara disponible; alternativa tabular utilizable y aviso de fuente/estimación cuando falte; una recta no se presenta como carretera. Falta de GPS no publica siguiente parada como posición actual. **Evidencia:** GeoJSON, respuesta API, origen OSRM y capturas mapa/tabla de la misma versión, incluyendo fallo controlado.

### V-13 — Reportes y exportaciones

**Relaciona:** B-17/33/34, RF-06/RF-017 interno. **Dataset:** DS-07.

Descargar PDF desde UI para rango/vehículo conocido, comparar filtros enviados, registro/versiones, KPI, factores y fechas reales. Probar rango vacío, rol indebido y, si se mantiene en baseline, hoja de ruta sin conductor y CSV filtrado. Inspeccionar PDF renderizado, legibilidad, unidades, encabezados y números; abrir archivo completo. Si se comprime, comparar tamaño y contenido antes/después con mismos datos.

**Aceptación:** conciliación numérica con referencia, filtros correctos, versiones sustituidas excluidas, fecha real de entrega y factor correctos; rango vacío no inventa actividad ni conformidad ISO. CSV, si exigido, coincide con fuente/filtros y respeta autorización. Mejoras de tamaño no pierden contenido. **Evidencia:** archivo exportado, dataset/filtros/commit, comparación y revisión visual; no pruebas frágiles buscando texto sin comprimir dentro de bytes PDF.

### V-14 — Build, PWA y actualización de caché

**Relaciona:** B-19/20, RNF-05/06. **Nivel:** artefacto + navegador real en futura etapa.

Construir candidato solo en fase autorizada, identificar hash de artefactos/commit; revisar manifiesto, SW versionado, precaché y ausencia de datos autenticados en caché pública. Instalar versión previa, actualizar a candidata, probar navegación offline y cola tras upgrade. Validar con scripts existentes y navegador real.

**Aceptación:** build trazable y auditoría de artefactos verde; upgrade no mezcla recursos incompatibles ni pierde operaciones; login/conductor offline según alcance y errores claros. El C-05 actual ya pasó sobre dist existente, por lo que no se presupone su fallo ni su correspondencia con el candidato. **Evidencia:** hashes, reporte build/SW y ensayo de dos versiones en navegador.

### V-15 — Reoptimización, reloj operativo y tráfico

**Relaciona:** B-18/24/25 y B-07/08/09/13/21. **Dataset:** DS-06.

Registrar GPS/hora/carga y entregas realizadas; avería retira unidad, bloqueo/cancelación/inserción cambia pendientes. Probar redistribución multivehículo apto y caso sin capacidad, prioridad por ventana que vence si está en baseline, destino real, jornada acumulada y estado actual. Medir evento aceptado→nueva ruta validada/persistida/notificada/renderizada; comprobar que no se modifica lo entregado. Reiniciar y usar dos workers si se acepta durabilidad.

**Aceptación:** entregados intactos, pendientes asignados una sola vez, vehículo averiado no se reutiliza, carga/jornada remanentes respetadas, ETA no anterior a hora actual; infactibilidad explícita sin publicación parcial falsa. Objetivo operativo del pedido **<30 s**; baseline interno EN-002 expresa ≤30 s, diferencia a conciliar con B-01 (adoptar el más estricto para el ensayo propuesto). Si sigue vigente EN-002 de recepción de tarea <1 s, verificarlo por separado o registrar cambio arquitectónico aprobado.

Para tráfico real: evidencia de proveedor/fecha/cobertura/frescura y efecto sobre tiempos, con fallback declarado. Evento manual/multiplicador fijo no acredita API de tráfico. Incidente resuelto deja de penalizar y conserva historia. **Evidencia:** trazas temporales, asignaciones/versiones antes/después, payloads privados/públicos, eventos y resultados por escenario/semilla; no afirmar multivehículo por recalcular solo una unidad.

### V-16 — Accesibilidad y uso por perfiles objetivo

**Relaciona:** B-03/22, RNF-03/05. **Dataset:** flujos DS-01/04.

Recorrer login, flota, pedidos, optimización, mapa/tabla, entrega/comprobante, seguimiento y PDF por teclado; foco de diálogos y retorno, nombres, errores/estado anunciados, lector de pantalla, contraste por contexto, zoom 200/400 % y reflow 320 CSS px. Verificar controles principales conductor ≥48×48 según requisito interno. Evaluar foto como alternativa a canvas si permite completar flujo y guardar comprobante.

**Aceptación:** criterios A/AA aplicables del baseline acordado con evidencia por flujo; corregir hallazgos de operador y no asumir accesibilidad integral por axe/Lighthouse. Conciliar WCAG 2.1 de baseline con evaluación histórica 2.2 sin reducir exigencias sin decisión. Usabilidad con participantes reales del perfil objetivo, protocolo y resultados; no inventar entrevistas. **Evidencia:** criterio, estado/pantalla, prueba automática/manual, dispositivo/tecnología asistiva y defecto/resultado.

### V-17 — Seguridad del despliegue y recuperación operativa

**Relaciona:** B-25/26/27; RNF-02/04/06.

En staging futuro validar HTTPS/WSS/certificado y proxy de confianza, puertos internos de BD/API y rechazo de bypass, configuración sin demo ni secretos en código/logs, CORS/cabeceras según política. Ensayar fallos de BD/OSRM/proceso, reinicio y restore desde backup; comprobar estado confirmado/incidentología compartida entre workers cuando aplique.

**Aceptación:** controles configurados y observados en entorno declarado, restauración recupera datos esperados y fallos son recuperables sin éxito falso; requisitos TLS exactos se cotejan con EN-003. No llamar producción a Compose demo HTTP ni exigir fingir ese entorno en un video local permitido. La DoD de staging sigue pendiente hasta despliegue automatizado real. **Evidencia:** configuración redactada, verificación de protocolo/puertos, registro de restore y comparación de datos.

### V-18 — Calidad y CI del candidato

**Relaciona:** B-29 y DoD histórica.

Ejecutar suites pertinentes en entorno reproducible y luego conjunto integrado del candidato; revisar conteos considerando parametrización/alcance. Generar cobertura por capa con métrica acordada (líneas/ramas/mixta), denominadores y commit; configurar fallo si umbral incumplido. Ejecutar análisis estático y dependencias runtime/dev, revisar falsos positivos/contexto y deuda bloqueante. Comprobar PR con revisión por un par y staging automatizado real, API actualizada.

**Aceptación:** evidencia vigente de todos los puntos de DoD o excepción explícita aprobada. Umbral histórico ≥80 % backend/frontend no queda acreditado por C-09 ni por gate de código nuevo Sonar. No cambiar denominador para alcanzar umbral ni equiparar SCA con Sonar sin SCA. **Evidencia:** logs/resultados/cobertura/gate revisado, PR/CI/staging vinculados a commit y fecha; sin secretos. No inventar enlaces a ejecuciones remotas.

### V-19 — Aceptación integral del MVP

**Relaciona:** B-30, RF-01…07 y RNF aplicables. **Nivel:** aceptación real, sin sustituir backend por mocks.

Por RF, cubrir todos los escenarios/condiciones acordados y flujos de fallo; ejecutar UI→API→BD→UI con roles reales de prueba. Cambiar dato desde UI, observar request/response redactado y persistencia al recargar. Repetir flujo después de recálculo/reasignación y fallo de red donde aplique. Verificar operaciones además de pantallas. Mostrar fallos controlados con mensajes útiles.

**Aceptación:** cada RF marcado completo tiene todos sus criterios cumplidos, sin bloqueantes de seguridad/integridad ni excepciones ocultas. Si se reclama ≥70 % del MVP: al menos cinco RF completos de siete, no promedio de avances parciales. Si RF-05/07 se presentan parciales, registrar explícitamente sus límites; su exclusión no elimina baseline original. Acta de aceptante real, fecha/entorno/commit, casos, resultados y defectos residuales. **Evidencia:** protocolo firmado/validado, capturas o grabación, API y registros sintéticos, referencia a requisitos.

## 4. Validación de gestión, entrega y comunicación

### V-20 — Documentos, EVM, visuales y enlaces finales

**Relaciona:** G-01…06/B-31; rúbrica R1/R2/R3. Ejecución posterior a datos suficientes.

Revisar cada campo de las plantillas 5.1–5.7 contra la matriz compañera. Para EVM, verificar autorización de BAC/moneda/reservas, PV por baseline temporal, EV por aceptación presupuestada, AC por soportes y periodos anterior/actual. Conciliar suma de paquetes, registros de horas/devengos, acumulados e incrementos. Recalcular independientemente SV/CV/SPI/CPI, tres EAC y porcentajes; no sumar índices ni dividir por cero. Revisar hipótesis del EAC elegido, signos/unidades, causa→impacto→acción y fecha de corte.

Verificar gráficos con sus datos originales: RAG con umbrales, líneas EVM, CFD, burbujas SPI/CPI/CSI definido y barras/gauges; burndown, burnup, Kanban, Mood y retro con capturas reales. No fabricar historia faltante. Validar satisfacción/aceptación/reunión de cierre y ocho categorías de lecciones. Nombres exactos y versiones, siete archivos en `docs/04 Cierre`, README→cada uno y cada uno→`../../README.md`, imágenes accesibles, sin marcadores.

**Aceptación:** estructura/datos/cálculos/evidencias completos y trazables, aprobación de cambios y cierre reales. Si faltan datos irrecuperables, registrar limitación y decisión del evaluador sin afirmar cumplimiento total. **Evidencia:** lista de revisión campo por campo, fuentes, recálculo independiente y validación de enlaces/nombres. No crear ahora los reportes finales para probar sus enlaces.

### V-21 — Ensayo de sustentación de 20 minutos

**Relaciona:** B-32; rúbrica R4 y gestión de R1/R2. Guion propuesto, ajustable después de aceptación.

| Tiempo de gestión | Contenido propuesto | Evidencia que debe sostenerlo |
|---|---|---|
| 0:00–2:00 | Problema, beneficiario, ámbito y alcance híbrido | Charter/visión y baseline conciliados, sin afirmar entrevistas inexistentes. |
| 2:00–5:00 | Baseline vs real, variaciones y EVM | Reportes 01–03 con datos económicos sustentados y elección EAC; si falta información, explicitar límite. |
| 5:00–7:00 | Tablero y radiadores | Gráficos/capturas de origen real con corte e interpretación, no imagen antigua como estado actual. |
| 7:00–10:00 | Riesgos/correcciones, calidad, aceptación, cierre y lecciones | Resultados del candidato, satisfacción/transferencia, pendientes y compromisos reales. |

| Tiempo de demostración técnica | Acción propuesta | Evidencia observable |
|---|---|---|
| 0:00–1:00 | Acceder como rol previsto y explicar conexión | Frontend del candidato y request backend real, sin mostrar claves/tokens. |
| 1:00–3:00 | Flota y pedidos de jornada seleccionada | Alta/importación/validación y persistencia al recargar; campos completos. |
| 3:00–5:00 | Generar ruta válida y abrir mapa/tabla/detalle | Resultado completo, versión, restricciones y calles OSRM; respuesta de API y errores controlados si procede. |
| 5:00–7:00 | Conductor, entrega y, si aceptado, recálculo | Estado real persistente, fecha/comprobante y roles; dinámica solo si pasa V-15. |
| 7:00–9:00 | Dashboard y PDF del mismo periodo | Números/factores/versiones conciliados y archivo abierto; no mezclar KPI logísticos con EVM. |
| 9:00–10:00 | Recuperación/fallo controlado y conclusión funcional | Fallback probado o rechazo de ruta inválida; estado/alcance final explícitos. |

**Aceptación:** ensayo cronometrado de 10 min gestión + 10 min técnicos, fluido, sin bloqueantes ni sustituciones silenciosas de API/BD. Mantener dataset precargado restaurable para no gastar tiempo en tecleo, declarar qué se precargó y qué se ejecuta. Una segunda persona reproduce el guion con instrucciones. Un ensayo adicional solo si aparecen fallos o el tiempo requiere ajuste.

**Contingencias:** comprobar red/proveedor antes; si OSRM/teselas fallan, usar fallback probado y declarar límite; no reemplazarlo por datos simulados anunciados como vivos. Backup y evidencia previa identificada pueden explicar un fallo, pero no cuentan como demostración funcional satisfactoria de un módulo que no ejecuta. No exponer credenciales en DevTools. **Evidencia:** checklist, duración por bloque, defectos encontrados/cerrados y candidato exacto.

### V-22 — MP4 de aproximadamente cinco minutos

**Relaciona:** B-32/G-05, rúbrica R5. **Destino futuro:** `docs/05 Video proyecto`, formato `.mp4`.

Guion propuesto: 0:00–1:00 problema, solución, valor y público; 1:00–1:40 flota/pedidos reales; 1:40–2:45 optimización válida/mapa/tabla; 2:45–3:45 entrega y persistencia (dinámica solo aceptada); 3:45–5:00 KPI/PDF conciliados y cierre del recorrido. Seleccionar funciones principales para mostrar un caso completo, no un montaje de pantallas sin transacción.

**Aceptación:** archivo abre y reproduce inicio a fin, ambos segmentos continuos, audio/imagen comprensibles y datos sensibles ocultos. Objetivo sobresaliente: duración 5 min ±15 s, imagen HD/transiciones claras; suficiente: ±30 s según consigna. Verificar contenido real frontend/backend y que el entorno coincide con el candidato aceptado; el video editado no debe hacer pasar una simulación por ejecución viva. Registrar duración, formato, reproducción y vínculo desde documentación futura si se acuerda. No se graba ni crea archivo ahora.

### V-23 — Capacidad y disponibilidad

**Relaciona:** B-27; RNF-01/04/06. **Dataset:** DS-08.

Definir qué significa 1000 pedidos/día y 50 vehículos: ventana, concurrencia, tasa, mezcla de operaciones y límites de latencia/errores aceptados; medir consultas/índices, recursos, colas y fallo/recuperación. Para disponibilidad, definir SLI (p. ej. peticiones elegibles exitosas o minutos disponibles), ventana y exclusiones acordadas; recopilar observación real y alertas.

**Aceptación:** capacidad demostrada bajo carga representativa y sin pérdida de datos/seguridad; disponibilidad ≥99,5 % solo si se acredita en ventana definida. Una prueba de minutos, endpoints saludables o un reinicio aislado no permiten declarar el porcentaje de disponibilidad. **Evidencia:** dataset/hardware/concurrencia/tiempo, métricas/errores/recursos, SLI y ventana, incidente/restore/alertas observadas.

### V-24 — Resultados ambientales y mejoras opcionales

**Relaciona:** B-02/12/28/33, E-03; Green Software y objetivos del charter.

Separar emisiones estimadas del transporte de energía/CO₂ digital. Para GA o compresión, comparar antes/después en unidad funcional y entorno iguales; explicitar estimación/medición, factor/fuente/fecha, carga y límites. Para ahorro ≥15 % km y ≥10 % CO₂, usar baseline acordada y distribución de escenarios; una simulación no acredita mejora mensual operacional. Si se incluye compensación, validar residual, plan/acciones/responsable/costo/calendario y evidencia de ejecución cuando se afirme.

**Aceptación:** cifras reproducibles con supuestos declarados, sin reutilizar ejemplo hipotético Green IT como medición ni equivalencia de árboles como plantación. Mejoras opcionales no degradan factibilidad, SLA o legibilidad. **Evidencia:** método, datos, factores, cálculos y límites; no declarar certificación integral por estos ensayos.

## 5. Registro y decisión de aceptación futura

Por caso registrar como mínimo:

| Campo | Contenido obligatorio |
|---|---|
| Identidad | ID V/caso, RF/RNF/US/EN y B/G asociado, título y prioridad. |
| Contexto | Fecha/huso, ejecutor/rol, commit, entorno/versiones/hardware, dataset/hash/semilla, configuración sin secretos. |
| Procedimiento | Precondiciones, pasos/comando real, entrada, resultado esperado y criterio/tolerancia acordados antes. |
| Resultado | Observado, medición/unidad, aprobado/fallido/bloqueado/no ejecutado, evidencia original y defecto relacionado. |
| Decisión | Responsable/aceptante, fecha real, decisión, excepción/riesgo residual y revisión que la aprueba si existe. |

**No ejecutado** no es aprobado; **bloqueado por setup** no equivale automáticamente a defecto del producto. Una prueba con mocks demuestra solo el contrato simulado. Una corrección reabre las verificaciones que afecte: solver→V-07/08/11/15/10/12/13; esquema→V-05/06/08/09; roles/WS→V-02/03/04/15; factores→V-10/13/24. Después de las pruebas pertinentes verdes, completar aceptación integrada del candidato; evitar repeticiones generales sin cambio o riesgo pendiente que las justifique.

## 6. Criterios de salida y bloqueantes de demostración

- Cero bloqueantes abiertos de privacidad/autorización, pérdida de operaciones, terminalidad, doble asignación, publicación inválida o doble contabilización en el alcance presentado.
- Requisitos presentados como completos aceptados con todos sus criterios; deuda/exenciones explícitas y coherentes con baseline. No mostrar como funcional tráfico real, redistribución multivehículo, comprobante o compensación si solo hay interfaz/parcial.
- Corrida candidata trazable y DoD cumplida o excepción formal acordada; valores históricos y actuales no mezclados. SLA solo acreditado con resultado válido y medición extrema a extremo.
- Datos suficientes para siete reportes, EVM y gráficos reales, aceptación/satisfacción/transición documentadas, enlaces/versiones revisados; si algo no se puede acreditar, comunicarlo antes del cierre sin fabricar evidencia.
- Guion reproducible y ensayo dentro del tiempo, entorno/dataset restaurables, video válido en ruta correcta. El demo no se usa como prueba de disponibilidad prolongada ni de ahorro mensual.

## 7. Lo comprobado hoy

Solo se ejecutaron inspecciones Git/archivos/enlaces/ignore/hashes, tipado TypeScript sin emisión (salida 0), cuatro pruebas SW en memoria (4/4) y auditoría de `dist` preexistente (aprobada, sin build). Se leyeron artefactos históricos de cobertura y benchmark; no se generaron nuevos ni se ejecutó el solver. La evidencia exacta y sus discrepancias están en C-01…10 del inventario compañero. Todo V-* continúa como protocolo pendiente salvo las comprobaciones de lectura que expresamente coincidan; estas no cierran RF ni aceptación integral.
