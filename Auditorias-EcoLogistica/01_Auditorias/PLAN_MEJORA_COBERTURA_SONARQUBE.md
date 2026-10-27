# Plan de mejora de cobertura y calidad SonarQube

**Proyecto:** EcoLogística Huancayo  
**Fecha de diagnóstico:** 27 de octubre de 2026  
**Base analizada:** revisión Git `564a90916240569f0072b14af6001b71c9f1f0c8`, con la corrección local `relative_files = true` para Coverage.py.  
**Restricción aplicada:** este diagnóstico no modifica código funcional, pruebas, reglas de negocio, base de datos, exclusiones ni umbrales.

## 1. Resumen ejecutivo

El último análisis procesado correctamente por SonarQube reporta **61.4% de cobertura global**, **62.8% de líneas**, **53.7% de condiciones** y **0.0% de duplicación**. El Quality Gate está en **ERROR** porque la cobertura de código nuevo es **52.9%**, inferior al umbral vigente de 80%.

La cobertura global se calcula sobre **5,583 líneas cubribles y 1,072 condiciones**. Actualmente quedan sin cubrir **2,075 líneas y 496 condiciones**. Para alcanzar 80% con el mismo conjunto de código serían necesarios, aproximadamente, **1,240 elementos adicionales cubiertos entre líneas y condiciones**. Esta cifra es aritmética; la cantidad real de pruebas necesaria depende de cuántas rutas ejecute cada caso.

Los reportes verificados muestran:

- Backend: 124 pruebas recopiladas. Coverage.py informa **80.31% de sentencias**, **53.35% de ramas** y **75.05% combinado**.
- Frontend: 6 pruebas aprobadas en 2 archivos. Vitest informa **12.98% de líneas** dentro de su alcance instrumentado actual.
- SonarQube: **61.4% global**, después de importar `coverage.xml` y `coverage/frontend/lcov.info` desde `/usr/src`.
- Alcance: 56 archivos Python de aplicación, 28 archivos TypeScript/TSX, 22 archivos de pruebas Python y 2 archivos de pruebas TypeScript.

Llegar a 80% es técnicamente viable, pero requiere trabajo en ambos lados. El mayor retorno inmediato está en funciones frontend puras y clientes HTTP; el mayor retorno asociado a riesgo de negocio está en WebSockets, rutas API, autenticación y operaciones de flota/restricciones.

## 2. Evidencia y configuración revisadas

### 2.1 Backend

Pytest se configura en `pyproject.toml` con `--cov=app`, cobertura de ramas y salida Cobertura en `coverage.xml`. La opción `relative_files = true` produce `<source>app</source>`, que permite a SonarScanner resolver correctamente los archivos desde `/usr/src`.

El reporte actual contiene 4,306 sentencias y 1,044 ramas. La cobertura de sentencias ya supera 80%, pero la cobertura combinada baja a 75.05% debido a 487 ramas no cubiertas.

### 2.2 Frontend

Vitest usa V8 y genera `lcov.info` y `coverage-summary.json`. La configuración actual instrumenta únicamente:

```text
src/lib/**/*.ts
```

SonarQube, en cambio, mide todo `src`, incluido `src/api.ts`, páginas y componentes TSX. Por ello, gran parte del frontend aparece correctamente como código sin cobertura. Para que nuevas pruebas de componentes y API sean contabilizadas, la instrumentación futura debe abarcar `src/**/*.{ts,tsx}`, conservando la exclusión de archivos de prueba. Este cambio no debe utilizarse para excluir archivos productivos.

### 2.3 Acceso desde SonarScanner

Se verificó desde la imagen oficial del escáner que ambos reportes existen y tienen contenido en:

```text
/usr/src/coverage.xml
/usr/src/coverage/frontend/lcov.info
```

El escaneo final registró explícitamente la lectura de ambos reportes y terminó con `SUCCESS`, sin advertencias de procesamiento.

## 3. Diagnóstico de cobertura

### 3.1 Backend: principales brechas

