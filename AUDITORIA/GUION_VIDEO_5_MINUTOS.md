# Guion de video — aproximadamente 5 minutos

17/11/2026, America/Lima; V_1_0_0. **Estado: guion/storyboard preparados; MP4 no creado ni verificado.** No hay demo continua en navegador aceptada y siguen bloqueantes. Este documento no equivale a evidencia audiovisual entregada.

Destino autorizado cuando exista grabación real: `docs/05 Video proyecto/` y archivo con extensión `.mp4`. No se creó archivo ficticio, captura falsa, audio sintético atribuido al equipo ni montaje de tests presentado como sistema vivo. No se creó carpeta vacía para simular entrega.

## 1. Elevator Pitch — 0:00 a1:00

Texto propuesto para voz real del equipo, ritmo a ensayar (no duración medida):

> Planificar un reparto implica decidir qué vehículo atiende cada pedido y en qué orden, sin exceder su capacidad ni incumplir ventanas de entrega. EcoLogística propone reunir estas decisiones en una plataforma web para el caso académico de Huancayo, El Tambo y Chilca. El operador gestiona flota y pedidos, ejecuta un algoritmo genético y consulta rutas en mapa o tabla; el conductor dispone de su secuencia y el equipo consulta indicadores y reportes. La propuesta incorpora estimaciones de emisiones para comparar alternativas y hacer visible su impacto ambiental. Nuestro avance se respalda con pruebas, y reconocemos sus límites: las estimaciones ambientales no son ahorros mensuales medidos ni compensaciones ejecutadas. El objetivo es apoyar un reparto más organizado con decisiones trazables; su aceptación completa sigue pendiente de resolver y validar las brechas publicadas.

Visuales propuestos: nombre/problema/ámbito documentado y luego sistema real del candidato de prueba. No usar logos de clientes reales ni testimonios inventados. Si el texto excede el minuto al leerlo, ajustar extensión manteniendo las limitaciones y no acelerar de forma ilegible.

## 2. Storyboard funcional — 1:00 a5:00

Todas las escenas requieren grabación real posterior y ensayo del [guion de20 min](GUIA_SUSTENTACION_20_MINUTOS.md). Datos sintéticos, entorno descartable, roles y versión identificados. Las capturas de componentes/tests actuales no son una demo frontend–backend continua.

| Tiempo / duración | Escena / acción real a grabar | Voz en off propuesta | Evidencia y transición | Estado previo a grabar |
|---|---|---|---|---|
|1:00–1:25 /25 s|Ingreso con operador ya preparado, rol/jornada visibles; petición API real sin token expuesto |«Trabajamos con una jornada y datos de prueba identificados. El rol determina qué acciones puede ejecutar cada usuario.» |Corte desde pitch a pantalla; fuente pruebas auth/roles. No mostrar claves |Ensayo UI real pendiente. |
|1:25–2:00 /35 s|Flota consultada y pedidos sintéticos importados/validados; recargar para comprobar persistencia |«La planificación parte de capacidad, ubicación y ventanas. Los errores deben corregirse antes de generar una ruta.» |Mostrar respuesta de importación y mismo pedido tras recarga; admin solo si alta flota |DEF-01/atributos incompletos deben resolverse o limitarse honestamente. |
|2:00–2:55 /55 s|Ejecutar GA sobre lote factible ensayado; mostrar metadata y mapa/tabla de la misma versión |«La publicación aplica restricciones duras. Una salida inválida se rechaza antes de guardar o notificar éxito.» |HTTP 201/versión y detalle de paradas; transición sin insertar resultados ajenos |B-08 backend está probado; navegador/OSRM real y candidato aceptado pendientes. |
|2:55–3:40 /45 s|Vista conductor asignado, entrega y recarga; no usar conductor ajeno |«El conductor registra el estado de su pedido. La conexión con el backend debe conservar el cambio al consultar de nuevo.» |Estado antes/después observable. No afirmar comprobante/fecha durable si no se completaron |Autorización vigente/terminalidad/fecha/comprobante son bloqueantes de aceptación. |
|3:40–4:30 /50 s|Dashboard y PDF del mismo periodo, abrir archivo legible |«Los indicadores y el reporte deben usar el mismo rango, versión, unidades y factores. Se trata de estimaciones del transporte, con sus límites declarados.» |Datos conciliados, filtro visible, PDF abierto; no prometer ahorro/ISO |Conciliación B-12/13/14/17 y ensayo pendientes. |
|4:30–5:00 /30 s|Rechazo seguro o recálculo de un vehículo solo si fue ensayado; cierre breve con límite |«La validación evita publicar soluciones que incumplen restricciones. Mostramos únicamente el alcance comprobado y mantenemos pendientes explícitos.» |Evento solo tras commit, sin datos de seguimiento público. Si no cumple, no anunciar éxito |No prometer redistribución por avería ni SLA<30 s sin prueba; decisión de escena tras ensayo. |

Total demo 4:00; pitch 1:00; total previsto 5:00. Evitar cortes que oculten un error y lo hagan pasar por transacción exitosa. Un material de pruebas o respaldo puede mostrarse con etiqueta propia, pero no reemplaza la demostración funcional exigida.

## 3. Plan preciso de grabación y verificación pendiente

1. Resolver bloqueantes del candidato o acordar formalmente alcance de demostración; conseguir ensayo completo con API/BD reales y cifras correctas. No modificar código durante estas fases para poder grabar.
2. Preparar dispositivo/captura de pantalla y micrófono del equipo, ventana sin credenciales/notificaciones personales y datos sintéticos. Captura/voz no se utilizaron en esta ejecución. La disponibilidad de un codificador por sí sola no valida contenido ni permite fabricar un video.
3. Grabar pitch y recorrido del mismo candidato/entorno; unir en un MP4 continuo con ambos segmentos. Conservar transiciones claras y tamaño de texto legible; objetivo HD para sobresaliente. No incluir secretos ni datos reales de clientes/conductores.
4. Guardar únicamente en `docs/05 Video proyecto/`. Si ya existe un archivo en ese momento, crear versión nueva sin sobrescribir evidencia anterior.
5. Reproducir inicio a fin; confirmar audio, imagen, continuidad, casos y conexión real. Medir duración: suficiente≈5 min±30 s; objetivo sobresaliente 5 min±15 s según rúbrica. No hay duración medida actualmente.
6. Registrar archivo/ruta/hash/duración/formato/fecha/versión del sistema, responsable real, reproducción y fallos en una versión posterior de revisión final. Solo entonces marcarlo creado/verificado.

## 4. Estado al corte

**MP4 pendiente.** No se observó demo continua de navegador ni se alcanzó puerta de aceptación técnica; las brechas impiden presentar una grabación como producto final aprobado. No hay archivo reproducido, grabación de voz ni evidencia audiovisual que calificar. Responsable de grabación/voz y fecha: por confirmar por el equipo, no asignados ficticiamente.
