# AUDITORIA_01_ESTADO_REPOSITORIO

Auditoría de solo lectura completada. No se modificó, creó, eliminó ni ejecutó ningún archivo, servicio, prueba o migración.

## 1. Resumen general

El repositorio está limpio y su implementación activa se encuentra en la raíz:

- Backend FastAPI: `app/`
- Frontend React/TypeScript/Vite: `src/`
- Pruebas Python: `tests/`
- Prueba frontend: `src/lib/orderWindow.test.ts`
- Infraestructura: Docker Compose y Dockerfiles en `backend/` y `frontend/`

Existe una segunda implementación mínima y antigua en `EcologisticaJunin/`. No participa en Docker, CI, Sonar ni en la aplicación raíz; README todavía la presenta erróneamente como el código fuente principal. Es el principal candidato a archivado, no a eliminación inmediata.

## 2. Estado Git

| Elemento | Estado |
|---|---|
| Rama actual | `main` |
| Seguimiento | `main...origin/main` |
| Directorio de trabajo | Limpio |
| Archivos modificados | Ninguno |
| Archivos no rastreados | Ninguno |
| Archivos ignorados físicos detectados | Ninguno |
| Remoto | `origin` → GitHub `Celestemi/ecologistica-junin.git` |
| Ramas locales | `main` |
| Ramas remotas | `origin/main`, `origin/paola-documento-03` |
| Etiquetas | No hay etiquetas Git |
| Último commit | `57f2439`, 2026-10-26 — ajuste de tests de optimización |
| Integridad Git | Sin objetos inalcanzables ni basura detectada por `git fsck` |

Los patrones de `.gitignore` cubren apropiadamente entornos virtuales, `node_modules`, cobertura, compilados, secretos `.env`, cachés, logs y temporales. En el árbol actual no hay artefactos ignorados presentes.

## 3. Estructura del proyecto

```text
ecologistica-junin/
├── app/                         Backend FastAPI activo
│   ├── api/v1/                  Auth, rutas, escritorio, WebSocket, restricciones
│   ├── core/                    Configuración, BD, geografía, emisiones, seguridad
│   ├── db/                      Inicialización y migraciones SQL propias
│   ├── models/                  Modelos SQLAlchemy/PostGIS
│   ├── schemas/                 DTOs/Pydantic
│   ├── services/                Solver GA, rutas, PDF, geocoding, RBAC, etc.
│   └── data/                    Área operativa GeoJSON
├── src/                         Frontend React + TypeScript activo
│   ├── components/              Dashboard, mapas, conductor, navegación
│   ├── pages/                   Login, flota, pedidos, seguimiento, auditoría
│   └── lib/                     Sesión, acceso, ventana horaria y test
├── tests/                       21 módulos de pruebas backend
├── backend/                     Dockerfile, entrypoints y requirements activo
├── frontend/                    Dockerfile y configuración Nginx activa
├── docs/                        Inicio, planificación, Sprint 1/2, QA y despliegue
├── .github/workflows/           CI de backend, frontend, Sonar y placeholder staging
├── EcologisticaJunin/           Prototipo antiguo duplicado
├── docker-compose.yml           PostgreSQL/PostGIS + backend + frontend
├── pyproject.toml / uv.lock     Manifiesto y lock Python
├── package.json / package-lock  Manifiesto y lock JavaScript
└── README.md                    Documentación de entrada
```

## 4. Inventario de archivos relevantes

| Área | Clasificación | Evidencia |
|---|---|---|
| `app/` | CONSERVAR | Código backend activo, importado por Docker, CI y pruebas. |
| `src/` | CONSERVAR | Aplicación React activa, compilada por Vite y Docker. |
| `tests/` | CONSERVAR | Suite backend; CI ejecuta `pytest` con cobertura. |
| `src/lib/orderWindow.test.ts` | CONSERVAR | Incluido por Vitest. |
| `app/db/migrations.py` | CONSERVAR | Mecanismo propio de migración; no se detectó Alembic. |
| `app/data/operating_area_dev.geojson` | CONSERVAR | Datos geográficos de desarrollo y README asociado. |
| `docker-compose.yml`, Dockerfiles, entrypoints | CONSERVAR | Topología operativa definida para PostGIS, backend y frontend. |
| `.env.example` | CONSERVAR | Plantilla actual con variables y comentarios operativos. |
| `docs/` | CONSERVAR / ACTUALIZAR selectivamente | Documentación de trazabilidad académica, funcional, QA y despliegue. |
| `package-lock.json` | CONSERVAR | Está alineado con `package.json`; incluye Vitest y cobertura. |
| `uv.lock` | CONSERVAR | Lock Python existente y coherente con `pyproject.toml`. |
| `sonar-project.properties` | CONSERVAR | Configuración de análisis; excluye explícitamente el prototipo antiguo. |