| Archivo | Cobertura actual | Evidencia de brecha |
|---|---:|---|
| `app/api/v1/websockets.py` | 38.3% | 194 líneas y 99 ramas sin cubrir; `_reroute`, `_apply_reroute`, `_on_incident`, `_on_cancel` y `_on_add` están esencialmente sin probar. |
| `app/api/v1/routes.py` | 52.4% | 167 líneas y 86 ramas sin cubrir; faltan escenarios de creación, confirmación de entrega, optimización, alcance vehicular y errores. |
| `app/api/v1/desk.py` | 55.9% | `update_vehicle` tiene 7.1% y `create_vehicle` 26.3%; faltan variantes de validación y auditoría. |
| `app/api/v1/plate_restrictions.py` | 40.8% | `update_plate_restrictions` tiene 5.2%; faltan combinaciones de reglas, cambios, validación y reemplazo. |
| `app/services/access.py` | 44.0% | `authenticate` tiene 14.3%; faltan usuario inexistente, contraseña incorrecta, bloqueo, inactivo y hash de tiempo constante. |
| `app/services/sequence_eta.py` | 43.8% | `recalculate_solution_etas` tiene 24.1%; 23 líneas y 18 ramas pendientes. |
| `app/core/emissions.py` | 33.3% | `altitude_emission_factor` y `leg_co2_grams` están en 0%; faltan límites, ascenso, descenso y combustibles. |
| `app/core/geo.py` | 51.2% | `linestring_geojson` y `linestring_wkt` están en 0%; faltan geometrías válidas, vacías y formatos alternativos. |
| `app/services/order_import.py` | 70.0% | 74 líneas y 40 ramas sin cubrir; faltan errores y combinaciones de importación menos frecuentes. |
| `app/services/realtime_router.py` | 80.6% | Buen nivel de líneas, pero conserva 24 ramas no cubiertas en incidentes y recálculo. |

Las pruebas actuales cubren bien el optimizador, restricciones duras, importación básica, geocodificación, estados vehiculares, autenticación de API y reglas de placa. La principal debilidad es la profundidad de ramas y estados alternativos, no la ausencia total de pruebas backend.

### 3.2 Frontend: principales brechas

| Archivo | Cobertura Sonar actual | Brecha principal |
|---|---:|---|
| `src/components/driver/DriverApp.tsx` | 0.0% | 221 líneas sin cubrir; modo offline, sincronización, entrega, errores y reconexión. |
| `src/lib/format.ts` | 0.0% | 114 líneas; formatos horarios, estados, etiquetas, CO₂ y límites. |
| `src/pages/OrdersDay.tsx` | 0.0% | 109 líneas; carga/importación, errores, edición y estados de UI. |
| `src/pages/Tracking.tsx` | 0.0% | 104 líneas; carga, seguimiento público/interno y errores. |
| `src/pages/Fleet.tsx` | 0.0% | 91 líneas; alta, edición, transición de estado y permisos. |
| `src/api.ts` | 0.0% | 82 líneas cubribles; manejo de respuestas, 401/403/404, errores y descarga PDF. |
| `src/lib/access.ts` | 2.5% | 79 de 80 líneas sin cubrir; matriz de permisos por rol. |
| `src/lib/session.ts` | 3.2% | 61 de 62 líneas sin cubrir; persistencia, recuperación, corrupción y limpieza de sesión. |
| `src/lib/offline.ts` | 3.8% | 51 de 52 líneas sin cubrir; IndexedDB, deduplicación, cola y errores de transacción. |
| `src/App.tsx` | 0.0% | 67 líneas; protección y selección de rutas según sesión/rol. |

Las únicas pruebas frontend cubren parcialmente `orderWindow.ts` y `routePresentation.ts`. No existen pruebas del cliente HTTP ni pruebas de componentes. Para componentes se requerirá un entorno DOM de pruebas y utilidades de renderizado; esto debe incorporarse como infraestructura de prueba, sin cambiar el comportamiento de producción.

## 4. Seguridad, confiabilidad y mantenibilidad

