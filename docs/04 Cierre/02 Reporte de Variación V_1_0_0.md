[Volver al README principal](../../README.md)



# Reporte de Variación (Variance Report)


**Proyecto:** EcoLogística Junín / Huancayo. **Periodo Reportado:** validación del 17/11/2026 **Fecha de Corte:** 17/11/2026 **Versión:** 1.0.0.


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

## 3. Variación de Calidad

| Métrica / Aspecto | Detalle |
|---|---|
| Resultados Planificados (Métricas/Criterios) | DoD: pruebas/cobertura≥80% backend/frontend,0 vulnerabilidades altas/críticas y deuda bloqueante tras análisis, revisión de par, staging automatizado y API actualizada. RF/RNF exigen además aceptación por flujo. |
| Resultados Reales (Defectos/Pruebas) | 210 backend aprobadas; 70/70 frontend y 4/4 SW. Backend 84,37 % líneas / 63,83 % ramas / 80,22 % combinado; frontend 80,47 % líneas / 71,55 % ramas. 0 fallos/omisiones en esos conjuntos. SCA npm/OSV sin avisos tras parche; revisión por par, CI remoto y staging no acreditados. |
| Variación Obtenida | Frente al umbral 80 %: backend líneas +4,37 pp, combinado +0,22 pp; frontend líneas +0,47 pp. AF-24 ya no falla. Las suites/denominadores crecieron: no se interpreta diferencia de cobertura o conteos como avance EV o variación temporal homogénea. |
| Causa Raíz | El fallo anterior de historial era expectativa (1) frente al contrato paginado (1,21); corregido conservando mantenimiento/edición y agregando continuación sin duplicados. P0 requerían regla vigente/terminalidad/contrato público y no solo más tests. |
| Respuesta Planificada | Mantener regresiones y gates explícitos (80 % combinado backend, 80 % líneas frontend); verificar campos/alcance pendientes, factores, entorno, revisión humana y aceptación. Correcciones ya implementadas documentadas en control, sin afirmar cierre global. |
