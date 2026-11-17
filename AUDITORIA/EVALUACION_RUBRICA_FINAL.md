# Evaluación de la rúbrica final

**Corte:** 17/11/2026, America/Lima. **Versión:** 1.0.0.  
**Commit:** b47d5eb7cda26444c56460ea74591cc5f973e0b3 · main.  
**Fuente normativa:** sección 4 del HTML docente, contrastada con sus secciones 1–3 y 5 completas. SHA256 del HTML: 098e994680f3a923a7b339a655ddf876a5b3ca712357884ef5c8697a4186a6a2.

**Resultado: no es posible emitir una nota global definitiva ni una puntuación provisional numérica sustentada sobre 21.** Hay incumplimientos verificables y perfiles mixtos entre descriptores, además de una demostración en vivo no observada. Esto no significa 0/21 ni aprobación. La matriz de cumplimiento concluye **NO cumple todos los requisitos**.

## Método y límites de la calificación

La solicitud exige elegir el nivel cuya **totalidad de condiciones** esté suficientemente acreditada, y no puntuar por intuición. La rúbrica contiene descriptores compuestos con varios supuestos. No especifica cómo agregar un perfil en el que unas condiciones corresponden a un nivel y otras a otro. Por tanto:

1. Se comprueba cada nivel íntegro, conservando sus alternativas expresas.
2. Se señalan las condiciones concretas acreditadas y las que faltan.
3. Si no se acredita un descriptor completo o falta evidencia esencial, se registra **NO EVALUABLE**, sin convertirlo en cero.
4. No se impone por cuenta propia una regla como “el peor subindicador determina toda la nota”, un promedio de subindicadores o puntos por archivo.
5. Los descriptores de desempeño parcial se usan para describir brechas, no para afirmar defectos que no se observaron.

Este método es más estricto que seleccionar una sola frase del nivel 0 por la ausencia de EVM, o una sola frase del nivel 1 por los gráficos faltantes. Para una cifra oficial se necesita aclaración docente del tratamiento de perfiles mixtos y la evidencia de demostración; mientras tanto los incumplimientos documentales sí se pueden y deben corregir.

Escala oficial: 3 Sobresaliente, 2 Suficiente, 1 En desarrollo, 0 Insatisfactorio. Estados de cumplimiento y niveles académicos son escalas distintas: un indicador financiero **NO VERIFICABLE** no recibe automáticamente cero.

## Tabla ponderada obligatoria

| Criterio | Peso | Nivel estimado | Puntos ponderados | Evidencia | Observaciones |
|---|---:|---|---:|---|---|
| Reportes Narrativos y Análisis de Valor Ganado (EVM) | 1 | **NO EVALUABLE: perfil mixto; EVM cuantitativo incumplido** | — | D01–D03; presupuesto estimado, acta y matriz matemática de verificación | Tres archivos y estructura presentes; no cifras PV/EV/AC ni índices/EAC aplicados. La ausencia de cálculos coincide con una condición de nivel 0, pero no faltan dos documentos ni hay múltiples marcadores, como también describe ese nivel. |
| Reportes Visuales y Cierre Administrativo | 1 | **NO EVALUABLE: perfil mixto con omisiones del nivel 1** | — | D04–D07; capturas proporcionadas y fuentes históricas de pruebas | Faltan gráficos/radiadores y satisfacción/cierre. A la vez hay RAG/barras reales, diferenciación híbrida y lecciones específicas; no se acredita íntegramente un único descriptor. |
| Trazabilidad y Versionamiento del Repositorio | 1 | **NO EVALUABLE: estructura/enlaces suficientes; versiones incoherentes** | — | Siete archivos exactos, 14 enlaces correctos; calidad Sprint 3 y capturas/versiones previas | No hay 1–2 enlaces bidireccionales rotos ni nombres incorrectos de los siete archivos de cierre; sí inconsistencias previas. Nivel 2 exige también actualización/versionamiento coherentes, todavía no acreditados. |
| Demostración Funcional y Arquitectura del Código | 4 | **NO EVALUABLE** | — | app/, src/, .gitignore, pruebas actuales, guía de exposición | Sin observación actual de arranque/BD/integración end-to-end ni ensayo de diez minutos. Código/tests no acreditan tiempo y fluidez. Tampoco se demostró fallo de arranque. |
| **Total de criterios incluidos** | **7** | **Sin nivel completo numéricamente acreditado** | **No determinable sobre 21** | Cuatro criterios revisados | No se suman los guiones como ceros ni se inventa puntuación parcial. |
| Evidencia audiovisual | 4 | **EXCLUIDO TEMPORALMENTE — NO EVALUADO** | — | Fuera de alcance por instrucción del usuario | Sin comprobaciones audiovisuales, sin cero y sin efecto en pendientes o puntuación incluida. |

