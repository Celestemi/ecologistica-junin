# Estándares de ingeniería de software y guía de desarrollo verde

**Proyecto:** EcoLogística Huancayo
**Versión:** 1.0.0
**Fecha:** 10 de noviembre de 2026
**Stack:** React, TypeScript, Vite, FastAPI, SQLAlchemy asíncrono, PostgreSQL/PostGIS
**Estado:** guía técnica adaptada al repositorio; no constituye certificación.

## 1. Propósito y alcance

Este documento convierte las referencias del informe HTML en prácticas concretas para este repositorio. La referencia propone ISO/IEC 25010, Green Software Foundation (GSF) y W3C Web Sustainability Guidelines (WSG), junto con normas separadas de backend, frontend y CI/CD. Aquí se conserva esa estructura, sustituyendo las prescripciones MERN por las tecnologías reales.

La guía distingue tres estados: **implementado** cuando hay código/configuración visible, **verificado** cuando además existe una comprobación ejecutada y **pendiente** cuando se requiere evidencia de ejecución o decisión del equipo. No se afirma conformidad completa con una norma ni se asigna una reducción de carbono sin medición.

## 2. Relación con los estándares y marcos

### 2.1 ISO/IEC 25010:2023 — modelo de calidad del producto

ISO/IEC 25010:2023 define un modelo de calidad de producto aplicable a productos TIC y software, compuesto por nueve características que sirven de referencia para especificar, medir y evaluar calidad. Para esta iniciativa se relacionan especialmente eficiencia de desempeño, mantenibilidad, fiabilidad, seguridad e interacción con el usuario.

**Aplicación local:** tamaños de build, consultas acotadas, división de pantallas, límites de concurrencia, respuestas HTTP privadas y políticas de caché. Cada requisito de calidad necesita una métrica de aceptación acordada; el build por sí solo no prueba una mejora de experiencia o eficiencia energética.

### 2.2 Principios de Green Software Foundation

La GSF explica que las actividades que reducen las emisiones del software incluyen eficiencia energética, consciencia de carbono y eficiencia de hardware. Este repositorio tiene acciones visibles sobre trabajo y transferencia evitables, pero no dispone de medida de energía ni de intensidad de carbono horaria/regional.

**Aplicación local:** evitar descargar módulos no usados, limitar solicitudes redundantes, agrupar consultas OSRM, acotar trabajo concurrente y prolongar el uso útil de assets versionados. No se implementa programación “carbon-aware” porque no existe integración con datos de intensidad de red ni una política operativa definida.

### 2.3 W3C Web Sustainability Guidelines (WSG)

WSG ofrece pautas para planear, desarrollar y operar productos digitales. Contempla eficiencia de medios y transferencia, documentación reutilizable, presupuestos de desempeño/impacto y consideraciones de accesibilidad, privacidad y operación.

**Aplicación local:** lazy loading, caché selectiva, compresión, paginación, inventario reproducible de artefactos y documentación de límites. No se declara conformidad parcial o total: se requiere evaluar criterios aplicables y mantener evidencia de cada uno.

## 3. Buenas prácticas de backend y datos

### 3.1 Consultas PostgreSQL/PostGIS y SQLAlchemy

- Seleccionar solo las columnas que consume la operación (`load_only`, columnas explícitas o agregaciones SQL cuando sea adecuado).
- Cargar relaciones de forma explícita para evitar N+1; revisar consultas con planes antes de agregar índices.
- Limitar y ordenar de forma estable los listados que crecen. Usar cursores para historiales y límites máximos en API.
- Evitar extraer filas completas si basta una columna o agregado. Aplicar filtros en SQL y validar cardinalidad con datos representativos.
- No crear ni cambiar índices/esquema sin revisión de planes, migración y autorización del proyecto.

**Evidencia actual:** proyección de campos de indicadores, detección de duplicados acotada a los códigos importados, jornadas con tamaño de página acotado e historiales con cursor. **Pendiente:** planes y latencias de PostgreSQL con volumen de operación.

### 3.2 Cómputo y dependencias de red

- Mantener I/O y cálculos síncronos intensivos fuera del event loop de FastAPI.
- Establecer un presupuesto total que incluya preparación de matrices y búsqueda; propagar timeout/error recuperable a la API.
- Acotar concurrencia y cola de trabajo para que un aumento de solicitudes no cree consumo ilimitado de CPU/memoria.
- Agrupar llamadas de red cuando el servicio lo permita; registrar fallos sin persistir payloads sensibles.
- En integraciones externas, controlar timeout, dimensiones, estado HTTP, datos nulos y ruta alternativa.

