# Plan de implementación — Sprint 1 (Fundación, Flota y Pedidos)

**Proyecto:** EcoLogística Huancayo — DistriRápido S.A.C.  
**Ámbito:** Huancayo, El Tambo y Chilca  
**Fecha de elaboración:** 26 de octubre de 2026  
**Alcance de este documento:** US-001, US-002, US-003, US-004, US-006 y EN-003 (sin cambios de código; solo planificación).

---

## 1. Contexto y objetivo del Sprint 1

Según `docs/03 Implementación/03_revision_del_sprint_v_1_0_0.md`, el Sprint 1 declaró **20 SP completados** (EN-003, US-001, US-002, US-003, US-004, US-006). Este plan contrasta esa declaración con el **código en la raíz del repositorio** (`app/`, `src/`, `tests/`), identifica brechas respecto a los criterios **originales** (RF/RNF + backlog ágil) y propone el orden de cierre.

**Nota metodológica:** Las historias ágiles (`01_transformando_a_agil_v_1_0_0.md`) incluyen **2 escenarios BDD** cada una; los RF atómicos (`06. Requisitos funcionales V_1_0_0.md`) incluyen **3 escenarios** (Gold / Feliz / Infeliz). La matriz inferior registra **ambas fuentes** como criterios completos.

---

## 2. Estado de Git y entorno

| Elemento | Estado |
|----------|--------|
| **Rama** | `main`, sincronizada con `origin/main` (commit `532ccaa`) |
| **Cambios locales** | Solo `README.md` modificado (sin stage) |
| **Migraciones** | No hay Alembic; esquema vía `Base.metadata.create_all` + `ALTER TABLE ... IF NOT EXISTS` en `app/db/init_db.py` |
| **Docker** | `docker-compose.yml`: PostGIS `5433→5432`, backend `:8000`, frontend nginx `:8080` |
| **BD desarrollo** | `ecologistica` (volumen `ecologistica_pgdata`) |
| **BD pruebas** | `ecologistica_test` (creada bajo demanda por pytest) |

---

## 3. Matriz de historias y criterios de aceptación

### Leyenda de estado

| Símbolo | Significado |
|---------|-------------|
| ✅ | Implementado y cubierto por prueba o flujo UI verificable en código |
| ⚠️ | Parcialmente implementado o desviación documental |
| ❌ | No implementado |
| N/A | No aplica al MVP actual (p. ej. manual assignment inexistente) |

---

### EN-003 — Seguridad transversal (RNF-003 / Ley N° 29733)

**Trazabilidad:** RNF-003, RN-001 (bloqueo), RBAC (`08. Usuarios V_1_0_3.md`).

| ID criterio | Descripción (fuente) | Estado | Evidencia / brecha |
|-------------|----------------------|--------|---------------------|
| EN3-1 | Rechazar o redirigir HTTP inseguro; exigir HTTPS/TLS 1.3 (EN-003 Esc. 1) | ❌ | `frontend/nginx.conf` escucha solo puerto **80**; uvicorn sin TLS. No hay middleware de redirección HTTPS. |
| EN3-2 | Contraseñas solo como hash bcrypt/argon2 (EN-003 Esc. 2) | ✅ | `app/services/passwords.py`, columna `usuarios.clave_hash`, semilla en `init_db` |
| EN3-RF | 100 % comunicaciones sensibles con TLS (RNF-003 medida) | ❌ | Tráfico local Docker/host en HTTP plano |
| EN3-RN1 | 3 intentos fallidos → bloqueo 15 min (RN-001) | ✅ | `app/services/access.py`, `auth_max_attempts=3`, `auth_lock_minutes=15`; `tests/test_auth.py` |
| EN3-JWT | JWT con expiración (revisión sprint: **15 min**) | ⚠️ | JWT HS256 en `app/services/tokens.py`; **`auth_token_hours=12`** en `app/core/config.py` (desalineado con acta de revisión) |
| EN3-RBAC | RBAC 6 perfiles; auditor solo lectura | ⚠️ | Backend: `require_roles` en desk, auth bitácora, optimizar, PDF. Frontend: `src/lib/access.ts`. **Varios GET operativos sin JWT** (ver §6) |
| EN3-OWASP | 0 vulns críticas/altas en evaluación definida | ⚠️ | No hay pipeline CodeQL/Sonar documentado en repo; endpoints públicos de pedidos/flota/rutas aumentan superficie |

