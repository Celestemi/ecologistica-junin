# Informe de reducción del impacto ambiental y estándares de ingeniería de software

**Proyecto:** EcoLogística Huancayo  
**Versión del informe:** 1.0.0  
**Fecha:** 10 de noviembre de 2026  
**Estado:** primera versión de optimización implementada; validación funcional integral y medición de consumo digital pendientes.

## 1. Alcance y criterios

Este informe adapta las ocho áreas del documento de referencia al proyecto real: React 18, TypeScript, Vite 7, FastAPI, SQLAlchemy asíncrono y PostgreSQL/PostGIS. Los ejemplos MERN/MongoDB del documento no corresponden a este repositorio y sus cifras no se trasladan como resultados.

La entrega conserva las pantallas, reglas de permisos, importación CSV/XLSX, planificación, mapa, seguimiento, modo conductor y esquema de persistencia. No se modificaron modelos, tablas, índices ni migraciones. El endpoint de jornada ahora devuelve una envoltura con los pedidos y los metadatos de paginación; el frontend del repositorio consume el nuevo formato. Un cliente externo que esperase el array anterior deberá adaptar su lectura. La pantalla de pedidos mantiene acceso progresivo a todos los registros. Las imágenes raster propias no están presentes; el mapa usa teselas externas.

## 2. Diagnóstico e implementación de las ocho áreas

| Optimización | Estado actual | Problema identificado | Archivos involucrados | Solución aplicada | Prioridad | Riesgo |
|---|---|---|---|---|---|---|
| Consultas y acceso a datos | Mejorado, pendiente medir en BD | La importación comparaba potencialmente contra códigos ajenos al archivo; algunas lecturas devolvían columnas que no se usaban. | `app/services/order_import.py`, `app/api/v1/routes.py` | Acotar la comprobación de duplicados a los códigos importados y proyectar las columnas necesarias en indicadores. Sin índices ni cambios de esquema. | Alta | Bajo; verificar planes y cardinalidades reales en despliegue. |
| Paginación | Implementada en listados de crecimiento | Jornadas e historiales podían cargar registros sin límite o requerir descargar todo el historial. | `app/api/v1/desk.py`, `app/api/v1/auth.py`, `app/api/v1/plate_restrictions.py`, `app/schemas/restrictions.py`, `src/api.ts`, `src/pages/OrdersDay.tsx`, `src/pages/AuditLog.tsx`, `src/pages/Fleet.tsx`, `src/pages/PlateRestrictions.tsx` | Jornada por páginas de 100 (máximo API 250) con total y orden estable; historiales con cursor por ID y controles “cargar más”. | Alta | Medio; requiere validar usuarios con historiales extensos y clientes API externos. |
| Imágenes WebP/AVIF | No aplicable a assets propios actuales | No se encontraron fotografías raster propias que justifiquen conversión. Convertir teselas del proveedor externo no está bajo control del proyecto. | `public/`, `src/components/PinMap.tsx` | Sin conversión artificial. Mantener SVG de marca/iconos y documentar que la cartografía se sirve externamente. Aplicar formatos modernos cuando se agreguen imágenes propias. | Baja | Bajo. |
| Lazy loading y división de código | Implementada | El paquete de entrada incluía pantallas que no se necesitaban en todas las rutas. | `src/main.tsx`, `vite.config.ts` | Ocho pantallas se cargan bajo demanda; el build crea chunks separados. El SW solo precarga recursos del flujo offline principal. | Alta | Bajo; revisar navegación por rol en navegador real. |
| Dependencias y tree shaking | Mejorado | Recharts no tenía imports de producción y dependencias de test estaban en el manifiesto runtime. | `package.json`, `package-lock.json`, `pyproject.toml`, `backend/requirements.txt`, `backend/Dockerfile`, `.github/workflows/ci.yml`, `README.md` | Eliminado Recharts y sus dependencias transitivas; separadas dependencias Python dev/runtime. `openpyxl` permanece en runtime porque soporta la importación XLSX existente. CI instala extras dev; imagen backend no incluye tests. | Media | Bajo; revisar instalaciones limpias en CI. |
| Solicitudes y cómputo | Mejorado | Las lecturas obsoletas de indicadores seguían activas; la matriz de rutas podía requerir muchas consultas individuales; cómputo/red síncronos podían bloquear el loop asíncrono. | `src/components/Dashboard.tsx`, `src/api.ts`, `app/services/osrm_client.py`, `app/services/routing_matrix.py`, `app/services/genetic_solver.py`, `app/services/optimizer_runtime.py`, `app/services/sequence_eta.py`, `app/api/v1/routes.py`, `app/api/v1/websockets.py`, `app/core/config.py` | Cancelación de lecturas anteriores; matriz OSRM Table por bloques configurables de hasta 50 orígenes y 50 destinos (hasta 100 ubicaciones por solicitud); deadline de matriz dentro del presupuesto del solver; ejecución fuera del loop y un espacio de cómputo por worker. Saturación responde 503 recuperable. | Alta | Medio; medir calidad de rutas, límites/configuración del servidor OSRM y rendimiento con carga real. |
| Caché y entrega offline | Implementada con límites explícitos | El frontend Docker no copiaba `public/`; caché del SW no estaba vinculada a versión reproducible de build y las cabeceras requerían verificación. | `frontend/Dockerfile`, `public/sw.js`, `vite.config.ts`, `frontend/nginx.conf`, `frontend/nginx-ssl.conf.example` | Build copia recursos públicos; versión de caché deriva de build; limpieza limitada a cachés `eco-shell-*`; API privada no se almacena; navegación cae al shell si falta conexión. Assets versionados tienen caché inmutable y HTML/SW revalidan. | Alta | Medio; el modo offline requiere haber cargado datos/sesión, y validación de sincronización en navegador queda pendiente. |
| Compresión | Configurada y comprobada en contenedor | Sin configuración de compresión/cache HTTP en la entrega Nginx. | `frontend/nginx.conf`, `frontend/nginx-ssl.conf.example` | Gzip para tipos de texto/JSON/GeoJSON/JS/CSS/SVG/manifest, ETag, `Vary: Accept-Encoding`, caché por tipo; APIs `private, no-store`. | Media | Bajo; proxy directo a Uvicorn no usa esta compresión. |

