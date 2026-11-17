# Verificación final exhaustiva de la consigna HTML

**Corte:** 17/11/2026, America/Lima (UTC−5). **Versión del informe:** 1.0.0.  
**Repositorio:** C:\Users\Baguette\Documents\Proyectos\ecologistica-junin.  
**Rama y commit:** main · b47d5eb7cda26444c56460ea74591cc5f973e0b3 (Sprint 4).  
**Dictamen general: NO cumple todos los requisitos aplicables.** Existe implementación sustantiva y estructura documental correcta, pero faltan cálculos EVM sustentados, radiadores, cierre/aceptación y validación integral; permanecen riesgos técnicos altos. No se declara el sistema terminado ni listo para una demostración integral.

## Objetivo, autoridad y límites

Contrastar las cinco secciones completas del HTML docente con documentos, código, pruebas y Git actuales. El texto adjunto del usuario es la instrucción de ejecución; el HTML es la fuente de requisitos evaluados, no una autorización para alterar el proyecto. Esta auditoría sustituye la ejecución de fases de mensajes anteriores: no implementa correcciones ni completa documentos oficiales.

**Audiovisual: EXCLUIDO TEMPORALMENTE — NO EVALUADO.** No se examinó la carpeta excluida ni archivos audiovisuales, no se califica su presencia/ausencia y no se incorpora a pendientes ni denominadores. La demostración técnica **en vivo de diez minutos sí está incluida**, además de los diez minutos de exposición de gestión indicados en el encabezado del HTML.

Estados: **CUMPLE** = evidencia suficiente; **CUMPLE PARCIALMENTE** = avance sustantivo con condiciones pendientes; **NO CUMPLE** = ausencia obligatoria o incumplimiento concreto; **NO VERIFICABLE** = evidencia insuficiente. “No disponible” es una declaración honesta, pero no satisface una exigencia de resultados reales. Un test verde no equivale a aceptación de usuario, porcentaje funcional ni EV.

Solo se autoriza crear los cuatro informes nuevos en AUDITORIA. No se modificaron archivos preexistentes de código, pruebas, configuración, README o documentos oficiales; no se ejecutaron migraciones ni operaciones de BD, instalaciones, commits o push. **Hubo una excepción de ejecución:** Vitest creó inesperadamente .vitest/json/output.json fuera de AUDITORIA. Se informó al usuario, se detuvo ese uso del reportero y se conservó el archivo sin borrarlo ni moverlo. Véase el control de integridad final.

## Fuentes y trazabilidad

| Código | Fuente revisada y función |
|---|---|
| S01 | HTML completo: C:\Users\Baguette\Downloads\Consigna de evaluación final y cierre del proyecto.html, secciones 1–5; SHA256 098e994680f3a923a7b339a655ddf876a5b3ca712357884ef5c8697a4186a6a2. Se contrastaron contenidos, rúbrica y siete plantillas, no solo títulos. |
| S02 | README.md, .gitignore, package.json, pyproject.toml, configuración, Git status/log/diff/ls-files/check-ignore/tag y estructura del árbol. |
| S03 | Lectura de los siete archivos completos de docs/04 Cierre. D01…D07 designan el número inicial del archivo exacto listado abajo. |
| S04 | docs/01 Inicio: Directrices y Auditoría, enfoque, Acta de constitución, visión, supuestos/restricciones, interesados, RF/RNF, usuarios, reglas, stack, base de datos y C4. docs/02 Planificacion: transformación ágil, Artefactos Jira, riesgos y presupuesto. docs/03 Implementación: estados, impedimentos, reviews y retrospectivas de Sprints 1–3, calidad, OWASP, WCAG y reducción del impacto ambiental. |
| S05 | AUDITORIA/AUDITORIA_ESTADO_ACTUAL.md, ANALISIS_SPRINTS.md, BACKLOG_IMPLEMENTACION.md, CUMPLIMIENTO_REQUERIMIENTOS.md, RESUMEN_EJECUTIVO.md; planes/resultado B-08, informes SPRINT4_*, CONTROL_FASES_3_4_5.md, validación de cierre, matriz final y evidencias técnicas posteriores. Sus conclusiones se recontrastaron; no se heredaron porcentajes técnicos. |
| S06 | docs/02 Planificacion/Capturas en JIRA/01-roadmap.png a 05-versiones-release.png y documentación que las referencia. Son imágenes proporcionadas, no acceso autenticado a Jira ni historial exportado verificable. |
| S07 | app/: API, autenticación, websockets, servicios, solver, modelos/esquemas, DB/migraciones, indicadores y PDF; src/: API, rutas/páginas/componentes, mapa, conductor/offline; tests/, scripts/ y workflows/configuración. |
| S08 | Pruebas de esta ejecución y registros terminales sintetizados aquí; .vitest/json/output.json actual (artefacto accidental); AUDITORIA/FASES_3_4_5_EVIDENCIAS/backend_junit.xml, frontend_results.json, backend_coverage.json, frontend_coverage/coverage-summary.json, benchmark_solver_actual.json y baseline_entrada.json, **históricos**. |
| S09 | AUDITORIA/GUIA_SUSTENTACION_20_MINUTOS.md, CHECKLIST_ENTREGA_FINAL.md, RESULTADO_REVISION_FINAL.md y documentación de despliegue/operación en README y deployment. Un guion no acredita una demostración observada. |

**Fuente inicial ausente:** no se localizó el original independiente de la consigna inicial EcoLogística. Los requisitos 150 pedidos/15 vehículos/45 s y reoptimización <30 s se contrastan con la solicitud actual, el catálogo local y las auditorías; no se atribuye literalidad a un original no disponible. El acta documenta adaptación a Huancayo/El Tambo/Chilca; la referencia histórica Lima no se sustituye por una consigna reconstruida.

Las cinco auditorías iniciales y las fases previas son antecedentes, no aprobaciones. Frente al baseline de fase 3 se cotejaron **299 archivos fuente/pruebas/configuración con igual contenido**. El commit actual incorporó B-08; por ello hay correspondencia técnica con evidencias previas, pero sus pruebas de BD siguen siendo históricas, no reejecutadas ahora.

## Matriz completa de requisitos aplicables del HTML

Universo de conteo: **56 comprobaciones H01–H56**, agrupadas por obligaciones del encabezado, §§1–3, indicadores de §4 y campos de §5. Las tablas detalladas siguientes descomponen esos grupos, **sin sumarlas otra vez**. No son 56 funcionalidades, igual peso académico ni porcentaje de producto terminado. Se incluyen los subgráficos exigidos por la plantilla aunque el texto general los presente como ejemplos. Medidores/barras son alternativa; una página ejecutiva es recomendación, no defecto obligatorio.

