# Matriz de adecuación a la consigna final

**Corte:** 17/11/2026, America/Lima. **Versión:** 1.0.0. **Referencia:** `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1`.

Fuente primaria local: `C:/Users/Baguette/Downloads/Consigna de evaluación final y cierre del proyecto.html`, secciones 1–5, incluida la rúbrica completa y las siete plantillas. Se usa como **criterio de evaluación futura**; sus mandatos de crear reportes, actualizar README o grabar video no prevalecen sobre la solicitud actual de diagnosticar sin implementar. No se crearon esos entregables finales ni sus carpetas.

Las fuentes D-* y verificaciones C-* se detallan con rutas y límites en [EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md](EVIDENCIAS_DISPONIBLES_Y_FALTANTES.md). Acciones B-*/G-* en [PLAN_SPRINT_4.md](PLAN_SPRINT_4.md); pruebas V-* en [PLAN_VALIDACION_SISTEMA.md](PLAN_VALIDACION_SISTEMA.md).

Estados: **base parcial** = hay insumos, falta completar/actualizar; **ausente** = no localizado en el ámbito inspeccionado; **no acreditado** = no basta lo disponible para afirmar cumplimiento. No se asigna una nota de rúbrica como si se hubiera sustentado el proyecto.

## 1. Reglas globales de entrega futura

| Exigencia de la consigna | Evidencia actual | Brecha y acción futura | Criterio verificable |
|---|---|---|---|
| Siete reportes Markdown con estructura de sección 5 y datos reales | D-18 completo; fuentes históricas D-01…17 | Siete definitivos ausentes; preparar G-04 tras completar datos, sin extrapolar resultados | Siete nombres exactos en `docs/04 Cierre`, campos pertinentes completos, sin marcadores, cálculos/evidencias sustentados. |
| Todos los marcadores sustituidos | Las plantillas HTML contienen marcadores por diseño | En la entrega final no basta reemplazarlos por cifras inventadas, «cumplido» o texto genérico | Dato real/cita/interpretación; si una falta no puede resolverse, comunicarla al evaluador como limitación y no afirmar cumplimiento del criterio. |
| Desempeño frente a baseline y cierre híbrido | Acta, requisitos, backlog, riesgos, informes de sprint | Falta baseline aprobada y conciliación predictivo/adaptativo y costos reales | Cada variación indica baseline, real, causa, impacto y respuesta; cambios con aprobación/versiones. |
| Coherencia de versiones previas | Versiones históricas y commits disponibles | Resolver D-08/D-12, declaraciones Sprint 3, fechas de capturas y documentos eliminados | Mantener historial; versión nueva según impacto (p. ej. V_1_1_0/V_2_0_0), título/metadatos/nombre/enlaces coherentes. No uniformar arbitrariamente historia. |
| Trazabilidad bidireccional | README enlaza documentación existente sin destinos de archivo rotos en C-06 | No tiene siete enlaces de cierre; varios docs históricos sí tienen vínculos rotos | README enlaza individualmente cada definitivo; cada uno retorna a `../../README.md`; imágenes/capturas también accesibles; V-20. |

## 2. Documento 01 — Reporte de Estado

**Nombre futuro exacto:** `docs/04 Cierre/01 Reporte de Estado V_1_0_0.md`. **Estado:** ausente; insumos parciales. Plantilla 5.1, enfoque ejecutivo, una página recomendada, comparación con periodo anterior.

