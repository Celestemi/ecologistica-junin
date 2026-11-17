# Evidencias disponibles y faltantes — preparación del Sprint 4

**Corte:** 17/11/2026, America/Lima. **Versión:** 1.0.0. **Commit:** `61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1`.

Raíz confirmada por el usuario: `C:/Users/Baguette/Documents/Proyectos/ecologistica-junin`. `Proyectos2` no está disponible. Rutas de este inventario relativas a la raíz, salvo las fuentes externas locales expresamente indicadas. Alcance: inspección de archivos y comprobaciones de lectura; no acceso al proyecto Jira remoto, CI remoto, sistema desplegado ni BD activa.

Compañeros: [plan](PLAN_SPRINT_4.md), [matriz de consigna](MATRIZ_CONSIGNA_FINAL.md), [protocolo de validación](PLAN_VALIDACION_SISTEMA.md). «Existe» identifica un artefacto; no certifica su contenido, aceptación ni vigencia.

## 1. Fuentes revisadas y ausencias

| ID | Fuente localizada | Información utilizable | Límite o falta |
|---|---|---|---|
| D-01 | Los cinco informes `AUDITORIA/AUDITORIA_ESTADO_ACTUAL.md`, `ANALISIS_SPRINTS.md`, `CUMPLIMIENTO_REQUERIMIENTOS.md`, `BACKLOG_IMPLEMENTACION.md`, `RESUMEN_EJECUTIVO.md` | Hallazgos, correspondencias RF/RNF, B-01…34 y E-01…03, estados y método de estimación | Corte 16/11, referencia `967efdf`, ruta antigua Proyectos2. Porcentajes son estimaciones técnicas; varios artefactos ignorados actuales difieren de los descritos. No se sobrescribieron. |
| D-02 | `docs/01 Inicio/02. Acta de constitución V_1_0_0.md` | Propósito, PM, objetivos, 14 semanas, hitos 2/3/7/11/14, presupuesto referencial y riesgos macro | S/500.000 desarrollo y S/120.000 operación anual explícitamente pendientes de validación local; no acta de aprobación económica vigente. |
| D-03 | `docs/01 Inicio/01. Selección del enfoque del proyecto V_1_0_0.md`, `03. Declaración de la visión V_1_0_0.md`, `04. Registro_de_Supuestos_y_Restricciones_EcoLogistica_Huancayo_V1.0.0.md`, `05. Registro de interesados V_1_0_0.md` | Justificación híbrida, supuestos, interesados y objetivos | No se encontró Plan de Gestión integral autónomo aprobado; estos documentos son insumos parciales. Interesados descritos no prueban satisfacción ni participación real. |
| D-04 | `docs/01 Inicio/06. Requisitos funcionales V_1_0_0.md`, `07. Requisitos no funcionales V_1_0_0.md`, `08. Usuarios V_1_0_3.md`, `09. Reglas de negocio V_1_0_4.md`, `13. Restricciones V_1_0_4.md` | Catálogo MRF/RF atómicos, BDD, calidad, roles, reglas y restricciones | No hay una matriz final única de requisito×prueba×resultado×aceptante. Conciliar catálogo auditado de 10 RF/7 RNF con interno de 18 RF/5 RNF, y restricciones normativas pendientes. |
| D-05 | `docs/02 Planificacion/01_transformando_a_agil_v_1_0_0.md` | Épicas, US/EN, Gherkin y DoD: ≥80 % cobertura, análisis, revisión de pares, staging y API | Catálogo de backlog, no historial de transiciones, aceptación, costos ni distribución presupuestaria temporal. OR-Tools/Celery previstos difieren de implementación. |
| D-06 | `docs/02 Planificacion/02 Artefactos Jira V_1_0_0.md` y cinco PNG en `Capturas en JIRA/` | Imágenes de roadmap, backlog, planning, tablero y releases, inspeccionadas visualmente | Fechas visibles 2024 frente a documentos 2026; discrepancias de puntos e IDs; sin exportación verificable ni procedencia/fecha de captura. No acreditan estado actual ni serie histórica. |
| D-07 | `docs/02 Planificacion/04_presupuesto_del_proyecto_v_1_0_0.md` | Modelo de costos por rol/herramientas/cloud y contingencia; cifras detalladas en §4 | Es presupuesto estimado, no costos ejecutados, BAC aprobado ni línea base distribuida por trabajo/periodo. |
| D-08 | `docs/02 Planificacion/03_registro_de_riesgos_v_1_0_0.md` | RIE-001…010, probabilidad/impacto, exposición y responsables sugeridos por rol | Título conserva V_1_0_0 y agrega «v2»; sin control de cambio equivalente. Actualizar estado, impacto real y respuestas aplicadas, no solo propuestas. |
| D-09 | `docs/03 Implementación/Sprint 1/01_informe_de_estado_del_proyecto_v_1_0_1.md`, `02_registro_de_impedimentos_v_1_0_1.md`, `03_revision_del_sprint_v_1_0_1.md`, `04_retrospectiva_del_sprint_V_1_0_1.md` | 20 SP comprometidos y 0 SP Done según DoD en su corte; IMP-001…009, aprendizaje y propuestas | No costos/horas reales. Enlaces a informes eliminados; las propuestas de retro no son compromisos aprobados ni evidencia de ceremonia. |
| D-10 | Los cuatro `.md` de `docs/03 Implementación/Sprint 2/` | 34 SP comprometidos, 0 SP Done en su corte; US-005/007/008/009, EN-001; IMP-010…013 y reaperturas | Mediciones narrativas con fuentes eliminadas; retrospectiva declara ser borrador no validado; falta aceptación integral con servicio real y commit. Frase sobre factibilidad «feasible=false en 0/5» es ambigua y no se toma como prueba. |
| D-11 | `docs/03 Implementación/Sprint 3/01 Revisión del Sprint V_1_0_0.md`, `02 Retrospectiva del Sprint V_1_0_0.md` | Declaran 143 backend/68 frontend, build y US-010…015/EN-004 cumplidas | Contradicen README y auditoría técnica; no aportan aquí acta, asistentes, commit ni resultados originales suficientes para resolver todas las brechas. |
| D-12 | `docs/03 Implementación/Sprint 3/03 Calidad de código V_1_0_0.md`, `04 OWASP V_1_0_0.md`, `05 WCAG V_1_0_0.md` | Evaluaciones históricas, vulnerabilidades/contexto, accesibilidad parcial, pendientes | Calidad tiene versión interna V_1_1_0 con nombre V_1_0_0; conteos 136/67 y 143/68 corresponden a referencias distintas. «Revisión general» no es fecha/commit identificable. No equivalen a cumplimiento integral ni estado actual. |
| D-13 | Los dos `.md` de `docs/03 Implementación/reduccion del impacto ambiental/` | Prácticas Green IT y estándares, límites, tamaños históricos y metodología futura | Escenario de 112,5→101,25 g CO₂e por 1.000 visitas es hipotético; no huella medida del proyecto ni ahorro de transporte. No usar en cierre como resultado real. |
| D-14 | `docs/01 Inicio/10. Stack tecnológico V_1_0_3.md`, `11. Base de datos V_1_0_3.md`, `12. Modelo C4 V_1_0_6.md`, `00. Directrices y Auditoria V_1_0_3.md` | Arquitectura y ER/SQL de diseño, reglas de versionado | Diseño histórico OR-Tools/GEOGRAPHY/servicios previstos frente a GA/Geometry/runtime actual; enlaces de vigencia apuntan a documento eliminado. No prueba esquema físico. |
| D-15 | `README.md`, `package.json`, `pyproject.toml`, `app/__init__.py`, `.github/workflows/ci.yml`, `.gitignore`, configuración Docker/Nginx y Git | Navegación, módulos/capas, versiones 0.1.0 consistentes, pipeline y reglas de exclusión | Sin siete reportes finales, guía operativa completa ni despliegue staging real. Badge passing estático sin vínculo a corrida. |
| D-16 | `app/`, `src/`, `tests/`, pruebas frontend, scripts de SW/build | Caminos conectados y pruebas escritas para roles, pedidos, solver, mapas, PDF y offline | No se ejecutó suite backend/frontend integrada ni API/BD. Faltan regresiones sobre versión vigente, carreras y aceptación final. |
| D-17 | `coverage.xml`, `coverage/frontend/coverage-summary.json`, `coverage/frontend/lcov.info`, `en001_benchmark_last.json`, `dist/` | Artefactos locales históricos/no rastreados, inspeccionados en este corte | No derivar autoría ni ejecución actual. Valores actuales distintos de la auditoría anterior: véase §2. |
| D-18 | `C:/Users/Baguette/Downloads/Consigna de evaluación final y cierre del proyecto.html` | Secciones 1–5 completas: requisitos, rúbrica y siete plantillas | Archivo local leído, sin copia ni ejecución de su HTML. Instrucciones del documento tratadas como criterios de evaluación futuros, no como autorización para implementar ahora. |
| D-19 | Consigna inicial original | No localizada en archivos del proyecto, adjunto actual ni búsqueda de nombres pertinentes en Downloads | Solo se dispone de referencias en acta/visión/auditoría. No se reconstruye ni afirma haber leído su texto original. Solicitar fuente al preparar baseline. |
| D-20 | Capítulos `Reporting for Hybrid Projects` y `Corrective Actions and Closure` citados en la consigna | Sus títulos y exigencia de alineación aparecen en HTML | Textos originales no disponibles en los materiales revisados; no se atribuyen definiciones adicionales no proporcionadas. |

