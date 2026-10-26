# Retrospectiva del sprint

**Versión documental:** V_1_0_0

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

## ¿Qué aprendimos?

- Tener funcionalidad ejecutable no equivale a tener una historia terminada: la DoD global exige cobertura, análisis estático sin deuda bloqueante, peer review, staging y documentación, y varias de esas condiciones siguen abiertas.
- La trazabilidad criterio–código–prueba detecta desviaciones que una prueba verde no muestra: US-013 pide litros pero la implementación entrega galones; US-014 calcula metas en backend pero no las resalta en UI; US-010 filtra en lugar de atenuar.
- Los estados degradados requieren pruebas propias. Implementar tabla fallback, IndexedDB, Service Worker e idempotencia no demuestra por sí solo recuperación cartográfica ni sincronización offline sin duplicados.
- Los indicadores deben provenir de una única fuente persistida y deben evitar resultados inventados. El servicio de indicadores reutiliza soluciones y línea base, y devuelve valores no comparables cuando faltan datos válidos.
- Accesibilidad y seguridad deben revisarse durante el desarrollo. Lighthouse/axe detectaron barreras en mapa, contraste y teclado; SonarQube y las auditorías de dependencias identificaron deuda que debe entrar en el flujo habitual, no solo al cierre.
- Separar claramente evidencia ejecutada, riesgo posible y asunto no evaluado mejora la calidad de las actas y evita declarar conformidad o cierre sin sustento.

## ¿Qué estamos haciendo bien?

- La suite vigente es reproducible en Docker: 118 pruebas backend aprobaron y el build de producción terminó correctamente; Vitest aprobó 6 pruebas frontend.
- Hay trazabilidad técnica para Sprint 3: GeoJSON autorizado para mapa/detalle, presentación común de paradas, endpoint de indicadores, línea base persistida, factor de Quinual y cola offline por usuario.
- Se evita inventar porcentajes cuando no hay línea base comparable y se muestra un mensaje explícito para periodos sin rutas.
- La confirmación de entregas incorpora una clave de idempotencia y el frontend mantiene una cola pendiente, decisiones coherentes con la sincronización sin duplicados.
- Se ejecutó SonarQube local con cobertura importada y se documentaron por separado calidad, OWASP y WCAG, incluyendo limitaciones y resultados no conformes.
- El control de acceso permanece en backend y las pruebas de seguridad verifican JWT/RBAC; la visibilidad del frontend no se usa como única barrera.
- Git conserva historial reciente de implementación y correcciones; el repositorio incluye lockfiles, CI, configuración de SonarQube y pruebas automatizadas.

## ¿Qué podemos hacer mejor?

### Personas

- Definir antes del cierre quién valida cada criterio de aceptación, quién ejecuta las pruebas de accesibilidad/offline y quién reúne la evidencia de DoD. No se encontró una asignación aprobada para estas tareas de Sprint 3.
- Reservar capacidad explícita para QA frontend, accesibilidad, seguridad y pruebas en navegadores; la concentración actual de evidencia en backend deja sin cobertura suficiente los flujos visuales y PWA.
- Mantener a la Project Manager informada de discrepancias entre backlog e implementación para que las decisiones de alcance o cambio de criterio queden registradas. No se atribuye aprobación alguna en esta retrospectiva.

### Relaciones

- No se encontró registro verificable de Sprint Review, retrospectiva celebrada, feedback de stakeholders, acuerdos del equipo ni aceptación de US-010 a US-015/EN-004.
- Tampoco se encontró evidencia de peer review del Sprint 3. Debe confirmarse si las revisiones ocurrieron fuera del repositorio y, si existen, enlazarlas sin reconstruirlas retrospectivamente.
- Como mejora propuesta, centralizar decisiones sobre unidades, metas visuales, factor ambiental y comportamiento offline en Jira o en el mecanismo acordado por el equipo, vinculándolas con PR y pruebas.

### Procesos

- Convertir cada escenario BDD en una prueba o evidencia explícita antes de mover una historia a Done, incluidos los caminos infelices: falla de tiles, ausencia de línea base, periodo vacío y reconexión.
- Incorporar una revisión de coherencia entre unidad, etiqueta de UI, contrato API y criterio de aceptación; esto habría detectado antes la diferencia litros/galones.
- Establecer gates reales de cobertura ≥80%, análisis estático y build. El `cov-fail-under=0` actual permite finalizar pytest aunque no se cumpla la DoD.
- Exigir evidencia de PR aprobado y despliegue en staging; el workflow existente y un placeholder no acreditan esos criterios.
- Ejecutar pruebas frontend de componentes y end-to-end con datos aislados para mapa, detalle, tabla, KPI y offline, además de pruebas manuales documentadas con teclado y lector de pantalla.
- Mantener Sprint 4 fuera del cierre Sprint 3. US-016 a US-018 y EN-002 no deben utilizarse para evaluar el cumplimiento de esta iteración.

