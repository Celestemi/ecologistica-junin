# Ámbito geográfico de operación (RF-005)

Este repositorio **no incluye** límites distritales oficiales de Huancayo, El Tambo y Chilca.

El archivo `operating_area_dev.geojson` es un **sobre operativo provisional** para desarrollo y pruebas automatizadas. Cubre los puntos de la semilla del MVP (centro de Huancayo, El Tambo, Chilca) y debe **reemplazarse** por un GeoJSON con fuente verificable (ordenanza municipal, catastro o extracto OSM documentado) antes de usar el filtro en producción.

Configure `OPERATING_AREA_GEOJSON_PATH` en el entorno para apuntar al archivo validado por el equipo.
