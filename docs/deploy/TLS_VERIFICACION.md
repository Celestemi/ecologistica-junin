# Verificación de HTTPS / TLS (EN-003 / RNF-003)

## Objetivo

Garantizar que el tráfico sensible (JWT, datos de clientes y coordenadas) viaje cifrado en despliegues expuestos a red.

## Configuración

1. Variables de entorno del backend:
   - `FORCE_HTTPS=true` — activa redirección 308 HTTP→HTTPS cuando el proxy no marca `X-Forwarded-Proto: https`.
   - `APP_ENVIRONMENT=production` — exige `SECRET_KEY` fuerte y deshabilita cuentas demo.
2. Certificados TLS en el proxy (nginx). Plantilla en `frontend/nginx-ssl.conf.example`.

## Pasos de verificación real

1. Desplegar con nginx escuchando **443** y certificado válido (Let's Encrypt o CA interna).
2. Comprobar redirección:
   ```bash
   curl -I http://tu-dominio/api/v1/auth/ingresar
   ```
   Debe responder **308** hacia `https://...` cuando `FORCE_HTTPS=true`.
3. Comprobar TLS:
   ```bash
   curl -I https://tu-dominio/health
   openssl s_client -connect tu-dominio:443 -tls1_3 </dev/null 2>/dev/null | head
   ```
4. Verificar que el frontend y las WebSockets usen `https` / `wss` (sin contenido mixto en el navegador).
5. Revisar que `SECRET_KEY` no sea la clave por defecto del repositorio.

## Desarrollo local

- `FORCE_HTTPS=false` (predeterminado) permite HTTP en `localhost` / Docker.
- Para pruebas TLS locales: mkcert + nginx con `nginx-ssl.conf.example`.