SonarQube mantiene **30 incidencias abiertas**: 16 bugs, 10 vulnerabilidades y 4 code smells. Su distribución es 1 bloqueante, 3 críticas, 25 mayores y 1 menor.

### 4.1 Confiabilidad

- `app/main.py:68`, regla `python:S930`: Sonar considera inesperado `summary` en `get_openapi`. La firma instalada de FastAPI sí acepta `summary`; la aplicación y sus pruebas funcionan. Debe validarse como falso positivo dependiente del modelo de tipos/versión y documentarse antes de marcarlo en Sonar. No se recomienda retirar el argumento sin revisar el contrato OpenAPI.
- Tres incidencias críticas `typescript:S2871` en `Sidebar.tsx`, `Map.tsx` y `PlateRestrictions.tsx`: los `sort()` necesitan comparadores explícitos, usando `localeCompare` para texto o comparación numérica para números. Deben acompañarse de pruebas de ordenamiento con datos ambiguos.
- Doce incidencias mayores `python:S1244`: comparaciones exactas de flotantes en `route_constraints.py` y `genetic_solver.py`. Deben revisarse por semántica: tolerancia con `math.isclose` cuando se trate de cálculos, o conservar igualdad solo si representa un centinela normalizado y queda justificado por pruebas.

### 4.2 Seguridad

- Nueve incidencias `python:S2245` corresponden a `random.Random` en el algoritmo genético y en datos sintéticos de benchmark. No se usan para claves, tokens o decisiones criptográficas y la reproducibilidad por semilla es deliberada. Requieren revisión y justificación de seguridad; sustituirlos automáticamente por `secrets` podría romper reproducibilidad y rendimiento.
- Una incidencia `python:S5332` identifica HTTP en orígenes locales predeterminados. Debe verificarse que producción fuerce HTTPS y no herede valores de desarrollo. Conviene probar explícitamente la configuración de producción.
- No hay Security Hotspots reportados, pero este dato no reemplaza análisis de dependencias, autorización por objeto, secretos o pruebas dinámicas.

### 4.3 Mantenibilidad

- Cuatro incidencias `typescript:S6671` en `offline.ts`: los rechazos de IndexedDB pueden entregar `null` u objetos que no son `Error`. Deben normalizarse a `Error` y probarse los fallos de apertura, lectura, escritura y limpieza.
- SonarQube reporta 0.0% de duplicación. No se recomienda refactorizar solo para mejorar una métrica que ya cumple.

## 5. Plan priorizado

Los incrementos son **estimaciones**, no resultados comprobados. Se expresan como puntos porcentuales potenciales sobre la cobertura global de Sonar, suponiendo que las pruebas ejerciten una parte razonable de las líneas y ramas señaladas. Solo un nuevo escaneo puede confirmar el resultado.