| ID | Exigencia y sección | Estado | Fuente | Observación verificable |
|---|---|---|---|---|
| H01 | §2/§5: siete archivos, ruta y nombres exactos | **CUMPLE** | S03 | Siete de siete presentes en docs/04 Cierre. |
| H02 | §5: Markdown, identificación, corte y versión | **CUMPLE** | S03 | Formato y versión 1.0.0 presentes; el cierre se identifica como borrador. |
| H03 | §5.1–5.7: secciones, campos y tablas de las plantillas | **CUMPLE** | S01/S03 | Estructura conservada; no equivale a valores completos. Detalle por documento abajo. |
| H04 | §1/§2: datos reales específicos y coherentes | **CUMPLE PARCIALMENTE** | S03/S04/S06 | Contenido específico con límites honestos, pero múltiples campos no disponibles y fuentes históricas sin conciliación. |
| H05 | §1/§5: sustitución de marcadores de plantilla | **CUMPLE** | S03 | No se localizaron marcadores [ ? ] en los siete archivos. La ausencia del marcador no acredita el dato faltante. |
| H06 | §1: desempeño frente a líneas base aprobadas y periodo anterior | **NO VERIFICABLE** | S04/S03 | Hay planes y estimaciones; faltan aprobación y series temporales comparables. |
| H07 | §2.1/§5.1: logros, cambios de alcance y defectos | **CUMPLE PARCIALMENTE** | D01/S05/S07 | B-08 y defectos concretos descritos; no aceptación integral ni exenciones aprobadas. |
| H08 | §2.1/§5.1: hitos, fechas reales, causas, ruta crítica y acciones | **NO CUMPLE** | D01/S04 | Diagnóstico y acciones propuestos; sin calendario base-real verificable ni impacto cuantificado en ruta crítica. |
| H09 | §2.1/§5.1: fondos ejecutados, variaciones y contingencia | **NO CUMPLE** | D01/S04 | No hay ejecución financiera ni consumo real de reserva documentados. |
| H10 | §2.1/§5.1: Look Ahead de actividades y costos | **CUMPLE PARCIALMENTE** | D01 | Actividades priorizadas concretas; costos siguientes no disponibles y calendario sin compromiso aprobado. |
| H11 | §2.1/§5.1: nuevos riesgos, incidentes y comentarios | **CUMPLE PARCIALMENTE** | D01/D06/S04 | Defectos y riesgos específicos; respuesta propuesta no equivale a cierre aprobado de cada incidente. |
| H12 | §2.2/§5.2: variación cronograma, plan/real/causa/respuesta | **NO CUMPLE** | D02/S04 | Tabla de cinco campos existe; falta variación temporal calculable con fechas y baseline válidos. |
| H13 | §2.2/§5.2: variación de costo, plan/real/causa/respuesta | **NO CUMPLE** | D02/S04 | No AC ni comparación de gasto real contra presupuesto aprobado. |
| H14 | §2.2/§5.2: variación de calidad, métricas/defectos/causas/acciones | **CUMPLE PARCIALMENTE** | D02/S05/S07 | Cobertura y fallo identificables; corte histórico y gate/aceptación todavía incompletos. |
| H15 | §2.3/§5.3: BAC aprobado, unidad y estado financiero | **NO VERIFICABLE** | D03/S04 | Presupuestos referenciales no prueban BAC aprobado. |
| H16 | §2.3/§5.3: PV/EV/AC del periodo y acumulados actual/anterior | **NO CUMPLE** | D03 | Columnas presentes, nueve celdas sin cifras sustentadas. |
| H17 | §2.3/§5.3: SV/CV/SPI/CPI calculados e interpretados | **NO CUMPLE** | D03 | Fórmulas correctas, resultados inexistentes; indicadores numéricos NO VERIFICABLES. |
| H18 | §2.3/§5.3: porcentajes PV/EV/AC respecto a BAC | **NO CUMPLE** | D03 | Expresiones presentes sin aplicación numérica. |
| H19 | §2.3/§5.3: tres EAC y selección justificada | **NO CUMPLE** | D03 | Tres expresiones correctas; no proyecciones numéricas ni selección fundamentada en datos. |
| H20 | §2.3/§5.3: causas e impactos financieros/temporales EVM | **NO VERIFICABLE** | D03/S04 | No puede deducirse sobrecosto o retraso EVM sin magnitudes base. |
| H21 | §2.4/§5.4: KPIs justificados, interesados, frecuencia e interpretación | **CUMPLE PARCIALMENTE** | D04 | Selección/frecuencia propuestas y lectura específica; sin operación periódica consolidada. |
| H22 | §2.4/§5.4: RAG por componente con enfoque y umbrales | **CUMPLE** | D04/S05 | Semáforo específico con backend, B-08, frontend, seguridad y finanzas; verde backend limitado al ensayo histórico indicado. |
| H23 | §5.4.3.1: líneas de tendencias/variación/EVM | **NO CUMPLE** | D04/D03 | Sin serie numérica ni gráfico EVM; la explicación de ausencia no lo sustituye. |
| H24 | §5.4.3.2: flujo acumulado/áreas apiladas | **NO CUMPLE** | D04/S06 | No CFD ni serie de estados a lo largo del tiempo. |
| H25 | §5.4.3.3: SPI/CPI con tamaño CSI e interpretación | **NO CUMPLE** | D04/D03 | No gráfico ni datos. Exigido por la plantilla/rúbrica; no inventar índices. |
| H26 | §5.4.3.4: medidor o barras con datos y lectura | **CUMPLE** | D04/S05 | Mermaid con aprobadas [185,68,4] y fallidas [0,1,0], trazable al ensayo histórico. La alternativa barras satisface este subapartado. |
| H27 | §2.5/§5.5: Burndown real y análisis de tasa | **NO CUMPLE** | D05/S06 | No captura/serie de trabajo restante real por fecha. |
| H28 | §2.5/§5.5: Burnup real y análisis de alcance/aceptado | **NO CUMPLE** | D05/S06 | No serie de alcance y trabajo aceptado por fecha. |
| H29 | §2.5/§5.5: Kanban y cuellos de botella | **CUMPLE PARCIALMENTE** | D05/S06 | Imagen legible del proyecto y lectura de columnas; fecha/procedencia y evolución no acreditadas. |
| H30 | §2.5/§5.5: Mood Chart e interpretación del clima | **NO CUMPLE** | D05 | Tabla con No disponible; no mediciones del equipo. No permite inferir satisfacción. |
| H31 | §2.5/§5.5: tablero real de retrospectiva y acciones implementadas | **NO CUMPLE** | D05/S04 | Relatos/propuestas no son captura ni registro validado de retrospectiva y sus acciones. |
| H32 | §2.6/§5.6: descripción y alineación con Charter | **CUMPLE** | D06/S04 | Proyecto de logística urbana Huancayo/El Tambo/Chilca alineado con el acta; metas se presentan como objetivos. |
| H33 | §2.6/§5.6: alcance/calidad predictivos y adaptativos, validación/exenciones | **CUMPLE PARCIALMENTE** | D06/S07 | Diferenciación y brechas específicas; aceptación y exenciones formales no acreditadas. |
| H34 | §2.6/§5.6: hitos previstos vs. fechas reales | **NO CUMPLE** | D06/S04/S06 | Faltan fechas reales aceptadas y reconciliación del calendario 2024/2026. |
| H35 | §2.6/§5.6: presupuesto aprobado vs. costo final y tolerancia | **NO CUMPLE** | D06/S04 | Hay estimación, no costo final ni aprobación/tolerancia verificables. |
| H36 | §2.6/§5.6: riesgos/incidentes/impedimentos e impacto/respuesta aplicada | **CUMPLE PARCIALMENTE** | D06/S04/S07 | Registro y respuestas técnicas concretas; subsisten impedimentos y falta validación de cierre. |
| H37 | §2.6/§5.6: éxito, satisfacción, cierre administrativo y transición | **NO CUMPLE** | D06 | Sin métricas auténticas de satisfacción, acta de cierre/aceptación ni transferencia validada. |
| H38 | §2.7/§5.7: ocho categorías de aprendizajes analíticos y accionables | **CUMPLE PARCIALMENTE** | D07/S04/S05 | Ocho categorías específicas y recomendaciones útiles; validación por equipo/reunión pendiente. |
| H39 | §2.7/§5.7: retrospectivas/reunión y conclusiones del cierre | **NO CUMPLE** | D07/S04 | Fecha/reunión de cierre no acreditadas; conclusiones provisionales no sustituyen ceremonia real. |
| H40 | §3/§4: separación y responsabilidades frontend/backend/configuración | **CUMPLE** | S02/S07 | src/ y app/ separados; API, servicios, modelos, pruebas y configuración identificables. |
| H41 | §3/§4: .gitignore y exclusión de dependencias/entornos/temporales | **CUMPLE PARCIALMENTE** | S02 | Dependencias y .env ignorados y no rastreados; .vitest/ no está excluido y apareció un residual durante esta auditoría. |
| H42 | §3: limpieza del árbol y archivos versionados | **CUMPLE PARCIALMENTE** | S02 | Entrada limpia; sin cambios de archivos previos. Salida incorpora residual accidental .vitest/json/output.json además de los cuatro informes. |
| H43 | §3/§4: ausencia de credenciales expuestas | **NO VERIFICABLE** | S02/S07 | Sin archivos .env privados/.key/.pem rastreados detectados; no escaneo exhaustivo de todos los blobs históricos ni certificación de secretos. |
| H44 | §3/§4: coherencia, historial y versión de artefactos previos afectados | **CUMPLE PARCIALMENTE** | S03/S04/S06 | Fuentes históricas preservadas; persisten referencias ausentes, fechas contradictorias y nombre/título de calidad discordantes. |
| H45 | §3/§4: siete enlaces directos desde README | **CUMPLE** | S02/S03 | Siete destinos exactos comprobados físicamente. |
| H46 | §3/§4: siete retornos al README principal | **CUMPLE** | S03 | Siete retornos ../../README.md resuelven al archivo raíz. |
| H47 | §1/§3: coherencia de referencias históricas usadas como evidencia | **NO CUMPLE** | S02/S04 | 31 ocurrencias rotas entre 156 referencias Markdown relativas revisadas; seis destinos distintos. |
| H48 | §3/§4: catorce enlaces bidireccionales funcionales | **CUMPLE** | S02/S03 | 14/14 válidos; no confundir con las otras 31 referencias históricas. |
| H49 | §3: historial Git y trazabilidad del corte | **CUMPLE** | S02/S05 | Commit completo identificado; historial local consultado. Evidencia anterior cotejada contra 299 archivos fuente/pruebas/configuración idénticos. |
| H50 | §1/§4: cumplimiento de criterios funcionales de aceptación | **CUMPLE PARCIALMENTE** | S07/S08 | Código sustantivo y pruebas parciales; defectos actuales y funcionalidades incompletas impiden aceptación integral. |
| H51 | §4: arranque frontend/backend/BD en entorno de exposición | **NO VERIFICABLE** | S07/S08 | No se inició stack ni se alteró BD; pruebas con mocks/unidades no prueban este arranque. |
| H52 | §4: integración efectiva frontend-backend en ejecución real | **NO VERIFICABLE** | S08 | Componentes usan dobles; sin sesión real actual contra BD/OSRM. |
| H53 | §4: flujo end-to-end y resultados coherentes sin fallos | **NO VERIFICABLE** | S07/S08 | No recorrido actual Pedido→Optimización→BD→Mapa→Conductor→Entrega→KPI→PDF. |
| H54 | Encabezado: exposición de gestión/cierre de diez minutos | **NO VERIFICABLE** | S01/S09 | Existe guía; no ensayo observado cronometrado. |
| H55 | §4: demostración técnica en vivo de diez minutos | **NO VERIFICABLE** | S01/S09 | No observada. No calificarla cero ni aprobarla por existencia de código. |
| H56 | §4: fluidez/aceptación y guía de despliegue para nivel superior | **NO VERIFICABLE** | S02/S09 | README/deployment y guion disponibles; no acreditan operación fluida ni aceptación final. |

