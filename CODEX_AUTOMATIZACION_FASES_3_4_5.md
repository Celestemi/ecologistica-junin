# Instrucción maestra para Codex — Fases 3, 4 y 5 de EcoLogística Junín

> **Uso:** Guarda este archivo en la raíz del repositorio `C:\Users\Baguette\Documents\Proyectos2\ecologistica-junin` y abre esa carpeta en Codex. Envíale una sola instrucción: **«Lee `CODEX_AUTOMATIZACION_FASES_3_4_5.md` completo y ejecuta sus fases 3, 4 y 5 en ese orden, respetando los puntos de control y las restricciones. No ejecutes la fase siguiente si no se cumple su puerta de entrada.»**
>
> Este documento automatiza **la secuencia de trabajo**, no garantiza que las pruebas, grabación de pantalla o fuentes externas estén disponibles. No inventes resultados ni entregables.

## 0. Reglas globales — aplican a todas las fases

### Contexto y fuentes

- **Proyecto:** EcoLogística Junín.
- **Raíz:** `C:\Users\Baguette\Documents\Proyectos2\ecologistica-junin`.
- Examina la consigna original, la **«Consigna de evaluación final y cierre del proyecto»** (HTML, con su sección 5 de plantillas y rúbrica), `README.md`, los documentos de `AUDITORIA/`, los registros de los sprints anteriores, los planes, presupuestos, riesgos, pruebas y el historial Git.
- Los diagnósticos anteriores son evidencia de una **fecha de corte**, no sustituyen verificación actual. La auditoría previa indicaba Sprint 3 en consolidación, 53,5 % de implementación estimada y 67,1 % de avance parcial del MVP: **no conviertas esas cifras en resultados de pruebas actuales ni en valor ganado EVM**.
- Busca las consignas en el repositorio. Si faltan, **no completes de memoria** los apartados exactos de las plantillas; informa el bloqueo y limita el trabajo a lo que esté sustentado.

### Ejecución autónoma con límites

1. Trabaja en este orden: **Fase 3 (validación) → control de entrada → Fase 4 (documentos) → control de entrada → Fase 5 (entrega y sustentación)**.
2. No requieras un nuevo prompt del usuario entre fases **cuando existan las fuentes, permisos y evidencias necesarios**. Antes de cada fase registra el cumplimiento de su puerta de entrada.
3. Si hay un riesgo de modificar datos de producción, migraciones, credenciales, historial Git o archivos fuera del alcance, **detén esa acción**. No simules éxito. Continúa con tareas independientes seguras y documenta las bloqueadas.
4. Puedes ejecutar verificaciones en un **entorno de pruebas aislado**, solo tras comprobar que las variables de entorno, base de datos, rutas de escritura y dependencias no afectan datos reales. No ejecutes comandos destructivos sobre bases existentes. No instales dependencias sin autorización.
5. No corrijas el código durante estas fases: registra defectos para un futuro ciclo de implementación. No commits, pushes, reseteos, rebases, limpiezas de Git ni borrados automáticos.
6. Conserva los archivos de usuario existentes; antes de escribir verifica si el archivo ya existe. Si está presente, realiza una actualización acotada solo cuando esté expresamente autorizada aquí, preservando cambios y versión; de lo contrario, crea una nueva versión o reporta conflicto.
7. Toda afirmación relevante debe indicar **fuente, fecha, ruta y, cuando sea posible, commit, prueba o evidencia concreta**. Separa «verificado ahora», «histórico», «estimado» y «no disponible».
8. No inventes valores de costo, fechas, entrevistas, métricas, estados de Jira, capturas, aprobaciones, satisfacción, pruebas exitosas o un video producido.
9. Las rutas Windows son ubicaciones en el equipo del usuario; trabaja en la raíz del repositorio accesible para Codex, no asumas que están montadas si el entorno es remoto.
10. Al finalizar cada fase, agrega al resumen general qué se realizó, qué se omitió, fallos y próximos pasos. Evita crear archivos adicionales fuera de las ubicaciones autorizadas.

### Zonas de escritura autorizadas