Tampoco se localizaron como artefactos vigentes independientes: cronograma detallado aprobado con dependencias/ruta crítica y costos por periodo; registros de horas reales/costos/aceptación económica; registro de rebaselining aprobado; resultados finales de aceptación; encuesta de satisfacción; reunión y acta de cierre; siete documentos de `docs/04 Cierre`; MP4 y guion final en `docs/05 Video proyecto`. No se deduce ausencia en servicios externos a partir de la ausencia local.

## 2. Comprobaciones ejecutadas en esta revisión

| ID | Comprobación estrictamente de lectura | Resultado y alcance |
|---|---|---|
| C-01 | `git status --short`, `git log`, `git tag --list`, diff `967efdf…HEAD` | Inicio limpio; HEAD `61f0e1e` del 17/11/2026; sin tags locales. Diff: cinco altas de auditoría y dieciocho bajas documentales; sin cambio de fuentes/config. Ningún fetch, checkout, add ni commit. |
| C-02 | SHA-256 en memoria | Inventario de 193 archivos rastreados fuera de AUDITORIA antes de las comprobaciones; inventario ampliado de 403 archivos antes de generar los nuevos documentos, excluyendo `.git`, `node_modules`, `.venv`. El ampliado incluye informes originales, artefactos y cachés. Control final de igualdad y altas limitado a estos árboles; no vigilancia del sistema entero. |
| C-03 | `node node_modules/typescript/bin/tsc --noEmit --incremental false` | Código de salida 0; tipado válido, sin emisión ni instalación. No prueba UX, red ni backend. |
| C-04 | `node --test scripts/test-service-worker.mjs` | 4 aprobadas, 0 fallidas; usa VM y cachés simuladas en memoria. No acredita entrega offline real ni IndexedDB concurrente. |
| C-05 | `node scripts/audit-green-build.mjs` sobre `dist` existente | **Aprobado**; 434.872 B totales de JS/CSS, precaché incluye conductor/login y excluye OrdersDay según script. Compresión calculada en memoria. No build nuevo ni tráfico HTTP medido. **Difiere del fallo narrado el 16/11**: dist es ignorado y su procedencia no está vinculada al commit; no inferir reparación de código ni despliegue actual. |
| C-06 | Análisis estático de enlaces Markdown en README + 33 `.md` rastreados de docs | 34 archivos, 115 referencias relativas a archivos, 31 ocurrencias con destino ausente, seis destinos distintos; ninguna rota desde README. Excluye enlaces web, fragmentos y formatos no capturados por la expresión de enlaces inline; no es auditoría completa de anchors/HTTP. |
| C-07 | `git check-ignore -v --no-index` con rutas de prueba que no se crearon; índice Git | Exclusiones funcionan para node_modules, .venv, dist, coverage, .pytest_cache, egg-info, .sonarqube-temp, `.env` y variantes; `.env.example` permitido por excepción. No hay esos árboles residuales ni `.env` privado rastreados; `.env.example` sí. |
| C-08 | Sondeo de nombres de claves/backups y patrones de secretos en archivos rastreados actuales | Sin coincidencias para cabeceras de claves privadas, tokens GitHub con formato examinado y claves AWS AKIA. `.pem`, `.key`, `.p12`, `.sql` y `.bak` genéricos no tienen exclusión por estos nombres de prueba. Se observan credenciales/valores demo en configuración; no se reproducen secretos en los informes. No se hizo un escaneo exhaustivo ni de todo el historial Git. |
| C-09 | Lectura de XML/JSON locales de cobertura | XML: 2.784/4.306 líneas = **64,65 %**, 343/1.044 ramas = **32,85 %**, timestamp `2026-10-27T17:41:36.999Z`. Resumen frontend: 47/362 líneas = **12,98 %**, 19/28 ramas = **67,85 %**, alcance parcial de seis módulos de lib. **No** son una corrida nueva ni métricas comparables automáticamente a cobertura global publicada. |
| C-10 | Lectura de `en001_benchmark_last.json` | 150×15: cinco repeticiones, media solver ~0,8883 s, 150 asignados, ratio factible **0,0** y última factible false. Dataset pequeño 5×2: ratio 1,0. Es artefacto histórico sin fecha/commit suficientes y sin HTTP/OSRM real demostrado; asignar todos no prueba restricciones. |

