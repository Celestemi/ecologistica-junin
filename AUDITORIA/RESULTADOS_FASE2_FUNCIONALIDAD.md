# Fase 2 — Integridad y funcionalidad

17/11/2026 America/Lima; main/b47d5eb7cda26444c56460ea74591cc5f973e0b3 + árbol sin commit. PostGIS tmpfs NUEVO verificado por runner; ninguna BD existente modificada ni migrada. Sin dependencias nuevas.

## Cambios y estado de aceptación

| ID | Cambio comprobado | Estado y límite |
|---|---|---|
| AF-07 | Último snapshot computed/published por jornada, archivo de previos sin borrado; indicadores dejan de sumar tres versiones; ruta/seguimiento no resucitan asignación antigua; cancelación total escribe snapshot vacío; copia de geometría/ETA/estado y factores del resto de la flota | PARCIAL: núcleo de deduplicación/vigencia probado. Falta referencia FIFO independiente por vehículo al mezclar recálculos; se marca referencia_comparable=false y se suprimen porcentajes/equivalencias en dashboard/PDF, sin fabricar una referencia. |
| AF-08 | Evento JSON v1 en Bitacora existente: pedido, operación, hora cliente con zona, recepción servidor, vehículo, plan y actor por FK; idempotencia bajo lock PostgreSQL, conflicto por operación ajena; notificación después de commit; PDF consume fecha efectiva y versión del evento | PARCIAL: núcleo durable de fecha/actor probado con reintento y periodo distinto al plan. Fotos/firmas bloqueadas por política de privacidad/retención/persistencia no aportada; no se reconstruyen eventos históricos desde ETA. |
| AF-09 | energy_accounting.py comparte cálculo combustible/electricidad/TCO; eléctricos nunca galones; factores de vehículo congelados en metadatos al publicar; costo explícitamente estimado con supuestos ya existentes del PDF | PARCIAL: oráculo eléctrico 1500 g→10 kWh→S/8,50 pasa. No son tarifas actuales, consumos medidos, AC ni ahorro económico aprobado. Modelos de emisiones/factores históricos y referencia por vehículo requieren validación adicional. |
| AF-10 | Testigo sintético independiente 15 grupos×10: 80 kg/1 m3 por vehículo, ventanas de 8 h, cota conservadora de 63,2 min por recorrido a 10 km/h; API ASGI completa + worker + PostGIS persiste 150 únicos factibles ≤45 s; pipeline dinámico <30 s | PARCIAL respecto a SLA de exposición: escenario favorable sintético identificado; sin OSRM/red externa ni latencia de WS real. No reemplaza benchmark representativo/múltiples semillas/proveedor. Detalle medido en propiedad benchmark del JUnit fase2-final. |
| AF-11 | Reoptimización no puede salir antes de hora del GPS; rutas se recuperan desde snapshot BD en vez de confiar en secuencia en memoria | PARCIAL: no jornada/carga acumulada completa, avería/redistribución multivehículo ni GPS/incidentología durable/multiworker. Retención de posición y backend compartido requieren diseño/política/infra; no se afirma continuidad total. |
| AF-12 | SQL versionado propuesto post_auditoria_001_geometria.sql; probado dos veces en tabla TEMP legado sintética con fila preservada y geometría LINESTRING SRID 4326 | PARCIAL/BLOQUEADO para BD reales: NO registrado en autoarranque ni aplicado a BD existente; falta esquema/backup histórico autorizado. Prueba ya es ejecución SQL real, no solo splitter. |
| AF-13 | Revisión de contratos confirma CSV y XLSX ya implementados en order_import.py, desk.py, API y UI, probados por suite de importación | PARCIAL/DECISIÓN: corregir falsa ausencia heredada de CSV. Tipo de vehículo/prioridad/tipo de producto con dominio/aplicación/persistencia completa requieren contrato validado y plan de esquema; no se inventan enums ni se añade ORM incompatible con BD previa. |
| AF-14 | PDF y UI distinguen equivalencia de plantación ejecutada | BLOQUEADO/PARCIAL: faltan reglas aprobadas de licencias/turnos, preferencias y proyecto/costo/responsable de compensación. No se presume exención. |
| AF-15 | PDF usa fecha del evento, descarta ETA como entrega, separa totales estimados de snapshots vigentes de listado de eventos reales; nuevo CSV autorizado, periodo y versión de plan, protección de fórmula de hoja de cálculo; botones PDF/CSV por periodo en dashboard | PARCIAL: descargas y periodos probados; falta aceptación metodológica/factores reales y conciliación ambiental completa por vehículo. El CSV se refiere a actividad con evento; header vacío no inventa entregas. |
| AF-24 | Prueba respeta consulta inicial de 20+1; añade regresión cursor 81, continuación y no duplicación; mantiene mantenimiento y edición | RESUELTO CON EVIDENCIA: 70 frontend pasan. |
| AF-23 | Runner exige etiqueta/tmpfs/ausencia de volúmenes; fixture BD exige ECOLOGISTICA_TEST_DISPOSABLE=1; no se prueba sobre datos existentes | ABIERTO/NO VERIFICABLE: falta ensayo representativo de 1000/día, 50 vehículos y ventana SLI 99,5 %. Se preparará protocolo fase 3; benchmark corto no es uptime. |
| AF-25 | Se preservan accesibilidad por etiquetas/teclado y se corrige aviso de mapa público sin GPS | PARCIAL/NO VERIFICABLE: falta evaluación visual/zoom/lector y usuarios reales. No se inventa conformidad WCAG. |

