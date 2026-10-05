# 01. Transformando a Ágil V_1_0_0.md
**Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Ámbito:** Huancayo, El Tambo y Chilca (Provincia de Huancayo, Junín)  
**Versión:** V_1_0_0  
**Fecha:** 15 de septiembre de 2026  

---

## 1. Metodología de Transformación Ágil

El presente documento establece la transformación de la línea base de requisitos del proyecto **EcoLogística Huancayo** (versión V_1_0_3) hacia un backlog de trabajo ágil estructurado en **Épicas**, **Historias de Usuario (US)** y **Historias Técnicas / Habilitadores (Enablers)**.

### A. Mapeo Jerárquico de Requisitos Funcionales (RF)
* **Macro-Requisitos Funcionales (MRF-01 a MRF-07)**: Se transforman directamente en **Épicas (EP-01 a EP-07)**, representando los grandes contenedores de valor del negocio.
* **Requisitos Funcionales Atómicos (RF-001 a RF-018)**: Se descomponen en **Historias de Usuario (US-001 a US-018)** alineadas a la plantilla canónica, asegurando que cada funcionalidad entregue un beneficio directo al negocio o al usuario final.

### B. Mapeo de Requisitos No Funcionales (RNF)
* **Escenarios de Calidad (RNF-001 a RNF-005)**: Se transforman en **Historias Técnicas o Habilitadores (EN-001 a EN-005)** enfocado en la infraestructura, arquitectura, rendimiento, resiliencia offline y seguridad (OWASP / Ley N° 29733).
* **Restricciones Transversales**: Determinados atributos de calidad se integran directamente como **Criterios de Aceptación (Gherkin)** dentro de las US operativas o como reglas globales en la **Definition of Done (DoD)**.

---

## 2. Definition of Done (DoD) Global del Proyecto

Para que cualquier Historia de Usuario (US) o Enabler (EN) sea considerado finalizado (**Done**) y listo para su entrega en las iteraciones del proyecto, debe cumplir de manera estricta y no ambigua los siguientes criterios de calidad técnica:

1. **Pruebas Unitarias**: Cobertura de pruebas unitarias automáticas $\ge 80\%$ en el código backend (FastAPI / OR-Tools) y frontend (React / PWA).
2. **Análisis Estático de Código**: Ejecución de análisis estático (SonarQube / CodeQL) con **0 vulnerabilidades críticas o altas** y 0 deuda técnica bloqueante.
3. **Revisión de Código (Peer Review)**: Pull Request (PR) revisado y aprobado por al menos un par técnico antes de la integración a la rama principal (`main`/`develop`).
4. **Integración y Despliegue Continuo (CI/CD)**: Despliegue automatizado exitoso ejecutable mediante pipeline en el ambiente de **Staging / Pruebas**.
5. **Documentación Técnica**: Documentación de API actualizada automáticamente en OpenAPI / Swagger (`/docs` en FastAPI) y código debidamente comentado mediante docstrings.

---

## 3. Catálogo de Épicas, Historias de Usuario (US) y Enablers

---

### ÉPICA EP-01: Gestión de Flota Vehicular
**MRF Relacionado:** MRF-01 Gestión de Flota Vehicular

#### ID: US-001
* **Título:** Registro y mantenimiento de vehículos de la flota
* **Épica Relacionada:** EP-01 Gestión de Flota Vehicular
* **Requisito Trazado:** RF-001
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** registrar, editar e inactivar los vehículos de la flota indicando placa, modelo, capacidad (kg/m³), tipo de combustible, rendimiento y factor de emisión,
  * **para** mantener actualizada la disponibilidad y características operativas de la flota en el sistema.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Registro exitoso de un nuevo vehículo
    * **Dado** que el Operador de Logística autenticado ingresa los datos completos de un vehículo nuevo con placa no existente,
    * **Cuando** confirma el registro con capacidad, tipo de combustible (Diésel, Gasolina, GNV) y rendimiento,
    * **Entonces** el sistema debe guardar el vehículo en la base de datos con estado **Activo** y mostrarlo en el catálogo de flota.
  * **Escenario 2 (Ruta Infeliz):** Intento de registro con placa duplicada
    * **Dado** que ya existe un vehículo registrado con la placa `W1A-802`,
    * **Cuando** el Operador intenta registrar un nuevo vehículo utilizando la misma placa `W1A-802`,
    * **Entonces** el sistema debe rechazar la operación, mostrar un mensaje de error notificando la duplicidad y evitar la duplicación del registro.