Los scripts ejecutados se inspeccionaron antes: leen archivos y operan en memoria; no escriben resultados/cachés. No se ejecutaron instaladores, build, Vitest/coverage, pytest, SonarScanner, Docker, inicializadores, API del proyecto ni migraciones. `tests/conftest.py` crea BD y trunca tablas; `backend/entrypoint.sh` invoca inicialización de BD. Ni siquiera un GET se considera automáticamente inocuo por su verbo.

### Diferencias con la evidencia previa

- La auditoría previa cita 81,07 % líneas backend, 55,17 % ramas, 76,02 % combinado y 90,91 % líneas frontend. Los artefactos actuales de C-09 tienen otros valores/alcances. `coverage/backend-coverage-final.json`, citado anteriormente, **no existe actualmente**. No reemplazar una fuente por la cifra más favorable ni llamar a la diferencia «regresión» sin corrida comparable.
- El documento Sonar D-12 declara 82,1 % global y gate de código nuevo OK junto con incidencias históricas. Son métricas declaradas de otro análisis; no se consultó servidor ni se suman/promedian con C-09.
- Dist pasó hoy sin regeneración. La corrección de B-20 debe comenzar verificando procedencia y actualización, no dando por vigente el fallo anterior.
- Las dieciocho eliminaciones de la auditoría previa ya están en el commit actual; no son eliminaciones nuevas de este trabajo.

