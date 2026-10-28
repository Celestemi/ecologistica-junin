# Revisión del sprint

**Versión documental:** V_1_0_0

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

## Historias de Usuario completadas en este Sprint

### Evidencia del sprint

La evaluación posterior se ejecutó en una pila Docker aislada, con datos de prueba desechables y sin modificar datos reales. Se obtuvieron **143 pruebas backend aprobadas** (cobertura total informada por `pytest-cov`: **76%**), **68 pruebas frontend aprobadas** y build de producción aprobado. `npm audit`, `npm audit --omit=dev` y `pip-audit --strict` no informaron vulnerabilidades conocidas en los manifiestos evaluados.

La validación dinámica de la ruta aislada verificó tabla, selección por teclado y detalle: había cinco paradas disponibles como botones nativos y `Enter` mostró el detalle de la parada seleccionada. La recuperación automática tras un fallo de tiles, el flujo marcador Leaflet–detalle y el ciclo offline/reconexión de EN-004 siguen sin evidencia extremo a extremo. Las pruebas de accesibilidad también confirmaron foco contenido y restaurado en el diálogo de firma; quedan dos objetivos con contraste insuficiente y una región desplazable sin foco en operador.

Lighthouse 13.5.0 informó 100/100 de accesibilidad en ingreso, seguimiento, operador y conductor bajo los recorridos aislados; axe-core encontró 0 violaciones en ingreso, seguimiento y conductor, y 2 tipos de violación en operador (3 nodos). Estos resultados automáticos son evidencia de esos recorridos, no una declaración de conformidad WCAG. Además, el escaneo final de SonarQube Community Build 26.10.0.133078 del sprint terminó en `SUCCESS` con Quality Gate `OK`/PASSED: procesó 125 archivos, importó cobertura Python y LCOV, y reportó 82.1% de cobertura global, 82.0% en código nuevo y 0.0% de duplicación. El gate no cierra las incidencias históricas: permanecen 16 bugs, 10 vulnerabilidades y 4 code smells; tampoco sustituye el SCA de dependencias.

### Consolidación de la revisión

La revisión se basa en el backlog oficial, el código vigente y las ejecuciones locales verificadas del sprint. La evaluación aislada más reciente aprobó **143 pruebas backend** y **68 frontend**; el escaneo SonarQube que generó los reportes de cobertura aprobó **136 pruebas backend** y **67 frontend**, importó ambos reportes y obtuvo **82.1% de cobertura global**. La diferencia entre conteos corresponde a ejecuciones distintas; no se deben mezclar para inferir una cobertura individual de backend. La ejecución aislada de `pytest-cov` registró 76% para backend, inferior al 80% exigido por la Definition of Done (DoD). Aunque el Quality Gate de código nuevo pasó, persisten 1 bug bloqueante, 3 bugs críticos, 12 bugs mayores, 10 vulnerabilidades y 4 code smells. Tampoco existe evidencia de peer review aprobado ni de despliegue automatizado exitoso en staging.

En consecuencia, **ninguna historia US-010 a US-015 ni EN-004 se declara completada en sentido Done**. La tabla detalla la implementación realmente disponible y las brechas que impiden cerrar cada elemento.

