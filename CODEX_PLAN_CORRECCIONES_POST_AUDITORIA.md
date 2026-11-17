# EcoLogística Junín — Prompts de implementación post-auditoría

**Ruta del repositorio:** `C:\Users\Baguette\Documents\Proyectos\ecologistica-junin`  
**Origen:** `AUDITORIA/ERRORES_Y_PENDIENTES_FINAL.md`, `AUDITORIA/VERIFICACION_FINAL_CONSIGNA_HTML.md`, `AUDITORIA/EVALUACION_RUBRICA_FINAL.md`, `AUDITORIA/CHECKLIST_CIERRE_DEFINITIVO.md` (corte 17/11/2026; commit auditado `b47d5eb7cda26444c56460ea74591cc5f973e0b3`).  
**Exclusión:** el video MP4 queda fuera del alcance por ahora.

> **Uso:** coloca este archivo en la raíz del repositorio y pega en Codex el **PROMPT MAESTRO** que aparece abajo. Este documento no autoriza a inventar cifras o actas, ni a alterar bases de datos existentes sin validación. Al terminar cada bloque Codex debe comprobar aceptación, registrar cambios y continuar solo si no hay bloqueos. Para tareas que requieran acceso, datos o autorizaciones ausentes, debe dejar una solicitud concreta y continuar con tareas independientes y seguras.

---

## PROMPT MAESTRO — EJECUCIÓN SECUENCIAL AUTÓNOMA

Actúa como ingeniero senior full-stack, QA, seguridad y responsable de documentación técnica del proyecto **EcoLogística Junín**. Trabaja desde `C:\Users\Baguette\Documents\Proyectos\ecologistica-junin`. Lee íntegramente este archivo y las cuatro auditorías de `AUDITORIA` arriba citadas. **Ejecuta en secuencia las fases 0, 1, 2, 3, 4 y 5 de este documento**, respetando sus dependencias. No solicites un nuevo prompt para pasar de una fase a otra si has satisfecho sus criterios de salida y los cambios son seguros. No marques resuelto un hallazgo por implementar código sin pruebas o evidencias. Si una fase tiene elementos bloqueados por ausencia de datos, credenciales, acceso, aprobaciones o servicios, consigna esos elementos como BLOQUEADOS, pasa solo a las actividades independientes y al final enumera las decisiones humanas necesarias.

**Reglas generales:**

1. Antes de modificar, ejecuta inspección de `git status`, rama y SHA, identifica cambios preexistentes y respétalos; nunca hagas `reset --hard`, `clean`, ni sobrescribas trabajo ajeno. No realices `commit`, `push`, deploy, cambios de secretos, ni toques producción.
2. Modifica el código solamente para corregir hallazgos identificados y sus dependencias demostradas, conservando React/TypeScript/FastAPI/PostgreSQL/PostGIS, contratos compatibles y arquitectura actual. Evita reescrituras masivas, dependencias nuevas o cambios cosméticos globales. Si algo requiere nuevas dependencias, justifícalo y deja constancia antes de introducirlas.
3. **Datos y seguridad:** cualquier migración de esquema, prueba destructiva, operación sobre datos reales o sustitución de credenciales requiere autorización humana específica. Puedes crear y utilizar fixtures, mocks y bases efímeras/descartables solo cuando hayas verificado su aislamiento. Si no hay aislamiento, no ejecutes esa prueba. No copies datos personales a informes ni reveles secretos.
4. **Ubicación:** informes de diagnóstico, logs consolidados, matrices y control de fases se crean en `AUDITORIA/`; código y pruebas solamente en sus directorios de origen; las revisiones oficiales de los siete `.md` solo en `docs/04 Cierre/`; cambios del README solo si son necesarios para trazabilidad; documentación técnica ya existente solo si la actualización es necesaria y queda versionada. No generes documentos nuevos dispersos en la raíz, salvo este archivo proporcionado por el usuario. Los archivos temporales de test/build deben estar configurados en carpetas controladas, ignoradas por Git, y documentarse.
5. Usa **test-driven regression** cuando corresponda: escribe/revisa escenarios que reproduzcan el defecto, implementa corrección mínima, ejecuta pruebas focalizadas y regresión relacionada. Distingue `PASÓ`, `FALLÓ`, `NO EJECUTADA`, `NO VERIFICABLE`. No se permite sustituir integración real por mocks sin reconocerlo.
6. Para los hallazgos AF-04/05/16–20/27/34 y otros históricos, no inventes presupuesto aprobado, PV/EV/AC, fechas, story points, encuestas, capturas, reuniones, actas o firmas. Documenta el dato exacto que falta y la fuente requerida. Crea plantillas de **recolección prospectiva** y reportes reproducibles solo con fuentes existentes. Etiqueta toda simulación como simulación y no la uses para afirmar cumplimiento.
7. El video MP4, `docs/05 Video proyecto` y su rúbrica permanecen **EXCLUIDOS TEMPORALMENTE**. Sí prepara y verifica la demostración en vivo de diez minutos.
8. Nunca declares “100%”, “cerrado”, “aceptado” ni puntaje de rúbrica si la evidencia no lo sustenta. Vincula cada corrección a su ID AF-xx y a Hxx cuando corresponda.
9. Los resultados y errores nuevos pueden modificar prioridades. Documenta el cambio de plan, pero no amplíes el alcance de forma arbitraria.
10. Mantén al final de cada fase `AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md` con fecha, SHA, archivos, hallazgos, comandos, resultados, regresiones, bloqueos y siguiente fase. Si ya existe, actualízalo preservando historial y añade nueva sección; no sobrescribas informes históricos.

