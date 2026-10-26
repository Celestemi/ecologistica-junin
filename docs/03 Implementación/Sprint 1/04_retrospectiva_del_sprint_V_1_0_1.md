# Retrospectiva del Sprint 1

**Nombre del Proyecto:** EcoLogística Huancayo — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Versión:** V_1_0_1 (SemVerDoc — corrección de coherencia post-verificación DoD, 2026-10-26)

> La versión **V_1_0_0** permanece como registro histórico genérico de madurez organizacional. Esta versión incorpora aprendizajes **observables** en el repositorio y en `REPORTE_VERIFICACION_DOD_SPRINT_1.md`.

---

## 1. ¿Qué aprendimos?

- La **Definition of Done global** (cobertura ≥ 80 %, análisis estático, peer review, staging) es independiente de tener el código funcional escrito; omitir su verificación produce **actas de sprint desalineadas** con el estado real del producto.
- Centralizar pruebas de integración en **PostGIS** (`ecologistica_test`) exige entorno reproducible (Docker o CI); sin ello, decenas de tests fallan en setup aunque la lógica de negocio esté implementada.
- La trazabilidad **RF / RNF / US / EN** se fortalece cuando cada historia enlaza archivos de código, suites en `tests/` y criterios BDD del documento ágil — pero la trazabilidad documental debe **actualizarse** tras cambios (p. ej. JWT 12 h vs 15 min en acta anterior).
- **RN-002** debe permanecer condicionada: la parametrización técnica (US-002) no sustituye la validación normativa (IMP-005).
- El registro histórico de **IMP-004** (OR-Tools) no coincide con el solver genético actual; conviene revalidar RNF-001 sobre la implementación vigente.

---

## 2. ¿Qué estamos haciendo bien?

- Estructura monorepo clara (`app/`, `src/`, `tests/`, `docs/`) y documentación de planificación en `docs/02 Planificacion/`.
- Historias del Sprint 1 con **servicios dedicados** y pruebas por historia (`test_*_us00*.py`, `test_security_en003.py`).
- Refuerzo de seguridad en pruebas: guardia de BD en `tests/conftest.py`.
- Preparación de **calidad continua**: pytest-cov, Vitest, `sonar-project.properties`, workflow CI.
- Separación documentación / código y versionamiento de entregables de implementación (V_1_0_0 → V_1_0_1).

---

## 3. ¿Qué podemos hacer mejor?

### 3.1 Personas

- Alinear **quién ejecuta** la verificación DoD (QA/DevOps) antes de firmar revisiones de sprint al 100 %.
- Evitar asumir roles de stakeholder en documentos sin minuta o evidencia.

### 3.2 Relaciones

- Comunicar explícitamente cuando la **documentación académica** (demo, staging) diverge del repo verificable, para corregir en la siguiente versión documental sin borrar el historial.

### 3.3 Procesos

- Definir como **gate de cierre de sprint**: suite verde + métricas de cobertura archivadas + enlace a PR revisado.
- Ejecutar CI en cada integración significativa; no depender solo de pruebas locales sin PostGIS.
- Mantener coherencia entre acta de revisión y `PLAN_IMPLEMENTACION_SPRINT_1.md` / reportes de verificación.

### 3.4 Herramientas

- Documentar en README el arranque mínimo: `docker compose up -d db` antes de `pytest`.
- Ampliar tests frontend en CI (`npm run test:coverage`) para cumplir DoD punto 1 en capa React.

---

## 4. Propuestas de mejora para el siguiente Sprint

*Las siguientes filas son **propuestas** para discusión en la retrospectiva de equipo; **no** constituyen compromisos aprobados ni acta firmada.*

| # | Propuesta | Responsable sugerido | Fecha objetivo sugerida | Resultado verificable |
|---|-----------|----------------------|-------------------------|------------------------|
| P-01 | Ejecutar pipeline CI con PostGIS y archivar log verde | DevOps / Backend | 15/11/2026 | Artefacto GitHub Actions + enlace en informe de estado |
| P-02 | Subir cobertura backend ≥ 80 % (capa httpx en desk/auth) | Backend / QA | 15/11/2026 | `coverage.xml` + umbral en CI |
| P-03 | Ejecutar SonarQube o CodeQL y registrar Quality Gate | QA | 22/11/2026 | Informe Sonar sin críticas/altas |
| P-04 | Abrir PR del cierre Sprint 1 con peer review | Tech Lead | 10/11/2026 | Aprobación registrada en GitHub |
| P-05 | Desplegar staging con TLS y validar EN-003 en runtime | DevOps | 30/11/2026 | URL staging + checklist RNF-003 |
| P-06 | Alinear configuración JWT con especificación acordada (15 min vs 12 h) | Backend + PM | 20/11/2026 | Commit + test de expiración |
| P-07 | Actualizar documentación de sprint solo tras verificación DoD | PM / Scrum Master | Cada cierre | Versión documental V_1_0_x con enlace a reporte |

---

## 5. Nota sobre compromisos (V_1_0_0)

La sección *Compromisos del equipo* de la retrospectiva **V_1_0_0** listaba diez acciones genéricas de organización. Se mantiene como referencia de intención formativa del curso. Para el cierre académico del Sprint 1, las acciones **prioritarias verificables** son las de la tabla §4 (propuestas).

---

## 6. Enlaces

- [Informe de estado V_1_0_1](01_informe_de_estado_del_proyecto_v_1_0_1.md)
- [Revisión del Sprint V_1_0_1](03_revision_del_sprint_v_1_0_1.md)
- [Registro de impedimentos V_1_0_1](02_registro_de_impedimentos_v_1_0_1.md)
- [Reporte verificación DoD](../../../Auditorias-EcoLogistica/03_Reportes_Verificacion/REPORTE_VERIFICACION_DOD_SPRINT_1.md)

---

[← Volver al README](../../../README.md)
