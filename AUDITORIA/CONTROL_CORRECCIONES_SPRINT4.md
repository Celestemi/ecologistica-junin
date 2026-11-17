# Control de correcciones Sprint 4

**Estado más reciente: fases0–5 finalizadas;ver sección Fase5 al final.** Se preserva el registro cronológico de estados e intentos anteriores. Proyecto sin cierre definitivo acreditado. Entrega vigente:REAUDITORIA_POST_CORRECCIONES.md,MATRIZ_AF_01_A_AF_35.md y PENDIENTES_PARA_USUARIO_Y_DOCENTE.md.

Referencia inicial: main/b47d5eb7cda26444c56460ea74591cc5f973e0b3, 17/11/2026 America/Lima. Ejecución autorizada por CODEX_PLAN_CORRECCIONES_POST_AUDITORIA.md y solicitud del usuario. Sin commits/push/deploy ni BD existentes.

## Fase 0 — En curso

Se leyeron plan, cuatro auditorías y backlog y se inspeccionaron fuentes/fixtures. Cambios preexistentes: .vitest/, cuatro informes finales y archivo del plan, todos sin seguimiento. No se eliminan ni sobrescriben.

Archivos de implementación: .gitignore, vitest.config.ts, scripts/run-post-audit-tests.ps1. Reportero JSON/caché ahora en rutas controladas de AUDITORIA; residual preservado. Nuevo PostGIS descartable verificado (tmpfs, sin volúmenes), puerto 25436; ninguna conexión a BD previa. Python 3.11.17 / Node 24.22.1. Plan completo: PLAN_CORRECCIONES_EJECUTABLE.md.

Pruebas base en ejecución con scripts/run-post-audit-tests.ps1 -Phase fase0. Resultado y autorización de siguiente fase se agregan al finalizar, sin borrar esta entrada.

### Fase 0 — Finalizada

Pruebas actuales en PostGIS NUEVO descartable: 185 backend PASARON, 0 fallos/omisiones, 30,20 s; frontend 68 PASARON/1 FALLÓ de 69 (AF-24 reproducido). JUnit/log/JSON en CORRECCIONES_EVIDENCIAS/fase0. Primer intento frontend interrumpido por tratamiento PowerShell de stderr; runner corregido para conservar advertencias y decidir por código de salida; segunda ejecución completa conservada. JSON quedó en la ruta explícita, sin tocar residual anterior. No es un fallo de producto adicional.

No hay bloqueos para fase 1. Los P0 de seguridad se confirman en código; presupuesto/actas siguen bloqueados por datos humanos. Siguiente: regresiones AF-01/02/03, mínimo cambio de política vigente, bloqueo transaccional y separación de canales. Cada cambio se probará contra B-08 y suite actual, no resultados históricos.

## Fase 1 — Corrección y regresión finalizadas

AF-01/02/03 corregidos en caminos REST/WS con 11 regresiones nuevas; 196 backend PASARON/0 fallos/0 omitidas (fase1-regresion, 36,43 s) y carrera reforzada 11 PASARON (fase1-carrera). B-08 28 unidades+14 BD preservadas. TypeScript PASÓ. Frontend 68/69 con AF-24 preexistente; contrato de token WS actualizado y prueba App correspondiente. UI tracking ajustada después de esa ejecución; se revalida antes de nuevos cambios acoplados.

AF-06 parcial: revocación en bitácora, expiración/watchdog/rol y subprotocolo probados; despliegue/proxy/límites globales no certificados. Detalle, archivos y fallos intermedios preservados en RESULTADOS_FASE1_SEGURIDAD.md. No migraciones ni BD existente. Plan de fase 2 mantiene bloqueos individuales por contrato/esquema/aprobación y no fabrica fuentes económicas.

Fase1-salida: frontend nuevamente 68/69, solo AF-24; prueba de tracking corregida para advertencia de destino aproximado sin GPS. No regresión nueva pendiente antes de fase 2. Se descubrió que importación CSV ya existe en order_import.py/desk.py; se corregirá la conclusión heredada en reauditoría, sin implementar una copia innecesaria.

## Fase 2 — Finalizada con operaciones bloqueadas identificadas