### Criterios de parada obligatoria

Detén **la operación riesgosa** y solicita permiso explícito si requiere migrar o modificar BD existente, usar credenciales reales, realizar despliegue, instalar dependencias disruptivas, alterar alcance/criterios aprobados o suprimir evidencia histórica. Puedes continuar otras tareas independientes. Detén la cadena completa si aparece un fallo crítico de seguridad o integridad introducido por tus cambios que no puedes resolver de forma segura. No ocultes las fallas para completar la automatización.

---

## FASE 0 — LÍNEA BASE Y PLAN EJECUTABLE

**IDs:** todos AF-01 a AF-35; H01–H56 (video excluido).

1. Abre los cuatro informes finales y `BACKLOG_IMPLEMENTACION.md`, confronta los hallazgos con **código actual**, identificando qué sigue abierto y qué ya cambió desde el SHA auditado. No heredes estados sin revisar.
2. Registra `git status`, herramientas, servicios, fixtures, comandos de test y riesgos de efectos secundarios. Identifica el residual `.vitest/json/output.json` de AF-30; **no lo borres automáticamente**. Corrige configuración del reporter y `.gitignore` únicamente si preservas evidencia y registras el cambio.
3. Crea `AUDITORIA/PLAN_CORRECCIONES_EJECUTABLE.md` con tabla: ID, impacto, archivos, dependencia, criterios de aceptación, test, permisos necesarios, estado inicial, prioridad, fase. Mapea hallazgos a requisitos RF/RNF y Hxx. Mantén prioritarios AF-01/02/03 y los bloqueos de EVM y aceptación, pero distingue implementación de aportación humana.
4. Antes de cada fase, verifica si la línea base sigue válida. No confundas la falla de `fleet.test.tsx` (AF-24) con una avería funcional demostrada; revisa el contrato de paginación.

**Salida:** inventario sustentado y plan; no suponer que la ejecución de un comando prueba el producto completo.

---

## FASE 1 — SEGURIDAD, TRANSICIONES Y WEBSOCKETS

**Prioridad:** AF-01, AF-02, AF-03 (P0), AF-06 (P1), AF-29 (P2); conservar B-08.

### A. Autorización vigente (AF-01)
- Inspecciona `app/api/v1/websockets.py`, `routes.py`, modelos de asignaciones, detalles y versiones de ruta, endpoints REST y eventos WS.
- Sustituye el criterio de autorización basado en **cualquier asociación histórica** por asignación efectivamente vigente según plan activo, pedido, vehículo, conductor, permisos y versión. Mantén historial para lectura autorizada.
- Comprueba de forma transaccional antes de mutar o publicar; resuelve carreras entre reasignación y entrega.
- Pruebas: asignación A→B, A no puede confirmar/cancelar; B sí; múltiples roles, expiración, cambio concurrente, rollback sin estado parcial.

### B. Estados terminales e idempotencia (AF-02)
- Define y usa matriz única de transiciones de pedido (incluidos terminales), y controla versión/concurrencia para entregas, cancelaciones y reroute.
- Pedido entregado no puede volver a pendiente ni cancelado; duplicados e intentos fuera de orden deben responder idempotentemente o ser rechazados con contrato documentado.
- Pruebas: entregar→cancelar; entregar→reroute; eventos repetidos; fallo entre persistencia y notificación; estados anteriores intactos.

