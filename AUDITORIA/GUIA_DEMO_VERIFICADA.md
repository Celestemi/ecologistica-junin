# Guía de demostración: qué se verificó y qué falta

17/11/2026, America/Lima; b47d5eb + cambios sin commit. **No se observó ni aprobó una demostración de diez minutos en navegador.** El nombre del archivo identifica la guía exigida por el plan, no certifica la sustentación.

## Verificación realizada

Backend/BD real en127.0.0.1:18000; frontend Vite15173 con proxy real; PostGIS NUEVO tmpfs25436. Scripts/post-audit-e2e.py completó10 pasos HTTP/TCP WebSocket con datos sintéticos: login por proxy→pedido→optimización→persistencia→GeoJSON→conductor→entrega/reintento→indicadores→PDF/CSV→rechazo por rol/logout. Última ejecución tras parche1.45.2:1,3382 s; no es tiempo de exposición.

**Bloqueo de UI:** inventario Computer Use, dos intentos: “The browser access host is unavailable”; pipe nativo no encontrado (os error2). No hay screenshot ni ensayo visual actual; no se automatizó por otro mecanismo. WCAG/zoom/lector,mapa renderizado y experiencia de usuario permanecen NO VERIFICABLES.

## Precondiciones para ensayo humano

- Revisión de [runbook](RUNBOOK_TECNICO_POST_CORRECCIONES.md), fuente/commit y manifiesto; usar datos sintéticos explícitos.
- Resolver o aceptar formalmente pendientes por RF; no mostrar módulos incompletos como terminados.
- Verificar navegador,red,tiles yOSRM si se pretende enseñar geometría vial; nuestro corte usa matriz geodésica y no acredita calles reales.
- Confirmar acceso/roles sin mostrar JWT/secretos; no aceptar geolocalización/cámara por automatismo.
- Dejar constancia de baseline/costo/EVM ausentes; no usar costo logístico como AC ni tests como EV.
- Ruta inicial sin entregas activas previas; si las hay, inserción/reoptimización, no sustitución silenciosa.
- Los recursos de pruebas pueden retirarse al terminar esta sesión; no confundir laboratorio con despliegue persistente.

## Guion propuesto, NO cronometrado: gestión diez minutos

| Tramo propuesto | Contenido y evidencia |
|---|---|
|0–1 |Problema,objetivo y geografía adaptada según acta |
|1–3 |Plan predictivo/backlog adaptativo; distinguir baseline aprobada y documentos disponibles |
|3–5 |Resultados209 backend/70 frontend/4 SW,gates y correcciones AF-01/02/03/24 |
|5–7 |EVM: mostrar fuentes reales si se aportan; en su ausencia explicar bloqueo,sin cifras ficticias |
|7–9 |Riesgos residuales,alcance no eximido,lecciones derivadas de pruebas |
|9–10 |Aceptación/satisfacción/transferencia pendientes y decisiones del equipo/docente |

## Guion propuesto, NO cronometrado: técnica diez minutos

| Tramo propuesto | Acción y comprobación |
|---|---|
|0–1 |Login de operador;flota/rol correctos |
|1–2 |Crear o importar pedido sintético CSV/XLSX;validar ubicación/ventana |
|2–4 |Optimizar instancia pequeña factible;comprobar asignación única/estados/plan |
|4–5 |Mapa y tabla equivalentes;declarar origen de distancia/ETA y fallback |
|5–7 |Conductor asignado,ruta activa,seguimiento público minimizado y entrega real idempotente |
|7–8 |Indicadores por periodo;plan vigente contado una vez;gal/kWh separados |
|8–9 |PDF/CSV del mismo periodo;fecha de evento y versión;explicar estimaciones |
|9–10 |Mostrar rechazo controlado por rol/terminal y declarar limitaciones;no ejecutar ataques contra producción |

Estos intervalos son planificación, no mediciones. No hay aceptación por tercera persona,fluidez certificada ni nota de rúbrica. El audiovisual está **EXCLUIDO TEMPORALMENTE — NO EVALUADO**, sin pendientes asociados.
