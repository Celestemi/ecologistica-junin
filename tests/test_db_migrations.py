"""Ejecutor de migraciones SQL: no partir bloques dollar-quoted."""

from app.db.migrations import _split_sql


def test_split_sql_preserves_do_dollar_blocks() -> None:
    script = """
        ALTER TABLE vehiculos ADD COLUMN IF NOT EXISTS x INT;
        DO $$ BEGIN
            ALTER TABLE vehiculos ADD CONSTRAINT ck_x CHECK (x > 0);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        SELECT 1;
        """
    parts = _split_sql(script)
    assert len(parts) == 3
    assert parts[0].startswith("ALTER TABLE vehiculos")
    assert "DO $$ BEGIN" in parts[1]
    assert parts[1].rstrip().endswith("END $$")
    assert parts[2] == "SELECT 1"


def test_split_sql_two_do_blocks_like_migration_007() -> None:
    script = """
        ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS estado_ubicacion VARCHAR(32);
        DO $$ BEGIN
            ALTER TABLE pedidos ADD CONSTRAINT ck_a CHECK (true);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        DO $$ BEGIN
            ALTER TABLE pedidos ADD CONSTRAINT ck_b CHECK (true);
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        CREATE INDEX IF NOT EXISTS idx_x ON pedidos (id);
        """
    parts = _split_sql(script)
    assert len(parts) == 4
    assert parts[0].startswith("ALTER TABLE pedidos")
    assert "ck_a" in parts[1]
    assert "ck_b" in parts[2]
    assert "CREATE INDEX" in parts[3]
