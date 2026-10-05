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

- 🚗 **Reducción de distancia:** disminución $\ge 15\%$ frente a la ruta secuencial sin optimizar.
- 🌿 **Reducción de emisiones:** reducción $\ge 10\%$ mensual de $\text{CO}_2$ basada en factores oficiales de combustible.
- ⏰ **Cumplimiento de ventanas horarias:** nivel de cumplimiento $\ge 90\%$ (incumplimiento $\le 10\%$).
- ⚡ **SLA de rendimiento:** generación de ruta en $\le 45\text{ s}$ (150 pedidos / 15 vehículos) y re-optimización en $\le 30\text{ s}$.

---

## 📁 Estructura del Repositorio

```text
ecologistica-junin/
├── 📄 README.md
├── 📄 .gitignore
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
│       ├── 📄 03_revision_del_sprint_v_1_0_0.md
│       └── 📄 04_retrospectiva_del_sprint_V_1_0_0.md
├── 📁 app/                      # API, VRPTW, tiempo real y PDF
├── 📁 src/                      # Panel, conductor y seguimiento
├── 📁 tests/
├── 📄 docker-compose.yml
└── 📁 EcologisticaJunin/        # esqueleto anterior
    ├── 📁 backend/
    └── 📁 frontend/
```

---

## 📚 Índice Detallado de Documentación

Haz clic en cualquier documento para navegar directamente a él dentro del repositorio.

### 🏛️ Fase 1: Inicio y Requisitos Base (`docs/01 Inicio/`)

| # | Documento | Descripción |
|---|-----------|-------------|
| 00 | [Directrices y Auditoria V_1_0_3](docs/01%20Inicio/00.%20Directrices%20y%20Auditoria%20V_1_0_3.md) | Normas documentales e informe de auditoría de coherencia. |
| 01 | [Selección del enfoque del proyecto V_1_0_0](docs/01%20Inicio/01.%20Selecci%C3%B3n%20del%20enfoque%20del%20proyecto%20V_1_0_0.md) | Justificación del enfoque Híbrido de gestión. |
| 02 | [Acta de constitución V_1_0_0](docs/01%20Inicio/02.%20Acta%20de%20constituci%C3%B3n%20V_1_0_0.md) | Project Charter, gobernanza, justificación y presupuesto referencial. |
| 03 | [Declaración de la visión V_1_0_0](docs/01%20Inicio/03.%20Declaraci%C3%B3n%20de%20la%20visi%C3%B3n%20V_1_0_0.md) | Visión estratégica del sistema EcoLogística Huancayo. |
| 04 | [Registro de Supuestos y Restricciones V1.0.0](docs/01%20Inicio/04.%20Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md) | Límites operativos, financieros y normativos. |
| 05 | [Registro de interesados V_1_0_0](docs/01%20Inicio/05.%20Registro%20de%20interesados%20V_1_0_0.md) | Matriz de Poder vs. Interés de stakeholders. |
| 06 | [Requisitos funcionales V_1_0_0](docs/01%20Inicio/06.%20Requisitos%20funcionales%20V_1_0_0.md) | Macro-requisitos (MRF-01 a MRF-07), RF-001 a RF-018 y escenarios BDD. |
| 07 | [Requisitos no funcionales V_1_0_0](docs/01%20Inicio/07.%20Requisitos%20no%20funcionales%20V_1_0_0.md) | Escenarios de calidad ISO/IEC 25010 (RNF-001 a RNF-005). |
| 08 | [Usuarios V_1_0_3](docs/01%20Inicio/08.%20Usuarios%20V_1_0_3.md) | Perfiles de usuario y matriz RBAC (con restricción para Auditor). |
| 09 | [Reglas de negocio V_1_0_4](docs/01%20Inicio/09.%20Reglas%20de%20negocio%20V_1_0_4.md) | Reglas RN-001 a RN-008 (bloqueos, capacidades, emisiones, horarios). |
| 10 | [Stack tecnológico V_1_0_3](docs/01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_3.md) | Selección multicriterio de arquitectura 100% código abierto. |
| 11 | [Base de datos V_1_0_3](docs/01%20Inicio/11.%20Base%20de%20datos%20V_1_0_3.md) | Modelo ER relacional en 3FN y extensiones geoespaciales PostGIS. |
| 12 | [Modelo C4 V_1_0_6](docs/01%20Inicio/12.%20Modelo%20C4%20V_1_0_6.md) | Diagramas C4 de Contexto, Contenedores y Componentes Backend. |
| 13 | [Restricciones V_1_0_4](docs/01%20Inicio/13.%20Restricciones%20V_1_0_4.md) | Análisis multidimensional de impacto, mitigación y LCC. |

### 📋 Fase 2: Planificación Ágil (`docs/02 Planificacion/`)

| Documento | Descripción |
|-----------|-------------|
| [01_transformando_a_agil_v_1_0_0](docs/02%20Planificacion/01_transformando_a_agil_v_1_0_0.md) | Transformación de requisitos a Épicas, US, Enablers y DoD global. |
| [02 Artefactos Jira V_1_0_0](docs/02%20Planificacion/02%20Artefactos%20Jira%20V_1_0_0.md) | Configuración operativa en Atlassian Jira Software. |
| [03_registro_de_riesgos_v_1_0_0](docs/02%20Planificacion/03_registro_de_riesgos_v_1_0_0.md) | Matriz de evaluación de riesgos PMBOK / CMMI. |
| [04_presupuesto_del_proyecto_v_1_0_0](docs/02%20Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md) | Modelado financiero CAPEX, OPEX y reserva de contingencia. |

