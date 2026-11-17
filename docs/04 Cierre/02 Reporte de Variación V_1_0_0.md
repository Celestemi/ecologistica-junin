[Volver al README principal](../../README.md)

# Reporte de Variación (Variance Report)

**Proyecto:** EcoLogística Junín / Huancayo. **Periodo Reportado:** validación del 17/11/2026; periodo de gestión anterior no delimitado. **Fecha de Corte:** 17/11/2026, America/Lima. **Versión:** 1.0.0.

**Borrador verificable; cierre pendiente de aprobación.** Plantilla 5.2 del HTML final. Datos actuales: [resultados](../../AUDITORIA/SPRINT4_RESULTADOS_PRUEBAS.md), HEAD 61 f0 e1 e+B-08 sin commit. Datos base históricos: acta 25/08, presupuesto 15/09, DoD y revisiones. No se comparan automáticamente métricas de distintos alcances como si fueran variaciones del mismo periodo.

## 1. Variación de Cronograma

| Métrica / Aspecto | Detalle |
|---|---|
| Resultados Planificados | Acta: iteraciones terminan semanas 3/7/11/14; MVP y cierre con pruebas/documentación/sustentación. No se dispone de fechas/calendario detallado y baseline aprobada de dependencias. |
| Resultados Reales | B-08 tiene 14 casos PostGIS aprobados ahora; aceptación global, SLA HTTP, evidencia económica, video y cierre siguen pendientes. |
| Variación Obtenida | No calculable en días con evidencia actual: faltan fechas planificadas/reales y calendario aplicable. Se identifica diferencia de estado, no atraso numérico inventado. |
| Causa Raíz | Restricción previa de infraestructura se resolvió; persisten brechas técnicas/aceptación y falta de trazabilidad temporal. El peso de cada causa sobre el plazo no está registrado. |
| Respuesta Planificada | Actualizar cronograma/aceptación con fechas reales, estimar capacidad y registrar cambios aprobados; corregir bloqueantes antes de ensayo final. Responsable/fecha por confirmar. |

## 2. Variación de Costo

| Métrica / Aspecto | Detalle |
|---|---|
| Resultados Planificados | Modelo estimado: USD 120.000 subtotal+USD 14.400 contingencia=USD 134.400; 3000 h asignadas. Acta mantiene referencias históricas pendientes de validación local. No se acredita BAC aprobado ni distribución por periodo. |
| Resultados Reales | No disponibles en los registros revisados: faltan horas ejecutadas, tarifas efectivas, facturas/devengos, AC por paquete/periodo y usos de reserva. |
| Variación Obtenida | No calculable con evidencia actual. No usar presupuesto como AC ni costo de combustible del producto como costo del desarrollo. |
| Causa Raíz | No existe soporte suficiente para atribuir variación de costo a horas/recursos. La ausencia de registro es una brecha de control, no evidencia de sobrecosto cero. |
| Respuesta Planificada | Conciliar presupuesto/aprobación, costos incurridos y periodos; conservar soportes/historia y rebaselining si fue aprobado. No reconstruir horas desde SP o commits. |

Fuente: [presupuesto,15/09/2026](../02%20Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md) y [auditoría EVM](../../AUDITORIA/EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md). Sin inferir tipo de cambio actual del 3,72 histórico.

## 3. Variación de Calidad

| Métrica / Aspecto | Detalle |
|---|---|
| Resultados Planificados (Métricas/Criterios) | DoD: pruebas/cobertura≥80% backend/frontend,0 vulnerabilidades altas/críticas y deuda bloqueante tras análisis, revisión de par, staging automatizado y API actualizada. RF/RNF exigen además aceptación por flujo. |
| Resultados Reales (Defectos/Pruebas) |185/185 backend; 68/69 frontend,1 fallo; 4/4 SW. Backend 83,27% líneas/59,98% ramas/78,68% combinado; frontend 78,80% líneas/70,80% ramas. Análisis actual de vulnerabilidades, staging y aprobación de par no acreditados. |
| Variación Obtenida | Frente a80% de líneas: backend+3,27 pp y frontend−1,20 pp. Si se acuerda combinado backend:−1,32 pp. Existe 1 caso fallido frontend. No hay serie comparable para tasa histórica de defectos; no promediar coberturas de herramientas distintas. |
| Causa Raíz | DEF-01: prueba de flota espera(1), implementación pagina con(1,21). El resto de causas de cobertura requiere análisis por módulo; brechas de seguridad/integridad se verifican por inspección, aunque los tests actuales pasen. |
| Respuesta Planificada | Revisar contrato de historial en ciclo de implementación, añadir cobertura significativa a rutas/canales faltantes, corregir B-09/10/11 y completar DoD/aceptación. No se aplicó corrección durante validación. |

[DoD histórico](../02%20Planificacion/01_transformando_a_agil_v_1_0_0.md), [defectos actuales](../../AUDITORIA/SPRINT4_DEFECTOS_PENDIENTES.md). La variación de cronograma EVM(SV) se expresa en presupuesto y no sustituye días de atraso; CV=EV−AC tampoco equivale a la diferencia costo real−plan de esta tabla.
