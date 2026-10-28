# Retrospectiva del sprint

**Versión documental:** V_1_0_0

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

## Actualización con evidencia posterior — 27 de octubre de 2026

La evaluación posterior usó una pila Docker aislada y datos de prueba desechables. Se verificaron 143 pruebas backend aprobadas (76% de cobertura total reportada), 68 pruebas frontend aprobadas y build de producción aprobado. `npm audit`, `npm audit --omit=dev` y `pip-audit --strict` no hallaron vulnerabilidades conocidas en las dependencias evaluadas.

En accesibilidad, Lighthouse 13.5.0 obtuvo 100/100 en ingreso, seguimiento, operador y conductor bajo los recorridos aislados. axe-core no halló violaciones en ingreso, seguimiento ni conductor; en operador permanecen dos tipos de violación, sobre tres nodos: contraste insuficiente en dos objetivos y una región desplazable sin foco. Playwright verificó la tabla de ruta aislada (cinco botones y selección con `Enter`) y el diálogo de firma (foco inicial, contención y restauración). Aún faltan comprobaciones manuales con lector de pantalla, reflow a 320 CSS px y zoom 200%/400% para todos los flujos.

El escaneo final de SonarQube Community Build 26.10.0.133078 del 27 de octubre concluyó en `SUCCESS`, importó los reportes Python y LCOV de 125 archivos y obtuvo Quality Gate `OK`/PASSED. Registró 82.1% de cobertura global, 85.4% de líneas, 69.7% de ramas, 82.0% en código nuevo y 0.0% de duplicación. No es evidencia de cierre: persisten 16 bugs (1 bloqueante, 3 críticos y 12 mayores), 10 vulnerabilidades (9 mayores y 1 menor) y 4 code smells; el SCA de dependencias no estuvo disponible en esa edición/configuración.

## ¿Qué aprendimos?

- Tener funcionalidad ejecutable no equivale a tener una historia terminada: la DoD global exige cobertura, análisis estático sin deuda bloqueante, peer review, staging y documentación, y varias de esas condiciones siguen abiertas.
- La trazabilidad criterio–código–prueba detecta desviaciones que una prueba verde no muestra: US-013 pide litros pero la implementación entrega galones; US-014 calcula metas en backend pero no las resalta en UI; US-010 filtra en lugar de atenuar.
- Los estados degradados requieren pruebas propias. Implementar tabla fallback, IndexedDB, Service Worker e idempotencia no demuestra por sí solo recuperación cartográfica ni sincronización offline sin duplicados.
- Los indicadores deben provenir de una única fuente persistida y deben evitar resultados inventados. El servicio de indicadores reutiliza soluciones y línea base, y devuelve valores no comparables cuando faltan datos válidos.
- Accesibilidad y seguridad deben revisarse durante el desarrollo. Lighthouse/axe detectaron barreras en mapa, contraste y teclado; SonarQube y las auditorías de dependencias identificaron deuda que debe entrar en el flujo habitual, no solo al cierre.
- Separar claramente evidencia ejecutada, riesgo posible y asunto no evaluado mejora la calidad de las actas y evita declarar conformidad o cierre sin sustento.

## ¿Qué estamos haciendo bien?