### Límites funcionales preservados

- La ruta `/api/v1/pedidos` sigue entregando el conjunto requerido para mapa/planificación. No se truncó la carga de trabajo del optimizador. La jornada operativa sí tiene paginación porque la pantalla puede avanzar por páginas.
- La importación admite hasta 150 filas por archivo, según la regla existente; no se cambió ese límite.
- La tabla de rutas usa el endpoint OSRM Table en bloques. Si un bloque falla o un par no tiene ruta, el optimizador conserva su manejo de distancia no confiable/modelo alternativo.
- No se añadieron métricas de carbono digital. Las emisiones de las rutas son una estimación de transporte y no equivalen a consumo eléctrico de software.

## 3. Cambios de frontend y entrega

`src/main.tsx` divide las pantallas con `React.lazy` y `Suspense`, conserva controles de acceso y activa el Service Worker solo en producción. `Dashboard` cancela solicitudes de indicadores cuando cambia el filtro, se actualiza o desmonta.

El plugin local de `vite.config.ts` crea una versión del cache shell a partir del SW, manifest y artefactos. Precarga únicamente recursos estáticos del shell, acceso y conductor; no precarga datos de usuario, APIs ni teselas. Las mutaciones y respuestas autenticadas no se guardan. La sincronización offline continúa dependiendo del almacenamiento local y de la reconexión.

Nginx define políticas por recurso: `/assets/` con caché inmutable para nombres versionados, HTML/SW/manifest revalidables y `/api/` sin caché compartida. Gzip se aplicó en el proxy; el backend accesible directamente por Uvicorn no hereda esa configuración.

## 4. Evidencia de tamaño local

Se comparó un build del commit `2716fd5` con el build modificado, mediante `scripts/measure-green-baseline.mjs`; el inventario actual se genera con `scripts/audit-green-build.mjs`. Los tamaños son bytes locales sin compresión HTTP. El Gzip informado por Vite es una estimación local del artefacto.

