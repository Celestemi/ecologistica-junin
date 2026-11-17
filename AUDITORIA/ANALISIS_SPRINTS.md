# Análisis de sprints e iteraciones

Fecha de corte: 16/11/2026 (America/Lima).
Referencia: consigna de cuatro iteraciones, contrastada con código y documentación local.
Este diagnóstico no modifica el backlog original ni sus actas.

## Diagnóstico del sprint actual

**Sprint actual: 3, en consolidación y cierre de brechas del MVP.**
**Sprint más avanzado con funcionalidades en código: 4**, por GA con medidas de rendimiento y reoptimización parcial.
**Último sprint completamente terminado: ninguno acreditado.**

Hay solapamiento: disponer de código de una actividad posterior no cierra automáticamente una iteración anterior. El Sprint 3 es el frente funcional principal pendiente de integración/aceptación; Sprint 2 conserva brechas de datos, factibilidad y rendimiento. Deben cerrarse esas dependencias antes de declarar el MVP listo.

La organización interna no coincide exactamente con la consigna: docs/03 Implementación/Sprint 1 agrupa flota/pedidos/seguridad, mientras el Sprint 1 de la consigna es análisis/diseño. Para las tablas siguientes se usa el alcance de la consigna solicitada, no la numeración interna.

## Método y resultados

Cada sprint pesa sus actividades por igual. Se puntúa el entregable existente, con crédito parcial cuando hay evidencia incompleta o componentes sin integrar. Se muestra el cálculo para que pueda revisarse; no se estima por semanas, commits, número de archivos ni por un badge.

| Sprint | Actividades | Peso por actividad | Puntuaciones | Avance estimado | Cierre completo |
|---|---:|---:|---|---:|---|
| 1 | 5 | 20 % | 100, 75, 100, 100, 50 | **85 %** | No acreditado |
| 2 | 4 | 25 % | 90, 65, 75, 50 | **70 %** | No acreditado |
| 3 | 4 | 25 % | 80, 55, 65, 0 | **50 %** | No acreditado |
| 4 | 5 | 20 % | 50, 40, 0, 40, 0 | **26 %** | No acreditado |

Los resultados representan avance estimado del trabajo correspondiente; no son porcentaje de historias aceptadas, cobertura automatizada ni capacidad productiva. Las puntuaciones reutilizadas de RF se desarrollan en [CUMPLIMIENTO_REQUERIMIENTOS.md](CUMPLIMIENTO_REQUERIMIENTOS.md).

No se promedian estos cuatro valores para obtener avance general: las actividades tienen diferente alcance y duplicarían RF/RNF ya contados. La fórmula general 70 % RF + 20 % RNF + 10 % análisis/diseño produce **53,5 %**.

## Sprint 1 — Semanas 1 a 3: análisis y diseño

| Actividad | Estado del entregable | Avance | Evidencia encontrada | Falta para cierre |
|---|---|---:|---|---|
| Análisis de requerimientos | Completo documentalmente | 100 % | docs/01 Inicio/06 y 07; usuarios, reglas y restricciones; escenarios BDD. | Resolver equivalencias entre catálogo de consigna y catálogo atómico; aceptar baseline final. |
| Investigación del contexto logístico | Parcial | 75 % | Acta, visión, supuestos de DistriRápido y delimitación Huancayo/El Tambo/Chilca. | Validar cifras, fuentes operativas, factores y límites geográficos. El caso es ficticio y se declara ausencia de entrevistas reales. |
| Diseño de arquitectura | Completo como diseño existente | 100 % | docs/01 Inicio/12 Modelo C4 y 10 Stack; separación SPA/API/servicios/BD. | Actualizar decisiones respecto de Celery/Redis, OR-Tools/DEAP previstos frente al runtime GA propio. |
| Diseño de base de datos | Completo como artefacto de diseño | 100 % | docs/01 Inicio/11 ER y SQL; modelos activos y migraciones. | Conciliar baseline y esquema activo; diseño presente no implica que toda entidad diseñada esté implementada. |
| Mockups de interfaz | Parcial por sustitución de evidencia | 50 % | Hay pantallas React implementadas para roles y operación. Capturas existentes son de Jira. | No se encontró artefacto específico de mockups ni validación de prototipo con usuarios. Se otorga crédito parcial por diseño UI materializado, sin inventar mockups. |

Cálculo: (100+75+100+100+50)/5 = **85 %**.

Completado como artefacto: requisitos, C4/stack y ER. Parcial: investigación y evidencia de diseño de interfaz. Pendiente: aceptación trazable de mockups/contexto y alineación de alcance.