| Trabajo | Ubicación autorizada |
|---|---|
| Informes de validación, guiones, checklists y control | `AUDITORIA/` |
| Siete entregables oficiales de cierre | `docs/04 Cierre/` |
| Índice documental y enlaces | `README.md` (solo Fase 4, cambios mínimos) |
| Video final, si realmente se puede producir y verificar | `docs/05 Video proyecto/` |

**Fuera de estas ubicaciones:** no crees ni modifiques archivos de código, datos, pruebas, configuración, documentación previa o artefactos. Si una prueba necesita cachés/salidas fuera de estas ubicaciones, configura una ruta aislada y permitida dentro de `AUDITORIA/` o no la ejecutes y documenta la limitación. No elimines archivos preexistentes.

---

# FASE 3 — PRUEBAS, VALIDACIÓN Y EVIDENCIAS DEL MVP

## Objetivo

Determinar qué funcionalidades del proyecto funcionan realmente y qué evidencia puede usarse en el cierre. **No cambies código ni datos de producción.** No confundir un archivo de test existente con un test aprobado.

## 3.1 Preparación y verificación del entorno

1. Registra rama, commit, estado `git status` y modificaciones preexistentes sin alterarlas.
2. Identifica comandos de test de frontend/backend, suites de integración, CI, versión de runtimes, Docker y servicio de base de datos; distingue el entorno de pruebas del operativo.
3. Inspecciona las fixtures y scripts: pueden crear, truncar o mutar tablas. No ejecutes nada hasta verificar aislamiento seguro.
4. Define un conjunto de datos reproducible y documenta si es sintético, anonimizado o histórico. Nunca introduzcas datos sensibles en los informes.
5. Documenta comandos usados, fechas, sistema y errores. Si no hay entorno seguro, realiza análisis estático y marca los resultados de ejecución como **No ejecutado**.

## 3.2 Backend — matriz de pruebas

Revisa y, cuando sea seguro, ejecuta casos asociados con:

- Autenticación, permisos y límites por rol.
- Alta, consulta, edición, estados y reglas de vehículos.
- Pedidos, importación CSV/XLSX, ventanas, coordenadas y validaciones.
- Motor genético: generación, restricciones, factibilidad, reproducibilidad y publicación.
- Persistencia, versiones, ETA, recálculos y consistencia de totales.
- Reoptimización en incidentes, cancelaciones, cambios de pedido y averías (solo lo implementado).
- Mapas, geometrías y manejo de fallos OSRM.
- Indicadores, unidades, ahorro y datos reportados.
- Reportes PDF, fechas, factores ambientales y periodos.
- API de conductor, entregas, operaciones offline, sesiones y WebSockets.

Registra por caso: **ID, RF/RNF, precondición, comando/pasos, resultado esperado, resultado observado, estado (Aprobado/Fallido/Parcial/No ejecutado), evidencia, defecto asociado y fecha**.

## 3.3 Frontend e integración

- Verifica, donde sea posible, login, navegación por roles, formularios, vehículos, pedidos, optimización, mapa, dashboard, PDF y vista del conductor.
- Ejecuta las suites existentes solo si sus efectos están confinados.
- Distingue test unitario, test de componente, prueba integrada y verificación manual visual.
- Para el flujo completo, traza: **Pedido → Validación → Optimización → Persistencia → Mapa → Conductor → Entrega → Indicadores → PDF**.
- No declares E2E aprobado sin observar el flujo en un entorno operativo controlado.

## 3.4 Rendimiento y requisitos de aceptación

- Caso solicitado: hasta **150 pedidos y 15 vehículos**, solución **válida** en máximo **45 segundos**, y reoptimización menor de **30 segundos**.
- Si ejecutas benchmark, registra hardware, versión, datos, semillas, matriz, proveedor vial, tiempos **extremo a extremo**, cantidad de pedidos asignados y factibilidad real.
- Una respuesta rápida con pedidos sin asignar, exceso de capacidad o violación de ventanas no satisface la prueba.
- Si no puedes ejecutarlo de forma fiable, registra **No verificado**; no extrapoles métricas históricas.
- Revisa controles OWASP, accesibilidad WCAG 2.1, seguridad de datos y calidad; no afirmes certificaciones sin respaldo.

