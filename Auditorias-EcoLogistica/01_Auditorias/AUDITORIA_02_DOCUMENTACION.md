# AUDITORIA_02_DOCUMENTACION

Auditoría documental de solo lectura completada. Se revisaron **36 archivos Markdown**; no se modificó, creó, movió ni eliminó ningún archivo.

Conclusión: la documentación es amplia y conserva buena trazabilidad académica, pero no tiene una fuente única clara para el estado técnico vigente. Los problemas prioritarios son enlaces relativos rotos en los documentos de Sprint, referencias del README a una estructura/prototipo antigua, y contradicciones entre arquitectura planificada y la implementación real.

## 1. Inventario completo

Abreviaturas: S1 = Sprint 1; S2 = Sprint 2; “README” significa que está indexado desde el documento principal.

| Ruta | Versión / fecha | Propósito / sprint | Referencias principales | Estado |
|---|---|---|---|---|
| `app/data/README_operating_area.md` | Sin versión/fecha | Uso provisional del polígono operativo; RF-005/S2 | `operating_area_dev.geojson` | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/00. Directrices y Auditoria V_1_0_3.md` | V_1_0_3; 01-09-2026 | Directrices y auditoría de requisitos | Docs 06–13; README | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/01. Selección del enfoque del proyecto V_1_0_0.md` | 1.0.0; 25-08-2026 | Justificación metodológica híbrida | README | CONSERVAR SIN CAMBIOS |
| `docs/01 Inicio/02. Acta de constitución V_1_0_0.md` | 1.0.0; 25-08-2026 | Charter, objetivos, alcance | README | CONSERVAR SIN CAMBIOS |
| `docs/01 Inicio/03. Declaración de la visión V_1_0_0.md` | 1.0.0; 25-08-2026 | Visión y KPIs base | README | CONSERVAR SIN CAMBIOS |
| `docs/01 Inicio/04. Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md` | 1.0.0; 25-08-2026 | Supuestos y restricciones iniciales | README | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/05. Registro de interesados V_1_0_0.md` | 1.0.0; 25-08-2026 | Stakeholders y matriz de interés | README | CONSERVAR SIN CAMBIOS |
| `docs/01 Inicio/06. Requisitos funcionales V_1_0_0.md` | 1.0.0; fecha no visible en cabecera | RF, BDD y trazabilidad | README; planes S1/S2 | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/07. Requisitos no funcionales V_1_0_0.md` | 1.0.0; fecha no visible en cabecera | RNF y escenarios de calidad | README; planes y reportes | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/08. Usuarios V_1_0_3.md` | V_1_0_3; sin fecha visible | Perfiles y RBAC | README; impedimentos S1 | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/09. Reglas de negocio V_1_0_4.md` | V_1_0_4; sin fecha visible | RN-001 a RN-008 | README; planes S1/S2 | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/10. Stack tecnológico V_1_0_3.md` | V_1_0_3; sin fecha visible | Stack objetivo | README; plan S2 | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/11. Base de datos V_1_0_3.md` | V_1_0_3; sin fecha visible | Modelo de datos y SQL de referencia | README; plan S2 | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/12. Modelo C4 V_1_0_6.md` | Archivo V_1_0_6; encabezado V_1_0_3; 01-09-2026 | Arquitectura C4 | README; plan S2 | CONSERVAR Y ACTUALIZAR |
| `docs/01 Inicio/13. Restricciones V_1_0_4.md` | V_1_0_4; sin fecha visible | Análisis multidimensional de restricciones | README | CONSERVAR Y ACTUALIZAR |
| `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` | V_1_0_0; 15-09-2026 | Backlog, épicas, US, BDD y DoD | Planes, reportes y README | CONSERVAR Y ACTUALIZAR |
| `docs/02 Planificacion/02 Artefactos Jira V_1_0_0.md` | V_1_0_0; sin fecha visible | Evidencias Jira | Capturas PNG; README | CONSERVAR SIN CAMBIOS |
| `docs/02 Planificacion/03_registro_de_riesgos_v_1_0_0.md` | V_1_0_0; 15-09-2026 | Riesgos de proyecto | README | CONSERVAR Y ACTUALIZAR |
| `docs/02 Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md` | V_1_0_0; 15-09-2026 | CAPEX/OPEX y presupuesto referencial | README | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 1/01_informe_de_estado_del_proyecto_v_1_0_1.md` | V_1_0_1; 26-10-2026 | Estado corregido de S1 | DoD, plan S1, README | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 1/02_registro_de_impedimentos_v_1_0_1.md` | V_1_0_1; 26-10-2026 | Impedimentos S1 corregidos | README, reportes técnicos | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 1/03_revision_del_sprint_v_1_0_1.md` | V_1_0_1; 26-10-2026 | Revisión S1 corregida | DoD, plan S1, README | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 1/04_retrospectiva_del_sprint_V_1_0_1.md` | V_1_0_1; 26-10-2026 | Retrospectiva técnica S1 | DoD, README | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 2/01_informe_de_estado_del_proyecto_v_1_0_0.md` | V_1_0_0; 26-10-2026 | Estado de implementación S2 | Plan S2, verificación, rendimiento | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 2/02_registro_de_impedimentos_v_1_0_0.md` | V_1_0_0; 26-10-2026 | Impedimentos nuevos/reabiertos S2 | S1, plan y verificación S2 | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 2/03_revision_del_sprint_v_1_0_0.md` | V_1_0_0; 26-10-2026 | Revisión S2 | Plan, rendimiento, verificación | CONSERVAR Y ACTUALIZAR |
| `docs/03 Implementación/Sprint 2/04_retrospectiva_del_sprint_v_1_0_0.md` | V_1_0_0; 26-10-2026 | Borrador técnico de retrospectiva S2 | Plan y verificación S2 | CONSERVAR Y ACTUALIZAR |
| `docs/deploy/TLS_VERIFICACION.md` | Sin versión/fecha | Checklist HTTPS/TLS; EN-003 | Infraestructura y S1 | CONSERVAR Y ACTUALIZAR |
| `docs/qa/COMANDOS_CALIDAD.md` | Sin versión/fecha; S1 | Comandos de calidad reproducibles | DoD S1 | CONSERVAR Y ACTUALIZAR |
| `PLAN_IMPLEMENTACION_SPRINT_1.md` | 26-10-2026 | Plan técnico retrospectivo S1 | RF/RNF, reglas, DoD | ARCHIVAR HISTÓRICAMENTE |
| `PLAN_IMPLEMENTACION_SPRINT_2.md` | 26-10-2026 | Plan técnico S2 y decisiones D-01…D-08 | RF/RNF, reglas, C4, BD | ARCHIVAR HISTÓRICAMENTE |
| `README.md` | Sin versión/fecha | Índice, descripción y guía de repositorio | Referencia a casi toda la documentación | CONSERVAR Y ACTUALIZAR |
| `REPORTE_AUDITORIA_CI.md` | 26-10-2026 | Auditoría CI/CD y correcciones reportadas | Workflow CI, manifiestos | ARCHIVAR HISTÓRICAMENTE |
| `REPORTE_RENDIMIENTO_EN_001.md` | 26-10-2026 | Medición del solver para EN-001/RNF-001 | Verificación e informe S2 | CONSERVAR Y ACTUALIZAR |
| `REPORTE_VERIFICACION_DOD_SPRINT_1.md` | 26-10-2026 | Evidencia DoD S1 | Backlog, QA, revisión S1 | CONSERVAR Y ACTUALIZAR |
| `VERIFICACION_FINAL_SPRINT_2.md` | 26-10-2026 | Auditoría técnica y QA S2 | Rendimiento, plan S2, pruebas | CONSERVAR Y ACTUALIZAR |

