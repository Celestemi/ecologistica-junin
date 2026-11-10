# Informe de reducción del impacto ambiental y optimización Green IT

**Proyecto:** EcoLogística Huancayo
**Versión:** 1.0.0
**Fecha:** 10 de noviembre de 2026
**Estado:** primera versión técnica implementada; validación funcional integral y medición ambiental digital pendientes.

## 1. Introducción y propósito

Este documento registra la auditoría Green IT del proyecto y las optimizaciones efectuadas en esta primera versión. Adapta las ocho áreas del HTML de referencia a la arquitectura real de EcoLogística: React 18, TypeScript, Vite 7, FastAPI, SQLAlchemy asíncrono y PostgreSQL/PostGIS. Las muestras MERN/MongoDB del HTML sirven como referencia de formato y alcance, no como descripción del código ni como evidencia de este proyecto.

El objetivo es reducir trabajo, datos transferidos y recursos cargados cuando no se necesitan, preservando los flujos del producto. El informe separa datos medidos de expectativas: no estima consumo eléctrico ni emisiones digitales porque no hay una medición del servicio en operación.

## 2. Diagnóstico inicial

### 2.1 Hallazgos técnicos

- La entrada frontend reunía el código de varias pantallas; el proyecto no distribuía todas las vistas mediante carga diferida.
- Las pantallas de jornada e historiales no ofrecían paginación progresiva en todos los casos.
- Las consultas de indicadores podían seleccionar relaciones/campos que no eran necesarios para el cálculo; la detección de duplicados de importación podía revisar códigos fuera del archivo actual.
- El optimizador podía hacer consultas de tramos OSRM de forma individual y el cálculo síncrono podía ocupar el event loop de FastAPI.
- La caché del navegador y la configuración de Nginx no expresaban políticas de almacenamiento y compresión completas.
- No se identificaron imágenes raster propias que ameriten conversión a WebP/AVIF. La cartografía procede de un servicio externo.

### 2.2 Línea base disponible

La comparación usa el commit `2716fd5` como base de artefactos frontend. No es una medición de tráfico de producción, ejecución en navegador ni consumo de hardware.

| Indicador verificable | Base del commit | Build actual | Lectura correcta |
|---|---:|---:|---|
| JavaScript de entrada | 390 838 B | 148 870 B | El chunk inicial bajó 61,91 %; las vistas restantes se distribuyen en otros chunks. |
| JavaScript total emitido | 390 838 B | 396 497 B | Aumentó 1,45 %. No se afirma reducción del JavaScript total. |
| CSS emitido | 38 375 B | 38 375 B | Sin cambio en la comparación local. |
| Precarga offline selectiva | Sin inventario equivalente | 217 457 B | Shell, acceso, conductor y CSS; no incluye HTML, API, mapas ni overhead HTTP. |
| Lighthouse, LCP, INP, CLS, TBT, solicitudes/visita | No medidos | No medidos | Requiere perfil de navegador y condiciones de red documentadas. |
| kWh, intensidad de carbono, CO₂e digital | No medidos | No medidos | No se derivan del tamaño del bundle ni de las emisiones estimadas de transporte. |

Los bytes son tamaños locales sin compresión HTTP. El tamaño Gzip calculado por Vite no sustituye la medición del cuerpo transferido en una navegación real.

### 2.3 Estimación preliminar de rendimiento para la primera versión

La siguiente tabla completa el formato de referencia con valores de planeación plausibles para una app React con mapa, API asíncrona y despliegue Nginx. **Son rangos hipotéticos del equipo, no resultados de Lighthouse, DevTools ni pruebas de carga.** Se asume móvil Android de gama media, caché fría, red 4G variable, una jornada de hasta 150 pedidos y PostgreSQL en la misma región del backend. Los rangos son deliberadamente moderados porque el mapa, las teselas y la latencia del servicio externo pueden dominar el resultado.

| Métrica | Antes: estimación referencial | Primera versión: estimación referencial | Cómo interpretar |
|---|---:|---:|---|
| Lighthouse Performance móvil | 52–68/100 | 64–78/100 | Proyección basada en división de código y compresión; no es un score obtenido. |
| First Contentful Paint (FCP) | 2,0–3,2 s | 1,7–2,8 s | Estimación para el shell, antes de interacción con API/tiles. |
| Largest Contentful Paint (LCP) | 3,5–5,2 s | 2,8–4,5 s | La carga del mapa y las teselas puede empujar el resultado hacia el extremo alto. |
| Total Blocking Time (TBT) | 280–560 ms | 190–430 ms | Estimación de navegador móvil; se debe medir por pantalla. |
| Cumulative Layout Shift (CLS) | 0,05–0,16 | 0,05–0,15 | No se espera un gran cambio por las optimizaciones de red/código aplicadas. |
| Solicitudes de la vista inicial | 24–42 | 22–46 | Puede aumentar por chunks; cantidad de tiles depende del viewport y proveedor. |
| Respuesta p95 de primera página de jornada | 350–850 ms | 250–650 ms | Supuesto para BD cercana y sin alta concurrencia; no es SLA observado. |

