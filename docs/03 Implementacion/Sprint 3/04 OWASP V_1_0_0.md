# Reporte de Seguridad OWASP Top 10 (2025)

**Nombre del Proyecto:** EcoLogística Huancayo  
**Herramienta de Escaneo:** SonarQube Community Build 26.10.0.133078 local mediante Docker Desktop

## 1. Matriz de Cumplimiento OWASP Top 10 2025

| Categoría OWASP 2025 | Estado en Proyecto (Limpio / Vulnerable / Bajo Revisión) | Hallazgos de SonarQube |
|---|---|---|
| A01:2025-Broken Access Control | Bajo Revisión — existen `get_current_user` y `require_roles` en `app/api/deps.py`, pero no se ejecutó una prueba integral de autorización por objeto. | Sin regla SonarQube específica identificada en este análisis. |
| A02:2025-Cryptographic Failures | Bajo Revisión — la fila se conserva por la plantilla; la categoría oficial equivalente es A04:2025. | 9 vulnerabilidades mayores `python:S2245` por aleatoriedad no criptográfica en benchmark/algoritmo; requieren clasificación de contexto. |
| A03:2025-Injection | Bajo Revisión — la fila se conserva por la plantilla; la categoría oficial equivalente es A05:2025. | Sin hallazgos específicos; la ausencia de regla disparada no acredita ausencia de inyección. |
| A04:2025-Insecure Design | Bajo Revisión — la fila se conserva por la plantilla; la categoría oficial equivalente es A06:2025. | Sin hallazgos específicos; falta modelado de amenazas. |
| A05:2025-Security Misconfiguration | Bajo Revisión — la fila se conserva por la plantilla; la categoría oficial equivalente es A02:2025. | 1 vulnerabilidad menor `python:S5332` en `app/core/config.py:35` por orígenes HTTP locales; verificar que no persistan en producción. |
| A06:2025-Vulnerable and Outdated Components | Bajo Revisión — la plantilla no coincide con la categoría oficial A03:2025 (Software Supply Chain Failures). | El análisis SCA de SonarQube fue omitido. `npm audit --omit=dev` no encontró vulnerabilidades frontend y `pip check` pasó, evidencia insuficiente para marcar Limpio. |
| A07:2025-Identification and Authentication Failures | Bajo Revisión — la denominación oficial es Authentication Failures. | Sin hallazgos específicos; se revisaron JWT, bloqueo por intentos y roles, pero faltan pruebas exhaustivas de sesión. |
| A08:2025-Software and Data Integrity Failures | Bajo Revisión — existen archivos de bloqueo y CI, sin validación completa de procedencia de artefactos. | Sin hallazgos específicos. |
| A09:2025-Security Logging and Monitoring Failures | Bajo Revisión — existe bitácora de acceso, pero no se verificaron alertas, retención ni monitorización desplegada. | Sin hallazgos específicos. |
| A10:2025-Server-Side Request Forgery (SSRF) | Bajo Revisión — la fila se conserva por la plantilla; en OWASP 2025 A10 es Mishandling of Exceptional Conditions. | Sin hallazgos de SSRF; `osrm_base_url` procede de configuración y requiere prueba de despliegue. |

La plantilla entregada conserva nomenclatura de OWASP Top 10 2021. La publicación oficial de 2025 ordena las categorías como A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures y A10 Mishandling of Exceptional Conditions. Se preservaron las diez filas solicitadas y se dejó trazabilidad de cada diferencia. Fuente: [OWASP Top 10:2025](https://top10.owasp.org/).

## 2. Detalles de Security Hotspots y Vulnerabilidades Críticas

- **Security Hotspots:** SonarQube detectó 0 hotspots en el análisis final.
- **Vulnerabilidades críticas:** No se reportaron vulnerabilidades de severidad bloqueante ni crítica. Se reportaron 9 mayores (`python:S2245`) y 1 menor (`python:S5332`). Las nueve mayores se localizan en `app/services/optimizer_benchmark.py` (líneas 41, 42, 44, 64, 65, 78 y 103) y `app/services/genetic_solver.py` (líneas 504 y 506); su uso de aleatoriedad es reproducible/no criptográfico según la revisión de código, pero deben revisarse y clasificarse explícitamente antes del cierre.
- **Hallazgos prioritarios no estrictamente de seguridad:** SonarQube reportó tres bugs críticos de ordenamiento sin comparador (`src/components/Map.tsx:83`, `src/pages/PlateRestrictions.tsx:120`, `src/components/Sidebar.tsx:178`) y un bug bloqueante de tipo en `app/main.py:68`, contrastado con una ejecución correcta de FastAPI y 118 pruebas aprobadas. No se aplicaron correcciones funcionales durante esta revisión.
- **Intervención requerida:** revisar y resolver/clasificar las vulnerabilidades `S2245`, restringir orígenes HTTP al entorno local y verificar TLS en staging/producción; completar SCA de dependencias y pruebas de autorización, sesión, SSRF y monitorización. SonarQube no reemplaza una evaluación integral de seguridad.
