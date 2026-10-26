"""Conjuntos de roles alineados a la matriz RBAC (08. Usuarios V_1_0_3)."""

from app.models.enums import RolUsuario

DESK_READ = (
    RolUsuario.ADMIN,
    RolUsuario.OPERADOR,
    RolUsuario.GERENTE,
    RolUsuario.AUDITOR,
)

ORDER_WRITE = (RolUsuario.ADMIN, RolUsuario.OPERADOR)

FLEET_READ = DESK_READ
FLEET_CREATE = (RolUsuario.ADMIN,)
FLEET_UPDATE = (RolUsuario.ADMIN, RolUsuario.OPERADOR)

MAP_READ = (
    RolUsuario.ADMIN,
    RolUsuario.OPERADOR,
    RolUsuario.GERENTE,
    RolUsuario.AUDITOR,
    RolUsuario.CONDUCTOR,
)

OPTIMIZE = (RolUsuario.OPERADOR,)

REPORT_READ = DESK_READ

AUDIT_READ = (RolUsuario.ADMIN, RolUsuario.AUDITOR)

FIELD_DRIVER = (RolUsuario.OPERADOR, RolUsuario.CONDUCTOR)

DENY_ANON = "Debes iniciar sesión."
DENY_ROLE = "Tu rol no tiene permiso para esta operación."