## 2. Redundancias y trazabilidad legítima

| Conjunto | Evaluación | Clasificación | Acción recomendada |
|---|---|---|---|
| Informes oficiales S1, plan S1 y reporte DoD S1 | No son duplicados directos: uno describe gestión, otro intención técnica y otro evidencia QA. | CONSERVAR | Mantener; actualizar sus enlaces y señalar el estado de cierre vigente. |
| Informes oficiales S2, plan S2, rendimiento y verificación final | Trazabilidad válida, aunque se repiten brechas de DoD, PostGIS, cobertura y SLA. | CONSERVAR | Definir `VERIFICACION_FINAL_SPRINT_2.md` como fuente técnica de estado y resumir desde los demás documentos. |
| RF/RNF/reglas/planificación ágil | Repetición esperable entre especificación, reglas y BDD. | CONSERVAR | Establecer qué documento es fuente primaria por tipo de criterio. |
| `PLAN_IMPLEMENTACION_SPRINT_1.md` y `PLAN_IMPLEMENTACION_SPRINT_2.md` | Son planes retrospectivos, conservan análisis y decisiones que posteriormente se implementaron o invalidaron. | ARCHIVAR HISTÓRICAMENTE | No fusionarlos ni borrar información; rotularlos como “plan al 26-10-2026”. |
| `REPORTE_AUDITORIA_CI.md` | Describe fallos ya corregidos y la corrección realizada. | ARCHIVAR HISTÓRICAMENTE | Mantener como evidencia; no usar como estado actual del CI. |
| Registro de impedimentos S1 y S2 | S2 repite IMP-004, IMP-005, IMP-006 e IMP-009 como referencia de continuidad. | REVISAR POR REDUNDANCIA | Mantener las referencias, pero usar enlaces correctos y marcar explícitamente “heredado, no duplicado”. |

