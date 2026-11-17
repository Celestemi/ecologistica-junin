[Volver al README principal](../../README.md)

> **Actualización documental r3 — 17/11/2026.** El [estado técnico vigente](../ESTADO_TECNICO_VIGENTE.md) contiene la medición frontend nueva y sus límites. El texto r2 que sigue se conserva como registro histórico; sus pruebas backend, SW, análisis de seguridad y aceptaciones no se reejecutaron en r3. No constituye cierre aprobado.

# Radiadores de Información (Information Radiators)

<!-- complemento-r4:inicio -->
> **Complementación documental r4 — 17/11/2026.** El apartado siguiente aporta propuestas y datos simulados para completar vacíos. No declara nuevas pruebas, gastos ni aprobaciones reales. [Escenario común](../COMPLEMENTO_CONTEXTUAL_DEL_PROYECTO.md).

## Complementación r4: radiadores simulados del trabajo de cierre

Se crean series ilustrativas para R4-01…R4-08 (20 puntos) del complemento común. No reconstruyen Sprint 1/2, no son capturas de Jira ni tareas ya aceptadas.

### Burndown y burnup del ejercicio

```mermaid
xychart-beta
    title "Burndown simulado: restante e ideal"
    x-axis [D0, D1, D2, D3, D4, D5]
    y-axis "Puntos" 0 --> 20
    line [20, 20, 18, 15, 9, 2]
    line [20, 16, 12, 8, 4, 0]
```

```mermaid
xychart-beta
    title "Burnup simulado: terminado y alcance"
    x-axis [D0, D1, D2, D3, D4, D5]
    y-axis "Puntos" 0 --> 20
    line [0, 0, 2, 5, 11, 18]
    line [20, 20, 20, 20, 20, 20]
```

Tabla accesible: restante 20/20/18/15/9/2; ideal 20/16/12/8/4/0; terminado 0/0/2/5/11/18; alcance 20 en los seis cortes. Se supone finalización de 18/20 puntos (90 %) y 7/8 tareas (87,5 %). Queda R4-08 (guía/demostración) en revisión; no se calcula velocidad histórica del equipo con este ejercicio único.

### Tablero propuesto en D3

| Por hacer | En curso | Revisión/QA | Terminadas |
|---|---|---|---|
| R4-07, R4-08 | R4-05, R4-06 | R4-03, R4-04 | R4-01, R4-02 |

### Mood ilustrativo por roles ficticios

| Rol ficticio, sin respuestas de integrantes | Iteración 1 | Iteración 2 | Iteración 3 | Iteración final |
|---|---:|---:|---:|---:|
| PM del ejemplo | 3 | 3 | 4 | 4 |
| Backend del ejemplo | 3 | 2 | 3 | 4 |
| Frontend del ejemplo | 3 | 3 | 4 | 4 |
| QA/DevOps del ejemplo | 2 | 2 | 3 | 4 |
| Promedio ilustrativo | 2,75 | 2,50 | 3,50 | 4,00 |

Escala 1–5 definida en el complemento. La menor valoración de la iteración 2 es una hipótesis de carga por integración; no mide clima laboral real. Para aplicarlo se propone encuesta voluntaria, fecha y respuestas agregadas sin atribución personal.

### Retrospectiva propuesta

Mantener: dataset repetible y regresiones por criterio. Mejorar: preparar entorno temprano y reducir cola en revisión. Acciones: QA consolida matriz al 20/11; DevOps prepara entorno al 23/11; PM coordina revisión al 27/11/2026. Son propuestas con responsables por rol, no acuerdos de una reunión celebrada.
<!-- complemento-r4:fin -->

---


> **Revisión técnica r2 — 17/11/2026, America/Lima.** Se conserva versión base 1.0.0 y nombre exigido por la plantilla. Referencia vigente: main / b47d5eb7cda26444c56460ea74591cc5f973e0b3 + correcciones sin commit. [Control de implementación](../../AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md) y [resultados actuales](../../AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md). El estado es borrador, sin aceptación administrativa. Los resultados previos se conservan en sus fuentes y en el historial al final.

**Proyecto:** EcoLogística Junín / Huancayo. **Marco Ágil Utilizado:** Scrum dentro del enfoque híbrido documentado. **Versión:** 1.0.0.

**Borrador; evidencia histórica incompleta; cierre pendiente de aprobación.** Plantilla 5.5, corte 17/11/2026, America/Lima. Las imágenes ya existentes se enlazan sin alterar fechas ni presentarlas como capturas actuales. No se accedió a Jira remoto ni se verificó autenticidad/exportación de origen. [Inventario y discrepancias](../../AUDITORIA/EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md), [fuentes actuales/históricas](../../AUDITORIA/SPRINT4_EVIDENCIAS_TECNICAS.md).

## 1. Burndown Chart (Trabajo Restante)

**Burndown Chart:** no disponible en los registros revisados. No se localizó captura/serie diaria real de trabajo restante e ideal con compromiso inicial/cambios.

**Análisis de velocidad y tasa de finalización:** no calculable como serie. Las actas registran 20 SP comprometidos/0 Done en Sprint 1 y34 SP/0 Done en Sprint 2 en sus cortes; no son una velocidad actual ni permiten dibujar una línea diaria. No convertir tests/commits/porcentaje técnico a SP aceptados ni interpolar historia.

## 2. Burnup Chart (Trabajo Completado y Cambios de Alcance)

