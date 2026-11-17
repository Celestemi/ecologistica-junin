[Volver al README principal](../../README.md)

> **Actualización documental r3 — 17/11/2026.** El [estado técnico vigente](../ESTADO_TECNICO_VIGENTE.md) contiene la medición frontend nueva y sus límites. El texto r2 que sigue se conserva como registro histórico; sus pruebas backend, SW, análisis de seguridad y aceptaciones no se reejecutaron en r3. No constituye cierre aprobado.

# Reporte Final de Lecciones Aprendidas (Final Lessons Learned Report)

<!-- complemento-r4:inicio -->
> **Complementación documental r4 — 17/11/2026.** El apartado siguiente aporta propuestas y datos simulados para completar vacíos. No declara nuevas pruebas, gastos ni aprobaciones reales. [Escenario común](../COMPLEMENTO_CONTEXTUAL_DEL_PROYECTO.md).

## Complementación r4: conclusiones propuestas y sesión preparada

**Fecha propuesta de reunión:** 27/11/2026. **Duración:** 30 minutos. Participantes por confirmar mediante convocatoria real: PM, equipo técnico, QA/DevOps y evaluador. No se simula una lista de asistentes ni aprobación.

| Conclusión propuesta para discutir | Acción concreta | Responsable por rol | Fecha objetivo | Verificación |
|---|---|---|---|---|
| Preparar entorno y dataset al inicio evita bloqueos tardíos. | Usar checklist de PostGIS, API y testigo factible. | DevOps + Backend | 23/11/2026 | Arranque y caso reproducibles. |
| Separar implementación, prueba y aceptación mejora trazabilidad. | Revisar matriz RF/RNF→criterio→evidencia→decisión. | QA + PM | 27/11/2026 | Cada estado tiene fuente y revisor. |
| El ahorro necesita referencia comparable. | Mantener mismo lote, flota y ventanas al comparar. | Backend + QA | 25/11/2026 | Cálculo y supuestos visibles. |
| Gestión económica debe registrarse por periodo. | Adoptar ficha de paquete, horas, tarifa, soporte y aceptación. | PM | 20/11/2026 para preparar formato | Datos reales distinguibles de supuestos. |
| Revisión es parte de la capacidad del equipo. | Limitar a dos tareas en QA y revisar antes de abrir trabajo nuevo. | QA + equipo | Durante validación | Menor acumulación observada en tablero futuro. |
| La entrega requiere transferencia operable. | Ensayar respaldo/restauración y guía por roles. | DevOps + equipo | 26/11/2026 | Recorrido y resultado registrados. |

Estas conclusiones son propuestas analíticas acordes con las brechas documentadas. La sesión deberá confirmar qué mantener, qué ajustar y quién asume cada acción. Para satisfacción y reconocimiento se propone una pregunta voluntaria 1–5 más comentario abierto, sin convertir el Mood ilustrativo en respuestas reales del equipo.
<!-- complemento-r4:fin -->

---


> **Revisión técnica r2 — 17/11/2026, America/Lima.** Se conserva versión base 1.0.0 y nombre exigido por la plantilla. Referencia vigente: main / b47d5eb7cda26444c56460ea74591cc5f973e0b3 + correcciones sin commit. [Control de implementación](../../AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md) y [resultados actuales](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md). El estado es borrador, sin aceptación administrativa. Los resultados previos se conservan en sus fuentes y en el historial al final.

**Proyecto:** EcoLogística Junín / Huancayo. **Fecha de Reunión de Cierre:** No disponible en los registros revisados; reunión y aprobación pendientes. **Versión:** 1.0.0.

**Borrador analítico para validar con el equipo.** Plantilla 5.7, corte 17/11/2026, America/Lima. Fuentes: retrospectivas textuales de Sprint 1/2/3 y [evidencia actual](../../AUDITORIA/SPRINT4_EVIDENCIAS_TECNICAS.md). Lo histórico se distingue del resultado actual; recomendaciones no son acciones aprobadas ni implantadas automáticamente.

## 1. Matriz Consolidada de Aprendizajes

