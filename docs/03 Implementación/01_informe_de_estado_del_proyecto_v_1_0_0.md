# 01. Informe de estado del proyecto V_1_0_0.md

# Revisión del sprint

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C. [1, 28, 55]

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager) [15, 55, 64, 81]

---

## Historias de Usuario completadas en este Sprint (Sprint 1: Fundación, Flota y Pedidos)

* **EN-003 (Habilitador Técnico de Seguridad):** Implementación de seguridad transversal, cifrado TLS 1.3 en tránsito, hash bcrypt de contraseñas, autenticación basada en JWT y matriz de control de acceso por roles (RBAC) [52, 123, 130].
* **US-001 (RF-001):** Registro y mantenimiento de vehículos de la flota (placa, modelo, capacidad kg/m³, tipo de combustible, rendimiento y factor de emisión de CO₂) [32, 88].
* **US-002 (RF-002 / RN-002):** Configuración de reglas de restricción de circulación vehicular por último dígito de placa para Huancayo, El Tambo y Chilca [33, 90, 132].
* **US-003 (RF-003):** Historial y control del estado operativo del vehículo (transiciones entre estados *Activo*, *Mantenimiento* e *Inactivo*) [34, 92].
* **US-004 (RF-004):** Importación masiva de lotes de hasta 150 pedidos mediante archivos estructurados en formato CSV o Excel [35, 93, 129].
* **US-006 (RF-006 / RN-005):** Gestión de ventanas de tiempo de entrega por pedido (rango horario [`Hora_inicio`, `Hora_fin`]) [37, 97, 134].

---

## Demostración del trabajo completado

Se realizó la demostración funcional ante los docentes, equipo evaluador y partes interesadas (stakeholders) [62, 83, 85]:

1. **Autenticación y Gobernanza de Acceso:** Demostración del inicio de sesión seguro con JWT, bloqueo automático de usuario por 15 minutos tras 3 intentos fallidos consecutivos (RN-001) [132] y verificación del perfil de Auditor Académico restringido en modo solo lectura/consulta [128, 130].
2. **Administración de Flota Vehicular:** Registro en vivo de unidades de transporte especificando combustible (Diésel, Gasolina, GNV), capacidad nominal y prueba de inactivación de vehículo para excluirlo de la futura asignación de rutas [32, 34].
3. **Carga y Validación Masiva de Pedidos:** Importación exitosa de un archivo CSV con 150 pedidos para los distritos de Huancayo, El Tambo y Chilca [35], demostrando la detección automática de errores de formato y la configuración exitosa de ventanas de tiempo de entrega por cliente [37].

---

## Pendientes (Backlog comprometido para las siguientes iteraciones)

* **US-005 (RF-005):** Geocodificación y ubicación espacial de pedidos sobre mapa en formato PostGIS `GEOGRAPHY(Point, 4326)` [36, 95, 146].
* **US-007 (RF-007 / RN-008):** Generación de rutas sostenibles mediante el motor de optimización VRPTW + Green VRP en Google OR-Tools / DEAP [38, 98, 140].
* **US-008 (RF-008 / RN-003 / RN-004):** Validación de restricciones duras (cero tolerancia a exceso de capacidad y jornada laboral máxima de 8 horas) [39, 100, 133].
* **US-009 (RF-009):** Cálculo de la secuencia de paradas y tiempo estimado de llegada (ETA) por cliente [40, 102].
* **EN-001 (RNF-001):** Tuning y optimización metaheurística del motor de ruteo para garantizar un tiempo de cálculo $\le 45$ segundos (SLA para 150 pedidos y 15 vehículos) [50, 121].
* **EN-004 (RNF-004):** Desarrollo de la aplicación móvil PWA en React.js con IndexedDB para almacenamiento offline y sincronización asíncrona de entregas en zonas de baja cobertura [53, 124, 129].