**Burnup Chart:** no disponible; faltan series de alcance total/completado aceptado y fechas de cambios aprobados.

**Análisis de crecimiento de alcance vs. trabajo aceptado:** no verificable. El backlog existe como catálogo y hay código parcial; no hay historial conciliado que permita cuantificar aumentos/reducciones ni aceptación acumulada. Obtener fuente auténtica y registrar desde ahora, sin retroproyectar datos.

## 3. Task Board / Tablero Kanban

![Tablero Scrum histórico aportado; no estado actual verificado](../02%20Planificacion/Capturas%20en%20JIRA/04-tablero-scrum.png)

**Análisis de flujo y cuellos de botella identificados:** la imagen muestra To Do/In Progress/In Review/QA/Done y tarjetas. No se dispone de fecha de captura/exportación actual ni tiempos de permanencia que permitan medir cuellos de botella. Los archivos relacionados de roadmap/planning/releases muestran 2024, frente a documentación 2026. Su presencia no prueba estado Done contra DoD actual. No se modifica la captura para que parezca reciente.

## 4. Mood Chart (Estado de Ánimo del Equipo)

| Integrante / Rol | Sprint 1 | Sprint 2 | Sprint 3 | Sprint Final |
|---|---|---|---|---|
| PM — respuestas individuales no registradas | No disponible | No disponible | No disponible | No disponible |
| Equipo técnico — respuestas individuales no registradas | No disponible | No disponible | No disponible | No disponible |

**Interpretación del clima laboral:** no disponible en los registros revisados; no hay escala, participantes/respondientes ni respuestas fechadas. Las filas identifican roles a consultar, no dos personas encuestadas. Retrospectivas optimistas o suites aprobadas no miden ánimo. Una encuesta actual no reconstruye el ánimo histórico de otros sprints.

## 5. Tableros de Retrospectiva

**Evidencia:** no se localizó imagen de un tablero real ni acta/participación de reunión de cierre. Existen retrospectivas textuales de Sprint 1/2/3; Sprint 2 se identifica como borrador técnico y Sprint 1 contiene propuestas no aprobadas. No sustituyen captura y ceremonia reales.

- **Lo que funcionó bien:** PostGIS descartable permitió regresiones de seguridad, integridad y suites completas; hay pruebas previas rojas y posteriores verdes conservadas. Es observación técnica, no resultado votado en retrospectiva.
- **Oportunidades de mejora:** alinear afirmaciones de Done, resultados originales, cobertura y contratos de prueba; registrar cambios, ánimo y aceptación oportunamente.
- **Acciones implementadas:** AF-01/02/03/24 corregidos con pruebas; estas son respuestas de ingeniería del ciclo autorizado, no acuerdos de una ceremonia histórica. No se acredita reunión/compromisos de equipo.

Faltan burndown/burnup/Mood/retro auténticos y un Kanban vigente para satisfacer completamente la rúbrica. No se fabricaron capturas, entrevistas ni series.

## Recolección pendiente, revisión r2

Las pruebas nuevas no aportan historia Jira, Mood o una retrospectiva real. [Solicitud prospectiva de evidencias](../../AUDITORIA/SOLICITUD_EVIDENCIAS_HUMANAS.md) y [fuentes irresolubles](../../AUDITORIA/FUENTES_HISTORICAS_IRRESOLUBLES.md). No se modificaron capturas ni fechas.

## Radiador técnico r3: observaciones registradas ahora

| Señal del corte r3 | Resultado observado | Acción pendiente |
|---|---|---|
| Regresiones frontend | 86 aprobadas; 0 fallidas y 0 pendientes | Probar el recorrido completo en navegador con API y cartografía reales. |
| Cobertura de líneas | 81,35 %; 268 líneas sin cubrir | Priorizar casos no cubiertos por impacto. |
| Cobertura de ramas | 73,93 %; 360 ramas sin cubrir | Ampliar errores y alternativas de flujo. |
| Alta y edición de puntos | Casos de componentes e integración de UI aprobados | Medir finalización, errores y duración con usuarios. |

Este radiador registra una corrida de pruebas, no un tablero de tareas aceptadas. No reconstruye burndown, velocidad, ánimo ni reuniones de los sprints. [Evidencia del corte](../evidencias/2026-11-17/frontend.json).

## Historial de revisiones del borrador

Revisión r3 (17/11/2026): incorporación de evidencia frontend nueva, cifras con denominador y límites, sin modificar costos reales ni aceptación. El registro r2 conserva sus valores históricos.

| Versión base / revisión | Fecha | Cambio y fuente |
|---|---|---|
|1.0.0 / r0 |17/11/2026, corte previo |Contenido previo conservado en Git b47d5eb y snapshot de bytes/hash [docs_cierre_antes_r1.json](../../AUDITORIA/CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json); auditorías originales sin editar. |
|1.0.0 / r1 técnica |17/11/2026, post auditoría |Actualización autorizada con evidencia nueva, corrección de referencias corruptas y límites explícitos. No cambia baseline aprobada ni constituye aceptación/cierre. |
|1.0.0 / r2 técnica |17/11/2026, validación final |210 backend/70 frontend/4 SW; cobertura final y escape literal en PDF. Evidencia r1 preservada en CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r2.json. Sin aceptación administrativa. |

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**. El ensayo técnico en vivo de diez minutos continúa pendiente de observación real.