**Resultado del universo:** 12 CUMPLE; 14 CUMPLE PARCIALMENTE; 20 NO CUMPLE; 10 NO VERIFICABLE. Total: 56. No se calculan porcentajes de implementación ni se incluyen los puntos audiovisuales.

**Opcionales/recomendaciones separados:** máximo de una página para D01 es recomendado; medidores no se exigen adicionalmente si hay barras; índice enriquecido y fluidez/despliegue son condiciones de nivel superior de rúbrica. No se penaliza inventando una obligación de microservicios o arquitectura físicamente separada en repositorios distintos.

## Los siete documentos: estructura y contenido

Todos existen en la ruta exacta docs/04 Cierre, con extensión .md, versión declarada 1.0.0, encabezados/tablas de plantilla y enlace de retorno. No hay marcadores de plantilla pendientes; sí datos sustantivos pendientes. Los documentos se identifican como **borradores**, no cierre aprobado.

| Documento | Existe | Estructura correcta | Contenido completo | Evidencia válida | Estado |
|---|---|---|---|---|---|
| 01 Reporte de Estado V_1_0_0.md | Sí | Sí: 5 apartados, metadatos y retorno | No: cronograma base-real, costos y proyección financiera faltantes | Parcial: B-08 y defectos trazables; comparación financiera no sustentable | CUMPLE PARCIALMENTE |
| 02 Reporte de Variación V_1_0_0.md | Sí | Sí: 3 dimensiones, cada tabla con plan/real/variación/causa/respuesta | No: cronograma y costo sin resultados reales calculables | Parcial: métricas de calidad históricas reales; faltan fechas/gastos | CUMPLE PARCIALMENTE |
| 03 Reporte de Análisis de Valor Ganado - EVM V_1_0_0.md | Sí | Sí: métricas en tres columnas, porcentajes, causas y 3 EAC | No: todas las magnitudes financieras y proyecciones sin aplicación numérica | No para EVM cuantitativo; sí para declarar honestamente falta de datos | NO CUMPLE |
| 04 Tableros de Control - Híbridos V_1_0_0.md | Sí | Sí: justificación, RAG y 4 tipos de visualización | No: faltan líneas, CFD y burbujas con series reales | Parcial: RAG y barras reproducibles de resultados históricos | CUMPLE PARCIALMENTE |
| 05 Radiadores de Información V_1_0_0.md | Sí | Sí: cinco radiadores y tabla Mood | No: faltan cuatro radiadores/series reales y validación del Kanban | Parcial: Kanban legible proporcionado; no prueba evolución ni clima | CUMPLE PARCIALMENTE |
| 06 Reporte Final del Proyecto V_1_0_0.md | Sí | Sí: descripción, alcance/calidad/cronograma/costo, riesgos y éxito | No: faltan fechas reales, costo final, satisfacción, aceptación y transición | Parcial: objetivos/riesgos/código reales; éxito no medido | CUMPLE PARCIALMENTE |
| 07 Reporte Final de Lecciones Aprendidas V_1_0_0.md | Sí | Sí: ocho categorías, tres columnas analíticas y conclusiones | No: reunión, validación de equipo y compromisos de cierre ausentes | Parcial: situaciones concretas de pruebas, alcance y datos faltantes; no acta de retrospectiva | CUMPLE PARCIALMENTE |

### Contraste específico con §§5.1–5.7

- **D01:** alcance tiene logros/cambios/defectos; cronograma contempla hitos, causas, ruta crítica y respuestas, pero sin fechas comparables; costo contiene los cuatro campos sin ejecución monetaria; Look Ahead tiene actividades sin costo sustentado; riesgos/incidentes/comentarios son específicos. No confundir propuesta de acción con ejecución aceptada.
- **D02:** las tres tablas contienen resultados planificados/reales, variación, causa y respuesta. La calidad sí relaciona tests/cobertura/defectos con acciones. Las variaciones de calendario/costo no se pueden recalcular sin fechas y gastos.
- **D03:** están BAC/estado, las siete filas PV/EV/AC/SV/CV/SPI/CPI × tres periodos, tres porcentajes, cuatro campos de causas/impactos y las tres expresiones EAC con selección. Falta contenido cuantitativo; véase la comprobación independiente.
- **D04:** incluye interesados, criterios de selección y frecuencia propuesta; RAG con enfoque/componente/umbral; cuatro subsecciones de gráficos. Tres explicaciones de ausencia no equivalen a tres gráficos. Las barras sí existen como diagrama estructurado, admitido por HTML.
- **D05:** Burndown y Burnup se declaran no disponibles; Kanban incorpora imagen; Mood conserva roles e iteraciones con datos no disponibles; retrospectiva no aporta tablero real ni acciones de una sesión validada.
- **D06:** describe Charter y diferencia gestión predictiva/adaptativa; explicita objetivos/criterios/evidencia/variaciones y requisitos no eximidos; tabla de hitos conserva enfoque/fechas/impacto; costo, riesgos y tres campos de éxito existen con faltantes explícitos. Metas 15 % km, 10 % CO₂ mensual, 90 % ventanas y 70 % MVP son objetivos, **no resultados medidos**.
- **D07:** cubre desempeño del equipo; evolución/control del alcance; integración del cronograma híbrido; presupuesto/costos; estimación de velocidad/duración/recursos; calidad; interesados; riesgos/incidentes/impedimentos. Hay prácticas/recomendaciones vinculadas a casos concretos, no solo frases genéricas. Falta acreditar retrospectiva y reunión de cierre, fecha, participantes y acciones efectivamente acordadas.

