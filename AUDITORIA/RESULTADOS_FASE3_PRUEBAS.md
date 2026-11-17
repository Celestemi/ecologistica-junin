# Fase 3 — Pruebas reproducibles e integración

17/11/2026 America/Lima; main/b47d5eb7cda26444c56460ea74591cc5f973e0b3 + cambios sin commit. Sin producción/BD existente/commit/push/deploy. Audiovisual EXCLUIDO TEMPORALMENTE — NO EVALUADO.

## Resultado actual

| Comprobación | Resultado | Evidencia y alcance |
|---|---|---|
| Backend completo tras parche de seguridad | 209 PASARON, 0 fallos/omisiones;74,21 s con cobertura | CORRECCIONES_EVIDENCIAS/fase3-parche-backend/backend-junit.xml, backend.log |
| Frontend completo |70 PASARON,0 fallos/omisiones | fase3-final-frontend/frontend-results.json; componentes con mocks, no navegador |
| Service Worker |4 PASARON | node --test scripts/test-service-worker.mjs |
| TypeScript |PASÓ | tsc --noEmit --incremental false |
| Build nuevo |PASÓ,96 módulos;437395 bytes JS/CSS | runtime/build-fase3; Vite --configLoader runner, destino verificado dentro de AUDITORIA |
| Auditor PWA/build |PASÓ | scripts/audit-green-build.mjs runtime/build-fase3; precaché versionado, conductor/login presentes; no se rehízo dist raíz |
| Sintaxis Python |PASÓ por AST en archivos app/tests/scripts | No sustituye lint completo; ruff/bandit no instalados, no se inventa resultado |
| Scan secretos |Sin coincidencias de patrones en560 blobs históricos y254 archivos de trabajo al primer corte | secret-scan.json; valores no se imprimen; no prueba ausencia absoluta ni configuración externa |
| npm audit |0 vulnerabilidades comunicadas,236 dependencias en reporte | npm-audit.json; registro público; sin actualización npm |
| SCA Python OSV |48 paquetes instalados/transitivos revisados,0 avisos después de parche | python-osv-before.json conserva aviso inicial; python-osv.json actual |
| Compatibilidad Python |47 distribuciones instaladas compatibles | uv pip check;48 consultas OSV incluyen nombres normalizados/extras, no son48 paquetes nuevos |
| Integración HTTP/WS TCP y PostGIS real |10 pasos PASARON,1,3382 s tras reiniciar servidor con parche | fase3-e2e/result.json; NO navegador/OSRM/TLS ni demo de10 min |
| Densidad/carga sintética |1000 pedidos,50 vehículos activos,80 lecturas concurrentes8;0 errores;1,7718 s | fase3-load/result.json; p50 .18144 s,p95 .26219 s; no certifica1000/día de negocio |
| Backup/restore sintético |PASÓ a otra BD NUEVA en el mismo contenedor descartable | backup258155 bytes;.3812 s,restore .7069 s;conteos1005 pedidos/52 vehículos/1 bitácora idénticos (incluye semilla) |
| Browser/zoom/lector/demo10 min |NO EJECUTADA/NO VERIFICABLE | Dos intentos: host navegador y pipe nativo no disponibles; no se sustituyó por capturas simuladas |
| CI remoto/staging/TLS/OSRM real |NO VERIFICABLE | Configuración local revisada; sin push/deploy ni credenciales externas |

Total de casos únicos en suites actuales: **209+70+4=283 aprobados**,0 fallidos/omitidos. Los10 pasos E2E y80 lecturas de carga se informan aparte; no inflan el conteo de tests. Los resultados intermedios y anteriores permanecen identificados por fase.

## Cobertura y gates

Backend: líneas4104/4869=84,2884 %; ramas787/1236=63,6731 %; combinado4891/6105=80,1147 %. Frontend: líneas1059/1316=80,47 %; ramas898/1255=71,55 %; statements77,89 %; funciones76,73 %. No se redondea una métrica distinta para afirmar otra.