| Categoría de Gestión | Prácticas Efectivas (Qué mantener) | Oportunidades de Mejora (Qué evitar/ajustar) | Recomendación para Futuros Equipos |
|---|---|---|---|
| Desempeño del Equipo (Dinámica ágil y general) |Separar implementación de verificación; la documentación Sprint 1/2 reconoce límites y propone responsabilidades QA/DevOps |No afirmar ceremonias/satisfacción sin asistentes/fecha/acta; no asumir que propuesta es compromiso |Acordar responsables y participantes reales antes de revisión; cerrar acciones con evidencia y recoger ánimo mediante escala, sin reconstruirlo retroactivamente. |
| Evolución y Control del Alcance (Predictivo vs. Adaptativo) |Mantener catálogo/baseline y relacionar incremento B-08 con criterios concretos |Dos numeraciones RF y estados Done contradictorios dificultan aceptación; un catálogo no prueba aceptación |Mantener matriz RF/RNF↔US/EN↔prueba↔resultado↔aceptante; registrar antes/después/aprobación de cambios de alcance. |
| Desempeño e Integración del Cronograma Híbrido |Hitos por iteración orientan secuencia y dependencias técnicas |Semanas sin fechas reales/dependencias no permiten calcular atraso ni ruta crítica; capturas 2024 no son baseline 2026 |Acordar calendario base y registrar fechas reales/aceptación; actualizar impacto y versiones sin borrar baseline original. |
| Gestión del Presupuesto y Costos |El modelo de 15/09 desglosa roles, herramientas, cloud y contingencia verificables como estimación |Sin BAC aprobado/PV temporal/EV valorado/AC no hay EVM defendible; no usar presupuesto como gasto |Aprobar baseline/reservas/moneda y registrar horas/devengos por paquete/periodo desde el inicio, con soporte y conciliación. |
| Técnicas de Estimación (Velocidad, duración, recursos) |SP y estimación de horas por rol explicitan supuestos de planificación |20/34 SP de actas y39/47/34 de capturas no son una serie conciliada; SP no equivalen automáticamente a dinero/horas |Medir trabajo aceptado y capacidad real por periodo; revisar estimaciones con la misma unidad/alcance y documentar incertidumbre. |
| Procesos de Aseguramiento de Calidad |Regresiones rojas/verdes, PostGIS descartable, 210 backend/70 frontend/4 SW y gates explícitos; SCA encontró y permitió corregir dependencia transitiva |Tests de tiempo sin factibilidad y dobles insuficientes daban confianza parcial; CI remoto/aceptación no se infieren de verde local |Conservar resultados por árbol, validar testigo factible, contratos/rollback/privacidad, registrar métrica exacta y revisar riesgo residual con responsables reales. |
| Involucramiento de Interesados (Stakeholders) |Hay matriz de interesados y criterios para organizar revisión |No se localizaron aceptación formal/encuestas/usuarios objetivo; no inventar validación por existir una pantalla |Definir aceptante y protocolo de demostración con datos sintéticos; registrar participación y satisfacción reales con fecha/escala/muestra. |
| Gestión de Riesgos, Incidentes e Impedimentos |RIE/IMP y regresiones permiten priorizar por evidencia; AF-01/02/03 corregidos en ciclo autorizado |Un P0 corregido no cierra alcance, infraestructura, GPS/comprobantes o aceptación; “resuelto” debe tener prueba y corte |Relacionar respuesta aplicada con caso/fecha/versión y validar riesgo residual; no cerrar por texto optimista ni reconstruir reuniones pasadas. |

Contexto e impacto actuales: las correcciones AF-01/02/03/24 y el parche transitivo tienen evidencia técnica. Faltan datos económicos, aceptación, radiadores, condiciones de RF y ensayo humano. Esta revisión analítica deriva de archivos/pruebas, no de una retrospectiva celebrada. [Solicitud para validación real](../../AUDITORIA/SOLICITUD_EVIDENCIAS_HUMANAS.md).

## 2. Conclusiones de la Retrospectiva de Cierre

No disponibles en los registros revisados como conclusiones de una reunión real: faltan fecha, participantes, discusión, aprobación y compromisos. La matriz anterior es insumo para esa sesión. El equipo deberá confirmar qué prácticas mantener, qué acciones asume, responsable/plazo y cómo verificarlas, junto con satisfacción/transferencia y límites económicos. No se simula acta, consenso ni reconocimiento del equipo.

## Lección técnica añadida en r3: verificar el pedido de extremo a extremo

**Hecho observado:** el mapa principal omitía pedidos nuevos si existía una ruta publicada; guardar una ubicación borraba su marcador de la vista. La corrección combina estado persistido, representación de pedidos pendientes y pruebas de reapertura/edición. Se añadieron casos para pedidos fuera de la primera página y errores recuperables. [Evidencia](../ESTADO_TECNICO_VIGENTE.md).

**Acción propuesta:** incluir en la siguiente revisión un recorrido observado de crear → guardar → volver al dashboard → editar → recargar, con un pedido que no sea de ejemplo. Registrar duración, errores y resultado, sin fijar porcentajes antes de medir. Esta lección procede de la revisión técnica actual; no se atribuye a una retrospectiva de equipo que no fue observada.

## Historial de revisiones del borrador

Revisión r3 (17/11/2026): incorporación de evidencia frontend nueva, cifras con denominador y límites, sin modificar costos reales ni aceptación. El registro r2 conserva sus valores históricos.

| Versión base / revisión | Fecha | Cambio y fuente |
|---|---|---|
|1.0.0 / r0 |17/11/2026, corte previo |Contenido previo conservado en Git b47d5eb y snapshot de bytes/hash [docs_cierre_antes_r1.json](../../AUDITORIA/CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json); auditorías originales sin editar. |
|1.0.0 / r1 técnica |17/11/2026, post auditoría |Actualización autorizada con evidencia nueva, corrección de referencias corruptas y límites explícitos. No cambia baseline aprobada ni constituye aceptación/cierre. |
|1.0.0 / r2 técnica |17/11/2026, validación final |210 backend/70 frontend/4 SW; cobertura final y escape literal en PDF. Evidencia r1 preservada en CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r2.json. Sin aceptación administrativa. |

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**. El ensayo técnico en vivo de diez minutos continúa pendiente de observación real.