---

#### ID: US-002
* **Título:** Configuración de restricciones de circulación por placa
* **Épica Relacionada:** EP-01 Gestión de Flota Vehicular
* **Requisito Trazado:** RF-002 / RN-002
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** configurar y aplicar reglas de restricción de circulación asociadas al último dígito de la placa,
  * **para** evitar asignar vehículos a rutas en días con restricciones normativas en Huancayo, El Tambo y Chilca.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Exclusión automática de vehículos restringidos
    * **Dado** que existe una regla de circulación por placa validada y activa para el día seleccionado,
    * **Cuando** el Operador genera la planificación de rutas para esa fecha,
    * **Entonces** el sistema debe excluir automáticamente de la asignación a los vehículos afectados por la restricción de placa.
  * **Escenario 2 (Ruta Infeliz):** Aplicación de regla pendiente de validación
    * **Dado** que la regla de restricción vehicular figura etiquetada como `[PENDIENTE DE VALIDACIÓN NORMATIVA]`,
    * **Cuando** el Operador intenta activar la regla sin la validación legal confirmada,
    * **Entonces** el sistema debe mantener la regla desactivada por defecto e informar que requiere validación normativa previa.

---

#### ID: US-003
* **Título:** Historial y control del estado operativo del vehículo
* **Épica Relacionada:** EP-01 Gestión de Flota Vehicular
* **Requisito Trazado:** RF-003
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** actualizar el estado operativo del vehículo entre Activo, Mantenimiento e Inactivo,
  * **para** garantizar que solo los vehículos en óptimas condiciones sean considerados en la generación de rutas.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Cambio de estado a Mantenimiento
    * **Dado** que un vehículo se encuentra en estado **Activo**,
    * **Cuando** el Operador cambia su estado a **Mantenimiento** registrando la fecha del evento,
    * **Entonces** el sistema debe guardar el cambio en el historial y excluir el vehículo de las optimizaciones de ruta futuras.
  * **Escenario 2 (Ruta Infeliz):** Intento de asignación manual de vehículo Inactivo
    * **Dado** que un vehículo se encuentra registrado con estado **Inactivo**,
    * **Cuando** el Operador intenta asignarlo manualmente a una ruta planificada,
    * **Entonces** el sistema debe rechazar la asignación e informar que el vehículo no está disponible por estado inactivo.

---

### ÉPICA EP-02: Gestión de Pedidos y Puntos de Entrega
**MRF Relacionado:** MRF-02 Gestión de Pedidos y Puntos de Entrega

#### ID: US-004
* **Título:** Importación masiva de lotes de pedidos
* **Épica Relacionada:** EP-02 Gestión de Pedidos y Puntos de Entrega
* **Requisito Trazado:** RF-004 / RNF-003
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** importar lotes de hasta 150 pedidos mediante archivos estructurados en formato CSV o Excel,
  * **para** cargar de manera ágil los pedidos diarios a distribuirse en Huancayo, El Tambo y Chilca.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Importación exitosa de lote válido
    * **Dado** un archivo CSV/Excel estructurado correctamente con 150 pedidos y todos sus campos obligatorios completos,
    * **Cuando** el Operador ejecuta el proceso de importación masiva,
    * **Entonces** el sistema debe validar los campos, almacenar los 150 pedidos en la base de datos y mostrar el resumen de carga exitosa.
  * **Escenario 2 (Ruta Infeliz):** Rechazo de archivo por campos requeridos ausentes
    * **Dado** un archivo de importación que omite campos obligatorios como dirección o peso,
    * **Cuando** el Operador intenta realizar la importación masiva,
    * **Entonces** el sistema debe rechazar el archivo, indicar la fila y campo faltante, y no guardar ningún registro inconsistente.

