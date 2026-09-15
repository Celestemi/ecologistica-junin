# 04. Presupuesto del Proyecto V_1_0_0.md

**Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Ámbito Geográfico:** Huancayo, El Tambo y Chilca — Provincia de Huancayo, Junín  
**Marco de Gestión:** Enfoque Híbrido (14 semanas / 4 iteraciones)  
**Fecha:** 15 de septiembre de 2026  
**Versión:** V_1_0_0 (SemVerDoc)  

---

## 1. Introducción y Modelo Financiero
El presente documento establece el **Modelado Financiero Integral** para la fase de desarrollo e implementación del Producto Final Académico (PFA) **EcoLogística Huancayo**. La estructura presupuestaria consolida los costos directos de desarrollo (**CAPEX**), los gastos recurrentes de licenciamiento y herramientas, los costos operacionales de infraestructura en la nube (**OPEX**) y la reserva de contingencia derivada de la Matriz de Evaluación de Riesgos (*CMMI/PMBOK*).

El presupuesto se alinea con la meta referencial histórica de **S/ 500,000.00 PEN** definida en la Declaración de la Visión y el Acta de Constitución [31, 36, 44], expresándose en dólares estadounidenses (USD) bajo un tipo de cambio referencial de **1 USD = 3.72 PEN**.

---

## 2. Estructura Desagregada del Presupuesto

### 2.1 Costo de Recursos Humanos (CAPEX)
Corresponde a la inversión en capital humano calificado durante el ciclo de vida de desarrollo de **14 semanas** (3.5 meses), considerando la asignación horaria necesaria para cubrir las 4 iteraciones del proyecto y la entrega del MVP funcional (alcance ≥ 70% de Requisitos Funcionales).

*Fórmula de Cálculo:* $	ext{Costo Total} = 	ext{Horas Asignadas} 	imes 	ext{Tarifa Hora (USD)}$

| Rol Profesional | Perfil / Responsabilidades Clave | Horas Asignadas | Tarifa Hora (USD) | Costo Subtotal (USD) |
| :--- | :--- | :---: | :---: | ---: |
| **Project Manager (PM)** | Liderazgo de proyecto, seguimiento de iteraciones en Jira, gestión de interesados y control de calidad documental. | 480 hrs | $ 40.00 | $ 19,200.00 |
| **Software Architect** | Diseño C4, arquitectura FastAPI/PostGIS, patrones de diseño, integración OSRM local y seguridad TLS/JWT. | 360 hrs | $ 50.00 | $ 18,000.00 |
| **Senior Developer** | Desarrollo del motor de optimización VRPTW/Green VRP en Python (Google OR-Tools/DEAP) y API REST backend. | 640 hrs | $ 40.00 | $ 25,600.00 |
| **Junior Developer** | Desarrollo Frontend Web SPA en React.js, Tailwind CSS, integración Leaflet.js y PWA móvil en IndexedDB. | 640 hrs | $ 25.00 | $ 16,000.00 |
| **QA Engineer** | Pruebas automatizadas (PyTest), ejecución de escenarios BDD/Gherkin, análisis SonarQube y pruebas de carga. | 480 hrs | $ 30.00 | $ 14,400.00 |
| **UI/UX Designer** | Diseño de prototipos en Figma, cumplimiento de accesibilidad WCAG 2.1 AA y diseño de interfaz táctil para conductores. | 400 hrs | $ 29.50 | $ 11,800.00 |
| **SUBTOTAL RECURSOS HUMANOS (CAPEX)** | **Asignación total de equipo técnico** | **3,000 hrs** | — | **$ 105,000.00** |

---

### 2.2 Costo de Licenciamiento y Herramientas
Desglose de herramientas de software, entornos de desarrollo integrados (IDEs), plataformas de gestión ágil, análisis estático de código y servicios de seguridad requeridos para el equipo durante las 14 semanas de desarrollo.

| Herramienta / Licencia | Propósito en el Proyecto | Unidades / Licencias | Periodo | Costo Subtotal (USD) |
| :--- | :--- | :---: | :---: | ---: |
| **Atlassian Jira Software & Confluence** | Gestión ágil de Backlog, Tablero Scrum, Hoja de Ruta y documentación de Sprints. | 10 usuarios | 3.5 meses | $ 525.00 |
| **Figma Professional** | Prototipado de alta fidelidad, mapas de navegación y diseño de componentes WCAG 2.1 AA. | 3 editores | 3.5 meses | $ 157.50 |
| **SonarQube Cloud (Developer Plan)** | Análisis estático de código, detección de deuda técnica y vulnerabilidades OWASP Top 10. | 100k LOC | 3.5 meses | $ 175.00 |
| **JetBrains All Products Pack** | IDEs especializados (PyCharm Professional para Python/FastAPI, WebStorm para React.js). | 5 licencias | 3.5 meses | $ 875.00 |
| **GitHub Team & CI/CD Runners** | Control de versiones Git, almacenamiento de artefactos y ejecución de pipelines automatizados. | 1 org / 5 dev | 3.5 meses | $ 420.00 |
| **Postman & OWASP ZAP Pro** | Pruebas automatizadas de endpoints API REST y escaneo de vulnerabilidades de seguridad. | 3 licencias | 3.5 meses | $ 350.00 |
| **Certificados SSL Wildcard & Dominios** | Cifrado TLS 1.3 en tránsito y registro de dominios institucionales de prueba (`.pe` / `.com`). | 1 dominio/SSL | 1 año | $ 350.00 |
| **Docker Hub Pro & Registry Cloud** | Almacenamiento de imágenes de contenedores Docker para FastAPI, Celery y servidor OSRM. | 1 cuenta Pro | 3.5 meses | $ 137.50 |
| **Herramientas GIS & Datos OSRM** | Software de procesamiento y validación de cartografía OpenStreetMap para Huancayo. | Global | Único | $ 1,210.00 |
| **SUBTOTAL LICENCIAMIENTO Y HERRAMIENTAS** | **Herramientas de desarrollo e ingeniería** | — | — | **$ 4,200.00** |