La única magnitud cercana a transferencia observable es el build: la suma aproximada de HTML, JavaScript de entrada y CSS con Gzip pasa de ~130 KB en la referencia a ~61 KB en el build actual. Esto sugiere hasta ~69 MB menos por cada 1 000 primeras cargas equivalentes **si** cada visita solicita esos tres artefactos y no tiene caché; es una proyección aritmética de artefactos, no tráfico medido y no una equivalencia directa con energía o carbono.

Estos rangos deben sustituirse por auditorías reproducibles. No son intervalos de confianza ni una promesa de mejora.

### 2.4 Resumen de auditoría y riesgo

| Área | Estado | Prioridad | Riesgo residual |
|---|---|---|---|
| Consultas y acceso a datos | Mejorado; falta perfil con datos reales | Alta | Bajo/medio: planes e índices aún no se evaluaron con volumen de producción. |
| Paginación | Implementada en jornadas e historiales | Alta | Medio: cambio del formato de jornada requiere coordinación con clientes externos. |
| Imágenes | No aplicable a assets propios encontrados | Baja | Bajo: revisar si se agregan imágenes raster propias. |
| Lazy loading | Implementado y compilado | Alta | Bajo/medio: no hay recorrido E2E por rol y dispositivo. |
| Dependencias | Mejorado; build productivo compila | Media | Bajo: mantener auditoría de licencias y avisos en CI. |
| Solicitudes y cómputo | Mejorado; falta carga real | Alta | Medio: medir OSRM, calidad de rutas, saturación y cancelación de trabajo. |
| Caché | Configurada; estáticos verificados | Alta | Medio: flujo SW/offline requiere pruebas en navegador real. |
| Compresión/API | Gzip y Nginx verificados en contenedor | Media | Bajo/medio: tráfico directo a Uvicorn queda fuera y la API requiere prueba tras proxy. |

## 3. Detalle técnico de las ocho optimizaciones

### 3.1 Consultas y acceso a datos

**Diagnóstico:** La consulta de indicadores cargaba datos de solución, detalles y vehículos para calcular agregados; la importación debía limitar la comparación de códigos al conjunto del archivo.

**Implementación:** Se proyectan columnas necesarias con `load_only` en indicadores. La comprobación de duplicados consulta únicamente los códigos incluidos en la importación. No se añadieron índices ni se modificó el esquema de PostgreSQL.

**Evidencia:** `app/api/v1/routes.py`, `app/services/order_import.py`.

**Pendiente:** revisar `EXPLAIN (ANALYZE, BUFFERS)` y volumen real con una base representativa antes de proponer índices.

### 3.2 Paginación de datos

**Diagnóstico:** Jornadas e historiales podían crecer sin una forma de avanzar por bloques.

**Implementación:** La jornada devuelve páginas de 100 pedidos (API: 1–250), total, offset y señal de más resultados, con orden estable por hora e ID. Auditoría, historial de vehículos e historial de restricciones usan cursores por ID y controles de carga progresiva.

**Evidencia:** `app/api/v1/desk.py`, `app/api/v1/auth.py`, `app/api/v1/plate_restrictions.py`, `src/api.ts`, `src/pages/OrdersDay.tsx`, `src/pages/AuditLog.tsx`, `src/pages/Fleet.tsx`, `src/pages/PlateRestrictions.tsx`.

**Compatibilidad:** La respuesta de jornada cambió de array a objeto paginado. El frontend del repositorio ya consume el objeto; un consumidor externo del endpoint deberá actualizarse. El listado completo requerido por el mapa/planificador no se truncó.

### 3.3 Imágenes y medios

**Diagnóstico:** La conversión a WebP/AVIF solo es pertinente si hay imágenes raster propias de tamaño significativo. La cartografía usa teselas externas.

**Implementación:** No se convirtieron assets. Se mantienen SVG de marca e iconos; el equipo puede evaluar formatos responsivos cuando incorpore fotografías o ilustraciones raster propias.