El validador histórico registra 24/14/31/16/19/30/18 campos (152 en total); la lectura actual confirma las estructuras. Ese número es control de presencia textual histórico, **no 152 requisitos sustantivos cumplidos**.

## Comprobación matemática independiente de EVM

Fuente principal: D03. Fuentes de respaldo buscadas: acta, presupuesto de planificación, estados/reviews, riesgos/impedimentos y evidencias de aceptación/costo. No se localizaron presupuesto aprobado, plan de desembolso temporal, registros reales de horas/gastos, regla presupuestada de avance aceptado, cambios/rebaseline aprobados o cortes financieros actual/anterior conciliados.

### Tabla de indicadores

“ND” significa dato no disponible, nunca cero. En las filas PV…CPI se revisaron separadamente **periodo actual / acumulado actual / acumulado anterior**: las tres columnas están presentes y ninguna contiene resultado financiero sustentado.

| Indicador | Valor documentado | Valor recalculado | Fuente | Estado |
|---|---|---|---|---|
| BAC | No disponible; presupuesto pendiente de validación | No calculable sin aprobación/baseline | D03; acta §presupuesto; presupuesto de planificación | NO VERIFICABLE |
| PV, tres cortes | ND / ND / ND | No calculable sin plan temporal presupuestado | D03; planificación sin curva aprobada por corte | NO VERIFICABLE |
| EV, tres cortes | ND / ND / ND | No calculable sin trabajo aceptado valorado según regla aprobada | D03; no actas/costos por entregable aceptado | NO VERIFICABLE |
| AC, tres cortes | ND / ND / ND | No calculable sin gasto/horas reales conciliados | D03; no libro de ejecución localizado | NO VERIFICABLE |
| SV = EV − PV, tres cortes | Fórmula correcta; ND / ND / ND | ND: faltan EV/PV | D03 | NO VERIFICABLE |
| CV = EV − AC, tres cortes | Fórmula correcta; ND / ND / ND | ND: faltan EV/AC | D03 | NO VERIFICABLE |
| SPI = EV / PV, tres cortes | Fórmula correcta; ND / ND / ND | ND: no PV/EV ni denominador validable | D03 | NO VERIFICABLE |
| CPI = EV / AC, tres cortes | Fórmula correcta; ND / ND / ND | ND: no AC/EV ni denominador validable | D03 | NO VERIFICABLE |
| % planificado = 100 × PV/BAC | Expresión sin resultado | ND: faltan PV/BAC | D03 | NO VERIFICABLE |
| % ganado = 100 × EV/BAC | Expresión sin resultado | ND: faltan EV/BAC | D03 | NO VERIFICABLE |
| % gastado = 100 × AC/BAC | Expresión sin resultado | ND: faltan AC/BAC | D03 | NO VERIFICABLE |
| EAC 1 = BAC/CPI | Fórmula correcta sin resultado | ND: faltan BAC/CPI | D03 | NO VERIFICABLE |
| EAC 2 = BAC/(CPI × SPI) | Fórmula correcta sin resultado | ND: faltan BAC/CPI/SPI | D03 | NO VERIFICABLE |
| EAC 3 = AC + (BAC − EV)/(CPI × SPI) | Fórmula correcta sin resultado | ND: faltan AC/BAC/EV/CPI/SPI | D03 | NO VERIFICABLE |
| EAC seleccionado y justificación | No selección cuantitativa posible | No determinable con la evidencia actual | D03 | NO VERIFICABLE |

Las siete expresiones base y las tres razones porcentuales coinciden con HTML. **No se verificó ninguna aplicación numérica EAC.** La ausencia de cálculos constituye NO CUMPLE del entregable exigido (H16–H19), mientras cada valor desconocido es NO VERIFICABLE. No se observó una división por cero ejecutada; no hay denominadores numéricos. En una aplicación futura, PV=0, AC=0 o BAC=0 requieren clasificar la razón correspondiente como no calculable y justificar el corte; no reemplazarla por cero ni infinito.

La interpretación general solo puede ser condicional: SV positivo indica EV mayor que PV en unidades presupuestarias, no días; CV positivo indica EV mayor que AC; SPI/CPI mayores que 1 suelen indicar desempeño favorable de cronograma/costo frente a esa baseline. No se atribuye al proyecto un sobrecosto, ahorro o adelanto específico. EAC1 prolonga desempeño de costo; EAC2 aplica desempeño conjunto al presupuesto; EAC3 agrega AC al trabajo restante ajustado. Son hipótesis distintas y su selección requiere justificar cuál representa el futuro; no escoger la menor cifra por conveniencia.

### Recalculo del presupuesto encontrado, sin convertirlo en BAC

Archivo: docs/02 Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md, fechado 15/09/2026.

| Partida estimada | Operación independiente | Resultado |
|---|---|---:|
| Mano de obra | 480×40 + 360×50 + 640×40 + 640×25 + 480×30 + 400×29,50 | USD 105 000 |
| Horas | 480+360+640+640+480+400 | 3 000 h |
| Licencias | 525+157,50+175+875+420+350+350+137,50+1 210 | USD 4 200 |
| Nube/infraestructura | 4 200+2 800+1 050+875+1 225+650 | USD 10 800 |
| Subtotal | 105 000+4 200+10 800 | USD 120 000 |
| Contingencia estimada | 120 000×12 % | USD 14 400 |
| Total estimado | 120 000+14 400 | USD 134 400 |
| Conversión referencial | 134 400×3,72 | PEN 499 968 |

**Aritmética correcta como estimación.** El acta del 25/08/2026 menciona PEN 500 000 de desarrollo y PEN 120 000/año de operación como referencias pendientes de validación local. La cercanía de 499 968 a 500 000 no prueba aprobación, ejecución ni autorización de contingencia. Las 3 000 horas son previstas, no realizadas. La narrativa de resolución del impedimento IMP-008 no aporta una aprobación financiera. No se utilizó implementación técnica, puntos de historia ni tests como EV.

Para conciliar tres cortes se necesitarían fechas, misma moneda/unidad, baseline versionada y relación periodo actual = acumulado actual − acumulado anterior para magnitudes aditivas. Los índices deben recalcularse de los acumulados, no sumarse/promediarse sin fundamento. No hay datos para comprobar esas identidades.

## Tableros, radiadores y procedencia visual

