# Checklist de entrega final — fase 5

17/11/2026, America/Lima; V_1_0_0. Responsable de cada cierre: **por confirmar** por el equipo, según rol sugerido; no se asignan compromisos ni fechas ficticios. Fuentes: HTML final y [matriz de consigna](MATRIZ_CONSIGNA_FINAL.md), [validación documental](VALIDACION_DOCUMENTOS_CIERRE.md), resultados/aceptación de fase 3.

Estados: verificado en el alcance indicado / parcial / pendiente / bloqueado. Tener un archivo no significa aprobar su contenido ni la rúbrica.

| Requisito | Ruta / evidencia | Responsable sugerido, por confirmar | Estado actual | Pendiente para entrega |
|---|---|---|---|---|
| Reporte 01 Estado |docs/04 Cierre/01 Reporte de Estado V_1_0_0.md |PM |Borrador con datos actuales |Costos/fechas reales comparables y aceptación. |
| Reporte 02 Variación |docs/04 Cierre/02 Reporte de Variación V_1_0_0.md |PM/QA |Borrador; cobertura calculada |Variación real plazo/costo, fuentes/aprobación. |
| Reporte 03 EVM |docs/04 Cierre/03 Reporte de Análisis de Valor Ganado - EVM V_1_0_0.md |PM/costos/autoridad |Bloqueado para cálculos reales |BAC aprobado, PV temporal, EV aceptado valorado y AC sustentado; cortes/moneda/reservas y tres EAC. |
| Reporte 04 Tableros |docs/04 Cierre/04 Tableros de Control - Híbridos V_1_0_0.md |PM/QA |Parcial, RAG y barra de datos actuales |Series EVM/CFD/SPI-CPI-CSI auténticas e interpretación. |
| Reporte 05 Radiadores |docs/04 Cierre/05 Radiadores de Información V_1_0_0.md |Scrum Master/equipo |Parcial/histórico |Burndown/burnup, Kanban vigente, Mood y retro reales; exportación/fechas conciliadas. |
| Reporte 06 Final |docs/04 Cierre/06 Reporte Final del Proyecto V_1_0_0.md |PM/aceptante |Cierre pendiente de aprobación |Satisfacción, costo final, fecha/acta y transferencia real; requisitos/exenciones aprobados. |
| Reporte 07 Lecciones |docs/04 Cierre/07 Reporte Final de Lecciones Aprendidas V_1_0_0.md |Equipo/PM |Borrador analítico |Reunión real, validación de aprendizajes y acciones asumidas. |
| Nombres/rutas/retorno |Siete archivos exactos sin subcarpetas; `../../README.md` |Mantenedor documental |Verificación estructural de fase 4 y control final |Conservar controles al actualizar versiones. |
| README→siete documentos |README.md, sección agregada; readme_update.json |Mantenedor |Agregado mínimo, prefijo original preservado |Enlaces bidireccionales finales revisados; no confundir índice con cierre aprobado. |
| Versionado/coherencia histórica |Auditoría de versiones/capturas; docs previos intactos |PM/mantenedor |Parcial |Resolver fecha 2024/2026, conteos contradictorios y versiones internas/archivo en ciclo autorizado. |
| Separación frontend/backend |src/app y frontend/backend de despliegue |Arquitectura |Verificada por inspección |Consolidar arquitectura efectiva/manuales; no requiere reorganización masiva. |
| .gitignore / dependencias |.gitignore y archivos rastreados |Mantenedor/seguridad |Reglas existentes revisadas |No empaquetar node_modules/.venv/dist/caches; claves/backups e historia requieren revisión específica. |
| Credenciales/datos |Solo datos sintéticos en contenedor nuevo; logs sin datos productivos |Seguridad/DevOps |Aislamiento comprobado para esta corrida |No afirmar ausencia exhaustiva de secretos históricos ni producción segura por configurar demo. |
| Backend y B-08 |backend_junit.xml:185/185; B-08 BD14/14 incluidos |QA/aceptante |Verificado para casos actuales |Revisión/aceptación formal B-08 y criterios completos RF. |
| Frontend |frontend_results.json:68/69 |Frontend/QA |Fallido 1 caso |Resolver DEF-01 fuera de estas fases y revalidar; no borrar la corrida fallida. |
| Cobertura/DoD |Backend 83,27% líneas/78,68% mixta; frontend 78,80% líneas |QA/equipo |Parcial |Acordar métrica y cumplir umbral, análisis/PR/staging reales. |
| Seguridad/integridad |DEF-02/03/04 y B-09/10/11 |Backend/seguridad |Bloqueante de aceptación |Autorización vigente, terminalidad, privacidad/ciclo WS y pruebas negativas completas. |
| Flujo continuo real |Guía 20 min§3; integración API y componentes por separado |QA/operador demo |No observado en navegador |Ensayo Pedido→Validación→GA→BD→Mapa→Conductor→Entrega→KPI→PDF. |
| SLA válido |benchmark_solver_actual.json; tests SLA débiles |Backend/QA |No acreditado |150 ×15 factible≤45 sHTTP y dinámica<30 s con dataset/testigo/hardware/OSRM/BD registrados. |
| Indicadores/PDF |DEF-06/07/08/09; tests parciales aprobados |Backend/QA |Parcial |Versiones/fecha real/energía/factores/rangos conciliados; no declarar ahorros mensuales. |
| Accesibilidad/usabilidad |Informe WCAG histórico y componentes actuales |UX/QA |No acreditado integral |Evaluación actual WCAG 2.1 A/AA/lector/reflow y perfiles objetivo reales. |
| Capacidad/disponibilidad |Sin SLI/ventana/carga representativa |DevOps/QA |Pendiente |1000 pedidos/50 vehículos y99,5% en ventana definida, restore/alertas con evidencia. |
| Sustentación gestión 10 min |GUIA_SUSTENTACION_20_MINUTOS.md§2 |Expositores |Guion preparado |Ensayo cronometrado y datos/aceptación reales; no cifras EVM simuladas. |
| Demo técnica 10 min |GUIA_SUSTENTACION_20_MINUTOS.md§3 |Operador de demo |Guion condicionado; ejecución pendiente |Resolver bloqueantes y ensayar entorno/datos/roles/conexión real. |
| Pitch 1 min+demo 4 min |GUION_VIDEO_5_MINUTOS.md |Equipo audiovisual |Storyboard/narración preparados |Grabar sistema real ensayado y voz autorizada, sin ocultar límites. |
| MP4 real |Destino docs/05 Video proyecto/ |Equipo audiovisual |**Pendiente; no archivo creado/verificado** |Grabación continua, duración≈5 min, reproducción total, audio/imagen legibles y ambos segmentos. |
| Aprobación/cierre/transferencia |No acta/constancia disponible |Aceptante/PM |Bloqueado |Intervención real de responsables; no suplir firmas/satisfacción con texto generado. |

