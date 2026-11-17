[Volver al README principal](../../README.md)

# Reporte de Análisis de Valor Ganado - EVM (Earned Value Analysis Report)

**Proyecto:** EcoLogística Junín / Huancayo. **Presupuesto hasta la Conclusión (BAC):** No disponible en los registros revisados como presupuesto aprobado. **Estado General:** borrador; no calculable con evidencia actual, cierre pendiente de aprobación. **Versión:** 1.0.0.

Plantilla 5.3 del HTML final. Corte 17/11/2026, America/Lima. Periodo actual de gestión y corte económico anterior no delimitados; no hay libro económico comparable. Fuente estimada: [presupuesto 15/09/2026](../02%20Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md), USD 134.400 y3000 h planificadas; el acta mantiene montos referenciales pendientes de validación. No equivalen a aprobación BAC ni AC. [Inventario económico y registros faltantes](../../AUDITORIA/EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md).

## 1. Métricas de Desempeño EVM

| Métrica / Indicador | Periodo Actual | Acumulado Periodo Actual | Acumulado Periodo Anterior |
|---|---|---|---|
| Valor Planificado (PV) | No disponible: falta presupuesto temporal aprobado. | No disponible: falta línea base por paquetes y corte. | No disponible: falta línea base y corte anterior. |
| Valor Ganado (EV) | No disponible: falta aceptación valorada al presupuesto base. | No disponible: falta registro acumulado de aceptación. | No disponible: falta aceptación monetizada anterior. |
| Costo Real (AC) | No disponible: faltan costos/horas/devengos con soporte. | No disponible: falta libro de costos conciliado. | No disponible: faltan costos del corte anterior. |
| Variación del Cronograma (SV = EV - PV) | No calculable con evidencia actual. | No calculable con evidencia actual. | No calculable con evidencia actual. |
| Variación del Costo (CV = EV - AC) | No calculable con evidencia actual. | No calculable con evidencia actual. | No calculable con evidencia actual. |
| Índice de Desempeño del Cronograma (SPI = EV / PV) | No calculable con evidencia actual. | No calculable con evidencia actual. | No calculable con evidencia actual. |
| Índice de Desempeño del Costo (CPI = EV / AC) | No calculable con evidencia actual. | No calculable con evidencia actual. | No calculable con evidencia actual. |

PV/EV/AC/SV/CV requieren misma moneda, baseline/corte y alcance; SPI/CPI son adimensionales. Un denominador cero se reportaría no definido, no se reemplaza por 0 o 1. No se suman ni promedian índices entre periodos. Ausencia de EV/AC no significa cero. Los 185 tests o53,5%/67,1% de implementación histórica no son EV.

## 2. Porcentajes de Avance Acumulado (Respecto al BAC)

- **Porcentaje Planificado (PV / BAC):** No calculable con evidencia actual; faltan PV acumulado y BAC aprobado. La expresión porcentual usaría 100 ×PV/BAC.
- **Porcentaje Ganado (EV / BAC):** No calculable con evidencia actual; faltan EV acreditado y BAC aprobado. Usaría 100 ×EV/BAC.
- **Porcentaje Gastado (AC / BAC):** No calculable con evidencia actual; faltan AC y BAC aprobado. Usaría 100 ×AC/BAC; gasto no es avance físico.

## 3. Análisis de Desviaciones

- **Causa raíz de la variación del cronograma:** no atribuible numéricamente sin EV/PV. Los impedimentos técnicos documentados no cuantifican por sí mismos SV.
- **Impacto en el cronograma:** no calculable; no hay fechas reales/baseline comparables para atraso ni valores EVM sustentados.
- **Causa raíz de la variación del costo:** no disponible; faltan horas/devengos/costos reales y su relación con trabajo presupuestado.
- **Impacto en el presupuesto:** no calculable; no se acredita sobregasto, ahorro ni consumo de contingencia.

El modelo suma USD 120.000+12% contingencia(14.400)=USD 134.400 y usa conversión histórica 3,72→S/499.968. Esa aritmética es verificable como **estimación**, no desempeño ejecutado ni adopción automática de BAC. Deben aprobarse moneda/alcance/tratamiento de reservas y registrar paquetes/periodos, aceptante y soportes de AC antes de calcular.

## 4. Estimaciones a la Conclusión (EAC)

- **Fórmula 1 (EAC = BAC / CPI):** No calculable con evidencia actual. Requiere BAC aprobado y CPI>0; proyectaría continuidad del desempeño de costo.
- **Fórmula 2 (EAC = BAC / (CPI × SPI)):** No calculable con evidencia actual. Requiere BAC e índices positivos; justificar efecto combinado sobre la proyección.
- **Fórmula 3 (EAC = AC + [(BAC - EV) / (CPI × SPI)]):** No calculable con evidencia actual. Requiere BAC/EV/AC sustentados e índices positivos; conserva lo incurrido y aplica desempeño combinado al remanente.
- **EAC Seleccionado, Justificación y Explicación:** No se selecciona numéricamente ningún escenario sin datos. Debe elegirse por causas reales y comportamiento esperado del trabajo restante, no por el resultado más bajo.

Este documento preserva campos y fórmulas, pero **no satisface la exigencia de cálculos reales de la rúbrica**. Requiere intervención del responsable económico/autoridad de aprobación; no se inventan costos, horas o aceptación histórica.