---

#### ID: US-005
* **Título:** Geocodificación y ubicación espacial de pedidos
* **Épica Relacionada:** EP-02 Gestión de Pedidos y Puntos de Entrega
* **Requisito Trazado:** RF-005
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** que el sistema asocie coordenadas de latitud y longitud a cada pedido dentro de los distritos de Huancayo, El Tambo y Chilca,
  * **para** ubicar con precisión espacial cada punto de entrega sobre la cartografía GIS.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Geocodificación automática exitosa
    * **Dado** un pedido cargado con una dirección válida dentro del área urbana de Huancayo,
    * **Cuando** el servicio de geocodificación procesa la dirección,
    * **Entonces** el sistema debe asignar las coordenadas GPS en formato PostGIS `GEOGRAPHY(Point, 4326)` y ubicar el punto en el mapa.
  * **Escenario 2 (Ruta Infeliz):** Dirección fuera de cobertura o no ubicable
    * **Dado** un pedido cuya dirección se encuentra fuera de los límites distritales de Huancayo, El Tambo o Chilca,
    * **Cuando** el sistema intenta la geocodificación espacial,
    * **Entonces** debe marcar el pedido como **Pendiente de Validación** y bloquear su inclusión automática en la ruta hasta su corrección.

---

#### ID: US-006
* **Título:** Gestión de ventanas de tiempo de entrega
* **Épica Relacionada:** EP-02 Gestión de Pedidos y Puntos de Entrega
* **Requisito Trazado:** RF-006 / RN-005
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** registrar para cada pedido un intervalo de hora de inicio y hora de fin,
  * **para** que el motor de optimización garantice la entrega dentro del rango comprometido con el cliente.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Registro correcto de intervalo de entrega
    * **Dado** un pedido con una ventana de tiempo válida (ejemplo: `09:00 - 11:00`),
    * **Cuando** el Operador guarda la configuración del pedido,
    * **Entonces** el sistema debe almacenar el rango horario y marcarlo como restricción estricta para la planificación.
  * **Escenario 2 (Ruta Infeliz):** Rango horario inconsistente
    * **Dado** un pedido donde la hora de fin es anterior o igual a la hora de inicio (ejemplo: `14:00 - 11:00`),
    * **Cuando** el Operador intenta guardar el registro,
    * **Entonces** el sistema debe rechazar la operación notificando que la ventana de tiempo no es cronológicamente válida.

---

### ÉPICA EP-03: Motor de Optimización de Rutas
**MRF Relacionado:** MRF-03 Motor de Optimización de Rutas

#### ID: US-007
* **Título:** Generación de rutas sostenibles (VRPTW + Green VRP)
* **Épica Relacionada:** EP-03 Motor de Optimización de Rutas
* **Requisito Trazado:** RF-007 / RNF-001 / RN-008
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** solicitar la optimización de rutas mediante metaheurísticas considerando pedidos, capacidad, ventanas de tiempo y emisiones,
  * **para** obtener secuencias de entrega eficientes que reduzcan la distancia recorrida y las emisiones de CO₂.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Generación exitosa de rutas optimizadas
    * **Dado** un lote de hasta 150 pedidos válidos y una flota activa de 15 vehículos con capacidad suficiente,
    * **Cuando** el Operador solicita la generación de rutas sostenibles,
    * **Entonces** el motor (OR-Tools) debe devolver la solución respetando ventanas de tiempo y capacidades con un ahorro $\ge 15\%$ en distancia y $\ge 10\%$ en CO₂.
  * **Escenario 2 (Ruta Infeliz):** Infactibilidad por capacidad insuficiente
    * **Dado** un lote de pedidos cuya demanda combinada de peso o volumen supera la capacidad de toda la flota disponible,
    * **Cuando** el Operador ejecuta la optimización,
    * **Entonces** el sistema debe notificar que no existe solución factible y detallar el exceso de carga no asignable.

---

