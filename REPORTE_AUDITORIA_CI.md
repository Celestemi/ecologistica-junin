# Reporte de auditoría CI/CD — EcoLogística Huancayo

**Fecha:** 2026-10-26  
**Workflow auditado:** `.github/workflows/ci.yml` (*CI Sprint 1*)  
**Alcance:** jobs `backend`, `frontend`, `sonar`, `deploy-staging`  
**Nota:** no se ejecutó un workflow real en GitHub Actions desde este entorno; las conclusiones del backend integrado se infieren del error reportado + corrección reproducible; el frontend se reprodujo localmente con los mismos comandos que CI.

---

## 1. Errores identificados

| # | Job | Síntoma | Severidad |
|---|-----|---------|-----------|
| E1 | **backend** | `ProgrammingError: unterminated dollar-quoted string at or near "$$ BEGIN"` al aplicar migración `003_vehiculo_modelo_rendimiento` (`ck_vehiculos_rendimiento`) | Bloqueante |
| E2 | **frontend** | `npm ci` falla: `package.json` y `package-lock.json` **desincronizados** (vitest / `@vitest/coverage-v8` en JSON sin entradas en lock) | Bloqueante (~12 s) |
| E3 | **sonar** | Job **SKIPPED** | Esperado (condición) |
| E4 | **deploy-staging** | Job **SKIPPED** | Esperado (condición) |
| E5 | **backend** (secundario, local) | Dos tests unitarios con fixtures incorrectos (`test_precheck_volume_exact_and_over`, `test_infeasible_windows_not_marked_feasible`) — podían fallar **después** de arreglar migraciones | Media |

---

## 2. Causa raíz

### E1 — Backend / migraciones SQL

**Causa raíz:** `app/db/migrations.py` ejecutaba cada migración con `_split_sql()` que partía el script en **`;` sin respetar bloques dollar-quoted** (`DO $$ ... END $$;`).

El bloque:

```sql
DO $$ BEGIN
    ALTER TABLE vehiculos ADD CONSTRAINT ck_vehiculos_rendimiento
    CHECK (rendimiento_km_gal > 0);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
```

se fragmentaba en varias “sentencias” inválidas (corte tras el `;` interno del `CHECK`), dejando `DO $$ BEGIN` **sin cerrar** → error PostgreSQL *unterminated dollar-quoted string*.

**Migraciones afectadas por el mismo mecanismo (mismo patrón `DO $$`):**

- `003_vehiculo_modelo_rendimiento`
- `007_geocodificacion_pedido` (dos bloques `DO $$`)

### E2 — Frontend

**Causa raíz:** se añadieron dependencias de prueba (`vitest`, `@vitest/coverage-v8`) en `package.json` pero **no se actualizó** `package-lock.json`. `npm ci` en GitHub Actions exige lock file **exactamente** alineado → fallo inmediato en instalación.

### E3 / E4 — Sonar y staging

| Job | Condición en workflow | Motivo SKIP |
|-----|----------------------|-------------|
| **sonar** | `if: vars.SONAR_ENABLED == 'true'` | Variable de repositorio no activada y/o jobs previos fallidos (`needs: [backend, frontend]`) |
| **deploy-staging** | `if: github.event_name == 'workflow_dispatch'` | Solo en ejecución manual; en `push`/`pull_request` no corre |

**Secretos Sonar (cuando se active):** `SONAR_TOKEN`, `SONAR_HOST_URL` — ver job `sonar` en `ci.yml`.

**Staging:** placeholder sin despliegue real; requiere environment `staging` y secretos `STAGING_*` (comentado en workflow).

---

## 3. Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `app/db/migrations.py` | Reimplementación de `_split_sql()` respetando etiquetas `$...$` |
| `tests/test_db_migrations.py` | **Nuevo** — regresión del splitter (003 y 007) |
| `tests/test_hard_constraints_us008.py` | Fixture volumen: 11 m³ > flota 10 m³ |
| `tests/test_optimizer_us007.py` | Ventanas 8:00–8:01 (como `test_solver.py`) |
| `package-lock.json` | Regenerado con `npm install` (sync con `package.json`) |

**No modificado:** `.github/workflows/ci.yml` (no fue necesario desactivar controles; el fallo era de aplicación, no de definición del pipeline).

---

## 4. Correcciones realizadas

