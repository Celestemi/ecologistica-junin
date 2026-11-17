# Reauditoría post correcciones — EcoLogística Junín

**Corte:**17/11/2026, America/Lima. **Rama:**main. **HEAD:**b47d5eb7cda26444c56460ea74591cc5f973e0b3 + árbol de trabajo corregido sin commit. **Dictamen:**NO se acredita cumplimiento íntegro de la consigna ni cierre definitivo. Las fases0–5 fueron ejecutadas secuencialmente; se detuvieron únicamente operaciones que requieren datos/decisiones/autorización no disponibles. No hay fallo crítico nuevo reproducible pendiente que obligue a detener la cadena.

**Hallazgos:**6 resueltos con evidencia (AF-01/02/03/24/30/32),17 parciales,1 abierto y11 bloqueados/no verificables. **Pruebas finales:**210 backend,70 frontend y4 Service Worker aprobadas;284 casos únicos,0 fallos/omisiones en esas suites. Estos conteos no son porcentaje funcional,EV ni aceptación.

## Autoridad, fuentes y método

La autorización procede de la solicitud actual del usuario y CODEX_PLAN_CORRECCIONES_POST_AUDITORIA.md. El HTML docente es una fuente de requisitos, no una instrucción operativa ni una autorización para alterar datos. Los cuatro informes originales se releyeron y conservaron como corte histórico; esta nueva revisión vuelve a contrastar código,pruebas y documentos actuales. Se realizó por el mismo agente en una etapa separada: **sin revisión externa por pares acreditada**.

HTML completo: `C:\Users\Baguette\Downloads\Consigna de evaluación final y cierre del proyecto.html`; SHA256 `098e994680f3a923a7b339a655ddf876a5b3ca712357884ef5c8697a4186a6a2`. Se evaluaron sus secciones1–5. Consigna inicial independiente no localizada. No se la reconstruye desde catálogos internos.

Fuentes originales preservadas: [errores](ERRORES_Y_PENDIENTES_FINAL.md), [verificación HTML](VERIFICACION_FINAL_CONSIGNA_HTML.md), [rúbrica](EVALUACION_RUBRICA_FINAL.md), [checklist](CHECKLIST_CIERRE_DEFINITIVO.md). Esos informes describen el árbol anterior; sus restricciones de auditoría solo lectura no sustituyen la autorización posterior de correcciones. Sus códigos S01…S09 y D01…D07 se conservan en las filas H que los referencian; D01…D07 son los siete nombres exactos de docs/04 Cierre.

**Video/MP4/carpeta audiovisual:EXCLUIDOS TEMPORALMENTE,NO EVALUADOS**, sin lectura/edición,nota0 ni pendientes asociados. Sí siguen incluidas la demostración técnica en vivo10min y exposición de gestión10min.

## Ejecución y resultados por fase

| Fase | Resultado y regresión | Control/evidencia |
|---|---|---|
|0 |Inventario,aislamiento y baseline:185 backend verdes;frontend68/69,AF-24 reproducido. Residual anterior preservado |PLAN_CORRECCIONES_EJECUTABLE.md;fase0 |
|1 |Asignación vigente,terminalidad,privacidad y sesión;196 backend verdes;frontend solo AF-24 conocido. B-08 preservado |RESULTADOS_FASE1_SEGURIDAD.md;fase1-regresion/carrera |
|2 |Eventos,versiones,energía,PDF/CSV,guardas y paginación;204 backend y70 frontend verdes;TS pasó |RESULTADOS_FASE2_FUNCIONALIDAD.md;fase2-final |
|3 |209 backend/70 frontend/4SW verdes;gates80,build/TS/AST/SCA/secretos;stack TCP/carga/restore sintéticos;parche transitivo verificado |RESULTADOS_FASE3_PRUEBAS.md;MATRIZ_PRUEBAS_ACTUALIZADA.md;runbook/guía |
|4 |Siete documentos r1 con historia,solicitudes EVM/humanas;verificación160 presencias/14 enlaces;logger público saneado y13 regresiones seguridad verdes |RESULTADOS_FASE4_DOCUMENTACION.md;fase4-log-verde |
|5 |Revisión independiente del corte,PDF literal seguro probado rojo/verde,210 backend/70 frontend/4SW verdes;E2E TCP repetido sobre último código;documentos r2/matrices/integridad |Este informe;MATRIZ_AF_01_A_AF_35.md;PENDIENTES_PARA_USUARIO_Y_DOCENTE.md |