**Archivos clave:** `app/api/v1/auth.py`, `app/api/deps.py`, `app/services/access.py`, `app/services/passwords.py`, `app/services/tokens.py`, `app/models/identity.py`, `tests/test_auth.py`, `frontend/nginx.conf`, `docker-compose.yml`.

---

### US-001 — Registro y mantenimiento de vehículos (RF-001)

| ID criterio | Descripción (fuente) | Estado | Evidencia / brecha |
|-------------|----------------------|--------|---------------------|
| US1-G | Registro completo → estado **Activo** y visible en catálogo (US Esc. 1 / RF Gold) | ⚠️ | Alta vía `POST /api/v1/flota` (solo **ADMIN**). `activo=true` por defecto. UI: `src/pages/Fleet.tsx`. **Operador no registra** (US dice Operador; RBAC doc: Admin C, Operador R/U) |
| US1-F | Editar dato permitido conservando identificación (RF Feliz) | ✅ | `PATCH /api/v1/flota/{id}` — capacidad, emisión, `activo`; placa inmutable en UI |
| US1-I | Placa duplicada rechazada (US Esc. 2 / RF Infeliz) | ✅ | Validación en `desk.create_vehicle`; `UniqueConstraint` en modelo |
| US1-CAMPO | Campos: placa, **modelo**, capacidad kg/m³, combustible, **rendimiento**, **factor emisión** | ⚠️ | Modelo `Vehiculo`: placa, capacidades, `tipo_combustible`, `emision_base_co2_g_km`, `factor_penalizacion_pendiente`. **Sin** `modelo` ni `rendimiento` (km/gal). Factor de emisión no mapea literalmente a RN-006 por combustible |

**Archivos:** `app/models/domain.py` (`Vehiculo`), `app/schemas/logistics.py` (`VehiculoCreate`), `app/api/v1/desk.py`, `src/pages/Fleet.tsx`, `tests/test_day.py` (registro + inactivación).

---

### US-002 — Restricciones de circulación por placa (RF-002 / RN-002)

| ID criterio | Descripción (fuente) | Estado | Evidencia / brecha |
|-------------|----------------------|--------|---------------------|
| US2-G | Regla validada y activa → excluir vehículos en planificación (US Esc. 1 / RF Gold) | ❌ | No hay tabla/API/UI de reglas; `solve_vrptw` / `_require_vehicles` no filtran por dígito de placa ni fecha |
| US2-F | Regla desactivada → todos los activos elegibles (RF Feliz) | ❌ | Sin módulo de reglas |
| US2-I | Sin regla validada → no activar restricción incompleta (US Esc. 2 / RF Infeliz) | ❌ | RN-002 marca `[PENDIENTE DE VALIDACIÓN NORMATIVA]`; no hay flag ni mensaje en sistema |
| US2-RN | Regla desactivada por defecto hasta validación normativa | ❌ | Solo documentado en `09. Reglas de negocio V_1_0_4.md` |

**Dependencia:** Afecta **US-007** (optimización), no Sprint 1 entregables mínimos salvo parametrización + UI de aviso.

**Archivos esperados (a crear):** modelo de regla, endpoint en `desk` o `routes`, integración en `app/services/genetic_solver.py` o filtro previo en `_require_vehicles`.

---

### US-003 — Historial y estado operativo del vehículo (RF-003)