No hay evidencia suficiente para proponer eliminar documentación académica, evidencias Jira, planes históricos o reportes QA.

## 3. Documentos desactualizados frente al repositorio

1. `README.md` presenta `EcologisticaJunin/` como el código fuente principal. La implementación activa realmente está en `app/`, `src/`, `tests/`, `backend/` y `frontend/`.
2. `README.md`, Documento 10 y Documento 12 presentan como componentes actuales Google OR-Tools / DEAP, Redis / Celery, OSRM local, y PWA offline con IndexedDB y Service Workers. La evidencia de implementación y los manifiestos revisados indican que el motor actual es un algoritmo genético propio; OSRM es opcional o apagado; no se observan dependencias de OR-Tools, DEAP, Redis ni Celery; y la funcionalidad PWA offline no está verificada como implementada.
3. `docs/01 Inicio/11. Base de datos V_1_0_3.md` documenta `GEOGRAPHY`, entidades y campos que no coinciden completamente con la implementación descrita en el plan/verificación S2, que reconoce el uso de `geometry` 4326 y ausencia de algunas tablas/campos planificados.
4. `docs/01 Inicio/04...Supuestos_y_Restricciones...` asume OSRM local como fuente de tráfico y matrices; esa condición sigue pendiente de validación o no está activa.
5. `docs/03 Implementación/Sprint 1/02_registro_de_impedimentos_v_1_0_1.md` conserva el relato de PWA con IndexedDB/Service Workers como resolución de IMP-003. La evidencia S2 posterior indica que EN-004 permanece fuera de alcance y sin verificación. Debe corregirse como “solución prevista/parcial” o respaldarse con evidencia.

## 4. Contradicciones relevantes

| Tema | Documentación en conflicto | Evidencia disponible | Riesgo |
|---|---|---|---|
| Motor de optimización | Docs 10, 12, README y backlog indican OR-Tools/DEAP; plan y verificación S2 declaran GA propio. | `REPORTE_RENDIMIENTO_EN_001.md` identifica `genetic_solver.py`; manifiestos no declaran OR-Tools/DEAP. | Alto: arquitectura y alcance técnico ambiguos. |
| Persistencia geográfica | Doc 11 y backlog exigen `GEOGRAPHY`; S2 documenta `geometry` 4326 y brechas de modelo. | `PLAN_IMPLEMENTACION_SPRINT_2.md`, informe S2 y verificación. | Alto: contrato de datos no consolidado. |
| OSRM | Docs de inicio lo describen como componente seleccionado; S2 lo define opcional/apagado. | Plan y verificación S2. | Medio: métricas ETA y arquitectura de rutas. |
| PWA offline | Documento 10, README e IMP-003 la describen como implementada; S2 deja EN-004 fuera de alcance. | Informe y revisión S2. | Alto: se afirma una capacidad no verificada. |
| Estado del Sprint 1 | Las versiones V_1_0_1 corrigen afirmaciones antiguas de 100 % y DoD cumplida. | Las V_1_0_0 que supuestamente sustituyen no existen en el árbol actual. | Medio: trazabilidad incompleta. |
| DoD y pruebas | Informes S1/S2 actuales indican DoD no cumplida, cobertura inferior a 80 %, E2E pendiente, Sonar/CodeQL no ejecutado. | `REPORTE_VERIFICACION_DOD_SPRINT_1.md` y `VERIFICACION_FINAL_SPRINT_2.md`. | Alto: no debe declararse “Sprint terminado” en sentido formal. |
| Rendimiento EN-001 | Tiempo del solver cumple en benchmark, pero solución válida 150×15 no es sistemática y HTTP total no fue medido. | `REPORTE_RENDIMIENTO_EN_001.md`, verificación S2. | Alto: RNF-001 sigue parcial. |
| Reglas normativas RN-002/RN-003 | Documentación de requisitos las describe como obligatorias; reglas e impedimentos las marcan pendientes de validación normativa. | Documento 09 e impedimentos S1/S2. | Medio: riesgo de presentar cumplimiento legal no validado. |