## Pruebas

- fase2-rojo: cuatro fallos que reproducen suma de snapshots, galones eléctricos, ETA usada como fecha y periodo real omitido.
- fase2-focal: cuatro casos corregidos PASARON; después se agregaron reloj real y snapshot vacío (fase2-empty: seis PASARON).
- fase2-sla-upgrade: dos PASARON: API ASGI 150×15 y upgrade TEMP sintético. El JUnit conserva parámetros/tiempo/hardware; no se presenta prueba ASGI como navegador o proveedor real.
- **fase2-final: 204 backend PASARON, 0 fallos/omisiones, 40,25 s.** Incluye 28+14 B-08 y 11 regresiones de seguridad fase 1.
- **fase2-frontend-final: 70 PASARON/0 fallos**, 15 archivos; TypeScript --noEmit --incremental false PASÓ.
- Advertencias: deprecación Starlette/httpx y compatibilidad record_property/xunit2; propiedad sí disponible, runner ajustará formato de JUnit. Advertencia jsdom de navegación no interrumpe casos ni equivale a navegador real.
- Fallos intermedios preservados: nuevas propiedades requerían ampliar dos dobles de B-08; expectativa de galones del test API era incorrecta para ruta totalmente eléctrica y se sustituyó por comprobación de energía con unidades y no negativos, sin perder aceptación de consumo.

## Archivos

Nuevos: app/services/delivery_events.py, energy_accounting.py; app/db/post_auditoria_001_geometria.sql (propuesta no automática); tests/test_post_audit_integrity.py, test_post_audit_sla_and_upgrade.py. Modificados: active_plan.py, order_lifecycle.py (fase 1), operational_indicators.py, pdf_generator.py, genetic_solver.py, realtime_router.py; routes.py, websockets.py, schemas/logistics.py; tests/conftest.py, test_publication_b08.py, test_api.py; src/types.ts, api.ts, components/Dashboard.tsx, pages/fleet.test.tsx; runner scripts/run-post-audit-tests.ps1. Fuente de verdad de lista completa final: git diff y manifiesto de fase 5.

## Salida

No regresiones conocidas de seguridad/integridad introducidas; suites verdes y alcance de cada prueba explícito. Se pasa a fase 3 para pruebas reproducibles/cobertura/CI/arranque/flujo real aislado. Las decisiones de alcance, evidencia de comprobantes, esquemas históricos y disponibilidad solo bloquean esas operaciones, no autorizan cambios tácitos ni afectan fuentes históricas.