| Apartado obligatorio | Qué existe / dónde | Actualizar y calcular | Gráfico/evidencia faltante o bloqueo | Rúbrica / acción |
|---|---|---|---|---|
| Proyecto, corte y versión | Nombre/PM en D-02, README D-15 | Conciliar EcoLogística Junín/Huancayo y fijar corte real | Fecha de esta auditoría no es fecha de cierre | R1/R3; B-01, G-01 |
| Alcance: logros, cambios, defectos | Matrices Sprint 1/2 D-09/10 y revisión Sprint 3 D-11; hallazgos D-01/16 | Separar implementado de aceptado, resolver contradicciones, identificar cambios aprobados y defectos vigentes | Acta de aceptación y resultados B-30; no convertir estimaciones de auditoría en logros aceptados | R1; B-30, G-04 |
| Cronograma: hitos no completados, causa, ruta crítica, acciones | Hitos por semanas D-02; impedimentos D-09/10 | Planeado vs real por hito y periodo; analizar dependencias y efecto en próximo hito/ruta crítica | Cronograma detallado aprobado, fechas reales y causas verificadas; no calcular días desde semanas abstractas | R1; G-01 |
| Costos: fondos del periodo, causas, presupuesto/reserva y acciones | Modelo D-07 y contexto D-02 | AC del periodo, variación horas/recursos, efecto sobre BAC/reserva | Registro de horas/costos, presupuesto aprobado y consumos de reserva faltantes; bloqueado económicamente | R1; G-02 |
| Look Ahead: entregables y costos pendientes | Backlog B-* y plan Sprint 4 | Selección con capacidad real, costo restante previsto y responsable | No hay capacidad/estimación de sprint ni costo pendiente aprobado | R1; G-02, B-01 |
| Riesgos, incidentes y comentarios | RIE-001…010 D-08; IMP D-09/10; hallazgos D-01 | Reevaluar vigencia, diferenciar riesgo de incidente materializado y propuesta de respuesta aplicada | Responsables/decisiones y evidencia de respuesta actual | R1; G-04 |

La plantilla 5.1 no obliga un gráfico específico: priorizar lectura ejecutiva; semáforo opcional con umbral explícito. Su falta principal es de datos comparables y aceptación, no de decoración.

## 3. Documento 02 — Reporte de Variación

**Nombre:** `docs/04 Cierre/02 Reporte de Variación V_1_0_0.md`. **Estado:** ausente; base narrativa parcial. Plantilla 5.2: tres dimensiones, cada una con planificado, real, variación, causa raíz y respuesta planificada.

| Dimensión | Fuentes disponibles | Actualizar / cálculos | Evidencia/gráfico faltante y apartados bloqueados | Rúbrica / acción |
|---|---|---|---|---|
| Cabecera proyecto/periodo/corte/versión | D-02/09/10 | Definir mismo periodo/corte del estado y EVM | Falta periodo comparativo validado | R1; G-01/02 |
| Cronograma | Hitos del acta, roadmap como imagen, SP comprometidos y pendientes | Fechas reales−planificadas en días con calendario explícito; trabajo aceptado vs comprometido en misma unidad; dependencia y causa verificable | Baseline detallada y fechas reales; captura 2024 no equivale a fechas 2026. No afirmar ruta crítica sin red de dependencias | R1; G-01, B-30 |
| Costo | Estimación D-07 | Diferencia real−plan por rubro, horas reales−plan, porcentaje con denominador no cero; explicar signo distinto de CV EVM=EV−AC | No AC ni plan temporal aprobado. No comparar total presupuestado con costos de combustible del producto | R1; G-02 |
| Calidad | DoD D-05, informes Sonar/OWASP/WCAG D-12, artefactos C-09, defectos D-01 | Por métrica comparar criterio→resultado del mismo alcance/commit; diferencias en puntos porcentuales, defectos por severidad y respuesta | Corrida candidata, cobertura comparable, análisis revisado y aceptación; contradicción 136/143, 67/68 debe contextualizarse | R1; B-29/30 |

Las tablas completas son obligatorias; gráficos de variación son apoyo si hay serie real. Una falla de setup no demuestra un defecto funcional; un gate de código nuevo aprobado tampoco cierra incidencias históricas. Causa raíz debe vincular evidencia a una acción verificable y responsable, sin atribuir causas no investigadas.

## 4. Documento 03 — Análisis de Valor Ganado

**Nombre:** `docs/04 Cierre/03 Reporte de Análisis de Valor Ganado - EVM V_1_0_0.md`. **Estado:** ausente; **bloqueado por datos económicos primarios**. Plantilla 5.3.