Máximo aplicable: 1×3 + 1×3 + 1×3 + 4×3 = **21 puntos**. Máximo completo de la rúbrica original: **33**, de los cuales **12 están excluidos**. Criterios con nivel íntegro acreditado para suma numérica: **0 de 4**; esto cuenta criterios calificables, **no puntos obtenidos**. No hay subtotal numérico emitible. No se convierte a una nota sobre 20. La falta de nota no neutraliza el dictamen de incumplimiento.

## Contraste completo de niveles

Las condiciones siguientes son paráfrasis del HTML, no una nueva rúbrica. D01…D07 son los siete archivos oficiales en docs/04 Cierre; las rutas y pruebas se detallan en [verificación](VERIFICACION_FINAL_CONSIGNA_HTML.md).

### 1. Reportes narrativos y EVM, peso 1

| Nivel | Condiciones del descriptor | Contraste con evidencia |
|---|---|---|
| 3 | Tres documentos completamente llenos sin marcadores; EVM y tres EAC exactos/justificados; causas conectadas con métricas, acciones e historia | **No acreditado:** estructura/sin marcadores sí; cifras reales, comparación histórica financiera y EAC aplicados no. |
| 2 | Tres documentos con estructura, cálculos básicos EVM/variaciones, sin marcadores y explicaciones generales sin errores matemáticos críticos | **No acreditado:** estructura sí, pero los cálculos básicos no existen. Ausencia de cifras no equivale a cálculo correcto. |
| 1 | Un documento faltante o secciones incompletas; errores SPI/CPI/EAC; hasta tres marcadores o análisis superficial | **Perfil parcial:** secciones sustantivas incompletas sí. No falta archivo, no hay errores numéricos demostrables ni marcadores; expresiones correctas. No atribuir errores inexistentes para completar el descriptor. |
| 0 | Dos o más documentos faltantes; cálculos erróneos/inexistentes; múltiples marcadores; sin variaciones/causas | **Perfil parcial:** cálculos inexistentes sí. Los tres archivos existen, cero marcadores y hay causas/variaciones cualitativas. No corresponde afirmar todas esas deficiencias. |

**Conclusión:** EVM requerido **NO CUMPLE**; BAC/valores/resultados son **NO VERIFICABLES**. Una calificación 0 basada solo en una condición o una calificación 1 por estructura incompleta impondrían una regla de agregación no proporcionada. Se conserva NO EVALUABLE para la cifra, con defecto cuantitativo inequívoco.

### 2. Reportes visuales y cierre, peso 1

| Nivel | Condiciones del descriptor | Contraste con evidencia |
|---|---|---|
| 3 | Cuatro documentos con gráficos legibles, RAG/tendencias/CSI/radiadores reales; separación predictivo-adaptativa; satisfacción y aprendizajes accionables | **No acreditado:** gráficos/mediciones/reunión faltantes. Sí hay diferenciación y recomendaciones concretas. |
| 2 | Cuatro documentos con gráficos solicitados/capturas; final y lecciones cubren categorías sin errores graves ni marcadores | **No acreditado:** archivos/categorías/sin marcadores sí; conjunto de gráficos y radiadores no. |
| 1 | Faltan gráficos/radiadores; saturación o falta de interpretación; omisión de diferenciación híbrida o lecciones genéricas | **Perfil mixto:** faltan elementos visuales obligatorios. No se observó saturación y sí hay interpretaciones de lo disponible; la diferenciación híbrida existe y las lecciones tienen casos específicos. |
| 0 | Dos o más reportes faltantes; ausencia de gráficos/evidencia de radiadores; omisión de evaluación de cierre/lecciones | **No acreditado:** existen los cuatro, barras/RAG/Kanban y análisis de cierre/enseñanzas, aunque incompletos. |

**Conclusión:** no satisface niveles 2/3. Las omisiones se parecen a parte del nivel 1; no se afirman las restantes carencias de ese descriptor. NO EVALUABLE numérico hasta contar con regla de perfil mixto o conjunto completo de evidencias.

### 3. Repositorio y trazabilidad, peso 1

| Nivel | Condiciones del descriptor | Contraste con evidencia |
|---|---|---|
| 3 | Todos los enlaces bidireccionales funcionan; documentos previos modificados conservan historia y versión coherente; índice enriquecido | **No acreditado íntegramente:** 14/14 enlaces sí; consistencia de artefactos/versiones previos no. README tiene índice, pero eso no subsana referencias ausentes. |
| 2 | Siete nombres/ruta exactos; enlaces correctos; documentos afectados actualizados y versionados | **Parcial:** primeros dos requisitos sí. Falta reconciliar historia/cortes/versiones de artefactos previos. |
| 1 | 1–2 enlaces de ida/vuelta rotos o nomenclatura incorrecta; control de versiones omitido/inconsistencias menores en previos | **Perfil mixto:** no están rotos los 14 enlaces y los siete nombres son exactos. Sí hay nombre/título de calidad discordantes, referencias de hash corruptas y coherencia histórica pendiente. |
| 0 | Archivos fuera de la ruta, sin enlaces README o incoherencia grave sin versionar | **No acreditado como descriptor completo:** ruta/enlaces correctos; no se exagera cada desfase histórico como incoherencia grave integral. |

