# Sprint 4 — resultados actuales de pruebas (fase 3)

**Corte:** 17/11/2026, America/Lima. **Versión:** 1.0.0. **Estado:** validación parcial del MVP; cierre técnico bloqueado.

Fuente de instrucciones: `../CODEX_AUTOMATIZACION_FASES_3_4_5.md`, leído completo. Rama `main`, HEAD `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1`, **árbol de trabajo con B-08 preexistente sin commit**. Los resultados corresponden a ese árbol, no al código limpio del commit. No se modificó código, pruebas ni configuración durante esta fase.

## 1. Entorno y aislamiento

Windows 11 Pro 10.0.26200; AMD Ryzen 7 5700 X, 8 núcleos/16 hilos, 16.701.480 KiB de RAM visible. Python 3.11.17 de `.venv/Scripts/python.exe`, pytest 9.1.1, pytest-cov 7.1.0; Node v24.22.1, Vitest 5.0.5. Dependencias existentes; ninguna instalación.

Docker Server 29.7.2 sí estuvo disponible hoy. Se creó exclusivamente `eco-fases345-audit-20261117`, ID `7ce9d5f3a2b7f98b11ce8c691cd8221cbd829d484964fb552d49d328576e09a7`, desde la imagen local `postgis/postgis:15-3.4`, con `--pull=never`, base **ecologistica_test**, puerto **127.0.0.1:25435**, sin volúmenes previos, almacenamiento PostgreSQL tmpfs y logs Docker deshabilitados. Se inspeccionaron montajes/puerto antes de ejecutar fixtures. El intento inicial de puerto 55434 falló por reserva de Windows; se verificó con `netsh`, no se cambió configuración del SO. No quedó aquel contenedor fallido.

Las fixtures crean/restablecen datos sintéticos únicamente en este servidor nuevo y descartable. Se ejecutaron creación de esquema y migraciones del fixture **solo en esa BD temporal**, sin modificar archivos de migración ni bases existentes. Ningún dato operativo fue usado. `OSRM_BASE_URL` vacío, por lo que no se validó red vial externa. Al terminar se detuvo exclusivamente el contenedor creado aquí; `--rm` retiró su infraestructura temporal. No se eliminaron archivos preexistentes.

Bytecode y caché pytest deshabilitados. Cobertura, JUnit, temporales y resultados de frontend quedaron en [FASES_3_4_5_EVIDENCIAS](FASES_3_4_5_EVIDENCIAS/). Vitest utilizó configLoader runner, sin modificar configuraciones, caché de resultados/módulos deshabilitada y cacheDir Vite dentro de esa carpeta. No se ejecutó build.

## 2. Resultados ejecutados ahora

| ID | Comprobación | Aprobadas / fallidas / omitidas | Alcance real |
|---|---|---|---|
| CMD-01 | Suite backend completa, pytest/PostGIS aislado | **185 / 0 / 0**; 59,08 s de suite | Unidad e integración API/BD y WS TestClient. No es navegador E2 E. |
| CMD-01-B08 | Subconjunto nuevo PostGIS B-08, incluido en CMD-01 | **14 / 0 / 0**, no sumar otra vez | Rechazos de peso/volumen/ventana/jornada/omisión, rollback, cancelación y notificación tras commit. |
| CMD-02 | Suite frontend completa, Vitest/jsdom/node y mocks | **68 / 1 / 0**, 69 casos | Componentes y unidades, no API/BD real desde navegador. |
| CMD-03 | TypeScript `tsc --noEmit --incremental false` | Salida 0 | Tipado; no ejecución funcional. |
| CMD-04 | `node --test scripts/test-service-worker.mjs` | **4 / 0 / 0** | SW en VM y cachés en memoria; no offline de campo. |
| CMD-05 | `node scripts/audit-green-build.mjs` | Aprobado | `dist` preexistente: 434.872 B JS/CSS, sin reconstrucción; no prueba qué está desplegado. |
| CMD-06 | Medición adicional solver 150 ×15, semillas 901001/2/3 | Tres ejecuciones; **0 soluciones factibles** | Geodesia, sin HTTP/BD/OSRM; no acredita SLA extremo a extremo. |