## 3. Trazabilidad y credibilidad documental

### Enlaces con destino ausente

Las 31 ocurrencias de C-06 apuntan a estos seis archivos; se mantienen como ausentes, sin restaurarlos ni crear sustitutos:

1. `docs/ESTADO_TECNICO_VIGENTE.md`.
2. `Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_VERIFICACION_DOD_SPRINT_1.md`.
3. `Auditorias-EcoLogistica/02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_1.md`.
4. `Auditorias-EcoLogistica/03_Reportes_Verificacion/VERIFICACION_FINAL_SPRINT_2.md`.
5. `Auditorias-EcoLogistica/02_Planes_Implementacion/PLAN_IMPLEMENTACION_SPRINT_2.md`.
6. `Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_RENDIMIENTO_EN_001.md`.

El historial Git permite rastrear que hubo esos documentos; no se recuperaron versiones antiguas para hacerlas pasar por evidencia vigente. Una fase futura puede recuperar fuentes legítimas con fecha/commit o reemplazar referencias con una decisión documentada.

### Inspección visual de las cinco imágenes Jira

| Imagen | Observación directa | Uso admisible pendiente de conciliación |
|---|---|---|
| `01-roadmap.png` | Eje septiembre–diciembre **2024**, ocho épicas ELH-1…8 | Ilustra planificación, pero no baseline temporal aprobada de 2026. Falta exportación y correspondencia a EP/US. |
| `02-backlog-priorizado.png` | Sprint 1 01–31/10/2024; ocho filas; cabecera estima **39**, puntos visibles suman **47** | Conciliar suma, selección y fecha con fuente original. No usar ese total para velocidad, presupuesto ni burndown. |
| `03-sprint-planning.png` | 01–31/10/2024, 4 semanas, siete ítems y **34 SP** | Difiere de Sprint 1 documental con 20 SP de 2026; no inferir cambio aprobado ni mezclar con los 34 SP del Sprint 2. |
| `04-tablero-scrum.png` | Columnas To Do/In Progress/In Review/Done con tarjetas e iniciales | Evidencia visual parcial de tablero; no fecha/corte actual, transiciones ni acta que pruebe Done contra DoD. |
| `05-versiones-release.png` | MVP lanzado 31/10/2024 al 100 %, versión 2.0 planificada para 15/12/2024 | No prueba release actual; paquete/backend siguen 0.1.0 y no hay tags locales. No afirmar lanzamiento de 2026 con esta imagen. |