204 backend PASARON/0 fallos/0 omitidas, 40,25 s (fase2-final), 70 frontend PASARON/0 fallos (fase2-frontend-final); TypeScript PASÓ. AF-24 resuelto con caso adicional de cursor/continuación. Seguridad fase1 y B-08 conservados. Testigo independiente sintético 150×15 factible por API ASGI/PostGIS y pipeline dinámico dentro de límites; no OSRM/red real. Upgrade SQL real solo TEMP sintético, no BD previa. Estados parciales/bloqueos y archivos en RESULTADOS_FASE2_FUNCIONALIDAD.md.

AF-07/08/09/10/11/12/13/14/15 parciales según evidencia, no cerrados íntegramente: faltan referencias/factores por vehículo, política de comprobantes/GPS, contratos de alcance, esquema legado y validación de infraestructura/usuarios. CSV de importación ya existía (rectificación de auditoría). Nuevos eventos usan Bitacora existente, sin DDL automático ni nueva dependencia. Siguiente fase 3: suites con cobertura, CI/secretos, build y stack descartable; demo de diez minutos solo si realmente observada.

## Fase 3 — En curso

Suites con cobertura inicial: 204 backend verdes, líneas 4100/4864=84,2928 %, ramas 784/1234=63,5332 %, combinado 4884/6098=80,0918 %; frontend 70 verdes, líneas1059/1316=80,47 %, ramas898/1255=71,55 %. Gates ahora >=80 combinado backend y >=80 líneas frontend, sin reducir umbrales. Configuración CI actualizada, staging no observado. Suites finales fase3-final-backend (en ejecución) y fase3-final-frontend (70 verdes) revalidan fixture con clave sintética.

Se detectó dependencia de política snapshot: optimización inicial podría ocultar entregas activas al añadir nuevos pedidos. Guard 409 exige inserción/reoptimización, con prueba sin mutación; siete regresiones integridad verdes (fase3-guard); total backend esperado205, verificar JUnit, no asumir. Nueva corrección documentada, no cambio de alcance.

Build nuevo en runtime/build-fase3 pasa Vite y auditor PWA (437395 bytes JS/CSS); SW4/4, TypeScript y AST94 archivos pasan. Escáner de patrones HEAD/historial:560 blobs y254 archivos de trabajo, sin coincidencias; no certificado absoluto. npm audit registro público:0 vulnerabilidades; pip-audit/ruff/bandit no instalados, sin instalar dependencias. Browser/Computer Use sin host ni pipe nativo tras dos intentos: UI/lector/zoom/demo10min NO VERIFICABLES, no se usó automatización alternativa de navegador.

Servidores propios localhost: backend18000 inicialmente PID19540 (detenido), reiniciado PID4868 sesión17012 tras guard; Vite15173 sesión75276, proxy API_PROXY_TARGET18000. Contenedor sigue NUEVO tmpfs puerto25436. No tocar otros procesos/BD. Flujo scripts/post-audit-e2e.py ejecutado por -m scripts.post-audit-e2e pasó10 pasos TCP HTTP/WS, BD real, login por proxy, pedido→solver→mapa GeoJSON→conductor→entrega→KPI→PDF/CSV; 2,4449 s, sin navegador/OSRM/TLS/tiempo de exposición. Artifacts fase3-e2e/result.json y reportes sintéticos. Repetir luego de suite final (sin ejecutar ambas sobre BD al mismo tiempo).

Pendiente fase3: protocolo/carga aislada y backup/restore descartable, resultados/matriz/runbook/guía de demo. Después fase4: HTML completo, revisiones técnicas aditivas de siete documentos oficiales, solicitudes de datos EVM/humanos, preservar historia. Fase5: regresión final, matriz35AF/56H, reauditoría e integridad/limpieza de recursos propios. No commits/push. Los cuatro informes originales y residual .vitest deben permanecer intactos.

### Fase 3 — Finalizada

Resultados definitivos tras parche:209 backend PASARON/0 fallos/0 omitidas,74,21 s;líneas4104/4869=84,2884 %,ramas787/1236=63,6731 %,combinado4891/6105=80,1147 %. Frontend70 verdes,80,47 % líneas;SW4/4;total283 casos únicos. E2E real TCP10 pasos1,3382 s tras reiniciar backend PID12952/sesión89330 con parche. Vite sigue sesión75276. Lab carga:1000 pedidos/50 activos,80 lecturas concurrencia8,0 errores,1,7718 s;p95.26219 s;dump/restore NUEVO con conteos iguales en BD ecologistica_restore_20261117_104943. No se probó reinicio de almacenamiento tmpfs como durabilidad.