| ID criterio | Descripción (fuente) | Estado | Evidencia / brecha |
|-------------|----------------------|--------|---------------------|
| US3-G | Activo → **Mantenimiento** con fecha; excluido de optimización (US Esc. 1 / RF Gold) | ⚠️ | Historial en `historial_vehiculo` (`HistorialVehiculo`) con timestamp `creado_en`. Estado operativo = boolean **`activo`** (inactivo ≈ fuera de servicio). **No existe estado `Mantenimiento`** distinto de Inactivo |
| US3-F | Mantenimiento → Activo, elegible de nuevo (RF Feliz) | ⚠️ | `activo: true` en PATCH restaura elegibilidad |
| US3-I | Vehículo **Inactivo** → rechazar asignación manual a ruta (US Esc. 2 / RF Infeliz) | N/A | No hay asignación manual de vehículo a ruta; optimizador solo usa `activo=true` (`_require_vehicles`) |
| US3-OPT | Inactivos excluidos de optimización | ✅ | `Vehiculo.activo.is_(True)` en `routes.py`; `GET /vehiculos` solo activos |

**Archivos:** `app/models/operations.py`, `app/api/v1/desk.py`, `tests/test_day.py`.

---

### US-004 — Importación masiva de pedidos (RF-004 / RNF-003)

| ID criterio | Descripción (fuente) | Estado | Evidencia / brecha |
|-------------|----------------------|--------|---------------------|
| US4-G | Hasta **150** pedidos válidos CSV/Excel → resumen de carga (US Esc. 1 / RF Gold) | ⚠️ | `POST /api/v1/jornadas/{fecha}/importar` + `order_import.py`. **Solo CSV** (texto en JSON). **Sin tope 150** en código |
| US4-F | Lote menor al máximo → importación OK (RF Feliz) | ✅ | Sin mínimo exigido |
| US4-I | Campos ausentes / formato inválido → rechazo con observaciones (US Esc. 2 / RF Infeliz) | ✅ | `parse_csv`, `_classify`, reporte por fila; `tests/test_day.py` |
| US4-RBAC | Solo roles autorizados importan | ✅ | Operador/Admin en `import_day`; auditor 403 en prueba |
| US4-GEO | Coordenadas / geocodificación ligera en import | ⚠️ | `geocode.locate_address` para direcciones conocidas; filas sin punto → `pendiente_punto` (solapamiento con US-005) |

**Archivos:** `app/services/order_import.py`, `app/services/geocode.py`, `app/api/v1/desk.py`, `src/pages/OrdersDay.tsx`, `tests/test_day.py`.

---

### US-006 — Ventanas de tiempo de entrega (RF-006 / RN-005)

| ID criterio | Descripción (fuente) | Estado | Evidencia / brecha |
|-------------|----------------------|--------|---------------------|
| US6-G | Intervalo válido guardado y usado en planificación (US Esc. 1 / RF Gold) | ✅ | Columnas `ventana_inicio/fin`, CK en BD; import y `POST /pedidos`; solver VRPTW |
| US6-F | Actualizar ventana antes de ruta (RF Feliz) | ❌ | **No hay** `PATCH/PUT` de pedido; solo nueva alta o reimportación |
| US6-I | Fin ≤ inicio → rechazo (US Esc. 2 / RF Infeliz) | ✅ | Pydantic en `PedidoCreateRequest`, `_classify` en CSV, CK SQL `ck_pedidos_ventana`; `tests/test_api.py` |
| US6-RN5 | ETA dentro de ventana en optimización | ⚠️ | Responsabilidad del solver (`tests/test_solver.py`); no es criterio US-006 puro |

**Archivos:** `app/schemas/logistics.py`, `app/models/domain.py`, `app/api/v1/routes.py`, `app/services/order_import.py`, `src/pages/OrdersDay.tsx`.

---

## 4. Resumen ejecutivo de brechas (Sprint 1)

| Historia | Criterios ágiles (2) | RF extendido (3) | Veredicto código |
|----------|---------------------|------------------|------------------|
| **EN-003** | 1/2 ✅ (hash); TLS ❌ | RNF-003 TLS ❌ | **Parcial** — base auth/RBAC sólida; falta capa TLS y endurecimiento de API |
| **US-001** | 1/2 pleno; registro ⚠️ rol | Feliz ✅ | **Parcial** — CRUD usable; campos RF-001 incompletos |
| **US-002** | 0/2 | 0/3 | **No implementado** (salvo texto RN en docs) |
| **US-003** | 1/2 (exclusión optimización vía `activo`) | Mantenimiento ⚠️ | **Parcial** — historial OK; enum de estados RF-003 no modelado |
| **US-004** | 1/2 (150/Excel ⚠️) | Feliz ✅ | **Parcial** — CSV robusto; falta Excel y límite 150 |
| **US-006** | 1/2 (update ❌) | Feliz ❌ | **Parcial** — validación alta/import OK |