No se juzga autenticidad ni se atribuye manipulación: son archivos aportados sin exportación de origen verificable. Se requiere procedencia e historial real. No editar fechas de una captura para simular ejecución actual.

### Versiones y arquitectura

`package.json`, `pyproject.toml` y `app/__init__.py` coinciden en 0.1.0; esto es coherencia de código, no evidencia de release 1.0. Documentos de inicio tienen versiones heterogéneas con intención histórica; no hace falta uniformarlas artificialmente. Sí se debe resolver nombre V_1_0_0/contenido V_1_1_0 del reporte de calidad y «V_1_0_0 (v2)» de riesgos, registrar cambios y actualizar versiones según impacto en futura fase.

Separación actual: `src/` React/TS y `app/` FastAPI/servicios/modelos; `frontend/` y `backend/` contienen despliegue. Es monorepo modular; no necesita mover archivos solo para obtener carpetas llamadas frontend/backend. README representa esta organización y enlaza documentos actuales. Sus badges passing/MIT no prueban ejecución ni licencia incorporada. Faltan guía completa de arranque/configuración/migración/recuperación y enlaces finales de cierre; preservados sin modificación ahora.

Hay residuos locales ignorados (`node_modules`, `.venv`, `dist`, coverage, caches, egg-info). Distinguir copia de trabajo de repositorio entregado: no están rastreados, pero no empaquetarlos ni eliminarlos en esta fase. Las exclusiones genéricas de claves/backups pueden reforzarse posteriormente según política del equipo. Valores demo son riesgo de configuración si se usan fuera de demo, no prueba de una credencial productiva filtrada. No se acredita saneamiento histórico de secretos sin revisión específica.

## 4. Auditoría económica y de valor ganado

### 4.1 Datos que sí existen