**Evidencia actual:** OSRM Table en bloques y worker con una ranura por proceso. **Pendiente:** perfil de duración/calidad y prueba de carga con OSRM real. El 503 de saturación es recuperable, pero debe verificarse en el flujo de usuario.

### 3.3 API, seguridad y almacenamiento

- Mantener caché compartida desactivada para respuestas autenticadas o de usuario (`private, no-store`).
- Mantener tiempos de espera y límites explícitos; no devolver pilas de error ni datos personales en logs.
- Mantener HTTPS en el despliegue público y revisar proxy WebSocket/API en cada entorno.
- Preservar autorización por rol en el servidor aunque la UI oculte acciones.
- Versionar contratos de paginación. El endpoint de jornada ahora devuelve un objeto con metadatos en lugar de un array; coordinar su adopción con cualquier consumidor externo.

## 4. Buenas prácticas de frontend

- Importar pantallas y módulos de peso bajo demanda con `React.lazy`/`Suspense`; revisar el grafo de importación de cada entrada.
- Añadir dependencias solo cuando resuelven una necesidad real y revisar imports antes de conservarlas.
- Cancelar o ignorar solicitudes obsoletas al cambiar filtros, desmontar vistas o iniciar una lectura nueva.
- Servir assets con nombre versionado y caché inmutable; revalidar HTML, manifest y Service Worker.
- No almacenar en Service Worker respuestas privadas, APIs mutables o recursos de terceros sin una política explícita.
- Preservar accesibilidad, legibilidad, navegación móvil y tiempos de interacción; reducción de bytes no sustituye una evaluación UX.
- Optimizar imágenes propias con dimensiones y formatos adecuados al dispositivo cuando existan; no procesar ni cachear teselas de terceros por cuenta del proyecto.

**Evidencia actual:** carga diferida, cancelación de lecturas de indicadores, cache shell selectiva, compresión/caché Nginx. **Pendiente:** auditoría real de teclado/lectores, dispositivos lentos y modo offline.

## 5. Integración continua y calidad

La CI del repositorio instala las dependencias backend de desarrollo, audita dependencias runtime, ejecuta pytest con cobertura, instala frontend con `npm ci`, ejecuta Vitest, compila y verifica el Service Worker e inventario de build. Son gates de calidad de código; su presencia no implica que la ejecución actual haya pasado.

| Control | Evidencia configurada | Criterio para mantenerlo |
|---|---|---|
| Instalación reproducible frontend | `npm ci`, lockfile versionado | No depender de módulos instalados localmente sin registrar. |
| Backend runtime/dev separado | `pyproject.toml`, `backend/requirements.txt` | Mantener solo dependencias de ejecución en la imagen productiva; conservar XLSX porque es funcionalidad activa. |
| Pruebas frontend/backend | Vitest y pytest en CI | Revisar resultado de CI para cada cambio; no omitir fallas. |
| Build y auditoría de assets | `npm run build`, `scripts/audit-green-build.mjs` | Revisar existencia, tamaño, grafo y precache. Añadir umbrales solo desde baseline estable. |
| Service Worker | `scripts/test-service-worker.mjs` en CI | Complementar simulación con navegación E2E real para claims offline. |
| Dependencias | `pip-audit` sobre requisitos productivos y auditoría npm de instalación | Investigar advisories; actualizar lockfiles de forma revisable. |

### 5.1 Presupuesto provisional de rendimiento

Para que la primera versión tenga criterios cuantitativos de revisión, se proponen los siguientes presupuestos **estimados**. Son metas de planificación, no resultados ya alcanzados. Se basan en el tamaño de build disponible y en un escenario de móvil Android medio, caché fría y 4G variable; el equipo debe ajustarlos después de obtener Lighthouse y trazas reales.