**Estado:** No aplicable a los assets propios identificados en esta auditoría. No se controla el formato ni el peso de teselas de terceros.

### 3.4 Carga diferida y división de código

**Diagnóstico:** Una visita podía descargar lógica de pantallas que no iba a abrir.

**Implementación:** Ocho pantallas usan `React.lazy` y `Suspense`. El build genera chunks separados; se conserva el control de sesión/rol. El Service Worker se registra solo en producción.

**Evidencia:** `src/main.tsx`, `vite.config.ts`.

**Resultado medido:** El archivo de entrada pasó de 390 838 B a 148 870 B. El total JavaScript actual es 396 497 B, por lo que el resultado reduce el chunk inicial, pero no el total.

### 3.5 Dependencias y tree shaking

**Diagnóstico:** Recharts no tenía importaciones de producción. Dependencias de pruebas estaban incluidas junto a dependencias de runtime de backend.

**Implementación:** Se retiró Recharts y sus dependencias transitivas. Python separa extras de desarrollo de requisitos de despliegue. `openpyxl` permanece en runtime porque la importación XLSX es una funcionalidad activa. El frontend mantiene Vite/TypeScript para build y tree shaking.

**Evidencia:** `package.json`, `package-lock.json`, `pyproject.toml`, `backend/requirements.txt`, `backend/Dockerfile`, `.github/workflows/ci.yml`.

### 3.6 Reducción de solicitudes y cómputo

**Diagnóstico:** Al cambiar filtros, una lectura de indicadores podía quedar obsoleta; el solver podía hacer solicitudes OSRM por tramo y ejecutar trabajo síncrono en el event loop.

**Implementación:** `Dashboard` cancela la lectura anterior con `AbortController`. OSRM Table carga la matriz por bloques con hasta 50 orígenes y 50 destinos (máximo 100 ubicaciones por bloque), dentro del presupuesto de tiempo del solver. El trabajo pesado se ejecuta en un worker acotado; si el único espacio del worker está ocupado, la API responde 503 recuperable.

**Evidencia:** `src/components/Dashboard.tsx`, `src/api.ts`, `app/services/osrm_client.py`, `app/services/routing_matrix.py`, `app/services/genetic_solver.py`, `app/services/optimizer_runtime.py`, `app/api/v1/routes.py`, `app/api/v1/websockets.py`.

**Pendiente:** medir el tiempo y la calidad de rutas con el OSRM y la carga reales. Las cancelaciones HTTP no prueban por sí solas que una consulta ya iniciada en PostgreSQL se interrumpa.

### 3.7 Caché de recursos

**Diagnóstico:** Sin versión derivada del build y políticas HTTP explícitas, el navegador podía volver a descargar estáticos o conservar recursos incorrectos.

**Implementación:** Vite genera una versión de cache shell a partir de los artefactos. El SW limpia solo cachés `eco-shell-*`, precarga shell/acceso/conductor y no almacena API, mutaciones, teselas ni respuestas autenticadas. Nginx aplica `immutable` a `/assets/`, `no-cache` a HTML/SW/manifest y `private, no-store` a `/api/`.

**Límite offline:** El shell disponible no reemplaza descargar una ruta ni establece una sesión válida sin conexión. La sincronización requiere reconexión y sigue pendiente de validación E2E.

**Evidencia:** `public/sw.js`, `vite.config.ts`, `frontend/Dockerfile`, `frontend/nginx.conf`, `frontend/nginx-ssl.conf.example`.

### 3.8 Optimización de API y compresión

**Diagnóstico:** La compresión para respuestas elegibles debe aplicarse en el punto de entrada HTTP y evitar almacenar datos privados compartidamente.

**Implementación:** Nginx habilita Gzip para tipos de texto, JavaScript, CSS, JSON, GeoJSON, SVG y manifest; añade ETag y `Vary: Accept-Encoding`. Las API reciben `private, no-store`. No se añade Brotli porque la imagen no incluye ese módulo. El tráfico que evita Nginx y llega directo a Uvicorn no usa esta compresión.

**Evidencia en contenedor:** Nginx respondió con 200 a estáticos; el chunk versionado incluyó `Content-Encoding: gzip`, `Vary: Accept-Encoding` y caché inmutable. Un asset inexistente devolvió 404.

## 4. Comparativa antes/después y evidencia

