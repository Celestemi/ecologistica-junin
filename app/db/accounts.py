"""Cuentas de demostración del aula. En un despliegue real se cambian las claves."""

from app.models.enums import RolUsuario

DEMO_PASSWORD_BY_ROLE: dict[RolUsuario, str] = {
    RolUsuario.ADMIN: "Admin.2026",
    RolUsuario.OPERADOR: "Operador.2026",
    RolUsuario.CONDUCTOR: "Conductor.2026",
    RolUsuario.GERENTE: "Gerente.2026",
    RolUsuario.AUDITOR: "Auditor.2026",
}

DEMO_ACCOUNTS: tuple[tuple[str, str, RolUsuario], ...] = (
    ("Rosa Camargo", "admin@distrirapido.pe", RolUsuario.ADMIN),
    ("Luis Huamán", "operador@distrirapido.pe", RolUsuario.OPERADOR),
    ("Pedro Quispe", "conductor@distrirapido.pe", RolUsuario.CONDUCTOR),
    ("Elena Torres", "gerente@distrirapido.pe", RolUsuario.GERENTE),
    ("Jorge Delgado", "auditor@distrirapido.pe", RolUsuario.AUDITOR),
)
