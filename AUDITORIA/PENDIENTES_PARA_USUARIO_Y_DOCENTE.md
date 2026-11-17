# Pendientes para el usuario, equipo y docente

17/11/2026 America/Lima. Base main/b47d5eb7cda26444c56460ea74591cc5f973e0b3 + árbol sin commit. Las fases0–5 se ejecutaron en orden; el cierre del proyecto continúa sin acreditar. Estos pedidos identifican fuentes/decisiones necesarias, no actas ya celebradas ni autorización solicitada por esta ejecución. No se envió ningún mensaje a terceros.

| Prioridad · AF / H | Aportación o decisión concreta | Quién puede aportarla (rol propuesto) | Verificación posterior |
|---|---|---|---|
|P0 AF-04;H06/15–20 |BAC aprobado con moneda, fecha, alcance y cambios;PV/EV/AC del periodo,acumulado actual y anterior;fecha de los tres cortes;avance presupuestado aceptado,horas/gastos y comprobantes |Patrocinador/responsable financiero y responsable de gestión |Conciliar nueve valores;SV/CV/SPI/CPI,%BAC,tres EAC y selección;denominadores válidos. Formulario en SOLICITUD_DATOS_EVM.md. Presupuesto estimado no reemplaza aprobación. |
|P0 AF-05;H33/37 |Criterios de aceptación por RF/RNF,resultados reales,defectos/exenciones aceptados,instrumento y resultados de satisfacción,acta de aceptación/cierre y recepción operativa |Cliente/patrocinador,usuarios reales y equipo |Revisión por personas identificadas,fechas y evidencias;no firmar ni reconstruir firmas. Formatos en SOLICITUD_EVIDENCIAS_HUMANAS.md. |
|P1 AF-16/17;H08–13/34/35 |Cronograma base aprobado,fechas reales por hito,dependencias/ruta crítica,cambios;costos/horas ejecutados,reserva/contingencia y Look Ahead costeado |Gestión/equipo y finanzas |Comparar plan/real con causas,impacto,acciones y responsables;conciliar calendario2024/2026. |
|P1 AF-18/19/27;H23–29/44 |Exportación Jira auténtica con proyecto,consulta,zona horaria,fechas,tickets,estimaciones,cambios de alcance,transiciones por fecha y trabajo aceptado;origen de las capturas existentes |Administrador Jira/equipo |Conciliar34SP vs20 y39 vs47;series EVM/CFD/CSI/Burndown/Burnup sin interpolar observaciones. Capturas originales quedan intactas. |
|P1 AF-20/34;H30/31/38/39 |Mediciones voluntarias de clima con método/fecha;tablero/acta de retro real,participantes,acciones,responsables y seguimiento;reunión de cierre futura cuando corresponda |Equipo/participantes reales y facilitador |Distinguir histórico auténtico de recolección prospectiva;validar las ocho categorías de lecciones. |
|P1 AF-08/09/15;H50/53 |Política de comprobantes/privacidad/retención y almacenamiento;factores ambientales y energéticos aprobados por tipo/fecha,tarifas de planificación,referencia FIFO comparable y método de puntualidad/ahorro |Dueño de producto/privacidad y especialista de dominio |Completar oráculo mixto y conciliar solver→BD→KPI→PDF/CSV;no llamar gasto real/EVM al TCO estimado. |
|P1 AF-11/13/14;H50 |Contrato aprobado de jornada/carga/GPS/avería;tipo vehicular,prioridad/producto/volumen;licencias/turnos de conductores,maestro de clientes/preferencias y plan real de compensación o cambio de alcance formal |Dueño de producto/cliente/docente según autoridad |Trazar RF-01/02/07/08/09/10 y aceptación por atributo/rol;ninguna exención se presume. |
|P1 AF-12;H50/51 |Esquema legado auténtico y autorización específica para crear copia descartable sin datos personales;posterior autorización separada para migrar una BD existente |Propietario/administrador de BD |Ensayar upgrade completo/restauración/compatibilidad en copia aislada antes de aplicar propuesta. SQL actual NO integrado en inicio automático;solo TEMP sintético probado. |
|P1 AF-21/25/35;H51–56 |Navegador operativo,perfiles objetivo,entorno de exposición y permisos de ubicación;red/OSRM/tiles/TLS/WS comprobables |Usuario/equipo e infraestructura |Ejecutar GUIA_DEMO_VERIFICADA.md:ensayo de gestión10min y técnico10min reales;WCAG teclado/zoom/lector/contraste y tareas de usuarios. Host/pipe de Computer Use ausentes en esta sesión;sin capturas ni tiempos de demo inventados. |
|P1 AF-22/23/31;H14/49/56 |Infraestructura y acceso autorizados de CI/staging;revisor por pares;ventana SLI y carga objetivo,procedimiento de recuperación/rollback y responsable de recepción |Equipo/infraestructura y operación |CI/health por versión,reproducción por tercero,carga de negocio representativa,reinicio/restore y99,5 % en ventana acordada. Smoke local no prueba producción. |
|P2 AF-26/28/33;H44/47/50 |Seis fuentes históricas ausentes,consigna inicial original identificable y explicación de versiones/calendarios |Usuario/equipo/docente |FUENTES_HISTORICAS_IRRESOLUBLES.md lista destinos;reparar enlaces solo a fuentes auténticas;contrastar RF/RNF sin reescribir historia. |
|Rúbrica |Aclaración docente de cómo calificar descriptores con perfiles mixtos,si no se completan todas sus condiciones |Docente |Pesos1/1/1/4,máximo21;sin promedio/peor subindicador inventado,sin convertir no observado en0. |