[Control secuencial](CONTROL_CORRECCIONES_SPRINT4.md) conserva intentos,fallos intermedios,archivos y dependencias. No se ocultan ejecuciones rojas anteriores ni se suman repeticiones como casos nuevos. Los informes de cada fase mantienen su propio corte;el resultado final210 sustituye209 para el árbol actual.

## Correcciones verificadas y límites técnicos

- **AF-01:**plan vigente por día Lima,advisory lock transaccional compartido y revalidación de usuario/asignación antes de mutar. Pruebas reales A→B:conductor antiguo rechazado en REST/cancelación;actual entrega;A espera la transacción de B y se rechaza tras su commit.
- **AF-02:**matriz común de estados,validación integral previa a persistir y terminales protegidos;entregado no se cancela/reinserta. Entrega repetida idempotente,fecha inválida no deja evento/estado parcial. B-08 conserva28 unidades y14 integraciones de publicación/atomicidad.
- **AF-03:**salas públicas separadas por pedido y whitelist de estado/ETA;sin IDs/GPS/secuencia/rutas ajenas. Snapshot,filtrado de ETA anidada,aislamiento y desconexión por canal efectivo verificados. Rol interno conserva sus mensajes autorizados.
- **AF-24/30/32:**contrato de paginación probado sin quitar mantenimiento/edición;reportero/caché controlados y residual idéntico;hash histórico correcto confirmado con Git,tipografía/corte reparados.
- **Mejoras parciales:**sesión revocable/expirable con vigilancia inactiva,subprotocolo Bearer,rol y límites;una versión activa por jornada y snapshot vacío que no revive historia;guard409 evita huérfanos por nueva optimización inicial;evento real durable en Bitacora,PDF por fecha efectiva,CSV por rol/periodo;galones separados de kWh/TCO estimado;factores del plan y ocultamiento de comparación inválida.
- **Regresión adicional fase5 AF-15:**texto de cliente/dirección se interpretaba como markup ReportLab. Nuevo `tests/test_pdf.py:72` reprodujo fallo de parser (fase5-pdf-rojo) y pasó tras `html.escape` en `app/services/pdf_generator.py:414` (fase5-pdf-verde4/4);suite completa final210/210. No se usaron URLs externas ni datos reales. No equivale a inspección visual completa del PDF.
- **Regresión adicional fase4 AF-06:**token público aparecía en logger de desconexión;caso existente amplió caplog/IO doble con BD real,reprodujo filtración sintética y quedó verde. El logger de aplicación ya no imprime ese token. **El servidor/proxy puede registrar el path**;no se certifican registros ni configuración de despliegue. Evidencia actual obliga a mantener AF-06 parcial.
- **Rectificación de auditoría:**importación CSV ya existía en order_import.py/desk.py junto a XLSX. La nueva exportación CSV de sostenibilidad es otro contrato;no se cuenta como completar la importación. RF-01/02 siguen parciales por atributos/validación de alcance.

Faltan por completo o en parte:administración de clientes/conductores y compensación según contrato,redistribución ante avería entre vehículos,carga/jornada acumuladas,estado GPS durable y multiworker,referencia FIFO/factores/conciliación integral de métricas,comprobantes con política de privacidad,upgrade legado real y aceptación. No son corregidos por tener suites verdes.

## Pruebas actuales reproducibles

