# Sprint 4 — índice de evidencia técnica (fase 3)

Fecha 17/11/2026, America/Lima, V_1_0_0. Raíz `C:/Users/Baguette/Documents/Proyectos/ecologistica-junin`. HEAD `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1` con cambios B-08 previos sin commit; ese árbol fue probado. La identificación por commit solo no representa esos cambios: el control final de hashes debe confirmar que estas fases no alteraron código/pruebas/configuración.

## 1. Evidencia verificada ahora

| ID | Fuente / ruta | Dato y corte | Límite |
|---|---|---|---|
| E-01 | [backend_junit.xml](FASES_3_4_5_EVIDENCIAS/backend_junit.xml), [backend_pytest.log](FASES_3_4_5_EVIDENCIAS/backend_pytest.log), backend_exit.txt | 185 aprobadas, salida 0, fecha 17/11; incluye 14 B-08 BD | Unidad/integración ASGI/PostGIS/WS TestClient; no navegador continuo. |
| E-02 | [backend_coverage.json](FASES_3_4_5_EVIDENCIAS/backend_coverage.json), backend_coverage.xml, coverage_backend_data | 83,27% líneas,59,98% ramas,78,68% combinado; corriente actual | Mide ejecución del conjunto; no aceptación RF ni cobertura de estándares. |
| E-03 | [frontend_results.json](FASES_3_4_5_EVIDENCIAS/frontend_results.json), [frontend_vitest.log](FASES_3_4_5_EVIDENCIAS/frontend_vitest.log), frontend_exit.txt | 68 aprobadas/1 fallida de69, salida 1 | Mocks de API y DOM; no integración con BD desde UI. |
| E-04 | [frontend_coverage/coverage-summary.json](FASES_3_4_5_EVIDENCIAS/frontend_coverage/coverage-summary.json), lcov y HTML acompañantes | 78,80% líneas,70,80% ramas,76,76% sentencias | Cobertura generada incluso con fallo; configuración vigente, no comparar indiscriminadamente con Sonar. |
| E-05 | [casos_prueba.json](FASES_3_4_5_EVIDENCIAS/casos_prueba.json) | 254 casos backend/frontend con ID/fuente/criterio/resultado/fecha | Correspondencia de familias RF/RNF orientativa; aceptación completa en matriz. |
| E-06 | [benchmark_solver_actual.json](FASES_3_4_5_EVIDENCIAS/benchmark_solver_actual.json) | Tres semillas 150 ×15; 150 asignados en cada una,0 factibles; parámetros/timestamp originales | Solver/geodesia; no HTTP/OSRM/BD ni testigo factible. No acredita 45 s/<30 s. |
| E-07 | [resumen_ejecucion.json](FASES_3_4_5_EVIDENCIAS/resumen_ejecucion.json) | Hardware/runtime descritos en informe; contenedor/puerto/almacenamiento y SHA del HTML fuente | Datos de ejecución y aislamiento, sin credenciales reales. |
| E-08 | Salida de `tsc --noEmit --incremental false`, script SW y auditoría dist; comandos en resultados | Tipado 0; 4/4 SW; dist estático aprobado 434.872 B,17/11 | No hubo build nuevo; fuente scripts/test-service-worker.mjs y scripts/audit-green-build.mjs. |
| E-09 | Código actual `app/`, `src/`, `tests/`; [defectos](SPRINT4_DEFECTOS_PENDIENTES.md) | Paths/métodos y evidencia estática actual para DEF-01…16 | Inspección no es explotación, SCA ni certificación. |

Todos estos resultados se obtuvieron con imagen PostGIS local en contenedor exclusivo tmpfs, loopback 25435 y sin volumen existente. Se detuvo al terminar. Las fixtures mutaron únicamente ese entorno sintético. No se publicó servidor operativo ni se usaron datos de clientes reales.

## 2. Fuentes históricas y estimaciones