| Elemento | Evidencia observada | Evaluación |
|---|---|---|
| RAG | D04: métricas de backend, B-08, frontend, seguridad y finanzas con enfoques/umbrales | Válido para el corte histórico señalado; “backend verde” no significa sistema completo aprobado. |
| Barras de pruebas | Mermaid con 185/68/4 aprobadas y 0/1/0 fallidas, apoyado en registros anteriores | Visualización reproducible de datos reales, no captura histórica de Jira. El soporte Markdown admite diagramas estructurados; renderización en el visor de entrega no observada. |
| Líneas EVM / CFD / SPI-CPI-CSI | No hay series ni gráficos en D04 | Pendientes obligatorios por §5.4; no fabricar historia o finanzas para dibujarlos. |
| Burndown / Burnup | Ausencia expresamente documentada | Pendientes: requieren fechas, alcance/restante/aceptado y cambios auténticos. |
| Kanban | Imagen 04-tablero-scrum.png, columnas con 5/3/2/3 elementos visibles | Legible y rotulada EcoLogística Huancayo. Una instantánea no prueba velocidad, evolución, antigüedad del WIP ni cierre de tickets. |
| Mood | Tabla sin mediciones | No permite reconstruir satisfacción retrospectivamente ni inferir clima por tests. |
| Retrospectiva | Relatos y propuestas de sprints; no tablero real aportado | No acredita sesión/acciones implementadas; la retrospectiva Sprint 2 se identifica como borrador sin ceremonia formal. |

Las cinco imágenes proporcionadas corresponden nominalmente al proyecto, pero **su autenticidad, extracción de Jira y fecha efectiva no están certificadas**. No se concluye que sean inventadas. Hay incoherencias concretas que impiden usarlas como baseline actual sin aclaración:

- Roadmap con eje septiembre–diciembre de 2024; planificación textual de 2026.
- Sprint planning 01–31/10/2024, cuatro semanas, siete incidencias y 34 SP; no concilia con Sprint 1 textual de 20 SP de 2026.
- Backlog visible: cabecera 39 SP; ocho valores 8+3+5+8+5+8+5+5 = **47 SP**, diferencia de 8 SP.
- Imagen de release con 31/10/2024 y MVP 100 % frente a versión de aplicación 0.1.0 y sin tags locales. No constituye por sí sola release desplegada ni aceptación.

Se requiere exportación/procedencia, fechas y relación con tickets/versiones actuales, preservando las capturas originales. No retocar fechas de imágenes para hacerlas coincidir.

## Repositorio, README, versiones y seguridad

Arquitectura de monolito modular backend en app/ y cliente en src/, con API/servicios/modelos diferenciados. No se encontró necesidad de reorganizar para cumplir la separación pedida. Dependencias locales instaladas no son contaminación Git cuando están correctamente ignoradas. Configuración de API/BD/OSRM y despliegue documentada; operación efectiva depende del entorno.

Los siete enlaces directos y siete retornos fueron resueltos contra el sistema de archivos: **14/14 correctos**. De **156 ocurrencias relativas Markdown** en README y documentación aplicable, se localizaron **31 referencias rotas**, hacia seis destinos distintos:

1. docs/ESTADO_TECNICO_VIGENTE.md.
2. Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_VERIFICACION_DOD_SPRINT_1.md.
3. Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md.
4. Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_RENDIMIENTO_EN_001.md.
5. Auditorias-EcoLogistica/02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_1.md.
6. Auditorias-EcoLogistica/02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_2.md.

Las referencias rotas están en Directrices/Stack/BD/C4 y estados/reviews/retrospectivas de Sprints 1–2. La comprobación valida existencia de destinos relativos locales; no certifica cada URL remota, ancla Markdown o recurso de producción.

Git entró limpio, HEAD b47d5eb…, historial legible y sin tags locales. package.json y pyproject.toml declaran 0.1.0; los siete documentos iniciales de cierre declaran 1.0.0, lo cual no es por sí solo contradicción porque son productos/versiones diferentes. Sí existe título interno V_1_1_0 en calidad Sprint 3 con nombre de archivo V_1_0_0, y referencias de riesgo con revisión “v2” sin reconciliación completa. README conserva situación Sprint 3 no Done mientras su review histórica declara resultados satisfactorios; debe distinguirse cada corte.

En D02/D04/D06 aparece la referencia corrupta **“HEAD 61 f0 e1 e+B-08 sin commit”**. Era un corte histórico previo, no un cambio sucio actual, pero la cadena no es un identificador Git resoluble. Restituir el hash real y explicar su corte en un ciclo autorizado. Otros espacios artificiales (“E2 E”) o el signo “?” del encabezado de gestión del README son defectos editoriales menores; no son marcadores [ ? ] del HTML.

.gitignore cubre .env y variantes salvo plantilla, node_modules, .venv, caches, dist, logs y temporales comunes. git ls-files no encontró entornos/dependencias, .env privados ni archivos .key/.pem rastreados bajo la búsqueda delimitada. **Esto no certifica ausencia de secretos en cada línea/blob de todo el historial.** No se publican valores de credenciales. Hay valores demo/default en configuración que requieren validar el entorno antes de exposición; no se demostró fuga de credenciales productivas. .vitest/ no está ignorado; el residual observado fue originado por esta auditoría y se atribuye a ella.

## Auditoría funcional por módulo

La columna Estado aplica los cuatro estados de cumplimiento, no un porcentaje. “Histórico equivalente” remite a fuentes/pruebas iguales en 299 archivos, sin reejecución actual de BD. No se realizó explotación de seguridad ni ejecución sobre datos reales.

| Módulo | Implementado | Prueba ejecutada | Resultado | Evidencia | Estado |
|---|---|---|---|---|---|
| Autenticación/usuarios | Login JWT, roles, dependencias y protección de API/WS | Unidades seguridad/core actuales; API/BD omitidas. Histórico: auth/roles con BD | Partes pasan; sesión viva, revocación y autorización de asignación vigente sin cerrar | app/core/config.py; app/api/v1/routes.py y websockets.py; tests/test_security_en003.py; S08 | CUMPLE PARCIALMENTE |
| Flota | CRUD, estado, capacidades, consumos, factores y restricción por placa | Componentes actuales; un caso falla antes de terminar mantenimiento/edición; API histórica | 68/69 frontend global; fallo de contrato (1) vs (1,21). Falta tipo completo y validación integral por perfil | src/pages/fleet.test.tsx:65; Fleet.tsx:108; src/api.ts:178; modelos/logistics | CUMPLE PARCIALMENTE |
| Pedidos | Alta, Excel, geocodificación/coordenadas, ventanas, estados, edición | Componentes con mocks actuales; importación/ventanas/ubicación con BD históricas | No se acredita importación CSV equivalente ni atributos prioridad/producto/volumen completos; terminalidad pendiente | modelos/esquemas/API; S07/S08 y matriz Sprint 4 | CUMPLE PARCIALMENTE |
| Algoritmo genético | Población, fitness, selección, cruce, mutación, restricciones y solución persistible | Unidades solver/optimizer/restricciones actuales; B-08 28 actuales; persistencia B-08 histórica 14 | GA real, no simulación nominal; casos pequeños pasan. No SLA válido integral 150×15; benchmark histórico 0/3 factibles | genetic_solver.py; route_constraints.py; tests/test_publication_b08.py; benchmark JSON | CUMPLE PARCIALMENTE |
| Mapas/rutas/ETA | Leaflet/GeoJSON, puntos, detalle, filtros, OSRM/fallback | GeoJSON 4, OSRM 3, ETA 4 unidades actuales; componentes con dobles | Partes pasan; no proveedor/tiles/OSRM ni navegador end-to-end real actual; versiones requieren conciliación | tests/test_route_geometry_geojson.py, test_osrm_routing.py, test_eta_us009.py; src/components/Map.tsx | CUMPLE PARCIALMENTE |
| Dashboard | Distancia/CO₂/combustible y lecturas de indicadores | 2 unidades indicadores actuales y componentes con mocks | Suma de versiones, galones para eléctricos y puntualidad/ahorro real incompletos | app/services/operational_indicators.py:45; dashboard/frontend | CUMPLE PARCIALMENTE |
| Reportes | PDF, descarga y cálculos ambientales parciales | 2 unidades PDF actuales; endpoint con BD histórico | PDF lógico parcial; fecha de ETA/ventana sustituye fecha real, CSV/factores/costos/periodos sin cerrar | pdf_generator.py:633; tests/test_pdf.py; endpoint routes | CUMPLE PARCIALMENTE |
| Conductores/operaciones | Vista conductor, asignación, seguimiento y confirmación | Componentes actuales con mocks; endpoints históricos | Fecha real/actor/comprobante no persistidos integralmente; autorización por asociación histórica | routes.py:488; websockets.py:453; schemas/logistics.py:260; DriverApp | CUMPLE PARCIALMENTE |
| Offline | IndexedDB/cola, estados y Service Worker | Componentes actuales y 4 tests SW actuales | Casos simulados pasan; no ensayo de pérdida de red/reconexión concurrente contra servidor ni entrega durable integral | src/lib/offline.ts; scripts/test-service-worker.mjs; S08 | CUMPLE PARCIALMENTE |
| Reoptimización/WS | Inserción/cancelación/recalculo, validación B-08 antes de persistir, commit/avisos | 3 unidades realtime actuales + B-08 28; 14 B-08 BD históricas | B-08 mejora publicación y atomicidad. Avería multivehículo, reloj/jornada acumulados, terminalidad, privacidad y durabilidad pendientes | realtime_router.py; websockets.py:249/453/472; route_constraints.py | CUMPLE PARCIALMENTE |
| Flujo integral y aceptación | Componentes y endpoints conectables en diseño | No ejecutado actualmente con stack/BD/proveedores reales | Arranque y recorrido actual NO VERIFICABLES; sin acta de aceptación o exenciones | S07/S08/S09 | NO VERIFICABLE |

