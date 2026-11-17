# Fase 4 — Documentación y evidencia

17/11/2026 America/Lima; main/b47d5eb7cda26444c56460ea74591cc5f973e0b3 + cambios sin commit. Se releyó HTML completo §§1–5, SHA256098e994680f3a923a7b339a655ddf876a5b3ca712357884ef5c8697a4186a6a2, y siete documentos completos. Audiovisual EXCLUIDO TEMPORALMENTE — NO EVALUADO.

## Cambios autorizados y preservación

Siete documentos oficiales revisados en docs/04 Cierre, conservando nombres exactos y versión base1.0.0 con revisión técnica r1 e historial. Estado borrador explícito. Snapshot de bytes/base64/hash anterior: CORRECCIONES_EVIDENCIAS/docs_cierre_antes_r1.json; además versión previa en Git b47d5eb. Los cuatro informes finales originales no se editaron. No se modificaron originales históricos de docs/01 Inicio,02 Planificacion o03 Implementación ni capturas.

Se actualizaron logros,defectos/respuestas,variación de calidad,RAG/barras y lecciones analíticas con209 backend/70 frontend/4 SW,pruebas actuales y límites. El fallo de flota y los P0 corregidos dejaron de describirse como abiertos actuales; antecedentes rojos permanecen en sus fuentes. No se inventó una ceremonia que validara las lecciones.

README conserva sus siete enlaces,actualiza estado técnico y agrega enlaces a control/matriz/runbook/solicitudes. Se corrigió signo editorial del encabezado y hashes corruptos de D02/D04/D06 por61f0e1e9b0d71c1a0ea3c971fb77e93d0ea977b1, objeto commit comprobado y descrito como corte previo con B-08 sin commit, no como árbol actual.

## Validaciones actuales

- scripts/verify_closure_documents.py contra HTML original: **7/7 nombres/rutas presentes,160 comprobaciones textuales de estructura sin faltantes,0 marcadores,14/14 relaciones README↔documentos funcionales**, versión/historial presentes. Counts por documento25/18/32/18/20/25/22. Es presencia estructural, no160 obligaciones sustantivas cumplidas ni aceptación.
- El primer intento del verificador trataba “5.x Archivo” como contenido requerido; se corrigió el verificador en vez de alterar documentos para satisfacer un falso positivo.
- git diff --check pasa; avisos LF/CRLF no son errores.
- No se repiten suites por edición puramente documental; la fase5 verifica regresión final del árbol.
- Revisión de seguridad adicional: logger de desconexión incluía token público. Se amplió el caso existente de snapshot/cleanup para ejecutar la rama real de desconexión (IO doble+BD real), reproduciendo filtración sintética. Se eliminó token del logger de aplicación. **13 regresiones seguridad pasan** en fase4-log-verde; fuente WS modificada solo en ese log. Configuración/redacción de logs de proxy/Uvicorn en despliegue continúa pendiente AF-06. No se certifica todo el entorno.

## Datos y fuentes que siguen bloqueados

| Grupo | Resultado de revisión | Salida útil |
|---|---|---|
|EVM/cronograma/costos AF-04/16/17 |No datos aprobados nuevos;BAC/PV/EV/AC y tres cortes no calculables;no proyección EAC aplicada |SOLICITUD_DATOS_EVM.md con campos,roles propuestos,fuentes,periodos/soportes y hoja prospectiva |
|Aceptación/satisfacción/retro/transición AF-05/20/34 |Sin registros reales;no se firman actas ni encuestas |SOLICITUD_EVIDENCIAS_HUMANAS.md con formularios prospectivos |
|Gráficos AF-18/19/20/27 |Sin series auténticas;solo barras de pruebas reproducibles actualizadas |No se dibujaron EVM/CFD/CSI/Burndown/Burnup/Mood ficticios;solicitud de exportación Jira |
|Historia AF-26/27/28/33 |31 ocurrencias/séis destinos anteriores ausentes;sin correspondencia inequívoca ni original inicial |FUENTES_HISTORICAS_IRRESOLUBLES.md;no redirigir actas antiguas a tests nuevos |
|Metodología/alcance/privacidad/BD AF-08/09/11/12/13/14/15 |Faltan decisiones/factores/esquema/políticas y autorización de BD existente |Tabla concreta en solicitud humana;no exención ni cambio tácito |
|Demostración/WCAG AF-21/25/35 |Herramienta de navegador sin host/pipe;sin ensayo real10min |Guía con intervalos **propuestos**,no observados |

No usar USD134400/PEN499968 estimados como BAC aprobado;su aritmética correcta no se convirtió en ejecución. Las fórmulas EVM se preservan sin rellenar resultados. La corrección de código no reemplaza aceptación/hitos/horas reales.

## Salida y archivos

Modificados: siete archivos exactos de docs/04 Cierre y README; nuevo verificador en scripts. Nuevos informes: este archivo,SOLICITUD_DATOS_EVM.md,SOLICITUD_EVIDENCIAS_HUMANAS.md,FUENTES_HISTORICAS_IRRESOLUBLES.md; snapshot/validación JSON en AUDITORIA. Corrección adicional documentada: websockets.py y caso de seguridad existente,sin nuevo contrato ni dependencia.

AF-32 corregido con fuente comprobada; AF-26 sigue abierto hasta recuperar fuentes; AF-28 parcial. Los bloqueos económicos/humanos son individuales y explícitos. Se continúa fase5: relectura independiente por AF/H,regresión final,integridad y reauditoría,sin nota inventada ni cierre definitivo.
