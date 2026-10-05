# EcoLogística Huancayo

MVP de optimización de rutas de última milla para Huancayo, Perú. El backend corre un algoritmo genético VRPTW sobre PostgreSQL 15 con PostGIS. El panel del dispatcher muestra el mapa, el CO2 evitado y el equivalente en Quinuales del Valle del Mantaro.

El código está en inglés. Los comentarios, la semilla y la interfaz están en español.

## Contexto local

- Centro de operaciones: Plaza Constitución, `-12.06513, -75.20486`.
- Depósito semilla: Av. Ferrocarril, El Tambo, `-12.0520, -75.2120`, 3250 m s.n.m.
- Banda de altitud: 3200 m a 3450 m.
- Sostenibilidad: 1 Quinual abonado en la zona andina equivale a 12 kg de CO2 al año.
- Geometrías en WGS84 (EPSG:4326) para Leaflet.

## Requisitos

- Docker con Compose v2
- Para las pruebas en el host, además: Python 3.11 o superior

## Despliegue con Docker Compose

Desde la raíz del proyecto:

```powershell
docker compose up --build
```

Eso levanta tres servicios:

| Servicio | Imagen | Puerto en el host | Función |
| --- | --- | --- | --- |
| `db` | `postgis/postgis:15-3.4` | 5433 | PostgreSQL 15 + PostGIS, volumen `ecologistica_pgdata` |
| `backend` | FastAPI | 8000 | API y semilla |
| `frontend` | Nginx | 8080 | Panel del dispatcher |

El backend declara `depends_on` con `condition: service_healthy` sobre PostGIS. El contenedor, además, reintenta la conexión y solo entonces ejecuta `python -m app.db.init_db` (extensión PostGIS, tablas y semilla). La semilla es idempotente: si ya hay un depósito, no vuelve a insertar.

Cuando los healthchecks pasan:

- Panel: http://localhost:8080/
- API y Swagger: http://localhost:8000/docs
- Salud de PostGIS: http://localhost:8000/health/db

El panel sale en el **8080** para poder convivir con otro sitio que ya use el puerto 80. Nginx reenvía `/api/` al backend, así que el mapa usa el mismo origen.

Para dejarlo en segundo plano: `docker compose up --build -d`. Para detenerlo sin borrar los datos: `docker compose down`.

## Pruebas dentro del contenedor

Con la pila en marcha:

```powershell
docker compose exec backend pytest
```

`tests/test_solver.py` comprueba la penalización por pendiente y las ventanas de tiempo. `tests/test_api.py` llama a pedidos, vehículos y `POST /api/v1/optimizar-rutas` con el cliente asíncrono de HTTPX. Esas pruebas usan la base `ecologistica_test`, no la semilla que ve el panel.

En el host, contra el PostGIS publicado en el 5433:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

## Datos semilla

| Pieza | Referencia | Notas |
| --- | --- | --- |
| Depósito | Av. Ferrocarril, El Tambo | 3250 m |
| Furgón | Placa `W4U-158` | Diésel, 1500 kg, 220 g CO2/km, penalización 0.045 |
| Motocarro | Placa `E7M-304` | Eléctrico, 300 kg, 38 g CO2/km, penalización 0.012 |
| PED-001 | Plaza Constitución | 120 kg |
| PED-002 | Jr. Calixto, zona mayorista | 480 kg |
| PED-003 | UNCP, El Tambo | 85 kg |
| PED-004 | Chilca Alta | 40 kg, 3410 m |
| PED-005 | San Jerónimo de Tunán | 260 kg |

Los clientes y los pesos son ficticios. Las coordenadas corresponden a esos lugares.

## Emisión de un tramo en el optimizador

```
E = distancia_km × emision_base_g_km × (1 + penalizacion_pendiente × max(0, Δh / 100))
```

Δh es solo la subida, en metros. El tiempo de viaje usa 25 km/h. Llegar después de `ventana_fin`, superar `capacidad_kg` o meter un vehículo grande al Centro Histórico suma una penalización alta. El CO2 evitado se convierte a Quinuales con `co2_evitado_kg / 12`.

## Tiempo real

Dos canales WebSocket, además de la API REST:

- `ws://localhost:8000/ws/driver/{driver_id}` recibe la posición (`type: position`, con `lat`, `lon` y, si se conoce, `order_code`) y devuelve la ETA. También acepta `incident` (`traffic`, `landslide`, `blockade`), `cancel_order` y `add_order`.
- `ws://localhost:8000/ws/tracking/{order_code}` escucha la posición y la ETA de ese pedido. El código `despacho` recibe todos los eventos de la flota.

Un incidente bloqueante o un pedido cancelado o prioritario recalcula la secuencia que falta desde el GPS del conductor. El tráfico alarga el tramo; un deslizamiento o un cierre que cae sobre la parada la deja en estado `incident`.

## Seguimiento del cliente

`/seguimiento/PED-001` muestra el destino, la posición del repartidor cuando está en vivo, la hora de llegada, cuántas paradas van antes y el CO2 evitado de ese pedido. Si el ETA baja de 5 minutos, la página simula un aviso de WhatsApp o SMS en el navegador.

## Modo conductor

En el panel, el enlace **Modo conductor** abre `/conductor`. Esa vista lista las paradas de la ruta activa, abre Google Maps o Waze, toma la firma o una foto de la entrega y manda incidentes por `ws://<host>/ws/driver/{placa}`.

## Informe PDF

`GET /api/v1/reportes/sostenibilidad/pdf` devuelve el informe de sostenibilidad. Acepta `fecha_inicio` y `fecha_fin` (`YYYY-MM-DD`). Sin fechas, el rango cubre las soluciones guardadas. El archivo trae la huella de CO2, el TCO en soles por combustible y eléctrico, la equivalencia en Quinual y Aliso, y las entregas completadas.

## Esquema

- `depositos`: nombre, dirección, punto y altitud.
- `vehiculos`: placa, capacidades, combustible y factores de emisión.
- `pedidos`: cliente, punto, peso, ventana horaria y estado.
- `soluciones_ruta`: resultado del algoritmo genético, CO2 evitado y Quinuales.
- `rutas_detalle`: paradas ordenadas por vehículo, desnivel y geometría del tramo.