### Hallazgos técnicos concretos

1. **Asignación/terminalidad (B-09):** _require_order_on_vehicle_route y confirm_delivery seleccionan RutaDetalle por pedido/vehículo sin exigir versión activa. Un conductor previamente asociado podría conservar autorización tras reasignación. _on_cancel no impone estado terminal; _apply_reroute convierte eliminados en CANCELLED. Son riesgos por inspección actual, no ataques ejecutados.
2. **Privacidad pública (B-10):** _tracking_snapshot expone lat/lon exactas e IDs internos; publicación comparte payload de ruta/secuencia. Limpieza de tracking usa order_code frente al canal resuelto. No se capturaron datos de usuarios reales.
3. **Sesión WS (B-11):** duración JWT por defecto 12 h, token en URL y sin revalidación continua/revocación acreditada en el bucle. Las pruebas verdes no validan todo el ciclo.
4. **Versiones/KPI (B-13):** summarize_indicators suma soluciones sin excluir versiones sustituidas; hay riesgo de trabajo repetido y discrepancia de cabecera/detalle/mapa.
5. **Entrega real (B-14):** esquema recibe delivered_at, pero confirm_delivery solo cambia estado/bitácora sin evento durable completo. PDF _completion_day usa detail.eta u order.ventana_fin; no demuestra fecha efectiva.
6. **Ambiente/costo (B-12/15):** cálculo de combustible sin separar electricidad y combustibles, factores/unidades no unificados y costo/ahorro/puntualidad insuficientes. Equivalencia de quinuales no acredita compensación ejecutada.
7. **Upgrade (B-06/16):** columna de geometría del modelo sin equivalencia de actualización histórica demostrada. Los dos tests test_db_migrations actuales verifican procesamiento de SQL, **no migración real de un esquema legado**.
8. **Dinámica/operación:** estado FleetState en memoria, reoptimización centrada en vehículo y sin reloj/carga/jornada acumulada real acreditados; sin redistribución completa por avería. Reinicio, 50 vehículos, 1 000 pedidos/día y 99,5 % de disponibilidad sin ensayo representativo.
9. **Alcance restante:** clientes/preferencias, administración completa de conductores, prioridades/productos/tipo vehicular, CSV y plan de compensación no están íntegramente implementados ni eximidos. No se transforma esa ausencia en opcional.
10. **DoD:** suite frontend roja; umbral de cobertura no acordado/forzado integralmente (cov-fail-under=0), staging CI no acredita despliegue real, revisión por pares/seguridad/accesibilidad y aceptación siguen pendientes.

## Pruebas de esta auditoría y pruebas históricas

### Ejecución actual, segura salvo incidente de contención frontend

Se revisaron comandos/configuración/fixtures antes de ejecutar. Se usó Python del entorno existente .venv/Scripts/python.exe, -B/PYTHONDONTWRITEBYTECODE, addopts vacío y cacheprovider desactivado; EN001_WRITE=0, OSRM desactivado, URL de BD a puerto local sin servicio. Un plugin omite por cierre de fixtures todo acceso client/database/db_case y temporales tmp_path/tmpdir. No se ejecutó fixture que cree/trunque/modifique BD. No se corrió init_db ni migraciones.

| Grupo actual | Catálogo | Ejecutadas | Aprobadas | Fallidas | Omitidas/no ejecutadas | Evidencia |
|---|---:|---:|---:|---:|---:|---|
| Backend pytest | 185 | 95 | 95 | 0 | 90 | Sesión terminal exit 0, resumen y nodos abajo; addopts vacío, sin cobertura/cache |
| Frontend Vitest | 69 | 69 | 68 | 1 | 0 | JSON actual .vitest/json/output.json; success=false |
| Service Worker node:test | 4 | 4 | 4 | 0 | 0 | node --test scripts/test-service-worker.mjs, exit 0 |
| **Total de casos catalogados** | **258** | **168** | **167** | **1** | **90** | Las 90 omitidas no se suman como ejecutadas/aprobadas |

Comprobaciones adicionales, **fuera del total de casos**: TypeScript con node node_modules/typescript/bin/tsc --noEmit --incremental false: exit 0. Auditor estático del dist existente con node scripts/audit-green-build.mjs: exit 0, 434 872 bytes. No se compiló/build, no se cambió dist y esta lectura no demuestra correspondencia de ese build con HEAD ni despliegue.

**Fallo reproducido:** src/pages/fleet.test.tsx:65, “fleet management page loads fleet, validates maintenance and saves edits”. Espera fetchVehicleHistory(1); recibe fetchVehicleHistory(1,21). Fleet.tsx:108 solicita una página de 20 + 1 para detectar siguiente página; src/api.ts:178 acepta límite opcional. Se debe acordar el contrato y corregir prueba/implementación según requisito, no eliminar paginación para poner verde la suite sin revisar. El caso se interrumpe antes de validar todo mantenimiento/edición. No se demuestra por esta aserción un fallo productivo del historial.

**Incidente frontend:** se llamó Vitest por API con caché y cobertura desactivadas e intento de capturar reporter JSON en memoria. El reporter creó por defecto .vitest/json/output.json; la captura stdout no produjo JSON completo y su parseo terminó en SyntaxError. Se leyó el archivo real válido: 69/68/1/0; no se confundió el error del envoltorio con el fallo de aserción. SHA256 del artefacto: 31e739ba1b8d8ae00250e386666eb5fc901db13b12b8e19f326a685a79c39ac8. No se repitió Vitest ni se eliminó el residual.

### Desglose actual backend aprobado

| Archivo | Casos aprobados actuales |
|---|---:|
| tests/test_core_quality_units.py | 12 |
| tests/test_db_migrations.py | 2 |
| tests/test_eta_us009.py | 4 |
| tests/test_hard_constraints_us008.py | 9 |
| tests/test_operational_indicators.py | 2 |
| tests/test_optimizer_us007.py | 6 |
| tests/test_osrm_routing.py | 3 |
| tests/test_pdf.py | 2 |
| tests/test_publication_b08.py | 28 |
| tests/test_realtime.py | 3 |
| tests/test_route_geometry_geojson.py | 4 |
| tests/test_security_en003.py | 4 |
| tests/test_solver.py | 5 |
| tests/test_solver_sla_en001.py | 3 |
| tests/test_unit_services.py | 8 |