### C. Privacidad del tracking (AF-03)
- Separa modelo público de seguimiento por pedido del modelo interno para operador/conductor autorizado.
- El payload público no debe exponer posición GPS precisa, IDs internos, secuencias de otros pedidos, rutas ajenas ni eventos que revelen operaciones de terceros.
- Verifica todos los mensajes, incluida conexión inicial, snapshot, inserción/cancelación, reoptimización y desconexión; elimina suscripción usando la misma clave efectiva con la que fue registrada.
- Crea pruebas negativas de filtración y aislamiento con clientes concurrentes.

### D. Sesión WebSocket (AF-06)
- Asegura caducidad, revalidación de permisos, revocación y cierre de socket. Revisa tokens en URLs/logs, reconexiones, límites y manejo de expiración.
- Prioriza cambios compatibles; documenta si trasladar el token requiere actualizar clientes y tests. No guardes ni escribas tokens reales en pruebas.
- Inspecciona secretos en HEAD y mecanismos para revisar historial (AF-29) sin publicar valores sensibles. La revocación real de un secreto solo puede ser autorizada por su propietario.

**Control y salida:** pruebas de regresión de seguridad/REST/WS verdes; B-08 preserva rechazo de rutas inválidas y atomicidad; no exponer datos sensibles en reportes. `AUDITORIA/RESULTADOS_FASE1_SEGURIDAD.md`. No avances a cambios acoplados si queda un defecto P0 reproducible sin resolver.

---

## FASE 2 — INTEGRIDAD OPERATIVA, MODELOS, ALGORITMO Y REPORTES

**IDs principales:** AF-07 a AF-15, AF-24, AF-23 según posibilidad; AF-12 migración condicionada a permiso.

### Bloque 2A: estado y eventos
1. AF-07: especifica versión **activa / archivada / ejecutada**; evita sumar planes sustituidos. No elimines historial. Sincroniza mapas, ETA, KPI, API, grupos de vehículos y PDF.
2. AF-08: persiste evento de entrega real (hora servidor/cliente con zona horaria, actor, estado y evidencia según permisos), con idempotencia y trazabilidad; no confundir ETA/ventana con hora efectiva. No almacenes fotografías/firmas si falta política de privacidad y persistencia aprobada; documenta bloqueo.
3. AF-09: define un oráculo de cálculo independiente de distancia, combustible/energía, CO₂, costos, ahorro y puntualidad, con unidades y factores versionados; prueba flotas mixtas eléctrico/combustión y consistencia solver→BD→KPI→PDF.
4. AF-11: verifica origen/carga/jornada/horario real y reoptimización multivehículo ante avería; continuidad de estado tras reinicio. No afirmes durabilidad sin un backend durable comprobado.

### Bloque 2B: alcance y esquemas
5. AF-13: compara RF-01/02 con modelos/API/UI/importaciones; completa atributos realmente requeridos (tipo vehículo, prioridad, tipo producto, peso/volumen, CSV/XLSX cuando obligatorio) de extremo a extremo, sin cambiar el alcance de forma tácita.
6. AF-14: compara RF-08/09/10 con requisitos originales y alcance aprobado. Completa las funcionalidades claramente implementables y dependientes del diseño existente; si falta decisión sobre licencias, preferencias o plan de compensación, especifica contrato y solicita información. No declares exención sin aprobación.
7. AF-12: diseña migración versionada y tests para esquema legado, pero **NO ejecutes migración sobre BD persistente o existente** sin autorización. Prueba con copia descartable solo si el aislamiento es comprobable y permitido.
8. AF-15: corrige reportes PDF/CSV, versiones y fechas según contrato, conciliando cifras con el mismo oráculo, y verifica integridad del archivo generado en directorio de pruebas seguro.