Los 258 casos automáticos backend+frontend+SW producen **257 aprobados y 1 fallido**; los 14 B-08 ya están dentro de los 185. No se usa esta proporción como porcentaje de requisitos aceptados ni como EV.

La ejecución actual elimina el bloqueo de infraestructura que dejó 14 casos B-08 sin verificar en el informe de fase 2. Ese informe histórico se conserva sin reescribir. Ahora esos catorce casos específicos sí están aprobados con BD real; esto no acepta todo el MVP ni cierra los demás defectos.

### Fallo actual DEF-01

`src/pages/fleet.test.tsx:65`, caso `loads fleet, validates maintenance and saves edits`: esperaba `fetchVehicleHistory(1)` y recibió **(1, 21)**. La pantalla pagina historial (`src/pages/Fleet.tsx:108`) y la firma de API acepta límite (`src/api.ts:178`). Existe una desalineación entre aserción y llamada actual; no se probó a partir de ello un fallo productivo de paginación. La prueba se detiene antes de completar sus comprobaciones posteriores de mantenimiento/edición. No se corrigió prueba ni pantalla: las fases 3–5 prohíben cambios de código.

Avisos: Starlette depreca uso de httpx con TestClient; jsdom indica navegación a otro documento no implementada. No son certificación de fallos reales del navegador ni motivo para instalar bibliotecas aquí. El fallo de flota sí hace que Vitest termine con salida 1.

## 3. Cobertura de esta corrida

| Capa / métrica | Numerador / denominador | Resultado |
|---|---:|---:|
| Backend líneas/sentencias | 3773 / 4531 | **83,27 %** |
| Backend ramas | 667 / 1112 | **59,98 %** |
| Backend combinado líneas+ramas | 4440 / 5643 | **78,68 %** |
| Frontend líneas | 1026 / 1302 | **78,80 %** |
| Frontend sentencias | 1100 / 1433 | **76,76 %** |
| Frontend ramas | 873 / 1233 | **70,80 %** |
| Frontend funciones | 316 / 413 | **76,51 %** |

Fuentes: `backend_coverage.json/xml` y `frontend_coverage/coverage-summary.json`. Backend omite `app/db/init_db.py` según configuración vigente; frontend incluye código de producción de src conforme al config existente. Cobertura frontend se emitió incluso con el caso fallido. DoD histórica exige ≥80 % por capa sin precisar todas las modalidades: líneas backend superan 80 %, frontend queda **1,20 puntos porcentuales por debajo**; combinado backend queda 1,32 puntos por debajo si esa fuera la métrica acordada. No se impuso un umbral nuevo ni se presentó el gate actual como suficiente. Resultados Sonar/coberturas históricas con otros cortes no son comparaciones equivalentes.

## 4. Rendimiento y flujo integrado

[benchmark_solver_actual.json](FASES_3_4_5_EVIDENCIAS/benchmark_solver_actual.json): dataset `synthetic_orders(150,seed=901001)`, 15 vehículos del generador con la misma semilla, GA 32 generaciones/población 24; semillas de búsqueda 901001/901002/901003. Tiempos de llamada 0,9723/0,9823/0,9038 s, 150 asignados en las tres, pero retrasos agregados de 1974,55/1904,01/2258,50 minutos y `feasible=false`. No hay solución testigo independiente que garantice factibilidad de ese dataset: no se concluye que el solver no pueda resolver cualquier instancia 150 ×15. Sí se concluye que **estos resultados no cumplen una entrega válida**.

Los cuatro tests `test_solver_sla_en001.py` aprobaron sus propias aserciones, pero el test SLA solo exige tiempo/alguna asignación; no prueba 150/150 factibles ni latencia HTTP. **SLA válido 150 ×15 ≤45 s y recálculo <30 s: no acreditados**. No se midieron 1000 pedidos/50 vehículos ni disponibilidad 99,5 %.

Trazabilidad del flujo: Pedido/validación→optimización→persistencia→mapa están cubiertos parcialmente por integración API/PostGIS; conductor/entrega y PDF tienen casos API separados. Componentes UI/IndexedDB se prueban con mocks. No se observó una sesión continua en navegador **Pedido→Validación→Optimización→Persistencia→Mapa→Conductor→Entrega→Indicadores→PDF**. Tampoco OSRM real, caída de red real, comprobante durable ni usuarios objetivo. No se declara E2 E ni aceptación de RF completo.