B-08: **28 unidades aprobadas ahora; 14 integraciones de BD no ejecutadas ahora**. Las pruebas “migrations” son unidades de división/procesamiento SQL y no elevan el estado de upgrade real a aprobado.

### Evidencia histórica conservada

| Evidencia anterior | Resultado documentado | Límite de uso actual |
|---|---|---|
| backend_junit.xml | 185 aprobadas, 0 fallidas/errores/omitidas; 59,087 s; timestamp 17/11/2026 03:54:31,783380−05:00 | PostGIS descartable de fase 3, ya retirado. No es la ejecución actual de 95 casos. |
| frontend_results.json | 68 aprobadas / 1 fallida / 69 | Antecedente; el mismo fallo se volvió a observar ahora. |
| backend_coverage.json | Líneas 3 773/4 531 = 83,27 %; ramas 667/1 112 = 59,98 %; combinado 4 440/5 643 = 78,68 % | No cobertura actual; hay que acordar qué métrica usa DoD. |
| frontend coverage-summary | Líneas 1 026/1 302 = 78,80 %; ramas 873/1 233 = 70,80 %; statements 76,76 %, funciones 76,51 % | No cobertura actual; líneas por debajo del 80 % citado en DoD. |
| benchmark_solver_actual.json | Tres ejecuciones solver 150×15, 150 asignados cada una, 0/3 factibles por ventanas | Benchmark anterior sobre código equivalente; sin HTTP/BD/OSRM/testigo de factibilidad. |

No se generó nueva cobertura ni se ejecutaron API/BD completas, build, escáner que escriba resultados, carga productiva, revisión WCAG visual/lector ni despliegue. Su omisión no equivale a aprobado ni a fallo observado. No se instalaron herramientas.

### Rendimiento y factibilidad

El benchmark previo usa dataset synthetic_orders(150, seed=901001), synthetic_vehicles(15, seed=901001), matriz geodésica, OSRM desactivado, población 24, tope 32 generaciones y semillas de búsqueda 901001/2/3. Tiempos de llamada: **0,972290 / 0,982327 / 0,903764 s**. Asigna 150 cada vez, pero late_minutes = **1974,551 / 1904,015 / 2258,498**, feasible=false en las tres. Excesos de peso/volumen/jornada registrados: cero. No hay testigo independiente que pruebe que esa instancia concreta sea factible, por lo que no se atribuye toda la infactibilidad al GA ni se afirma incapacidad universal.

Las unidades SLA actuales pasan las aserciones existentes de tiempo/asignación parcial; no exigen todo el criterio de aceptación. **No se acredita 150×15 factible ≤45 s de extremo a extremo ni reoptimización válida <30 s.** Cumplir tiempo de CPU sin factibilidad no basta. Se requiere dataset factible validado, restricciones completas, conteo/duplicados, persistencia/mapa y tiempo HTTP total incluyendo proveedor/matriz/BD.

## Preparación de la sustentación y demostración en vivo

No se levantó el stack con BD porque el arranque puede inicializar datos/esquema y esta auditoría no autoriza alterarlos. La decisión es **NO VERIFICABLE** para arranque, no “el sistema no arranca”. Tampoco se observó una sesión cronometrada, por lo que no se acredita duración, fluidez, login real ni integración efectiva. No hay error de arranque demostrado.

| Área para demostración | Clasificación | Condición pendiente |
|---|---|---|
| Autenticación y estructura de flota/pedidos | Listo con limitaciones | Evidencia parcial de código/componentes e histórico API; revalidar stack, perfiles y fallo de prueba antes de afirmar operación en vivo |
| GA y publicación B-08 en ejemplos acotados | Listo con limitaciones | No extrapolar unidades a SLA; confirmar testigo factible y aceptación humana |
| Mapas/ETA y PDF en entorno real | No verificable | OSRM/tiles/BD, descarga, geometría y periodos reales sin ensayo actual |
| Dashboard como resultado definitivo | No listo | Resolver versiones/unidades/puntualidad/costo y conciliación con PDF |
| Operación dinámica y tracking público | No listo | Asignación vigente, terminalidad, privacidad, sesión, averías y durabilidad |
| Offline en campo | No verificable | Reintentos/concurrencia/red real, sin pérdida o duplicación de entregas |
| Recorrido completo de diez minutos | No verificable; no se acredita preparación integral | Ensayo Pedido→Optimización→Persistencia→Mapa→Conductor→Entrega→Dashboard→Reporte, con evidencia consistente y sin bloqueos |

“Listo con limitaciones” identifica material parcial para preparar una muestra controlada, no autoriza afirmar que el módulo completo está listo ni que la demostración ya fue validada. La aceptación global continúa pendiente.

Dependencias externas de exposición: PostgreSQL/PostGIS y configuración de conexión; backend y URL/CORS/proxy del cliente; proveedor OSRM/tiles/geocodificación; HTTPS/WebSocket, reloj/zona horaria, conectividad, navegador/Service Worker/IndexedDB y permisos de geolocalización. Su disponibilidad real no se verificó. No usar una captura o un mock como prueba de conexión efectiva.

La exposición de gestión también necesita ensayo de diez minutos, aclaración de borradores y faltantes EVM. El guion existente ayuda a preparar, pero no sustituye resultados ni aceptación.

## Control de integridad y conclusión

Se tomó inventario SHA256 de **484 archivos preexistentes** antes de las comprobaciones, excluyendo .git, node_modules, .venv y el material expresamente fuera de alcance. La comparación final verifica esos archivos por contenido; no es una certificación de todos los archivos del equipo, dependencias ni superficies excluidas. Git estaba limpio al inicio. No hay modificación ni eliminación de esos archivos; los nuevos elementos de salida son los cuatro informes solicitados y **el residual accidental .vitest/json/output.json**. Los informes anteriores se conservaron; no hubo commit/push ni restauraciones. La excepción impide afirmar “ninguna escritura fuera de AUDITORIA”.

**Conclusión:** NO cumple todos los requisitos evaluados. La estructura de siete documentos y sus 14 enlaces está satisfecha; el contenido de cierre sigue siendo provisional. Faltan evidencia financiera/aceptación, visualizaciones/radiadores y validación integral; los riesgos de autorización, terminalidad, privacidad y consistencia operacional requieren corrección en otro ciclo autorizado. Los indicadores desconocidos no se inventaron, y las pruebas actuales no se mezclaron con las históricas.

Informes complementarios: [rúbrica](EVALUACION_RUBRICA_FINAL.md), [errores y pendientes](ERRORES_Y_PENDIENTES_FINAL.md), [checklist](CHECKLIST_CIERRE_DEFINITIVO.md).

## Anexo: motivo de cada prueba backend omitida

Las **90** siguientes son no ejecutadas actualmente. Se conservaron nodos individuales para no ocultarlas tras un porcentaje.

### 89 nodos: BD/API con fixtures mutables

Motivo común de cada nodo listado: el cierre de fixtures incluye client/database/db_case, que puede crear, truncar o modificar BD. Sin autorización para alterar BD, el plugin omite el caso **antes** de ejecutar esas fixtures. Sus resultados históricos no se convierten en aprobados actuales.