| Archivo o módulo | Cobertura actual | Funcionalidad a probar | Tipo recomendado | Prioridad | Dificultad | Riesgo funcional | Incremento potencial estimado |
|---|---:|---|---|---|---|---|---:|
| `src/lib/format.ts`, `access.ts`, `session.ts` | 0–3.2% | Formatos/límites, matriz completa de roles, sesión válida/corrupta/expirada | Unitarias parametrizadas con reloj y storage simulados | P0 | Baja | Bajo | +3.0 a +3.8 pp |
| `src/api.ts` | 0.0% | Métodos HTTP, cuerpo, cabeceras, errores, 404 opcional, descarga PDF | Unitarias con `fetch` simulado | P0 | Media | Bajo | +0.8 a +1.2 pp |
| `app/services/access.py` | 44.0% | Autenticación, bloqueo, usuario inactivo y contraseña inválida | Unitarias e integración de servicio | P0 | Media | Medio | +0.4 a +0.6 pp |
| `app/api/v1/routes.py` | 52.4% | Confirmación de entrega, optimización, errores y alcance por vehículo | Integración API con PostGIS y dobles controlados | P0 | Alta | Medio | +1.7 a +2.3 pp |
| `app/api/v1/websockets.py` | 38.3% | Incidente, cancelación, alta prioritaria, reroute y snapshot | Integración WebSocket + unitarias de helpers | P0 | Alta | Alto | +2.0 a +2.8 pp |
| `src/lib/offline.ts` | 3.8% | IndexedDB, cola idempotente, completados y errores | Unitarias con IndexedDB simulado | P1 | Media | Medio | +0.5 a +0.8 pp |
| `src/components/driver/DriverApp.tsx` | 0.0% | Online/offline, sincronización, entrega y recuperación de errores | Componentes con DOM, API e IndexedDB simulados | P1 | Alta | Alto | +1.8 a +2.5 pp |
| `src/pages/OrdersDay.tsx`, `Tracking.tsx`, `Fleet.tsx` | 0.0% | Estados de carga/error/éxito, formularios, permisos y actualizaciones | Componentes e integración frontend | P1 | Alta | Medio | +2.5 a +3.5 pp |
| `app/api/v1/desk.py` y `plate_restrictions.py` | 40.8–55.9% | Actualización vehicular, historial, reemplazo y validación de reglas | Integración API parametrizada | P1 | Media | Medio | +1.0 a +1.5 pp |
| `app/services/sequence_eta.py` | 43.8% | Matrices incompletas, secuencias, esperas y datos inválidos | Unitarias parametrizadas | P1 | Media | Medio | +0.4 a +0.6 pp |
| `app/core/emissions.py` y `geo.py` | 33.3–51.2% | Ascenso/descenso, límites, combustibles y geometrías | Unitarias de tabla y propiedades | P1 | Baja | Bajo | +0.5 a +0.8 pp |
| `app/services/order_import.py` | 70.0% | Codificaciones, columnas opcionales, duplicados cruzados y fallos parciales | Unitarias + integración CSV/XLSX | P2 | Media | Medio | +0.8 a +1.2 pp |
| `src/App.tsx`, navegación y componentes auxiliares | 0.0% | Protección de rutas, redirección y permisos visibles | Integración de componentes/router | P2 | Media | Medio | +1.0 a +1.8 pp |
| Incidencias Sonar de ordenamiento/flotantes | No aplica | Orden determinista y tolerancias numéricas | Regresión unitaria antes de corregir | P0 | Media | Alto si se corrige sin prueba | Mejora de ratings; cobertura marginal |
| Configuración de producción | Parcial | HTTPS, CORS, secretos por defecto y cuentas demo | Pruebas de configuración/arranque | P0 | Media | Bajo | Cobertura marginal; alto valor de seguridad |

## 6. Etapas de implementación

### Etapa 0 — Alinear medición y línea base

1. Mantener `relative_files = true` para Cobertura Python.
2. Ampliar la instrumentación Vitest a todo el código productivo `src/**/*.{ts,tsx}` sin excluir componentes o páginas.
3. Incorporar entorno DOM y utilidades de prueba frontend.
4. Ejecutar backend, frontend y Sonar; archivar la línea base. Es posible que la métrica frontend de Vitest inicialmente baje al medir todo `src`; esto representa una medición más honesta, no una regresión.

### Etapa 1 — Ganancias rápidas y protección de seguridad

1. Añadir pruebas exhaustivas de `format.ts`, `access.ts`, `session.ts` y `api.ts`.
2. Añadir pruebas de `emissions.py`, `geo.py` y autenticación de servicio.
3. Añadir pruebas de configuración de producción: secreto no predeterminado, demo deshabilitado, HTTPS y CORS.
4. Crear pruebas de regresión para los tres ordenamientos críticos antes de corregirlos.

**Resultado estimado:** +5 a +7 puntos globales, sujeto a escaneo.

### Etapa 2 — Flujos backend críticos

1. Cubrir los manejadores WebSocket de incidente, cancelación, alta y reruteo.
2. Cubrir confirmación de entrega, optimización y excepciones de `routes.py`.
3. Completar actualización vehicular y reglas de placa.
4. Completar ETA y ramas de importación.

**Resultado estimado acumulado:** +10 a +14 puntos globales desde la línea base.