1. **Splitter SQL dollar-safe** en `apply_migrations` → bloques `DO $$ ... END $$` se envían como **una sola** sentencia a PostgreSQL.
2. **Lock file frontend** actualizado para que `npm ci` sea determinista en CI.
3. **Tests unitarios** corregidos para no fallar tras suite verde en migraciones.
4. **Prueba de regresión** `tests/test_db_migrations.py` para evitar reintroducir el split naive por `;`.

---

## 5. Resultados de pruebas ejecutadas (local)

Entorno: Windows, Python 3.14 (`uv run`), Node 24.22.1 (instalado para reproducir CI). **PostGIS/Docker no disponible** en este host → suite backend **completa con BD no ejecutada** aquí.

| Comando | Resultado |
|---------|-----------|
| `uv run pytest tests/test_db_migrations.py tests/test_hard_constraints_us008.py::test_precheck_volume_exact_and_over tests/test_optimizer_us007.py::test_infeasible_windows_not_marked_feasible -q` | **4 passed** |
| `npm ci` | **OK** (tras actualizar lock) |
| `npm run test:coverage` | **4 tests passed** (`orderWindow.test.ts`) |
| `npm run build` (`tsc --noEmit && vite build`) | **OK** |
| `pytest` completo (114 tests, equivalente CI backend) | **No ejecutado** — requiere PostGIS (`localhost:5432` en Actions, `5433` opcional local) |

**Expectativa tras push:** con E1 y E2 corregidos, el job **backend** debería pasar la fase de migraciones en `init_database()` y ejecutar la suite; **frontend** debería completar install + tests + build.

---

## 6. Problemas pendientes

| Item | Detalle |
|------|---------|
| **Verificación GitHub Actions** | Hace falta **una corrida real** en `main`/`develop` tras commit/push para certificar verde (no afirmado en este informe). |
| **Suite backend local sin Docker** | Desarrolladores sin PostGIS seguirán viendo `ConnectionRefused` en tests con fixture `client`. |
| **SonarQube** | Activar `SONAR_ENABLED=true` en variables del repo + secretos; job sigue siendo opcional por diseño. |
| **Deploy staging** | Sigue siendo placeholder; no activar despliegue real sin credenciales. |
| **npm audit** | 5 vulnerabilidades reportadas por npm en dependencias transitivas — **no** abordadas en esta auditoría (fuera del fallo CI inmediato). |
| **Cobertura DoD ≥ 80 %** | Independiente del CI verde; no es gate actual en `ci.yml` (`cov-fail-under=0`). |

---

## 7. Instrucciones para comprobar en GitHub Actions

1. **Commit** de los archivos listados en §3 (sin incluir secretos).
2. **Push** a `main` o `develop`, o abrir **Pull Request** hacia esas ramas (disparan `ci.yml`).
3. En GitHub → **Actions** → workflow *CI Sprint 1* → última ejecución:
   - **backend:** debe pasar *Install backend dependencies* y *Pytest with coverage* (~2 min si incluye tests `@slow`).
   - **frontend:** *npm ci* → *test:coverage* → *build* en secuencia.
4. Si **backend** falla de nuevo, descargar log del step *Pytest with coverage* y buscar:
   - errores SQL → revisar `_split_sql` / nueva migración con `DO $$`
   - fallos de assert → prueba funcional (no migración)
5. **Sonar (opcional):** Settings → Secrets and variables → Actions → Variables: `SONAR_ENABLED` = `true`; Secrets: `SONAR_TOKEN`, `SONAR_HOST_URL`. Re-ejecutar workflow.
6. **Staging (opcional):** Actions → *CI Sprint 1* → **Run workflow** (`workflow_dispatch`) → job `deploy-staging` solo imprime placeholder.

### Reproducción local equivalente

```powershell
# Backend (PostGIS en 5432 o 5433 según DATABASE_URL)
pip install -r backend/requirements.txt
$env:DATABASE_URL = "postgresql+asyncpg://ecologistica:ecologistica@localhost:5432/ecologistica"
pytest --cov=app --cov-report=xml:coverage.xml

# Frontend (mismo orden que CI)
npm ci
npm run test:coverage
npm run build
```

---

## 8. Resumen ejecutivo

| Área | Estado tras correcciones |
|------|---------------------------|
| Migraciones PostgreSQL | **Corregido** (causa raíz E1) |
| Frontend CI | **Corregido** (lock file, verificado localmente) |
| Sonar / staging | **Sin cambio** — skipped por diseño |
| CI verde en GitHub | **Pendiente de confirmación** en remoto |

---

*Fin del reporte `REPORTE_AUDITORIA_CI.md`.*