| Fuente / cifra | Naturaleza comprobable | Uso permitido |
|---|---|---|
| Acta: S/500.000 desarrollo y S/120.000 operación anual | Referencial/histórico, pendiente de validación local explícita en §6 | Contexto y contradicción por resolver; **no BAC aprobado ni AC**. No sumar O&M anual al presupuesto del desarrollo sin decisión. |
| Presupuesto D-07: RR.HH. USD105.000, licencias USD4.200, infraestructura USD10.800 | Estimación detallada; subtotal USD120.000 | Conciliar rubros/alcance antes de aprobar baseline. Licencias/OPEX del desarrollo no prueban facturas ni uso. |
| Contingencia 12 % = USD14.400; total estimado USD134.400 | Aritmética reproducible: 120.000×0,12; total 120.000+14.400 | Decidir tratamiento de reserva y BAC con aprobación; no confundir contingencia con reserva de gestión. |
| Tipo de cambio referencial 3,72; equivalencia S/499.968 | 134.400×3,72 | Conversión histórica del modelo, no tipo de cambio actual ni evidencia de aprobación. Diferencia S/32 frente a meta referencial no demuestra aprobación. |
| 3.000 h asignadas por rol | PM480, arquitecto360, senior640, junior640, QA480, UX400; tarifas USD40/50/40/25/30/29,50 respectivamente | Base de estimación, **no horas realizadas** ni capacidad actual de los integrantes académicos. |
| Acta: 14 semanas/4 iteraciones; hitos semanales | Cronograma de alto nivel | Insumo para reconstruir baseline validada; no PV periódico ni ruta crítica detallada. |
| Revisiones: Sprint 1 20 SP y Sprint 2 34 SP; código y tests | Compromisos/documentos y trabajo parcialmente implementado | Inventariar trabajo a valorar. SP y porcentajes de auditoría no son dinero ganado. |
| IMP-008 figura resuelto por elaborar modelo presupuestario | Declaración histórica de resolución documental | No acredita autorización financiera; resolver contradicción con acta pendiente. |

### 4.2 Datos faltantes y dónde deberán registrarse

Los registros siguientes son **destinos futuros propuestos**, no archivos creados hoy. Pueden mantenerse como anexos versionados de los documentos de planificación/gestión y del reporte EVM final; evitar dispersar fuentes maestras contradictorias.

| Dato | Falta exacta | Registro futuro y campos mínimos | Validación / rol sugerido |
|---|---|---|---|
| BAC | Monto/base/alcance/moneda y fecha aprobados; vigencia y tratamiento de contingencia/gestión | Presupuesto versionado de `docs/02 Planificacion/04…` + decisión: versión, paquetes, monto, reservas, moneda, aprobador y evidencia | PM y autoridad competente confirman aprobación. Acta limita autoridad PM sobre presupuesto institucional. |
| Línea base costo-cronograma | Paquetes valorados por periodo, inicio/fin/dependencias y corte | Anexo de cronograma y presupuesto: ID WBS/US, requisito, presupuesto, fecha planificada, periodo, PV previsto, versión/aprobación | Suma presupuestos de trabajo = BAC acordado con reglas de reserva; PV acumulado no excede alcance presupuestado. |
| PV | Importe programado al corte anterior y actual | Libro EVM por periodo: corte, baseline, PV periodo/acumulado, fuente | PM; sumar planificación aprobada, no repartir BAC linealmente por semanas sin baseline. |
| EV | Trabajo realmente completado y aceptado por paquete; regla de acreditación preacordada | Registro de aceptación: ID, presupuesto base, regla 0/100 u hitos ponderados acordados, cantidad aceptada, fecha, aceptante, evidencia/commit | Aceptante + QA; valorar al costo presupuestado. No tomar 53,5 %, 67,1 % ni 26 % como EV. No asumir EV=0 por evidencia incompleta. |
| AC | Horas realizadas, costos incurridos, periodo y soporte | Registro de horas: fecha, persona/rol, ID trabajo, horas, validación; libro de costos: comprobante/soporte, fecha devengo, monto/moneda, cambio si corresponde, paquete y pago pendiente | Responsable de costos concilia horas/tarifas aplicables y facturas/devengos; no reemplazar AC por presupuesto. |
| Cortes comparables | Periodo anterior/actual, acumulados y consistencia de alcance/moneda | Libro EVM: periodo, corte, PV/EV/AC del periodo y acumulados, vínculo a evidencia y responsable | Incremento = acumulado actual−anterior, sin doble conteo; cierre del mismo periodo para las tres magnitudes. |
| Cambios/replanificación | Solicitud, impacto, aprobación y efecto en baseline; historia no borrada | Registro de cambios ligado a acta/backlog/cronograma/presupuesto: ID, motivo, alcance/costo/plazo antes/después, fecha, aprobador, versión efectiva | PM/evaluador según autoridad; comparar ejecución tanto con baseline vigente como con original cuando proceda. |
| Costo final y transición | Cierre de obligaciones y aceptación final | Futuro reporte final + acta de cierre: costos conciliados, pendientes/reservas, aceptación, responsables de transferencia | No declarar costo final ni fecha de cierre mientras falte evidencia. |