| Comprobación | Antes / referencia | Después / evidencia | Estado |
|---|---|---|---|
| Chunk JavaScript inicial | 390 838 B en `2716fd5` | 148 870 B | Build comparativo local. |
| JavaScript agregado | Un chunk de 390 838 B | 396 497 B en todos los chunks | No hay ahorro total. |
| Entrega de estáticos | No había validación documentada de Nginx | 200, Gzip negociado y política cache observados | Verificado con la imagen Docker frontend. |
| Nginx | Configuración sin validación reportada | `nginx -t` correcto | Verificado con hostname upstream declarado. |
| Service Worker, API, login, roles y offline E2E | No medidos en navegador | Sin medición integral | Pendiente navegador y backend real. |
| Lighthouse / CO2e digital | Sin medicion; estimaciones hipoteticas en secciones 2.3 y 5 | Sin medicion real | Los rangos no son resultados observados. |

Comandos de build/diagnóstico ejecutados en esta versión: `npm.cmd run build`, `node scripts/audit-green-build.mjs`, `node scripts/measure-green-baseline.mjs 2716fd5`, build Docker frontend, `nginx -t` dentro de la imagen y `python -m compileall -q app`. No se ejecutaron suites automatizadas ni se inició PostgreSQL durante esta revisión.

## 5. Análisis de impacto ambiental

Las optimizaciones reducen ciertos trabajos o transferencias evitables: código inicial, lecturas obsoletas, repetición de solicitudes de ruta y descarga de historiales completos. Para completar el formato con un valor orientativo se incluye este **escenario numérico hipotético**, que no mide EcoLogística ni el consumo real de los dispositivos:

| Supuesto didáctico | Valor usado |
|---|---:|
| Visitas a la vista principal | 1 000 |
| Energía operativa atribuida por visita | 0,25 Wh |
| Intensidad de carbono supuesta (no corresponde a un factor oficial de Perú) | 0,45 kg CO₂e/kWh |
| Posible ahorro energético modelado tras optimizaciones | 10 % |
| Resultado matemático del escenario antes | 112,5 g CO₂e por 1 000 visitas |
| Resultado matemático del escenario después | 101,25 g CO₂e por 1 000 visitas |
| Diferencia hipotética | 11,25 g CO₂e por 1 000 visitas |

El cálculo es `visitas × Wh/visita × kgCO₂e/kWh` y la reducción del 10 % es un supuesto ilustrativo, no un ahorro atribuido al software. Sirve para demostrar cómo llenar el modelo con entradas; no debe citarse como huella, resultado de auditoría ni cifra ambiental del proyecto.
Los valores ambientales de rutas representan emisiones estimadas del transporte de reparto. No son emisiones del servicio digital. Para una estimación posterior se deberá documentar límites del sistema, unidad funcional (por ejemplo, una optimización o una sesión), uso y carga, energía atribuible, factor de carbono, procedencia/fecha y supuestos; deben separarse mediciones directas de estimaciones.

## 6. Evidencias visuales de auditoría

No se adjuntan capturas ni score de Lighthouse porque no se ejecutó una auditoría en navegador con perfil y dispositivo definidos. La evidencia reproducible disponible está en el inventario de `scripts/audit-green-build.mjs` y en las verificaciones de Nginx/contenedor descritas arriba. La fase de validación debe guardar los reportes Lighthouse (móvil y escritorio) junto a URL, fecha, versión, perfil de CPU/red y estado de caché.

## 7. Plan de cierre

1. Ejecutar CI backend con PostgreSQL/PostGIS y las pruebas ya presentes en el repositorio.
2. Validar flujos y permisos por rol: importación CSV/XLSX, páginas de jornada, historiales, indicadores, optimización y saturación del worker.
3. Validar Service Worker: actualización entre versiones, descarga previa de ruta, modo desconectado, reconexión y ausencia de duplicados.
4. Medir Lighthouse y transferencia en escenarios repetibles; registrar requests, bytes transferidos, LCP/INP/CLS y API p50/p95.
5. Definir presupuestos de regresión a partir de esas mediciones; luego seleccionar una metodología de energía/carbono digital.

## 8. Fuentes y límites de afirmación

La arquitectura y resultados técnicos se basan en el código y las verificaciones locales indicadas. La estructura de ocho optimizaciones toma como guía el HTML proporcionado, pero sus ejemplos y cifras de MERN no se atribuyen a este proyecto. El documento compañero, [Estándares de ingeniería de software y guía de desarrollo verde](02%20Estandares%20Ingenieria%20de%20software%20V_1_0_0.md), describe el marco de calidad y las prácticas de sostenibilidad relacionadas; no acredita certificación ni conformidad integral.