---

## 5. Mapa de componentes (archivos y endpoints)

### Backend (`app/`)

| Módulo | Responsabilidad Sprint 1 |
|--------|-------------------------|
| `api/v1/auth.py` | Login, `/yo`, bitácora |
| `api/v1/desk.py` | Jornada, import CSV, flota CRUD, historial |
| `api/v1/routes.py` | Pedidos, listado vehículos activos, optimización (fuera alcance declarado pero acoplado) |
| `api/deps.py` | JWT Bearer, `require_roles` |
| `services/access.py` | RN-001, bitácora de acciones |
| `services/order_import.py` | US-004 |
| `models/domain.py` | `Vehiculo`, `Pedido` |
| `models/operations.py` | `Jornada`, `HistorialVehiculo` |
| `models/identity.py` | `Usuario`, `Bitacora` |
| `db/init_db.py` | Esquema + semilla Huancayo |

### Frontend (`src/`)

| Pantalla | Historia |
|----------|----------|
| `pages/Login.tsx` | EN-003 |
| `pages/Fleet.tsx` | US-001, US-003 (parcial) |
| `pages/OrdersDay.tsx` | US-004, US-006 (parcial) |
| `lib/access.ts` | EN-003 RBAC UI |
| `api.ts` | Cliente REST con Bearer |

### Endpoints relevantes

| Método | Ruta | Auth | Historia |
|--------|------|------|----------|
| POST | `/api/v1/auth/ingresar` | No | EN-003 |
| GET | `/api/v1/auth/yo`, `/bitacora` | Sí | EN-003 |
| GET/POST/PATCH | `/api/v1/flota`… | Sí (roles) | US-001, US-003 |
| POST | `/api/v1/jornadas/{fecha}/importar` | Sí | US-004 |
| GET | `/api/v1/jornadas/{fecha}` | Sí | US-004 |
| POST | `/api/v1/pedidos` | Sí | US-004/006 |
| GET | `/api/v1/pedidos`, `/api/v1/vehiculos` | **No** | Brecha EN-003 |
| GET | `/api/v1/rutas/mapa`, `/rutas/activas` | **No** | Brecha EN-003 |
| GET | `/api/v1/seguimiento/{codigo}` | **No** | Diseño público (cliente final) |

---

## 6. Dependencias entre historias

```mermaid
flowchart TD
  EN003[EN-003 Seguridad]
  US001[US-001 Flota CRUD]
  US002[US-002 Restricción placa]
  US003[US-003 Estados vehículo]
  US004[US-004 Import CSV]
  US006[US-006 Ventanas tiempo]
  US007[US-007 Optimización]

  EN003 --> US001
  EN003 --> US004
  EN003 --> US006
  US001 --> US003
  US001 --> US002
  US004 --> US006
  US006 --> US007
  US002 --> US007
  US003 --> US007
```

- **EN-003** es habilitador transversal: debe cerrarse antes de considerar “Done” cualquier US que exponga datos (importación ya protegida; listados no).
- **US-002** solo aporta valor en conjunto con optimización (**US-007**); puede entregarse en Sprint 1 como **parametrización desactivada** + mensaje RN-002 sin tocar el solver.
- **US-006** alimenta VRPTW; la edición de ventanas (RF Feliz) puede implementarse sin US-007.

---

## 7. Riesgos de regresión

