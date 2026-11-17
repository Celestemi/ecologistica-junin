[Volver al README principal](../../README.md)

# Reporte de Variación (Variance Report)

> **Revisión técnica r2 — 17/11/2026, America/Lima.** Se conserva versión base 1.0.0 y nombre exigido por la plantilla. Referencia vigente: main / b47d5eb7cda26444c56460ea74591cc5f973e0b3 + correcciones sin commit. [Control de implementación](../../AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md) y [resultados actuales](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md). El estado es borrador, sin aceptación administrativa. Los resultados previos se conservan en sus fuentes y en el historial al final.

**Proyecto:** EcoLogística Junín / Huancayo. **Periodo Reportado:** validación del 17/11/2026; periodo de gestión anterior no delimitado. **Fecha de Corte:** 17/11/2026, America/Lima. **Versión:** 1.0.0.

**Borrador verificable; cierre pendiente de aprobación.** Plantilla 5.2. Corte técnico r2 basado en REAUDITORIA_POST_CORRECCIONES y árbol actual sin commit sobre b47d5eb. El corte previo HEAD 61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1 + B-08 sin commit permanece en las fuentes anteriores.

## 1. Variación de Cronograma

| Métrica / Aspecto | Detalle |
|---|---|
| Resultados Planificados | Acta: iteraciones terminan semanas 3/7/11/14; MVP y cierre con pruebas/documentación/sustentación. No se dispone de fechas/calendario detallado y baseline aprobada de dependencias. |
| Resultados Reales | Correcciones AF-01/02/03/24 y pruebas técnicas ejecutadas; aceptación global, SLA representativo, datos económicos y cierre pendientes. No se imputa fecha real de cierre. |
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
| Resultados Reales (Defectos/Pruebas) | 210 backend aprobadas; 70/70 frontend y 4/4 SW. Backend 84,37 % líneas / 63,83 % ramas / 80,22 % combinado; frontend 80,47 % líneas / 71,55 % ramas. 0 fallos/omisiones en esos conjuntos. SCA npm/OSV sin avisos tras parche; revisión por par, CI remoto y staging no acreditados. |
| Variación Obtenida | Frente al umbral 80 %: backend líneas +4,37 pp, combinado +0,22 pp; frontend líneas +0,47 pp. AF-24 ya no falla. Las suites/denominadores crecieron: no se interpreta diferencia de cobertura o conteos como avance EV o variación temporal homogénea. |
| Causa Raíz | El fallo anterior de historial era expectativa (1) frente al contrato paginado (1,21); corregido conservando mantenimiento/edición y agregando continuación sin duplicados. P0 requerían regla vigente/terminalidad/contrato público y no solo más tests. |
| Respuesta Planificada | Mantener regresiones y gates explícitos (80 % combinado backend, 80 % líneas frontend); verificar campos/alcance pendientes, factores, entorno, revisión humana y aceptación. Correcciones ya implementadas documentadas en control, sin afirmar cierre global. |

[DoD histórico](../02%20Planificacion/01_transformando_a_agil_v_1_0_0.md), [defectos actuales](../../AUDITORIA/SPRINT4_DEFECTOS_PENDIENTES.md). La variación de cronograma EVM(SV) se expresa en presupuesto y no sustituye días de atraso; CV=EV−AC tampoco equivale a la diferencia costo real−plan de esta tabla.

## Historial de revisiones del borrador

| Versión base / revisión | Fecha | Cambio y fuente |
|---|---|---|
|1.0.0 / r0 |17/11/2026, corte previo |Contenido previo conservado en Git b47d5eb y snapshot de bytes/hash [docs_cierre_antes_r1.json](../../AUDITORIA/CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json); auditorías originales sin editar. |
|1.0.0 / r1 técnica |17/11/2026, post auditoría |Actualización autorizada con evidencia nueva, corrección de referencias corruptas y límites explícitos. No cambia baseline aprobada ni constituye aceptación/cierre. |
|1.0.0 / r2 técnica |17/11/2026, validación final |210 backend/70 frontend/4 SW; cobertura final y escape literal en PDF. Evidencia r1 preservada en CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r2.json. Sin aceptación administrativa. |

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**. El ensayo técnico en vivo de diez minutos continúa pendiente de observación real.