OSV detectó transitoria opentelemetry-api1.45.1 moderada;parche oficial1.45.2 verificado SHA y mismo Requires-Dist,instalado solo ese paquete con --no-deps/no-index/no-cache/copy después de fallo de caché por acceso denegado. No elevación/protecciones cambiadas. uv pip check47 compatibles;OSV48 consultas actuales0 avisos;npm audit0. Evidencia anterior conservada. Nueva dependencia instalada:ninguna;un paquete existente actualizado y mínimo fijado. Fuente primaria/documento en CORRECCION_DEPENDENCIA_SEGURIDAD.md. ReDoS no explotado.

Entregables: RESULTADOS_FASE3_PRUEBAS.md,MATRIZ_PRUEBAS_ACTUALIZADA.md,GUIA_DEMO_VERIFICADA.md,RUNBOOK_TECNICO_POST_CORRECCIONES.md. Host de navegador/pipe indisponibles:demo10min/WCAG visual/lector NO VERIFICABLES;no se simularon. Se continúa fase4 solo con evidencias nuevas reales,fuentes económicas/humanas bloqueadas individualmente. Cualquier consulta de esquema/BD existente permanece sin ejecutar.

## Fase 4 — Finalizada con fuentes bloqueadas

HTML completo y siete documentos releídos. Siete revisiones oficiales r1 en mismos nombres/versión base1.0.0,con historial y snapshot de bytes/hash/base64 previo en docs_cierre_antes_r1.json. README actualizado solo por trazabilidad/estado;14 relaciones ida/vuelta siguen funcionales. Verificador contra HTML:160 presencias textuales,0 faltantes/markers (no equivalen a contenido completo). Hash previo61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1 comprobado antes de corregir formato. Cuatro auditorías originales y docs01/02/03/capturas intactos.

Sin datos económicos nuevos ni series Jira/encuestas/actas. Solicitudes prospectivas SOLICITUD_DATOS_EVM.md y SOLICITUD_EVIDENCIAS_HUMANAS.md;fuentes irresolubles enumeradas sin redirigir a evidencia distinta. AF-32 corregido,AF-26 abierto,AF-28 parcial. Nueva prueba de desconexión detectó token público en logger de aplicación;corregido sin cambiar contrato,13 casos seguridad verdes fase4-log-verde. Logging de servidor/proxy real sigue pendiente AF-06. Resultado/archivos detallados en RESULTADOS_FASE4_DOCUMENTACION.md. Siguiente fase5:209backend completos sobre último log hardening,frontend/SW,matrices35AF/56H y reauditoría/integridad final.

## Fase 5 — Finalizada,17/11/2026 11:40 America/Lima

Rama main y HEAD b47d5eb7cda26444c56460ea74591cc5f973e0b3 siguen sin commits. Relectura de auditorías/HTML y contraste separado del corte actual;sin revisión externa por pares acreditada. Se mantuvieron los criterios originales,sin sustituir aceptación por tests.

Nueva regresión PDF (AF-15):tests/test_pdf.py:72 reprodujo error al interpretar texto de cliente/dirección como markup ReportLab (fase5-pdf-rojo);html.escape en pdf_generator.py:414 lo corrige (fase5-pdf-verde4/4). Sin URLs externas ni datos reales. AF-15 permanece parcial por metodología/factores/conciliación/aceptación visual. Intentos fallidos conservados.

Pruebas finales:runner -Phase fase5-final-backend -Coverage → **210 aprobadas,0 fallos/omitidas,73,351s**;4109/4870líneas=84,3737%,789/1236ramas=63,8350%,4898/6106combinado=80,2162%. Frontend -Phase fase5-frontend -Frontend -Coverage → **70aprobadas**,80,47%líneas/71,55%ramas. node --test scripts/test-service-worker.mjs → **4aprobadas**,0omitidas;TypeScript sin emisión PASÓ. **284casos únicos**,sin sumar repeticiones. B-08 y regresiones anteriores verdes. Un aviso de deprecación Starlette/httpx,no fallo. AST98fuentes pasa;no lint completo. Gates80combinado/80líneas satisfechos sin inventar aprobación humana de DoD.