| Riesgo | Impacto | Mitigación propuesta |
|--------|---------|---------------------|
| Proteger con JWT `GET /pedidos`, `/vehiculos`, `/rutas/*` | Mapa, sidebar y conductor dejan de funcionar sin sesión | Mantener excepciones documentadas (`/seguimiento`); asegurar que `src/api.ts` siempre envíe Bearer; pruebas en `test_api.py` |
| Introducir enum `estado_operativo` (Activo/Mantenimiento/Inactivo) | Migración de datos; cambio semántica de `activo` | Script de migración en `init_db`; mapear `activo=false` → Inactivo; default Mantenimiento vs Inactivo acordado con negocio |
| Tope 150 en import | Rechazo de lotes válidos en demo | Validar en `import_orders` + mensaje claro; prueba unitaria |
| TLS en nginx | URLs absolutas, cookies, WebSocket `wss` | Terminar TLS en nginx; `proxy_set_header X-Forwarded-Proto`; documentar certificados dev |
| Reducir JWT a 15 min | Sesiones cortas en demo | Refresh token o re-login UX; alinear `auth_token_hours` con revisión de sprint |
| US-002 en solver | Cambia asignación de flota en tests de optimización | Feature flag `restriccion_placa_habilitada=false` por defecto |

---

## 8. Estrategia de migraciones

1. **Estado actual:** `init_database()` crea tablas idempotentes; una migración ad hoc: `jornada_id` en `pedidos`.
2. **Próximos cambios Sprint 1 (recomendado):**
   - **US-001:** columnas opcionales `modelo VARCHAR`, `rendimiento_km_gal FLOAT` en `vehiculos` vía `ALTER TABLE ... IF NOT EXISTS` (mismo patrón que `jornada_id`).
   - **US-003:** columna `estado_operativo ENUM` o check constraint; sincronizar con `activo` durante transición.
   - **US-002:** tabla `restricciones_placa` (dígito, días, `validada_normativamente`, `activa`).
3. **Entornos:** ejecutar `python -m app.db.init_db` en contenedor backend tras despliegue; **no** truncar volumen `ecologistica_pgdata` en desarrollo.
4. **Pruebas:** pytest usa BD **`ecologistica_test`** aislada (ver §9).

---

## 9. Estrategia de pruebas

### Aislamiento (inspección de `tests/conftest.py`)

- Antes de importar la app, fuerza `DATABASE_URL` → base **`ecologistica_test`** (derivada del host `localhost:5433` o `db:5432`).
- Crea la BD de prueba si no existe (`asyncpg` contra `postgres`).
- Fixture `client`: **TRUNCATE** de tablas operativas (`pedidos`, `vehiculos`, `jornadas`, rutas, bitácora, historial) + `UPDATE usuarios` (reset intentos/bloqueo) + `init_database()` para resembrar depósito/flota/pedidos demo.
- **No trunca** `usuarios` (cuentas demo persisten en test DB).
- `AUTH_BCRYPT_ROUNDS=4` para velocidad.

**Conclusión de seguridad:** Ejecutar `pytest` **no debe modificar** la base `ecologistica` de desarrollo siempre que `DATABASE_URL` apunte al puerto estándar y conftest no sea parcheado. Verificar que no exista `.env` forzando otra URL antes de correr pruebas.

### Cómo ejecutar (sin afectar datos de desarrollo)

1. Levantar solo PostGIS: `docker compose up -d db`
2. Instalar deps: `pip install -e ".[dev]"` (desde raíz del repo)
3. Confirmar `.env` o variable: `DATABASE_URL=postgresql+asyncpg://ecologistica:ecologistica@localhost:5433/ecologistica`
4. Ejecutar: `python -m pytest tests/ -q`
5. Opcional cobertura: ampliar con `pytest --cov=app` (no configurado aún en `pyproject.toml`)

### Cobertura existente por historia

| Suite | Historias |
|-------|-----------|
| `tests/test_auth.py` | EN-003 (login, bloqueo, RBAC optimizar/bitácora) |
| `tests/test_day.py` | US-001, US-004, US-003 (parcial) |
| `tests/test_api.py` | US-006 (validación ventana), integración pedidos/optimización |
| `tests/test_solver.py` | US-006/RN-005 (ventanas en solver) |

**Faltan pruebas automatizadas para:** TLS, Excel/150, US-002, enum Mantenimiento, hash no expuesto en API (explícito).

### Docker / CI

