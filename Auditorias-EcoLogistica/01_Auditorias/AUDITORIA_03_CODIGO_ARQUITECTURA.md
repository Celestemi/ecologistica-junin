# AUDITORIA_03_CODIGO_ARQUITECTURA

Auditoría estática de solo lectura completada. No se modificó ningún archivo; el árbol Git permanece limpio. No ejecuté tests ni builds: el workspace no tiene intérprete Python funcional ni `node_modules`, y la solicitud prohíbe operaciones que generen artefactos.

## 1. Arquitectura real

Aplicación activa única:

```text
React/Vite raíz (src/, index.html)
  → Nginx (frontend/nginx.conf)
  → FastAPI (app/main.py)
  → PostgreSQL 15 + PostGIS 3.4
```

- Frontend activo: `src/`, compilado por el `frontend/Dockerfile`. Entrada: `src/main.tsx`.
- Backend activo: `app/`, servido como `uvicorn app.main:app`. Entrada HTTP: `app/main.py`.
- Persistencia: SQLAlchemy async, GeoAlchemy2, PostgreSQL/PostGIS.
- Inicialización/migración: `backend/entrypoint.sh` espera la BD, ejecuta `app.db.init_db`, que aplica `Base.metadata.create_all` y migraciones SQL internas en `app/db/migrations.py`.
- Docker activo: `docker-compose.yml` levanta `db`, `backend` y `frontend`; no referencia el árbol legado.
- Reverse proxy: Nginx entrega SPA y redirige `/api/`, `/ws/`, salud y OpenAPI al backend.
- Pruebas: 20 archivos Pytest bajo `tests/`; una prueba Vitest bajo `src/lib/orderWindow.test.ts`. CI en `.github/workflows/ci.yml`.

Los routers API activos son `auth`, `desk`, `plate_restrictions`, `routes` y `websockets`.

## 2. Estructura de módulos y código activo

- `app/core`: configuración, BD, geometría, emisiones y seguridad de arranque.
- `app/models`: ORM de dominio, identidad, operaciones y restricciones.
- `app/schemas`: DTOs Pydantic.
- `app/services`: importación, geocodificación, restricciones, optimización, ETA, tiempo real, PDF, autenticación.
- `app/api/v1`: adaptadores HTTP/WebSocket.
- `src/pages` y `src/components`: interfaz de despacho, flota, pedidos, auditoría, seguimiento y conductor.

La separación frontend/backend es correcta y los endpoints usados por `src/api.ts` tienen contraparte estática en FastAPI. La aparente duplicación `/vehiculos` y `/flota` es legítima:

- `/vehiculos`: flota disponible para operación/ruteo.
- `/flota`: consola administrativa, incluidas unidades inactivas e historial.

## 3. Código legado: `EcologisticaJunin/`

Contiene un MVP independiente:

- Backend FastAPI de 4 KB, CRUD en memoria, sin base de datos, autenticación ni optimizador.
- Frontend React mínimo de cuatro archivos.
- Sus hashes y estructura no coinciden con los componentes activos.

No hay referencias desde Docker, CI, pruebas, imports ni configuración de despliegue. Son referencias únicamente documentales:

- `README.md` lo lista como el “Código Fuente”.
- `sonar-project.properties` lo excluye explícitamente del análisis.

No hay funcionalidad única activa que dependa de él. Archivarlo tendría bajo riesgo operativo, pero no debe eliminarse sin preservar su valor histórico/entregable académico y corregir primero el README. Clasificación: **CANDIDATO A ARCHIVAR**, no a eliminación automática.

## 4. Duplicaciones confirmadas

1. **Cálculo de CO₂ duplicado — CONSOLIDAR**

   - `app/core/emissions.py:leg_co2_grams`
   - `app/services/genetic_solver.py:leg_co2_grams`

   La aplicación activa usa la versión del solver; la de `core` no tiene consumidores productivos detectados. Ambas implementan el mismo concepto de emisiones por tramo, aunque la de `core` añade ajuste por altitud y combustible. Esto permite divergencia de resultados y hace ambigua la fuente de verdad.

2. **API cliente con funciones de bajo uso — REVISAR**

   `fetchTracking` no tiene consumidor en el frontend actual; el seguimiento público usa `fetchPublicTracking`. No es prueba suficiente para borrarla: representa un endpoint interno existente y podría ser previsto para una pantalla futura.

3. **Utilidades sin referencias productivas detectadas — CANDIDATO A ARCHIVAR/CONSOLIDAR**

   - `altitude_emission_factor` en `core/emissions.py`
   - `geodesic_adjuster` en `routing_matrix.py`
   - `hard_feasible` en `route_constraints.py`
   - `avoided_co2_to_quinual` en `schemas/logistics.py`

   No se recomienda eliminarlas sin revisar contratos externos, notebooks o material docente; sí añadir pruebas o retirarlas de la API interna si no tienen caso de uso.

No se halló duplicación indebida de componentes React. Las vistas de mapa, selección geográfica y tracking comparten biblioteca Leaflet, pero persiguen responsabilidades distintas.

## 5. Calidad y mantenibilidad

Hallazgos relevantes:

- **REFAC TORIZAR — alta prioridad:** `genetic_solver.py` (~51 KB) concentra modelo de problema, matriz, heurísticas iniciales, GA, evaluación, restricciones blandas, simulación de ETA, geometría y serialización de resultado. Es el principal foco de complejidad.
- **REFAC TORIZAR — alta prioridad:** `app/api/v1/routes.py` (~46 KB) mezcla endpoints, queries, persistencia de soluciones, mapeo de DTOs, reglas de negocio y metadatos.
- **REFAC TORIZAR — alta prioridad:** `websockets.py` importa localmente `_persist_solution` y `retain_other_vehicles` desde `routes.py`. Evita un ciclo de importación inmediato, pero crea un acoplamiento arquitectónico inverso: transporte WebSocket depende de helpers privados de otro adaptador HTTP.
- **ACTUALIZAR:** `sequence_eta.py` depende de símbolos privados del solver (`_build_problem`, `_schedule_vehicle`). Un refactor del solver puede romper ETA sin señal contractual.
- **MANTENER:** `route_constraints.py` separa adecuadamente penalizaciones de búsqueda de restricciones duras de publicación.
- **MANTENER:** módulos pequeños de estado de vehículo, ventanas, geocodificación, placas y RBAC presentan responsabilidades razonables.
- **RIESGO:** el solver llama opcionalmente OSRM de forma síncrona por tramo mediante `urllib`; en una solicitud async puede bloquear el event loop y generar hasta N² solicitudes. OSRM no es un servicio del `docker-compose.yml`.

## 6. Modelos, migraciones y dependencias

Modelos activos:

- Dominio: depósito, vehículo, pedido, solución y detalle de ruta.
- Identidad: usuario y bitácora.
- Operaciones: jornada, asignación de conductor, historial, área de operación.
- Restricciones: configuración, reglas e historial de placa.

Migraciones:

- Ocho migraciones SQL internas, registradas en `schema_migrations`.
- No usa Alembic.
- Riesgo moderado: combina `create_all` de SQLAlchemy y migraciones SQL manuales. Es aceptable para MVP, pero exige disciplina de compatibilidad y pruebas de upgrade.

Dependencias:

- `pyproject.toml` y `backend/requirements.txt` duplican la declaración Python.
- Docker instala `backend/requirements.txt`, no consume `uv.lock`; por tanto, el lockfile Python no asegura el runtime de contenedor.
- `requirements.txt` incluye herramientas de test (`pytest`, `pytest-asyncio`, `pytest-cov`, `httpx`) en la imagen productiva. `openpyxl` sí es requerida en producción para XLSX.
- Las versiones usan mínimos sin topes máximos; aumenta riesgo de incompatibilidades futuras.
- Dependencias frontend declaradas son coherentes con el código: React, Leaflet/react-leaflet, Recharts y Tailwind.
- No se detectaron paquetes claramente sin uso entre las dependencias declaradas.

## 7. Configuración y seguridad

- La validación de secreto fuera de demo está correctamente centralizada en `security_boot.py`.
- Los valores por defecto de Compose permiten `SECRET_KEY` conocida y cuentas demo; es aceptable solo para desarrollo, pero el archivo no es seguro como base directa de producción.
- PostGIS queda publicado en `5433` hacia el host.
- Hay ejemplo de TLS, pero la configuración Nginx activa es HTTP; TLS depende del despliegue externo.
- El endpoint público de tracking usa token opaco y parece intencional.
- `FORCE_HTTPS` está desactivado por defecto, como corresponde a entorno local.

## 8. Deuda técnica y documentación

La deuda documental es significativa:

- `README.md` describe `EcologisticaJunin/` como código fuente y declara OR-Tools, DEAP, Celery, Redis, PWA e IndexedDB.
- El runtime activo no contiene esas dependencias ni servicios.
- El optimizador actual es un GA implementado internamente; OSRM es opcional y no se despliega en Compose.
- Sonar excluye correctamente el legado, pero el README puede inducir a ejecutar o evaluar el sistema incorrecto.

## 9. Riesgos de limpieza

| Elemento | Clasificación | Riesgo/dependencia |
|---|---|---|
| `EcologisticaJunin/` | CANDIDATO A ARCHIVAR | Documentación lo referencia; no Docker/CI/tests. |
| Fórmula CO₂ en solver/core | CONSOLIDAR | Cambia métricas, PDF, optimización y pruebas si se unifica sin contrato. |
| Helpers privados solver usados por ETA | REFAC TORIZAR | Rompería recálculo de ETA si se mueve el solver. |
| Helpers privados de `routes.py` usados en WebSocket | REFAC TORIZAR | Rompería reoptimización en tiempo real. |
| `requirements.txt` vs `pyproject.toml` | CONSOLIDAR | Cambiar fuente de instalación afecta Docker y CI. |
| Utilidades sin referencias | CANDIDATO A ARCHIVAR | Validar consumidores externos antes de eliminar. |
| README/stack histórico | ACTUALIZAR | Riesgo de onboarding, evaluación y despliegue equivocados. |

## 10. Recomendaciones priorizadas antes del Sprint 3

1. Extraer un servicio de aplicación para persistir/publicar soluciones y hacerlo común para HTTP y WebSocket.
2. Convertir el solver en módulos: matriz/geometría, modelo, evaluación, operadores GA, construcción de itinerarios y métricas.
3. Definir una única fuente de verdad para emisiones y cobertura específica que garantice igual resultado en optimizador, API y PDF.
4. Formalizar interfaces públicas entre solver, ETA y restricciones; dejar de importar helpers con prefijo `_`.
5. Elegir una fuente de dependencias para runtime, bloquear versiones reproducibles y separar dependencias de producción de QA.
6. Actualizar README para identificar `app/` + `src/` como código activo y marcar `EcologisticaJunin/` como histórico.
7. Decidir explícitamente si OSRM es parte del despliegue Sprint 3; si lo es, añadirlo y evitar llamadas síncronas N² durante optimización.
8. Antes de limpiar candidatos, ejecutar la suite completa con PostGIS y añadir análisis estático/linting al CI.

Conclusión: la arquitectura activa es coherente para un MVP post-Sprint 2, con límites claros de mantenibilidad en el motor, el router principal y el acoplamiento WebSocket–HTTP. El legado no está operativo, pero su presencia y documentación desactualizada constituyen el mayor riesgo de confusión arquitectónica.