## 3.5 Entregables de Fase 3 — crear en `AUDITORIA/`

1. `SPRINT4_RESULTADOS_PRUEBAS.md`: entorno, comandos, resultados, cobertura obtenida y limitaciones.
2. `SPRINT4_MATRIZ_ACEPTACION.md`: RF-01 a RF-10 y RNF-01 a RNF-07, criterios, evidencias y estados.
3. `SPRINT4_DEFECTOS_PENDIENTES.md`: prioridad, impacto, reproducción, ubicación y propuesta de corrección; sin modificar código.
4. `SPRINT4_EVIDENCIAS_TECNICAS.md`: índice de fuentes y rutas/commits, sin copiar secretos.

Si existe alguno de estos archivos, no sobrescribas evidencia anterior: utiliza una variante versionada y registra qué versión está vigente.

## Puerta 3 → 4

- Deben existir los cuatro informes y distinguir claramente pruebas ejecutadas de no ejecutadas.
- Los resultados no tienen que ser todos aprobados para **redactar informes de estado y variación**, pero un defecto crítico abierto impide **declarar cierre técnico aprobado** o presentar un reporte final como aceptación formal.
- Si faltan datos para documentos de cierre, continúa con contenido verificable y reporta apartados no completables sin inventar datos.

---

# FASE 4 — SIETE DOCUMENTOS DE GESTIÓN Y CIERRE

## Objetivo

Crear los **siete Markdown oficiales** conforme a las **plantillas exactas de la sección 5 del HTML de la consigna final**. Preservar títulos, orden, tablas, campos, criterios y fórmulas. Usar evidencia del repositorio, documentos de gestión y Fase 3.

## 4.1 Preparación de fuentes y control de consistencia

1. Identifica la ubicación exacta del HTML de la consigna y extrae las siete plantillas.
2. Analiza Project Charter/acta, plan de gestión, presupuesto, cronograma, matriz de riesgos, sprints anteriores, retros, tableros, evidencias Jira disponibles, README, auditoría y pruebas.
3. Construye una trazabilidad interna de cada dato: **dato → fuente → fecha/periodo → estado de verificación**.
4. Contrasta documentos históricos que se contradigan; registra conflictos y evita seleccionar automáticamente cifras optimistas.
5. Revisa el alcance geográfico: el repositorio se denomina `ecologistica-junin` mientras la consigna original es «EcoLogística Lima». Utiliza la adaptación **solo si existe decisión documentada**, sin presentar la ubicación nueva como requisito original de la consigna.
6. Conserva historia y nomenclatura de versiones `V_1_0_0`, `V_1_1_0`, etc.; no alteres las fechas de los documentos anteriores.

## 4.2 EVM — no inventar

Obtén **BAC, PV, EV y AC** de líneas base y registros reales, para periodo actual, acumulado actual y periodo anterior.

Calcula cuando los datos lo permitan:

- `SV = EV - PV`, `CV = EV - AC`, `SPI = EV / PV`, `CPI = EV / AC`.
- Avance planificado, ganado y gastado respecto de BAC.
- `EAC_1 = BAC / CPI`.
- `EAC_2 = BAC / (CPI × SPI)`.
- `EAC_3 = AC + (BAC - EV) / (CPI × SPI)`.

Explica unidades, fechas, fuentes, elección de fórmula y limitaciones. Si falta AC o algún denominador es cero, consigna **No calculable con evidencia actual**; jamás uses un cero inventado o sustituyas EV por el porcentaje técnico de la auditoría. Tampoco supongas que el presupuesto ilustrativo de la consigna es el BAC aprobado.

## 4.3 Archivos oficiales — nombres y carpetas exactos

Crea en `docs/04 Cierre/`, sin subcarpetas:

1. `01 Reporte de Estado V_1_0_0.md`: logros, cambios de alcance, calidad, hitos, causas raíz, costo ejecutado, look-ahead, riesgos e incidentes; síntesis ejecutiva preferiblemente breve.
2. `02 Reporte de Variación V_1_0_0.md`: variación de cronograma, costo y calidad; plan/real/variación/causa/respuesta.
3. `03 Reporte de Análisis de Valor Ganado - EVM V_1_0_0.md`: PV/EV/AC por periodo, acumulados, SV/CV/SPI/CPI y tres escenarios EAC.
4. `04 Tableros de Control - Híbridos V_1_0_0.md`: KPI predictivos/adaptativos, RAG, tendencias, flujo acumulado y visualizaciones verificables; indicar frecuencia e interpretación, principio **less is more**.
5. `05 Radiadores de Información V_1_0_0.md`: Burndown, Burnup, Kanban, Mood Chart y retrospectivas con capturas reales o datos auténticos; **no crear capturas falsas**.
6. `06 Reporte Final del Proyecto V_1_0_0.md`: carta/objetivos, alcance, calidad, cronograma, costos, riesgos, éxito y transición. Si no hay aceptación, indicar «cierre pendiente de aprobación».
7. `07 Reporte Final de Lecciones Aprendidas V_1_0_0.md`: aprendizajes específicos sobre equipo, alcance, gestión híbrida, estimaciones, presupuesto, calidad, interesados y riesgos, con contexto/impacto/acción.

### Reglas documentales específicas

- Cada archivo debe tener enlace de retorno funcional: `[Volver al README principal](../../README.md)`.
- En `README.md`, agregar **siete enlaces relativos** hacia cada documento dentro de `docs/04 Cierre/`, conservando el resto del README.
- No dejar marcadores de plantilla `[ ? ]`. Cuando falte un dato, explicar **«No disponible en los registros revisados»**, indicando la fuente ausente y el impacto; **esto no equivale a cumplir la rúbrica de dato real**.
- No fabricar gráficos históricos: usar registros auténticos, tablas o Mermaid cuando reflejen datos verificables. No simular Mood Chart ni entrevistas.
- Cuando corresponda, anotar el **estado de cierre actual** y la fecha de corte: no declarar entregado o aceptado algo que siga pendiente.
- No generar archivos de imágenes ni anexos fuera de ubicaciones autorizadas; si el requisito de capturas no puede satisfacerse, enlazar evidencias existentes o registrar la ausencia.

## 4.4 Validación y reporte de control

Comprueba:

- Siete nombres y rutas exactos.
- Estructura igual a las siete plantillas de la consigna.
- Enlaces de ida y vuelta, sin rutas rotas.
- Cero marcadores de plantilla `[ ? ]` pendientes.
- Coherencia temporal, presupuestaria, de estado de requisitos y versión.
- Cálculos EVM verificables y denominadores válidos.
- Evidencias visuales genuinas, no fabricadas.
- Correspondencia explícita con la rúbrica.

Genera `AUDITORIA/VALIDACION_DOCUMENTOS_CIERRE.md` con una matriz criterio/archivo/evidencia/resultado/brecha y menciona todo dato insuficiente.

## Puerta 4 → 5

- Si no se pueden completar fielmente todas las plantillas, **no bloquees la preparación de guiones**, pero clasifica los documentos como borradores y detalla los apartados sin evidencia.
- No declares «cierre administrativo aprobado» sin acta o constancia real.
- Verifica que ningún código fuente ni BD haya sido cambiado por esta fase.

---

# FASE 5 — SUSTENTACIÓN, DEMOSTRACIÓN Y VIDEO

## Objetivo

Preparar una **sustentación de 20 minutos** (10 de gestión/cierre + 10 de demostración en vivo) y un **video MP4 de aproximadamente 5 minutos** (pitch ~1 min + demo ~4 min). El video real solo puede marcarse entregado si se crea, reproduce y verifica efectivamente.

## 5.1 Exposición de gestión — 10 minutos

Prepara un guion con tiempos, mensaje principal, diapositiva o documento de apoyo y fuente real:

- Presentación y objetivo.
- Problema y propuesta de valor.
- Gestión híbrida y evolución del alcance.
- Cronograma, desviaciones y acciones correctivas.
- Costos y EVM (solo cifras fundamentadas).
- Calidad, riesgos y defectos pendientes.
- Resultados, estado de aceptación y lecciones aprendidas.

No afirmar certificaciones, ahorros, pruebas aprobadas o satisfacción de interesados no documentados.