---

### 2.3 Costo de Infraestructura Cloud y Servicios (OPEX)
Desglose de servicios en la nube para los ambientes de Desarrollo, Staging y Pruebas de Carga en AWS / GCP durante el desarrollo del proyecto (14 semanas).

| Servicio Cloud | Especificación Técnica / Instancia | Propósito en la Arquitectura | Costo Mensual (USD) | Costo Subtotal (USD) |
| :--- | :--- | :--- | ---: | ---: |
| **Cómputo Backend & OSRM** | 2x Instancias EC2 / Compute Engine (`c6i.2xlarge` - 8 vCPU, 16GB RAM) | Ejecución del servidor FastAPI, Celery Workers, OR-Tools y motor de ruteo OSRM local. | $ 1,200.00 | $ 4,200.00 |
| **Base de Datos Gestionada** | AWS RDS PostgreSQL 15 + PostGIS 3 Multi-AZ (4 vCPU, 16GB RAM, SSD 100GB) | Persistencia relacional 3FN, procesamiento de geometrías GIS y logs de auditoría. | $ 800.00 | $ 2,800.00 |
| **Caché y Colas en Memoria** | Managed Redis Cluster / ElastiCache (2 nodos, 4GB RAM) | Gestión de colas asíncronas para Celery, caché de matrices de distancia y sesiones JWT. | $ 300.00 | $ 1,050.00 |
| **Almacenamiento y CDN** | AWS S3 + CloudFront CDN | Hosting estático de la PWA/React SPA, distribución de tiles OSM y reportes PDF. | $ 250.00 | $ 875.00 |
| **Networking & Seguridad** | VPC Peering, NAT Gateway, Elastic IPs y AWS WAF / Firewall | Protección de endpoints, aislamiento de red y transferencia de datos segura. | $ 350.00 | $ 1,225.00 |
| **Monitoreo & Observabilidad** | AWS CloudWatch + Datadog APM | Monitoreo de latencia en tiempo real, alertas de SLA (≤45s / ≤30s) y logs de API. | $ 185.71 | $ 650.00 |
| **SUBTOTAL INFRAESTRUCTURA CLOUD (OPEX)** | **Servicios e infraestructura gestionada** | — | — | **$ 10,800.00** |

---

### 2.4 Reserva de Contingencia (Imprevistos)
Conforme a la evaluación de riesgos realizada en el **Artefacto 3 (Registro de Riesgos - RIE-001 a RIE-010)** y los estándares PMBOK®, se establece una reserva de contingencia del **12%** sobre el subtotal del proyecto.

Esta reserva cubre eventos de riesgo identificados como:
* Re-alojamiento o escalado de instancias de cómputo ante mayor volumen de pruebas metaheurísticas (RIE-001).
* Pruebas adicionales de usabilidad y conectividad offline para la PWA de conductores (RIE-002).
* Auditorías de ciberseguridad adicionales para garantizar cumplimiento de la Ley N° 29733 (RIE-003).

$$	ext{Reserva de Contingencia} = 	ext{SUBTOTAL DE PROYECTO} 	imes 12\% = \$ 120,000.00 	imes 0.12 = \$ 14,400.00 	ext{ USD}$$

---

## 3. Tabla Resumen Financiera

La siguiente tabla resume el consolidado presupuestario del proyecto **EcoLogística Huancayo**:

| Categoría | Costo Subtotal (USD) | Porcentaje del Total |
| :--- | ---: | ---: |
| **1. Recursos Humanos (CAPEX)** | $ 105,000.00 | 87.5% |
| **2. Licenciamiento de Software** | $ 4,200.00 | 3.5% |
| **3. Infraestructura Cloud (OPEX)** | $ 10,800.00 | 9.0% |
| **SUBTOTAL DE PROYECTO** | **$ 120,000.00** | **100.0%** |
| **4. Reserva de Contingencia (12%)** | $ 14,400.00 | N/A |
| **PRESUPUESTO TOTAL ESTIMADO** | **$ 134,400.00** | **100.0%** |

*Nota de Conversión:* El Presupuesto Total Estimado de **$ 134,400.00 USD** equivale a **S/ 499,968.00 PEN** (tipo de cambio 1 USD = 3.72 PEN), lo cual satisface con máxima precisión la meta presupuestaria institucional referencial de **S/ 500,000.00 PEN** establecida en los documentos baseline del proyecto [31, 36, 44].
