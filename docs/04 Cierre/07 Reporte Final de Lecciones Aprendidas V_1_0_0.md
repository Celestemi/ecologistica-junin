[Volver al README principal](../../README.md)

# Reporte Final de Lecciones Aprendidas (Final Lessons Learned Report)

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
| Procesos de Aseguramiento de Calidad |Entorno PostGIS descartable permitió 185 casos backend y14 B-08 de integración; fallos se conservan en resultados originales |Una prueba SLA débil puede pasar con solución inválida; frontend falló por contrato de argumentos; cobertura difiere por métrica/alcance |Exigir factibilidad completa además de tiempo, validar contrato y guardar resultados por árbol/commit; bloquear aceptación con defectos críticos y acordar métrica de cobertura. |
| Involucramiento de Interesados (Stakeholders) |Hay matriz de interesados y criterios para organizar revisión |No se localizaron aceptación formal/encuestas/usuarios objetivo; no inventar validación por existir una pantalla |Definir aceptante y protocolo de demostración con datos sintéticos; registrar participación y satisfacción reales con fecha/escala/muestra. |
| Gestión de Riesgos, Incidentes e Impedimentos |RIE/IMP y auditoría permiten identificar deuda técnica y su impacto |Estado «resuelto» histórico puede no describir runtime actual; privacidad/autorización siguen abiertas pese a suites verdes |Revisar por riesgo residual, ligar respuesta aplicada a prueba/fecha y no cerrar por texto optimista; priorizar B-09/10/11 antes de aceptación. |

Contexto e impacto actuales: B-08 ya tiene evidencia PostGIS que antes faltaba; DEF-01 y las brechas de seguridad impiden declarar cierre completo. Estas observaciones derivan de archivos/resultados, no de una retrospectiva de cierre celebrada.

## 2. Conclusiones de la Retrospectiva de Cierre

No disponibles en los registros revisados como conclusiones de una reunión real: faltan fecha, participantes, discusión, aprobación y compromisos. La matriz anterior es insumo para esa sesión. El equipo deberá confirmar qué prácticas mantener, qué acciones asume, responsable/plazo y cómo verificarlas, junto con satisfacción/transferencia y límites económicos. No se simula acta, consenso ni reconocimiento del equipo.