#### ID: US-008
* **Título:** Validación de restricciones duras de capacidad y jornada laboral
* **Épica Relacionada:** EP-03 Motor de Optimización de Rutas
* **Requisito Trazado:** RF-008 / RN-003 / RN-004
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** que el sistema impida generar rutas que excedan el 100% de la capacidad del vehículo o las 8 horas de jornada del conductor,
  * **para** garantizar la seguridad operativa y el cumplimiento de la normativa laboral.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Cumplimiento estricto de límites
    * **Dado** un conjunto de rutas calculadas por el motor,
    * **Cuando** se valida la asignación,
    * **Entonces** el sistema confirma que ningún vehículo supera el 100% de su peso/volumen y que el tiempo total de conducción es $\le 8$ horas.
  * **Escenario 2 (Ruta Infeliz):** Intento de asignación con exceso de jornada
    * **Dado** una propuesta de ruta calculada que requiere 8.5 horas continuas de trabajo para un conductor,
    * **Cuando** el validador de restricciones procesa la ruta,
    * **Entonces** el sistema debe rechazar la asignación por incumplimiento de jornada máxima (RN-003) y dividir la carga.

---

#### ID: US-009
* **Título:** Cálculo de secuencia de paradas y hora estimada de llegada (ETA)
* **Épica Relacionada:** EP-03 Motor de Optimización de Rutas
* **Requisito Trazado:** RF-009 / RN-005
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** calcular la secuencia exacta de paradas y el ETA preciso para cada punto de entrega,
  * **para** brindar información de seguimiento transparente al conductor y al cliente final.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Secuenciamiento y cálculo de ETA exitoso
    * **Dado** una ruta optimizada con 10 paradas asignadas a un vehículo,
    * **Cuando** el sistema finaliza la secuenciación,
    * **Entonces** debe generar el orden de visita (`1` a `10`) y calcular el ETA para cada cliente asegurando que caiga dentro de su ventana.
  * **Escenario 2 (Ruta Infeliz):** Inconsistencia por falta de matriz de tiempo/distancia
    * **Dado** un punto de entrega que carece de matriz de tiempo calculada desde el servidor OSRM local,
    * **Cuando** el sistema intenta calcular el ETA de esa parada,
    * **Entonces** debe advertir la inconsistencia, marcar la parada para revisión y no publicar un ETA erróneo.

---

### ÉPICA EP-04: Visualización Cartográfica Interactiva
**MRF Relacionado:** MRF-04 Visualización Cartográfica Interactiva

#### ID: US-010
* **Título:** Visualización de rutas en mapa interactivo
* **Épica Relacionada:** EP-04 Visualización Cartográfica Interactiva
* **Requisito Trazado:** RF-010 / RNF-005
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** visualizar en un mapa interactivo (Leaflet.js) las rutas de distribución diferenciadas por colores según vehículo,
  * **para** supervisar geográficamente la cobertura de despacho en Huancayo, El Tambo y Chilca.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Renderizado de rutas diferenciadas
    * **Dado** que existen rutas optimizadas para la jornada,
    * **Cuando** el Operador abre el módulo de visualización cartográfica,
    * **Entonces** el mapa debe cargar las trazas geográficas y puntos de entrega codificados por colores únicos por cada vehículo.
  * **Escenario 2 (Ruta Feliz):** Filtrado dinámico por vehículo
    * **Dado** que el mapa muestra múltiples rutas de la flota,
    * **Cuando** el Operador selecciona un vehículo específico en el panel lateral,
    * **Entonces** el mapa debe resaltar únicamente la ruta del vehículo seleccionado y atenuar el resto de trayectos.

---

