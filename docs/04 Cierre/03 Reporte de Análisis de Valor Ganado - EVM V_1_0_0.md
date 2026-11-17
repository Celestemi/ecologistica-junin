[Volver al README principal](../../README.md)

> **Actualización documental r3 — 17/11/2026.** El [estado técnico vigente](../ESTADO_TECNICO_VIGENTE.md) contiene la medición frontend nueva y sus límites. El texto r2 que sigue se conserva como registro histórico; sus pruebas backend, SW, análisis de seguridad y aceptaciones no se reejecutaron en r3. No constituye cierre aprobado.

# Reporte de Análisis de Valor Ganado - EVM (Earned Value Analysis Report)

<!-- complemento-r4:inicio -->
> **Complementación documental r4 — 17/11/2026.** El apartado siguiente aporta propuestas y datos simulados para completar vacíos. No declara nuevas pruebas, gastos ni aprobaciones reales. [Escenario común](../COMPLEMENTO_CONTEXTUAL_DEL_PROYECTO.md).

## Complementación r4: EVM calculado con datos simulados del proyecto

**Todos los valores de esta sección pertenecen al ejercicio académico.** BAC supuesto USD 134 400, con contingencia distribuida y sin reserva de gestión adicional. Corte anterior 09/11/2026; actual 16/11/2026; periodo 10–16/11. No hay BAC aprobado, gasto ni aceptación reales añadidos.

| Métrica | Periodo actual simulado | Acumulado actual simulado | Acumulado anterior simulado |
|---|---:|---:|---:|
| PV, USD | 12 000 | 112 000 | 100 000 |
| EV, USD | 13 440 | 107 520 | 94 080 |
| AC, USD | 14 700 | 112 700 | 98 000 |
| SV = EV−PV, USD | 1 440 | −4 480 | −5 920 |
| CV = EV−AC, USD | −1 260 | −5 180 | −3 920 |
| SPI = EV/PV | 1,1200 | 0,9600 | 0,9408 |
| CPI = EV/AC | 0,9143 | 0,9540 | 0,9600 |

Porcentajes acumulados sobre BAC: PV 83,33 %, EV 80,00 % y AC 83,85 %. El periodo recupera avance respecto del plan, pero su costo por unidad de trabajo es menos favorable que el acumulado. SV no expresa días de retraso. Se mantienen los valores sin redondear para las proyecciones:

| Proyección del ejercicio | Resultado USD | Supuesto |
|---|---:|---|
| EAC1 = BAC/CPI | 140 875,00 | Continúa la eficiencia acumulada de costos. |
| EAC2 = BAC/(CPI×SPI) | 146 744,79 | El desempeño combinado afecta todo el presupuesto. |
| EAC3 = AC+(BAC−EV)/(CPI×SPI) | 142 048,96 | Conserva lo incurrido y aplica desempeño combinado al remanente. |
| ETC1 = EAC1−AC | 28 175,00 | Costo esperado para completar en EAC1. |
| VAC1 = BAC−EAC1 | −6 475,00 | Sobrecosto final proyectado del 4,82 %. |

Se selecciona **EAC1 únicamente dentro del ejercicio**, suponiendo que la pérdida de eficiencia de costos continúa y que el retraso no añade un multiplicador de costo independiente. Si el trabajo pendiente exige recursos por demora, revisar EAC3 con una estimación detallada. PM consolidaría decisiones; el responsable económico real debe aportar horas, soportes y aceptación para usar EVM de ejecución.

Este contenido completa fórmulas, interpretación y proyección con un caso consistente; las tablas históricas siguientes conservan la ausencia de datos reales y no se convierten en mediciones por esta adición.
<!-- complemento-r4:fin -->

---


> **Revisión técnica r2 — 17/11/2026, America/Lima.** Se conserva versión base 1.0.0 y nombre exigido por la plantilla. Referencia vigente: main / b47d5eb7cda26444c56460ea74591cc5f973e0b3 + correcciones sin commit. [Control de implementación](../../AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md) y [resultados actuales](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md). El estado es borrador, sin aceptación administrativa. Los resultados previos se conservan en sus fuentes y en el historial al final.

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

PV/EV/AC/SV/CV requieren misma moneda, baseline/corte y alcance; SPI/CPI son adimensionales. Un denominador cero se reportaría no definido, no se reemplaza por 0 o 1. No se suman ni promedian índices entre periodos. Ausencia de EV/AC no significa cero. Ni los 185 tests anteriores ni los 210 actuales, ni porcentajes de implementación histórica, son EV.

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

## Recolección pendiente, revisión r2

No se recibieron datos financieros nuevos. Se mantiene NO CALCULABLE en los tres cortes y las tres EAC, sin inventar aprobación o gasto. [Solicitud concreta de BAC/PV/EV/AC, periodos y soportes](../../AUDITORIA/SOLICITUD_DATOS_EVM.md). La corrección del software y los costos logísticos estimados no modifican el BAC ni prueban AC.

## Anexo r3: ejercicio separado, sin datos reales nuevos

Se añade un [ejemplo EVM hipotético](../EJEMPLO_EVM_HIPOTETICO.md) con entradas inventadas y cálculo reproducible: SPI supuesto de 0,96 y CPI supuesto de 0,954 en su último corte, con retraso y sobrecosto dentro del ejercicio. **No son resultados de EcoLogística**, no se incorporan a las tablas reales de este reporte y no acreditan BAC, aceptación ni gasto. Las métricas reales de EVM continúan no calculables.

## Historial de revisiones del borrador

Revisión r3 (17/11/2026): incorporación de evidencia frontend nueva, cifras con denominador y límites, sin modificar costos reales ni aceptación. El registro r2 conserva sus valores históricos.

| Versión base / revisión | Fecha | Cambio y fuente |
|---|---|---|
|1.0.0 / r0 |17/11/2026, corte previo |Contenido previo conservado en Git b47d5eb y snapshot de bytes/hash [docs_cierre_antes_r1.json](../../AUDITORIA/CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json); auditorías originales sin editar. |
|1.0.0 / r1 técnica |17/11/2026, post auditoría |Actualización autorizada con evidencia nueva, corrección de referencias corruptas y límites explícitos. No cambia baseline aprobada ni constituye aceptación/cierre. |
|1.0.0 / r2 técnica |17/11/2026, validación final |210 backend/70 frontend/4 SW; cobertura final y escape literal en PDF. Evidencia r1 preservada en CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r2.json. Sin aceptación administrativa. |

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**. El ensayo técnico en vivo de diez minutos continúa pendiente de observación real.