| Medida | Base `2716fd5` | Versión actual | Interpretación |
|---|---:|---:|---|
| JavaScript de entrada | 390 838 B | 148 870 B | 61,91 % menos en el chunk inicial; las pantallas se distribuyen entre chunks. |
| Total JavaScript generado | 390 838 B | 396 497 B | 1,45 % más en el total, por división de módulos y cambios del build; no se afirma ahorro total de JavaScript. |
| CSS generado | 38 375 B | 38 375 B | Sin variación relevante. |
| Recursos estáticos del precache selectivo | No había manifiesto selectivo equivalente | 217 457 B | Incluye shell, acceso, conductor y CSS; no incluye respuestas API, HTML ni overhead HTTP. |

La división reduce el chunk de entrada, no garantiza una reducción equivalente de la primera transferencia: depende de la pantalla abierta. La instalación del SW puede descargar recursos adicionales para el uso offline. No se midieron visitas reales, caché del navegador ni uso de teselas.

## 5. Verificaciones realizadas

| Verificación | Resultado |
|---|---|
| `npm.cmd run build` | Correcto: TypeScript y build Vite de producción. Entrada de 148 870 B; CSS de 38 375 B. |
| `node scripts/audit-green-build.mjs` | Correcto: archivos, grafo y precache selectivo identificados. |
| `node scripts/measure-green-baseline.mjs 2716fd5` | Correcto: build comparativo reproducible. |
| `docker build -f frontend/Dockerfile -t ecologistica-green-frontend:check .` | Correcto; la imagen incluye `public/`, manifest y SW. npm reportó cero vulnerabilidades en su auditoría de dependencias instaladas. |
| `nginx -t` en la imagen | Correcto, con hostname `backend` declarado para validar el upstream sin iniciar la base de datos. |
| Solicitudes HTTP al contenedor | HTML y SW 200; chunk versionado 200 con `Content-Encoding: gzip`, `Vary: Accept-Encoding` y caché inmutable; asset inexistente 404. El manifest se sirvió 200. |
| `python -m compileall -q app` | Correcto usando el intérprete del entorno virtual. |
| Pruebas automatizadas y validación con PostgreSQL | No ejecutadas en esta revisión. Se requiere una pasada de CI con PostgreSQL/PostGIS para confirmar integración de consultas y contratos. |

No se ejecutó navegador E2E ni se modificó/inició ninguna base de datos. Las verificaciones HTTP confirman la entrega de estáticos, no login, APIs, permisos o sincronización offline completa.

## 6. Medidas y estándares de ingeniería

La entrega aplica prácticas asociadas a eficiencia de desempeño, uso de red, mantenibilidad y medición responsable. La referencia a ISO/IEC 25010, Green Software Foundation y Web Sustainability Guidelines expresa una relación de objetivos; no representa certificación ni auditoría formal.

No se midieron Lighthouse, LCP/INP/CLS, latencias p95, carga de PostgreSQL, throughput, energía ni CO₂ digital. Para estimar impacto digital en una siguiente versión se debe declarar método, unidades, factores de emisión, procedencia, fecha, límites y supuestos, separando medición de estimación.

## 7. Plan de cierre por fases

1. **Primera versión técnica (implementada):** carga diferida, cache shell versionado, gzip/cache HTTP, optimización de consultas/importación, páginas de listados, dependencias runtime/dev y matriz OSRM por bloques con cálculo aislado.
2. **Validación funcional (siguiente):** ejecutar CI backend con PostgreSQL/PostGIS; recorrer roles y pantallas; validar importación CSV/XLSX, paginación en jornadas e historiales, cálculo de rutas y manejo de saturación del optimizador.
3. **Validación PWA (siguiente):** probar instalación desde build anterior, actualización del SW, ruta offline previamente descargada, reconexión y cola sin duplicados en navegador real.
4. **Medición de desempeño/impacto (siguiente):** registrar tamaños transferidos y solicitudes por flujo, métricas web, latencia API/SQL y carga del solver; fijar umbrales a partir de baseline medido. Solo después seleccionar una metodología de energía/carbono digital.

## 8. Reversión

Los cambios son reversibles por control de versiones y reconstrucción de las imágenes frontend/backend. No hay migraciones ni datos que revertir. Al retirar el SW se debe publicar una versión de transición que permita al navegador recuperar conexión, activar el código correspondiente y limpiar solo los caches identificados por el proyecto.