#### ID: US-011
* **Título:** Consulta de detalle por parada en el mapa
* **Épica Relacionada:** EP-04 Visualización Cartográfica Interactiva
* **Requisito Trazado:** RF-011
* **Redacción:**
  * **Como** Conductor / Operador,
  * **quiero** hacer clic o pulsar en un marcador de entrega dentro del mapa para ver el detalle de la parada,
  * **para** conocer la razón social del cliente, ETA, ventana de tiempo y carga a entregar.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Despliegue de modal informativo por parada
    * **Dado** que las rutas se muestran activas en el mapa interactivo,
    * **Cuando** el usuario selecciona la parada N° 4,
    * **Entonces** el sistema debe desplegar una ventana flotante con el cliente, dirección, ventana pactada, ETA y peso/volumen asignado.
  * **Escenario 2 (Ruta Feliz):** Actualización dinámica al cambiar de parada
    * **Dado** que se encuentra abierto el detalle de la parada N° 4,
    * **Cuando** el usuario hace clic inmediatamente en la parada N° 5,
    * **Entonces** el panel debe actualizar los datos instantáneamente sin recargar el mapa completo.

---

#### ID: US-012
* **Título:** Vista resiliente tabular ante falla del servicio de mapas
* **Épica Relacionada:** EP-04 Visualización Cartográfica Interactiva
* **Requisito Trazado:** RF-012 / RNF-004
* **Redacción:**
  * **Como** Operador / Conductor,
  * **quiero** contar con una vista tabular estructurada de la secuencia de paradas cuando el mapa no esté disponible,
  * **para** mantener la continuidad de la operación de reparto sin interrupciones.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Activación de vista fallback por fallo cartográfico
    * **Dado** que el servicio de mapa (tiles/Leaflet) presenta indisponibilidad o falla de red,
    * **Cuando** el usuario intenta consultar la ruta asignada,
    * **Entonces** el sistema debe mostrar automáticamente la lista ordenada en formato de tabla con orden, cliente, dirección y ETA.
  * **Escenario 2 (Ruta Feliz):** Retorno a la vista gráfica tras restablecimiento
    * **Dado** que la vista tabular fallback se encuentra activa y el servicio cartográfico se restablece,
    * **Cuando** el usuario presiona el botón de reintentar vista gráfica,
    * **Entonces** el sistema debe volver a cargar el mapa interactivo manteniendo el estado de las paradas.

---

### ÉPICA EP-05: Dashboard e Indicadores de Sostenibilidad
**MRF Relacionado:** MRF-05 Dashboard e Indicadores de Sostenibilidad

#### ID: US-013
* **Título:** Consolidado de KPIs operativos y ambientales
* **Épica Relacionada:** EP-05 Dashboard e Indicadores de Sostenibilidad
* **Requisito Trazado:** RF-013 / RN-006
* **Redacción:**
  * **Como** Gerente de Operaciones,
  * **quiero** consultar un dashboard consolidado con los indicadores de distancia recorrida (km), consumo de combustible (L) y emisiones de CO₂ (kg),
  * **para** evaluar el desempeño operativo y ambiental de la flota de reparto.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Despliegue de métricas consolidadas
    * **Dado** que existen rutas procesadas en el periodo seleccionado,
    * **Cuando** el Gerente abre el Dashboard de Sostenibilidad,
    * **Entonces** el sistema debe calcular y mostrar los totales de km recorridos, litros de combustible consumidos y kg de CO₂ emitidos.
  * **Escenario 2 (Ruta Infeliz):** Periodo sin registros
    * **Dado** que se selecciona un rango de fechas sin rutas ejecutadas u optimizadas,
    * **Cuando** el Gerente consulta el dashboard,
    * **Entonces** el sistema debe informar la ausencia de datos para ese rango sin mostrar valores inventados o errores de división por cero.

---

#### ID: US-014
* **Título:** Comparación contra la línea base de ruteo
* **Épica Relacionada:** EP-05 Dashboard e Indicadores de Sostenibilidad
* **Requisito Trazado:** RF-014 / RN-008
* **Redacción:**
  * **Como** Gerente de Operaciones,
  * **quiero** visualizar el porcentaje de variación de distancia y CO₂ de las rutas optimizadas frente a la línea base secuencial,
  * **para** verificar si se cumple el objetivo estratégico de ahorro del $\ge 15\%$ en distancia y $\ge 10\%$ en CO₂.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Verificación de cumplimiento de ahorros
    * **Dado** una ruta optimizada y su correspondiente trazado en línea base secuencial,
    * **Cuando** el sistema procesa la comparación,
    * **Entonces** debe calcular los porcentajes de ahorro y resaltar visualmente si alcanzaron las metas ($\ge 15\%$ km y $\ge 10\%$ CO₂).
  * **Escenario 2 (Ruta Infeliz):** Inexistencia de línea base comparable
    * **Dado** que un conjunto de pedidos no cuenta con una simulación de línea base generada,
    * **Cuando** el Gerente intenta consultar la comparativa,
    * **Entonces** el sistema debe notificar que requiere ejecutar la simulación de línea base previa para habilitar los porcentajes.