### Herramientas

- **Codex:** se utilizó en esta sesión para inspección del repositorio, ejecución local de verificaciones y elaboración de los dos documentos. Su salida debe conservar revisión humana; no constituye peer review ni aprobación del equipo.
- **Git:** aporta historial y control de cambios, pero no reemplaza evidencia de PR aprobado. Conviene vincular commits, historias y revisiones sin incluir cambios ajenos o no consolidados.
- **SonarQube:** ya produce resultados reales y cobertura, pero el Quality Gate observado se centra en código nuevo y puede pasar mientras existen incidencias históricas bloqueantes. Se requiere un gate alineado con la DoD y clasificación formal de falsos positivos.
- **Docker Compose/PostGIS:** permitió ejecutar la suite integrada del backend de forma reproducible. Deben añadirse entornos efímeros para pruebas de demo, offline y staging sin afectar datos persistentes.
- **Pytest/pytest-cov:** ofrecen buena cobertura del dominio y 118 pruebas verdes, pero el total backend es 75% y WebSockets/API conservan zonas con cobertura baja.
- **Vitest/V8:** está operativo, aunque las 6 pruebas se concentran en utilidades; faltan componentes React, mapa, tabla, dashboard, IndexedDB y Service Worker.
- **Lighthouse, axe-core y Playwright:** permitieron evaluar pantallas renderizadas y encontraron fallos reales. Deben integrarse como regresión después de corregir accesibilidad, manteniendo pruebas manuales para criterios no automatizables.
- **npm audit y pip check:** aportaron evidencia de dependencias; npm encontró avisos en herramientas de desarrollo y `pip check` no encontró requisitos rotos. Falta una SCA Python capaz de consultar vulnerabilidades.
- **GitHub Actions:** existe configuración de CI, pero no se verificó una ejecución remota verde ni un despliegue staging real para este cierre.
- **Jira:** existen artefactos y capturas históricas de planificación, pero no se encontró evidencia actualizada de estados, acuerdos o aceptación del Sprint 3; su vigencia debe confirmarse con el equipo.

### Acciones a realizar

Las siguientes son **propuestas derivadas de la evidencia**, no acuerdos aprobados. Responsable, fecha objetivo y aceptación deben confirmarse en la retrospectiva real del equipo.

| Acción propuesta | Evidencia verificable de cierre | Responsable / aprobación |
|---|---|---|
| Alinear US-010, US-013 y US-014 con sus criterios: atenuación de rutas, litros y resaltado de metas. | Pruebas de componente/E2E verdes y criterio actualizado solo si el equipo aprueba un cambio. | Por confirmar |
| Completar pruebas de mapa, detalle y tabla ante falla/restablecimiento de cartografía. | Ejecución automatizada con datos aislados y evidencia de teclado/accesibilidad. | Por confirmar |
| Cubrir EN-004 extremo a extremo: IndexedDB, corte de red, reconexión, Background Sync e idempotencia. | Una entrega encolada offline se sincroniza una sola vez tras reintentos; pruebas repetibles en navegador. | Por confirmar |
| Corregir hallazgos WCAG confirmados y repetir la evaluación. | Lighthouse/axe sin los fallos corregidos y checklist manual de teclado, foco y lector de pantalla. | Por confirmar |
| Elevar la cobertura backend/frontend al 80% o someter a aprobación una modificación de la DoD. | Reportes de cobertura archivados y pipeline bloqueando valores inferiores al umbral vigente. | Por confirmar |
| Resolver/clasificar incidencias SonarQube y endurecer el Quality Gate. | Sin deuda bloqueante bajo el criterio DoD; decisiones de falso positivo justificadas en la herramienta. | Por confirmar |
| Incorporar SCA de Python y auditoría completa de dependencias en CI. | Reporte reproducible, política de severidades y tratamiento documentado de hallazgos. | Por confirmar |
| Obtener peer review y desplegar a staging mediante pipeline real. | PR aprobado por un par y ejecución de staging exitosa enlazada al Sprint 3. | Por confirmar |
| Realizar Sprint Review y retrospectiva con el equipo. | Acta con fecha, participantes, feedback, decisiones, responsables y aceptación/rechazo de cada historia. | Por confirmar |
\n+[← Volver al README principal](../../../README.md)