| Campo de plantilla | Disponible | Necesario / cálculo | Evidencia/visual pendiente | Rúbrica / acción |
|---|---|---|---|---|
| BAC y estado general | D-07: USD134.400 estimados; D-02: referencia pendiente | Confirmar aprobación, moneda, alcance y tratamiento de reservas antes de fijar BAC | Aprobación y reconciliación, no simple commit de presupuesto | R1; G-02 |
| PV, EV, AC: periodo, acumulado actual y anterior | Estimación RR.HH./licencias/cloud; 3.000 h planificadas | PV por paquetes/periodos de baseline; EV de trabajo aceptado al valor presupuestado; AC incurrido con soportes | Libro de costos/horas, aceptación por paquete y baseline temporal; ninguno suficiente actualmente | R1; G-02 |
| SV, CV, SPI, CPI en tres columnas | Fórmulas en consigna | SV=EV−PV; CV=EV−AC; SPI=EV/PV; CPI=EV/AC; cada columna con magnitudes comparables | Revisión independiente de cálculos; denominadores cero=no definido | R1; V-20 |
| % planificado, ganado y gastado | BAC estimado sin aprobar | 100×PV/BAC, 100×EV/BAC, 100×AC/BAC acumulados | No usar porcentajes de auditoría ni de cobertura como avance económico | R1; G-02 |
| Desviaciones: causas e impacto costo/plazo | Impedimentos/hallazgos documentados | Relacionar causas reales con SV/CV/índices, fechas y respuesta | Falta evidencia económica y causal; no atribuir CV a una falla técnica sin registro | R1; G-04 |
| Tres EAC y selección justificada | Fórmulas completas de HTML | EAC₁=BAC/CPI; EAC₂=BAC/(CPI×SPI); EAC₃=AC+[(BAC−EV)/(CPI×SPI)] | Inputs faltantes; documentar hipótesis de cada una y por qué una describe el trabajo restante | R1; G-02/04 |

No se puede calcular un EVM numérico defendible al corte. Tampoco corresponde declarar EV=0, AC=0, BAC=S/500.000 o distribuir USD134.400 linealmente por semanas. La falta de dato no es cero. Para tendencias del tablero 04 se requiere además serie temporal comparable; un punto aislado no acredita tendencia. El inventario compañero §4 especifica campos y dónde registrarlos.

## 5. Documento 04 — Tableros de Control Híbridos

**Nombre:** `docs/04 Cierre/04 Tableros de Control - Híbridos V_1_0_0.md`. **Estado:** ausente; base parcial. Plantilla 5.4.

| Apartado / gráfico | Disponible y fuente | Actualizar / cálculos | Falta para completarlo | Rúbrica / acción |
|---|---|---|---|---|
| Proyecto, frecuencia y justificación less is more | Interesados D-03; requisitos/DoD D-04/05 | Elegir pocos KPI que respondan a decisiones de PM, QA y equipo; frecuencia/responsable | Confirmar necesidades reales, umbrales y fuente por métrica. Dashboard logístico del producto no reemplaza tablero de gestión del proyecto | R2; G-03/04 |
| RAG por componente, enfoque y observación/umbral | Hallazgos y estados de auditoría | Estado según regla acordada, fecha, dueño y efecto; separar predictivo/adaptativo | Semáforo real actualizado con umbrales; no colores arbitrarios ni «verde» por archivo existente | R2; B-30, G-04 |
| 3.1 Líneas de tendencias variación/EVM + interpretación | Modelo económico y narrativas | Serie PV/EV/AC y/o SV/CV por corte comparable | G-02: al menos cortes fechados suficientes para tendencia, sin datos imputados | R2; G-02 |
| 3.2 Áreas apiladas / flujo acumulado + interpretación | Imagen estática del tablero D-06 | Conteos por estado a través del tiempo, WIP/cuello de botella | Historial de transiciones o snapshots diarios reales; una captura no produce CFD | R2; G-03 |
| 3.3 Burbujas SPI vs CPI con tamaño CSI + interpretación | Fórmula EVM, sin serie | SPI/CPI por periodo/componente comparable; definir CSI y escala explícitas, sin inferir fórmula omitida por la pauta | Datos y definición validada; si se adopta CPI×SPI debe declararse la convención. No inventar burbujas | R2; G-02/04 |
| 3.4 Gauges / barras + interpretación | Criterios DoD y RF, resultados limitados C-03/04 | Barras/gauges sobre medidas actuales con denominador/unidad/objetivo | Datos finales por alcance; no mostrar 12,98 % parcial como cobertura frontend global | R2; B-29/30 |