Las **31 ocurrencias históricas rotas de 156 referencias** están en otros enlaces, no en los catorce de cierre. No se usan para inventar “1–2 enlaces bidireccionales rotos”. Se debe corregir la trazabilidad histórica aunque no se pueda atribuir una nota unívoca.

### 4. Demostración y arquitectura, peso 4

| Nivel | Condiciones del descriptor | Contraste con evidencia |
|---|---|---|
| 3 | Diez minutos fluidos sin fallos end-to-end; arquitectura modular/desacoplada; ignore completo; guía despliegue | **No acreditado:** separación y guía existen, no se observó demo; ignore no cubre el residual .vitest. |
| 2 | Aproximadamente diez minutos con funciones principales e integración operativa, carpetas separadas e ignore sin errores críticos | **No verificable:** arquitectura sí; tiempo e integración real no observados. |
| 1 | Desviación >2 minutos, fallos menores en vivo, carpetas desordenadas o temporales no excluidos | **No acreditado íntegramente:** .vitest no excluido sí; no hubo demo para medir tiempo/fallos, ni se observó desorden general. |
| 0 | Sistema no ejecuta/falla críticamente en demo; sin separación; dependencias/entornos/claves expuestos | **No demostrado:** no hay prueba actual de fallo de arranque; separación existente y dependencias no rastreadas. Sin certificación exhaustiva de secretos. |

**Conclusión:** NO EVALUABLE. No se asigna 0 por ausencia de prueba, ni 2/3 por unidades verdes. Los riesgos estáticos impiden afirmar preparación integral sin corrección y ensayo.

## Evidencia técnica que apoya el juicio, sin sustituir la demo

Actual: **95 backend aprobadas, 90 omitidas; 68 frontend aprobadas y 1 fallida; 4 SW aprobadas**. Total de catálogo 258; 168 ejecutadas: 167 pasan y 1 falla, 90 no ejecutadas. TypeScript sin emisión pasa; inspección estática del dist previo pasa, sin build actual.

Histórico equivalente: backend 185 aprobadas con PostGIS aislado; cobertura backend 83,27 % líneas/78,68 % combinado, frontend 78,80 % líneas; benchmark solver 150×15 asigna todo en menos de un segundo pero 0/3 soluciones factibles por ventanas. Ninguno de estos resultados prueba la demo real de diez minutos, EVM o satisfacción.

## Qué falta para acreditar sobresaliente

| Criterio | Evidencia objetiva necesaria para nivel 3 |
|---|---|
| Narrativos/EVM | Aprobar BAC/baselines y cortes; obtener PV/EV/AC auténticos, costos/horas y avance aceptado; recalcular índices, porcentajes y tres EAC; seleccionar hipótesis con sustento; ligar causas, acciones, responsables, periodos y comparación histórica. Completar D01–D03 sin fabricar datos. |
| Visuales/cierre | Series trazables para EVM, CFD y CSI; barras/RAG actualizados; Burndown/Burnup/Kanban/Mood/retrospectivas reales y legibles con interpretación; validar satisfacción de interesados/equipo, acciones de lecciones y transferencia/cierre. |
| Repositorio | Conservar nombres/ruta y 14 enlaces; resolver 31 referencias históricas, fuentes Jira/calendarios, versiones y hashes; historial de cambios claro en artefactos afectados e índice navegable. No renombrar retrospectivamente evidencia para ocultar diferencias. |
| Demo/arquitectura | Resolver riesgos de autorización/terminalidad/privacidad y coherencia de KPI/PDF; probar stack y flujo integral con roles/datos autorizados; ensayo real cronometrado de 10 min sin fallos, guía reproducible, ignore completo y verificación de secretos. Evidenciar criterios de aceptación, no solo funcionamiento aparente. |

Esto es un plan de cierre **no ejecutado** por esta auditoría. Una exención requiere aprobación real; no se autoriza por marcar una casilla.

## Integridad y exclusiones

No se editaron fuentes/documentos oficiales ni se alteró BD. Se conservaron 484 hashes preexistentes bajo el perímetro de inventario. **Vitest creó accidentalmente .vitest/json/output.json fuera de AUDITORIA**; se informó y no se borró. Por esa excepción no se afirma contención perfecta. El inventario excluye dependencias, .git y material expresamente fuera de alcance; no certifica todo el equipo.

Audiovisual: **EXCLUIDO TEMPORALMENTE — NO EVALUADO**, sin cero y sin pendientes asociados. No se hicieron comprobaciones del material excluido.

Referencias complementarias: [verificación completa](VERIFICACION_FINAL_CONSIGNA_HTML.md), [problemas y aceptación](ERRORES_Y_PENDIENTES_FINAL.md), [lista de cierre](CHECKLIST_CIERRE_DEFINITIVO.md).