### Bloque 2C: rendimiento y calidad funcional
9. AF-10: construye benchmark de 150 pedidos / 15 vehículos con instancia de referencia independientemente factible; evalúa asignación completa sin duplicados, ventanas, capacidades, jornada y tiempo HTTP real ≤45 s; reoptimización válida <30 s. Documenta hardware y dependencia OSRM. Si no hay entorno o instancia factible, no declares SLA cumplido.
10. AF-24: determina contrato correcto de historial de flota; corrige implementación o prueba sin eliminar aserciones sustantivas para hacerla pasar. Repite `fleet.test.tsx` y suite frontend.
11. AF-23: prepara pruebas de carga y disponibilidad 1 000 pedidos/día, 50 vehículos, SLI 99,5 %, backup/reinicio/restore según RNF. Ejecuta solo con infraestructura aislada autorizada; no infieras uptime productivo de pruebas cortas.
12. AF-25: verifica accesibilidad WCAG en flujos relevantes (teclado, foco, zoom/reflow, contraste, lector) y corrige defectos verificables; pruebas reales de usuario no se inventan.

**Criterios de salida:** casos representativos verdes en entorno autorizado, conciliación de plan/versiones/datos, sin regresiones de fase 1; lista separada de pruebas bloqueadas, migraciones sin ejecutar y requisitos que requieren decisión. `AUDITORIA/RESULTADOS_FASE2_FUNCIONALIDAD.md`.

---

## FASE 3 — PRUEBAS REPRODUCIBLES, CI, ARRANQUE Y DEMOSTRACIÓN

**IDs:** AF-21/22/23/25/29/30/31/35 y otros afectados.

1. Define matriz por RF-01…RF-10, RNF-01…RNF-07 y hallazgos AF-xx: test, caso positivo/negativo, resultado, fecha, SHA, entorno, evidencia.
2. Ejecuta suite backend y frontend **completa** cuando haya PostGIS aislado; no uses BD productiva. Separa unidades con mocks de integración real. Ejecuta TypeScript, build si hay destino seguro, revisión de tests y Service Worker. Indica cobertura por métrica exacta (líneas versus combinado), y umbral si fue aprobado; no reduzcas umbrales artificialmente.
3. Configura y verifica CI (incluida cobertura, lint y seguridad si herramientas disponibles) sin declarar staging operativo hasta que se haya desplegado y observado. Escaneo de secretos sin divulgación; no borres residuos heredados sin consentimiento.
4. Prueba integración end-to-end con datos descartables y roles autorizados: login→pedido→optimización→persistencia→mapa→conductor→entrega→KPI→PDF. Comprueba que cada paso usa persistencia real aislada; no lo sustituya todo por fixtures de UI.
5. Elabora un guion y prueba de demostración **en vivo de 10 minutos** y gestión de 10 minutos. Cronometra solo si realmente puedes operar el navegador/servicios, y registra resultados; si no, entrega instrucciones y estado NO VERIFICADO. Comprueba red, OSRM, tiles, WS, CORS y contingencias.
6. Revisa guía por roles, instalación, runbook, rollback y recuperación, con versión SHA. No simules validación de tercero.

**Salida:** `AUDITORIA/RESULTADOS_FASE3_PRUEBAS.md`, `AUDITORIA/MATRIZ_PRUEBAS_ACTUALIZADA.md`, `AUDITORIA/GUIA_DEMO_VERIFICADA.md`. No atribuyas resultados históricos a esta ejecución.

---

## FASE 4 — DOCUMENTOS, EVM, HISTORIA Y EVIDENCIA ÁGIL

**IDs:** AF-04/05/16–20/26–28/31–34 y AF-32. **Esta fase NO autoriza fabricar registros ni firmar actas.**