El crédito de 100 % corresponde a la existencia del entregable documental de la actividad, no a conformidad de todo su contenido. Los riesgos pendientes impiden declarar el sprint completamente terminado. Con un criterio literal que no diera crédito alguno por pantallas como sustituto parcial de mockups, el sprint sería 75 % y el general 52,5 %; se explicita esta sensibilidad.

## Sprint 2 — Semanas 4 a 7: operaciones y GA

| Actividad | Estado | Avance | Evidencia | Bloqueo de cierre |
|---|---|---:|---|---|
| Gestión de flota | Parcial | 90 % | Vehiculo; VehiculoCreate/Update; desk.create_vehicle/update_vehicle; Fleet.tsx; pruebas de flota/estado/placa. | Falta tipo_vehiculo explícito; verificar roles/flujo integral y unidades de energía. |
| Gestión de pedidos | Parcial | 65 % | Pedido, import_orders CSV/XLSX, ventanas, jornada paginada, corrección de ubicación, OrdersDay.tsx. | Sin prioridad/producto; volumen no atraviesa todo el contrato; geocodificación por hitos y polígono provisional. |
| Generación mediante metaheurística básica | Parcial | 75 % | GA real: OX, torneo, mutación, elitismo y fitness; POST /optimizar-rutas con persistencia. | Matriz desconocida puede aprobar ventanas; factibilidad no garantizada y restricciones personales incompletas. |
| Pruebas iniciales de rendimiento | Parcial | 50 % | optimizer_benchmark.py, test_solver_sla_en001.py y reportes narrativos Sprint 2. | No hay prueba concluyente actual de solución válida completa 150×15, ni tiempo HTTP total con OSRM. |

Cálculo: (90+65+75+50)/4 = **70 %**.

La puntuación 50 % de pruebas se divide en cuatro evidencias con peso 25 %: dataset reproducible presente 100 %, suite de medición presente 100 %, resultados originales actuales vinculados a esta revisión 0 %, validación extremo a extremo de solución válida en SLA 0 %. Existen narraciones históricas, pero el informe original de benchmark está eliminado previamente y no se consultó desde Git para sustituir el estado del árbol.

Completado en subcapacidades: flota básica, importación y mecanismos GA. Ninguna de las cuatro actividades integrales está aceptada como terminada. El objetivo de generar una ruta válida no se satisface solo por terminar rápido o asignar al menos un pedido.

El test lento :64 exige tiempo <= presupuesto +0,05, al menos una generación y alguna asignación; no comprueba feasible ni 150/150. El presupuesto interno tampoco limita toda la preparación geométrica y persistencia.

## Sprint 3 — Semanas 8 a 11: mapa, indicadores, sostenibilidad y tráfico

| Actividad | Estado | Avance | Evidencia | Bloqueo de cierre |
|---|---|---:|---|---|
| Visualización de rutas en mapas | Parcial | 80 % | MapView, RouteTable y StopDetail; GET /rutas/mapa; geometría OSRM, selección por vehículo, tabla alternativa. | Geometría/metadatos incompletos en copia de recálculo; tráfico ausente; verificación real integrada pendiente. |
| Dashboard | Parcial | 55 % | summarize_indicators; GET /indicadores con fechas; Dashboard.tsx. | Sin ahorro monetario ni cumplimiento real; mezcla de versiones/galones y actualización por misma fecha. |
| Reportes de sostenibilidad | Parcial | 65 % | PDF ReportLab, costos supuestos, tablas ambientales y botón de descarga. | Totales duplicables, fecha estimada presentada como fecha de entrega, factores sin calibración y periodo de UI desconectado. |
| Integración con API de tráfico | Pendiente | 0 % | No se identifica proveedor/cliente/credencial de tráfico; OSRM declara que no aporta tráfico real. | Implementar proveedor o fuente acordada y usar sus datos en tiempos, mapa y recálculo. |

Cálculo: (80+55+65+0)/4 = **50 %**.

La API OSRM consulta red vial con perfil driving, distancia, duración y geometría. Los botones “tráfico denso” generan eventos manuales y un multiplicador fijo 1,8; no son integración con una API de tráfico. Google Maps/Waze son enlaces externos para navegar, no datos de tráfico ingeridos por el optimizador.

La PWA parcial es trabajo transversal adicional de la planificación interna. Se reconoce como código existente; no sustituye las cuatro actividades solicitadas ni aumenta artificialmente el porcentaje del sprint.

### Conflicto de actas

