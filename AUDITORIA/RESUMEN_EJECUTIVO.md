# Resumen ejecutivo de la auditoría

**EcoLogística — corte al 16 de noviembre de 2026 (America/Lima).**
Repositorio: C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin.
Commit de referencia: 967efdfac77d14eb0ffb14210637640c13f9c332.

## Resultado principal

| Pregunta | Dictamen |
|---|---|
| Sprint actual | **Sprint 3 en consolidación**, con deuda funcional/de aceptación de Sprint 2. |
| Sprint más avanzado con código | **Sprint 4**, por reoptimización y medidas avanzadas parciales del GA. |
| Último sprint completamente terminado | **Ninguno acreditado** con todos sus entregables y evidencia de aceptación/DoD. |
| Avance general estimado de implementación | **53,5 %**. |
| Avance Sprint 1 / 2 / 3 / 4 | **85 % / 70 % / 50 % / 26 %**, respectivamente. |
| Implementación parcial estimada del MVP | **67,1 %**, promedio de RF-01…RF-07. |
| Cumplimiento estricto acreditado del MVP | **0 de 7 requisitos completos y verificados: 0 %**. No se acredita el umbral. |
| Mínimo para alcanzar ≥70 % | **5 de 7 RF completos = 71,4 %**. |

El 0 % es el resultado del criterio de aceptación integral solicitado: cada RF del MVP conserva una brecha identificada, aunque sus subfunciones tengan código conectado y pruebas. **No significa que el sistema carezca de funcionalidad ni que todos sus módulos fallen.** Tampoco se confunde el promedio parcial de 67,1 % con cumplimiento del umbral.

Fórmula del general: 70 % × promedio RF (52 %) + 20 % × promedio RNF (42,857 %) + 10 % × análisis/diseño (85 %) = 53,471 %, redondeado a 53,5 %. Los pesos son una decisión explícita de esta auditoría, no un dato de la consigna. Las listas de diez comprobaciones por RF/RNF permiten reproducirlos; representan estimación de implementación, no porcentaje de funcionamiento observado.

## Qué está implementado y qué falta

**Subfunciones implementadas en código:** autenticación y roles, alta/edición/estado de flota, importación CSV/XLSX y ventanas, geocodificación por hitos/corrección manual, GA real con OX/mutaciones/torneo, validaciones normales de capacidad, mapa/tabla/detalle, KPI desde persistencia, descarga PDF y operación básica del conductor con cola IndexedDB.

**Módulos integrales completos y verificados:** ninguno acreditado según los requisitos completos de la consigna. La comprobación de tipos frontend pasó y cuatro pruebas unitarias del Service Worker aprobaron; esto respalda partes específicas.

**Parciales:** flota 90 %, pedidos 65 %, optimización 75 %, mapa 80 %, dashboard 55 %, reportes 65 %, dinámica 40 %, conductores 25 %, compensación 25 %.

**Pendientes identificables:** gestión de clientes 0 %, integración con API de tráfico, ficha/licencias/turnos de conductores, prioridad/producto y volumen integral, redistribución por avería/accidente, ahorro económico/puntualidad real, plan de compensación ejecutable, aceptación final, manuales completos y presentación final.

## Problemas que bloquean la entrega

1. Reoptimización persiste soluciones sin pasar el validador normal; mapa informa factibilidad fija. Puede publicar una solución inválida.
2. Recálculos/copias dejan totales, geometría y ETA inconsistentes; dashboard/PDF suman versiones que pueden representar el mismo trabajo.
3. Seguimiento público WebSocket recibe payload interno con GPS exacto/identificadores y secuencias; autorización por asociación histórica permite acciones tras reasignación; cancelación puede cambiar un entregado.
4. Solver no acredita solución válida completa 150×15 ≤45 s ni reoptimización <30 s; el test SLA no exige factibilidad total.
5. Fecha real de entrega no se persiste; PDF usa ETA/ventana. Firma/foto del conductor no se conservan ni envían.
6. Upgrade de geometría carece de migración explícita, área es provisional y fórmulas ambientales divergen.
7. Configuración demo/HTTP no acredita producción segura; staging es un placeholder; estado realtime solo reside en memoria.
8. dist/sw.js preexistente es antiguo y falla el script de validación de artefactos; no se deduce de ello qué versión está desplegada.