Si no se registraron horas/costos históricos, recolectar solo soportes reales identificables, marcar cobertura y lagunas y registrar desde ahora. No reconstruirlos a partir de commits, SP o recuerdo como si fueran medición. Costos de combustible/KPI logísticos del producto no son automáticamente costos del desarrollo EVM.

### 4.3 Calculabilidad al corte

**No es posible producir hoy una serie EVM numérica defendible.** Hay modelo estimado, pero faltan BAC aprobado, PV temporal, EV aceptado valorado y AC sustentado. Ausencia no equivale a cero.

| Indicador solicitado | Entradas/condición | Estado actual |
|---|---|---|
| SV = EV − PV | EV y PV del mismo periodo/base monetaria | No calculable; faltan ambos. Es variación en unidades de presupuesto, no días. |
| CV = EV − AC | EV y AC comparables | No calculable; faltan ambos. |
| SPI = EV / PV | PV >0, EV acreditado | No calculable. Denominador cero se marca no definido, no 0/1 inventado. |
| CPI = EV / AC | AC >0, EV acreditado | No calculable. |
| EAC₁ = BAC / CPI | BAC aprobado y CPI >0 | No calculable; escenario de continuidad del desempeño de costo. |
| EAC₂ = BAC / (CPI × SPI) | BAC aprobado, CPI×SPI >0 | No calculable; justificar hipótesis de desempeño combinado de costo/plazo para toda la proyección. |
| EAC₃ = AC + [(BAC − EV)/(CPI × SPI)] | BAC/EV/AC sustentados e índices positivos | No calculable; aplica desempeño combinado al trabajo restante y conserva AC incurrido. |
| PV/BAC, EV/BAC, AC/BAC | BAC >0 y magnitudes sustentadas | No calculables; no confundir porcentaje gastado con avance físico. |

La consigna exige periodo actual, acumulado actual y acumulado anterior para PV/EV/AC/SV/CV/SPI/CPI. Variaciones se restan y suman según periodo; índices se recalculan con sus numeradores/denominadores, **no se suman ni promedian por periodos**. Justificar EAC seleccionado con causas reales; no elegir el menor. CSI para burbujas requiere definición explícita y validación con la pauta, habitualmente combinando CPI/SPI; no se cuenta con serie para dibujarlo aún.

## 5. Evidencia técnica y demostrabilidad por módulo