La sección descriptiva de la consigna ofrece tipos de gráficos «tales como»; la plantilla 5.4 enumera los cuatro apartados 3.1–3.4 y la rúbrica pide gráficos solicitados. Planificar los cuatro con sus interpretaciones evita omitir un apartado. Admitidos imágenes embebidas o diagramas estructurados legibles; siempre necesitan datos originales identificables.

## 6. Documento 05 — Radiadores de Información

**Nombre:** `docs/04 Cierre/05 Radiadores de Información V_1_0_0.md`. **Estado:** ausente; solo imágenes históricas parciales. Plantilla 5.5, exige capturas reales y análisis.

| Radiador/campo | Qué existe | Qué actualizar o calcular | Faltante / apartado no completable | Rúbrica / acción |
|---|---|---|---|---|
| Proyecto, marco ágil, versión | Scrum/híbrido D-03/05/06 | Confirmar marco, periodo y fuente real | Fuente Jira actual sin validar | R2; G-01/03 |
| Burndown: trabajo restante/ideal, velocidad y tasa | SP comprometidos D-09/10; sin serie restante diaria | Saldo restante diario y línea ideal desde compromiso real; completado aceptado por duración | Historia de cambios/transiciones y unidad/DoD; no reconstruir gráfica lineal a partir de estimación de implementación | R2; G-03 |
| Burnup: completado/cambios de alcance | Backlog como catálogo | Serie de alcance total y trabajo aceptado, entradas/salidas aprobadas | Serie/fechas/aprobaciones; no sumar commits o SP ambiguos de capturas | R2; G-03 |
| Task Board/Kanban: flujo y cuellos | `04-tablero-scrum.png` D-06 | Captura actual con corte, filtros, estados, WIP y análisis; relacionar tiempos de permanencia si existen | Vigencia y origen de imagen; exportación actual, aceptación de Done y trazabilidad de tarjetas | R2; G-03 |
| Mood Chart: integrante/rol, Sprint 1/2/3/final e interpretación | Retrospectivas textuales, sin mediciones de ánimo | Recoger respuestas reales por escala y fecha; respetar ausencia histórica | No se puede inferir ánimo por tests/commits/retro optimista. Historia faltante debe declararse; encuestar ahora no mide retroactivamente sprints previos | R2; G-03/06 |
| Tablero retro: imagen, qué funcionó, oportunidades y acciones implementadas | Retros D-09/10/11 | Reunión/participación reales, captura original, acción con responsable/seguimiento | Sprint 2 es borrador y Sprint 1 contiene propuestas; no afirmar acciones implementadas sin prueba | R2; G-03/06 |

Las cinco imágenes Jira existentes no incluyen burndown, burnup, Mood ni tablero de retrospectiva. Son base documental con incoherencias 2024/2026 y SP que deben resolverse. No se crean radiadores falsamente históricos para llenar plantillas.

## 7. Documento 06 — Reporte Final del Proyecto

**Nombre:** `docs/04 Cierre/06 Reporte Final del Proyecto V_1_0_0.md`. **Estado:** ausente, cierre no acreditado. Plantilla 5.6.