- README:11 y :111 mantienen historias Sprint 3 sin Done y pendientes de demostración/DoD.
- docs/03 Implementación/Sprint 3/01 Revisión del Sprint V_1_0_0.md declara US-010…015 y EN-004 cumplidas, 143 tests backend y 68 frontend.
- El reporte de calidad cita 136/67 y métricas históricas; los artefactos actuales no incluyen una ejecución nueva equivalente.
- La documentación Green IT mantiene offline E2E pendiente y declara cifras de energía hipotéticas.

Estas declaraciones se conservan, pero no se elige la más optimista como evidencia concluyente. El código confirma brechas específicas y la auditoría no pudo reproducir el despliegue sin incumplir las reglas de escritura/mutación.

## Sprint 4 — Semanas 12 a 14: robustez y entrega

| Actividad | Estado | Avance | Evidencia | Falta |
|---|---|---:|---|---|
| Optimización avanzada | Parcial | 50 % | Caché de evaluaciones, matriz por bloques, semilla, ajuste de población/generaciones, worker acotado y estancamiento. | Benchmark calidad/tiempo representativo, reparación de factibilidad y búsqueda mejorada validada. |
| Reoptimización dinámica | Parcial | 40 % | WebSockets, incidentes, cancelación/inserción y recálculo de un vehículo. | Multivehículo/avería, reloj/carga, controles de publicación, consistencia e incidentes persistentes. |
| Pruebas de aceptación | Pendiente | 0 % | Hay unitarias/componentes/integración escritas y reportes históricos. | No se encontró suite/acta integral de aceptación con usuarios, entorno/commit y criterios del MVP. |
| Documentación final | Parcial | 40 % | README, C4/ER, requisitos, docstrings y evaluaciones de calidad. | Manuales, operación/API consolidada y resolución de contradicciones; varios documentos fueron eliminados antes de auditoría. |
| Presentación final | Pendiente | 0 % | No se identificó presentación final ni guion/demo reproducible de entrega. | Preparar materiales y evidencia de demostración aceptada. |

Cálculo: (50+40+0+40+0)/5 = **26 %**.

Optimización avanzada: seis comprobaciones iguales; caché 100, escalado 100, matriz por bloques 100, factibilidad robusta 0, calidad comparativa reproducida 0, SLA integral 0: 50 %. Documentación final: cinco comprobaciones; base técnica 100, informes 100, manual usuario 0, manual admin/operación 0, paquete coherente final 0: 40 %.

Los documentos nuevos de AUDITORIA **no se usan para aumentar este puntaje**: describen el estado previo, no constituyen los manuales ni entregables funcionales faltantes.

## Cierre formal y DoD

La DoD interna exige cobertura >=80 %, análisis sin vulnerabilidades altas/críticas ni deuda bloqueante, revisión por pares, staging automatizado y API actualizada (docs/02 Planificacion/01, sección 2).

Estado de evidencia:

| Criterio | Resultado de auditoría |
|---|---|
| Cobertura | Artefactos históricos: backend 81,07 % líneas y 76,02 % combinado; frontend 90,91 % líneas. No se reejecutaron; debe aclararse métrica y versión. |
| Análisis estático | Reporte histórico Sonar gate OK para código nuevo; incidencias históricas requieren revisión de contexto. No se consultó servidor ni se acreditó cierre actual. |
| Peer review | Sin evidencia suficiente de PR aprobado vinculada a esta entrega dentro de lo inspeccionado. |
| Staging | Workflow tiene un placeholder, no despliegue automatizado efectivo. |
| API/documentación | Esquema en código y docs condicionales; manuales y consolidación pendientes. |

Por ello, incluso las subcapacidades funcionales bien implementadas no permiten afirmar cierre formal de Sprint 1, 2 o 3. No se afirma que nunca existieran PR o demostraciones fuera del repositorio: simplemente no se acreditan aquí.

## Próximo sprint propuesto

**Cierre MVP, con deuda de Sprint 2 y consolidación de Sprint 3**, antes de abrir alcance adicional:

1. Bloquear publicación inválida y autorización mediante rutas históricas.
2. Asegurar totales/versiones/fechas reales y corregir recálculos.
3. Completar contratos flota/pedidos y factibilidad 150×15.
4. Verificar mapa y PDF contra la misma fuente de verdad.
5. Validar al menos cinco RF completos; consolidar evidencias de aceptación y DoD.

El sprint deberá contener tareas comprobables con dependencias, no una nueva promesa porcentual. Véase [BACKLOG_IMPLEMENTACION.md](BACKLOG_IMPLEMENTACION.md). Ninguna de estas tareas se implementó en esta auditoría.