| ID | Objetivo y criterios de aceptación | Evidencia de implementación y validación | Estado real respecto de la DoD |
|---|---|---|---|
| **US-010 — Visualización de rutas en mapa interactivo** | Mostrar trazas y paradas por vehículo con colores diferenciados; al seleccionar un vehículo, destacar su ruta y atenuar las demás. | `Map.tsx` renderiza GeoJSON con Leaflet, polilíneas, marcadores y colores por matrícula; `App.tsx` ofrece filtros por vehículo. La API protegida `/api/v1/rutas/mapa` se prueba en `test_api.py`. La aplicación renderizada fue inspeccionada en `localhost:8080`. El filtro actual oculta las rutas no seleccionadas en vez de atenuarlas, y no hay prueba de componente que verifique la interacción completa. | **Parcial; no completada.** Implementación principal presente, pero un criterio visual no coincide literalmente y falta validación UI automatizada; DoD global incumplida. |
| **US-011 — Consulta de detalle por parada** | Al seleccionar una parada, mostrar cliente, dirección, ventana, ETA y carga; actualizar el detalle al cambiar de parada sin recargar el mapa. | El GeoJSON incluye cliente, dirección, peso, secuencia y ETA; `Map.tsx` actualiza la selección y `StopDetail` presenta los campos requeridos. `test_api.py` verifica los datos reales publicados y `routePresentation.test.ts` verifica orden y detalle. Durante la revisión de accesibilidad no había una solución publicada, por lo que no se reprodujo el flujo completo marcador-detalle en pantalla. | **Parcial; no completada.** Contrato y componentes implementados, pero falta evidencia dinámica integral y la DoD global no se cumple. |
| **US-012 — Vista resiliente tabular** | Activar automáticamente una tabla ordenada ante fallo cartográfico y permitir reintentar el mapa conservando el estado. | `App.tsx` cambia a `RouteTable` por `tileerror`, ofrece “Vista tabular” y “Reintentar mapa”; la tabla incluye orden, vehículo, cliente, dirección, ETA, ventana y carga. La evaluación aislada del sprint verificó cinco paradas como botones nativos y la apertura del detalle mediante `Enter`. No se ejecutó una prueba automatizada de fallo/restablecimiento de tiles. | **Parcial; no completada.** Se corrigió y verificó la operación por teclado; aún falta la evidencia end-to-end de recuperación de tiles y la DoD global. |
| **US-013 — Consolidado de KPIs operativos y ambientales** | Mostrar distancia, consumo en litros y emisiones de CO₂; informar correctamente cuando no hay datos. | `operational_indicators.py`, `/api/v1/indicadores` y `Dashboard.tsx` consolidan distancia, duración, consumo, CO₂ emitido/evitado y periodo sin registros. `test_operational_indicators.py` y `test_api.py` validan cálculos e integración. El consumo se calcula y muestra en **galones**, mientras el criterio oficial pide **litros**. | **Parcial; no completada.** Cálculo y dashboard presentes, pero existe discrepancia de unidad y faltan pruebas UI; DoD global incumplida. |
| **US-014 — Comparación contra línea base** | Calcular ahorro porcentual en distancia y CO₂ frente a línea base secuencial; resaltar si alcanza ≥15% y ≥10%; no inventar porcentajes sin base comparable. | El solver persiste las líneas base y metas; el servicio calcula porcentajes y el dashboard muestra comparación o mensaje de falta de base. Las pruebas verifican los porcentajes y el caso no comparable. El dashboard no presenta un resaltado explícito de cumplimiento de las dos metas, aunque el backend calcula los indicadores booleanos. | **Parcial; no completada.** Cálculo y manejo de ausencia acreditados; falta la señalización visual exigida y la DoD global. |
| **US-015 — Árboles equivalentes** | Convertir CO₂ evitado a árboles equivalentes mediante un factor configurable y recalcular al cambiar el factor. | El backend usa `quinual_kg_co2_per_year`, persiste el resultado y la API/dashboard muestran una equivalencia referencial en Quinuales, aclarando que no representa árboles plantados. Las pruebas validan CO₂ evitado dividido entre el factor de 12 kg/año. No hay una prueba específica que cambie el factor y demuestre el recálculo dinámico completo. | **Parcial; no completada.** Camino principal probado; falta prueba del cambio de factor y cumplimiento DoD global. |
| **EN-004 — Persistencia offline y sincronización PWA/IndexedDB** | Guardar entregas offline con marca temporal y sincronizarlas al recuperar red sin duplicados. | `offline.ts` implementa IndexedDB por usuario, cola pendiente y registros completados; `DriverApp.tsx` cachea ruta/flota, encola entregas y sincroniza al evento `online`; `sw.js` registra shell y Background Sync; el envío usa `Idempotency-Key` y el backend trata la confirmación como idempotente. Existen manifest y registro del Service Worker. No hay pruebas automatizadas dedicadas de IndexedDB, desconexión/reconexión, Background Sync ni duplicidad extremo a extremo; el manifest no declara iconos. SonarQube reporta cuatro smells en el manejo de rechazos de `offline.ts`. | **Parcial; no completada.** Arquitectura implementada, pero los dos escenarios de aceptación no están acreditados de extremo a extremo y la DoD global no se cumple. |