| Módulo | Disponible por código/artefacto | Falta antes de presentarlo como completo |
|---|---|---|
| Login/roles | UI, JWT, bcrypt, bloqueo, RBAC y pruebas escritas | V-02/03 contra backend real, sesión WS, autorización vigente y aislamiento entre objetos. |
| Flota | UI/API alta, edición, estado e historial | Tipo/campos completos, permisos y persistencia en entorno candidato; B-04. |
| Pedidos | CSV/XLSX, ventanas, pin/hitos y jornada | Prioridad/producto/volumen integral, validación geográfica y errores; B-05/23. |
| Optimización | GA real, normal validate_for_publication, persistencia | Mejor factible y matriz confiable; todas las vías validadas, 150×15 factible/SLA HTTP; B-07/08/21. |
| Mapa/tabla | GeoJSON, filtro/detalle, OSRM opcional y fallback | Versión/ETA/geometría consistentes, factibilidad real y OSRM integrado; B-13/16. |
| Dashboard | Indicadores desde persistencia | Deduplicación, energía por combustible, costos/ahorro y puntualidad real, actualización; B-12/13/14/15. |
| PDF | Endpoint de descarga y generación real en memoria | Fecha real, factor/versión y rango seleccionado conciliados; B-17. |
| Conductor/offline | Ruta, GPS, incidente, entrega y cola IndexedDB | Fecha/comprobante persistidos, concurrencia/idempotencia y recuperación demostradas; B-09/14/19. |
| Seguimiento | REST público minimizado, WS por token/pedido | WS filtra datos internos y limpieza/revalidación; B-10/11. |
| Reoptimización | Recálculo de un vehículo con mensajes WS | Publicación válida, multivehículo por avería, reloj/carga, durabilidad; B-08/13/24/25. |
| Tráfico, clientes, conductores completos, compensación | Tráfico manual, nombre de cliente, asignación parcial, equivalencia de árboles | No son integración de tráfico, CRUD clientes, módulo completo de conductores ni compensación ejecutada. Declarar alcance pendiente. |

Son **candidatos a demostrar tras ensayo**, no módulos acreditados en ejecución por esta fase. La conexión está implementada en `src/api.ts` → `/api/v1`, proxy Nginx y rutas FastAPI, con WS separado; no se confirmó un proceso vivo ni persistencia real. El paquete actual no incluye grabación MP4 ni presentación final localizada.

## 6. Prioridad para obtener evidencia faltante

1. Resolver G-01/G-02: original de consigna, baseline económica/temporal, fuente real de Jira y aceptación. Conservar evidencia disponible y sus límites.
2. Ejecutar correcciones P0/P1 en fase autorizada y pruebas V-02…19 en entorno aislado con datos restaurables; registrar defectos y resultados por candidato.
3. Recopilar series ágiles y costos desde el inicio del sprint, no después; verificar discrepancias de capturas sin alterarlas.
4. Preparar reportes/visuales solo con datos suficientes; encuesta/reunión reales para cierre y lecciones; completar enlaces y versiones en fase posterior.
5. Ensayar sustentación y MP4 con integración real; guardar archivo reproducible en ruta exigida cuando esté autorizado y aceptado el candidato.

## 7. Integridad de esta entrega

Se generaron exclusivamente los cuatro `.md` solicitados dentro de `AUDITORIA`. La comparación final SHA-256 confirmó **193/193 archivos rastreados fuera de AUDITORIA sin cambios** respecto del inventario anterior a las comprobaciones. El inventario ampliado previo a redactar pasó de **403 a 407 archivos**, con **cero modificaciones de preexistentes, cero bajas y exactamente cuatro altas**, correspondientes a los documentos solicitados. Los cinco informes previos conservaron su hash. Los árboles `.git`, `node_modules` y `.venv` no están incluidos en el inventario ampliado; no se ejecutaron operaciones de modificación sobre ellos.

El estado Git final muestra únicamente los cuatro archivos nuevos sin rastrear; `git diff --name-only` no muestra cambios a archivos rastreados. Los enlaces relativos de los cuatro documentos resuelven y la comprobación UTF-8 no encontró caracteres de sustitución. No se atribuyen a esta fase resultados históricos, cambios de artefactos locales anteriores ni costos/horas no registrados. La edición de este párrafo solo actualiza uno de los cuatro documentos nuevos.
