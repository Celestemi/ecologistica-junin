# Ajuste de dependencia de seguridad — AF-22

17/11/2026; main/b47d5eb + correcciones sin commit.

OSV detectó opentelemetry-api1.45.1, dependencia instalada de FastAPI0.162.0, afectada por GHSA-mf5v-w3w3-f6cg/CVE-2026-126360 (moderado5,3). ReDoS al extraer traceparent manipulado con salto de línea. No se encontró uso directo del propagador en app y no se explotó el servicio; presencia de versión afectada no prueba exposición.

Fuente primaria revisada: [aviso del mantenedor](https://github.com/open-telemetry/opentelemetry-python/security/advisories/GHSA-mf5v-w3w3-f6cg). [Distribución PyPI1.45.2](https://pypi.org/project/opentelemetry-api/1.45.2/) parcheada, mismo Requires-Dist typing-extensions>=4.5.0 que1.45.1, compatible con Python3.11. Wheel verificado por SHA2562cbd737377e710ee740d261c94e93fa0f08e6d037c18f17513cc0a2d94479a34.

Decisión previa a instalar: parche mínimo de UN paquete ya presente, 1.45.1→1.45.2, con --no-deps/--no-index desde wheel oficial verificado. No se introduce paquete instalado nuevo ni se actualiza el resto del entorno, no hay migración ni despliegue. Se fija mínimo1.45.2 en pyproject y backend/requirements para que un entorno nuevo no resuelva la versión afectada. Es una corrección no disruptiva autorizada por el plan; la aprobación específica se reserva a instalaciones disruptivas.

Salida SCA previa conservada en CORRECCIONES_EVIDENCIAS/python-osv-before.json. Salida posterior, comprobación de compatibilidad y pruebas quedan en control de fase3/fase5. No declarar reparado antes de repetir análisis y regresión. No se ocultan dependencias vulnerables mediante filtros/allowlist.

Resultado de instalación: primer intento uv con caché falló por acceso denegado al renombrar su directorio temporal, sin reemplazar el paquete. Segundo intento con --no-cache --link-mode copy y TEMP/TMP dentro de runtime controlado instaló únicamente1.45.2 (1 desinstalado/1 instalado, sin dependencias nuevas). No se cambió ninguna protección del sistema ni se usó elevación. Comprobación de compatibilidad y repetición de OSV/pruebas registradas en fases3/5; los límites de exposición siguen siendo los indicados por el mantenedor.
