"""Migraciones SQL versionadas (sin Alembic)."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

MIGRATIONS: tuple[tuple[str, str], ...] = (
    (
        "001_pedido_token_seguimiento",
        """
        ALTER TABLE pedidos
        ADD COLUMN IF NOT EXISTS token_seguimiento VARCHAR(36);
        CREATE UNIQUE INDEX IF NOT EXISTS uq_pedidos_token_seguimiento
        ON pedidos (token_seguimiento)
        WHERE token_seguimiento IS NOT NULL;
        """,
    ),
    (
        "002_asignaciones_conductor",
        """
        CREATE TABLE IF NOT EXISTS asignaciones_conductor (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            vehiculo_id INTEGER NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
            activa BOOLEAN NOT NULL DEFAULT true,
            asignado_en TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        CREATE UNIQUE INDEX IF NOT EXISTS uq_asignacion_conductor_activo
        ON asignaciones_conductor (usuario_id)
        WHERE activa = true;
        CREATE INDEX IF NOT EXISTS ix_asignaciones_vehiculo
        ON asignaciones_conductor (vehiculo_id)
        WHERE activa = true;
        """,
    ),
    (
        "003_vehiculo_modelo_rendimiento",
        """
        ALTER TABLE vehiculos ADD COLUMN IF NOT EXISTS modelo VARCHAR(120);
        ALTER TABLE vehiculos ADD COLUMN IF NOT EXISTS rendimiento_km_gal DOUBLE PRECISION;
        UPDATE vehiculos SET modelo = 'No registrado'
        WHERE modelo IS NULL OR btrim(modelo) = '';
        UPDATE vehiculos SET rendimiento_km_gal = 10.0
        WHERE rendimiento_km_gal IS NULL OR rendimiento_km_gal <= 0;
        ALTER TABLE vehiculos ALTER COLUMN modelo SET NOT NULL;
        ALTER TABLE vehiculos ALTER COLUMN rendimiento_km_gal SET NOT NULL;
        DO $$ BEGIN
            ALTER TABLE vehiculos ADD CONSTRAINT ck_vehiculos_rendimiento
            CHECK (rendimiento_km_gal > 0);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """,
    ),
    (
        "004_vehiculo_estado_operativo",
        """
        ALTER TABLE vehiculos ADD COLUMN IF NOT EXISTS estado_operativo VARCHAR(32);
        UPDATE vehiculos SET estado_operativo = 'activo'
        WHERE estado_operativo IS NULL AND activo = true;
        UPDATE vehiculos SET estado_operativo = 'inactivo'
        WHERE estado_operativo IS NULL AND activo = false;
        UPDATE vehiculos SET estado_operativo = 'activo' WHERE estado_operativo IS NULL;
        ALTER TABLE vehiculos ALTER COLUMN estado_operativo SET NOT NULL;
        UPDATE vehiculos SET activo = (estado_operativo = 'activo');
        """,
    ),
    (
        "005_historial_estado_operativo",
        """
        ALTER TABLE historial_vehiculo ADD COLUMN IF NOT EXISTS estado_anterior VARCHAR(32);
        ALTER TABLE historial_vehiculo ADD COLUMN IF NOT EXISTS estado_nuevo VARCHAR(32);
        ALTER TABLE historial_vehiculo ADD COLUMN IF NOT EXISTS motivo VARCHAR(240);
        UPDATE historial_vehiculo SET estado_nuevo = CASE WHEN activo THEN 'activo' ELSE 'inactivo' END
        WHERE estado_nuevo IS NULL;
        """,
    ),
    (
        "006_restriccion_placa",
        """
        CREATE TABLE IF NOT EXISTS restriccion_placa_config (
            id SERIAL PRIMARY KEY,
            ambito VARCHAR(120) NOT NULL,
            etiqueta_validacion VARCHAR(64) NOT NULL,
            validada_normativamente BOOLEAN NOT NULL DEFAULT false,
            activa BOOLEAN NOT NULL DEFAULT false,
            referencia_normativa VARCHAR(240),
            actualizada_en TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        CREATE TABLE IF NOT EXISTS restriccion_placa_reglas (
            id SERIAL PRIMARY KEY,
            config_id INTEGER NOT NULL REFERENCES restriccion_placa_config(id) ON DELETE CASCADE,
            ultimo_digito SMALLINT NOT NULL,
            dias_semana SMALLINT[] NOT NULL
        );
        CREATE TABLE IF NOT EXISTS historial_restriccion_placa (
            id SERIAL PRIMARY KEY,
            correo VARCHAR(120) NOT NULL,
            detalle TEXT NOT NULL,
            creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        INSERT INTO restriccion_placa_config (ambito, etiqueta_validacion)
        SELECT 'Huancayo, El Tambo y Chilca', '[PENDIENTE DE VALIDACIÓN NORMATIVA]'
        WHERE NOT EXISTS (SELECT 1 FROM restriccion_placa_config);
        """,
    ),
    (
        "007_geocodificacion_pedido",
        """
        ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS estado_ubicacion VARCHAR(32);
        UPDATE pedidos SET estado_ubicacion = 'geocodificado'
        WHERE estado_ubicacion IS NULL;
        ALTER TABLE pedidos ALTER COLUMN estado_ubicacion SET NOT NULL;
        ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS volumen_m3 DOUBLE PRECISION;
        ALTER TABLE pedidos ALTER COLUMN ubicacion DROP NOT NULL;
        ALTER TABLE pedidos ALTER COLUMN altitud_msnm DROP NOT NULL;
        DO $$ BEGIN
            ALTER TABLE pedidos ADD CONSTRAINT ck_pedidos_estado_ubicacion CHECK (
                (estado_ubicacion = 'pendiente_validacion' AND ubicacion IS NULL AND altitud_msnm IS NULL)
                OR (estado_ubicacion = 'geocodificado' AND ubicacion IS NOT NULL AND altitud_msnm IS NOT NULL)
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        DO $$ BEGIN
            ALTER TABLE pedidos ADD CONSTRAINT ck_pedidos_volumen
            CHECK (volumen_m3 IS NULL OR volumen_m3 > 0);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        CREATE TABLE IF NOT EXISTS area_operacion (
            id SERIAL PRIMARY KEY,
            etiqueta VARCHAR(240) NOT NULL,
            geom geometry(MultiPolygon, 4326) NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_area_operacion_geom ON area_operacion USING GIST (geom);
        """,
    ),
    (
        "008_eta_detalle_ruta",
        """
        ALTER TABLE rutas_detalle ADD COLUMN IF NOT EXISTS estado_eta VARCHAR(32);
        ALTER TABLE rutas_detalle ADD COLUMN IF NOT EXISTS minutos_espera_ventana DOUBLE PRECISION;
        ALTER TABLE rutas_detalle ADD COLUMN IF NOT EXISTS minutos_tarde_ventana DOUBLE PRECISION;
        ALTER TABLE rutas_detalle ADD COLUMN IF NOT EXISTS secuencia_entrega INTEGER;
        ALTER TABLE rutas_detalle ADD COLUMN IF NOT EXISTS modelo_distancia VARCHAR(16);
        UPDATE rutas_detalle SET estado_eta = 'calculado'
        WHERE estado_eta IS NULL AND eta IS NOT NULL;
        UPDATE rutas_detalle SET estado_eta = 'sin_datos'
        WHERE estado_eta IS NULL AND eta IS NULL;
        UPDATE rutas_detalle SET minutos_espera_ventana = 0
        WHERE minutos_espera_ventana IS NULL;
        UPDATE rutas_detalle SET minutos_tarde_ventana = 0
        WHERE minutos_tarde_ventana IS NULL;
        UPDATE rutas_detalle SET modelo_distancia = 'geodesica'
        WHERE modelo_distancia IS NULL;
        """,
    ),
)


async def apply_migrations(connection: AsyncConnection) -> None:
    await connection.execute(
        text(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version VARCHAR(64) PRIMARY KEY, aplicada_en TIMESTAMPTZ NOT NULL DEFAULT now())"
        )
    )
    for version, sql in MIGRATIONS:
        applied = (
            await connection.execute(
                text("SELECT 1 FROM schema_migrations WHERE version = :version"),
                {"version": version},
            )
        ).scalar()
        if applied is not None:
            continue
        for statement in _split_sql(sql):
            await connection.execute(text(statement))
        await connection.execute(
            text("INSERT INTO schema_migrations (version) VALUES (:version)"),
            {"version": version},
        )


def _split_sql(script: str) -> list[str]:
    return [chunk.strip() for chunk in script.split(";") if chunk.strip()]