---

#### ID: US-015
* **Título:** Indicador social de impacto ambiental (árboles equivalentes)
* **Épica Relacionada:** EP-05 Dashboard e Indicadores de Sostenibilidad
* **Requisito Trazado:** RF-015
* **Redacción:**
  * **Como** Gerente de Operaciones,
  * **quiero** visualizar la equivalencia del CO₂ evitado expresado en cantidad de árboles necesarios para absorber dicha huella,
  * **para** comunicar el impacto ecológico del proyecto en un lenguaje socialmente comprensible.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Cálculo y despliegue del indicador de árboles
    * **Dado** que el sistema ha calculado una reducción de 500 kg de CO₂ en un periodo,
    * **Cuando** el Gerente consulta la sección social del dashboard,
    * **Entonces** el sistema debe aplicar la equivalencia metodológica y mostrar el número equivalente de árboles ahorrados.
  * **Escenario 2 (Ruta Feliz):** Actualización dinámica de factor
    * **Dado** que se actualiza el factor oficial de absorción de CO₂ por árbol en la configuración,
    * **Cuando** se vuelve a renderizar el dashboard,
    * **Entonces** el valor de equivalencia de árboles debe recalcularse automáticamente con el nuevo parámetro.

---

### ÉPICA EP-06: Generación y Exportación de Reportes
**MRF Relacionado:** MRF-06 Generación y Exportación de Reportes

#### ID: US-016
* **Título:** Exportación de hoja de ruta en formato PDF
* **Épica Relacionada:** EP-06 Generación y Exportación de Reportes
* **Requisito Trazado:** RF-016
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** exportar la hoja de ruta en formato PDF con los datos del vehículo, conductor, secuencia de paradas y espacio para firma de conformidad,
  * **para** entregar un manifiesto impreso o digital de respaldo al conductor antes del despacho.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Generación de PDF completo
    * **Dado** una ruta programada con vehículo y conductor asignados,
    * **Cuando** el Operador presiona el botón "Exportar Hoja de Ruta PDF",
    * **Entonces** el sistema debe generar un documento PDF maquetado con la lista de clientes, direcciones, ETAs y recuadro de firma.
  * **Escenario 2 (Ruta Infeliz):** Intento de exportación de ruta incompleta
    * **Dado** una ruta que carece de conductor asignado,
    * **Cuando** el Operador solicita la exportación en PDF,
    * **Entonces** el sistema debe impedir la descarga e informar que se requiere completar la asignación del conductor.

---

#### ID: US-017
* **Título:** Exportación auditable de datos operativos en CSV
* **Épica Relacionada:** EP-06 Generación y Exportación de Reportes
* **Requisito Trazado:** RF-017 / RNF-003
* **Redacción:**
  * **Como** Auditor Académico / Operador,
  * **quiero** exportar los registros de distancia, combustible consumido y emisiones calculadas en formato CSV,
  * **para** auditar externamente los datos de la operación y respaldar la trazabilidad del sistema.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Exportación en CSV con filtros aplicados
    * **Dado** que existen rutas registradas para un rango de fechas seleccionado,
    * **Cuando** el usuario solicita la exportación en CSV,
    * **Entonces** el sistema genera un archivo CSV estandarizado delimitado por comas con todos los atributos auditables.
  * **Escenario 2 (Ruta Infeliz):** Solicitud de exportación sin resultados
    * **Dado** que se aplican filtros de consulta que no retornan ningún registro,
    * **Cuando** el usuario intenta exportar en CSV,
    * **Entonces** el sistema notifica que no existen datos para exportar y evita generar un archivo vacío.

