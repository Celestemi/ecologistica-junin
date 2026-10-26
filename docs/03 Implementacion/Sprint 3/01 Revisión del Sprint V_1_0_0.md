# Revisión del sprint

**Versión documental:** V_1_0_0

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

## Historias de Usuario completadas en este Sprint

La revisión se basa en el backlog oficial, el código vigente y una ejecución local del 26 de octubre de 2026: **118 pruebas backend aprobadas**, **6 pruebas frontend aprobadas** y **build de producción aprobado**. La cobertura backend obtenida fue **75%**, inferior al 80% exigido por la Definition of Done (DoD). SonarQube registra Quality Gate `PASSED` para código nuevo, pero conserva una incidencia bloqueante de fiabilidad, tres críticas, diez vulnerabilidades de severidad media/baja y cobertura global importada de 61.2%. Tampoco existe evidencia de peer review aprobado ni de despliegue automatizado exitoso en staging.

En consecuencia, **ninguna historia US-010 a US-015 ni EN-004 se declara completada en sentido Done**. La tabla detalla la implementación realmente disponible y las brechas que impiden cerrar cada elemento.

| ID | Objetivo y criterios de aceptación | Evidencia de implementación y validación | Estado real respecto de la DoD |
|---|---|---|---|
| **US-010 — Visualización de rutas en mapa interactivo** | Mostrar trazas y paradas por vehículo con colores diferenciados; al seleccionar un vehículo, destacar su ruta y atenuar las demás. | `Map.tsx` renderiza GeoJSON con Leaflet, polilíneas, marcadores y colores por matrícula; `App.tsx` ofrece filtros por vehículo. La API protegida `/api/v1/rutas/mapa` se prueba en `test_api.py`. La aplicación renderizada fue inspeccionada en `localhost:8080`. El filtro actual oculta las rutas no seleccionadas en vez de atenuarlas, y no hay prueba de componente que verifique la interacción completa. | **Parcial; no completada.** Implementación principal presente, pero un criterio visual no coincide literalmente y falta validación UI automatizada; DoD global incumplida. |
| **US-011 — Consulta de detalle por parada** | Al seleccionar una parada, mostrar cliente, dirección, ventana, ETA y carga; actualizar el detalle al cambiar de parada sin recargar el mapa. | El GeoJSON incluye cliente, dirección, peso, secuencia y ETA; `Map.tsx` actualiza la selección y `StopDetail` presenta los campos requeridos. `test_api.py` verifica los datos reales publicados y `routePresentation.test.ts` verifica orden y detalle. Durante la revisión de accesibilidad no había una solución publicada, por lo que no se reprodujo el flujo completo marcador-detalle en pantalla. | **Parcial; no completada.** Contrato y componentes implementados, pero falta evidencia dinámica integral y la DoD global no se cumple. |
| **US-012 — Vista resiliente tabular** | Activar automáticamente una tabla ordenada ante fallo cartográfico y permitir reintentar el mapa conservando el estado. | `App.tsx` cambia a `RouteTable` por `tileerror`, ofrece “Vista tabular” y “Reintentar mapa”; la tabla incluye orden, vehículo, cliente, dirección, ETA, ventana y carga. `routePresentation.test.ts` demuestra que los puntos se ordenan y que la tabla puede existir sin geometría de línea. No se ejecutó una prueba automatizada de fallo/restablecimiento de tiles; además, las filas seleccionables no son operables por teclado, según la revisión WCAG. | **Parcial; no completada.** Fallback implementado, con pruebas unitarias de presentación, pero faltan prueba end-to-end y corrección de accesibilidad; DoD global incumplida. |
| **US-013 — Consolidado de KPIs operativos y ambientales** | Mostrar distancia, consumo en litros y emisiones de CO₂; informar correctamente cuando no hay datos. | `operational_indicators.py`, `/api/v1/indicadores` y `Dashboard.tsx` consolidan distancia, duración, consumo, CO₂ emitido/evitado y periodo sin registros. `test_operational_indicators.py` y `test_api.py` validan cálculos e integración. El consumo se calcula y muestra en **galones**, mientras el criterio oficial pide **litros**. | **Parcial; no completada.** Cálculo y dashboard presentes, pero existe discrepancia de unidad y faltan pruebas UI; DoD global incumplida. |
| **US-014 — Comparación contra línea base** | Calcular ahorro porcentual en distancia y CO₂ frente a línea base secuencial; resaltar si alcanza ≥15% y ≥10%; no inventar porcentajes sin base comparable. | El solver persiste las líneas base y metas; el servicio calcula porcentajes y el dashboard muestra comparación o mensaje de falta de base. Las pruebas verifican los porcentajes y el caso no comparable. El dashboard no presenta un resaltado explícito de cumplimiento de las dos metas, aunque el backend calcula los indicadores booleanos. | **Parcial; no completada.** Cálculo y manejo de ausencia acreditados; falta la señalización visual exigida y la DoD global. |
| **US-015 — Árboles equivalentes** | Convertir CO₂ evitado a árboles equivalentes mediante un factor configurable y recalcular al cambiar el factor. | El backend usa `quinual_kg_co2_per_year`, persiste el resultado y la API/dashboard muestran una equivalencia referencial en Quinuales, aclarando que no representa árboles plantados. Las pruebas validan CO₂ evitado dividido entre el factor de 12 kg/año. No hay una prueba específica que cambie el factor y demuestre el recálculo dinámico completo. | **Parcial; no completada.** Camino principal probado; falta prueba del cambio de factor y cumplimiento DoD global. |
| **EN-004 — Persistencia offline y sincronización PWA/IndexedDB** | Guardar entregas offline con marca temporal y sincronizarlas al recuperar red sin duplicados. | `offline.ts` implementa IndexedDB por usuario, cola pendiente y registros completados; `DriverApp.tsx` cachea ruta/flota, encola entregas y sincroniza al evento `online`; `sw.js` registra shell y Background Sync; el envío usa `Idempotency-Key` y el backend trata la confirmación como idempotente. Existen manifest y registro del Service Worker. No hay pruebas automatizadas dedicadas de IndexedDB, desconexión/reconexión, Background Sync ni duplicidad extremo a extremo; el manifest no declara iconos. SonarQube reporta cuatro smells en el manejo de rechazos de `offline.ts`. | **Parcial; no completada.** Arquitectura implementada, pero los dos escenarios de aceptación no están acreditados de extremo a extremo y la DoD global no se cumple. |

Estado de los cinco criterios DoD globales aplicables a todas las historias:

| Criterio DoD | Evidencia actual | Resultado |
|---|---|---|
| Cobertura automática backend y frontend ≥80% | Backend 75% en la ejecución actual; SonarQube importó 61.2% global. Las seis pruebas frontend no cubren todos los componentes Sprint 3. | **No cumple** |
| Análisis estático sin vulnerabilidades críticas/altas ni deuda bloqueante | SonarQube ejecutado; 0 hotspots y sin vulnerabilidad crítica/alta, pero conserva un hallazgo bloqueante de fiabilidad y tres críticos, además de diez vulnerabilidades medias/bajas. | **No cumple** |
| Peer review aprobado | No se encontró PR o aprobación de un par técnico asociada al Sprint 3. | **No acreditado** |
| Pipeline y despliegue automatizado exitoso en staging | Existe workflow; el job de staging es un placeholder manual y no hay ejecución de despliegue acreditada. | **No cumple** |
| OpenAPI/docstrings actualizados | `/openapi.json` está operativo y el endpoint de indicadores está documentado; hay docstrings en servicios, aunque no se auditó su cobertura total. | **Parcial** |

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

## Pendientes

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
\n+[← Volver al README principal](../../../README.md)
