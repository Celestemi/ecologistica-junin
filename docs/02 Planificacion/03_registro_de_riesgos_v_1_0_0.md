# 03. Registro de Riesgos V_1_0_0 (v2)

**Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Estándar:** PMBOK® Guide 7.ª Edición / CMMI-DEV v2.0 (Gestión de Riesgos - RSKM)  
**Versión:** V_1_0_0 (v2)  
**Fecha:** 15 de septiembre de 2026  

---

## 1. Marco Metodológico y Fórmulas de Cálculo

La gestión de riesgos de **EcoLogística Huancayo** consolida la identificación, análisis cualitativo, planificación de respuestas y monitoreo continuo de las amenazas y oportunidades del proyecto.

### Fórmulas y Escalas de Evaluación

$$\text{Severidad (Exposición)} = \text{Probabilidad (1 a 5)} \times \text{Impacto (1 a 5)}$$

* **Probabilidad (1 a 5):**
  * **1 (Muy baja):** Evento raro o de muy improbable ocurrencia (< 10%).
  * **2 (Baja):** Poco frecuente pero posible en el ciclo de vida (10% – 30%).
  * **3 (Media):** Frecuencia moderada (31% – 50%).
  * **4 (Alta):** Ocurrencia probable durante las iteraciones (51% – 80%).
  * **5 (Muy alta):** Casi certeza de ocurrencia (> 80%).

* **Impacto (1 a 5):**
  * **1 (Insignificante):** Desviación mínima sin afectación a hitos o calidad.
  * **2 (Menor):** Leve afectación en costos o tiempos (< 5%), absorbible en el Sprint.
  * **3 (Moderado):** Requiere reconfiguración de componentes o ajustes de alcance secundario.
  * **4 (Mayor):** Compromete SLAs de calidad (rendimiento, seguridad) o velocidad del equipo.
  * **5 (Catastrófico):** Compromete el lanzamiento del MVP, la viabilidad legal o la arquitectura base.

* **Clasificación de Severidad:**
  * **Low (1 - 6):** Riesgo tolerable. Monitoreo pasivo y control en reuniones de Sprint.
  * **Medium (8 - 12):** Riesgo moderado. Requiere plan preventivo activo y responsable asignado.
  * **High (15 - 25):** Riesgo crítico. Planes preventivo y reactivo obligatorios con seguimiento semanal por la PM.

---

## 2. Matriz de Evaluación de Riesgos