| Fuente / ruta | Fecha/versionado disponible | Uso correcto |
|---|---|---|
| Cinco informes originales en AUDITORIA y cuatro planes de fase 1 | Corte 16/11 y planificación 17/11; referencia antigua 967 efdf | Hallazgos/alcance/dependencias. 53,5%,67,1%,26% son estimaciones, no pruebas nuevas ni EV. |
| SPRINT 4_B08_RESULTADOS.md |17/11, estado previo sin PostGIS | Evidencia de implementación y67 pruebas; la limitación de14 casos fue superada en E-01, sin sobrescribir historia. |
| `docs/01 Inicio/02. Acta de constitución V_1_0_0.md` |25/08/2026; objetivos,14 semanas; presupuesto referencial pendiente | Charter y adaptación local documentados; no BAC aprobado. |
| `docs/01 Inicio/01. Selección del enfoque del proyecto V_1_0_0.md`, visión y supuestos |Documentos de inicio 2026 | Documentan adaptación Lima→Huancayo/El Tambo/Chilca. No atribuir geografía adaptada al texto original no localizado. |
| `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` |15/09/2026 | Backlog US/EN/DoD y Gherkin; no historial diario ni aceptación final. |
| `docs/02 Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md` |15/09/2026; USD 134.400/3000 h planificadas | Estimación:120.000+14.400 contingencia; conversión histórica 3,72. No AC ni aprobación BAC. |
| Registro de riesgos `docs/02 Planificacion/03_registro_de_riesgos_v_1_0_0.md` |15/09/2026, título agrega v2 | RIE-001…010 y respuestas propuestas; actualizar evidencia de aplicación, sin inventar impactos. |
| Cuatro documentos de Sprint 1 y cuatro de Sprint 2 |Corte documental 26/10/2026 | Sprint 1 20 SP/0 Done; Sprint 2 34 SP/0 Done en sus cortes; no equivalencia SP→horas/dinero. Retros contienen propuestas/borradores. |
| Revisión/retro Sprint 3, calidad/OWASP/WCAG |Versiones internas distintas; algunos cortes sin fecha precisa | Declaraciones 143/68 y136/67 y métricas Sonar son históricas y contradictorias, no resultados de E-01/03. No aceptación formal automática. |
| Dos documentos Green IT de reducción de impacto ambiental |10/11/2026 | Prácticas y límites; ejemplo 112,5→101,25 gCO₂e es hipotético, no ahorro medido. |
| Modelo C4/BD/stack y requisitos en docs/01 Inicio |Baseline previsto | Conciliar GA/Geometry actuales frente a diseño OR-Tools/GEOGRAPHY/servicios previstos; no garantiza esquema físico de instancias externas. |
| Cinco PNG Jira en `docs/02 Planificacion/Capturas en JIRA/` |Fechas visibles 2024; procedencia/exportación no verificada | Archivos existentes genuinos como evidencia aportada, no captura nueva ni prueba de estado 2026. Backlog muestra 39 aunque filas suman 47; planning 34 difiere de20 SP de acta. |

## 3. Fuentes no disponibles y evidencia no ejecutada

- Consigna inicial original: no localizada en repositorio/adjuntos actuales; solo referencias históricas. No se reconstruye.
- HTML final: disponible en Downloads, leído con sus secciones 1–5; [plantillas_fuente.json](FASES_3_4_5_EVIDENCIAS/plantillas_fuente.json) conserva títulos/campos/tablas/fórmulas extraídos de las siete plantillas. Ruta exacta y SHA-256 en resumen_ejecucion.json. No se ejecutó HTML ni se copió fuera de ubicaciones autorizadas.
- Capítulos de referencia citados por la consigna: textos no disponibles; no se atribuye contenido no leído.
- BAC aprobado, cronograma detallado/costos por periodo, aceptación monetizada, horas/devengos/AC y cambios aprobados: no disponibles. EVM no calculable.
- Series burndown/burnup/CFD, Mood, capturas retrospectiva actual y exportación Jira confiable: no disponibles. No se fabricaron gráficos/capturas.
- Encuesta de satisfacción, reunión/acta de cierre, aprobación administrativa, exenciones y transferencia: no disponibles.
- Nuevo Sonar/SCA, WCAG integral, tráfico/OSRM real, E2 E navegador, disponibilidad/carga y video: no ejecutados/no producidos. No hay MP4 verificable.

## 4. Documentos de interpretación

- [Resultados y comandos](SPRINT4_RESULTADOS_PRUEBAS.md).
- [Matriz de aceptación](SPRINT4_MATRIZ_ACEPTACION.md).
- [Defectos, reproducción y propuestas](SPRINT4_DEFECTOS_PENDIENTES.md).
- [Control de puertas](CONTROL_FASES_3_4_5.md).

Estos documentos distinguen ejecución actual, inspección, historia, estimación y ausencia; solo los resultados originales de esta carpeta respaldan las cifras actuales. Nuevos reportes de cierre conservarán estado borrador mientras falten datos/aprobaciones.