| Verificación | Comando / evidencia | Resultado y alcance |
|---|---|---|
|Backend completo | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-post-audit-tests.ps1 -Phase fase5-final-backend -Coverage`;fase5-final-backend/backend-junit.xml |210 aprobadas,0 fallos/0 omitidas,73,351s;un aviso de deprecación Starlette/httpx. Incluye unidades y API/PostGIS real aislado;no todo es prueba de navegador |
|Frontend completo |Runner `-Phase fase5-frontend -Frontend -Coverage`;frontend-results.json |70 aprobadas,0 fallos/0 pendientes. Componentes y APIs con dobles donde corresponda |
|Service Worker | `node --test scripts/test-service-worker.mjs`;fase5-control/service-worker.log |4 aprobadas;no prueba reconexión de campo completa |
|TypeScript | `node node_modules/typescript/bin/tsc --noEmit --incremental false` |PASÓ,sin emisión |
|Build actual |Vite con `--configLoader runner --outDir AUDITORIA/CORRECCIONES_EVIDENCIAS/runtime/build-fase3`;auditor con destino explícito |PASÓ96 módulos;437395 bytesJS/CSS;SW/PWA. Frontend fuente sin cambios después de ese build;solo documentación/backend variaron |
|Seguridad estática |audit-repository-secrets.py;secret-scan.json;npm-audit.json;python-osv.json |Patrones560 blobs históricos y archivos de trabajo,sin coincidencias;SCA npm0/OSV0 después del parche. No certificación absoluta ni explotación de producción |
|Sintaxis Python |AST de app/tests/scripts con `ast.parse`;fase5-control |PASÓ. ruff/bandit/pip-audit no instalados;no se afirma lint/DAST completo |
|Documentos |verify_closure_documents.py con HTML original;closure-validation.json |7/7 rutas/nombres,160 presencias textuales,0 faltantes/markers,14/14 relaciones README↔documentos. No160 obligaciones sustantivas satisfechas |
|Git/integridad |git diff --check;verify_post_audit_delivery.py;manifiestos finales |Verificación del perímetro descrito abajo;sin commits,push ni deploy |

Los controles finales se registran en `CORRECCIONES_EVIDENCIAS/fase5-control/`:typescript.log,service-worker.log y checks.log. El runner se reforzó al final para comprobar también puerto/host y estado del contenedor antes de abrir fixtures;cuatro pruebas PDF con BD volvieron a pasar en fase5-runner-seguro. No altera el código de aplicación ni el conteo210 de la suite final.

**Cobertura final backend:**4109/4870 líneas=84,3737%;789/1236 ramas=63,8350%;4898/6106 combinado=80,2162%. Gate conservado/exigido80% combinado. **Frontend:**1059/1316 líneas=80,47%,898/1255 ramas=71,55%,statements1131/1452=77,89%,functions320/417=76,73%;gate80% líneas. Líneas y combinado no se intercambian. Umbrales configurados/técnicamente satisfechos;no se inventa aprobación humana del DoD.

**SLA:**testigo independiente150pedidos/15vehículos,150 únicos/factibles persistidos;API ASGI1,771442s≤45,pipeline dinámico0,244362s<30. Jornada8h/80kg/1m³,grupos cercanos al depósito,caso sintético favorable,testigo conservador63,2min,OSRM desactivado. Es API ASGI+worker+PostGIS real,**sin latencia HTTP TCP/WS/proveedor** para ese benchmark. Windows/Python3.11.17,Node24.22.1,16CPU lógicas registradas. No borra el benchmark histórico0/3 factible ni demuestra SLA universal.

**E2E actual TCP:**`python -B -m scripts.post-audit-e2e fase5-e2e`,10 pasos aprobados en0,938784s,17/11/2026 11:28:35−05. HealthBD,frontendHTML/JS/proxy,login/pedido,solver/persistencia/GeoJSON,conductor/WS público/entrega durable+retry,KPI,PDF11909bytes/CSV241bytes y403/401 por rol/logout. Solo datos sintéticos en BD nueva;no mocks de red. **Sin ejecución UI/tiles/OSRM/TLS**,geometría vial=false y sobre geográfico provisional advertido. No es un ensayo de diez minutos ni validación de la apariencia del PDF.

**Carga/recuperación limitada:**1000pedidos/50vehículos activos,80 lecturas/concurrencia8,0 errores,1,771769s,p50=0,181441s,p95=0,262192s. Dump258155bytes/0,381160s yrestore0,706918s a otra BD nueva;conteos fuente/restaurada1005|52|1 (totales incluyen fixtures previas/dos inactivas). No demuestra1000/día con mezcla completa,uptime99,5%,RPO/RTO productivo ni recuperación de GPS/multiworker.

**Parche de dependencia:**OSV detectó opentelemetry-api1.45.1 (GHSA-mf5v-w3w3-f6cg/CVE-2026-126360). Se justificó previamente,se verificó wheel oficial/hash y mismo Requires-Dist,se actualizó solo ese paquete existente a1.45.2 con --no-deps/no-index;no nuevas dependencias instaladas. Se fijó mínimo en pyproject/requirements;47 distribuciones compatibles en uv pip check,48 consultas OSV sin avisos actuales. Intento previo con caché falló por acceso denegado;reintento sin caché/copy funcionó,sin elevación ni cambios de protección. [Detalle y fuentes primarias](CORRECCION_DEPENDENCIA_SEGURIDAD.md). No se explotó ReDoS ni se rotaron secretos reales.

## Documentos oficiales y fuentes humanas

Siete archivos exactos en docs/04 Cierre permanecen con versión base1.0.0 y **revisión técnica r2**;identificación/corte/historial y snapshot r0/r1 permiten revisar todo lo anterior. Se actualizaron cifras solo desde resultados nuevos;README conserva14 relaciones de cierre. No se modificaron docs/01 Inicio,docs/02 Planificacion,docs/03 Implementación ni capturas para esconder inconsistencias.

EVM sigue sin cifras aprobadas:USD134400/PEN499968 a3,72 son estimación aritméticamente consistente,**no BAC aprobado ni AC**. Nueve celdas PV/EV/AC,SV/CV/SPI/CPI,%BAC y tres EAC no aplicables numéricamente sin fuentes reales. No disponible no equivale a0. [Solicitud de datos](SOLICITUD_DATOS_EVM.md).

Sin calendario base-real/gasto/Look Ahead costado,series EVM/CFD/CSI/Burndown/Burnup/Mood ni reunión/acta/satisfacción/transferencia auténticas. Jira2024/2026 y34/20SP,39/47SP no conciliados. Se entregaron [formatos prospectivos](SOLICITUD_EVIDENCIAS_HUMANAS.md),sin firmas ni aprobación inventadas. [Seis fuentes históricas](FUENTES_HISTORICAS_IRRESOLUBLES.md) permanecen ausentes;31 ocurrencias de enlaces rotas no se redirigieron a evidencia distinta.

## Matriz actual de las56 verificaciones HTML

**14 CUMPLE,16 PARCIAL,20 NO CUMPLE,6 NO VERIFICABLE.** Cambios de estado:H14/H41→CUMPLE;H51/H52/H53/H56→PARCIAL. Las restantes mantienen su clasificación con evidencia actualizada. No son un porcentaje de producto ni puntos académicos. Se separa ausencia del entregable obligatorio (NO CUMPLE) de magnitud o evento no observables (NO VERIFICABLE). Sin nota0 por falta de observación.

| ID | Requisito del HTML | Estado actual | Fuente | Contraste actual |
|---|---|---|---|---|
|H01 |§2/§5: siete archivos, ruta y nombres exactos |**CUMPLE** |S03 |Siete de siete presentes en docs/04 Cierre. |
|H02 |§5: Markdown, identificación, corte y versión |**CUMPLE** |S03 |Formato y versión 1.0.0 presentes; el cierre se identifica como borrador. |
|H03 |§5.1–5.7: secciones, campos y tablas de las plantillas |**CUMPLE** |S01/S03 |Estructura conservada; no equivale a valores completos. Detalle por documento abajo. |
|H04 |§1/§2: datos reales específicos y coherentes |**PARCIAL** |S03/S04/S06 |Contenido específico con límites honestos, pero múltiples campos no disponibles y fuentes históricas sin conciliación. |
|H05 |§1/§5: sustitución de marcadores de plantilla |**CUMPLE** |S03 |No se localizaron marcadores [ ? ] en los siete archivos. La ausencia del marcador no acredita el dato faltante. |
|H06 |§1: desempeño frente a líneas base aprobadas y periodo anterior |**NO VERIFICABLE** |S04/S03 |Hay planes y estimaciones; faltan aprobación y series temporales comparables. |
|H07 |§2.1/§5.1: logros, cambios de alcance y defectos |**PARCIAL** |D01/D06 y resultados fase1–5 |AF-01/02/03/24 corregidos con regresiones;sin aceptación integral ni cambios/exenciones de alcance aprobados. |
|H08 |§2.1/§5.1: hitos, fechas reales, causas, ruta crítica y acciones |**NO CUMPLE** |D01/S04 |Diagnóstico y acciones propuestos; sin calendario base-real verificable ni impacto cuantificado en ruta crítica. |
|H09 |§2.1/§5.1: fondos ejecutados, variaciones y contingencia |**NO CUMPLE** |D01/S04 |No hay ejecución financiera ni consumo real de reserva documentados. |
|H10 |§2.1/§5.1: Look Ahead de actividades y costos |**PARCIAL** |D01 |Actividades priorizadas concretas; costos siguientes no disponibles y calendario sin compromiso aprobado. |
|H11 |§2.1/§5.1: nuevos riesgos, incidentes y comentarios |**PARCIAL** |D01/D06 y matriz35AF |Incidentes/acciones ejecutadas y riesgos restantes diferenciados;no todos los incidentes tienen cierre aprobado. |
|H12 |§2.2/§5.2: variación cronograma, plan/real/causa/respuesta |**NO CUMPLE** |D02/S04 |Tabla de cinco campos existe; falta variación temporal calculable con fechas y baseline válidos. |
|H13 |§2.2/§5.2: variación de costo, plan/real/causa/respuesta |**NO CUMPLE** |D02/S04 |No AC ni comparación de gasto real contra presupuesto aprobado. |
|H14 |§2.2/§5.2: variación de calidad, métricas/defectos/causas/acciones |**CUMPLE** |D02 r2;JUnit/JSON/cobertura fase5 |Plan80 y resultados exactos,variación,causas/acciones y fallos intermedios trazados. Cobertura/verde no se presentan como aceptación. |
|H15 |§2.3/§5.3: BAC aprobado, unidad y estado financiero |**NO VERIFICABLE** |D03/S04 |Presupuestos referenciales no prueban BAC aprobado. |
|H16 |§2.3/§5.3: PV/EV/AC del periodo y acumulados actual/anterior |**NO CUMPLE** |D03 |Columnas presentes, nueve celdas sin cifras sustentadas. |
|H17 |§2.3/§5.3: SV/CV/SPI/CPI calculados e interpretados |**NO CUMPLE** |D03 |Fórmulas correctas, resultados inexistentes; indicadores numéricos NO VERIFICABLES. |
|H18 |§2.3/§5.3: porcentajes PV/EV/AC respecto a BAC |**NO CUMPLE** |D03 |Expresiones presentes sin aplicación numérica. |
|H19 |§2.3/§5.3: tres EAC y selección justificada |**NO CUMPLE** |D03 |Tres expresiones correctas; no proyecciones numéricas ni selección fundamentada en datos. |
|H20 |§2.3/§5.3: causas e impactos financieros/temporales EVM |**NO VERIFICABLE** |D03/S04 |No puede deducirse sobrecosto o retraso EVM sin magnitudes base. |
|H21 |§2.4/§5.4: KPIs justificados, interesados, frecuencia e interpretación |**PARCIAL** |D04 |Selección/frecuencia propuestas y lectura específica; sin operación periódica consolidada. |
|H22 |§2.4/§5.4: RAG por componente con enfoque y umbrales |**CUMPLE** |D04 r2 |RAG backend/frontend verdes para suites actuales;seguridad parcial/finanzas y cierre pendientes;enfoques y límites explícitos. |
|H23 |§5.4.3.1: líneas de tendencias/variación/EVM |**NO CUMPLE** |D04/D03 |Sin serie numérica ni gráfico EVM; la explicación de ausencia no lo sustituye. |
|H24 |§5.4.3.2: flujo acumulado/áreas apiladas |**NO CUMPLE** |D04/S06 |No CFD ni serie de estados a lo largo del tiempo. |
|H25 |§5.4.3.3: SPI/CPI con tamaño CSI e interpretación |**NO CUMPLE** |D04/D03 |No gráfico ni datos. Exigido por la plantilla/rúbrica; no inventar índices. |
|H26 |§5.4.3.4: medidor o barras con datos y lectura |**CUMPLE** |D04 r2 y fase5 |Barras Mermaid con aprobadas[210,70,4] y fallidas[0,0,0],tabla accesible y lectura;B-08 no se cuenta dos veces. |
|H27 |§2.5/§5.5: Burndown real y análisis de tasa |**NO CUMPLE** |D05/S06 |No captura/serie de trabajo restante real por fecha. |
|H28 |§2.5/§5.5: Burnup real y análisis de alcance/aceptado |**NO CUMPLE** |D05/S06 |No serie de alcance y trabajo aceptado por fecha. |
|H29 |§2.5/§5.5: Kanban y cuellos de botella |**PARCIAL** |D05/S06 |Imagen legible del proyecto y lectura de columnas; fecha/procedencia y evolución no acreditadas. |
|H30 |§2.5/§5.5: Mood Chart e interpretación del clima |**NO CUMPLE** |D05 |Tabla con No disponible; no mediciones del equipo. No permite inferir satisfacción. |
|H31 |§2.5/§5.5: tablero real de retrospectiva y acciones implementadas |**NO CUMPLE** |D05/S04 |Relatos/propuestas no son captura ni registro validado de retrospectiva y sus acciones. |
|H32 |§2.6/§5.6: descripción y alineación con Charter |**CUMPLE** |D06/S04 |Proyecto de logística urbana Huancayo/El Tambo/Chilca alineado con el acta; metas se presentan como objetivos. |
|H33 |§2.6/§5.6: alcance/calidad predictivos y adaptativos, validación/exenciones |**PARCIAL** |D06 y matriz35AF |Distinción predictivo/adaptativo y resultados reales nuevos;RF incompletos y exenciones/aceptación pendientes. |
|H34 |§2.6/§5.6: hitos previstos vs. fechas reales |**NO CUMPLE** |D06/S04/S06 |Faltan fechas reales aceptadas y reconciliación del calendario 2024/2026. |
|H35 |§2.6/§5.6: presupuesto aprobado vs. costo final y tolerancia |**NO CUMPLE** |D06/S04 |Hay estimación, no costo final ni aprobación/tolerancia verificables. |
|H36 |§2.6/§5.6: riesgos/incidentes/impedimentos e impacto/respuesta aplicada |**PARCIAL** |D06 y matriz35AF |P0 técnicos corregidos,riesgos/acciones y resultados documentados;impedimentos de gestión/alcance y cierre siguen abiertos. |
|H37 |§2.6/§5.6: éxito, satisfacción, cierre administrativo y transición |**NO CUMPLE** |D06 |Sin métricas auténticas de satisfacción, acta de cierre/aceptación ni transferencia validada. |
|H38 |§2.7/§5.7: ocho categorías de aprendizajes analíticos y accionables |**PARCIAL** |D07 r2 |Ocho categorías y lecciones específicas con hechos nuevos;no reunión/validación humana acreditada. |
|H39 |§2.7/§5.7: retrospectivas/reunión y conclusiones del cierre |**NO CUMPLE** |D07/S04 |Fecha/reunión de cierre no acreditadas; conclusiones provisionales no sustituyen ceremonia real. |
|H40 |§3/§4: separación y responsabilidades frontend/backend/configuración |**CUMPLE** |S02/S07 |src/ y app/ separados; API, servicios, modelos, pruebas y configuración identificables. |
|H41 |§3/§4: .gitignore y exclusión de dependencias/entornos/temporales |**CUMPLE** |.gitignore/vitest.config.ts/runner;integridad-final.json |Entornos/dependencias/temporales excluidos;reportero/caché/build controlados;residual previo preservado idéntico. |
|H42 |§3: limpieza del árbol y archivos versionados |**PARCIAL** |Git/manifiesto-final.json |Árbol autorizado modificado y sin commits por instrucción expresa;residual histórico conservado e ignorado. Inventario para revisión,paquete/versión aceptados aún pendientes. |
|H43 |§3/§4: ausencia de credenciales expuestas |**NO VERIFICABLE** |secret-scan.json;configuración |560 blobs históricos y archivos actuales revisados por patrones sin hallazgos;ausencia absoluta/secretos de despliegue no certificada. |
|H44 |§3/§4: coherencia, historial y versión de artefactos previos afectados |**PARCIAL** |D01–D07 r2 y snapshots;fuentes históricas |Revisiones oficiales versionadas con fuentes originales preservadas;persisten versiones/fechas y documentos históricos no reconciliables. |
|H45 |§3/§4: siete enlaces directos desde README |**CUMPLE** |S02/S03 |Siete destinos exactos comprobados físicamente. |
|H46 |§3/§4: siete retornos al README principal |**CUMPLE** |S03 |Siete retornos ../../README.md resuelven al archivo raíz. |
|H47 |§1/§3: coherencia de referencias históricas usadas como evidencia |**NO CUMPLE** |FUENTES_HISTORICAS_IRRESOLUBLES.md;links-final.json |31 ocurrencias históricas hacia seis destinos ausentes;sin correspondencia inequívoca.14 relaciones de cierre sí funcionan. |
|H48 |§3/§4: catorce enlaces bidireccionales funcionales |**CUMPLE** |S02/S03 |14/14 válidos; no confundir con las otras 31 referencias históricas. |
|H49 |§3: historial Git y trazabilidad del corte |**CUMPLE** |git rev-parse/log;manifiesto-final.json |HEAD completo identificado,sin commits;manifiesto SHA256 identifica árbol revisado. Hash anterior61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1 resuelve. |
|H50 |§1/§4: cumplimiento de criterios funcionales de aceptación |**PARCIAL** |MATRIZ_PRUEBAS_ACTUALIZADA.md y35AF |210backend/70frontend/4SW verdes,P0 corregidos;RF/RNF incompletos y aceptación/operación integral pendientes. |
|H51 |§4: arranque frontend/backend/BD en entorno de exposición |**PARCIAL** |fase5-e2e/result.json |Backend/PostGIS nuevos/frontendHTTP/proxy iniciados y health reales;entorno de exposición/navegador/proveedor no comprobados. |
|H52 |§4: integración efectiva frontend-backend en ejecución real |**PARCIAL** |fase5-e2e/result.json |Login mediante proxy,ViteHTML/JS transformado y TCPAPI/WS con BD reales pasan. No ejecución de UI ni OSRM/tiles reales. |
|H53 |§4: flujo end-to-end y resultados coherentes sin fallos |**PARCIAL** |fase5-e2e/result.json |Pedido→solver→BD→GeoJSON→conductor→entrega→KPI→PDF/CSV pasó en TCP. Sin render UI ni todos los criterios de aceptación. |
|H54 |Encabezado: exposición de gestión/cierre de diez minutos |**NO VERIFICABLE** |GUIA_DEMO_VERIFICADA.md |Guion prospectivo;no exposición de gestión10min observada/cronometrada. |
|H55 |§4: demostración técnica en vivo de diez minutos |**NO VERIFICABLE** |GUIA_DEMO_VERIFICADA.md |Ensayo técnico10min no observado;host/pipe navegador ausentes;no cero ni aprobado por tests. |
|H56 |§4: fluidez/aceptación y guía de despliegue para nivel superior |**PARCIAL** |RUNBOOK_TECNICO_POST_CORRECCIONES.md;E2E |Guía por versión y comandos propios probados;sin reproducción de tercero,fluidez/aceptación ni demo10min. |

## Rúbrica recalculada por evidencia

Se contrastaron nuevamente los descriptores completos del HTML,conservando el método de la auditoría original. Perfiles mixtos no producen una nota unívoca sin regla docente;la mejora técnica no autoriza promedio,peor subindicador ni puntos por archivo.

| Criterio | Peso | Nivel sustentable | Puntos ponderados | Evidencia y brecha |
|---|---:|---|---|---|
|Narrativos/EVM |1 |NO EVALUABLE numérico:perfil mixto |— |Tres archivos/estructura/causas/variación técnica presentes;sin aplicación numéricaEVM/EAC. No se acreditan enteros niveles2/3;la sola inexistencia de cálculos no permite inventar las demás condiciones del nivel0 |
|Visuales/cierre |1 |NO EVALUABLE numérico:perfil mixto |— |Cuatro archivos,RAG/barras reales y lecciones específicas;faltan gráficos/radiadores auténticos,satisfacción/reunión/cierre. No cumplir2/3 no justifica atribuir saturación o lecciones genéricas no observadas |
|Trazabilidad/versionado |1 |NO EVALUABLE numérico:perfil mixto |— |7 nombres/14 enlaces correctos,revisiones actuales con historia;31 enlaces históricos/versiones previas sin conciliar. No inventar1–2 enlaces bidireccionales rotos |
|Demo/arquitectura |4 |NO EVALUABLE:ensayo en vivo no observado |— |Arquitectura separada,ignore/runbook y TCP real mejoran;sin UI/fluidez/10min/aceptación. Ni0 por no observado ni2/3 por unidades verdes |
|Total aplicable |7 |Sin puntuación provisional numérica sustentable |No determinable sobre21 |Máximo1×3+1×3+1×3+4×3=21;guiones no son ceros |
|Audiovisual |4 |EXCLUIDO TEMPORALMENTE,NO EVALUADO |— |12 puntos fuera del máximo33 original;sin efectos en pendientes ni nota |

No se convierte a/20 ni se emite0/21. Se necesita completar evidencia o aclarar tratamiento de perfiles mixtos;el dictamen de incumplimiento sustantivo sigue siendo explícito.

## Integridad,archivos y operaciones detenidas

Los archivos modificados y nuevos se enumeran con SHA256 en [manifest-final.json](CORRECCIONES_EVIDENCIAS/manifest-final.json). Cambios principales:API REST/WS/auth/dependencias de sesión,servicios de planes/estados/eventos/energía/reportes/GA/indicadores,clientes tracking/conductor/dashboard/sesión,pruebas y herramientas de aislamiento/seguridad/verificación,CI/coverage/Vite/ignore,README y siete documentos de cierre. Informes/logs/snapshots se limitaron a AUDITORIA;temporales de pruebas/cobertura/build/backup en runtime ignorado.

[Integridad](CORRECCIONES_EVIDENCIAS/integridad-final.json) contrasta hashes previos de38 archivos históricos del inventario (incluidas capturas),los cuatro informes originales y residual .vitest. No se afirma que los484 archivos del inventario anterior sigan iguales:el código/configuración/documentos de cierre fueron modificados deliberadamente. .git,deps y material excluido quedan fuera de esa comparación. Un paquete existente de .venv cambió por el parche documentado;herramientas pueden usar cachés ignoradas de dependencias.

No se operó ninguna BD preexistente ni se migró esquema persistente. Solo contenedor NUEVO ecologistica-post-audit-20261117,ID88bb14474e69e51e15f96c4c9844e553bcb83ae8921869eed5f444ef6734b614,PostGIS15-3.4,tmpfs sin volúmenes,puerto127.0.0.1:25436 y claves sintéticas. Upgrade propuesto solo TEMP sintético;SQL no ejecutado automáticamente en arranque. No se usaron credenciales reales,no se eliminó el residual,no se hicieron commits/push/deploy. Recursos propios detenidos al finalizar:backend/Vite y contenedor verificado;sin listeners18000/15173/25436 ni contenedor propio restante. Datos sintéticos tmpfs descartados,backup/evidencias preservados. Resultado en resource-cleanup.json y control.

Comprobación final de enlaces README+docs (material excluido omitido):192ocurrencias,31rotas hacia6destinos históricos;14relaciones de cierre válidas. AST98archivos correcto y tablas/enlaces de informes nuevos y documentos oficiales correctos. No se certifica renderización visual ni lint completo.

Operaciones detenidas:BD existente/migración real,extensiones de contrato/esquema sin decisión,comprobantes sin política,datos económicos y evidencias humanas/históricas inexistentes,CI/staging externo y ensayos de navegador sin host. Se continuaron trabajos independientes. No se pide aprobación retroactiva ni se presume autorización por haber transcurrido tiempo.

## Disposición para demostración y siguiente intervención

**Listo con limitaciones para ensayo técnico local de API/WS con datos sintéticos;demostración UI integral y10min NO VERIFICADOS.** Computer Use se intentó dos veces y devolvió host/pipe no disponible;no se fabricaron capturas,temporización o aceptación. Guion y contingencias en [GUIA_DEMO_VERIFICADA.md](GUIA_DEMO_VERIFICADA.md),operación/rollback en [runbook](RUNBOOK_TECNICO_POST_CORRECCIONES.md).

El siguiente paso verificable requiere los datos,contratos,accesos y personas enumerados en [PENDIENTES_PARA_USUARIO_Y_DOCENTE.md](PENDIENTES_PARA_USUARIO_Y_DOCENTE.md),además del trabajo técnico aún parcial. No hay cierre administrativo acreditado ni cumplimiento íntegro de la consigna.