## 5. Archivos y carpetas potencialmente innecesarios

| Ruta | Clasificación | Motivo y evidencia | Dependencias posibles | Riesgo | Confianza |
|---|---|---|---|---|---|
| `EcologisticaJunin/` | CANDIDATO A ARCHIVAR | Prototipo FastAPI/React de 9 archivos. Tiene datos en memoria, CRUD básico y mensaje de “siguiente iteración”. No es usado por Docker, CI ni Sonar; README lo referencia como código principal. | Valor histórico, evaluación académica, enlaces de README, rama o entrega previa. | Alto si se elimina: puede romper trazabilidad documental. | Alta para archivar; baja para eliminar. |
| `EcologisticaJunin/backend/main.py` | CANDIDATO A ARCHIVAR | API antigua independiente, sin BD y con datos temporales. La implementación activa equivalente está en `app/main.py`. | Evidencia del MVP inicial. | Medio. | Alta. |
| `EcologisticaJunin/frontend/` | CANDIDATO A ARCHIVAR | Frontend JSX mínimo, Vite 5, sin lockfile ni integración con la app actual. La app activa es TypeScript en raíz. | Referencia histórica y README. | Medio. | Alta. |
| `EcologisticaJunin/backend/.env.example` | REVISAR | Plantilla mínima con URL PostgreSQL distinta del `.env.example` actual. | Puede servir para explicar el prototipo. | Bajo técnico, medio documental. | Alta. |
| `EcologisticaJunin/backend/.gitkeep` | CANDIDATO A ELIMINAR | Archivo vacío dentro de un directorio que ya contiene archivos. | Valor histórico de la estructura inicial. | Bajo, pero debe acompañar la decisión sobre el prototipo completo. | Alta. |
| `EcologisticaJunin/frontend/.gitkeep` | CANDIDATO A ELIMINAR | Igual caso: archivo vacío en directorio no vacío. | Valor histórico. | Bajo. | Alta. |
| `tests/__init__.py` | CONSERVAR | Está vacío, pero puede preservar el comportamiento de paquete e importación de pruebas. | Pytest, imports relativos futuros. | Bajo, pero no hay beneficio material al retirarlo. | Media. |

No se encontraron archivos de caché, builds, logs, backups (`.bak`, `.old`, `.orig`) ni temporales versionados.

## 6. Carpetas duplicadas o antiguas

`EcologisticaJunin/` es una duplicación funcional antigua del backend y frontend actuales:

| Componente antiguo | Sustituto activo |
|---|---|
| `EcologisticaJunin/backend/main.py` | `app/main.py` + `app/api/`, `app/services/`, `app/models/` |
| `EcologisticaJunin/backend/requirements.txt` | `backend/requirements.txt` + `pyproject.toml` |
| `EcologisticaJunin/frontend/src/*.jsx` | `src/**/*.tsx` |
| `EcologisticaJunin/frontend/package.json` | `package.json` + `package-lock.json` |

El README conserva enlaces y descripciones hacia el prototipo, por lo que actualmente documenta una estructura que ya no representa la aplicación ejecutable.

## 7. Dependencias

### Frontend

Las dependencias declaradas de la raíz tienen uso estático identificado:

- `react`, `react-dom`: aplicación React.
- `leaflet`, `react-leaflet`, `@types/leaflet`: mapas.
- `recharts`: dashboard.
- `tailwindcss`, `@tailwindcss/vite`: estilos.
- `vite`, `@vitejs/plugin-react`, `typescript`: compilación.
- `vitest`, `@vitest/coverage-v8`: pruebas y cobertura.