### Etapa 3 — UI operativa y modo offline

1. Probar `offline.ts` con IndexedDB simulado y errores reales.
2. Probar `DriverApp.tsx` en modo online/offline y sincronización.
3. Probar `OrdersDay`, `Tracking`, `Fleet` y protección de rutas.
4. Incluir accesibilidad básica: roles, nombres accesibles, foco y mensajes de error.

**Resultado estimado acumulado:** +17 a +21 puntos. Este rango haría viable alcanzar 80%, pero debe confirmarse módulo por módulo.

### Etapa 4 — Remediación Sonar y endurecimiento

1. Corregir bugs solamente después de disponer de pruebas de regresión.
2. Revisar y clasificar los usos no criptográficos de `random.Random` con justificación documentada.
3. Validar el posible falso positivo de `get_openapi` contra la versión fijada de FastAPI.
4. Corregir rechazos de promesas a instancias de `Error` y comparaciones de flotantes donde corresponda.
5. Repetir análisis de dependencias y pruebas de configuración de producción.

## 7. Orden recomendado de ejecución

1. Instrumentación frontend completa y pruebas de utilidades/API.
2. Pruebas de regresión para incidencias bloqueante/críticas y configuración de seguridad.
3. WebSockets y `routes.py`, por impacto combinado en cobertura y riesgo operativo.
4. Modo offline y `DriverApp`.
5. Páginas operativas y ramas residuales backend.
6. Nuevo análisis Sonar al final de cada etapa, sin esperar a completar todo el plan.

## 8. Criterios de aceptación

- Todas las pruebas existentes y nuevas son verdes y verifican resultados observables.
- `coverage.xml` y `lcov.info` se generan desde fuentes vigentes y Sonar los importa sin advertencias.
- Cobertura global y cobertura de código nuevo alcanzan el umbral acordado sin exclusiones artificiales.
- Ningún bug bloqueante o crítico se cierra sin prueba de regresión o justificación reproducible.
- Vulnerabilidades revisadas con evidencia de contexto; los falsos positivos se documentan, no se ocultan mediante exclusiones.
- La aplicación construye y conserva sus contratos API, reglas de negocio y comportamiento de base de datos.

## 9. Actualización de implementación — 27 de octubre de 2026

### 9.1 Alcance implementado

Se ejecutaron primero los cambios P0/P1 de bajo riesgo y alto retorno. No se modificaron reglas de negocio ni funcionalidades productivas.

- Se amplió la instrumentación Vitest de `src/lib/**/*.ts` a `src/**/*.{ts,tsx}` para medir el mismo código productivo que SonarQube.
- Se excluyeron únicamente archivos de prueba y declaraciones `*.d.ts`, que no contienen runtime.
- SonarQube fue configurado para reconocer `*.test.tsx` como pruebas y no como código productivo.
- Se añadieron dependencias de desarrollo para pruebas DOM e IndexedDB: Testing Library, jsdom y fake-indexeddb.
- Se agregaron pruebas frontend de formatos, permisos, sesión, cliente HTTP, IndexedDB, componentes comunes, indicadores, login, bitácora y flota.
- Se agregaron pruebas backend de emisiones, geometrías y límites de configuración.

### 9.2 Archivos de pruebas agregados

- `src/api.test.ts`
- `src/lib/access.test.ts`
- `src/lib/format.test.ts`
- `src/lib/offline.test.ts`
- `src/lib/session.test.ts`
- `src/components/uiFlows.test.tsx`
- `src/pages/fleet.test.tsx`
- `tests/test_core_quality_units.py`

Configuraciones actualizadas:

- `vitest.config.ts`
- `sonar-project.properties`
- `package.json` y `package-lock.json`
- `pyproject.toml` conserva la corrección portable `relative_files = true` realizada antes de esta etapa.

### 9.3 Resultados comprobados

