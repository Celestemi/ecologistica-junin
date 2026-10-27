# 🌱 EcoLogística Huancayo — Optimizador de Rutas Sostenibles

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg)](https://reactjs.org/)
[![PostGIS](https://img.shields.io/badge/PostgreSQL-15%20%2B%20PostGIS%203-336791.svg)](https://postgis.net/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![Sprint](https://img.shields.io/badge/Sprint-3%20Cierre%20documental-yellow.svg)](#)

Sistema web de optimización de rutas de reparto de última milla para **DistriRápido S.A.C.** en los distritos de **Huancayo, El Tambo y Chilca** (provincia de Huancayo, Junín). Integra algoritmos de ruteo vehicular con ventanas de tiempo (**VRPTW**) y criterios ecológicos (**Green VRP**). Sprint 3 incorpora mapa y detalle de rutas, alternativa tabular, indicadores operativos/ambientales y una implementación parcial de PWA offline con IndexedDB y Service Worker; las historias aún no se declaran *Done* porque permanecen brechas de aceptación y de Definition of Done.

> **Estado verificable al cierre documental de Sprint 3:** los requisitos y la arquitectura histórica se conservan como baseline. Los resultados reales, limitaciones y pendientes del Sprint 3 están enlazados en la sección correspondiente de este README.

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
├── README.md
├── app/                            # API y lógica de negocio FastAPI
├── backend/                        # Dockerfile y entrypoint del backend
├── docs/
│   ├── 01 Inicio/
│   ├── 02 Planificacion/
│   ├── 03 Implementación/
│   │   ├── Sprint 1/
│   │   ├── Sprint 2/
│   │   └── Sprint 3/
├── frontend/                       # Dockerfile y configuración Nginx
├── public/                         # Recursos estáticos y service worker
├── scripts/                        # Scripts de soporte
├── src/                            # Aplicación React/TypeScript
├── tests/                          # Pruebas del backend
├── docker-compose.yml
├── package.json                    # Scripts y dependencias del frontend
├── pyproject.toml                  # Dependencias y configuración Python
├── vite.config.ts
└── vitest.config.ts
```

---

## 📚 Índice Detallado de Documentación

### 🏛️ Fase 1: Inicio y Requisitos Base (`docs/01 Inicio/`)
* [00. Directrices y Auditoria V_1_0_3.md](docs/01%20Inicio/00.%20Directrices%20y%20Auditoria%20V_1_0_3.md) — *Normas documentales y informe de auditoría de coherencia.*
* [01. Selección del enfoque del proyecto V_1_0_0.md](docs/01%20Inicio/01.%20Selecci%C3%B3n%20del%20enfoque%20del%20proyecto%20V_1_0_0.md) — *Justificación del enfoque Híbrido de gestión.*
* [02. Acta de constitución V_1_0_0.md](docs/01%20Inicio/02.%20Acta%20de%20constituci%C3%B3n%20V_1_0_0.md) — *Project Charter, gobernanza, justificación y presupuesto referencial.*
* [03. Declaración de la visión V_1_0_0.md](docs/01%20Inicio/03.%20Declaraci%C3%B3n%20de%20la%20visi%C3%B3n%20V_1_0_0.md) — *Visión estratégica del sistema EcoLogística Huancayo.*
* [04. Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md](docs/01%20Inicio/04.%20Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md) — *Límites operativos, financieros y normativos.*
* [05. Registro de interesados V_1_0_0.md](docs/01%20Inicio/05.%20Registro%20de%20interesados%20V_1_0_0.md) — *Matriz de Poder vs. Interés de stakeholders.*
* [06. Requisitos funcionales V_1_0_0.md](docs/01%20Inicio/06.%20Requisitos%20funcionales%20V_1_0_0.md) — *Macro-requisitos (MRF-01 a MRF-07), RF-001 a RF-018 y escenarios BDD.*
* [07. Requisitos no funcionales V_1_0_0.md](docs/01%20Inicio/07.%20Requisitos%20no%20funcionales%20V_1_0_0.md) — *Escenarios de Calidad ISO/IEC 25010 (RNF-001 a RNF-005).*
* [08. Usuarios V_1_0_3.md](docs/01%20Inicio/08.%20Usuarios%20V_1_0_3.md) — *Perfiles de usuario y Matriz RBAC (con restricción para Auditor).*
* [09. Reglas de negocio V_1_0_4.md](docs/01%20Inicio/09.%20Reglas%20de%20negocio%20V_1_0_4.md) — *Reglas RN-001 a RN-008 (bloqueos, capacidades, emisiones, horarios).*
* [10. Stack tecnológico V_1_0_3.md](docs/01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_3.md) — *Selección multicriterio de arquitectura 100% Código Abierto.*
* [11. Base de datos V_1_0_3.md](docs/01%20Inicio/11.%20Base%20de%20datos%20V_1_0_3.md) — *Modelo ER relacional en 3FN y extensiones geoespaciales PostGIS.*
* [12. Modelo C4 V_1_0_6.md](docs/01%20Inicio/12.%20Modelo%20C4%20V_1_0_6.md) — *Diagramas C4 de Contexto, Contenedores y Componentes Backend.*
* [13. Restricciones V_1_0_4.md](docs/01%20Inicio/13.%20Restricciones%20V_1_0_4.md) — *Análisis multidimensional de impacto, mitigación y LCC.*

---

### 📋 Fase 2: Planificación Ágil (`docs/02 Planificacion/`)
* [01_transformando_a_agil_v_1_0_0.md](docs/02%20Planificacion/01_transformando_a_agil_v_1_0_0.md) — *Transformación de requisitos a Épicas, US, Enablers y DoD global.*
* [02 Artefactos Jira V_1_0_0.md](docs/02%20Planificacion/02%20Artefactos%20Jira%20V_1_0_0.md) — *Configuración operativa en Atlassian Jira Software.*
* [03_registro_de_riesgos_v_1_0_0.md](docs/02%20Planificacion/03_registro_de_riesgos_v_1_0_0.md) — *Matriz de evaluación de riesgos PMBOK / CMMI.*
* [04_presupuesto_del_proyecto_v_1_0_0.md](docs/02%20Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md) — *Modelado financiero CAPEX, OPEX y Reserva de Contingencia.*

#### 🖼️ Evidencias de Jira Software (`docs/02 Planificacion/Capturas en JIRA/`)
* [01-roadmap.png](docs/02%20Planificacion/Capturas%20en%20JIRA/01-roadmap.png) — *Hoja de ruta con alineación de Épicas EP-01 a EP-07.*
* [02-backlog-priorizado.png](docs/02%20Planificacion/Capturas%20en%20JIRA/02-backlog-priorizado.png) — *Product Backlog con estimación en Story Points (Fibonacci).*
* [03-sprint-planning.png](docs/02%20Planificacion/Capturas%20en%20JIRA/03-sprint-planning.png) — *Planificación del Sprint 1 y Sprint Goal.*
* [04-tablero-scrum.png](docs/02%20Planificacion/Capturas%20en%20JIRA/04-tablero-scrum.png) — *Tablero Scrum activo con flujo To Do → Done.*
* [05-versiones-release.png](docs/02%20Planificacion/Capturas%20en%20JIRA/05-versiones-release.png) — *Configuración de versión `v1.0.0-MVP`.*

---

### 🚀 Fase 3: Implementación y Sprints (`docs/03 Implementación/`)

#### Sprint 1 — Fundación, flota y pedidos
* [01_informe_de_estado_del_proyecto_v_1_0_1.md](docs/03%20Implementaci%C3%B3n/Sprint%201/01_informe_de_estado_del_proyecto_v_1_0_1.md) — *Informe de estado (Plantilla 1, cierre documental 2026-10-26).*
* [02_registro_de_impedimentos_v_1_0_1.md](docs/03%20Implementaci%C3%B3n/Sprint%201/02_registro_de_impedimentos_v_1_0_1.md) — *Registro de impedimentos (Plantilla 2).*
* [03_revision_del_sprint_v_1_0_1.md](docs/03%20Implementaci%C3%B3n/Sprint%201/03_revision_del_sprint_v_1_0_1.md) — *Revisión del sprint con matriz de historias (Plantilla 3).*
* [04_retrospectiva_del_sprint_V_1_0_1.md](docs/03%20Implementaci%C3%B3n/Sprint%201/04_retrospectiva_del_sprint_V_1_0_1.md) — *Retrospectiva (Plantilla 4).*

#### Sprint 2 — Geocodificación y motor de rutas (`docs/03 Implementación/Sprint 2/`)
* [01_informe_de_estado_del_proyecto_v_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%202/01_informe_de_estado_del_proyecto_v_1_0_0.md) — *Informe de estado Sprint 2 (2026-10-26).*
* [02_registro_de_impedimentos_v_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%202/02_registro_de_impedimentos_v_1_0_0.md) — *Impedimentos Sprint 2 (IMP-010…; referencia IMP-001…009 en Sprint 1).*
* [03_revision_del_sprint_v_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%202/03_revision_del_sprint_v_1_0_0.md) — *Revisión del Sprint 2 con matriz US-005…EN-001.*
* [04_retrospectiva_del_sprint_v_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%202/04_retrospectiva_del_sprint_v_1_0_0.md) — *Retrospectiva Sprint 2 (borrador técnico; validación de equipo pendiente).*

#### Sprint 3 — Visualización, indicadores y soporte offline (`docs/03 Implementación/Sprint 3/`)
* [01 Revisión del Sprint V_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%203/01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) — *Estado real de US-010 a US-015 y EN-004, demostración pendiente y brechas DoD.*
* [02 Retrospectiva del Sprint V_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%203/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) — *Aprendizajes basados en evidencia y acciones propuestas pendientes de aprobación.*
* [03 Calidad de código V_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%203/03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md) — *Resultados reales de SonarQube, cobertura y deuda técnica.*
* [04 OWASP V_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%203/04%20OWASP%20V_1_0_0.md) — *Evaluación puntual OWASP Top 10:2025 y riesgos pendientes.*
* [05 WCAG V_1_0_0.md](docs/03%20Implementaci%C3%B3n/Sprint%203/05%20WCAG%20V_1_0_0.md) — *Evaluación WCAG 2.2 AA de pantallas renderizadas y verificaciones manuales pendientes.*

Los cinco documentos usan la versión documental inicial `V_1_0_0`. Este cierre no declara las historias Sprint 3 como *Done* ni acredita una Sprint Review/Retrospective celebrada; esas confirmaciones siguen pendientes del equipo.

---

### 💻 Código fuente activo
* [📁 Backend](app/) — *API REST en FastAPI, SQLAlchemy asíncrono y PostgreSQL/PostGIS.*
* [📁 Frontend](src/) — *Aplicación React, TypeScript, Vite, Tailwind, Leaflet y Recharts.*

---

## 🛠️ Stack Tecnológico (100% Código Abierto)

| Componente | Tecnología Seleccionada | Justificación |
| :--- | :--- | :--- |
| **Backend API** | Python 3.11 + FastAPI | Asincronía, alto rendimiento, documentación automática OpenAPI/Swagger. |
| **Motor VRPTW / Green VRP** | Algoritmo genético propio | Implementado en `app/services/genetic_solver.py`; OR-Tools y DEAP no figuran en manifiestos activos. |
| **Base de Datos Geoespacial** | PostgreSQL 15 + PostGIS 3 | Persistencia activa con SQLAlchemy/GeoAlchemy y geometrías SRID 4326; la decisión `geometry`/`GEOGRAPHY` sigue pendiente de consolidación. |
| **Frontend Web** | React.js + Tailwind CSS | Interfaz modular e interactiva para operadores logísticos. |
| **Móvil / Conductor** | React.js + PWA parcial | Vista de conductor, IndexedDB, Service Worker y cola de sincronización implementados; faltan pruebas extremo a extremo de desconexión, reconexión y no duplicidad para acreditar EN-004 como *Done*. |
| **Cartografía y Ruteo** | Leaflet + distancia geodésica; OSRM opcional | OSRM está apagado por defecto y no forma parte de `docker-compose.yml`. |
| **Tareas asíncronas** | Sin servicio separado implementado | Redis/Celery pertenecen a la arquitectura prevista, no al runtime actual |

---

## 👥 Equipo del Proyecto

* **Project Manager (PM)**: Nikole Celeste Bastidas Vilca
* **Software Architect & Lead Dev**: Dante Edgar Chuquirachi Martinez
* **DevOps & Data Engineer**: Hernan Anibal Osorio Diaz
* **Calidad y desarrollo backend**: Geraldine Paola Gómez Toribio
* **Frontend Developer**: BryanY29