Son hallazgos de código/artefactos; sus efectos de explotación o carga no se provocaron. La documentación del Sprint 3 declara cierre mientras README y otros informes mantienen pendientes; no se toma esa declaración como prueba suficiente.

## Siguiente actividad recomendada

Ejecutar un **sprint de cierre del MVP**, empezando por publicación válida común, autorización vigente y minimización del WS; después corregir versiones/totales/fechas y completar flota/pedidos. Validar el solver y los flujos integrados en entorno aislado en una etapa de desarrollo autorizada.

La ruta cercana al umbral es cerrar RF-01, RF-02, RF-03, RF-04 y RF-06, sin tolerar defectos transversales de seguridad/integridad para alcanzar el número. El backlog contiene tareas, dependencias, archivos y criterios de aceptación; no se implementó ninguna.

## Verificaciones y limitaciones

- TypeScript sin emisión: **aprobado**.
- Service Worker en VM: **4/4 aprobadas**.
- Auditoría de dist existente: **falló** en scripts/audit-green-build.mjs:14, por formato de SW antiguo.
- No se ejecutaron backend/BD, migraciones, algoritmo persistente, Docker, build, instalaciones ni suites que pudieran escribir fuera de AUDITORIA.
- El comando python no dispone de un intérprete operativo; no se instaló ninguno.
- Cobertura histórica leída: backend 81,07 % líneas, 55,17 % ramas y 76,02 % combinado; frontend 90,91 % líneas y 84,52 % ramas. No son resultados de esta auditoría ni aceptación integral.
- Sin acceso a la instancia activa no se confirman esquema físico, registros, certificados, disponibilidad, rendimiento de despliegue ni servicios externos.
- No se acredita conformidad integral W3C/WCAG, ISO/IEC 25010, OWASP, Green Software o ISO 14083. Las fuentes oficiales y el alcance están en el informe de cumplimiento.

## Documentos generados y rutas exactas

Los cinco documentos se guardan directamente en el único directorio autorizado, sin subcarpetas:

1. [AUDITORIA_ESTADO_ACTUAL.md](AUDITORIA_ESTADO_ACTUAL.md)  
   C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin/AUDITORIA/AUDITORIA_ESTADO_ACTUAL.md
2. [ANALISIS_SPRINTS.md](ANALISIS_SPRINTS.md)  
   C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin/AUDITORIA/ANALISIS_SPRINTS.md
3. [CUMPLIMIENTO_REQUERIMIENTOS.md](CUMPLIMIENTO_REQUERIMIENTOS.md)  
   C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin/AUDITORIA/CUMPLIMIENTO_REQUERIMIENTOS.md
4. [BACKLOG_IMPLEMENTACION.md](BACKLOG_IMPLEMENTACION.md)  
   C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin/AUDITORIA/BACKLOG_IMPLEMENTACION.md
5. [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)  
   C:/Users/Baguette/Documents/Proyectos2/ecologistica-junin/AUDITORIA/RESUMEN_EJECUTIVO.md

## Control de cambios

Se verificaron mediante SHA-256 los **247 archivos inventariados fuera de AUDITORIA**, incluyendo fuentes, configuración, documentación y artefactos/cachés locales. **No se detectaron modificaciones, altas ni bajas en ese inventario** durante la auditoría. Los árboles .git, node_modules y .venv se excluyeron del inventario de contenido; no se ejecutaron comandos de instalación ni operaciones que pretendieran modificarlos.

El estado Git conserva **18 eliminaciones preexistentes** fuera de AUDITORIA (15 documentos de Auditorias-EcoLogistica y tres de docs), identificadas antes de trabajar. No se atribuyen a esta auditoría ni se restauraron. La única alta adicional de Git corresponde a AUDITORIA con los cinco informes.

No se modificó código fuente ni base de datos, no se sobrescribieron documentos preexistentes y no se generaron archivos temporales, logs ni cachés fuera de AUDITORIA.