## 5. Casos individuales y comandos reproducibles

[casos_prueba.json](FASES_3_4_5_EVIDENCIAS/casos_prueba.json) registra **254 casos individuales** backend/frontend con ID, RF/RNF orientativo, precondición, selección/comando, esperado, observado, estado, fuente, evidencia, defecto y fecha. El mapeo de familias de tests es orientativo; la aceptación integral se evalúa en [SPRINT 4_MATRIZ_ACEPTACION.md](SPRINT4_MATRIZ_ACEPTACION.md), no por conteo. Las cuatro pruebas SW están identificadas por su nombre en el script fuente y salida CMD-04.

CMD-01 (variables solo del proceso; DATABASE_URL debe apuntar al contenedor nuevo con credenciales efímeras, omitidas de este informe):

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OSRM_BASE_URL=''
$env:EN001_WRITE='0'
$env:COVERAGE_FILE=(Join-Path (Get-Location) 'AUDITORIA\FASES_3_4_5_EVIDENCIAS\coverage_backend_data')
& '.venv\Scripts\python.exe' -B -m pytest -o addopts= -p no:cacheprovider --basetemp=AUDITORIA/FASES_3_4_5_EVIDENCIAS/pytest-tmp --cov=app --cov-report=term --cov-report=json:AUDITORIA/FASES_3_4_5_EVIDENCIAS/backend_coverage.json --cov-report=xml:AUDITORIA/FASES_3_4_5_EVIDENCIAS/backend_coverage.xml --cov-fail-under=0 --junitxml=AUDITORIA/FASES_3_4_5_EVIDENCIAS/backend_junit.xml -ra
```

Es el comando efectivamente usado, con salida registrada en `backend_pytest.log`. Para otra corrida deben elegirse destinos **nuevos/versionados**, porque pytest puede limpiar su basetemp y no se autoriza sobrescribir evidencia anterior. No usar DB de trabajo ni productiva: las fixtures hacen TRUNCATE. La infraestructura de esta corrida ya se detuvo.

CMD-02 invocó `startVitest('test', [], options, viteOverrides)` de la versión local con: run=true, config=`vitest.config.ts`, configLoader=`runner`, cache=false, fsModuleCache=false, maxWorkers=2, update=`none`, reporters default/json; outputFile JSON, attachments, fsModuleCachePath, cacheDir Vite y coverage.reportsDirectory dentro de `AUDITORIA/FASES_3_4_5_EVIDENCIAS`. Cobertura V8 habilitada y reportOnFailure=true. [frontend_vitest.log](FASES_3_4_5_EVIDENCIAS/frontend_vitest.log) y [frontend_results.json](FASES_3_4_5_EVIDENCIAS/frontend_results.json) preservan el resultado. No se usó `npm ci` ni se alteró el config.

CMD-03/04/05 son los comandos de §2 ejecutados con recursos existentes. CMD-06 llamó directamente a `solve_vrptw` con generaciones/población obtenidas por `resolve_ga_parameters`, presupuesto de 45 s, matriz geodésica, datos/semillas registrados en su JSON. No creó rutas persistidas.

## 6. Límites y salida de fase 3

No se ejecutaron nuevo Sonar/SCA, escaneo completo OWASP, axe/Lighthouse, lector de pantalla, benchmark HTTP con OSRM, E2 E navegador, aceptación de interesados ni medición de disponibilidad. No se certifican normas. Las pruebas de roles aprobadas no cubren por sí solas los defectos de autorización histórica y privacidad WS aún visibles.

Los cuatro informes de fase 3 existen, con resultados actuales y fuentes distinguibles. **Puerta 3→4 habilitada solo para redactar borradores verificables**, conforme al archivo maestro. Fallo frontend, brechas de seguridad, aceptación incompleta, EVM sin registros y SLA sin demostrar bloquean un cierre técnico/administrativo aprobado y una demo presentada como íntegramente aceptada. No se corrige código ni se ignoran esos bloqueos al continuar documentación.
