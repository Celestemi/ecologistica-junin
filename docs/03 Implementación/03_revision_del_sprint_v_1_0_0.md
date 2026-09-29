# 03. Revisión del Sprint V_1_0_0.md

# Revisión del sprint

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

---

## Historias de Usuario completadas en este Sprint

En el presente Sprint (Sprint 1: Fundación, Flota y Pedidos) se han completado y verificado satisfactoriamente las siguientes Historias de Usuario e Historias Técnicas/Habilitadores (Enablers), cumpliendo al 100% con los criterios de aceptación BDD (Gherkin) y la Definition of Done (DoD) global:

* **EN-003 (Habilitador Técnico de Seguridad & Gobierno - RNF-003):** 
  * *Título:* Seguridad Transversal, Autenticación JWT y Cifrado.
  * *Puntos de Historia:* 5 SP.
  * *Entregable:* Módulo de seguridad con cifrado TLS 1.3 en tránsito, hashing bcrypt de contraseñas, emisión de tokens JWT con expiración automática de 15 minutos e implementación del control de acceso basado en roles (RBAC) para los 6 perfiles del sistema (incluyendo la restricción estricta de solo lectura/consulta para el Auditor Académico/Docente).

* **US-001 (RF-001):** 
  * *Título:* Registro y mantenimiento de vehículos de la flota.
  * *Puntos de Historia:* 3 SP.
  * *Entregable:* Panel de administración CRUD de la flota vehicular que permite registrar, editar e inactivar unidades capturando la placa, modelo, capacidad (kg y m³), tipo de combustible (Diésel, Gasolina, GNV), rendimiento (km/galón) y factor de emisión oficial de CO₂ (RN-006).

* **US-002 (RF-002 / RN-002):** 
  * *Título:* Configuración de restricciones de circulación por placa.
  * *Puntos de Historia:* 2 SP.
  * *Entregable:* Módulo de parametrización de reglas de restricción vehicular según el último dígito de la placa para los distritos de Huancayo, El Tambo y Chilca, configurado con flag de control `[PENDIENTE DE VALIDACIÓN NORMATIVA]` que la mantiene desactivada por defecto.

* **US-003 (RF-003):** 
  * *Título:* Historial y control del estado operativo del vehículo.
  * *Puntos de Historia:* 2 SP.
  * *Entregable:* Sistema de gestión de estados operativos de vehículos (*Activo*, *Mantenimiento*, *Inactivo*) con registro de auditoría (*audit_log*) que excluye automáticamente de la asignación de rutas a las unidades que no estén en estado *Activo*.

* **US-004 (RF-004):** 
  * *Título:* Importación masiva de pedidos.
  * *Puntos de Historia:* 5 SP.
  * *Entregable:* Endpoint y componente de interfaz para la carga masiva en lote de hasta 150 pedidos mediante archivos CSV/Excel, con validación de estructura de datos, detección de duplicados y asociación automática a clientes de Huancayo, El Tambo y Chilca.

* **US-006 (RF-006 / RN-005):** 
  * *Título:* Gestión de ventanas de tiempo de entrega por pedido.
  * *Puntos de Historia:* 3 SP.
  * *Entregable:* Formulario y servicio backend para el registro estricto de ventanas de entrega pactadas con el cliente (`[Hora_inicio, Hora_fin]`), asegurando la captura de precondiciones para el motor de ruteo VRPTW.

**Total de Puntos de Historia Completados:** 20 SP (100% del alcance comprometido para el Sprint 1).

---

## Demostración del trabajo completado

Durante la sesión de revisión con los stakeholders (Docente Evaluador, Gerencia de Operaciones de DistriRápido S.A.C. y equipo de desarrollo), se realizó la demostración en vivo (*Sprint Demo*) del software desplegado en el ambiente de Staging:

1. **Demostración de Seguridad, Gobernanza RBAC y Bloqueo (EN-003):**
   * Se simuló un intento de ataque por fuerza bruta realizando 3 intentos fallidos consecutivos de inicio de sesión, verificando el bloqueo automático de la cuenta por 15 minutos conforme a la regla de negocio **RN-001**.
   * Se inició sesión con las credenciales del **Auditor Académico/Docente**, demostrando que la interfaz restringe la ejecución de acciones operativas (como optimizar rutas o modificar flota) habilitando exclusivamente la visualización de paneles y reportes.

2. **Demostración de Gestión de Flota y Restricciones (US-001, US-002, US-003):**
   * Se registró un nuevo vehículo furgón para la flota de Huancayo seleccionando combustible GNV (factor 2.75 kg CO₂/m³) y capacidad nominal de 1,500 kg / 8 m³.
   * Se cambió el estado de un vehículo a *Mantenimiento* y se comprobó que el sistema actualizó la bitácora de auditoría y bloqueó su asignación a rutas.
   * Se mostró la configuración de restricciones por placa (`RN-002`), evidenciando el mensaje de advertencia sobre el estado de confirmación normativa municipal.

3. **Demostración de Importación Masiva y Ventanas de Tiempo (US-004, US-006):**
   * Se ejecutó la carga en vivo de un archivo CSV con un lote de 150 pedidos distribuidos en Huancayo, El Tambo y Chilca.
   * Se mostró el reporte de validación en pantalla, resaltando la correcta asignación de las coordenadas iniciales y el rango horario de entrega de cada pedido (`RN-005`).

---

## Pendientes

De acuerdo con el plan de versiones (`v1.0.0-MVP`) y el Roadmap del proyecto, los siguientes elementos del Backlog priorizado continúan en estado pendiente para ser abordados en los Sprints 2, 3 y 4:

1. **Sprint 2 (Algoritmos y Motor de Optimización):**
   * **US-005 (RF-005):** Geocodificación y ubicación espacial de pedidos con PostGIS `GEOGRAPHY(Point, 4326)`. *(5 SP)*
   * **US-007 (RF-007 / RN-008):** Generación de rutas sostenibles mediante motor metaheurístico VRPTW + Green VRP en Google OR-Tools y DEAP. *(13 SP)*
   * **US-008 (RF-008 / RN-003 / RN-004):** Validación de restricciones duras (tolerancia cero a exceso de capacidad y límite de jornada de 8h). *(5 SP)*
   * **US-009 (RF-009):** Cálculo de la secuencia óptima de paradas y tiempo estimado de llegada (ETA) por pedido. *(3 SP)*
   * **EN-001 (RNF-001):** Optimización y tuning del motor de ruteo para cumplir el SLA de generación de rutas en $\le 45$ segundos para 150 pedidos y 15 vehículos. *(8 SP)*

2. **Sprint 3 (Cartografía, Resiliencia PWA y Sostenibilidad):**
   * **US-010 a US-012 (RF-010 a RF-012):** Visualización en mapa interactivo Leaflet, panel de detalle por parada y vista alternativa tabular ante contingencias cartográficas. *(13 SP)*
   * **US-013 a US-015 (RF-013 a RF-015):** Dashboard de sostenibilidad con consolidado de KPIs (distancia, combustible, CO₂), comparación contra línea base y equivalencia en árboles. *(11 SP)*
   * **EN-004 (RNF-004):** Desarrollo de la aplicación móvil PWA para conductores con almacenamiento offline en IndexedDB y Service Workers. *(8 SP)*

3. **Sprint 4 (Reportes, Re-optimización Dinámica y Cierre de MVP):**
   * **US-016 y US-017 (RF-016, RF-017):** Exportación de hoja de ruta en PDF con espacio de conformidad e historial auditable en CSV. *(6 SP)*
   * **US-018 (RF-018 / RN-007):** Módulo de re-optimización dinámica en tiempo real ante incidentes en vía (averías, bloqueos). *(8 SP)*
   * **EN-002 (RNF-002):** Tuning del tiempo de respuesta del motor de re-optimización en $\le 30$ segundos. *(5 SP)*