| Apartado | Disponible / fuente | Actualizar / cálculos | Pendiente o bloqueo | Rúbrica / acción |
|---|---|---|---|---|
| Proyecto, fecha cierre, descripción general | Charter D-02, visión D-03 y README | Alinear objetivo/beneficiario/ámbito Huancayo-El Tambo-Chilca con producto final | No hay fecha ni aprobación real de cierre; no usar 17/11 como cierre por defecto | R2; G-01/06 |
| 2.1 Alcance predictivo/adaptativo: éxito, evidencia, variaciones/causa/impacto | Requisitos/backlog/auditoría | RF completos aceptados, entregables aprobados y cambios; explicar baseline frente a evolución de sprints | B-30 y decisión de alcance/exenciones; 5/7 completos solo si se acredita cada uno | R2; B-30, G-04 |
| 2.2 Calidad: criterios, verificación/validación y exenciones | DoD y evaluaciones D-05/12, C-03/04/09 | Comparación contra criterios por commit y flujo; estado de defectos | Corrida final, aceptación, excepciones aprobadas, cobertura comparable, seguridad/accesibilidad pendientes | R2; B-29/30 |
| 2.3 Cronograma: hito, enfoque, fecha plan/real, variación/impacto | Hitos semanales D-02 y reportes de sprint | Días de desviación y efecto sobre dependencias; identificar trabajos predictivos y adaptativos | Baseline temporal detallada/aprobada y fechas reales; evidencia Jira 2024 no sustituye | R2; G-01 |
| 2.4 Costo: aprobado/tolerancia, final real, variaciones/impacto | Modelo D-07 | BAC y tolerancia acordados vs costo final conciliado; reservas/obligaciones pendientes | BAC, AC final y autorización faltantes; no declarar éxito económico | R2; G-02/06 |
| Riesgos, incidentes, impedimentos: ID/tipo/impacto real/respuesta aplicada | RIE e IMP D-08/09/10 | Actualizar estado, consecuencias y eficacia de respuesta; separar mitigación propuesta/aplicada | Seguimiento con soportes y responsables de riesgos residuales | R2; G-04/06 |
| Éxito/cierre: satisfacción interesados, equipo/reconocimiento, transición y administración | Lista de interesados/equipo | Medir satisfacción con escala, muestra, fecha y resultados; aceptación, transferencia, soporte y pendientes | Encuesta, reunión de cierre y runbook/transferencia no localizados | R2; B-31, G-06 |

No existe gráfico obligatorio específico para el 06 en su plantilla; sus tablas y evidencias deben permitir juzgar éxito. Puede reutilizar gráficos de 03/04/05 con misma fuente/corte sin duplicar valores ni interpretar simulaciones como operación real.

## 8. Documento 07 — Lecciones Aprendidas

**Nombre:** `docs/04 Cierre/07 Reporte Final de Lecciones Aprendidas V_1_0_0.md`. **Estado:** ausente; base cualitativa parcial. Plantilla 5.7: por categoría, prácticas efectivas, oportunidades y recomendación futura; además conclusiones de retrospectiva de cierre.

| Categoría exigida | Insumo disponible | Falta/actualización para lección sustentada |
|---|---|---|
| Desempeño del equipo | Retros Sprint 1/2: roles QA/DevOps y necesidad de revisión; Sprint 3: relato de integración | Validar por equipo qué ocurrió, efecto y recomendación concreta; no asumir satisfacción o ceremonia. |
| Evolución/control del alcance predictivo/adaptativo | Dos catálogos RF y discrepancias de Done; backlog técnico | Registrar decisiones aprobadas y efecto; aprender de trazabilidad y control de cambios sin ocultar deuda. |
| Integración del cronograma híbrido | Hitos 14 semanas y problemas de entorno | Fechas/dependencias reales y lección sobre programación; no atribuir retrasos específicos sin registro. |
| Presupuesto/costos | Modelo detallado y ausencia de registros reales | Documentar limitación, práctica futura de BAC aprobado/horas/devengos; sin inventar sobrecostos o ahorros. |
| Técnicas de estimación | SP comprometidos 20/34 y capturas divergentes | Conciliar fuente y velocidad real; comparar estimación vs resultado aceptado, sin equivalencia automática SP=horas. |
| Aseguramiento de calidad | DoD vs gates parciales, cobertura de distinto alcance, defectos y tests | Evidencia de acción aplicada y eficacia; distinguir setup, unitario, integración, aceptación y análisis. |
| Involucramiento de interesados | Matriz de interesados, actas de aceptación ausentes | Recoger participación/satisfacción real y decisiones; no presentar perfiles ficticios como entrevistados reales. |
| Riesgos, incidentes e impedimentos | RIE/IMP e inventario de deuda | Eficacia de prevención/contingencia, responsables/fecha de acciones; contraste de estado declarado y evidencia. |