---

### ÉPICA EP-07: Re-optimización Dinámica ante Incidentes
**MRF Relacionado:** MRF-07 Re-optimización Dinámica ante Incidentes

#### ID: US-018
* **Título:** Re-optimización de rutas ante incidentes en vía
* **Épica Relacionada:** EP-07 Re-optimización Dinámica ante Incidentes
* **Requisito Trazado:** RF-018 / RNF-002 / RN-007
* **Redacción:**
  * **Como** Operador de Logística,
  * **quiero** ejecutar la re-optimización dinámica de rutas ante imprevistos (avería, bloqueo o cancelación),
  * **para** reasignar los pedidos pendientes a otros vehículos de la flota sin modificar las entregas que ya fueron completadas.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1 (Ruta Gold):** Reasignación exitosa respetando historial
    * **Dado** una ruta en ejecución con 3 entregas completadas y 5 pendientes donde el vehículo sufre una avería,
    * **Cuando** el Operador registra el incidente y solicita la re-optimización,
    * **Entonces** el sistema debe congelar las 3 entregas completadas y redistribuir los 5 pedidos pendientes entre los vehículos activos cercanos, priorizando los que vencen en $<2$ horas (RN-007).
  * **Escenario 2 (Ruta Infeliz):** Capacidad de flota restante insuficiente
    * **Dado** un incidente que inhabilita un vehículo y los vehículos restantes están al 100% de capacidad,
    * **Cuando** se ejecuta la re-optimización,
    * **Entonces** el sistema debe notificar la imposibilidad de reasignar el 100% de los pedidos e indicar cuáles quedan en cola de excepción.

---

## 4. Historias Técnicas / Habilitadores (Enablers)

---

#### ID: EN-001
* **Título:** Optimización del motor de ruteo para SLA de generación $\le 45$ segundos
* **Tipo:** Rendimiento / Algoritmo
* **Requisito Trazado:** RNF-001 / RF-007
* **Redacción:**
  * **Como** Arquitecto de Software,
  * **quiero** tuning y optimización en las metaheurísticas de Google OR-Tools en Python 3.11,
  * **para** garantizar la generación de rutas válidas en $\le 45$ segundos para escenarios de hasta 150 pedidos y 15 vehículos.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1:** Prueba de carga con 150 pedidos y 15 vehículos
    * **Dado** un escenario de prueba automatizado con 150 pedidos y 15 vehículos en Huancayo,
    * **Cuando** se ejecuta la llamada a la API de optimización,
    * **Entonces** el motor debe procesar la solución completa en un tiempo total de respuesta $T \le 45.0$ segundos.
  * **Escenario 2:** Control de Timeout
    * **Dado** que un cálculo de ruta excede los 45 segundos por complejidad,
    * **Cuando** se alcance el umbral de tiempo límite,
    * **Entonces** el sistema debe retornar la mejor solución factible encontrada hasta ese momento sin colapsar el servicio.

---

#### ID: EN-002
* **Título:** Servicio de procesamiento asíncrono para re-optimización en $\le 30$ segundos
* **Tipo:** Rendimiento / Arquitectura
* **Requisito Trazado:** RNF-002 / RF-018
* **Redacción:**
  * **Como** Desarrollador Backend,
  * **quiero** implementar tareas asíncronas utilizando Celery y Redis,
  * **para** resolver peticiones de re-optimización por incidentes en $\le 30$ segundos sin bloquear la interfaz de usuario.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1:** Re-optimización asíncrona dentro del SLA
    * **Dado** un incidente registrado en una ruta activa,
    * **Cuando** el backend dispara la tarea asíncrona en Celery,
    * **Entonces** el recálculo debe completarse y retornar la nueva secuencia en $\le 30.0$ segundos.
  * **Escenario 2:** Respuesta inmediata de recepción de tarea
    * **Dado** la solicitud de re-optimización por parte del operador,
    * **Cuando** se envía la petición HTTP al endpoint de FastAPI,
    * **Entonces** la API debe responder en $< 1$ segundo con el ID de tarea asíncrona para monitoreo en segundo plano.

