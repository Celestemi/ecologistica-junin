# Reporte de saneamiento documental pre-Sprint 3

**Fecha:** 26 de octubre de 2026  
**Alcance:** organización y corrección documental. No se modificaron backend, frontend activo, modelos, servicios, migraciones, Docker, CI, dependencias ni bases de datos.

## Estructura final

```text
Auditorias-EcoLogistica/
├── 01_Auditorias/
├── 02_Planes_Implementacion/
├── 03_Reportes_Verificacion/
├── 04_Informes_CI/
└── 05_Preparacion_Sprint_3/
```

`docs/` conserva los documentos oficiales de inicio, planificación y Sprints. `README.md` continúa como punto de entrada. La aplicación activa se documenta como `app/` (backend) y `src/` (frontend).

## Inventario de movimientos

| Origen previo | Destino final |
|---|---|
| `Auditorias-EcoLogistica/AUDITORIA_01_ESTADO_REPOSITORIO.md` a `AUDITORIA_MAESTRA_PRE_SPRINT_3.md` | `01_Auditorias/` |
| `PLAN_IMPLEMENTACION_SPRINT_1.md`, `PLAN_IMPLEMENTACION_SPRINT_2.md` | `02_Planes_Implementacion/` |
| `REPORTE_RENDIMIENTO_EN_001.md`, `REPORTE_VERIFICACION_DOD_SPRINT_1.md`, `VERIFICACION_FINAL_SPRINT_2.md` | `03_Reportes_Verificacion/` |
| `REPORTE_AUDITORIA_CI.md` | `04_Informes_CI/` |

El contenido de informes y planes no se alteró: solo cambió su ubicación. El prototipo `EcologisticaJunin/` ya había sido retirado mediante instrucción previa explícita; no se restauró ni se modificó código activo durante este saneamiento.

## Documentos actualizados

| Documento | Actualización |
|---|---|
| `README.md` | Enlaces a informes/planes centralizados; enlaces Sprint 1 corregidos; descripción del stack activa; inventario de auditorías. |
| `docs/ESTADO_TECNICO_VIGENTE.md` | Nueva fuente de consulta para separar arquitectura prevista, implementada, pendiente y evidencia S1/S2; incluye matriz de trazabilidad. |
| `docs/01 Inicio/10. Stack tecnológico V_1_0_3.md` | Nota de vigencia que distingue selección histórica y runtime. |
| `docs/01 Inicio/11. Base de datos V_1_0_3.md` | Nota de divergencia `GEOGRAPHY` prevista frente a `geometry` implementado. |
| `docs/01 Inicio/12. Modelo C4 V_1_0_6.md` | Encabezado alineado con nombre y nota de arquitectura vigente. |
| Documentos S1/S2 de `docs/03 Implementación/` | Referencias corregidas a planes/reportes centralizados, README y documentos de Sprint hermano. |

## Enlaces y validación

- Se corrigieron rutas de README a los documentos S1 dentro de `docs/03 Implementación/Sprint 1/`.
- Se reemplazaron enlaces a informes/planes que estaban en raíz por sus nuevas rutas bajo `Auditorias-EcoLogistica/`.
- Se corrigieron enlaces desde Sprint 1 al README (tres niveles) y desde Sprint 2 al directorio hermano `Sprint 1/`.
- Un comprobador de enlaces local reportó falsos positivos para enlaces con nombres acentuados al leer Markdown mediante la codificación de consola de Windows. Las rutas citadas existen con sus nombres Unicode reales; no se detectaron referencias residuales de ejecución al prototipo eliminado.

## Inconsistencias resueltas y pendientes

Resueltas documentalmente: README ya identifica el código activo, el motor como GA propio, OSRM como opcional, Redis/Celery como no implementados y PWA offline como no verificada. Las fuentes de evidencia ahora están centralizadas y vinculadas.

Permanecen registradas, no ocultadas: decisión formal `geometry`/`GEOGRAPHY`; ausencia de OSRM/Redis/Celery/PWA offline en runtime; TLS productivo no acreditado; E2E con PostGIS, cobertura DoD, Sonar/CodeQL, CI/staging y factibilidad HTTP/150×15 pendientes.

## Estado de Sprints

| Sprint | Estado documental sustentado |
|---|---|
| Sprint 1 | Implementación estática y pruebas dedicadas; DoD global no acreditada. |
| Sprint 2 | Implementación parcial de US-005/007/008/009 y EN-001; tiempo del solver acreditado, no E2E/factibilidad completa/HTTP. |
| Sprint 3 | Puede iniciar trabajo funcional condicionado; no está listo para declarar evaluación o cierre formal sin atender las brechas heredadas. |

## Resultado

La documentación queda centralizada y con una fuente explícita de estado técnico vigente. No se declara que S1 o S2 estén formalmente cerrados, ni que el sistema esté validado integralmente. Antes de evaluar Sprint 3 deben ejecutarse los controles señalados en `docs/ESTADO_TECNICO_VIGENTE.md` y en las auditorías de `01_Auditorias/`.

## Estado Git

El estado de Git y `git diff --stat` se consultaron al finalizar la validación. Muestran las eliminaciones previamente autorizadas del prototipo, la reubicación documental (Git la refleja como archivos de origen eliminados y nuevos destinos no rastreados hasta que se agreguen), y las actualizaciones Markdown de este saneamiento. No se realizaron commits ni push.
