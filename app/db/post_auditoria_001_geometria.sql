-- Propuesta versionada AF-12, SRID 4326 del esquema actual.
-- NO integrada al arranque. Aplicar a BD existente requiere autorización y backup.
-- Probada solo en tabla legado sintética TEMP de PostgreSQL descartable.
ALTER TABLE rutas_detalle
ADD COLUMN IF NOT EXISTS geometria_tramo geometry(LINESTRING, 4326);