- `tests/test_api.py::test_health`
- `tests/test_api.py::test_list_vehicles_and_pending_orders`
- `tests/test_api.py::test_create_order_and_reject_invalid_payloads`
- `tests/test_api.py::test_optimize_routes_returns_geojson_and_then_404`
- `tests/test_auth.py::test_login_and_me`
- `tests/test_auth.py::test_third_failure_locks_the_account_for_fifteen_minutes`
- `tests/test_auth.py::test_auditor_cannot_optimize_and_operator_can`
- `tests/test_day.py::test_csv_accepts_known_places_and_leaves_the_pin_for_the_rest`
- `tests/test_day.py::test_admin_registers_a_vehicle_and_operator_can_inactivate_it`
- `tests/test_eta_us009.py::test_optimize_geojson_eta_fields`
- `tests/test_eta_us009.py::test_recalculate_etas_endpoint`
- `tests/test_fleet_us001.py::test_valid_registration_is_active`
- `tests/test_fleet_us001.py::test_duplicate_plate_is_rejected`
- `tests/test_fleet_us001.py::test_required_fields_and_invalid_numbers`
- `tests/test_fleet_us001.py::test_edit_keeps_id_and_inactivation_excludes_from_optimizer`
- `tests/test_fleet_us001.py::test_operator_cannot_create_but_can_update`
- `tests/test_geocode_us005.py::test_landmark_geocodes_and_persists_point`
- `tests/test_geocode_us005.py::test_unknown_address_persisted_pending_and_excluded_from_optimizer`
- `tests/test_geocode_us005.py::test_coordinates_outside_operating_area_become_pending`
- `tests/test_geocode_us005.py::test_manual_patch_geocodes_and_allows_routing`
- `tests/test_geocode_us005.py::test_create_order_rejects_invalid_and_out_of_area`
- `tests/test_geocode_us005.py::test_import_still_rejects_invalid_weight`
- `tests/test_hard_constraints_us008.py::test_seed_optimize_regression_sprint1`
- `tests/test_hard_constraints_us008.py::test_fleet_insufficient_409_without_persisting`
- `tests/test_hard_constraints_us008.py::test_import_optional_volume_persisted`
- `tests/test_import_us004.py::test_valid_csv_import_summary`
- `tests/test_import_us004.py::test_empty_file_is_rejected_atomically`
- `tests/test_import_us004.py::test_missing_header_columns_rejects_file`
- `tests/test_import_us004.py::test_row_missing_weight_is_rejected_partially`
- `tests/test_import_us004.py::test_invalid_weight_type_and_window`
- `tests/test_import_us004.py::test_duplicate_in_file_and_database`
- `tests/test_import_us004.py::test_max_150_rows_and_reject_151`
- `tests/test_import_us004.py::test_xlsx_import`
- `tests/test_import_us004.py::test_corrupt_xlsx`
- `tests/test_import_us004.py::test_auditor_denied`
- `tests/test_import_us004.py::test_jornada_link_persisted`
- `tests/test_import_us004.py::test_import_then_optimize_on_other_day`
- `tests/test_optimizer_us007.py::test_optimize_seed_metadata_rn008`
- `tests/test_optimizer_us007.py::test_jornada_filter_excludes_other_days`
- `tests/test_order_window_us006.py::test_valid_window_update_persists`
- `tests/test_order_window_us006.py::test_rejects_inverted_and_equal_windows`
- `tests/test_order_window_us006.py::test_auditor_cannot_edit_window`
- `tests/test_order_window_us006.py::test_missing_order_returns_404`
- `tests/test_order_window_us006.py::test_assigned_order_blocks_window_change`
- `tests/test_order_window_us006.py::test_delivered_order_blocks_window_change`
- `tests/test_order_window_us006.py::test_updated_window_used_by_optimizer`
- `tests/test_pdf.py::test_sustainability_pdf_endpoint`
- `tests/test_plate_restriction_us002.py::test_default_config_is_pending_and_inactive`
- `tests/test_plate_restriction_us002.py::test_cannot_activate_without_validation`
- `tests/test_plate_restriction_us002.py::test_operator_cannot_confirm_validation`
- `tests/test_plate_restriction_us002.py::test_auditor_can_read_but_not_update`
- `tests/test_plate_restriction_us002.py::test_optimizer_unchanged_without_active_validated_rule`
- `tests/test_plate_restriction_us002.py::test_validated_inactive_rule_does_not_filter`
- `tests/test_plate_restriction_us002.py::test_active_validated_rule_excludes_vehicle_and_explains`
- `tests/test_plate_restriction_us002.py::test_allowed_vehicle_still_routes`
- `tests/test_plate_restriction_us002.py::test_configuration_changes_are_audited`
- `tests/test_publication_b08_db.py::test_api_database_and_map_agree_after_valid_publication`
- `tests/test_publication_b08_db.py::test_api_rejection_rolls_back_and_does_not_create_map[weight-CAPACIDAD_PESO]`
- `tests/test_publication_b08_db.py::test_api_rejection_rolls_back_and_does_not_create_map[volume-CAPACIDAD_VOLUMEN]`
- `tests/test_publication_b08_db.py::test_api_rejection_rolls_back_and_does_not_create_map[window-VENTANA_ENTREGA]`
- `tests/test_publication_b08_db.py::test_api_rejection_rolls_back_and_does_not_create_map[shift-JORNADA_MAXIMA]`
- `tests/test_publication_b08_db.py::test_api_rejection_rolls_back_and_does_not_create_map[missing-PEDIDOS_SIN_ASIGNAR]`
- `tests/test_publication_b08_db.py::test_invalid_live_result_preserves_database_and_sends_no_success[weight]`
- `tests/test_publication_b08_db.py::test_invalid_live_result_preserves_database_and_sends_no_success[volume]`
- `tests/test_publication_b08_db.py::test_invalid_live_result_preserves_database_and_sends_no_success[window]`
- `tests/test_publication_b08_db.py::test_invalid_live_result_preserves_database_and_sends_no_success[shift]`
- `tests/test_publication_b08_db.py::test_invalid_live_result_preserves_database_and_sends_no_success[missing]`
- `tests/test_publication_b08_db.py::test_live_commit_failure_rolls_back_flushed_rows`
- `tests/test_publication_b08_db.py::test_rejected_cancellation_keeps_all_database_states`
- `tests/test_publication_b08_db.py::test_live_success_notifies_only_when_committed_plan_is_visible`
- `tests/test_realtime.py::test_driver_socket_rejects_a_fix_outside_the_valley`
- `tests/test_realtime.py::test_tracking_desk_receives_the_hello_and_a_bad_driver_id_is_refused`
- `tests/test_security_en003.py::test_anonymous_cannot_read_operational_endpoints`
- `tests/test_security_en003.py::test_auditor_reads_but_cannot_optimize`
- `tests/test_security_en003.py::test_invalid_and_expired_tokens_are_rejected`
- `tests/test_security_en003.py::test_inactive_user_cannot_use_the_api`
- `tests/test_security_en003.py::test_conductor_cannot_open_driver_channel_for_foreign_plate`
- `tests/test_security_en003.py::test_conductor_may_open_assigned_plate`
- `tests/test_security_en003.py::test_conductor_cannot_cancel_an_order_outside_his_route`
- `tests/test_security_en003.py::test_public_tracking_hides_personal_data`
- `tests/test_security_en003.py::test_api_sets_defensive_security_headers`
- `tests/test_security_en003.py::test_hsts_is_only_sent_for_https`
- `tests/test_security_en003.py::test_cors_preflight_restricts_methods_and_headers`
- `tests/test_vehicle_state_us003.py::test_active_to_maintenance_requires_motive_and_excludes_routing`
- `tests/test_vehicle_state_us003.py::test_maintenance_back_to_active`
- `tests/test_vehicle_state_us003.py::test_active_to_inactive_and_invalid_transition`
- `tests/test_vehicle_state_us003.py::test_auditor_cannot_change_state`
- `tests/test_vehicle_state_us003.py::test_legacy_activo_flag_maps_to_operational_state`
- `tests/test_vehicle_state_us003.py::test_historical_routes_remain_after_inactivation`

### 1 nodo: fixture temporal que requiere escritura

Motivo: tmp_path/tmp_path_factory/tmpdir (o dependencia equivalente) escribe artefactos temporales fuera del destino autorizado; omitido antes de la fixture.

- `tests/test_solver_sla_en001.py::test_en001_benchmark_report_json`