1. Revisa `docs/04 Cierre` frente a las siete plantillas exactas del HTML, respetando nombres y los enlaces README↔documentos actualmente correctos (14/14). Actualiza contenido solo cuando exista evidencia nueva verificable; conserva versión e historial de cambios, diferenciando borrador/cierre validado.
2. **EVM:** inventaria BAC aprobado, PV/EV/AC del periodo, acumulado actual y anterior; identifica fuentes y unidades. Si existen valores auténticos: calcula SV=EV−PV, CV=EV−AC, SPI=EV/PV, CPI=EV/AC, % respecto BAC y tres EAC; justifica elección y trata denominadores nulos. Si faltan, **no inventes**; genera `AUDITORIA/SOLICITUD_DATOS_EVM.md` con tabla de campos, propietario, fuente, periodo y comprobante requerido. No uses el presupuesto estimado USD 134 400 / S/ 499 968 como BAC aprobado salvo confirmación documental.
3. AF-16/17: concilia fechas/hitos 2024 vs 2026, costos reales/estimados y Look Ahead; agrega solo hechos corroborados. Si no hay registros, emite plantilla de recolección sin imputar fechas ni gastos.
4. AF-18/19/20/27: reconstruye gráficos EVM, CFD, CSI, Burndown, Burnup, Mood y retrospectivas **solo** a partir de datos históricos verificables; conecta capturas de Jira con fecha, consulta y ticket si la fuente lo permite. Si no, registra ausencia; no generes series sintéticas con apariencia histórica ni inventes clima del equipo.
5. AF-05/34: prepara un paquete de preguntas y campos para aceptación, satisfacción, acuerdos de retrospectiva y transición operativa **para que personas reales los completen y validen**. No inventes firmas, encuestas, aprobaciones, exenciones, actas o reuniones pasadas. Conserva estado pendiente hasta que haya evidencia.
6. AF-26/28/32: repara enlaces históricos únicamente cuando localices destino auténtico o correspondencia inequívoca, sin alterar imágenes originales ni ocultar versiones; arregla hashes corruptos comprobando SHA real y contexto, nunca adivinando. Consigna los enlaces irresolubles. Preserva los 14 enlaces correctos de cierre.
7. AF-33: solicita y registra ausencia de consigna original independiente si no está en el repositorio; no la reconstruyas como fuente auténtica.
8. Incorpora al reporte de cierre resultados técnicos nuevos, distinguiendo comprobado, pendiente y aprobado por autoridad real. Ninguna edición documental sustituye aceptación administrativa.

**Salida:** `AUDITORIA/RESULTADOS_FASE4_DOCUMENTACION.md`, `AUDITORIA/SOLICITUD_EVIDENCIAS_HUMANAS.md`, y, si faltan entradas, `AUDITORIA/SOLICITUD_DATOS_EVM.md`. Revisión de siete documentos y enlaces, sin video.

---

## FASE 5 — REAUDITORÍA INDEPENDIENTE Y ENTREGA DE RESULTADOS

**Referencias:** 35 hallazgos AF-01…AF-35 y 56 verificaciones H01…H56; no contabilizar video.

1. Relee las cuatro auditorías originales y el HTML docente completo, contrasta el código/documentos **actuales**; no marques hallazgo como resuelto por haber editado archivos.
2. Para cada AF-xx, asigna `RESUELTO CON EVIDENCIA`, `PARCIAL`, `ABIERTO` o `BLOQUEADO/NO VERIFICABLE`, con archivo/línea/comando/prueba/fecha/SHA. Para Hxx asigna CUMPLE/PARCIAL/NO CUMPLE/NO VERIFICABLE. No confundas una prueba omitida con aprobada.
3. Recalcula la evaluación de los cuatro criterios aplicables de la rúbrica (pesos 1/1/1/4, máximo provisional 21), solo si las pruebas y la demostración permiten sustentar niveles. Si persisten perfiles mixtos, no inventes nota. Video excluido, no 0.
4. Ejecuta pruebas de regresión seguras, inspecciona `git diff --check`, resumen de diffs, referencias, archivos nuevos e ignorados; informa residuales, migraciones no ejecutadas y secretos sin mostrar valores.
5. Genera `AUDITORIA/REAUDITORIA_POST_CORRECCIONES.md`, `AUDITORIA/MATRIZ_AF_01_A_AF_35.md` y `AUDITORIA/PENDIENTES_PARA_USUARIO_Y_DOCENTE.md`. Último archivo debe indicar exactamente cuáles datos, capturas, aprobaciones, ensayos o accesos externos solo el usuario/equipo/docente puede proporcionar.
6. Finaliza con: hallazgos resueltos/parciales/abiertos/bloqueados; tests actuales; lista de archivos modificados; qué quedó sin verificar; qué requiere intervención humana; disposición para demo; puntuación provisional únicamente si sustentable. **No declares cierre definitivo salvo evidencia íntegra de aceptación y cumplimiento.**

---

## Condición importante sobre automatización

Este plan automatiza la **secuencia de trabajo de Codex** dentro de una sesión con acceso al proyecto y permisos adecuados; no crea una tarea programada que siga ejecutándose por sí sola cuando cierres la sesión. Si Codex alcanza límites de contexto o tiempo, deberá registrar estado, fase actual y siguiente paso en `AUDITORIA/CONTROL_CORRECCIONES_SPRINT4.md`, para que otra sesión continúe leyendo el archivo, sin perder trazabilidad.