- La suite es reproducible en Docker aislado: la evaluación posterior aprobó 143 pruebas backend y 68 frontend, además del build de producción. La cobertura backend vigente (76%) continúa por debajo del 80% exigido por la DoD.
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
- **SonarQube:** el escaneo final del 27 de octubre fue `SUCCESS` y el Quality Gate de código nuevo fue `OK`, con 82.1% de cobertura global. No obstante, el proyecto conserva 16 bugs, 10 vulnerabilidades y 4 code smells; se requiere un gate alineado con la DoD y clasificación formal, contextual y trazable de los posibles falsos positivos.
- **Docker Compose/PostGIS:** permitió ejecutar la suite integrada del backend de forma reproducible. Deben añadirse entornos efímeros para pruebas de demo, offline y staging sin afectar datos persistentes.
- **Pytest/pytest-cov:** la evaluación posterior obtuvo 143 pruebas verdes y 76% total. La mejora no alcanza el umbral DoD; WebSockets/API aún requieren cobertura dirigida.
- **Vitest/V8:** la evaluación posterior obtuvo 68 pruebas verdes, incluidas pruebas de flujos y componentes. Persisten huecos end-to-end para recuperación de tiles e IndexedDB/Background Sync.
- **Lighthouse, axe-core y Playwright:** permitieron evaluar pantallas renderizadas y encontraron fallos reales. Deben integrarse como regresión después de corregir accesibilidad, manteniendo pruebas manuales para criterios no automatizables.
- **npm audit y pip-audit:** la evaluación posterior ejecutó `npm audit`, `npm audit --omit=dev` y `pip-audit --strict`, sin vulnerabilidades conocidas. Deben mantenerse en CI y complementarse con revisión de imágenes/SBOM según la infraestructura disponible.
- **GitHub Actions:** existe configuración de CI, pero no se verificó una ejecución remota verde ni un despliegue staging real para este cierre.
- **Jira:** existen artefactos y capturas históricas de planificación, pero no se encontró evidencia actualizada de estados, acuerdos o aceptación del Sprint 3; su vigencia debe confirmarse con el equipo.

### Acciones a realizar

Las siguientes son **propuestas derivadas de la evidencia**, no acuerdos aprobados. Responsable, fecha objetivo y aceptación deben confirmarse en la retrospectiva real del equipo.

| Acción propuesta | Evidencia verificable de cierre | Responsable / aprobación |
|---|---|---|
| Alinear US-010, US-013 y US-014 con sus criterios: atenuación de rutas, litros y resaltado de metas. | Pruebas de componente/E2E verdes y criterio actualizado solo si el equipo aprueba un cambio. | Por confirmar |
| Completar pruebas de mapa y detalle ante falla/restablecimiento de cartografía. | Ejecución automatizada con datos aislados que cubra recuperación de tiles y marcador Leaflet–detalle; la selección de tabla con teclado ya fue verificada. | Por confirmar |
| Cubrir EN-004 extremo a extremo: IndexedDB, corte de red, reconexión, Background Sync e idempotencia. | Una entrega encolada offline se sincroniza una sola vez tras reintentos; pruebas repetibles en navegador. | Por confirmar |
| Corregir los hallazgos WCAG aún confirmados en operador y completar la evaluación manual. | axe-core sin los dos fallos de contraste ni la región desplazable sin foco, más checklist manual de teclado, foco, lector de pantalla, reflow y zoom. | Por confirmar |
| Elevar la cobertura backend/frontend al 80% o someter a aprobación una modificación de la DoD. | Reportes de cobertura archivados y pipeline bloqueando valores inferiores al umbral vigente. | Por confirmar |
| Resolver/clasificar incidencias SonarQube y endurecer el Quality Gate. | Revisión de los 16 bugs, 10 vulnerabilidades y 4 code smells del escaneo `SUCCESS` del 27 de octubre; sin deuda bloqueante bajo el criterio DoD y decisiones de falso positivo justificadas en la herramienta. | Por confirmar |
| Mantener SCA de Python y auditoría completa de dependencias en CI. | Reporte reproducible de `npm audit`, `npm audit --omit=dev` y `pip-audit`, política de severidades y tratamiento documentado de hallazgos. | Por confirmar |
| Obtener peer review y desplegar a staging mediante pipeline real. | PR aprobado por un par y ejecución de staging exitosa enlazada al Sprint 3. | Por confirmar |
| Realizar Sprint Review y retrospectiva con el equipo. | Acta con fecha, participantes, feedback, decisiones, responsables y aceptación/rechazo de cada historia. | Por confirmar |
\n+[← Volver al README principal](../../../README.md)