## 5.2 Demostración técnica — 10 minutos

Planifica secuencia y duración para flujos **realmente comprobados**:

1. Login y perfil.
2. Gestión de flota.
3. Registro/importación de pedidos.
4. Optimización por GA, con indicadores de factibilidad.
5. Rutas en mapa/tabla.
6. Vista del conductor y entrega.
7. Dashboard y PDF.
8. Reoptimización si fue validada de forma suficiente.

Para cada paso especifica usuario/rol, datos de demostración, pasos, pantalla/API implicada, resultado esperado, duración y alternativa ante fallo de servicios externos. No usar producción ni datos sensibles.

## 5.3 Video de 5 minutos

- Guion del **Elevator Pitch** de ~1 minuto: problema, público, solución, diferenciación y valor ambiental; evitar prometer resultados no comprobados.
- Storyboard del segmento de **demostración funcional** de ~4 minutos: escenas, acciones reales, transiciones, voz en off, evidencias y tiempo.
- Comprobar que el video exigido sea un **MP4 continuo con ambos segmentos**, con audio e imagen legibles. La rúbrica valora una duración aproximada de cinco minutos, con mayor exigencia para sobresaliente.
- Si Codex no tiene captura de pantalla, micrófono o codificación de video en el entorno, **no generes un archivo ficticio**. Deja un plan preciso de grabación y marca el MP4 como pendiente.
- Si realmente dispones de acceso técnico autorizado para crear un MP4 genuino desde una demostración en funcionamiento, guárdalo **únicamente** en `docs/05 Video proyecto/` y valida que se reproduce, contiene los dos segmentos y su duración.

## 5.4 Revisión de repositorio y checklist de rúbrica

- Comprobar separación frontend/backend; `.gitignore`; archivos rastreados sensibles, `node_modules`, entornos virtuales y residuos; enlaces del README y documentos de cierre.
- Revisar el estado Git **sin modificarlo**; no borrar o restaurar material previo automáticamente.
- Evaluar los cinco grupos de rúbrica: reportes/EVM, tableros/cierre, trazabilidad, demo funcional y video. Registrar evidencia y nivel **estimado**, nunca calificación oficial del docente.
- Dar prioridad a **demostración y video**, que concentran 24 de los 33 puntos ponderados posibles.

## 5.5 Entregables de Fase 5 — crear en `AUDITORIA/`

1. `GUIA_SUSTENTACION_20_MINUTOS.md`: guion completo de ambos bloques con tiempos.
2. `GUION_VIDEO_5_MINUTOS.md`: narración y storyboard para grabación real.
3. `CHECKLIST_ENTREGA_FINAL.md`: requisitos de la consigna, ruta, responsable por confirmar, evidencia, estado y pendiente.
4. `RESULTADO_REVISION_FINAL.md`: preparación de entrega, defectos y riesgos, enlaces, estado MP4, archivos generados y conclusión sustentada.

Si algún documento existe, versionar sin sobrescribir pruebas previas.

---

# Cierre de la ejecución autónoma

Al terminar, responde en el chat de Codex **sin ocultar fallos**:

1. **Fase 3:** pruebas ejecutadas/aprobadas/fallidas/no ejecutadas, requisitos acreditados, defectos y rutas de informes.
2. **Fase 4:** estado de los siete Markdown, calidad de enlaces, cálculos EVM y datos faltantes, estado de aprobación del cierre.
3. **Fase 5:** guiones creados, nivel de preparación de demo, ubicación y **estado real** del MP4 (creado/verificado o pendiente), checklist y riesgos.
4. Lista de **todos los archivos creados o modificados**, con ruta.
5. Estado Git final y explicación de cualquier cambio fuera del alcance o limitación de entorno.
6. Acciones que todavía requieren intervención humana (por ejemplo, obtener registros AC/EVM, capturas auténticas, acta de aceptación, grabar voz/video).

**Definición de terminado de la automatización:** las fases han sido ejecutadas hasta donde la evidencia y los permisos lo permiten, los archivos autorizados están generados/verificados, y todos los pendientes están explícitos. **No equivale a que el proyecto esté aprobado o cerrado.**