## 5. Enlaces rotos confirmados

Los enlaces del README a documentos existentes de Inicio, Planificación y Sprint 2 son coherentes a nivel de estructura. Sin embargo, se detectaron enlaces internos rotos reales.

### Sprint 1

Los cuatro documentos usan `../../` para referirse a archivos en la raíz. Desde `docs/03 Implementación/Sprint 1/`, la raíz requiere `../../../`.

Afectados:

- `01_informe_de_estado_del_proyecto_v_1_0_1.md`
- `02_registro_de_impedimentos_v_1_0_1.md`
- `03_revision_del_sprint_v_1_0_1.md`
- `04_retrospectiva_del_sprint_V_1_0_1.md`

Enlaces afectados: `README.md`, `PLAN_IMPLEMENTACION_SPRINT_1.md` y `REPORTE_VERIFICACION_DOD_SPRINT_1.md`.

### Sprint 2 hacia Sprint 1

Los documentos S2 enlazan archivos de Sprint 1 con rutas como `../03_revision_del_sprint_v_1_0_1.md`, pero el destino real está en el directorio hermano `Sprint 1/`. Deben apuntar a `../Sprint 1/03_revision_del_sprint_v_1_0_1.md`.

Afectados: informe S2, impedimentos S2, revisión S2 y retrospectiva S2.

### README y versiones históricas S1

README enlaza cuatro documentos históricos V_1_0_0 de Sprint 1 que no están presentes:

- `docs/03 Implementación/01_informe_de_estado_del_proyecto_v_1_0_0.md`
- `docs/03 Implementación/02_registro_de_impedimentos_v_1_0_0.md`
- `docs/03 Implementación/03_revision_del_sprint_v_1_0_0.md`
- `docs/03 Implementación/04_retrospectiva_del_sprint_V_1_0_0.md`

Los documentos V_1_0_1 declaran sustituirlos, pero la ausencia de las versiones reemplazadas impide conservar esa trazabilidad mediante enlaces.

## 6. Problemas de versionamiento

- El Documento 12 se llama `V_1_0_6`, mientras su encabezado declara `V_1_0_3`.
- Documento 00 exige nombres de versiones que no coinciden con los archivos reales de RF y RNF: el texto cita versiones `V_1_0_3`, pero los archivos vigentes son `V_1_0_0`.
- La nomenclatura no es uniforme: `V_1_0_0`, `V1.0.0`, `v_1_0_0`, “SemVerDoc” y documentos sin versión.
- Varios documentos no incorporan fecha o historial de cambios visible.
- Las fechas de modificación del sistema de archivos no sirven como fecha documental: todos reflejan el checkout actual; deben usarse las fechas declaradas y Git.
- Los documentos S1 V_1_0_1 sustituyen versiones V_1_0_0 no disponibles. Debe aclararse si nunca se versionaron, fueron eliminadas antes del registro o deben recuperarse desde Git.

## 7. Documentos que deben preservarse

No deben eliminarse sin una decisión de gobernanza documental:

- Todos los documentos de `docs/01 Inicio/`.
- El backlog y DoD en `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md`.
- Evidencias Jira y capturas.
- Todos los informes oficiales de Sprint 1 y Sprint 2.
- `PLAN_IMPLEMENTACION_SPRINT_1.md` y `PLAN_IMPLEMENTACION_SPRINT_2.md`.
- `REPORTE_AUDITORIA_CI.md`.
- `REPORTE_RENDIMIENTO_EN_001.md`.
- `REPORTE_VERIFICACION_DOD_SPRINT_1.md`.
- `VERIFICACION_FINAL_SPRINT_2.md`.

Son evidencia de evolución, decisiones, limitaciones o auditoría; la repetición que contienen es principalmente trazabilidad legítima.

## 8. Propuestas de actualización

Prioridad alta:

1. Actualizar README para reflejar la estructura ejecutable real y declarar el estado de `EcologisticaJunin/` como prototipo histórico.
2. Corregir enlaces rotos de S1/S2 y retirar o sustituir los cuatro enlaces históricos S1 inexistentes.
3. Crear una sección “Estado técnico vigente al cierre S2” en README, con enlaces a la verificación S2 y al reporte EN-001.
4. Actualizar Documento 10 y Documento 12 para distinguir arquitectura objetivo, componentes implementados y componentes pospuestos, opcionales o no verificados.
5. Resolver la contradicción `GEOGRAPHY` versus `geometry` mediante una decisión arquitectónica versionada.
6. Corregir el encabezado/versionado de Documento 12.

Prioridad media:

1. Añadir a los documentos de requisitos una sección breve de “estado de implementación” enlazada a la evidencia de Sprint, sin alterar su valor como baseline.
2. Actualizar IMP-003 para no afirmar PWA offline como implementada sin evidencia reproducible.
3. Actualizar `docs/qa/COMANDOS_CALIDAD.md` con requisitos de entorno y separación clara entre comandos que sólo leen y pruebas que escriben en `ecologistica_test`.
4. Definir una fuente única de estado para cada tipo:

| Dominio | Fuente primaria propuesta |
|---|---|
| Requisitos y reglas | Docs 06, 07 y 09 |
| Backlog, BDD y DoD | Planificación 01 |
| Arquitectura objetivo | Docs 10, 11 y 12 |
| Estado técnico real | `VERIFICACION_FINAL_SPRINT_2.md` |
| Rendimiento EN-001 | `REPORTE_RENDIMIENTO_EN_001.md` |
| Estado de Sprint | Informe de estado respectivo |
| Incidencias activas | Registro de impedimentos respectivo |

## 9. Propuestas de fusión o archivo

No se recomienda fusionar documentos oficiales de Sprint ni eliminar evidencias.

- **Archivar históricamente** `PLAN_IMPLEMENTACION_SPRINT_1.md`, `PLAN_IMPLEMENTACION_SPRINT_2.md` y `REPORTE_AUDITORIA_CI.md`, con una leyenda visible de fecha y estado.
- Mantener `VERIFICACION_FINAL_SPRINT_2.md` como documento principal de evidencia QA S2.
- Mantener `REPORTE_RENDIMIENTO_EN_001.md` como anexo especializado, no fusionarlo: contiene protocolo y limitaciones valiosas.
- Mantener `REPORTE_VERIFICACION_DOD_SPRINT_1.md` como evidencia de cierre S1, no fusionarlo con la revisión oficial.
- No archivar aún los documentos de Inicio: varios son baselines requeridos para trazabilidad y evaluación académica.

## 10. Recomendaciones para preparar Sprint 3

1. Resolver los enlaces antes de crear documentación de S3.
2. Congelar y etiquetar el estado documental S2 como “implementación parcial / DoD pendiente”.
3. Crear una matriz única `requisito → historia → evidencia → estado → limitación` para S3.
4. No reutilizar porcentajes de cobertura, resultados de CI, rendimiento HTTP o estado de seguridad sin una ejecución verificable nueva.
5. Registrar explícitamente si una historia S3 depende de PostGIS disponible, validación normativa, GeoJSON distrital con fuente, corrección de pruebas S2 o medición HTTP integral de EN-001.
6. Mantener separados “objetivo/plan” y “resultado/evidencia”; esta separación ya comenzó correctamente en las versiones corregidas de S1 y los informes S2.
7. No declarar completado el DoD global hasta disponer de evidencia de suite integrada, cobertura, análisis de seguridad, revisión por pares y staging.