Backend propio reiniciado con último código (PID16920,sesión49472);E2E **10pasos TCP HTTP/WS+PostGIS real**,fase5-e2e/result.json,0,938784s a11:28:35−05;PDF11909bytes/CSV241bytes. Geometría vial=false,sobre geográfico provisional,OSRM/TLS/UI no probados. Script admite identificador validado de salida para preservar fase3. Benchmark ASGI actual150×15factible1,771442s y dinámica pipeline0,244362s;no SLA TCP150ni demo10min. Frontend fuente sin cambios después del build fase3.

Runner reforzado:verifica etiqueta,tmpfs,sin volúmenes,contenedor activo y bindingexacto127.0.0.1:25436 antes de abrir fixtures;focal4PDF/BD pasó otra vez en fase5-runner-seguro,sin cambios de aplicación posteriores a210. Secret scan560blobs y archivos actuales por patrones sin hallazgos;SCA npm/OSV sin avisos tras parche documentado. Logs de Uvicorn mostraron path público,por eso AF-06 sigue parcial pese a logger de aplicación saneado. No se certifican secretos/logs externos.

Archivos fase5:pdf_generator.py,test_pdf.py,runner,post-audit-e2e.py;verificador nuevo scripts/verify_post_audit_delivery.py;README y siete documentos oficiales revisión técnica r2,base1.0.0 e historial r0/r1 conservados,snapshot r1 en docs_cierre_antes_r2.json. Nuevos REAUDITORIA_POST_CORRECCIONES.md,MATRIZ_AF_01_A_AF_35.md,PENDIENTES_PARA_USUARIO_Y_DOCENTE.md;baseline/manifiesto/integridad/enlaces/logs finales en CORRECCIONES_EVIDENCIAS. Temporales final_checks.py/finalize_docs.py solo en runtime ignorado. manifest-final.json enumera rutas+SHA de modificados/nuevos,excepto tres salidas autorreferentes/runtime.

Resultado:**6resueltos AF-01/02/03/24/30/32,17parciales,1abierto AF-26,11bloqueados/no verificables**. H01–H56:**14CUMPLE,16PARCIAL,20NO CUMPLE,6NO VERIFICABLE**. Sin porcentaje de avance/EV ni nota inventada;cuatro criterios rúbrica sin puntuación numérica sustentable (perfiles mixtos/demo no observada;máximo aplicable21). Video excluido,sin0ni pendiente.

Integridad:38/38archivos históricos del inventario y5/5protegidos (cuatro auditorías+residual .vitest) idénticos. No se afirma conservar484archivos intactos:fuentes/configs/cierre cambiaron deliberadamente. Documentos r2:7nombres exactos,160presencias/0faltantes/0markers/14relaciones correctas. README+docs:192ocurrencias revisadas,31rotas hacia6destinos históricos ausentes,sin redirigir a otras evidencias. git diff --check PASÓ;avisos LF/CRLF sin error. Reportes nuevos/documentos:enlaces resuelven,tablas consistentes,35AFy56Hsin duplicación.

Recursos propios cerrados:backend49472 yVite75276 interrumpidos;contenedor88bb14474e69e51e15f96c4c9844e553bcb83ae8921869eed5f444ef6734b614 detenido tras verificar ID/etiqueta/tmpfs/sin volúmenes;--rm eliminó solo datos sintéticos efímeros. resource-cleanup.json:sin contenedor propio ni listeners18000/15173/25436,PID16920 ausente. Backup sintético/evidencias en runtime preservados. No BD previas alteradas,ni migración persistente;SQL solo TEMP sintético. Residual/históricos preservados. Un paquete existente1.45.1→1.45.2 por aviso verificado,sin dependencias nuevas,secretos reales,producción,commits/push/deploy.

**Entrega:**fases autorizadas finalizadas y reauditoría disponible;proyecto sin cierre definitivo. Operaciones detenidas individualmente:EVM/calendarios/Jira/aceptación/retro auténticos,contratos/políticas faltantes,BDexistente,ensayos navegador/campo y servicios externos. Trabajo técnico parcial y aportaciones exactas separados en PENDIENTES_PARA_USUARIO_Y_DOCENTE.md. Guía disponible;UI/10min/tercero NO VERIFICADOS. No se solicita otro prompt para fases ya ejecutadas ni aprobación retroactiva.