Para cada fila: hecho con fuente → impacto observado → aprendizaje → recomendación accionable y forma de verificarla. Completar versión, proyecto y **fecha real de reunión de cierre**, participantes y conclusiones validadas. No basta copiar retrospectivas genéricas ni propuestas como si estuvieran implementadas. Rúbrica R2; G-03/06/04.

## 9. Requisitos técnicos y de repositorio

| Requisito | Verificación y estado | Brecha / acción posterior | Aceptación |
|---|---|---|---|
| Frontend/backend separados | `src/` y `app/` claros; infraestructura en `frontend/`/`backend/` (D-15/16) | Mantener modularidad; actualizar arquitectura efectiva, sin mover carpetas por estética | V-01: responsabilidades y conexión documentadas; R4 |
| .gitignore funcional | C-07: dependencias, entornos, builds y caches correctamente excluidos | Revisar patrones de claves/backups C-08 y paquete final sin residuos | V-01/20: no rastreados/empacados secretos, dependencias o temporales; R4 |
| Credenciales | Solo `.env.example` entre `.env*` locales; valores demo en configuración; patrones limitados sin coincidencias | Separar secretos de demo/productivo, revisar historial si se requiere garantía histórica; sin exponer valores en evidencia | V-02/17; configuración candidata sin cuentas/claves demo fuera de demo; R4 |
| README y guía | Índice existente y links a docs actuales; badge estático | Faltan arranque/despliegue/recuperación y cierre; contradicción con acta Sprint 3 | B-31/G-05; prueba por tercero, enlaces finales; R3/R4 |
| Git/historial | Limpio inicialmente; commits disponibles; sin tags locales | Relacionar candidato, reportes, build y release; aclarar bajas documentales del HEAD | No inventar PR/CI ni release; evidencia por commit, versiones coherentes; R3 |
| Enlaces documentales | README 0 destinos rotos en sondeo; docs 31 ocurrencias ausentes, 6 destinos | Corregir o reemplazar con fuente válida/versionada en etapa autorizada; añadir 7 ida/vuelta | V-20; R3 |
| Pruebas | Tipado y SW pasaron; dist pasó; artefactos de cobertura/benchmark limitados | Corrida integrada y datos aceptados faltan; CI no impone todo el umbral, staging placeholder | V-18/19, B-29/30; R4 |
| Sistema demostrable | Contratos REST/WS y consumidores conectados por código | No comprobación viva ni evidencia completa de API↔BD↔UI; defectos de integridad/seguridad | Ensayo real satisfactorio V-19/21; R4 |

## 10. Sustentación y video

| Entregable | Exigencia exacta/relevante | Actualidad | Condición futura y evidencia |
|---|---|---|---|
| Sustentación de gestión | 10 min dentro de 20 totales | Insumos de gestión parciales | Explicar problema/alcance híbrido, baseline vs real, EVM, riesgos/correcciones, aceptación y lecciones. Cronometrar, sin inventar índices para ocupar diapositivas. |
| Demostración técnica | 10 min, 50 % del total, integración real y criterios aceptados | Código de flota/pedidos/GA/mapa/conductor/PDF candidato; ninguno integral aceptado en esta fase | Guion V-21: flota→pedidos→ruta→mapa→entrega→KPI/PDF. Mostrar recarga/persistencia y API; dinámica solo si pasa sus pruebas, con estado declarado. |
| MP4 | `docs/05 Video proyecto`, ~5 min, segmentos continuos ~1 pitch+~4 demo | Archivo/guion final no localizado | Pitch problema/solución/valor/público; demo funcional real. R5 suficiente: ±30 s, audio/imagen comprensibles; sobresaliente: ±15 s, HD/transiciones claras/casos completos. |
| Honestidad del entorno | Local o desplegado permitido para video | Compose demo/HTTP y OSRM público opcional por configuración | Presentar entorno real y límites; no decir producción segura, tráfico vivo ni redistribución completa sin evidencia. Para DoD de staging sí hay requisitos adicionales. |