Gates configurados >=80 % **combinado backend** y >=80 % **líneas frontend**; ambos pasan actualmente. Se elevó el antiguo cov-fail-under=0; no se redujo un umbral para ocultar fallos. Esta selección de medición queda explícita para validación de DoD por responsables reales, no es aceptación docente por sí misma. El margen combinado backend es pequeño: mantener regresiones de caminos relevantes; no añadir pruebas de espejo solo por subir un número.

## Rendimiento: escenario y testigo

En JUnit actual: API ASGI+worker+PostGIS,150 pedidos/15 vehículos,150 únicos y factibles,**1,782138 s**; reoptimización por pipeline de función/worker/persistencia **.237260 s**. Testigo independiente de15 grupos×10,80 kg/1 m3/grupo,ventana8 h y cota63,2 min con velocidad conservadora10 km/h. No es el dataset aleatorio anterior; su0/3 factible no se borra ni contradice este escenario favorable. Matriz geodésica, sin OSRM. No se afirma SLA universal ni latencia WS de150 pedidos.

Carga es smoke de lecturas sobre densidad sintética, no mezcla de todas las operaciones/optimización concurrente. No se reinició PostgreSQL tmpfs para fingir durabilidad; la BD restore fue nueva y descartable. Falta ventana/SLI de99,5 % y diseño durable multiworker.

## Hallazgo adicional de seguridad y corrección acotada

OSV detectó dependencia instalada opentelemetry-api1.45.1 con aviso moderado GHSA-mf5v-w3w3-f6cg. Se contrastó con [mantenedor](https://github.com/open-telemetry/opentelemetry-python/security/advisories/GHSA-mf5v-w3w3-f6cg) y wheel oficial1.45.2, mismo requisito typing-extensions>=4.5.0 y SHA256 verificado. Se reemplazó **solo ese paquete existente** con --no-deps/--no-index/--no-cache; mínimo corregido en pyproject y backend/requirements. No se instalaron herramientas de auditoría ni nuevos paquetes transitivos.

Primer intento de caché falló por rename/acceso denegado; segundo con copia/cache temporal controlada pasó, sin cambiar protecciones del SO ni elevar permisos. Compatibilidad, OSV y209 tests tras el parche pasan. No se encontró uso directo del propagador en app ni se ejecutó ataque ReDoS; presencia de dependencia no equivalía a explotación. Ver CORRECCION_DEPENDENCIA_SEGURIDAD.md.

## Regresión acoplada encontrada y corregida

La política de snapshot completo exige no sustituir pedidos asignados con una nueva optimización solo de pendientes. Se añadió rechazo409 antes de publicar, indicando usar inserción/reoptimización. Prueba demuestra planes/estado intactos. Esto evita un problema de integridad introducido por la nueva regla de vigencia; no se avanzó dejando una regresión P0 reproducible.

## Reproducibilidad y archivos

Runner scripts/run-post-audit-tests.ps1 verifica etiqueta, puerto, tmpfs y ausencia de volúmenes antes de fixture destructiva; tests/conftest exige marcador explícito de BD descartable. Se fijan clave JWT sintética, cache/cobertura/tmp/JSON en rutas controladas. Nunca usar marcador para una BD importante.

Cambios fase3: runner, .github/workflows/ci.yml, pyproject.toml, backend/requirements.txt, vitest.config.ts, vite.config.ts (proxy local configurable), scripts/audit-green-build.mjs; nuevos scripts/audit-repository-secrets.py,audit_python_osv.py,post-audit-e2e.py,post_audit_load.py. Guard dependiente en routes.py y regresiones adicionales de seguridad/integridad. Nuevos informes de fase/matriz/guía/runbook.

CI usa servicio PostGIS efímero, historial completo para escaneo, cobertura exigida y SCA existente. Staging está desactivado por defecto y su placeholder falla si se intenta activar sin implementación; no se declara despliegue.

**Salida:** pruebas técnicas seguras completadas con los límites anteriores; AF-21/22/23/25/29/31/35 siguen parciales o no verificables en sus condiciones externas/humanas. Se continúa fase4 sin fabricar evidencias.
