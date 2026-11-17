# Fase 1 — Seguridad, estados y WebSockets

17/11/2026 America/Lima; main/b47d5eb7cda26444c56460ea74591cc5f973e0b3 + cambios sin commit. Código autorizado; PostgreSQL nuevo tmpfs verificado, no BD existente.

## Resultado

AF-01: corregido criterio histórico por snapshot computed/published más reciente de la jornada. Advisory lock transaccional común a optimización/entrega/reroute/posición; locks de pedido/asignación/actor. El conductor anterior no entrega/cancela tras A→B. Prueba de carrera: B sin commit y entrega A en espera; al confirmar B, A se rechaza sin cambiar el pedido. No se borran planes anteriores.

AF-02: matriz única order_lifecycle; validación previa de todo el lote, terminales protegidos en cancelación/reroute/publicación; entrega repetida no crea segunda transición. La aplicación de reroute conserva rechazo B-08 y avisos después de commit. No se admite reenviar entregado a assigned/cancelled.

AF-03: salas públicas separadas y whitelist solo de estado/ETA del propio pedido, sin GPS, códigos internos, IDs, incidentes ni secuencias. Snapshot público usa pedido/detalle vigente, no posiciones en memoria. Desconexión por channel_code efectivo. UI pública ya no consume GPS crudo ni estados de terceros; personal conserva contrato interno.

AF-06: jti + huella de credencial/rol en JWT; revocación durable en Bitacora existente (solo jti, nunca JWT), endpoint /auth/salir y llamada de cliente; revalidación por mensaje y watchdog de 1 s aun inactivo, cambio de rol/asignación/activo y bloqueo de cuenta; límite 30 mensajes/10 s conductor y tamaño 8000 caracteres. Clientes usan subprotocolo bearer en vez de token en URL; query token solo compatible en demo. Tokens previos sin campos nuevos requieren ingresar de nuevo. **Parcial** hasta revisión de configuración de proxy/logs real, límites globales de infraestructura y revisión de secretos AF-29. No se cambia SECRET_KEY ni se revoca secreto real.

## Pruebas actuales

- Base previa: 185 backend pasan.
- Regresiones iniciales rojas: cinco; el primer REST usaba identificador demasiado corto y respondió 400, por lo que no se usa ese resultado como prueba de IDOR. Entrada corregida; asociación histórica y transiciones sin protección sí reproducidas.
- 11 regresiones nuevas verdes con PostgreSQL y TestClient reales, incluyendo salas con dobles de sockets (esa parte es unidad) y conexión pública/limpieza, REST A→B, terminales, carrera, revocación, expiración inactiva y rol.
- Suite completa fase1-regresion: **196 PASARON, 0 fallos, 0 omitidas, 36,43 s**. Evidencia: CORRECCIONES_EVIDENCIAS/fase1-regresion/backend-junit.xml/log.
- Carrera ampliada: 11 PASARON, 6,13 s, fase1-carrera. Suite B-08 preservada (28 unidades +14 BD dentro de las 196).
- Frontend fase1-frontend-final: 68 PASARON/1 FALLÓ, únicamente AF-24 preexistente. Prueba App actualizada para exigir token fuera de URL; no se eliminó cobertura de optimización. Cambio posterior de UI de tracking se validará de nuevo antes de fase 2.
- TypeScript sin emisión PASÓ. git diff --check PASÓ (avisos LF/CRLF no son errores).

Los intentos intermedios están conservados. Un doble B-08 no implementaba execute del lock; se extendió el doble, sin debilitar aserciones. Una prueba nueva de cambio de rol contaminó usuario en la BD efímera; se corrigió con finally y se repuso exclusivamente la cuenta sintética. Suite completa posterior verde. No se ocultaron estos fallos ni se aplicaron cambios a una BD previa.

## Archivos de esta fase

app/services/active_plan.py y order_lifecycle.py nuevos; app/api/v1/routes.py, websockets.py y auth.py; app/api/deps.py; app/services/driver_assignment.py, realtime_router.py, tokens.py; src/App.tsx, App.test.tsx, components/driver/DriverApp.tsx, lib/session.ts, pages/Tracking.tsx y tracking.test.tsx; tests/test_post_audit_security.py nuevo y test_publication_b08.py (doble de transacción). Sin nueva dependencia ni migración.

## Control de salida

AF-01/02/03 se consideran corregidos con evidencia focalizada y regresión, sujetos a reauditoría final. AF-06 parcial y AF-29 pendiente de escaneo. No hay P0 reproducible conocido pendiente en los caminos corregidos. Los datos EVM/aceptación siguen bloqueados individualmente; no detienen integridad operativa independiente. Próxima fase: snapshot/entrega real/indicadores/reportes y AF-24; sin almacenar fotos/firmas sin política ni aplicar DDL a BD existente.
