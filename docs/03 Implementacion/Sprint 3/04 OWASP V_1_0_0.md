# Reporte de Seguridad OWASP Top 10 (2025)

**Versión documental:** V_1_0_0

**Nombre del proyecto:** EcoLogística Junín  
**Fecha de evaluación puntual:** 26 de octubre de 2026  
**Alcance:** backend FastAPI/Python, frontend React/Vite, configuración Docker y servicios locales en `localhost`  
**Herramienta de escaneo:** SonarQube Community Build 26.10.0.133078 local mediante Docker Desktop  
**Criterio de estado:** `Vulnerable` = debilidad confirmada; `Bajo revisión` = controles parciales, riesgo posible o evidencia insuficiente; `Limpio` solo se usaría con evidencia suficiente. Ninguna categoría se marca como Limpio en esta evaluación puntual.

La ficha original empleaba nombres y numeración de OWASP Top 10:2021. Esta versión conserva la sección y la tabla de la consigna, pero usa las diez categorías oficiales vigentes de [OWASP Top 10:2025](https://top10.owasp.org/2025/). Los cambios principales son: Security Misconfiguration pasa a A02; Software Supply Chain Failures amplía la antigua categoría de componentes vulnerables y pasa a A03; Cryptographic Failures pasa a A04; Injection a A05; Insecure Design a A06; Authentication Failures simplifica el nombre de A07; A09 enfatiza alertas; SSRF deja de ser A10 y se integra en A01; A10 ahora es Mishandling of Exceptional Conditions.

## 1. Matriz de Cumplimiento OWASP Top 10 2025

| Categoría OWASP 2025 | Estado en Proyecto (Limpio / Vulnerable / Bajo Revisión) | Hallazgos de SonarQube y revisión complementaria |
|---|---|---|
| A01:2025 — Broken Access Control | **Bajo revisión.** Los permisos sí se aplican en backend mediante `get_current_user` y `require_roles`. Las pruebas confirmaron 401 anónimo, 403 por rol, restricción del canal de conductor a su vehículo y minimización del seguimiento público. Falta una matriz integral por endpoint/objeto y pruebas IDOR/SSRF para todas las rutas. | SonarQube no reportó una regla específica. Evidencia dinámica: 12 pruebas de seguridad/autenticación aprobadas; solicitudes sin JWT o con JWT inválido a recursos protegidos devolvieron 401. El frontend también oculta funciones por rol, pero no es el control decisivo. |
| A02:2025 — Security Misconfiguration | **Vulnerable.** La instancia evaluada es deliberadamente de demostración: HTTP, clave y cuenta de base de datos predeterminadas, cuentas demo habilitadas, API y base de datos publicadas en el host, documentación OpenAPI pública y ausencia de cabeceras defensivas en Nginx (por ejemplo CSP, HSTS, `X-Content-Type-Options` y `Referrer-Policy`). El arranque bloquea la clave y cuentas demo fuera del entorno demo, pero no convierte esta instancia en apta para producción. | 1 vulnerabilidad menor abierta `python:S5332` en `app/core/config.py:35` por orígenes HTTP. La prueba CORS con origen no autorizado fue rechazada (400), resultado favorable pero parcial. |
| A03:2025 — Software Supply Chain Failures | **Vulnerable.** `npm audit` completo confirmó 5 paquetes afectados en herramientas de desarrollo: 2 críticos, 1 alto y 2 moderados, asociados a Vitest/Tinypool/Vite. `npm audit --omit=dev` reportó 0 vulnerabilidades en 48 dependencias de producción. Las imágenes Docker usan etiquetas móviles/no fijadas por digest y CI no ejecuta auditoría SCA. | El procesamiento de SonarQube indicó expresamente que Software Composition Analysis no estaba disponible. `pip check` no halló requisitos rotos, pero `pip-audit` no está instalado y por tanto las vulnerabilidades Python quedaron **no evaluadas**. |
| A04:2025 — Cryptographic Failures | **Bajo revisión.** JWT usa HS256, expiración y validación de firma/algoritmo; las contraseñas usan bcrypt y los tokens públicos son opacos. La instancia opera por HTTP y el JWT carece de `iss`, `aud` y mecanismo de revocación; TLS y gestión/rotación de secretos no se comprobaron en un despliegue real. | SonarQube reportó 9 vulnerabilidades mayores `python:S2245`: 7 en `optimizer_benchmark.py` y 2 en `genetic_solver.py`. La revisión confirma que el PRNG se usa para benchmark y optimización reproducible, no para secretos; son **avisos contextuales**, no una falla criptográfica explotable confirmada. |
| A05:2025 — Injection | **Bajo revisión.** Se observaron consultas SQLAlchemy parametrizadas, esquemas Pydantic y validación de tokens/entradas. No se identificó inyección confirmada, pero no se ejecutó un DAST exhaustivo ni fuzzing de todos los importadores, WebSockets y parámetros. | Sin vulnerabilidad SonarQube específica. Los avisos npm de Vite/Vitest afectan herramientas de desarrollo y se clasifican principalmente en A03; no se demostró explotación en la aplicación servida por Nginx. |
| A06:2025 — Insecure Design | **Bajo revisión.** Hay bloqueo tras intentos fallidos, RBAC, minimización de datos públicos, límites operativos y validaciones de dominio. No existe evidencia de modelado formal de amenazas, abuso, límites de tasa globales ni análisis completo de aislamiento entre objetos/usuarios. | Sin hallazgo SonarQube específico. La ausencia de findings automáticos no acredita diseño seguro. |
| A07:2025 — Authentication Failures | **Bajo revisión.** Se confirmaron rechazo de token inválido/expirado, usuario inactivo y credenciales incorrectas, además de bloqueo de cuenta. Persisten riesgos: JWT de hasta 12 horas, sin revocación/rotación, sin MFA y con token WebSocket en query string (puede aparecer en registros de infraestructura). | Sin hallazgo SonarQube específico. Las 12 pruebas seleccionadas de autenticación/RBAC pasaron; no se realizó prueba de fuerza bruta prolongada ni de gestión de sesión distribuida. |
| A08:2025 — Software or Data Integrity Failures | **Bajo revisión.** Existen `package-lock.json`, `uv.lock`, `npm ci` y CI con acciones versionadas. No se verifican firmas/procedencia de artefactos, dependencias o imágenes; las imágenes no están fijadas por digest y no hay evidencia de SBOM. | Sin hallazgo SonarQube específico. La falta de SCA de SonarQube y de verificación de procedencia mantiene la categoría abierta. |
| A09:2025 — Security Logging and Alerting Failures | **Vulnerable.** Existe bitácora de accesos y denegaciones, protegida para administrador/auditor, y se registran excepciones. No se encontró configuración de alertas, monitorización, retención, correlación ni respuesta automática; registro sin alertamiento no satisface la categoría 2025. | Sin hallazgo SonarQube específico. No se evaluó un SIEM ni un sistema externo, por estar fuera del alcance local. |
| A10:2025 — Mishandling of Exceptional Conditions | **Bajo revisión.** FastAPI traduce errores de validación e integridad y oculta detalles de excepciones inesperadas al cliente; la API registra la traza internamente. No se cubrieron fallos de todos los servicios externos, agotamiento de recursos, transacciones parciales ni comportamiento fail-open. | SonarQube no reportó una vulnerabilidad de seguridad específica. Reportó además 20 problemas de fiabilidad, entre ellos un blocker `python:S930`; son defectos de calidad pendientes, no evidencia por sí solos de explotación A10. SSRF ya no es A10 en 2025: se revisó de forma parcial bajo A01 y la URL OSRM proviene de configuración, no de entrada directa del usuario. |

## 2. Detalles de Security Hotspots y Vulnerabilidades Críticas

### Evidencia de SonarQube local

- El análisis más reciente observado para `ecologistica-huancayo` terminó correctamente el 26 de octubre de 2026. La API web exige autenticación; para no exponer credenciales, los resultados se contrastaron con las métricas e incidencias persistidas por la propia instancia local.
- **Quality Gate:** OK, pero su condición observada se limita a código nuevo; no equivale a ausencia de vulnerabilidades.
- **Vulnerabilidades abiertas:** 10; calificación de seguridad C. Son 9 mayores `python:S2245` y 1 menor `python:S5332`.
- **Security Hotspots:** 0; calificación de revisión A. Cero hotspots significa que el perfil no generó hotspots, no que todas las categorías OWASP estén limpias.
- **Otras incidencias abiertas:** 20 de fiabilidad y 4 code smells, para 30 incidencias totales. Destacan un blocker `python:S930`, tres críticas `javascript:S2871`, doce mayores `python:S1244` y cuatro mayores `javascript:S6671`. Se mantienen fuera del conteo de vulnerabilidades salvo que una revisión posterior demuestre impacto de seguridad.
- **SCA:** no disponible en esta edición/ejecución; SonarQube no evaluó dependencias.

### Hallazgos confirmados

1. **A02 — configuración local no apta para producción:** HTTP, valores demo/predeterminados, servicios publicados y falta de cabeceras defensivas. La validación de arranque reduce el riesgo fuera de demo, pero se debe verificar en el entorno desplegado.
2. **A03 — dependencias de desarrollo vulnerables:** `npm audit` completo encontró 5 paquetes afectados (2 críticos, 1 alto y 2 moderados). El árbol de producción no presentó avisos en la consulta ejecutada.
3. **A03/A08 — cadena de suministro incompleta:** imágenes Docker sin digest, sin SBOM/verificación de procedencia y sin SCA Python disponible.
4. **A09 — alertamiento no implementado/evidenciado:** existe registro local, pero no alertas ni monitorización verificables.

Los 9 avisos `S2245` no se consideran vulnerabilidades confirmadas tras revisar su contexto: la aleatoriedad controla simulación/optimización y no genera claves, contraseñas ni tokens. El `S5332` sí describe correctamente el uso local de HTTP, aunque su explotabilidad depende de que esa configuración alcance un entorno no demostrativo.

### Pruebas y comprobaciones ejecutadas

| Comprobación no destructiva | Resultado |
|---|---|
| `npm audit` | 5 paquetes afectados en desarrollo: 2 críticos, 1 alto y 2 moderados. |
| `npm audit --omit=dev` | 0 vulnerabilidades en dependencias de producción. |
| `python -m pip check` dentro del backend | Sin requisitos rotos. No detecta CVE. |
| `pip-audit` | No disponible; vulnerabilidades Python no evaluadas. |
| Pruebas `test_security_en003.py` y `test_auth.py` en el contenedor | 12 aprobadas, 1 advertencia de deprecación; incluyen JWT, RBAC backend, usuario inactivo, WebSocket y minimización. |
| HTTP local `/health` y frontend | 200. |
| Endpoint protegido anónimo/JWT inválido | 401. |
| Preflight CORS desde origen no permitido | 400 sin `Access-Control-Allow-Origin`. |
| Cabeceras del frontend local | No se observaron cabeceras defensivas adicionales; servidor Nginx expone su versión. |

Las pruebas usaron datos de demostración incluidos en el entorno local y solicitudes de solo lectura o rechazo; no se probaron sistemas externos ni se alteró información real. No se ejecutó carga, explotación, borrado, fuerza bruta ni manipulación masiva.

### Correcciones y mitigaciones

No se cambió código, configuración ni dependencias porque la consigna restringe la actualización exclusivamente a esta ficha. La única corrección aplicada es documental: matriz actualizada a OWASP 2025, clasificación diferenciada y eliminación de cualquier referencia a credenciales.

Mitigaciones pendientes, en orden recomendado:

1. Actualizar Vite/Vitest/Tinypool en una rama controlada, regenerar el lockfile y ejecutar pruebas/build antes de integrar; no aplicar automáticamente el salto mayor sugerido por `npm audit`.
2. Añadir `pip-audit` u otra SCA Python al CI, auditoría npm completa, SBOM y política de revisión de CVE/licencias.
3. Separar explícitamente perfiles demo y producción: secretos obligatorios desde un gestor, cuentas demo deshabilitadas, TLS forzado, puertos de base de datos/API no publicados y documentación API restringida donde corresponda.
4. Añadir cabeceras CSP, HSTS solo bajo HTTPS, `X-Content-Type-Options`, `Referrer-Policy` y ocultar la versión de Nginx; probar compatibilidad del frontend.
5. Fijar imágenes y acciones por versiones/digest revisados, habilitar actualización automatizada con revisión y verificar procedencia de artefactos.
6. Incorporar alertas sobre bloqueos, fallos de autenticación, 403 reiterados y errores 5xx; definir retención, acceso, correlación y procedimiento de respuesta.
7. Completar pruebas backend por endpoint, rol y objeto (incluidos IDOR, importación, WebSockets, seguimiento público y SSRF), además de expiración/revocación de sesión y límites de tasa.
8. Incorporar `iss`, `aud`, rotación/revocación de JWT y evitar tokens en query strings cuando la arquitectura permita un canal autenticado más seguro.

### Riesgos pendientes y límites

- Vulnerabilidades de dependencias Python: **no evaluadas** por falta de `pip-audit`/SCA.
- Autorización por objeto, SSRF, inyección y condiciones excepcionales: evidencia parcial, no evaluación exhaustiva.
- TLS, secretos, red Docker, logs, alertas y endurecimiento: evaluados solo en la composición local, no en staging/producción.
- No hubo DAST completo, fuzzing, pentest autenticado exhaustivo, revisión de infraestructura externa ni validación de procedencia de imágenes.
- Los findings de SonarQube son análisis estático: necesitan revisión contextual y no cubren por sí solos el OWASP Top 10.

**Resumen de los diez estados:** A01 Bajo revisión; A02 Vulnerable; A03 Vulnerable; A04 Bajo revisión; A05 Bajo revisión; A06 Bajo revisión; A07 Bajo revisión; A08 Bajo revisión; A09 Vulnerable; A10 Bajo revisión. Ninguna categoría queda declarada Limpio por insuficiencia de evidencia integral.
\n+[← Volver al README principal](../../../README.md)