| Métrica | Línea base | Resultado final | Variación |
|---|---:|---:|---:|
| Pruebas frontend | 6 | 45 | +39 |
| Cobertura frontend de líneas | 12.98% sobre solo `src/lib` | 37.02% sobre todo `src` | No comparable directamente; el alcance final es mucho mayor |
| Funciones frontend | 77.77% sobre `src/lib` | 80.68% sobre todo `src` | Alcance ampliado |
| Ramas frontend | 67.85% sobre `src/lib` | 82.71% sobre todo `src` | +14.86 pp con alcance ampliado |
| Pruebas backend | 124 | 136 | +12 |
| Sentencias backend | 80.31% | 81.07% | +0.76 pp |
| Ramas backend | 53.35% | 55.17% | +1.82 pp |
| Cobertura backend combinada | 75.05% | 76.02% | +0.97 pp |
| SonarQube global | 61.4% | 62.0% | +0.6 pp |
| Líneas SonarQube | 62.8% | 61.7% | -1.1 pp por ampliación del denominador frontend |
| Ramas SonarQube | 53.7% | 63.2% | +9.5 pp |
| Cobertura de código nuevo | 52.9% | 65.3% | +12.4 pp |
| Duplicación | 0.0% | 0.0% | Sin cambio |

El descenso aparente de cobertura de líneas de Sonar no representa pérdida de pruebas: al instrumentar todo `src`, las líneas cubribles aumentaron de 5,583 a 7,675. Antes, numerosos componentes TSX eran marcados por el sensor de cobertura cero con una granularidad menor; LCOV ahora informa todas sus líneas ejecutables. La medición final es más completa y reproducible.

### 9.4 Validaciones ejecutadas

- Backend completo: **136 passed**, una advertencia deprecada de Starlette/httpx, sin fallos.
- Frontend completo: **45 passed**, sin fallos.
- TypeScript y Vite: build de producción aprobado.
- SonarScanner: análisis procesado con éxito; ambos reportes fueron importados.
- Dependencias de producción frontend: `npm audit --omit=dev` reportó 0 vulnerabilidades.

El audit completo reporta incidencias en herramientas de desarrollo Vite/Vitest. Algunas correcciones requieren un salto mayor a Vitest 5, por lo que no se aplicó una actualización automática de alto riesgo dentro de esta etapa. Debe planificarse una migración separada y validarse contra toda la suite.

### 9.5 Motivo para detener el incremento antes de 80%

Alcanzar 80% exige cubrir principalmente:

- `src/components/driver/DriverApp.tsx`: flujo offline, sincronización, WebSocket y confirmación de entrega.
- `src/pages/OrdersDay.tsx`: importación CSV/XLSX, edición de ventanas y geolocalización.
- `src/pages/Tracking.tsx`: Leaflet, WebSocket, alertas y seguimiento público.
- `src/components/Map.tsx` y `Sidebar.tsx`: mapas, selección y ordenamiento.
- `app/api/v1/websockets.py` y `app/api/v1/routes.py`: persistencia, reruteo y errores operativos.

Estos módulos combinan mapas, sockets, IndexedDB, PostGIS y reglas operativas. Cubrirlos de forma real requiere infraestructura de integración más compleja y cambios de riesgo medio/alto en los dobles de prueba. Conforme a la restricción solicitada, no se añadieron pruebas superficiales ni se modificó producción para facilitar el porcentaje. Se recomienda continuar en una etapa específica de integración, con casos de aceptación por flujo y un escaneo después de cada módulo.

## 10. Ampliación específica del frontend — 27 de octubre de 2026

Se implementó un segundo bloque de pruebas de comportamiento, sin modificar código productivo:

- `src/pages/operations.test.tsx`: importación de jornada, resolución de ubicación, edición de ventana, permisos de auditor, errores de API y reglas de restricción vehicular.
- `src/pages/tracking.test.tsx`: carga pública, errores, token inválido, actualización WebSocket, ETA, ubicación, paradas y alertas por canal.
- `src/App.test.tsx`: carga del despacho, optimización, errores, actualización WebSocket y alternativa tabular al mapa.
- `src/components/Sidebar.test.tsx`: estados de carga/lectura/optimización, advertencias e itinerarios ordenados.