| ID | Descripción del Riesgo | Categoría | Prob. | Imp. | Severidad | Plan de Mitigación (Preventivo) | Plan de Contingencia (Reactivo) | Responsable |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **RIE-001** | El motor de optimización VRPTW + Green VRP excede el tiempo límite de cálculo de ≤ 45 segundos para 150 pedidos y 15 vehículos (RNF-001). | Técnica / Rendimiento | 3 | 5 | **High (15)** | Implementar pre-clustering geoespacial mediante PostGIS antes de invocar Google OR-Tools y aplicar técnicas de warm-start metaheurístico. | Activar particionamiento de lote por distritos (Huancayo, El Tambo, Chilca) y conmutar a algoritmo genético simplificado (DEAP). | Dev Backend / Arquitecto |
| **RIE-002** | Inestabilidad o pérdida de conectividad 2G/3G en zonas periféricas durante la operación móvil del conductor en campo (RNF-004). | Técnica / Infraestructura | 4 | 3 | **Medium (12)** | Desarrollar la aplicación móvil como React PWA utilizando IndexedDB para almacenamiento local persistente de hojas de ruta y estado de entregas. | Ejecutar cola de sincronización asíncrona mediante Service Workers al detectar reconexión y permitir impresión previa de PDF de respaldo (RF-016). | Dev Frontend / PWA |
| **RIE-003** | Exposición no autorizada de datos personales de clientes/conductores (DNI, GPS) incumpliendo la Ley N° 29733 (RNF-003). | Seguridad / Normativa | 2 | 5 | **Medium (10)** | Cifrado estricto TLS 1.3 en tránsito, hash bcrypt para contraseñas, autenticación JWT con expiración y control de acceso RBAC estricto. | Revocación inmediata de tokens JWT comprometidos, aislamiento del componente API afectado y reporte formal del incidente de seguridad. | Especialista Ciberseguridad |
| **RIE-004** | Inconsistencias o imprecisión en datos de direcciones y geocodificación en sectores urbanos de Huancayo, El Tambo y Chilca. | Datos / Operativa | 4 | 3 | **Medium (12)** | Validación de geometrías distritales con PostGIS e interfaz interactiva Leaflet que permite al Operador corregir las coordenadas visualmente (RF-005). | Marcar el pedido como 'Pendiente de Validación' e iniciar protocolo de contacto directo con la bodega/comercio para confirmación de referencia. | Operador de Logística |
| **RIE-005** | Falla o indisponibilidad del servidor local de ruteo OSRM sobre cartografía OpenStreetMap. | Técnica / Servicios | 2 | 4 | **Medium (8)** | Contenedorización en Docker de OSRM con tiles pre-procesados locales de Junín y monitoreo continuo de disponibilidad (healthchecks). | Conmutación automática a la vista alternativa tabular (RF-012) con cálculo matricial aproximado por distancia Manhattan/Euclidiana. | DevOps / Backend |
| **RIE-006** | Exceso de capacidad vehicular (>100% peso/volumen) o violación de jornada máxima laboral de 8h del conductor (RN-003 / RN-004 / Ley 30224). | Operativa / Normativa | 3 | 4 | **Medium (12)** | Inclusión de validación de restricciones duras e infranqueables en el motor de optimización (RF-008) previo a la generación de ruta. | Rechazo automático de la solución en el backend y notificación en interfaz para división de lote o asignación de vehículo de retén. | Operador de Logística |
| **RIE-007** | Baja adopción digital o dificultad de uso de la PWA por parte de los conductores de la flota. | Usabilidad / Social | 3 | 3 | **Medium (9)** | Diseño UX/UI simplificado bajo normas WCAG 2.1 AA con controles táctiles principales de mínimo 48 x 48 px (RNF-005) y prototipado adaptativo. | Habilitar el 'Modo Conductor Asistido' (solo secuencia de paradas) e impresión de hojas de ruta físicas en PDF (RF-016). | Diseñador UX/UI / PM |
| **RIE-008** | Inconsistencias normativas sobre restricción vehicular por placa (RN-002 / DS 033-2012-MTC) en ordenanzas locales de Huancayo. | Normativa / Legal | 2 | 3 | **Low (6)** | Parametrización dinámica en BD con flag `[PENDIENTE DE VALIDACIÓN NORMATIVA]` manteniéndola desactivada por defecto hasta confirmación legal. | Activación o modificación del parámetro vía panel de administración sin requerir modificaciones en código fuente o re-despliegues. | PM / Analista Legal |
| **RIE-009** | Ocurrencia de incidentes en vía (averías mecánicas, bloqueos, accidentes) interrumpiendo rutas en tránsito (RF-018). | Operativa / Clima & Vía | 3 | 4 | **Medium (12)** | Módulo de reporte de incidentes en tiempo real en la PWA e identificación de zonas de riesgo/sensibles en la capa cartográfica. | Re-optimización dinámica en ≤ 30s (RNF-002) asignando prioridad a pedidos con ventana a vencer en < 2 horas (RN-007). | Operador de Logística |
| **RIE-010** | Sobrecarga académica o rotación de integrantes del equipo afectando el cumplimiento del cronograma estricto de 14 semanas. | Gestión / Proyecto | 3 | 5 | **High (15)** | Gestión ágil en Jira Software con Sprints de 2 semanas, revisiones por pares (Peer Review) y seguimiento estricto del Definition of Done (DoD). | Re-priorización del Backlog asegurando la cobertura del MVP (≥70% de RFs según RES-06) y redistribución de asignaciones. | Project Manager (PM) |

---

## 3. Plan de Monitoreo y Control de Riesgos

1. **Revisión Continua en Sprint Reviews:** En cada cierre de Sprint (semanas 3, 7, 11 y 14), la Project Manager (Nikole Bastidas) actualizará la matriz de riesgos para identificar nuevas amenazas o reevaluar la probabilidad/impacto de los riesgos existentes.
2. **Alertas de Desviación:** Si un riesgo pasa de nivel *Medium* a *High*, se convocará a una reunión extraordinaria de arquitectura/gestión en un plazo menor a 24 horas.
3. **Auditoría de Cumplimiento:** El Auditor Académico / Docente contará con permisos de lectura/consulta sobre este registro para verificar la trazabilidad y eficacia de los planes preventivos.