#### 🖼️ Evidencias de Jira Software (`docs/02 Planificacion/Capturas en JIRA/`)

| Captura | Descripción |
|---------|-------------|
| [01-roadmap.png](docs/02%20Planificacion/Capturas%20en%20JIRA/01-roadmap.png) | Hoja de ruta con alineación de Épicas EP-01 a EP-07. |
| [02-backlog-priorizado.png](docs/02%20Planificacion/Capturas%20en%20JIRA/02-backlog-priorizado.png) | Product Backlog con estimación en Story Points (Fibonacci). |
| [03-sprint-planning.png](docs/02%20Planificacion/Capturas%20en%20JIRA/03-sprint-planning.png) | Planificación del Sprint 1 y Sprint Goal. |
| [04-tablero-scrum.png](docs/02%20Planificacion/Capturas%20en%20JIRA/04-tablero-scrum.png) | Tablero Scrum activo con flujo To Do → Done. |
| [05-versiones-release.png](docs/02%20Planificacion/Capturas%20en%20JIRA/05-versiones-release.png) | Configuración de versión v1.0.0-MVP. |

### 🚀 Fase 3: Implementación y Sprints (`docs/03 Implementación/`)

| Documento | Descripción |
|-----------|-------------|
| [01_informe_de_estado_del_proyecto_v_1_0_0](docs/03%20Implementaci%C3%B3n/01_informe_de_estado_del_proyecto_v_1_0_0.md) | Informe de estado del Sprint 1 (Plantilla 1). |
| [02_registro_de_impedimentos_v_1_0_0](docs/03%20Implementaci%C3%B3n/02_registro_de_impedimentos_v_1_0_0.md) | Registro y trazabilidad de impedimentos (Plantilla 2). |
| [03_revision_del_sprint_v_1_0_0](docs/03%20Implementaci%C3%B3n/03_revision_del_sprint_v_1_0_0.md) | Informe de revisión del Sprint y demostración a stakeholders (Plantilla 3). |
| [04_retrospectiva_del_sprint_V_1_0_0](docs/03%20Implementaci%C3%B3n/04_retrospectiva_del_sprint_V_1_0_0.md) | Retrospectiva del Sprint 1 y acciones de mejora del equipo. |

### 💻 Código de la implementación

La aplicación que se ejecuta está en la raíz del repositorio: `app/` (API, algoritmo genético VRPTW, WebSockets y PDF), `src/` (panel, modo conductor y seguimiento del cliente), `tests/` y `docker-compose.yml`. `EcologisticaJunin/` conserva el esqueleto anterior.

Copia `.env.example` a `.env` y, desde la raíz:

```powershell
docker compose up --build -d
```

`backend/entrypoint.sh` espera a PostGIS, crea el esquema con la semilla y arranca Uvicorn.

| Servicio | Puerto en el host | Función |
| --- | --- | --- |
| PostGIS 15-3.4 | 5433 | Base geoespacial |
| Backend FastAPI | 8000 | API, semilla y Swagger en `/docs` |
| Frontend Nginx | 8080 | Panel en http://localhost:8080/ |

El panel usa el 8080 para convivir con otro sitio en el puerto 80. Seguimiento del cliente: http://localhost:8080/seguimiento/PED-001. Modo conductor: http://localhost:8080/conductor. Pruebas: `docker compose exec backend pytest`.

---

## 🛠️ Stack Tecnológico (100% Código Abierto)

| Componente | Tecnología Seleccionada | Justificación |
|------------|-------------------------|---------------|
| Backend API | Python 3.11 + FastAPI | Asincronía, alto rendimiento, documentación automática OpenAPI/Swagger. |
| Motor VRPTW / Green VRP | Google OR-Tools + DEAP | Metaheurísticas avanzadas de ruteo con ventanas de tiempo sin costo de licenciamiento. |
| Base de Datos Geoespacial | PostgreSQL 15 + PostGIS 3 | Modelo en 3FN con soporte nativo de tipo `GEOGRAPHY` y consultas espaciales. |
| Frontend Web | React.js + Tailwind CSS | Interfaz modular e interactiva para operadores logísticos. |
| Móvil / Conductor | React.js PWA + IndexedDB | Funcionamiento resiliente en zonas 2G/3G de baja cobertura. |
| Cartografía y Ruteo | Leaflet.js + OSRM Local | Mapeo interactivo y matriz de distancias sobre tiles de OpenStreetMap (OSM). |
| Tareas Asíncronas | Redis + Celery | Cola de procesamiento desacoplada para optimizaciones pesadas. |

---

## 👥 Equipo del Proyecto

| Rol | Integrante |
|-----|------------|
| Project Manager (PM) | Nikole Celeste Bastidas Vilca |
| Software Architect & Lead Dev | Dante Edgar Chuquirachi Martinez |
| DevOps & Data Engineer | Hernan Anibal Osorio Diaz |
| QA & Backend Developer | Geraldine Paola Gómez Toribio |
| Frontend Developer | BryanY29 |

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).
