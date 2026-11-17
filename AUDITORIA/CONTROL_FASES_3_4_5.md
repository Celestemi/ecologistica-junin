# Control de ejecución autónoma — fases 3, 4 y 5

Fecha de corte: 17/11/2026, America/Lima. Instrucción: `../CODEX_AUTOMATIZACION_FASES_3_4_5.md`, leído completo. Raíz accesible confirmada: `C:/Users/Baguette/Documents/Proyectos/ecologistica-junin`; Proyectos 2 no disponible. Rama main, HEAD `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1`; se evalúa el árbol de trabajo con B-08 sin commit.

## Entrada a fase 3 — registrada antes de ejecutar pruebas

- Autorización: validación sin correcciones de código ni cambios de datos operativos; resultados/cachés exclusivamente en AUDITORIA.
- Preexistentes modificados: `app/api/v1/routes.py`, `app/api/v1/websockets.py`, `app/services/realtime_router.py`, `app/services/route_constraints.py`, `tests/test_hard_constraints_us008.py`. Preexistentes sin rastrear: cuatro planes de fase 1, informe B-08, dos pruebas B-08 y archivo maestro. Se conservarán íntegros; manifest SHA-256 en memoria antes de trabajar.
- Fuentes: HTML final disponible en Downloads y plantillas originales leídas; consigna inicial original ausente del repositorio. La falta de esa fuente limita contraste de alcance, no autoriza reconstruirla.
- Entorno actual: Python 3.11.17 en .venv, Node v24.22.1; Docker Server 29.7.2 disponible ahora, sin contenedores en ejecución y con imagen local PostGIS 15-3.4. Esto difiere del bloqueo de la fase 2 y debe verificarse de nuevo.
- Aislamiento previsto: contenedor nuevo exclusivo, imagen ya presente sin descargas, puerto loopback nuevo 55434, datos PostgreSQL en tmpfs sin volumen/carpeta de usuario, sin logs persistentes Docker; fixtures solo sobre ecologistica_test de este servidor nuevo. No usar bases/volúmenes previos. Inicialización/esquema y resets solo dentro de este entorno descartable; archivos de migración intactos.
- Backend: inspeccionadas fixtures que crean BD, TRUNCATE y usuarios; verificar identidad del contenedor/puerto y ausencia de montajes persistentes antes de permitirlas. Si falla el aislamiento, omitir integración y registrar bloqueo.
- Frontend: ejecutar suites con servicios simulados, sin build; cachés, cobertura y resultados dirigidos a AUDITORIA; configuración temporal de ejecución sin editar los archivos del proyecto. No equiparar componentes con E2 E.
- Límite: defectos críticos impedirán aceptación técnica y grabación de una demo presentada como válida. Se continuará únicamente con informes verificables y preparación documental expresamente permitida por las puertas del archivo maestro.

## Control posterior

Se completará por adición al terminar cada fase, con fuentes y resultados reales. Este registro no acredita todavía pruebas, cierre ni video.

## Salida de fase 3 y puerta de entrada a fase 4

Verificados al 17/11/2026:185 pruebas backend aprobadas (incluye 14 B-08 PostGIS),68 frontend aprobadas/1 fallida de69,4 SW aprobadas y tipado/dist estático aprobados. Fuentes originales en FASES_3_4_5_EVIDENCIAS. Backend líneas 83,27%/ramas 59,98%/combinado 78,68%; frontend líneas 78,80%. Tres mediciones del solver 150 ×15 asignan 150 pero son infactibles; no acreditan SLA HTTP. No se corrigió código.

Infraestructura efectiva: el puerto 55434 estaba excluido por Windows; se creó nuevo contenedor 7 ce9 d5 f3… en loopback 25435, sin volúmenes persistentes y PostgreSQL en tmpfs. Se comprobó disponibilidad y se ejecutaron fixtures solo en ecologistica_test de ese servidor nuevo. Contenedor detenido y retirado automáticamente tras pruebas. No datos operativos ni archivos de migración modificados.

Existen los cuatro informes de fase 3. Bloqueos de aceptación: DEF-02/03/04 seguridad/integridad/privacidad, frontend rojo, SLA no acreditado, EVM y cierre sin registros. **No se avanza a aceptación técnica, administrativa ni a grabación como producto aprobado.**

**Entrada a fase 4 autorizada únicamente como borradores** por la puerta 3→4 del archivo maestro: HTML final y siete plantillas exactas disponibles/extractadas; se preservarán sus títulos/orden/tablas/campos/fórmulas, con ausencias explícitas. Consigna inicial original ausente, sin inventarla. Se crearán siete archivos nuevos en docs/04 Cierre y siete enlaces mínimos en README; no se modificarán documentos históricos ni código. No acta ni costos ficticios. Aprobación del cierre permanece pendiente.

## Salida de fase 4 y puerta de entrada a fase 5

Se generaron los siete archivos oficiales V_1_0_0 como **borradores verificables** y VALIDACION_DOCUMENTOS_CIERRE.md. Estructuras extraídas de la fuente, fórmulas conservadas, ausencias económicas/visuales/de aceptación explícitas; sin marcadores ni cifras EVM inventadas. README recibió siete enlaces por agregado, con prefijo original preservado (readme_update.json). No se modificaron fuentes/pruebas/configuración ni documentación histórica.

**Puerta 4→5 permite exclusivamente preparación:** datos insuficientes impiden completar todo lo exigido y no hay acta/aceptación/cierre administrativo. Se prepararán guiones 20/5 min y revisión/checklist; no se publicará ni se grabará una demo simulada, ni se declarará MP4 entregado. Los pasos funcionales aún no observados en navegador se marcarán condicionados. La confirmación final de enlaces/integridad se registrará al terminar las tres fases.


## Salida de fase 5 y control final

Se crearon guía de sustentación, guion/storyboard de video, checklist y resultado de revisión. Gestión 10 min/demo 10 min y pitch 1 min/demo 4 min son tiempos propuestos, no ensayos medidos. MP4 no creado; demo continua en navegador, registros económicos y aceptación real pendientes. No se eludieron bloqueantes para presentar cierre aprobado.

Validación estructural final aprobada:7 nombres exactos,7 enlaces de ida,7 retornos,152 comprobaciones de títulos/campos, sin marcadores ni enlaces rotos en documentos nuevos/README. La comparación SHA-256 confirmó cero bajas/cambios fuera de alcance y solo README modificado entre archivos preexistentes; prefijo original preservado. Fuentes/pruebas/configuración y material previo del usuario intactos. El inventario exhaustivo y controles están en FASES_3_4_5_EVIDENCIAS/archivos_generados.json y validacion_final.json. No commits/push, correcciones, instalaciones ni cambios productivos.