`package-lock.json` incluye las dependencias de Vitest declaradas. El informe histórico `REPORTE_AUDITORIA_CI.md` documenta una desincronización pasada, pero el lock actual contiene dichas entradas; ese informe debería leerse como evidencia histórica, no como estado actual.

### Backend

Las dependencias de producción declaradas en `pyproject.toml` se corresponden, en general, con importaciones o infraestructura activa: FastAPI, SQLAlchemy, asyncpg, PostGIS/GeoAlchemy, Pydantic, JWT, bcrypt, Shapely y ReportLab.

| Elemento | Clasificación | Hallazgo |
|---|---|---|
| `backend/requirements.txt` | ACTUALIZAR | Mezcla dependencias de ejecución y desarrollo/pruebas. El Dockerfile instala también `pytest`, `pytest-cov`, `httpx` y `openpyxl` en la imagen de producción. |
| `pyproject.toml` | CONSERVAR | Separa correctamente extras `dev`, aunque el flujo Docker/CI usa `requirements.txt` en lugar de esos extras. |
| `tzdata` | REVISAR | Declarado en producción; no se encontró importación directa. Puede ser requisito indirecto o necesario para zonas horarias en imágenes slim. No debe eliminarse sin prueba controlada. |
| Doble manifiesto Python | REVISAR | `pyproject.toml` y `backend/requirements.txt` replican versiones. Existe riesgo de divergencia futura. |
| Dependencias del prototipo | CANDIDATO A ARCHIVAR | El manifiesto antiguo solo contiene `fastapi`, `uvicorn`, `pydantic`, insuficiente para la implementación actual y no usado por la infraestructura. |

## 8. Riesgos de limpieza

1. No eliminar `EcologisticaJunin/` directamente: README y posiblemente entregables académicos lo usan como historial.
2. No borrar documentación que mencione OR-Tools, DEAP, Celery, Redis, OSRM o PWA sin decidir primero si representa alcance planificado, desviación aceptada o deuda documental. El código actual emplea un algoritmo genético propio; el plan de Sprint 2 ya reconoce esta decisión.
3. No eliminar `tzdata` sólo por falta de importación directa.
4. No modificar `uv.lock`, `package-lock.json`, requisitos ni manifiestos sin una validación reproducible posterior.
5. No ejecutar pruebas en esta auditoría: `docs/qa/COMANDOS_CALIDAD.md` indica que las pruebas escriben en `ecologistica_test`. Por restricción de solo lectura, su resultado queda como “No verificado”.

## 9. Recomendaciones priorizadas

1. **Alta — Actualizar `README.md`** para señalar `app/` y `src/` como implementación principal, y describir `EcologisticaJunin/` como prototipo histórico si se decide conservarlo.
2. **Alta — Decidir el destino documental de `EcologisticaJunin/`**: moverlo a una ubicación histórica o mantenerlo explícitamente como snapshot académico. No eliminar sin validación de equipo.
3. **Media — Resolver la estrategia Python**: usar `pyproject.toml`/`uv.lock` como fuente de verdad, o mantener `requirements.txt` generado y separar runtime de desarrollo.
4. **Media — Actualizar documentación técnica** que todavía presenta OR-Tools, DEAP, Redis/Celery, OSRM local e IndexedDB como componentes implementados. El plan de Sprint 2 documenta parcialmente las desviaciones, pero README y documentos de arquitectura siguen siendo ambiguos.
5. **Baja — Evaluar los `.gitkeep`** únicamente después de resolver el archivado del prototipo.
6. **Baja — Crear la primera etiqueta Git** al cerrar una versión validada, ya que actualmente no existe ninguna.

## 10. Archivos que no deben modificarse sin análisis adicional

- `app/db/migrations.py`, `app/db/init_db.py`, `app/core/database.py`
- `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`, entrypoints
- `pyproject.toml`, `uv.lock`, `backend/requirements.txt`
- `package.json`, `package-lock.json`
- `.env.example`
- `.github/workflows/*`
- `sonar-project.properties`
- `app/data/operating_area_dev.geojson`
- `README.md` y los documentos de planificación/arquitectura relacionados con decisiones técnicas
- Toda la carpeta `EcologisticaJunin/` hasta acordar si es evidencia histórica o material descartable.