## Preparación frente a la rúbrica — estimación documental, no nota oficial

| Grupo / peso | Nivel estimado al corte | Fundamento y siguiente condición |
|---|---|---|
| R1 Reportes 01–03 /1 |Insatisfactorio respecto del cálculo EVM real |Estructuras presentes pero PV/EV/AC/SPI/CPI/EAC no calculables; falta evidencia económica. |
| R2 Visuales/cierre 04–07 /1 |En desarrollo |Hay RAG/barra real, tabla/imagen histórica y análisis; faltan gráficos/radiadores actuales y aceptación/satisfacción. |
| R3 Trazabilidad/versionamiento /1 |En desarrollo, con enlaces nuevos verificados |Siete nombres/rutas/retornos e índice completos; conflictos/documentación previa no conciliados ni versionados por restricciones de esta ejecución. |
| R4 Demo funcional/arquitectura /4 |No acreditado en vivo |Separación/casos API reales demostrados por tests, sin recorrido cronometrado en navegador ni aceptación integral. No se asigna puntuación de una demo no observada. |
| R5 MP4 /4 |Insatisfactorio por evidencia audiovisual ausente |No hay MP4 real; guion no lo sustituye. |

Máximo ponderado 33 puntos; demo/video concentran 24. No se calcula calificación oficial ni se oculta la falta de evidencia. Prepararlos tiene alta prioridad, pero exige un candidato seguro y realmente ensayado.

## Intervención humana pendiente

Confirmar responsables y aceptación del incremento; autorizar nuevo ciclo de correcciones, conseguir registros económicos/cronograma/aceptación monetizada, exportaciones/capturas auténticas y respuesta del equipo; realizar encuesta/reunión/transferencia; ensayar interfaz con API real y grabar voz/video. Estas acciones no se sustituyeron por suposiciones ni se ejecutaron fuera del alcance.