Resultados verificados con `npm run test:coverage`:

| Métrica frontend | Antes del bloque | Después del bloque | Variación |
|---|---:|---:|---:|
| Pruebas | 45 | 58 | +13 |
| Cobertura de líneas | 37.02% | 69.18% | +32.16 pp |
| Cobertura de ramas | 82.71% | 84.52% | +1.81 pp |
| Cobertura de funciones | 80.68% | 81.09% | +0.41 pp |
| Cobertura de páginas | 45.96% aprox. | 90.23% | mejora sustancial |

También se ejecutó `npm run build`: TypeScript y Vite finalizaron correctamente. Los principales módulos pendientes son `DriverApp.tsx`, `Map.tsx`, `PinMap.tsx` y el punto de entrada `main.tsx`. Alcanzar el 80% global frontend exige cubrir sobre todo `DriverApp`, cuyo flujo integra geolocalización, WebSocket, sincronización offline e IndexedDB; se recomienda tratarlo como una etapa de integración separada para evitar pruebas superficiales o cambios de alto riesgo.

## 11. Implementación de pruebas del modo conductor — 27 de octubre de 2026

Se agregó `src/components/driver/DriverApp.test.tsx` con cinco escenarios de comportamiento:

- carga de vehículo, ruta activa e itinerario;
- registro de evidencia y confirmación de entrega;
- cola offline y sincronización con el backend;
- recuperación de flota y ruta desde caché cuando falla la red;
- geolocalización, incidentes y mensajes WebSocket del despacho.

No se modificó `DriverApp.tsx` ni ninguna regla de negocio. Resultados verificados:

| Métrica frontend | Antes | Después | Variación |
|---|---:|---:|---:|
| Pruebas | 58 | 63 | +5 |
| Cobertura de líneas global | 69.18% | 83.01% | +13.83 pp |
| Cobertura de ramas global | 84.52% | 83.90% | -0.62 pp por incorporación de ramas complejas del conductor |
| Cobertura de funciones global | 81.09% | 78.69% | -2.40 pp por funciones internas ahora instrumentadas |
| Líneas de `DriverApp.tsx` | 0% | 85.34% | +85.34 pp |
| Ramas de `DriverApp.tsx` | 0% | 80.13% | +80.13 pp |

La suite frontend completa finalizó con **63 pruebas aprobadas de 63**. El build TypeScript/Vite también finalizó correctamente y `coverage/lcov.info` quedó regenerado para el siguiente análisis de SonarQube.

## 12. Implementación de pruebas cartográficas — 27 de octubre de 2026

Se agregó `src/components/maps.test.tsx` con cuatro escenarios para `Map.tsx` y `PinMap.tsx`:

- depósito y pedidos todavía no asignados a una ruta;
- trazado vial, rutas optimizadas, marcadores y selección de paradas;
- filtrado por placa, ajuste automático de límites y advertencia cuando OSRM no entrega geometría;
- errores de teselas y selección manual de coordenadas en el mapa de ubicación.

Los dobles de Leaflet se limitaron al motor de renderizado del navegador; las pruebas verifican callbacks, datos, conversiones de coordenadas y comportamiento observable de los componentes.

| Métrica frontend | Antes | Después | Variación |
|---|---:|---:|---:|
| Pruebas | 63 | 67 | +4 |
| Cobertura de líneas global | 83.01% | 90.91% | +7.90 pp |
| Cobertura de ramas global | 83.90% | 84.52% | +0.62 pp |
| Cobertura de funciones global | 78.69% | 80.65% | +1.96 pp |
| Líneas de `Map.tsx` | 0% | 98.34% | +98.34 pp |
| Ramas de `Map.tsx` | 0% | 87.65% | +87.65 pp |
| `PinMap.tsx` | 0% | 100% | +100 pp |

La suite completa terminó con **67 pruebas aprobadas de 67** y el build de producción finalizó correctamente. Se regeneró `coverage/lcov.info`; no se modificaron componentes productivos, exclusiones ni umbrales.

