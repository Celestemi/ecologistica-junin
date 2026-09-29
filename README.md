# 🌱 EcoLogística Huancayo — Optimizador de Rutas Sostenibles

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg)](https://react.dev/)
[![PostGIS](https://img.shields.io/badge/PostgreSQL-15%20%2B%20PostGIS%203-336791.svg)](https://postgis.net/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![Sprint](https://img.shields.io/badge/Sprint-1%20Completado-success.svg)](#)

Sistema web y móvil (PWA) de optimización de rutas de reparto de última milla para **DistriRápido S.A.C.** en los distritos de **Huancayo, El Tambo y Chilca** (provincia de Huancayo, Junín). Integra algoritmos de ruteo vehicular con ventanas de tiempo (**VRPTW**) y criterios ecológicos (**Green VRP**).

---

## 🎯 Objetivos Principales (SMART)

* 🚗 **Reducción de Distancia**: Disminución ≥ 15% frente a la ruta secuencial sin optimizar.
* 🌿 **Reducción de Emisiones**: Reducción ≥ 10% mensual de CO₂ basada en factores oficiales de combustible.
* ⏰ **Cumplimiento de Ventanas Horarias**: Nivel de cumplimiento ≥ 90% (incumplimiento ≤ 10%).
* ⚡ **SLA de Rendimiento**: Generación de ruta en ≤ 45 s (150 pedidos / 15 vehículos) y re-optimización en ≤ 30 s.

---

## 📁 Estructura del Repositorio

```text
ecologistica-junin/
├── 📄 README.md
├── 📄 .gitignore
│
├── 📁 docs/
│   │
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
│   │
│   ├── 📁 02 Planificacion/
│   │   ├── 📁 Capturas en JIRA/
│   │   │   ├── 🖼️ 01-roadmap.png
│   │   │   ├── 🖼️ 02-backlog-priorizado.png
│   │   │   ├── 🖼️ 03-sprint-planning.png
│   │   │   ├── 🖼️ 04-tablero-scrum.png
│   │   │   └── 🖼️ 05-versiones-release.png
│   │   │
│   │   ├── 📄 01_transformando_a_agil_v_1_0_0.md
│   │   ├── 📄 02 Artefactos Jira V_1_0_0.md
│   │   ├── 📄 03_registro_de_riesgos_v_1_0_0.md
│   │   └── 📄 04_presupuesto_del_proyecto_v_1_0_0.md
│   │
│   └── 📁 03 Implementación/
│       ├── 📄 01_informe_de_estado_del_proyecto_v_1_0_0.md
│       ├── 📄 02_registro_de_impedimentos_v_1_0_0.md
│       ├── 📄 03_revision_del_sprint_v_1_0_0.md
│       └── 📄 04_retrospectiva_del_sprint_V_1_0_0.md
│
└── 📁 EcologisticaJunin/
    ├── 📁 backend/
    └── 📁 frontend/
