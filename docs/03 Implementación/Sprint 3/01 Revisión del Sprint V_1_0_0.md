# Revisión del sprint

<!-- complemento-r4:inicio -->
> **Complementación documental r4 — 17/11/2026.** El apartado siguiente aporta propuestas y datos simulados para completar vacíos. No declara nuevas pruebas, gastos ni aprobaciones reales. [Escenario común](../../COMPLEMENTO_CONTEXTUAL_DEL_PROYECTO.md).

## Complementación r4: base de comparación y aceptación propuesta

Para US-014 se añade una base **simulada** homogénea: 150 pedidos, misma flota y ventanas, secuencia base de 300 km/jornada y propuesta de 249 km (17 % menos). Con consumo equivalente de 10 km/L y factor diésel supuesto del proyecto, el cálculo pasa de 80,92 a 67,16 kg CO₂/jornada. No es resultado del solver ni ahorro de campo observado.

La revisión propuesta debe comprobar también que un pedido nuevo aparezca con ruta publicada, que la edición del pin se conserve, que mapa y tabla representen las mismas paradas y que el PDF use el mismo conjunto de datos. QA registra versión, dataset y resultado por criterio; Frontend corrige interacción y Backend revisa los agregados.

Fecha objetivo de revalidación: 23–25/11/2026. Presentación y decisión: propuesta para el 27/11/2026. Los 86 casos frontend reportados en r3 conservan su alcance; r4 no añade una ejecución ni convierte esos casos en aceptación integral.
<!-- complemento-r4:fin -->

---


**Versión documental:** V_1_0_0; aclaración de evidencia r3, 17/11/2026.

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Nikole Celeste Bastidas Vilca (Project Manager)

## Historias de usuario implementadas y validación pendiente

### Evidencia del sprint

El registro anterior declara una validación aislada con datos descartables. Sus conteos se conservan como históricos, sin atribuirlos a una ejecución nueva ni a una Sprint Review observada:

- **143 pruebas backend aprobadas**.
- **68 pruebas frontend aprobadas**.
- **Build de producción completado correctamente**.
- Auditorías de dependencias, evaluación puntual de accesibilidad y escaneo de calidad reportados en aquel corte; no reejecutados en la actualización r3.

La actualización r3 ejecutó 86 pruebas frontend, con 81,35 % de cobertura de líneas y 73,93 % de ramas. TypeScript y build pasaron. [Resultados reproducibles](../../evidencias/2026-11-17/frontend.json). Estas pruebas acreditan comportamientos dentro de sus entornos; no acreditan aceptación integral, cobertura de todas las condiciones de la DoD ni conformidad de accesibilidad/seguridad.

### Consolidación de la revisión

Las capacidades siguientes tienen implementación y comprobaciones técnicas. La aceptación requiere verificar también las condiciones que no cubren las pruebas de componentes. Por ello se corrige la calificación global «Cumplida» de la versión anterior:

| ID | Requisito del sprint | Estado | Evidencia disponible |
|---|---|---|---|
| **US-010** | Visualización de rutas en mapa interactivo | Implementada; aceptación pendiente | Casos de mapa, rutas y pedidos nuevos aprobados con mocks; falta recorrido en navegador con cartografía real. |
| **US-011** | Detalle de parada por selección | Implementada; aceptación pendiente | Selección y datos cubiertos parcialmente; falta observación integral con datos operativos y API real. |
| **US-012** | Vista resiliente alternativa tabular | Implementada; aceptación pendiente | Recuperación y tabla verificadas en pruebas de UI; falta comprobar teclado y fallo real del proveedor en navegador. |
| **US-013** | KPIs operativos y ambientales | Implementada; validación operativa pendiente | Cálculos y casos sin datos presentes; no se midieron consumo ni emisiones reales de transporte. |
| **US-014** | Comparación contra línea base | Implementada; base operativa pendiente | Existe manejo de referencia ausente; hace falta base comparable para declarar ahorro real. |
| **US-015** | Árboles equivalentes por factor configurable | Implementada; validación metodológica pendiente | Equivalencia modelada; no representa árboles plantados ni compensación ambiental verificada. |
| **EN-004** | Persistencia offline y sincronización PWA | Implementada parcialmente; E2E pendiente | Persistencia/cola con pruebas, sin ensayo completo observado de desconexión, reconexión y no duplicidad en navegador. |

El incremento ofrece funciones demostrables y regresiones automatizadas, con pendientes de aceptación explícitos. No se declara un sprint aceptado ni una reunión celebrada. [Estado técnico vigente y límites](../../ESTADO_TECNICO_VIGENTE.md).

[← Volver al README principal](../../../README.md)