## Trabajo técnico que sigue pendiente

Estos puntos no son datos que el usuario deba fabricar: requieren otra implementación/validación con los contratos y entorno anteriores disponibles. No se consideran resueltos ni automáticamente exentos:

- AF-07/09/15: completar referencias y factores por vehículo,conciliación integral de métricas,legado y revisión visual de archivos. Los reportes actuales distinguen eventos reales de estimaciones;no certifican ahorros operativos reales.
- AF-11: estado durable de operación GPS,avería con redistribución entre vehículos,carga/jornada acumulada y recuperación/multiworker;el reloj corregido y snapshot en BD no completan esos casos.
- AF-13/14: completar atributos/administración de alcance confirmado con persistencia/permisos/historial y aceptación. CSV de importación ya existía;no está pendiente implementarlo de nuevo.
- AF-06/29: validar registros del servidor/proxy y configuración real sin exponer tokens;TLS y límites globales;revisión de secretos efectivos del despliegue. El token público en path puede aparecer en logs de infraestructura aun con logger de aplicación saneado.
- AF-10/21/23/25/31/35: SLA con proveedor/red y carga representativa,ensayos UI/campo/WCAG/usuarios,CI/revisión/staging y reproducción del runbook por tercero. No hubo despliegue durante esta tarea.
- AF-26/28: recuperar fuentes y conciliar historia/versiones;31 ocurrencias siguen rotas hacia seis destinos. Documentar ausencia no repara enlaces ni concede excepción.

## Estado de entrega

Seis hallazgos resueltos con evidencia:AF-01/02/03/24/30/32;17 parciales,1 abierto,11 bloqueados/no verificables. Pruebas actuales:210 backend+70 frontend+4 SW,284 casos únicos verdes;flujo TCP con BD real pasó. La demostración integral sigue **NO VERIFICADA**, con guía disponible. Datos sintéticos y restauración solo en contenedor nuevo descartable;sin cambios en BD anteriores.

No se hicieron commits,push ni deploy. Un paquete instalado se actualizó de opentelemetry-api1.45.1 a1.45.2 por aviso oficial,con hash verificado,sin dependencias nuevas. Residual .vitest preservado. Video y carpeta correspondiente excluidos de inspección/cambios/calificación;no pendientes asociados.

[Reauditoría](REAUDITORIA_POST_CORRECCIONES.md) · [Matriz35AF](MATRIZ_AF_01_A_AF_35.md) · [Control](CONTROL_CORRECCIONES_SPRINT4.md)

