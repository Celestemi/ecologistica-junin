# Runbook técnico post correcciones — revisión1

Corte17/11/2026; main/b47d5eb + árbol sin commit. Arquitectura: React/TypeScript en src/,FastAPI/servicios/SQLAlchemy en app/,PostgreSQL/PostGIS. No microservicios nuevos ni reemplazo de stack. No hay despliegue productivo ni validación de tercero acreditados.

## Roles y contratos nuevos

Operador: flota/pedidos,CSV/XLSX,optimizador e inserción dinámica. Conductor: solo vehículo/asignación y plan vigentes; entrega idempotente. Gerente/auditor/admin:lecturas/reportes según permisos existentes. Seguimiento público:solo token opaco,estado/ETA propios,sin GPS preciso,IDs o secuencias. El mapa público muestra destino aproximado.

WS de personal usa subprotocolo bearer.<JWT> en vez de query URL. Compatibilidad de query solo en demo. No imprimir JWT. Tokens anteriores sin jti/huella nueva requieren reingreso. Logout /api/v1/auth/salir revoca jti en bitácora; caída de red al salir no garantiza que el cliente haya podido revocarlo: expiración/revalidación siguen aplicando.

Entrega registra evento v1 en Bitacora: actor por usuario_id,identificador de operación,hora cliente con zona,recepción servidor,vehículo y versión de plan. Fecha futura>5 min o sin zona se rechaza; reintento de misma operación no duplica. No se añadió almacenamiento de fotos/firmas. Legado sin evento no recibe una fecha “real” inferida de ETA.

Último snapshot por jornada es vigente; anteriores se archivan sin eliminar. Snapshot vacío impide resurrección de asignaciones. Optimización inicial rechaza409 si ya hay entregas activas; usar inserción/reoptimización. Los escritores usan advisory lock PostgreSQL común; es deliberadamente conservador y requiere carga representativa antes de escalar.

## Laboratorio seguro reproducible

Requiere herramientas/dependencias ya instaladas y Docker. Nunca apuntar runner a BD operativa. Nuevo contenedor: nombre ecologistica-post-audit-20261117,etiqueta ecologistica.purpose=post-audit-disposable,PostGIS15-3.4,puerto127.0.0.1:25436,tmpfs /var/lib/postgresql/data:rw,sin bind/volumen,log-driver none y --rm. Credenciales del laboratorio son sintéticas y solo para ese contenedor. Ver comando de creación e ID en PLAN_CORRECCIONES_EJECUTABLE.md/control; si existe un contenedor con ese nombre, comprobar identidad/montajes antes de reutilizarlo.

Comandos de prueba desde la raíz:

- powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-post-audit-tests.ps1 -Phase validacion -Coverage
- powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-post-audit-tests.ps1 -Phase validacion-frontend -Frontend -Coverage
- node node_modules/typescript/bin/tsc --noEmit --incremental false
- node --test scripts/test-service-worker.mjs

Runner verifica Docker y configura DATABASE_URL del laboratorio,clave JWT sintética,ECOLOGISTICA_TEST_DISPOSABLE=1,caché/tmp/cobertura/reportero controlados. La fixture aborta sin marcador. No forzar ese marcador para saltarse validación de aislamiento.

Para stack local de prueba: backend uvicorn app.main:app --host127.0.0.1 --port18000 --no-access-log --ws-max-size8000,con el mismo entorno sintético. Frontend: API_PROXY_TARGET=http://127.0.0.1:18000 y Vite --host127.0.0.1 --port15173 --strictPort --configLoader runner. No hace falta API pública. No trasladar credenciales demo a producción.

Scripts de integración (requieren esas variables y validan contenedor antes de reset): python -B -m scripts.post-audit-e2e y python -B -m scripts.post_audit_load. El segundo genera1000 pedidos/50 vehículos,realiza lecturas y restaura un dump **solo en otra BD nueva del mismo contenedor efímero**. Nunca ejecutarlos sobre una BD existente/importante. Sus datos no son actividad comercial ni evidencia histórica.

## Artefactos, calidad y seguridad

Logs/JUnit/JSON: AUDITORIA/CORRECCIONES_EVIDENCIAS/<fase>. Temporales/cache/build/wheel/backup: runtime/ ignorado. .vitest/json/output.json previo se conserva e ignora; no se borra. Build verificado en runtime/build-fase3; auditor acepta ese directorio como argumento sin tocar dist raíz.

Gates80 % combinado backend y80 % líneas frontend; ramas se informan aparte. CI local configurado no equivale a ejecución remota; staging placeholder no despliega. SCA: npm audit público y scripts/audit_python_osv.py (solo nombres/versiones de dependencias),scanner Git por patrones sin valores. No sustituyen revisión de infraestructura o secretos fuera del repo.

Parche actual: opentelemetry-api1.45.1→1.45.2,único paquete reemplazado,compatible por uv pip check y regresión; SHA del wheel en CORRECCION_DEPENDENCIA_SEGURIDAD.md. No se instalaron herramientas nuevas ni otras dependencias.

## Métricas y límites operativos

Dashboard/PDF totales son estimaciones de planes vigentes, no consumos medidos ni AC del proyecto. Combustión:km/rendimiento cuando existe; electricidad inferida del CO₂ con supuestos antiguos explícitos del PDF; no tarifas actuales. Factores de vehículo congelados al publicar; legado sin snapshot no obtiene validación retroactiva.

La referencia por vehículo tras mezclar recálculos no está disponible: referencia_comparable=false suprime porcentajes/equivalencias en dashboard/PDF. Costo/ahorro real,puntualidad integral y modelos de emisiones requieren validación. La equivalencia de árboles no acredita compensación ejecutada.

GPS/incidentes permanecen en memoria; snapshot de ruta/eventos sí son durables en BD. No asumir recuperación multitrabajador,averías con redistribución,jornada/carga acumulada o99,5 % de disponibilidad por estos ensayos. Carga de80 lecturas no es aceptación de todo el negocio.

## Upgrade, backup,rollback y transferencia

SQL post_auditoria_001_geometria.sql es propuesta **no conectada al autoarranque**. Solo se probó en tabla TEMP sintética; no autoriza aplicarlo a BD real. Para esa operación faltan inventario/esquema original,backup verificable,ventana,plan de rollback y permiso específico del dueño.

Backup/restore del laboratorio conserva conteos y datos sintéticos, no certifica respaldo productivo. Para producción se deben definir cifrado,retención,RPO/RTO,restauración y pruebas con acceso autorizado; no se ejecutaron aquí. No reiniciar almacenamiento tmpfs como prueba de persistencia.

Rollback de código debe revisar diff/manifiesto y restaurar solo cambios propios aprobados,preservando trabajo preexistente; no automatizar reset/clean. Revertir un parche de seguridad requiere decisión responsable y mitigación, no se recomienda volver a versión afectada sin evaluación. No borrar eventos de bitácora ni evidencia histórica.

Transición pendiente: asignar soporte/operación,entregar accesos por canal seguro,aprobar pendientes/criterios y validar guía por otra persona. Este documento no firma aceptación.