Estado de los cinco criterios DoD globales aplicables a todas las historias:

| Criterio DoD | Evidencia actual | Resultado |
|---|---|---|
| Cobertura automática backend y frontend ≥80% | SonarQube importó 82.1% global, 85.4% de líneas, 69.7% de ramas y 82.0% en código nuevo; Vitest aportó 90.91% de líneas frontend. La ejecución aislada de backend obtuvo 76%, por debajo del umbral, y no hay evidencia homogénea que acredite ≥80% en ambas capas. | **No cumple** |
| Análisis estático sin vulnerabilidades críticas/altas ni deuda bloqueante | SonarQube finalizó `SUCCESS` con Quality Gate `OK` para código nuevo, pero conserva 1 bug bloqueante, 3 críticos, 12 mayores, 10 vulnerabilidades (9 mayores y 1 menor) y 4 code smells. | **No cumple** |
| Peer review aprobado | No se encontró PR o aprobación de un par técnico asociada al Sprint 3. | **No acreditado** |
| Pipeline y despliegue automatizado exitoso en staging | Existe workflow; el job de staging es un placeholder manual y no hay ejecución de despliegue acreditada. | **No cumple** |
| OpenAPI/docstrings actualizados | `/openapi.json` está operativo y el endpoint de indicadores está documentado; hay docstrings en servicios, aunque no se auditó su cobertura total. | **Parcial** |

### Estado vigente de la DoD — evidencia del sprint

| Criterio DoD | Evidencia posterior | Resultado |
|---|---|---|
| Cobertura automática backend y frontend ≥80% | La ejecución aislada registró 143 pruebas backend y 76% de cobertura backend, además de 68 pruebas frontend. El escaneo SonarQube importó una medición distinta con 82.1% global y 90.91% de líneas frontend. El backend aislado sigue bajo el 80%, por lo que no se acredita el umbral por capa. | **No cumple** |
| Análisis estático y dependencias | `npm audit`, `npm audit --omit=dev` y `pip-audit --strict` no informaron vulnerabilidades conocidas. El escaneo SonarQube final del sprint obtuvo Quality Gate `OK`, pero mantiene 16 bugs (incluido 1 bloqueante), 10 vulnerabilidades y 4 code smells; el análisis SCA de SonarQube no estuvo disponible. | **No cumple** |
| Peer review aprobado | No se aportó nueva evidencia de aprobación de un par técnico. | **No acreditado** |
| Pipeline y despliegue automatizado exitoso en staging | La pila de evaluación fue local y aislada; no se ejecutó ni acreditó despliegue a staging. | **No cumple** |
| OpenAPI/docstrings actualizados | No se modificó ni auditó de nuevo de forma exhaustiva en esta evaluación. | **Parcial** |

## Demostración del trabajo completado

No se encontró acta, grabación, lista de asistentes, aceptación de stakeholders ni otra evidencia de una demostración de Sprint 3 ya realizada. Por ello, lo siguiente es un **guion de demostración pendiente**, no el registro de una sesión efectuada:

1. **Preparación controlada:** iniciar Docker, confirmar salud de frontend/backend/PostGIS y acceder con una cuenta de demostración autorizada. Usar una jornada y pedidos desechables preparados para la demostración.
2. **Mapa de rutas optimizadas:** ejecutar la optimización con el rol permitido; comprobar trazas, marcadores y colores por vehículo. Seleccionar cada matrícula y registrar la diferencia entre ocultar rutas y el criterio pendiente de atenuarlas.
3. **Detalle de paradas:** seleccionar dos paradas consecutivas y comprobar que cliente, dirección, ventana, ETA y carga cambian sin recarga completa.
4. **Vista tabular:** abrirla manualmente; después simular de forma controlada la indisponibilidad de tiles y verificar activación automática, orden de paradas, conservación del detalle y retorno mediante “Reintentar mapa”.
5. **KPIs operativos y ambientales:** consultar un periodo con rutas y otro vacío; mostrar distancia, duración, consumo, CO₂ emitido y evitado. Señalar que la unidad actual es galón y no el litro pedido por US-013.
6. **Comparación con línea base:** presentar porcentajes de distancia y CO₂; demostrar el mensaje cuando no existe base comparable. Señalar como pendiente el resaltado visual de las metas de 15% y 10%.
7. **Árboles equivalentes:** mostrar la equivalencia referencial en Quinuales, el factor utilizado y la advertencia de que no son árboles plantados; preparar una prueba separada del cambio de factor.
8. **Offline y sincronización:** en un perfil de navegador desechable, cargar la ruta del conductor, cortar red, registrar una entrega, verificar IndexedDB y la cola visible, recuperar conectividad y comprobar una sola confirmación en backend pese a reintentos.
9. **Cierre:** presentar resultados de pruebas, SonarQube, OWASP y WCAG, junto con las brechas que impiden declarar Done; solicitar aceptación o decisiones explícitas y documentarlas.

## Pendientes identificados en la revisión inicial

- Corregir US-010 para atenuar rutas no seleccionadas o acordar formalmente que filtrarlas satisface el criterio; añadir prueba de interacción del mapa.
- Ejecutar y archivar una validación dinámica marcador-detalle para US-011 con una ruta de prueba publicada.
- Probar US-012 extremo a extremo ante fallo y recuperación real/simulada de tiles; hacer seleccionables las filas de la tabla mediante teclado.
- Alinear US-013 con la unidad oficial en litros o aprobar y documentar el cambio del backlog a galones; cubrir dashboard y periodo vacío en pruebas frontend.
- Mostrar explícitamente en US-014 si se alcanzan las metas de ahorro, reutilizando los indicadores calculados por backend.
- Probar US-015 cambiando el factor configurable y verificando el recálculo en API y UI.
- Añadir pruebas de EN-004 para IndexedDB, modo offline, reconexión, reintentos e idempotencia extremo a extremo; completar requisitos de instalabilidad PWA y normalizar rechazos a objetos `Error`.
- Elevar cobertura backend y frontend al umbral DoD ≥80% o aprobar formalmente un cambio de DoD; conservar los reportes reproducibles.
- Resolver o clasificar justificadamente las incidencias SonarQube, repetir el análisis y verificar el criterio de deuda bloqueante.
- Acreditar un PR con peer review y una ejecución real del pipeline con despliegue exitoso a staging.
- Corregir los incumplimientos WCAG confirmados: contraste, landmark principal, nombres accesibles del mapa, teclado en tabla y anuncios de estado; repetir Lighthouse/axe y pruebas manuales.
- Realizar y registrar la Sprint Review con stakeholders. Los participantes, fecha, resultado y aceptación siguen pendientes de confirmación.

Las exportaciones, reoptimización y procesamiento asíncrono correspondientes a US-016 a US-018 y EN-002 pertenecen al Sprint 4 y no se registran como pendientes del Sprint 3.

## Pendientes vigentes tras la evaluación del sprint

- Validar extremo a extremo la recuperación de tiles y el flujo marcador Leaflet–detalle con una ruta de prueba publicada.
- Corregir en operador los dos objetivos de contraste insuficiente y hacer focalizable la región desplazable; completar validaciones manuales con lector de pantalla, reflow a 320 CSS px y zoom 200%/400% en todos los flujos.
- Ejecutar pruebas extremo a extremo de EN-004: IndexedDB, desconexión, reconexión, Background Sync e idempotencia.
- Elevar la cobertura backend y frontend al 80% exigido por la DoD o aprobar formalmente el cambio de dicho umbral.
- Resolver o clasificar en SonarQube los 16 bugs, 10 vulnerabilidades y 4 code smells del escaneo final; conservar el escaneo reproducible y no tratar el Quality Gate de código nuevo como cierre de la DoD.
- Acreditar peer review, pipeline y despliegue real en staging; realizar y registrar la Sprint Review con stakeholders.
\n+[← Volver al README principal](../../../README.md)