| Indicador | Presupuesto inicial propuesto | Estado actual conocido |
|---|---:|---|
| HTML + JavaScript inicial + CSS con Gzip | ≤80 KB | ~61 KB aproximados calculados a partir de artefactos actuales. |
| Lighthouse Performance móvil | ≥70/100 | Aún no medido; estimación de la primera versión 64–78/100. |
| FCP | ≤2,8 s | Estimación 1,7–2,8 s; no instrumentado. |
| LCP | ≤4,0 s | Estimación 2,8–4,5 s; el mapa puede exceder el presupuesto. |
| TBT | ≤400 ms | Estimación 190–430 ms; medir en los dispositivos objetivo. |
| CLS | ≤0,15 | Estimación 0,05–0,15; validar visualmente las pantallas. |
| p95 de primera página de jornada | ≤650 ms | Estimación 250–650 ms suponiendo BD cercana y baja concurrencia. |
| Escenario digital ilustrativo | 0,1125 → 0,1013 g CO₂e/visita para 1 000 visitas | Solo cálculo con supuestos didácticos del informe acompañante; no es huella del proyecto ni meta verificada. |

El presupuesto de LCP/TBT queda intencionalmente algo más amplio que un objetivo ideal porque la cartografía y las condiciones de red pueden dominar la experiencia. Debe revisarse tras 3–5 ejecuciones comparables en móvil y usar mediana/rango; no marcar como cumplido usando solo la estimación.

## 6. Matriz de mapeo: estándares, optimizaciones y evidencia

| Área | Calidad de producto relacionada | GSF/WSG relacionado | Evidencia en EcoLogística | Brecha de aceptación |
|---|---|---|---|---|
| Consultas y campos | Eficiencia de desempeño, mantenibilidad | Menos procesamiento/transferencia | Proyección de indicadores y filtro de códigos de importación | Planes y latencias reales. |
| Paginación | Eficiencia, interacción | Entrega de datos a escala necesaria | Jornada e historiales paginados | API externa y uso en grandes volúmenes. |
| Medios | Eficiencia, interacción | Optimización de medios | No hay imágenes raster propias identificadas; SVG y tiles externos | Reevaluar al añadir assets propios. |
| Lazy loading | Desempeño, mantenibilidad | Menor trabajo/descarga inicial | Ocho pantallas en chunks | Auditoría navegador por ruta/rol. |
| Dependencias | Mantenibilidad, seguridad | Uso eficiente de software | Recharts retirado; runtime/dev separado | Revisiones periódicas de uso y avisos. |
| Solicitudes/cómputo | Desempeño, fiabilidad | Eficiencia energética | AbortController, OSRM Table, worker acotado | Carga, rutas y CPU medidos en entorno real. |
| Caché | Desempeño, fiabilidad, seguridad | Evitar transferencia repetida | SW versionado y políticas por recurso | Actualización, privacidad y reconexión E2E. |
| Compresión | Desempeño, capacidad | Eficiencia de red | Gzip y ETag verificados en contenedor | Verificar API tras proxy y tráfico representativo. |

## 7. Criterios de aceptación para la siguiente revisión

1. CI completa en rama objetivo con backend/PostGIS, frontend y auditoría de dependencias sin fallos no justificados.
2. Recorrido de permisos y flujos principales con consola sin errores, sin regresión visual y con funcionalidad preservada.
3. Paginación consistente (sin omisiones/duplicados bajo altas concurrentes razonables) y contrato de jornada confirmado con consumidores.
4. Prueba de actualización del SW, disponibilidad offline de ruta previamente descargada y sincronización de entregas sin duplicados.
5. Perfil de navegador reproducible por ruta con bytes transferidos, solicitudes, LCP/INP/CLS y estado de caché; guardar informes de Lighthouse y reemplazar los rangos de planeación del apartado 5.1.
6. Latencias/recursos de API, consultas y solver medidos con datos de prueba representativos; derivar presupuestos de desempeño de esos resultados.
7. Toda afirmación ambiental usa método, unidad, límite del sistema, factor, origen y fecha; separar dato medido de estimación.
8. Cambios de esquema/índices se proponen aparte con evidencia y aprobación del proyecto.

## 8. Referencias

- [ISO/IEC 25010:2023 — Product quality model](https://www.iso.org/standard/78176.html). Modelo de calidad de producto para TIC y software; la relación descrita aquí no es una evaluación de conformidad.
- [W3C Web Sustainability Guidelines](https://www.w3.org/TR/web-sustainability-guidelines/). Guía para diseñar, desarrollar y operar productos digitales sostenibles.
- [Green Software Foundation — Learn Green Software](https://learn.greensoftware.foundation/introduction/). Material sobre eficiencia energética, consciencia de carbono, eficiencia de hardware, medición y competencias relacionadas.
- [Informe de reducción del impacto ambiental](01%20Informe%20de%20reduccion%20del%20impacto%20ambiental%20V_1_0_0.md). Auditoría y evidencia técnica específica de esta versión del proyecto.