- Imagen backend incluye `tests/` pero no hay job CI en repo.
- Healthchecks: `/health`, `/health/db` en compose.

---

## 10. Orden de desarrollo recomendado (cierre Sprint 1)

1. **EN-003 (cierre)** — TLS terminación nginx + redirección; auditar endpoints públicos; alinear expiración JWT con acta (15 min vs 12 h); prueba de hash; documentar excepción `/seguimiento`.
2. **US-001 (ajuste)** — Campos `modelo`/`rendimiento` o actualizar documentación si se mantiene modelo simplificado de emisiones; confirmar rol registrador (Admin vs Operador) con matriz RBAC.
3. **US-003 (modelo)** — Tres estados + historial; UI en `Fleet.tsx`; exclusión en `_require_vehicles` por estado.
4. **US-006 (RF Feliz)** — `PATCH /api/v1/pedidos/{id}` ventanas con validación; UI en `OrdersDay.tsx`.
5. **US-004 (completitud)** — Límite 150; soporte Excel (p. ej. `openpyxl` en backend o conversión client-side acordada).
6. **US-002 (mínimo Sprint 1)** — Entidad regla + UI aviso “pendiente validación normativa”; flag desactivado; sin filtro en solver hasta validación legal.

---

## 11. Decisiones documentales que requieren validación

| # | Tema | Opciones | Recomendación técnica |
|---|------|----------|------------------------|
| D1 | **JWT 15 min vs 12 h** | Acta sprint vs `config.py` | Validar con PM; si 15 min, cambiar `auth_token_hours` o introducir minutos + refresh |
| D2 | **Campos vehículo RF-001** | Ampliar BD vs reinterpretar `emision_base_co2_g_km` | Alinear con doc 11 BD o actualizar RF/backlog |
| D3 | **Registro vehículos** | Solo Admin (código) vs Operador (US-001) | Seguir `08. Usuarios` (Admin C) y ajustar redacción US-001 |
| D4 | **RN-002** | Implementar regla ficticia vs solo placeholder | Mantener **desactivada** hasta validación; UI de advertencia obligatoria |
| D5 | **Estados RF-003** | Enum triple vs boolean `activo` | Enum + migración; `activo` derivado o deprecado |
| D6 | **Excel US-004** | Parser server vs plantilla CSV única | Parser server si DoD exige Excel literal |
| D7 | **Endpoints públicos** | Cerrar todo vs excepciones | Cerrar datos personales (pedidos/flota); mantener tracking anonimizado |
| D8 | **TLS 1.3** | Solo staging/prod vs dev | TLS en nginx prod; dev puede usar mkcert con misma config |

---

## 12. ¿Entorno listo para iniciar EN-003?

| Prerrequisito | ¿Listo? |
|---------------|---------|
| Docker Compose (PostGIS + backend + frontend) | ✅ Configurado |
| Módulo auth JWT + bcrypt + RN-001 | ✅ Implementado |
| RBAC backend/frontend base | ✅ Implementado |
| Aislamiento BD pruebas (`ecologistica_test`) | ✅ Documentado en conftest |
| **Cierre EN-003 (TLS + superficie API + SLA token)** | ❌ **Pendiente** |

**Veredicto:** El entorno está **apto para continuar el trabajo de EN-003** (infraestructura y código base presentes), pero **no** se considera EN-003 **terminado** según criterios BDD y RNF-003. Se recomienda tratar EN-003 como **historia en progreso** hasta TLS, política de endpoints sensibles y alineación documental del token.

---

## 13. Referencias consultadas

- `docs/01 Inicio/06. Requisitos funcionales V_1_0_0.md`
- `docs/01 Inicio/07. Requisitos no funcionales V_1_0_0.md`
- `docs/01 Inicio/08. Usuarios V_1_0_3.md`
- `docs/01 Inicio/09. Reglas de negocio V_1_0_4.md`
- `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md`
- `docs/03 Implementación/03_revision_del_sprint_v_1_0_0.md`

---

*Documento temporal de planificación. Eliminar o archivar tras ejecutar el sprint de cierre.*