El mapa puede mostrar ruta vial al contar con OSRM real; la tabla es contingencia declarada. El dashboard logístico no reemplaza EVM de gestión. La demo no debe certificar 99,5 % de disponibilidad ni ahorros mensuales con una ejecución de minutos.

## 11. Rúbrica: cobertura y criterio de éxito

| Código / criterio | Peso / máximo | Para suficiencia según consigna | Para sobresaliente / brecha al corte |
|---|---:|---|---|
| R1 · Narrativos y EVM (01–03) | 1 / 3 pts | Estructuras completas, sin marcadores, cálculos básicos/variaciones correctos y explicación causal | Tres EAC exactos y justificados, comparación histórica y acciones conectadas a causas. Faltan definitivos y datos EVM. |
| R2 · Visuales y cierre (04–07) | 1 / 3 pts | Gráficos/capturas solicitados, categorías completas, sin errores graves/marcadores | Gráficos legibles less is more, RAG/tendencias/burbujas CSI/radiadores reales, diferenciación híbrida, satisfacción y lecciones accionables. Faltan series, capturas actuales y cierre real. |
| R3 · Trazabilidad/versionamiento | 1 / 3 pts | Siete archivos con nombres exactos en `docs/04 Cierre`, links bidireccionales correctos, previos afectados actualizados/versionados | 100 % enlaces correctos e índice enriquecido, control histórico coherente. No hay paquete final y existen vínculos históricos rotos. |
| R4 · Demo funcional/arquitectura | 4 / 12 pts | ~10 min, funciones principales e integración frontend/backend operativas, carpetas separadas e ignore sin errores críticos | Demo fluida en 10 min, flujos E2E sin fallos, arquitectura modular/desacoplada, sin dependencias/credenciales/residuos en entrega y guía de despliegue. Separación/ignore tienen evidencia parcial; integración viva y aceptación no acreditadas. |
| R5 · MP4 | 4 / 12 pts | ~5 min ±30 s, ruta exacta, ambos segmentos, audio/imagen comprensibles | 5 min ±15 s, HD, pitch persuasivo y demo con casos completos/transiciones claras. MP4 ausente en inspección. |

Suma de pesos = **11**; cada criterio vale 0/1/2/3 según nivel; máximo ponderado = **33 puntos**. R4+R5 concentran 24/33 puntos posibles, sin eximir los siete reportes ni justificar datos falsos. La consigna penaliza ausencia de reportes/cálculos, gráficos/radiadores omitidos, ubicaciones/enlaces incorrectos, fallos críticos y video ausente/corrupto. No se adjudica puntaje real antes de entregar y sustentar.

## 12. Puertas para redactar los definitivos

1. Baseline de alcance/cronograma/costo y originales/procedencia conciliados (G-01/02). Si no existe dato histórico recuperable, declarar la limitación; gestionar con el evaluador cómo tratarla sin fabricarla.
2. Candidato validado y aceptado por requisito, con resultados trazables (B-29/30). No usar porcentajes de implementación como EV, capturas 2024 como ejecución 2026 ni cobertura parcial como global.
3. Series/visuales y retro reales (G-03), costos/aceptación conciliados y reunión/satisfacción/cierre/transferencia reales (G-06).
4. Redacción G-04 según plantillas, revisión matemática independiente y enlaces/nombres/versiones G-05; después ensayo y MP4 B-32. Nada de esta secuencia autoriza código, migraciones o entrega final en la fase actual.