---

#### ID: EN-003
* **Título:** Implementación de seguridad transversal, cifrado y alineación OWASP / Ley 29733
* **Tipo:** Seguridad / Cumplimiento
* **Requisito Trazado:** RNF-003 / Ley N° 29733
* **Redacción:**
  * **Como** Oficial de Seguridad de TI,
  * **quiero** implementar cifrado TLS 1.3 en tránsito, hash bcrypt para contraseñas y middleware de autenticación JWT,
  * **para** garantizar la protección de datos personales de clientes y conductores protegiendo el sistema contra el OWASP Top 10.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1:** Forzado de cifrado TLS en todas las comunicaciones
    * **Dado** un cliente HTTP intentando conectar mediante protocolo inseguro HTTP,
    * **Cuando** realiza la petición a cualquier endpoint de la API,
    * **Entonces** el servidor debe rechazar o redirigir la conexión exigiendo estrictamente HTTPS/TLS 1.3.
  * **Escenario 2:** Almacenamiento seguro de credenciales mediante hash
    * **Dado** el registro o actualización de un usuario en el sistema,
    * **Cuando** el usuario guarda su contraseña,
    * **Entonces** la base de datos debe almacenar exclusivamente el hash de la clave (bcrypt/argon2) sin exponer jamás texto plano.

---

#### ID: EN-004
* **Título:** Soporte de persistencia offline y sincronización PWA mediante IndexedDB
* **Tipo:** Fiabilidad / Arquitectura Móvil
* **Requisito Trazado:** RNF-004 / RF-012
* **Redacción:**
  * **Como** Desarrollador Frontend Móvil,
  * **quiero** integrar IndexedDB y Service Workers en la PWA del Conductor,
  * **para** permitir el registro local de entregas en zonas con baja o nula cobertura (2G/3G) y su posterior sincronización sin duplicados.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1:** Registro de entrega en modo offline
    * **Dado** que el conductor transita por una zona periférica sin señal celular,
    * **Cuando** marca un pedido como "Entregado" en la PWA,
    * **Entonces** el sistema debe almacenar la transacción en IndexedDB localmente con marca de tiempo sin perder datos.
  * **Escenario 2:** Sincronización automática sin duplicidad tras reconexión
    * **Dado** que la PWA recupera la conectividad a la red móvil,
    * **Cuando** el Service Worker detecta la señal,
    * **Entonces** debe sincronizar el 100% de las entregas pendientes con el backend sin generar registros duplicados.

---

#### ID: EN-005
* **Título:** Diseño accesible WCAG 2.1 AA e interfaz táctil para el modo conductor
* **Tipo:** Usabilidad / UX
* **Requisito Trazado:** RNF-005 / RF-010
* **Redacción:**
  * **Como** Diseñador UX/UI,
  * **quiero** maquetar la PWA del Conductor bajo los estándares WCAG 2.1 Nivel AA con botones táctiles de al menos $48 \times 48$ px,
  * **para** asegurar una operación limpia, accesible y de bajo impacto operativo durante la conducción.

* **Criterios de Aceptación (BDD / Gherkin):**
  * **Escenario 1:** Verificación de tamaño de controles táctiles
    * **Dado** la interfaz móvil desplegada en el dispositivo del conductor,
    * **Cuando** se inspeccionan los botones principales de acción ("Confirmar Entrega", "Reportar Incidente"),
    * **Entonces** todos los elementos interactivos deben medir como mínimo $48 \times 48$ píxeles táctiles.
  * **Escenario 2:** Verificación de contraste cromático WCAG AA
    * **Dado** el tema visual de la aplicación móvil,
    * **Cuando** se ejecuta la auditoría de accesibilidad en Lighthouse / WCAG,
    * **Entonces** la relación de contraste de color entre texto y fondo debe ser $\ge 4.5:1$ para garantizar legibilidad a luz de día.
