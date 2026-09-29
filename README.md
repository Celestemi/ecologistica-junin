# 🌱 EcoLogística Huancayo — Optimizador de Rutas Sostenibles

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg)](https://reactjs.org/)
[![PostGIS](https://img.shields.io/badge/PostgreSQL-15%20%2B%20PostGIS%203-336791.svg)](https://postgis.net/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![Sprint](https://img.shields.io/badge/Sprint-1%20Completado-success.svg)](#)

Sistema web y móvil (PWA) de optimización de rutas de reparto de última milla para **DistriRápido S.A.C.** en los distritos de **Huancayo, El Tambo y Chilca** (provincia de Huancayo, Junín). Integra algoritmos de ruteo vehicular con ventanas de tiempo (**VRPTW**) y criterios ecológicos (**Green VRP**).

---

## 🎯 Objetivos Principales (SMART)
* 🚗 **Reducción de Distancia**: Disminución $\ge 15\%$ frente a la ruta secuencial sin optimizar.
* 🌿 **Reducción de Emisiones**: Reducción $\ge 10\%$ mensual de $CO_2$ basada en factores oficiales de combustible.
* ⏰ **Cumplimiento de Ventanas Horarias**: Nivel de cumplimiento $\ge 90\%$ (incumplimiento $\le 10\%$).
* ⚡ **SLA de Rendimiento**: Generación de ruta en $\le 45	ext{ s}$ (150 pedidos / 15 vehículos) y re-optimización en $\le 30	ext{ s}$.

---

## 📁 Estructura del Repositorio y Navegación Directa

Haz clic en cualquiera de los archivos o carpetas para navegar directamente al documento correspondiente dentro del repositorio:

```text
ecologistica-junin/
├── 📄 README.md
├── 📁 docs/
│   ├── 📁 01 Inicio/
│   │   ├── 📄 00. Directrices y Auditoria V_1_0_3.md
│   │   ├── 📄 01. Selección del enfoque del proyecto V_1_0_0.md
│   │   ├── 📄 02. Acta de constitución V_1_0_0.md
│   │   ├── 📄 03. Declaración de la visión V_1_0_0.md
│   │   ├── 📄 04. Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md
│   │   ├── 📄 05. Registro de interesados V_1_0_0.md
│   │   ├── 📄 06. Requisitos funcionales V_1_0_0.md
│   │   ├── 📄 07. Requisitos no funcionales V_1_0_0.md
│   │   ├── 📄 08. Usuarios V_1_0_3.md
│   │   ├── 📄 09. Reglas de negocio V_1_0_4.md
│   │   ├── 📄 10. Stack tecnológico V_1_0_3.md
│   │   ├── 📄 11. Base de datos V_1_0_3.md
│   │   ├── 📄 12. Modelo C4 V_1_0_6.md
│   │   └── 📄 13. Restricciones V_1_0_4.md
│   ├── 📁 02 Planificacion/
│   │   ├── 📁 Capturas en JIRA/
│   │   │   ├── 🖼️ 01-roadmap.png
│   │   │   ├── 🖼️ 02-backlog-priorizado.png
│   │   │   ├── 🖼️ 03-sprint-planning.png
│   │   │   ├── 🖼️ 04-tablero-scrum.png
│   │   │   └── 🖼️ 05-versiones-release.png
│   │   ├── 📄 01_transformando_a_agil_v_1_0_0.md
│   │   ├── 📄 02 Artefactos Jira V_1_0_0.md
│   │   ├── 📄 03_registro_de_riesgos_v_1_0_0.md
│   │   └── 📄 04_presupuesto_del_proyecto_v_1_0_0.md
│   └── 📁 03 Implementación/
│       ├── 📄 01_informe_de_estado_del_proyecto_v_1_0_0.md
│       ├── 📄 02_registro_de_impedimentos_v_1_0_0.md
│       └── 📄 03_revision_del_sprint_v_1_0_0.md
└── 📁 EcologisticaJunin/
    ├── 📁 backend/
    └── 📁 frontend/
```

---

## 📚 Índice Detallado de Documentación

### 🏛️ Fase 1: Inicio y Requisitos Base (`docs/01 Inicio/`)
* [00. Directrices y Auditoria V_1_0_3.md](<docs/01 Inicio/00. Directrices y Auditoria V_1_0_3.md>) — *Normas documentales y informe de auditoría de coherencia.*
* [01. Selección del enfoque del proyecto V_1_0_0.md](<docs/01 Inicio/01. Selección del enfoque del proyecto V_1_0_0.md>) — *Justificación del enfoque Híbrido de gestión.*
* [02. Acta de constitución V_1_0_0.md](<docs/01 Inicio/02. Acta de constitución V_1_0_0.md>) — *Project Charter, gobernanza, justificación y presupuesto referencial.*
* [03. Declaración de la visión V_1_0_0.md](<docs/01 Inicio/03. Declaración de la visión V_1_0_0.md>) — *Visión estratégica del sistema EcoLogística Huancayo.*
* [04. Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md](<docs/01 Inicio/04. Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md>) — *Límites operativos, financieros y normativos.*
* [05. Registro de interesados V_1_0_0.md](<docs/01 Inicio/05. Registro de interesados V_1_0_0.md>) — *Matriz de Poder vs. Interés de stakeholders.*
* [06. Requisitos funcionales V_1_0_0.md](<docs/01 Inicio/06. Requisitos funcionales V_1_0_0.md>) — *Macro-requisitos (MRF-01 a MRF-07), RF-001 a RF-018 y escenarios BDD.*
* [07. Requisitos no funcionales V_1_0_0.md](<docs/01 Inicio/07. Requisitos no funcionales V_1_0_0.md>) — *Escenarios de Calidad ISO/IEC 25010 (RNF-001 a RNF-005).*
* [08. Usuarios V_1_0_3.md](<docs/01 Inicio/08. Usuarios V_1_0_3.md>) — *Perfiles de usuario y Matriz RBAC (con restricción para Auditor).*
* [09. Reglas de negocio V_1_0_4.md](<docs/01 Inicio/09. Reglas de negocio V_1_0_4.md>) — *Reglas RN-001 a RN-008 (bloqueos, capacidades, emisiones, horarios).*
* [10. Stack tecnológico V_1_0_3.md](<docs/01 Inicio/10. Stack tecnológico V_1_0_3.md>) — *Selección multicriterio de arquitectura 100% Código Abierto.*
* [11. Base de datos V_1_0_3.md](<docs/01 Inicio/11. Base de datos V_1_0_3.md>) — *Modelo ER relacional en 3FN y extensiones geoespaciales PostGIS.*
* [12. Modelo C4 V_1_0_6.md](<docs/01 Inicio/12. Modelo C4 V_1_0_6.md>) — *Diagramas C4 de Contexto, Contenedores y Componentes Backend.*
* [13. Restricciones V_1_0_4.md](<docs/01 Inicio/13. Restricciones V_1_0_4.md>) — *Análisis multidimensional de impacto, mitigación y LCC.*

---

### 📋 Fase 2: Planificación Ágil (`docs/02 Planificacion/`)
* [01_transformando_a_agil_v_1_0_0.md](<docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md>) — *Transformación de requisitos a Épicas, US, Enablers y DoD global.*
* [02 Artefactos Jira V_1_0_0.md](<docs/02 Planificacion/02 Artefactos Jira V_1_0_0.md>) — *Configuración operativa en Atlassian Jira Software.*
* [03_registro_de_riesgos_v_1_0_0.md](<docs/02 Planificacion/03_registro_de_riesgos_v_1_0_0.md>) — *Matriz de evaluación de riesgos PMBOK / CMMI.*
* [04_presupuesto_del_proyecto_v_1_0_0.md](<docs/02 Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md>) — *Modelado financiero CAPEX, OPEX y Reserva de Contingencia.*

#### 🖼️ Evidencias de Jira Software (`docs/02 Planificacion/Capturas en JIRA/`)
* [01-roadmap.png](<docs/02 Planificacion/Capturas en JIRA/01-roadmap.png>) — *Hoja de ruta con alineación de Épicas EP-01 a EP-07.*
* [02-backlog-priorizado.png](<docs/02 Planificacion/Capturas en JIRA/02-backlog-priorizado.png>) — *Product Backlog con estimación en Story Points (Fibonacci).*
* [03-sprint-planning.png](<docs/02 Planificacion/Capturas en JIRA/03-sprint-planning.png>) — *Planificación del Sprint 1 y Sprint Goal.*
* [04-tablero-scrum.png](<docs/02 Planificacion/Capturas en JIRA/04-tablero-scrum.png>) — *Tablero Scrum activo con flujo To Do → Done.*
* [05-versiones-release.png](<docs/02 Planificacion/Capturas en JIRA/05-versiones-release.png>) — *Configuración de versión `v1.0.0-MVP`.*

---

### 🚀 Fase 3: Implementación y Sprints (`docs/03 Implementación/`)
* [01_informe_de_estado_del_proyecto_v_1_0_0.md](<docs/03 Implementación/01_informe_de_estado_del_proyecto_v_1_0_0.md>) — *Informe de estado del Sprint 1 (Plantilla 1).*
* [02_registro_de_impedimentos_v_1_0_0.md](<docs/03 Implementación/02_registro_de_impedimentos_v_1_0_0.md>) — *Registro y trazabilidad de impedimentos (Plantilla 2).*
* [03_revision_del_sprint_v_1_0_0.md](<docs/03 Implementación/03_revision_del_sprint_v_1_0_0.md>) — *Informe de revisión del Sprint y demostración a stakeholders (Plantilla 3).*

---

### 💻 Código Fuente (`EcologisticaJunin/`)
* [📁 Backend](EcologisticaJunin/backend/) — *API REST en FastAPI, Python 3.11, OR-Tools, DEAP, PostgreSQL/PostGIS y Celery/Redis.*
* [📁 Frontend](EcologisticaJunin/frontend/) — *Aplicación Web/Desktop en React.js, Tailwind CSS, Leaflet.js y PWA móvil con IndexedDB.*

---

## 🛠️ Stack Tecnológico (100% Código Abierto)

| Componente | Tecnología Seleccionada | Justificación |
| :--- | :--- | :--- |
| **Backend API** | Python 3.11 + FastAPI | Asincronía, alto rendimiento, documentación automática OpenAPI/Swagger. |
| **Motor VRPTW / Green VRP** | Google OR-Tools + DEAP | Metaheurísticas avanzadas de ruteo con ventanas de tiempo sin costo de licenciamiento. |
| **Base de Datos Geoespacial** | PostgreSQL 15 + PostGIS 3 | Modelo en 3FN con soporte nativo de tipo `GEOGRAPHY` y consultas espaciales. |
| **Frontend Web** | React.js + Tailwind CSS | Interfaz modular e interactiva para operadores logísticos. |
| **Móvil / Conductor** | React.js PWA + IndexedDB | Funcionamiento resiliente en zonas 2G/3G de baja cobertura. |
| **Cartografía y Ruteo** | Leaflet.js + OSRM Local | Mapeo interactivo y matriz de distancias sobre tiles de OpenStreetMap (OSM). |
| **Tareas Asíncronas** | Redis + Celery | Cola de procesamiento desacoplada para optimizaciones pesadas. |

---

## 👥 Equipo del Proyecto

* **Project Manager (PM)**: Nikole Celeste Bastidas Vilca
* **Software Architect & Lead Dev**: Dante Edgar Chuquirachi Martinez
* **DevOps & Data Engineer**: Hernan Anibal Osorio Diaz
* **QA & Backend Developer**: Geraldine Paola Gómez Toribio
* **Frontend Developer**: BryanY29

---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Para más detalles, consulta el archivo [LICENSE](LICENSE).
